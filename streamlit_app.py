import streamlit as st

st.set_page_config(page_title="마왕의 성 퀴즈 던전", page_icon="⚔️", layout="centered")

PALETTE = {
    'K': '#111111', 'W': '#FFFFFF', 'Y': '#F9D71C', 'y': '#C7A800',
    'n': '#FDBCB4', 'N': '#D08070', 'O': '#222222',
    'B': '#1A237E', 'b': '#3949AB', 'r': '#C62828', 'R': '#E53935',
    'S': '#CFD8DC', 's': '#78909C',
    'T': '#4E342E', 't': '#6D4C41',
    'G': '#2E7D32', 'g': '#43A047',
    'P': '#4A148C', 'p': '#7B1FA2',
    'D': '#BF360C', 'd': '#FF6D00',
    'M': '#880E4F', 'm': '#AD1457',
}

def sprite_svg(rows, px=11):
    max_w = max(len(r) for r in rows)
    h = len(rows)
    rects = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            c = PALETTE.get(ch)
            if c:
                rects.append(f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}" fill="{c}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{max_w*px}" height="{h*px}" '
            f'style="image-rendering:pixelated;image-rendering:crisp-edges;display:block;">'
            + ''.join(rects) + '</svg>')

# ─── SPRITES ────────────────────────────────────────────────────────────────
HERO = [
    "..YYYY....",
    ".YYYYYYY..",
    ".KnnnnK...",
    ".KnOOnK...",
    ".KnnnnK...",
    ".Kn.WnK...",
    "KBBBBBBKsS",
    "KBrrrrBBSS",
    "KBrBBrBBSs",
    "KBrrrrBBsK",
    ".KBBBBBK..",
    ".KBK.KBK..",
    ".KBK.KBK..",
    ".KTK.KTK..",
    ".KKK.KKK..",
]

HERO_ATK = [
    "..YYYY....",
    ".YYYYYYY..",
    ".KnnnnK...",
    ".KnOOnK...",
    ".KnnnnK.SS",
    ".Kn.WnKSSS",
    "KBBBBBBsSS",
    "KBrrrrBBSs",
    "KBrBBrBBsK",
    "KBrrrrBBKK",
    ".KBBBBBK..",
    "..KBK.KBK.",
    "..KBK.KBK.",
    "..KTK.KTK.",
    "..KKK.KKK.",
]

HERO_HIT = [
    "..YYYY....",
    ".YYYYYYY..",
    ".KnnnnK...",
    ".KnXXnK...",
    ".KnnnnK...",
    ".KnVVnK...",
    ".KBBBBBKs.",
    ".KBrrrrBSK",
    ".KBrBBrBSK",
    ".KBrrrrBsK",
    "..KBBBBBK.",
    "..KBK.KBK.",
    "..KBK.KBK.",
    "..KTK.KTK.",
    "..KKK.KKK.",
]

MONSTERS = [
    # 0: 슬라임 (1-2층)
    (["..gggg..", ".gGGGGg.", "gGWgWGGg", "GGGgGGGG",
       "GGGnnnGG", "GggggggG", ".GgGGgG.", "..GG.GG."],
     "💚 슬라임", 10),
    # 1: 고블린 (3-4층)
    (["..KKKKK.", ".GgGgGgG", "GgOGGOgG", "GgGGGGgG",
       "GgKWKWgG", ".GgGGgG.", ".KBBBBK.", ".GK..KG."],
     "👺 고블린", 12),
    # 2: 오크 (5-6층)
    ([".KBBKBBK", "KBBBBBBK", "KGGgGGGK", "KGOgGOGK",
       "KGGGGGgK", "KGrWWrGK", "KBBBBBBK", "KBrBrBBK",
       ".KBBBBK.", ".KGK.KGK"],
     "💪 오크 전사", 15),
    # 3: 언데드 나이트 (7-8층)
    ([".KSSSSKK", "KSsSSsSK", "KSKSSKsK", "KSSOOSsK",
       "KSSSSsSK", "KBBBBBBK", "KBrBBrBK", "KBBBBsBK",
       ".KBBBBK.", ".KBK.KBK"],
     "💀 언데드 나이트", 18),
    # 4: 마왕 (9-10층)
    (["KPPKKKPPK", "KPpPPpPPK", "KPpPPpPPK", "KPPOOptPK",
       "KPPPPPpK.", "KPmmMmmPK", ".KPPPPPPK", "KPPrPrPPK",
       "KPPPPPpK.", ".KPK..KPK"],
     "😈 마왕", 25),
]

