import streamlit as st

st.title("🎈 하이 하이 ")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st

st.set_page_config(page_title="현재 상영작 안내", page_icon="🍿", layout="wide")

st.title("🍿 현재 상영중인 영화")
st.markdown("현재 극장에서 상영 중인 인기 영화들을 확인해보세요!")

# 현재 상영중인 영화 임시 데이터(Mock Data)
movies = [
    {
        "title": "파묘 (Exhuma)",
        "genre": "미스터리, 공포",
        "rating": "⭐ 8.2/10",
        "image": "https://image.tmdb.org/t/p/w500/1XDDXPXGiI8id7MrUxK36ke7wow.jpg",
        "description": "미국 LA, 거액의 의뢰를 받은 무당 화림과 봉길은 기이한 병이 대물림되는 집안의 장손을 만난다..."
    },
    {
        "title": "듄: 파트 2 (Dune: Part Two)",
        "genre": "액션, SF",
        "rating": "⭐ 8.8/10",
        "image": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2JGjjcNsV.jpg",
        "description": "황제의 모략으로 멸문한 가문의 유일한 후계자 폴. 어머니 레이디 제시카와 간신히 목숨을 부지한 채..."
    },
    {
        "title": "가여운 것들 (Poor Things)",
        "genre": "코미디, SF",
        "rating": "⭐ 8.5/10",
        "image": "https://image.tmdb.org/t/p/w500/kCGlIMHnOm8Phlozz52T1oXfXyq.jpg",
        "description": "천재적인 과학자 고드윈 박사에 의해 새로운 삶을 부여받은 벨라 백스터의 놀라운 여정..."
    },
    {
        "title": "웡카 (Wonka)",
        "genre": "가족, 팬타지, 코미디",
        "rating": "⭐ 7.9/10",
        "image": "https://image.tmdb.org/t/p/w500/qhb1qOilapbapxWQn9jtRCMwXJF.jpg",
        "description": "마법사이자 초콜릿 메이커 윌리 웡카가 디저트의 성지 달콤 백화점 입성을 향한 여정을 다룬 영화."
    }
]

st.divider()

# 영화 목록을 4열 그리드로 표시
cols = st.columns(4)

for i, movie in enumerate(movies):
    col = cols[i % 4]
    with col:
        # st.image가 제대로 출력되도록 외부 이미지 링크 사용
        st.image(movie["image"], use_container_width=True)
        st.subheader(movie["title"])
        st.caption(f"**장르:** {movie['genre']} | **평점:** {movie['rating']}")
        st.write(movie["description"])
        
        # 버튼 추가해보기
        if st.button("예매하기", key=f"btn_ticket_{i}", use_container_width=True):
            st.success(f"'{movie['title']}' 예매 페이지로 이동합니다!")

st.divider()
st.markdown("© 2026 Movie Homepage Example. Built with Streamlit.")
