import streamlit as st
import time

st.set_page_config(page_title="스트림릿독스", page_icon="🐶", layout="centered")

# CSS 애니메이션 정의
css = """
<style>
/* 🐶 기본 숨쉬기 애니메이션 (Neutral) */
@keyframes breathe {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* ✨ 기분 좋음 애니메이션 (Happy) - 통통 튀고 회전 */
@keyframes bounce_happy {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-30px) rotate(-10deg); }
    50% { transform: translateY(0) rotate(0deg); }
    75% { transform: translateY(-30px) rotate(10deg); }
}

/* 🍖 먹는중 애니메이션 (Eating) - 눌렸다 늘어났다 */
@keyframes squash_eat {
    0%, 100% { transform: scale(1, 1); }
    25% { transform: scale(1.2, 0.8) translateY(10px); }
    50% { transform: scale(0.9, 1.1) translateY(-10px); }
    75% { transform: scale(1.1, 0.9) translateY(5px); }
}

/* 💤 자는중 애니메이션 (Sleeping) - 느리고 깊게 숨쉬기, 투명도 조절 */
@keyframes sleep_breathe {
    0%, 100% { transform: scale(1) translateY(0); opacity: 1; }
    50% { transform: scale(1.02) translateY(5px); opacity: 0.8; }
}

/* 😠 화남 애니메이션 (Angry) - 부들부들 떨기 */
@keyframes shake_angry {
    0% { transform: translateX(0) scale(1.1); }
    25% { transform: translateX(-10px) scale(1.1); }
    50% { transform: translateX(10px) scale(1.1); }
    75% { transform: translateX(-10px) scale(1.1); }
    100% { transform: translateX(0) scale(1.1); }
}

.dog-neutral {
    display: inline-block;
    animation: breathe 3s infinite ease-in-out;
}

.dog-happy {
    display: inline-block;
    animation: bounce_happy 1s infinite;
}

.dog-eating {
    display: inline-block;
    animation: squash_eat 0.5s infinite;
}

.dog-sleeping {
    display: inline-block;
    animation: sleep_breathe 4s infinite ease-in-out;
}

.dog-angry {
    display: inline-block;
    animation: shake_angry 0.3s infinite;
    color: red; /* 약간 붉은 기운을 주고 싶지만 이모지라 큰 효과는 없을 수 있음 */
}

.emoji-container {
    text-align: center;
    font-size: 150px;
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

st.title("🐾 스트림릿독스 (Streamlit-dogs)")
st.markdown("나만의 가상 반려견과 수다떨고 놀아보세요!")

# 상태 초기화
if "dog_state" not in st.session_state:
    st.session_state.dog_state = "neutral"
if "affection" not in st.session_state:
    st.session_state.affection = 50
if "hunger" not in st.session_state:
    st.session_state.hunger = 50

# 강아지 상태 업데이트 로직 (간단하게)
if st.session_state.hunger < 20:
    st.session_state.dog_state = "angry"
elif st.session_state.affection > 80 and st.session_state.dog_state != "sleeping":
    st.session_state.dog_state = "happy"

# 강아지 상태에 따른 이미지와 메시지 설정
states = {
    "neutral": {"emoji": "🐕", "msg": "강아지가 평온하게 당신을 바라보고 있습니다.", "class": "dog-neutral"},
    "happy": {"emoji": "🐶💕", "msg": "강아지가 기분이 아주 좋습니다! 꼬리를 흔들며 방방 뜁니다.", "class": "dog-happy"},
    "eating": {"emoji": "🐕🍖", "msg": "강아지가 게걸스럽게 밥을 먹고 있습니다 냠냠!", "class": "dog-eating"},
    "sleeping": {"emoji": "🐕💤", "msg": "강아지가 새근새근 깊게 자고 있습니다... 쉿!", "class": "dog-sleeping"},
    "angry": {"emoji": "👿🐕", "msg": "강아지가 불만스러운 표정으로 으르렁거립니다. 배가 고프거나 화가 났어요.", "class": "dog-angry"}
}

current_state = states[st.session_state.dog_state]

# UI 출력
st.subheader("나의 강아지 '바둑이'")

# 강아지 애니메이션 출력 (CSS 클래스 적용)
html_dog = f"""
<div class="emoji-container">
    <div class="{current_state['class']}">{current_state['emoji']}</div>
</div>
"""
st.markdown(html_dog, unsafe_allow_html=True)
st.info(current_state["msg"])

st.divider()

# 상태바
col1, col2 = st.columns(2)
with col1:
    st.progress(st.session_state.affection / 100, text=f"친밀도: {st.session_state.affection}/100")
with col2:
    st.progress(st.session_state.hunger / 100, text=f"포만감: {st.session_state.hunger}/100")

st.divider()

# 액션 버튼들
st.write("무엇을 할까요?")
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("쓰다듬기 ✋", use_container_width=True):
        if st.session_state.dog_state != "sleeping":
            st.session_state.affection = min(100, st.session_state.affection + 10)
            st.session_state.dog_state = "happy"
            st.rerun()
        else:
            st.warning("강아지가 자고 있어서 깰까 봐 조심스럽게 쓰다듬었습니다.")

with c2:
    if st.button("밥 주기 🍖", use_container_width=True):
        if st.session_state.dog_state != "sleeping":
            st.session_state.hunger = min(100, st.session_state.hunger + 20)
            st.session_state.dog_state = "eating"
            st.rerun()
        else:
            st.warning("자는 중에는 밥을 먹일 수 없어요!")

with c3:
    if st.button("놀아주기 🎾", use_container_width=True):
        if st.session_state.dog_state != "sleeping":
            st.session_state.affection = min(100, st.session_state.affection + 15)
            st.session_state.hunger = max(0, st.session_state.hunger - 10)
            st.session_state.dog_state = "happy"
            st.rerun()
        else:
            st.warning("강아지가 너무 졸려합니다.")

with c4:
    if st.button("재우기 🛏️", use_container_width=True):
        st.session_state.dog_state = "sleeping"
        st.rerun()

# 시간이 지나면 배고파지는 스크립트를 위해 리셋 기능
if st.button("처음부터 다시 키우기", type="primary"):
    st.session_state.dog_state = "neutral"
    st.session_state.affection = 50
    st.session_state.hunger = 50
    st.rerun()
