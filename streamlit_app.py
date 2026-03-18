import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pathlib

st.set_page_config(page_title="🌬️ 2025년 1월 대기질 대시보드", page_icon="🌬️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background: #0f172a; }
.metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    margin: 4px 0;
}
.grade-good    { color: #22c55e; font-weight: 900; font-size: 20px; }
.grade-normal  { color: #3b82f6; font-weight: 900; font-size: 20px; }
.grade-bad     { color: #f97316; font-weight: 900; font-size: 20px; }
.grade-verybad { color: #ef4444; font-weight: 900; font-size: 20px; }
h1, h2, h3 { color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

# ─── 데이터 로드 ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = pathlib.Path(__file__).parent / "202501-air.csv"
    if not path.exists():
        return None
    # 인코딩: cp949(한국 윈도우) → 실패 시 utf-8 fallback
    for enc in ["cp949", "utf-8", "euc-kr"]:
        try:
            df = pd.read_csv(path, encoding=enc)
            break
        except (UnicodeDecodeError, Exception):
            continue
    else:
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

df = load_data()

if df is None:
    st.error("⚠️ **데이터 파일을 찾을 수 없습니다.**")
    st.info("`202501-air.csv` 파일이 `app.py`와 같은 폴더에 있어야 합니다.\n\nGit 저장소에 CSV 파일도 함께 올려주세요.")
    st.stop()

# ─── 헤더 ────────────────────────────────────────────────────────────────────
st.title("🌬️ 2025년 1월 전국 대기질 대시보드")
st.caption(f"측정소: {df['측정소명'].nunique()}개 | 지역: {df['시도'].nunique()}개 시도 | 총 {len(df):,}건 데이터")

# ─── 사이드바 필터 ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 필터")
    all_regions = sorted(df["시도"].unique())
    sel_region = st.multiselect("시도 선택", all_regions, default=all_regions[:5])
    all_stations = sorted(df[df["시도"].isin(sel_region)]["측정소명"].unique()) if sel_region else sorted(df["측정소명"].unique())
    sel_station = st.multiselect("측정소 선택 (선택 안하면 전체)", all_stations)
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

# ─── PM10 등급 판정 함수 ─────────────────────────────────────────────────────
def pm10_grade(v):
    if pd.isna(v): return "알수없음"
    if v <= 30: return "좋음"
    if v <= 80: return "보통"
    if v <= 150: return "나쁨"
    return "매우나쁨"

# ─── 주요 지표 카드 ──────────────────────────────────────────────────────────
st.subheader("📊 1월 전체 평균 요약")
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
            <div style="color:#94a3b8;font-size:12px">{label}</div>
            <div style="color:#f1f5f9;font-size:24px;font-weight:900">{val:.3g}</div>
            <div class="{grade_cls}">{grade_txt}</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# ─── 탭 레이아웃 ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 시간대별 추이", "🗺️ 지역별 비교", "🌡️ 오염물질 분포", "📅 날짜별 히트맵"])

# ── TAB 1: 시간별 추이 ──────────────────────────────────────────────────────
with tab1:
    st.subheader(f"📈 선택 지역 · {sel_pollutant} 일별 평균 추이")

    daily = fdf.groupby(["월일","시도"])[sel_pollutant].mean().reset_index()
    fig = px.line(
        daily, x="월일", y=sel_pollutant, color="시도",
        markers=True, template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        labels={"월일":"날짜","시도":"시도"},
    )
    fig.update_layout(
        plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
        font_color="#f1f5f9", legend=dict(bgcolor="#1e293b"),
        xaxis=dict(gridcolor="#334155"), yaxis=dict(gridcolor="#334155"),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("⏰ 시간대별 평균 (시도별)")
    hourly = fdf.groupby(["시간","시도"])[sel_pollutant].mean().reset_index()
    fig2 = px.line(
        hourly, x="시간", y=sel_pollutant, color="시도",
        markers=True, template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={"시간":"시간(0~23)"},
    )
    fig2.update_layout(
        plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
        font_color="#f1f5f9", height=380,
        xaxis=dict(gridcolor="#334155", dtick=1),
        yaxis=dict(gridcolor="#334155"),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── TAB 2: 지역별 비교 ──────────────────────────────────────────────────────
with tab2:
    st.subheader("🗺️ 시도별 오염물질 평균 비교")

    region_avg = fdf.groupby("시도")[["PM10","PM25","NO2","CO","O3","SO2"]].mean().reset_index()
    region_avg_melt = region_avg.melt(id_vars="시도", var_name="오염물질", value_name="평균값")

    fig3 = px.bar(
        region_avg_melt[region_avg_melt["오염물질"].isin(["PM10","PM25"])],
        x="시도", y="평균값", color="오염물질", barmode="group",
        template="plotly_dark",
        color_discrete_map={"PM10":"#f97316","PM25":"#ef4444"},
        labels={"평균값":"평균 농도 (μg/m³)"},
    )
    fig3.update_layout(
        plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
        font_color="#f1f5f9", height=400,
        xaxis=dict(gridcolor="#334155"), yaxis=dict(gridcolor="#334155"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📊 측정소별 PM10 상위/하위 현황")
    station_pm10 = fdf.groupby("측정소명")["PM10"].mean().dropna().reset_index()
    station_pm10 = station_pm10.sort_values("PM10", ascending=False)
    top10 = station_pm10.head(10)
    bot10 = station_pm10.tail(10)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**😷 PM10 평균 높은 측정소 TOP 10**")
        fig4 = px.bar(top10, x="PM10", y="측정소명", orientation="h",
                      template="plotly_dark", color="PM10",
                      color_continuous_scale="Reds")
        fig4.update_layout(plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
                           font_color="#f1f5f9", height=360, showlegend=False,
                           yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig4, use_container_width=True)
    with c2:
        st.markdown("**😊 PM10 평균 낮은 측정소 TOP 10**")
        fig5 = px.bar(bot10, x="PM10", y="측정소명", orientation="h",
                      template="plotly_dark", color="PM10",
                      color_continuous_scale="Greens")
        fig5.update_layout(plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
                           font_color="#f1f5f9", height=360, showlegend=False,
                           yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig5, use_container_width=True)

# ── TAB 3: 오염물질 분포 ────────────────────────────────────────────────────
with tab3:
    st.subheader("🌡️ 오염물질 상관관계 & 분포")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{sel_pollutant} 분포 히스토그램**")
        fig6 = px.histogram(fdf, x=sel_pollutant, nbins=60, template="plotly_dark",
                            color_discrete_sequence=["#3b82f6"],
                            labels={sel_pollutant:f"{sel_pollutant} 농도"})
        fig6.update_layout(plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
                           font_color="#f1f5f9", height=360,
                           bargap=0.05,
                           xaxis=dict(gridcolor="#334155"),
                           yaxis=dict(gridcolor="#334155"))
        st.plotly_chart(fig6, use_container_width=True)

    with c2:
        st.markdown("**PM10 vs PM2.5 산점도**")
        sample = fdf[["PM10","PM25","시도"]].dropna().sample(min(3000, len(fdf)), random_state=42)
        fig7 = px.scatter(sample, x="PM10", y="PM25", color="시도",
                          opacity=0.6, template="plotly_dark",
                          color_discrete_sequence=px.colors.qualitative.Vivid)
        fig7.update_layout(plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
                           font_color="#f1f5f9", height=360,
                           xaxis=dict(gridcolor="#334155"),
                           yaxis=dict(gridcolor="#334155"))
        st.plotly_chart(fig7, use_container_width=True)

    st.subheader("🕸️ 오염물질 간 상관계수 히트맵")
    corr = fdf[["SO2","CO","O3","NO2","PM10","PM25"]].corr()
    fig8 = px.imshow(corr, text_auto=".2f", template="plotly_dark",
                     color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                     labels=dict(color="상관계수"))
    fig8.update_layout(plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
                       font_color="#f1f5f9", height=420)
    st.plotly_chart(fig8, use_container_width=True)

# ── TAB 4: 날짜별 히트맵 ────────────────────────────────────────────────────
with tab4:
    st.subheader(f"📅 날짜 × 시간대 {sel_pollutant} 히트맵 (선택 지역 평균)")

    pivot = fdf.groupby(["월일","시간"])[sel_pollutant].mean().unstack(level=1)
    fig9 = px.imshow(
        pivot, template="plotly_dark",
        color_continuous_scale="YlOrRd",
        labels=dict(x="시간(0~23)", y="날짜", color=sel_pollutant),
        aspect="auto",
    )
    fig9.update_layout(plot_bgcolor="#1e293b", paper_bgcolor="#0f172a",
                       font_color="#f1f5f9", height=600)
    st.plotly_chart(fig9, use_container_width=True)

    st.subheader(f"🏆 {sel_pollutant} 최악의 날 TOP 5")
    worst_days = fdf.groupby("월일")[sel_pollutant].mean().nlargest(5).reset_index()
    worst_days.columns = ["날짜", f"평균 {sel_pollutant}"]
    worst_days[f"평균 {sel_pollutant}"] = worst_days[f"평균 {sel_pollutant}"].round(2)
    st.dataframe(worst_days, use_container_width=True, hide_index=True)
