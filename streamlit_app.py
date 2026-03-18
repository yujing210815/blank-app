import streamlit as st

st.set_page_config(page_title="알아두면 쓸데있는 신비한 상식사전", page_icon="💡", layout="centered")

# CSS로 UI 꾸미기
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        background-color: white;
        color: #4CAF50;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4CAF50;
        color: white;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    .score-text {
        font-size: 24px;
        font-weight: bold;
        color: #FF9800;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("💡 알쓸신상 퀴즈룸")
st.markdown("하루에 하나씩! 몰라도 살아가는데 지장 없지만 **알면 왠지 똑똑해 보이는 상식 퀴즈**를 풀어보세요.")

# 퀴즈 데이터셋
quiz_data = [
    {
        "question": "다음 중 가장 먼저 만들어진 패스트푸드 프랜차이즈는 무엇일까요?",
        "options": ["맥도날드", "버거킹", "A&W 레스토랑"],
        "answer": "A&W 레스토랑",
        "explanation": "A&W는 1919년에 루트비어 스탠드로 시작하여 1923년에 첫 번째 프랜차이즈 드라이브인 레스토랑을 열었습니다. 맥도날드는 1940년에 시작되었습니다."
    },
    {
        "question": "다음 중 딸기는 과연 어떤 부위를 먹는 것일까요?",
        "options": ["열매", "꽃받침", "씨앗"],
        "answer": "꽃받침",
        "explanation": "우리가 먹는 붉고 달콤한 딸기의 부위는 사실 열매가 아니라 꽃받침(화탁)이 부풀어 오른 것입니다. 진짜 열매는 겉에 씨앗처럼 콕콕 박혀있는 작은 알갱이들입니다."
    },
    {
        "question": "세계에서 가장 많이 팔린 게임은 무엇일까요? (2024년 기준)",
        "options": ["마인크래프트", "테트리스", "GTA 5"],
        "answer": "마인크래프트",
        "explanation": "마인크래프트(Minecraft)는 전 세계적으로 3억 장 이상 판매되어 역사상 가장 많이 팔린 비디오 게임 1위를 기록하고 있습니다."
    },
    {
        "question": "낙타의 혹에는 무엇이 들어있을까요?",
        "options": ["물", "지방", "근육"],
        "answer": "지방",
        "explanation": "낙타의 혹은 물주머니가 아니라 '지방'을 저장하는 곳입니다. 사막에서 먹이를 구하기 힘들 때 이 지방을 분해하여 에너지원과 수분으로 사용합니다."
    },
    {
        "question": "다음 중 대한민국의 천연기념물 제1호는 무엇일까요?",
        "options": ["진도의 진돗개", "대구 도동 측백나무 숲", "팔만대장경"],
        "answer": "대구 도동 측백나무 숲",
        "explanation": "대한민국의 천연기념물 제1호는 대구광역시 동구 도동에 위치한 수림지인 '대구 도동 측백나무 숲'입니다."
    }
]

# 세션 상태 초기화
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_answered" not in st.session_state:
    st.session_state.is_answered = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

# 현재 퀴즈 정보
q_idx = st.session_state.current_q
total_q = len(quiz_data)

if q_idx < total_q:
    q_data = quiz_data[q_idx]

    # 진행률 표시
    st.progress(q_idx / total_q, text=f"진행 상황: {q_idx + 1} / {total_q} 문제")

    # 질문 표시
    st.markdown(f"""
        <div class='question-box'>
            <h3>Q{q_idx + 1}. {q_data['question']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # 선택지 (이미 답을 고른 경우 비활성화 또는 표시 변경)
    if not st.session_state.is_answered:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, option in enumerate(q_data["options"]):
            with cols[i]:
                if st.button(option, key=f"btn_{q_idx}_{i}"):
                    st.session_state.is_answered = True
                    st.session_state.user_choice = option
                    # 정답 체크
                    if option == q_data["answer"]:
                        st.session_state.score += 1
                    st.rerun()
    else:
        # 문제 풀이 결과 및 해설 표시영역
        st.write("---")
        if st.session_state.user_choice == q_data["answer"]:
            st.success("🎉 정답입니다!")
        else:
            st.error(f"❌ 오답입니다. (내가 고른 답: {st.session_state.user_choice})")
        
        st.info(f"👉 **정답: {q_data['answer']}**\n\n💡 **해설:** {q_data['explanation']}")
        
        st.write("")
        # 다음 문제로 넘어가기 버튼
        if st.button("다음 문제로 ⏭️", type="primary"):
            st.session_state.current_q += 1
            st.session_state.is_answered = False
            st.session_state.user_choice = None
            st.rerun()

else:
    # 모든 문제를 다 풀었을 때의 결과 화면
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>🎊 퀴즈 종료! 🎊</h2>", unsafe_allow_html=True)
    
    st.markdown(f"<p class='score-text'>최종 점수: {st.session_state.score} / {total_q} 점</p>", unsafe_allow_html=True)
    
    # 점수에 따른 메시지
    score_ratio = st.session_state.score / total_q
    if score_ratio == 1.0:
        st.success("완벽합니다! 걸어다니는 백과사전이시군요! 📚")
    elif score_ratio >= 0.6:
        st.info("훌륭합니다! 상식이 아주 풍부하시네요! 🤓")
    else:
        st.warning("아깝네요! 하지만 오늘 새로운 지식을 많이 얻어가셨으니 성공입니다! 💪")
        
    st.write("---")
    if st.button("처음부터 다시 도전하기 🔄", use_container_width=True):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.is_answered = False
        st.session_state.user_choice = None
        st.rerun()
