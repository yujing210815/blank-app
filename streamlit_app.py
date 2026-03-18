import streamlit as st
import time

st.set_page_config(page_title="알아두면 쓸데있는 신비한 상식사전", page_icon="💡", layout="centered")

# 레트로 다마고치 감성 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DungGeunMo&display=swap');
    
    body {
        font-family: 'DungGeunMo', 'Press Start 2P', cursive;
        background-color: #f7f7f7;
    }
    .stApp {
        background-color: #fce3e3;
    }
    .tamagotchi-screen {
        background-color: #9cbca4; /* 옛날 게임보이/다마고치 액정 색상 */
        border: 15px solid #d3d3d3;
        border-radius: 20px;
        padding: 20px;
        box-shadow: inset 5px 5px 15px rgba(0,0,0,0.2), 10px 10px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        font-family: 'DungGeunMo', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: 4px solid #333;
        background-color: #ffd166;
        color: #333;
        font-weight: bold;
        font-size: 18px;
        font-family: 'DungGeunMo', sans-serif;
        box-shadow: 3px 3px 0px #333;
        transition: all 0.1s;
    }
    .stButton>button:active {
        box-shadow: 0px 0px 0px #333;
        transform: translate(3px, 3px);
    }
    .tamagotchi-character {
        font-size: 80px;
        margin: 10px 0;
        animation: float 2s infinite ease-in-out;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .question-image {
        max-width: 100%;
        border: 4px solid #333;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .score-text {
        font-size: 24px;
        font-weight: bold;
        color: #ff5252;
        text-align: center;
        text-shadow: 2px 2px 0px #333;
    }
    h1, h2, h3, p, span {
        font-family: 'DungGeunMo', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📟 알쓸신상 다마고치 퀴즈")

# 퀴즈 데이터셋 (이미지 URL 및 문제 추가)
quiz_data = [
    {
        "question": "다음 중 가장 먼저 만들어진 패스트푸드 프랜차이즈는 무엇일까요?",
        "options": ["맥도날드", "버거킹", "A&W 레스토랑"],
        "answer": "A&W 레스토랑",
        "explanation": "A&W는 1919년에 시작하여 1923년에 드라이브인 레스토랑을 열었습니다. 맥도날드는 1940년입니다.",
        "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" # 햄버거 이미지 예시
    },
    {
        "question": "다음 중 딸기는 과연 어떤 부위를 먹는 것일까요?",
        "options": ["열매", "꽃받침", "씨앗"],
        "answer": "꽃받침",
        "explanation": "우리가 먹는 붉고 달콤한 부위는 과육이 아니라 꽃받침이 헛자란 것입니다. 진짜 열매는 겉에 박힌 씨입니다.",
        "image": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" # 딸기 이미지
    },
    {
        "question": "세계에서 가장 많이 팔린 게임은 무엇일까요? (2024년 기준)",
        "options": ["마인크래프트", "테트리스", "GTA 5"],
        "answer": "마인크래프트",
        "explanation": "마인크래프트는 3억 장 이상 판매되어 역사상 가장 많이 팔린 비디오 게임 1위를 기록하고 있습니다.",
        "image": "https://images.unsplash.com/photo-1607853198084-25cb4819d451?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" # 게임 관련 이미지
    },
    {
        "question": "낙타의 혹에는 무엇이 들어있을까요?",
        "options": ["물", "지방", "근육"],
        "answer": "지방",
        "explanation": "낙타의 혹은 물이 아니라 에너지원인 지방을 저장하는 곳입니다.",
        "image": "https://images.unsplash.com/photo-1549472145-668b54388ff9?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" # 낙타 이미지
    }
]

# 다마고치 캐릭터 상태 정의
characters = {
    "waiting": "👾",     # 대기중
    "thinking": "🤔",    # 문제 푸는 중 (사용 안됨)
    "correct": "🤩💕",   # 정답
    "wrong": "😵💔",     # 오답
    "end_good": "👑✨",   # 최종 성적 우수
    "end_bad": "👻💧"     # 최종 성적 저조
}

# 세션 상태 초기화
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_answered" not in st.session_state:
    st.session_state.is_answered = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None
if "char_state" not in st.session_state:
    st.session_state.char_state = "waiting"

q_idx = st.session_state.current_q
total_q = len(quiz_data)

# 화면 컨테이너 (다마고치 액정)
with st.container():
    st.markdown("<div class='tamagotchi-screen'>", unsafe_allow_html=True)
    
    if q_idx < total_q:
        q_data = quiz_data[q_idx]

        # 1. 진행 상태 표시
        st.write(f"Lv. {q_idx + 1} / {total_q}")
        
        # 2. 다마고치 캐릭터 표시
        st.markdown(f"<p class='tamagotchi-character'>{characters[st.session_state.char_state]}</p>", unsafe_allow_html=True)
        
        # 3. 관련 이미지 표시
        st.image(q_data["image"], use_container_width=True)
        
        # 4. 질문 텍스트
        st.markdown(f"<h3>{q_data['question']}</h3>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True) # 액정 영역 종료
        
        # --- 조작부 (버튼 영역) ---
        if not st.session_state.is_answered:
            st.write("선택해 주세요!")
            for i, option in enumerate(q_data["options"]):
                if st.button(option, key=f"btn_{q_idx}_{i}"):
                    st.session_state.is_answered = True
                    st.session_state.user_choice = option
                    # 정답 검사
                    if option == q_data["answer"]:
                        st.session_state.score += 1
                        st.session_state.char_state = "correct"
                    else:
                        st.session_state.char_state = "wrong"
                    st.rerun()
        else:
            # 결과 및 해설
            if st.session_state.char_state == "correct":
                st.success("🎉 정답입니다!!")
            else:
                st.error(f"💥 오답입니다! (선택지: {st.session_state.user_choice})")
            
            st.info(f"👉 **정답: {q_data['answer']}**\n\n💡 **해설:** {q_data['explanation']}")
            
            if st.button("▶ 다음으로 ▶", type="primary"):
                st.session_state.current_q += 1
                st.session_state.is_answered = False
                st.session_state.user_choice = None
                st.session_state.char_state = "waiting"
                st.rerun()

    else:
        # 퀴즈 종료 화면
        score_ratio = st.session_state.score / total_q
        if score_ratio >= 0.7:
             st.session_state.char_state = "end_good"
        else:
             st.session_state.char_state = "end_bad"
             
        # 2. 다마고치 캐릭터 표시
        st.markdown(f"<p class='tamagotchi-character'>{characters[st.session_state.char_state]}</p>", unsafe_allow_html=True)

        st.markdown("<h3>게임 오버!</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='score-text'>최종 점수: {st.session_state.score} / {total_q}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True) # 액정 영역 종료

        if score_ratio == 1.0:
            st.success("천재적인 두뇌의 소유자입니다!")
        elif score_ratio >= 0.5:
            st.info("훌륭한 상식의 소유자네요!")
        else:
            st.warning("경험치가 조금 더 필요합니다.")
            
        if st.button("🔄 게임 리셋 🔄", use_container_width=True):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.is_answered = False
            st.session_state.user_choice = None
            st.session_state.char_state = "waiting"
            st.rerun()