SKILLS = [
    ("🔥 파이어볼", "⚔️ 검 휘두르기", "🌪️ 사이클론"),
    ("⚡ 번개", "🛡️ 방패 격돌", "❄️ 아이스 볼트"),
    ("💥 폭발", "🗡️ 쌍검 베기", "🌊 파도 공격"),
]

quiz_data = [
    {"stage":"1층 - 슬라임의 방","mon":0,
     "q":"딸기의 달콤한 붉은 부위는 식물학적으로 무엇일까요?",
     "opts":["열매(과육)","꽃받침(화탁)","씨앗"],"ans":"꽃받침(화탁)",
     "exp":"우리가 먹는 부위는 꽃받침이 발달한 것입니다. 진짜 열매는 표면의 작은 씨앗들이에요!"},
    {"stage":"2층 - 슬라임 둥지","mon":0,
     "q":"낙타의 혹 속에 가득 들어있는 것은?",
     "opts":["물","지방","근육"],"ans":"지방",
     "exp":"낙타의 혹은 지방을 저장하는 곳이에요. 사막에서 에너지와 수분을 여기서 얻습니다."},
    {"stage":"3층 - 고블린 땅굴","mon":1,
     "q":"세계 최초의 패스트푸드 프랜차이즈는?",
     "opts":["맥도날드","버거킹","A&W 레스토랑"],"ans":"A&W 레스토랑",
     "exp":"A&W는 1919년 시작! 맥도날드는 1940년이 되어서야 문을 열었습니다."},
    {"stage":"4층 - 고블린 왕의 방","mon":1,
     "q":"역사상 가장 많이 팔린 비디오 게임은? (2024 기준)",
     "opts":["마인크래프트","테트리스","GTA 5"],"ans":"마인크래프트",
     "exp":"마인크래프트는 3억 장 이상 팔려 역대 1위를 기록하고 있습니다!"},
    {"stage":"5층 - 오크 진지","mon":2,
     "q":"대한민국 천연기념물 제1호는?",
     "opts":["진도 진돗개","대구 도동 측백나무 숲","울릉 향나무"],"ans":"대구 도동 측백나무 숲",
     "exp":"1962년 지정된 대구 동구 도동의 측백나무 숲이 1호입니다."},
    {"stage":"6층 - 오크 장군의 방","mon":2,
     "q":"태양계에서 위성(달)의 수가 가장 많은 행성은?",
     "opts":["목성","토성","천왕성"],"ans":"토성",
     "exp":"2023년 기준 토성은 146개 이상의 위성을 보유해 태양계 최다입니다!"},
    {"stage":"7층 - 언데드 묘지","mon":3,
     "q":"성인 인체에서 가장 큰 기관(Organ)은?",
     "opts":["간","폐","피부"],"ans":"피부",
     "exp":"피부는 약 1.5~2㎡로 인체 최대 기관입니다. 체온 조절·보호 역할 수행!"},
    {"stage":"8층 - 언데드 기사단의 방","mon":3,
     "q":"모국어 사용자 수 기준 세계에서 가장 많이 쓰이는 언어는?",
     "opts":["영어","스페인어","만다린(중국어)"],"ans":"만다린(중국어)",
     "exp":"모국어 기준 만다린이 약 9억+ 명으로 1위! 영어는 총 사용자 기준 1위입니다."},
    {"stage":"9층 - 마왕의 전실","mon":4,
     "q":"청력을 완전히 잃은 후 베토벤이 작곡한 가장 유명한 교향곡은?",
     "opts":["운명(5번)","전원(6번)","합창(9번)"],"ans":"합창(9번)",
     "exp":"귀가 완전히 안 들리는 상태에서 합창 교향곡을 완성했습니다. 놀랍죠?"},
    {"stage":"10층 - 마왕의 옥좌 👑","mon":4,
     "q":"다음 중 실제로 존재하지 않는 원소는?",
     "opts":["아인슈타이늄(Es)","닥터륨(Dc)","오가네손(Og)"],"ans":"닥터륨(Dc)",
     "exp":"아인슈타이늄(99번)과 오가네손(118번)은 진짜 원소! 닥터륨은 존재하지 않습니다."},
]

