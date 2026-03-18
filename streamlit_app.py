import streamlit as st

st.set_page_config(page_title="던전 퀴즈 탐험대", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap');

html, body, [class*="stMarkdown"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

.dungeon-box {
    background: rgba(0,0,0,0.6);
    border: 3px solid #e94560;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    text-align: center;
}

.stage-title {
    font-family: 'Press Start 2P', cursive;
    color: #ffd700;
    font-size: 14px;
    letter-spacing: 3px;
    text-shadow: 0 0 10px #ffd700;
    margin-bottom: 10px;
}

.monster-box {
    font-size: 90px;
    margin: 10px 0;
    display: inline-block;
}

.player-box {
    font-size: 60px;
    display: inline-block;
}

.battle-vs {
    font-family: 'Press Start 2P', cursive;
    color: #e94560;
    font-size: 20px;
    font-weight: bold;
    text-shadow: 0 0 15px #e94560;
}

.health-bar-container {
    background: #333;
    border-radius: 10px;
    height: 20px;
    margin: 5px 0 15px 0;
    border: 2px solid #555;
    overflow: hidden;
}
.health-bar {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}
.health-green { background: linear-gradient(90deg, #00b09b, #96c93d); }
.health-yellow { background: linear-gradient(90deg, #f7971e, #ffd200); }
.health-red { background: linear-gradient(90deg, #e94560, #c0392b); }

.question-box {
    background: rgba(255,255,255,0.05);
    border: 2px solid #e2b714;
    border-radius: 10px;
    padding: 15px;
    color: #fffde7;
    font-size: 17px;
    font-weight: bold;
    margin-bottom: 15px;
    text-align: left;
}

.stButton>button {
    width: 100%;
    border-radius: 8px;
    border: 3px solid #e94560;
    background-color: #16213e;
    color: #fff;
    font-weight: bold;
    font-size: 16px;
    font-family: 'Noto Sans KR', sans-serif;
    box-shadow: 0 4px 15px rgba(233,69,96,0.4);
    transition: all 0.2s;
    padding: 12px 10px;
}
.stButton>button:hover {
    background-color: #e94560;
    transform: scale(1.02);
}

.battle-result-correct {
    background: rgba(0,255,100,0.1);
    border: 2px solid #00ff64;
    border-radius: 10px;
    padding: 12px;
    color: #00ff64;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}
.battle-result-wrong {
    background: rgba(233,69,96,0.15);
    border: 2px solid #e94560;
    border-radius: 10px;
    padding: 12px;
    color: #e94560;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.explanation-box {
    background: rgba(255,255,255,0.05);
    border-left: 4px solid #e2b714;
    border-radius: 0 8px 8px 0;
    padding: 10px 15px;
    color: #e0e0e0;
    font-size: 14px;
    margin-bottom: 15px;
}

@keyframes shake {
    0%,100%{transform:translateX(0)}
    20%{transform:translateX(-12px)}
    40%{transform:translateX(12px)}
    60%{transform:translateX(-8px)}
    80%{transform:translateX(8px)}
}
@keyframes bounce {
    0%,100%{transform:translateY(0)}
    30%{transform:translateY(-20px)}
    60%{transform:translateY(-10px)}
}
@keyframes float {
    0%,100%{transform:translateY(0)}
    50%{transform:translateY(-8px)}
}

.anim-shake  { display:inline-block; animation: shake 0.5s ease; }
.anim-bounce { display:inline-block; animation: bounce 0.6s ease; }
.anim-float  { display:inline-block; animation: float 2s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 퀴즈 데이터 (10 문제, 검증된 이미지 URL 사용)
# ────────────────────────────────────────────────
quiz_data = [
    {
        "stage": "1층 식품의 방",
        "monster": "🥦 야채 고블린",
        "monster_emoji": "👺",
        "question": "딸기의 달콤한 붉은 부위는 식물학적으로 무엇일까요?",
        "options": ["열매(과육)", "꽃받침(화탁)", "씨앗"],
        "answer": "꽃받침(화탁)",
        "explanation": "우리가 먹는 빨간 부위는 꽃받침이 발달한 것입니다. 진짜 열매는 표면에 박혀있는 작고 딱딱한 씨앗들입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/PerfectStrawberry.jpg/640px-PerfectStrawberry.jpg"
    },
    {
        "stage": "2층 동물의 방",
        "monster": "🐪 사막 낙타전사",
        "monster_emoji": "🐪",
        "question": "낙타의 혹 속에는 무엇이 가득 들어있을까요?",
        "options": ["물", "지방", "근육"],
        "answer": "지방",
        "explanation": "낙타의 혹은 물 주머니가 아니라 지방 저장소입니다. 사막에서 먹이가 없을 때 이 지방을 분해해 에너지와 수분을 얻습니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Camelus_bactrianus_-_Houston_Zoo.jpg/640px-Camelus_bactrianus_-_Houston_Zoo.jpg"
    },
    {
        "stage": "3층 음식의 방",
        "monster": "🍔 햄버거 드래곤",
        "monster_emoji": "🐉",
        "question": "세계 최초로 생긴 패스트푸드 프랜차이즈는?",
        "options": ["맥도날드", "버거킹", "A&W 레스토랑"],
        "answer": "A&W 레스토랑",
        "explanation": "A&W는 1919년에 루트비어 판매로 시작해 1923년에 첫 드라이브인 프랜차이즈를 열었습니다. 맥도날드는 1940년 설립입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/A%26W_Root_Beer_Stand%2C_Sacramento%2C_1950s.jpg/640px-A%26W_Root_Beer_Stand%2C_Sacramento%2C_1950s.jpg"
    },
    {
        "stage": "4층 게임의 방",
        "monster": "🎮 픽셀 마왕",
        "monster_emoji": "👾",
        "question": "역사상 가장 많이 팔린 비디오 게임은? (2024년 기준)",
        "options": ["마인크래프트", "테트리스", "GTA 5"],
        "answer": "마인크래프트",
        "explanation": "마인크래프트는 2024년 기준 전 세계 3억 장 이상 판매되어 역대 최다 판매 게임 1위입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/5/51/Minecraft_cover.png/300px-Minecraft_cover.png"
    },
    {
        "stage": "5층 한국의 방",
        "monster": "🌳 천연기념물 가디언",
        "monster_emoji": "🌳",
        "question": "대한민국 천연기념물 제1호는 무엇일까요?",
        "options": ["진도 진돗개", "대구 도동 측백나무 숲", "울릉 향나무"],
        "answer": "대구 도동 측백나무 숲",
        "explanation": "대한민국 천연기념물 제1호는 대구광역시 동구 도동에 있는 측백나무 숲(1962년 지정)입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Dodong_Thuja_Forest_01.JPG/640px-Dodong_Thuja_Forest_01.JPG"
    },
    {
        "stage": "6층 우주의 방",
        "monster": "🪐 우주 마법사",
        "monster_emoji": "🧙",
        "question": "태양계에서 위성(달)의 수가 가장 많은 행성은?",
        "options": ["목성", "토성", "천왕성"],
        "answer": "토성",
        "explanation": "2023년 발견된 위성들을 포함하면 토성은 146개 이상의 위성을 가지고 있어 태양계 최다 위성 보유 행성입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Saturn_during_Equinox.jpg/640px-Saturn_during_Equinox.jpg"
    },
    {
        "stage": "7층 언어의 방",
        "monster": "📚 언어 마녀",
        "monster_emoji": "🧝",
        "question": "전 세계에서 모국어 사용자 수 기준으로 가장 많이 쓰이는 언어는?",
        "options": ["영어", "스페인어", "만다린(중국어)"],
        "answer": "만다린(중국어)",
        "explanation": "모국어 사용자 기준으로는 만다린(중국 표준어)이 약 9억 명 이상으로 1위입니다. 영어는 전체 사용자 기준 1위입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/PRC_on_the_globe_%28China_centered%29.svg/600px-PRC_on_the_globe_%28China_centered%29.svg.png"
    },
    {
        "stage": "8층 인체의 방",
        "monster": "💀 해골 박사",
        "monster_emoji": "💀",
        "question": "성인 인체에서 가장 큰 기관(Organ)은 무엇일까요?",
        "options": ["간", "폐", "피부"],
        "answer": "피부",
        "explanation": "피부는 약 1.5~2㎡의 면적을 가진 인체에서 가장 큰 단일 기관입니다. 체온 조절, 보호, 감각 기능을 합니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG-Geschichtete_Epidermis.png/640px-PNG-Geschichtete_Epidermis.png"
    },
    {
        "stage": "9층 음악의 방",
        "monster": "🎻 음악 유령",
        "monster_emoji": "👻",
        "question": "베토벤이 청력을 완전히 잃은 후 작곡한 가장 유명한 교향곡은?",
        "options": ["운명 교향곡 (5번)", "전원 교향곡 (6번)", "합창 교향곡 (9번)"],
        "answer": "합창 교향곡 (9번)",
        "explanation": "베토벤은 귀가 완전히 들리지 않는 상태에서 교향곡 9번 '합창'을 완성했습니다. 초연 당시 그는 지휘를 했지만 청중의 박수 소리를 듣지 못했다고 전해집니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/480px-Beethoven.jpg"
    },
    {
        "stage": "10층 최후의 방 👑",
        "monster": "😈 지식의 대마왕",
        "monster_emoji": "😈",
        "question": "다음 중 실제로 존재하지 않는 원소는?",
        "options": ["아인슈타이늄 (Einsteinium)", "닥터륨 (Doctorium)", "오가네손 (Oganesson)"],
        "answer": "닥터륨 (Doctorium)",
        "explanation": "아인슈타이늄(Es, 99번)과 오가네손(Og, 118번)은 실제 주기율표의 원소입니다. 닥터륨은 실존하지 않는 가상의 원소입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Simple_Periodic_Table_Chart-en.svg/800px-Simple_Periodic_Table_Chart-en.svg.png"
    }
]

MAX_HP = 5  # 하트 개수

# ── 세션 상태 초기화 ──
def init_state():
    st.session_state.current_q = 0
    st.session_state.hp = MAX_HP
    st.session_state.is_answered = False
    st.session_state.user_choice = None
    st.session_state.last_correct = None  # True/False/None

if "current_q" not in st.session_state:
    init_state()

q_idx = st.session_state.current_q
total_q = len(quiz_data)
hp = st.session_state.hp

# ── HP 표시 함수 ──
def hp_bar(hp, max_hp):
    hearts = "❤️" * hp + "🖤" * (max_hp - hp)
    pct = int(hp / max_hp * 100)
    if pct > 60:
        color_class = "health-green"
    elif pct > 30:
        color_class = "health-yellow"
    else:
        color_class = "health-red"
    return hearts, pct, color_class

# ── GAME OVER ──
if hp <= 0:
    st.markdown("""
    <div class='dungeon-box'>
        <p class='stage-title'>💀 GAME OVER 💀</p>
        <div style='font-size:80px'>💀</div>
        <p style='color:#e94560; font-size:20px; font-weight:bold; margin-top:10px;'>용사여... 쓰러졌습니다</p>
        <p style='color:#aaa;'>HP가 모두 소진되었습니다. 지식을 보충하고 다시 도전하세요!</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#ffd700;font-size:18px;'>📊 {q_idx}층까지 진격했습니다!</p>", unsafe_allow_html=True)
    if st.button("🔄 처음부터 다시 도전!", use_container_width=True, type="primary"):
        init_state()
        st.rerun()
    st.stop()

# ── 클리어 ──
if q_idx >= total_q:
    st.balloons()
    st.markdown(f"""
    <div class='dungeon-box'>
        <p class='stage-title'>🏆 DUNGEON CLEAR! 🏆</p>
        <div style='font-size:80px'>👑</div>
        <p style='color:#ffd700; font-size:22px; font-weight:bold; margin-top:10px;'>최종 던전 정복!!</p>
        <p style='color:#e0e0e0;'>남은 HP: {"❤️" * hp} ({hp * 20}%)</p>
    </div>
    """, unsafe_allow_html=True)
    if hp == MAX_HP:
        st.success("💎 HP 한 칸도 안 깎이고 클리어! 완벽한 지식왕입니다!")
    elif hp >= 3:
        st.info("⚔️ 훌륭합니다! 강인한 지식 용사!")
    else:
        st.warning("😅 아슬아슬하게 클리어! 하지만 해냈습니다!")
    if st.button("🔄 다시 도전하기", use_container_width=True, type="primary"):
        init_state()
        st.rerun()
    st.stop()

# ── 현재 문제 ──
q = quiz_data[q_idx]
last_correct = st.session_state.last_correct

# 몬스터 애니메이션 클래스 결정
if last_correct is None:
    monster_anim = "anim-float"
    player_anim  = "anim-float"
elif last_correct:
    monster_anim = "anim-shake"   # 몬스터가 맞고 흔들림
    player_anim  = "anim-bounce"  # 플레이어가 기뻐서 튀어오름
else:
    monster_anim = "anim-bounce"  # 몬스터가 공격성공으로 튀어오름
    player_anim  = "anim-shake"   # 플레이어가 맞고 떨림

# ── 상단 HUD ──
hearts, pct, hp_class = hp_bar(hp, MAX_HP)
st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
    <span style='color:#ffd700; font-weight:bold; font-size:15px;'>⚔️ {q_idx+1} / {total_q} 층</span>
    <span style='font-size:18px;'>{hearts}</span>
</div>
<div class='health-bar-container'>
    <div class='health-bar {hp_class}' style='width:{pct}%'></div>
</div>
""", unsafe_allow_html=True)

# ── 전투 화면 ──
st.markdown(f"""
<div class='dungeon-box'>
    <p class='stage-title'>{q['stage'].upper()}</p>
    <div style='display:flex; justify-content:center; align-items:center; gap:30px;'>
        <div>
            <div class='{monster_anim} monster-box'>{q['monster_emoji']}</div>
            <p style='color:#e94560; font-size:12px; margin-top:5px;'>{q['monster']}</p>
        </div>
        <div class='battle-vs'>VS</div>
        <div>
            <div class='{player_anim} player-box'>🧙‍♂️</div>
            <p style='color:#4fc3f7; font-size:12px; margin-top:5px;'>📖 지식 사용자</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 결과 표시 (이전 문제 풀었을 때) ──
if last_correct is True:
    st.markdown("<div class='battle-result-correct'>✅ 정답! 몬스터에게 데미지를 입혔습니다!</div>", unsafe_allow_html=True)
elif last_correct is False:
    st.markdown(f"<div class='battle-result-wrong'>💥 오답! 몬스터의 공격을 받았습니다! (정답: {quiz_data[q_idx-1]['answer']})</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='explanation-box'>💡 <strong>해설:</strong> {quiz_data[q_idx-1]['explanation']}</div>", unsafe_allow_html=True)

# ── 문제 이미지 + 질문 ──
st.image(q["image"], use_container_width=True)
st.markdown(f"<div class='question-box'>❓ {q['question']}</div>", unsafe_allow_html=True)

# ── 답변 or 다음 버튼 ──
if not st.session_state.is_answered:
    for i, opt in enumerate(q["options"]):
        if st.button(f"{'① ② ③'[i*2]} {opt}", key=f"opt_{q_idx}_{i}"):
            correct = (opt == q["answer"])
            st.session_state.is_answered = True
            st.session_state.user_choice = opt
            st.session_state.last_correct = correct
            if not correct:
                st.session_state.hp -= 1
            st.rerun()
else:
    # 정답 맞힌 경우 해설 바로 표시, 오답은 위에서 표시됨
    if st.session_state.last_correct:
        st.markdown(f"<div class='explanation-box'>💡 <strong>해설:</strong> {q['explanation']}</div>", unsafe_allow_html=True)

    btn_label = "⚔️ 다음 층으로!" if q_idx < total_q - 1 else "👑 최후의 결전!"
    if st.button(btn_label, type="primary", use_container_width=True):
        st.session_state.current_q += 1
        st.session_state.is_answered = False
        st.session_state.user_choice = None
        st.session_state.last_correct = None
        st.rerun()
