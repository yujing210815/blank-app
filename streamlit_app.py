import streamlit as st
import pandas as pd
import pathlib
import os

st.set_page_config(page_title="🌬️ 2025년 1월 대기질 대시보드", page_icon="🌬️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.metric-card {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    margin-bottom: 10px;
}
.metric-title { font-size: 14px; color: #6c757d; }
.metric-value { font-size: 24px; font-weight: bold; color: #212529; }
.grade-good { color: #198754; font-weight: bold; }
.grade-normal { color: #0d6efd; font-weight: bold; }
.grade-bad { color: #fd7e14; font-weight: bold; }
.grade-verybad { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ─── 데이터 로드 ────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file_source):
    # file_source는 경로(str)이거나 업로드된 파일 객체입니다.
    # 인코딩: cp949 → fallback utf-8
    df = None
    for enc in ["cp949", "utf-8", "euc-kr"]:
        try:
            if isinstance(file_source, str) or isinstance(file_source, pathlib.Path):
                df = pd.read_csv(file_source, encoding=enc)
            else:
                file_source.seek(0) # 업로드 파일인 경우 포인터 초기화
                df = pd.read_csv(file_source, encoding=enc)
            break
        except Exception:
            continue
            
    if df is None:
        return None
        
    df.columns = ["지역","망","측정소코드","측정소명","측정일시","SO2","CO","O3","NO2","PM10","PM25","주소"]
    df["측정일시"] = pd.to_datetime(df["측정일시"].astype(str), format="%Y%m%d%H", errors="coerce")
    df = df.dropna(subset=["측정일시"])
    df["날짜"] = df["측정일시"].dt.date
    df["시간"] = df["측정일시"].dt.hour
    df["월일"] = df["측정일시"].dt.strftime("%m-%d")
    df["시도"] = df["지역"].str.split().str[0]
    
    for col in ["SO2","CO","O3","NO2","PM10","PM25"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

# 파일이 같은 경로에 있는지 확인
local_path = pathlib.Path(__file__).parent / "202501-air.csv"
df = None

if local_path.exists():
    df = load_data(local_path)
else:
    st.warning("⚠️ **GitHub(또는 서버)에 `202501-air.csv` 파일이 없습니다.** 화면에서 직접 파일을 업로드해주세요.")
    uploaded_file = st.file_uploader("202501-air.csv 파일 업로드", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        st.stop()

if df is None:
    st.error("데이터 파일을 읽는 중 오류가 발생했습니다. 파일 형식을 다시 확인해주세요.")
    st.stop()

# ─── 헤더 ────────────────────────────────────────────────────────────────────
st.title("🌬️ 2025년 1월 전국 대기질 대시보드")
st.caption(f"측정소: {df['측정소명'].nunique()}개 | 지역: {df['시도'].nunique()}개 시도 | 총 {len(df):,}건 데이터")

# ─── 사이드바 필터 ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 필터")
    all_regions = sorted(df["시도"].unique())
    sel_region = st.multiselect("시도 선택", all_regions, default=all_regions[:3])
    
    # 측정소는 선택한 시도에 따라 필터링
    if sel_region:
        all_stations = sorted(df[df["시도"].isin(sel_region)]["측정소명"].unique())
    else:
        all_stations = sorted(df["측정소명"].unique())
        
    sel_station = st.multiselect("측정소 선택 (선택 안하면 해당 시도 전체)", all_stations)
    sel_pollutant = st.selectbox("오염물질 선택", ["PM10","PM25","NO2","CO","O3","SO2"])

    st.markdown("---")
    st.markdown("""
    **대기질 등급 기준 (PM10 μg/m³)**
    - 🟢 좋음: 0~30
    - 🔵 보통: 31~80
    - 🟠 나쁨: 81~150
    - 🔴 매우나쁨: 151+
    """)

# 필터 적용
fdf = df[df["시도"].isin(sel_region)] if sel_region else df
if sel_station:
    fdf = fdf[fdf["측정소명"].isin(sel_station)]

if len(fdf) == 0:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
    st.stop()

# ─── 주요 지표 카드 ──────────────────────────────────────────────────────────
st.subheader("📊 선택 조건 평균 요약")
cols = st.columns(6)
metrics = {
    "PM10 (μg/m³)": ("PM10", 30, 80, 150),
    "PM2.5 (μg/m³)": ("PM25", 15, 35, 75),
    "NO₂ (ppm)": ("NO2", 0.03, 0.06, 0.1),
    "CO (ppm)": ("CO", 0.5, 1.0, 2.0),
    "O₃ (ppm)": ("O3", 0.03, 0.06, 0.1),
    "SO₂ (ppm)": ("SO2", 0.02, 0.05, 0.1),
}
for col, (label, (col_name, t1, t2, t3)) in zip(cols, metrics.items()):
    val = fdf[col_name].mean()
    if pd.isna(val):
        grade_cls, grade_txt = "grade-normal", "-"
    elif val <= t1:
        grade_cls, grade_txt = "grade-good", "좋음"
    elif val <= t2:
        grade_cls, grade_txt = "grade-normal", "보통"
    elif val <= t3:
        grade_cls, grade_txt = "grade-bad", "나쁨"
    else:
        grade_cls, grade_txt = "grade-verybad", "매우나쁨"
        
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{label}</div>
            <div class="metric-value">{val:.3g}</div>
            <div class="{grade_cls}">{grade_txt}</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# ─── 탭 레이아웃 ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈 시간/일자별 추이", "🗺️ 지역/측정소별 현황", "🌡️ 오염물질 데이터 분포"])

# ── TAB 1: 추이 ──────────────────────────────────────────────────────
with tab1:
    st.subheader(f"📅 일별 {sel_pollutant} 평균 추이")
    # 시도명 컬럼으로 피벗하여 line_chart용 데이터프레임 만들기
    daily = fdf.groupby(["날짜", "시도"])[sel_pollutant].mean().unstack(level=1)
    st.line_chart(daily)

    st.subheader(f"⏰ 시간대별(0~23시) {sel_pollutant} 평균")
    hourly = fdf.groupby(["시간", "시도"])[sel_pollutant].mean().unstack(level=1)
    st.line_chart(hourly)

# ── TAB 2: 현황 ──────────────────────────────────────────────────────
with tab2:
    st.subheader("🗺️ 시도별 오염물질 평균 비교")
    region_avg = fdf.groupby("시도")[["PM10", "PM25"]].mean()
    st.bar_chart(region_avg)

    st.subheader(f"🏆 {sel_pollutant} 농도 상위 측정소 (선택 지역 내)")
    station_avg = fdf.groupby("측정소명")[sel_pollutant].mean().dropna().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**가장 안 좋았던 곳 (상위 10개)**")
        st.dataframe(station_avg.head(10), use_container_width=True)
    with col2:
        st.markdown("**가장 좋았던 곳 (하위 10개)**")
        st.dataframe(station_avg.tail(10).sort_values(ascending=True), use_container_width=True)

# ── TAB 3: 분포 ────────────────────────────────────────────────────
with tab3:
    st.subheader("💨 미세먼지(PM10) vs 초미세먼지(PM2.5) 관계")
    # scatter_chart를 사용하기 위해 데이터 준비 (Streamlit 내장)
    scatter_df = fdf[["PM10", "PM25", "시도"]].dropna()
    if len(scatter_df) > 2000:
        scatter_df = scatter_df.sample(2000) # 브라우저 성능을 위해 샘플링
    
    st.scatter_chart(
        data=scatter_df,
        x="PM10",
        y="PM25",
        color="시도"
    )

    st.subheader(f"💡 데이터 요약 (상위 100건)")
    st.dataframe(fdf.head(100), use_container_width=True)
