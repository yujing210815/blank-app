import streamlit as st

st.title("🎈 하이 하이 ")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import time

st.set_page_config(page_title="스트림릿독스", page_icon="🐶", layout="centered")

st.title("🐾 스트림릿독스 (Streamlit-dogs)")
st.markdown("나만의 가상 반려견과 수다떨고 놀아보세요!")

# 상태 초기화
if "dog_state" not in st.session_state:
    st.session_state.dog_state = "neutral"
if "affection" not in st.session_state:
    st.session_state.affection = 50
if "hunger" not in st.session_state:
    st.session_state.hunger = 50

# 강아지 상태에 따른 이미지와 메시지 설정
states = {
    "neutral": {"emoji": "🐕", "msg": "강아지가 당신을 바라보고 있습니다."},
    "happy": {"emoji": "🐶✨", "msg": "강아지가 기분이 아주 좋습니다! 꼬리를 흔들어요."},
    "eating": {"emoji": "🍖🐕", "msg": "강아지가 밥을 맛있게 먹고 있습니다 냠냠."},
    "sleeping": {"emoji": "💤🐕", "msg": "강아지가 새근새근 자고 있습니다... 쉿!"},
    "angry": {"emoji": "😠🐕", "msg": "강아지가 불만스러운 표정입니다. 배가 고프거나 심심한가봐요."}
}

# 강아지 상태 업데이트 로직 (간단하게)
if st.session_state.hunger < 20:
    st.session_state.dog_state = "angry"
elif st.session_state.affection > 80:
    st.session_state.dog_state = "happy"

current_state = states[st.session_state.dog_state]

# UI 출력
st.subheader("나의 강아지 '바둑이'")

# 강아지 모습 출력 (큰 텍스트로 이모지 출력, 실제 앱이면 이미지로 대체 추천)
st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{current_state['emoji']}</h1>", unsafe_allow_html=True)
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