MAX_HP = 5
MONSTER_MAX_HP = [10, 10, 12, 12, 15, 15, 18, 18, 25, 25]

def init():
    st.session_state.update({
        "q_idx": 0, "player_hp": MAX_HP,
        "monster_hp": MONSTER_MAX_HP[0],
        "state": "idle",  # idle | correct | wrong | dead | clear
        "answered": False, "choice": None,
    })

if "q_idx" not in st.session_state:
    init()

q_idx = st.session_state.q_idx
player_hp = st.session_state.player_hp
state = st.session_state.state

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap');
.stApp { background: #0d0d1a; }
.pixel-font { font-family: 'Press Start 2P', cursive; }
.battle-area {
    background: linear-gradient(180deg,#1a0a2e 0%,#0d0d2a 60%,#0a1a0a 100%);
    border: 4px solid #ffd700;
    border-radius: 4px;
    padding: 16px;
    display: flex; justify-content: space-between; align-items: flex-end;
    min-height: 220px; position: relative;
    box-shadow: 0 0 30px rgba(255,215,0,0.15);
}
.battle-area::after {
    content:''; position:absolute; inset:0; pointer-events:none;
    background: repeating-linear-gradient(transparent,transparent 3px,rgba(0,0,0,0.08) 4px);
}
.stage-banner {
    font-family:'Press Start 2P',cursive; color:#ffd700;
    font-size:11px; text-align:center; padding:10px 0 6px;
    text-shadow:0 0 10px #ffd700;
}
.hp-row { display:flex; justify-content:space-between; align-items:center; margin:8px 0; }
.hp-label { font-family:'Press Start 2P',cursive; font-size:9px; color:#ccc; }
.hp-bar-bg { background:#333; border:2px solid #555; border-radius:2px; height:14px; flex:1; margin:0 8px; overflow:hidden; }
.hp-bar-fill { height:100%; border-radius:1px; transition:width 0.4s; }
.green-bar { background: linear-gradient(90deg,#00e676,#69f0ae); }
.yellow-bar { background: linear-gradient(90deg,#ffd600,#ffab40); }
.red-bar { background: linear-gradient(90deg,#f44336,#ef9a9a); }
.question-card {
    background: rgba(0,0,0,0.7); border:3px solid #5c6bc0;
    border-radius:4px; padding:14px; color:#fffde7;
    font-family:'Noto Sans KR',sans-serif; font-size:16px; font-weight:700; margin:10px 0;
}
.result-correct {
    background:rgba(0,255,100,0.1); border:2px solid #00e676;
    border-radius:4px; padding:10px; color:#00e676;
    font-family:'Press Start 2P',cursive; font-size:11px; text-align:center; margin:6px 0;
}
.result-wrong {
    background:rgba(244,67,54,0.1); border:2px solid #f44336;
    border-radius:4px; padding:10px; color:#ff5252;
    font-family:'Press Start 2P',cursive; font-size:11px; text-align:center; margin:6px 0;
}
.explanation { background:rgba(255,255,255,0.05); border-left:4px solid #ffd700;
    border-radius:0 4px 4px 0; padding:10px 14px; color:#e0e0e0;
    font-family:'Noto Sans KR',sans-serif; font-size:14px; margin:6px 0; }
.stButton>button {
    width:100%; border-radius:4px; border:3px solid #5c6bc0;
    background:#0d0d2a; color:#fff;
    font-family:'Noto Sans KR',sans-serif; font-weight:700; font-size:15px;
    box-shadow:3px 3px 0 #5c6bc0; transition:all 0.15s; padding:12px 8px;
}
.stButton>button:hover { background:#5c6bc0; box-shadow:0 0 0 #5c6bc0; transform:translate(3px,3px); }
@keyframes hero-atk {
    0%{transform:translateX(0) scaleX(1);}
    40%{transform:translateX(28px) scaleX(1.15);}
    70%{transform:translateX(16px) scaleX(1.05);}
    100%{transform:translateX(0) scaleX(1);}
}
@keyframes hero-hit {
    0%{transform:translateX(0);filter:none;}
    25%{transform:translateX(-18px);filter:brightness(2) saturate(0);}
    50%{transform:translateX(-28px);filter:brightness(2) hue-rotate(180deg);}
    75%{transform:translateX(-12px);}
    100%{transform:translateX(0);filter:none;}
}
@keyframes mon-hit {
    0%{transform:translateX(0);filter:none;}
    20%{transform:translateX(14px);filter:brightness(3) saturate(0);}
    50%{transform:translateX(10px);filter:brightness(2) hue-rotate(90deg);}
    100%{transform:translateX(0);filter:none;}
}
@keyframes mon-atk {
    0%{transform:translateX(0);}
    40%{transform:translateX(-24px) scaleX(1.2);}
    100%{transform:translateX(0) scaleX(1);}
}
@keyframes idle-float {
    0%,100%{transform:translateY(0);}
    50%{transform:translateY(-5px);}
}
.anim-hero-idle  { display:inline-block; animation:idle-float 2.2s ease-in-out infinite; }
.anim-hero-atk   { display:inline-block; animation:hero-atk 0.55s ease forwards; }
.anim-hero-hit   { display:inline-block; animation:hero-hit 0.55s ease forwards; }
.anim-mon-idle   { display:inline-block; animation:idle-float 2.8s ease-in-out infinite; }
.anim-mon-hit    { display:inline-block; animation:mon-hit 0.55s ease forwards; }
.anim-mon-atk    { display:inline-block; animation:mon-atk 0.55s ease forwards; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="stage-banner pixel-font">⚔ 마왕의 성 퀴즈 던전 ⚔</p>', unsafe_allow_html=True)

# ── GAME OVER ──
if player_hp <= 0 or state == "dead":
    st.markdown("""
    <div style='text-align:center;padding:30px'>
        <p style='font-family:"Press Start 2P",cursive;color:#f44336;font-size:22px;text-shadow:0 0 20px #f44336'>💀 GAME OVER 💀</p>
        <p style='color:#aaa;font-family:"Noto Sans KR",sans-serif;font-size:16px'>HP가 모두 소진되었습니다!</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#ffd700;font-family:\"Press Start 2P\",cursive;font-size:11px;'>{q_idx}층까지 진격</p>", unsafe_allow_html=True)
    if st.button("🔄 처음부터 다시!", use_container_width=True):
        init(); st.rerun()
    st.stop()

# ── CLEAR ──
if state == "clear" or q_idx >= len(quiz_data):
    st.balloons()
    st.markdown(f"""
    <div style='text-align:center;padding:30px'>
        <p style='font-family:"Press Start 2P",cursive;color:#ffd700;font-size:18px;text-shadow:0 0 20px #ffd700'>👑 DUNGEON CLEAR! 👑</p>
        <p style='color:#fff;font-family:"Noto Sans KR",sans-serif;font-size:17px'>마왕을 물리치고 성을 탈환했습니다!</p>
        <p style='color:#f48fb1;font-family:"Press Start 2P",cursive;font-size:11px'>잔여 HP: {"❤️"*player_hp}{"🖤"*(MAX_HP-player_hp)}</p>
    </div>""", unsafe_allow_html=True)
    if st.button("🔄 다시 도전하기", use_container_width=True):
        init(); st.rerun()
    st.stop()

# ── CURRENT QUESTION ──
q = quiz_data[q_idx]
mon_data = MONSTERS[q["mon"]]
mon_sprite, mon_name, mon_max_hp_def = mon_data
mon_max_hp = MONSTER_MAX_HP[q_idx]
mon_hp = st.session_state.monster_hp

# pick hero sprite
hero_rows = HERO_ATK if state == "correct" else (HERO_HIT if state == "wrong" else HERO)
hero_svg = sprite_svg(hero_rows, px=11)
mon_svg = sprite_svg(mon_sprite, px=12)

# animation class
hero_anim = "anim-hero-atk" if state=="correct" else ("anim-hero-hit" if state=="wrong" else "anim-hero-idle")
mon_anim  = "anim-mon-hit"  if state=="correct" else ("anim-mon-atk"  if state=="wrong" else "anim-mon-idle")

# HP bar color
def hp_color(cur, mx):
    r = cur/mx
    return "green-bar" if r>0.5 else ("yellow-bar" if r>0.25 else "red-bar")

player_pct = int(player_hp/MAX_HP*100)
mon_pct = int(mon_hp/mon_max_hp*100)

# Stage banner + battle scene
st.markdown(f'<p style="font-family:\'Press Start 2P\',cursive;color:#b39ddb;font-size:10px;text-align:center;margin-bottom:4px">{q["stage"]}</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class="battle-area">
    <div style="text-align:center">
        <div class="{hero_anim}">{hero_svg}</div>
        <p style="font-family:'Press Start 2P',cursive;color:#81d4fa;font-size:8px;margin-top:6px">용사</p>
    </div>
    <div style="font-family:'Press Start 2P',cursive;color:#f44336;font-size:18px;align-self:center;text-shadow:0 0 10px #f44336">VS</div>
    <div style="text-align:center">
        <div class="{mon_anim}">{mon_svg}</div>
        <p style="font-family:'Press Start 2P',cursive;color:#ef9a9a;font-size:8px;margin-top:6px">{mon_name}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# HP bars
st.markdown(f"""
<div class="hp-row">
    <span class="hp-label">용사 {"❤️"*player_hp}{"🖤"*(MAX_HP-player_hp)}</span>
</div>
<div class="hp-row">
    <span class="hp-label">몬스터 HP</span>
    <div class="hp-bar-bg"><div class="hp-bar-fill {hp_color(mon_hp,mon_max_hp)}" style="width:{mon_pct}%"></div></div>
    <span class="hp-label">{mon_hp}/{mon_max_hp}</span>
</div>
""", unsafe_allow_html=True)

# Result messages
if state == "correct":
    st.markdown('<div class="result-correct">✅ 크리티컬 히트! 몬스터에게 데미지!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="explanation">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif state == "wrong":
    st.markdown(f'<div class="result-wrong">💥 오답! 몬스터의 역습! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="explanation">💡 {q["exp"]}</div>', unsafe_allow_html=True)

# Question card
st.markdown(f'<div class="question-card">❓ {q["q"]}</div>', unsafe_allow_html=True)

# Skill buttons or Next button
if not st.session_state.answered:
    skill_set = SKILLS[q_idx % len(SKILLS)]
    c1, c2, c3 = st.columns(3)
    for col, opt, skill in zip([c1, c2, c3], q["opts"], skill_set):
        with col:
            if st.button(f"{skill}\n{opt}", key=f"opt_{q_idx}_{opt}"):
                correct = (opt == q["ans"])
                st.session_state.answered = True
                st.session_state.choice = opt
                if correct:
                    dmg = mon_max_hp // 3 + 1
                    st.session_state.monster_hp = max(0, mon_hp - dmg)
                    st.session_state.state = "correct"
                else:
                    st.session_state.player_hp = max(0, player_hp - 1)
                    st.session_state.state = "wrong"
                st.rerun()
else:
    next_label = "⚔️ 다음 층으로!" if q_idx < len(quiz_data)-1 else "👑 최후의 결전!!"
    if st.button(next_label, type="primary", use_container_width=True):
        nxt = q_idx + 1
        if player_hp <= 0:
            st.session_state.state = "dead"
        elif nxt >= len(quiz_data):
            st.session_state.state = "clear"
        else:
            st.session_state.q_idx = nxt
            st.session_state.monster_hp = MONSTER_MAX_HP[nxt]
            st.session_state.answered = False
            st.session_state.choice = None
            st.session_state.state = "idle"
        st.rerun()

st.markdown("---")
st.markdown(f"<p style='font-family:\"Press Start 2P\",cursive;color:#444;font-size:8px;text-align:center'>FLOOR {q_idx+1} / {len(quiz_data)}</p>", unsafe_allow_html=True)
