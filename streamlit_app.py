import streamlit as st

st.set_page_config(page_title="마왕의 성", page_icon="⚔️", layout="centered")

# ─── PALETTE ──────────────────────────────────────────────────────────────
P = {
    '.':None,'K':'#111','W':'#FFF',
    # hero
    'c':'#CC1100','C':'#FF3322','n':'#FDBCB4','m':'#8B4513',
    'B':'#1565C0','b':'#1E88E5','Y':'#FFD700','S':'#E0E0E0','s':'#9E9E9E',
    'T':'#3E2723','t':'#6D4C41','R':'#E53935',
    # slime
    'G':'#2ECC40','g':'#1A8026','e':'#FFEE00',
    # goblin
    'j':'#5D9B3A','J':'#3A6B20','p':'#7B1FA2','q':'#4A148C',
    # orc
    'O':'#D84315','o':'#BF360C','A':'#546E7A','a':'#78909C',
    # undead
    'U':'#E0E0E0','u':'#9E9E9E','V':'#1A237E','v':'#283593',
    # demon
    'X':'#B71C1C','x':'#D32F2F','Z':'#4A148C','z':'#7B1FA2',
    'F':'#FF6D00','f':'#FFD740','H':'#880E4F',
}

def svg(rows, px=11):
    mw = max(len(r) for r in rows)
    mh = len(rows)
    r = []
    for y,row in enumerate(rows):
        for x,ch in enumerate(row):
            c=P.get(ch)
            if c: r.append(f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}" fill="{c}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{mw*px}" height="{mh*px}" '
            f'style="image-rendering:pixelated;display:block;">{"".join(r)}</svg>')

# ─── HERO SPRITES (10 wide) ───────────────────────────────────────────────
HI = ["..KccccK..","..KcCCCcK.","..KcCCCcK.","KKnnnnnnKK",
      "KnKnnnnKnK","KnnnnnnnnK","KnmmmmmnnK","BBBBBBBBsS",
      "BbBBBBbBsS","BBBYBBBBs.","..BBBBBBK.","..KBB..BBK",
      "..KBB..BBK","..KTT..TTK"]
HA = ["..KccccK..",".KcCCCCcK.","..KcCCCcK.","KKnnnnnnKK",
      "KnKnnnnK.K","KnnnnnnnnK","KnmmmmmnnK","BBBBBBsSSSSS",
      "BbBBBBbSSSSs","BBBYBBBBssss","..BBBBBBK....","..KBB..BBK...",
      "..KBB..BBK...","..KTT..TTK..."]
HH = ["..KccccK..","..KcCCCcK.","..KcCCCcK.","KKnnnnnnKK",
      "KnKKnnKKnK","KnnnnnnnnK","KnKKKKKnnK","BBBBBBBBsS",
      "BbBBBBbBsS","BBBYBBBBs.","..BBBBBBK.","..KBB..BBK",
      "..KBB..BBK","..KTT..TTK"]

# ─── MONSTER SPRITES ─────────────────────────────────────────────────────
SLIME_SPR = [
    "..GGGGGG..","GGGGGgGGGG","GGGGGGGGgG",
    "GGeGGGGeGG","GGgGGGGgGG","GGGGGGGGgG",
    "GKWWWWWWKg",".GGGGGGgG.","GGG.GG.GGG"]

GOB_SPR = [
    ".KKKKKKKKK.",".JjjjJjjjJ.",".JjKJJKjjJ.",
    "JjKWGKWGjjJ","JjKOGKOGjjJ",".JjJJJJjJ.",
    ".JjKwKwKjJ.","..KpBpBpK..","..KjK.KjK.",
    "..KjK.KjK..","..KJKkKJK.."]

ORC_SPR = [
    "..KOOOOKKK","KOOoOOOoOOK","KOOOOOOOoOK",
    "KOKnKKnKOK","KOOOOOOOoOK","KOKwKwKOOK",
    "KAAAAAAAAK.","KAaAAAaAAK.","KAARRRAAaK.",
    "..KAK.KAK..","..KOKKOK...","..KtKKKtK.."]

UND_SPR = [
    ".KVVVVVVVk.","KVVvVVVvVVK","KVVVVVVVvVK",
    "KVKuVKuVvK","KVVVVVVVvVK","KVKKKKKKvVK",
    "KAAAAAAAAK.","KAaAAaAAaK.","KAARRAAaAK.",
    "..KAK.KAK..","..KVKKVK...","..KuKKKuK.."]

DEM_SPR = [
    "FKZZzZZKF.","KZZzZZzZZK","KZKZZZZZKZK",
    "KZKxZKxZZK","KZzZZZZZZK","KZKHZzHZZK",
    ".KZZZZZZK..","KZXxXxXZZK","KZZXxXZZZK",
    "..KZK.KZK..","..KZKFKZK..", "..KfKKKfK.."]

MONSTERS = [
    ("슬라임",   SLIME_SPR, "💚"),
    ("고블린",   GOB_SPR,   "👺"),
    ("오크전사", ORC_SPR,   "💪"),
    ("언데드",   UND_SPR,   "💀"),
    ("마왕",     DEM_SPR,   "😈"),
]

SKILLS = ["🔥","⚔️","🌪️"]

# ─── QUIZ DATA (3 questions per monster, need 3 correct to defeat) ────────
QUIZ = [
  # SLIME (floor 1)
  [{"q":"딸기의 달콤한 빨간 부위는 식물학적으로?","opts":["열매(과육)","꽃받침(화탁)","씨앗"],"ans":"꽃받침(화탁)","exp":"우리가 먹는 붉은 부위는 꽃받침이 발달한 것! 진짜 열매는 표면의 작은 씨앗들입니다."},
   {"q":"낙타 혹 속에 가득 들어있는 것은?","opts":["물","지방","근육"],"ans":"지방","exp":"낙타의 혹은 지방 저장소! 이 지방 분해로 에너지와 수분을 얻습니다."},
   {"q":"세계 최초로 생긴 패스트푸드 프랜차이즈는?","opts":["맥도날드","버거킹","A&W 레스토랑"],"ans":"A&W 레스토랑","exp":"A&W는 1919년 시작! 맥도날드는 1940년이에요."},
   {"q":"딸기는 장미과의 식물이다?","opts":["참이다","거짓이다","장미과가 아닌 딸기과"],"ans":"참이다","exp":"딸기는 장미과(Rosaceae)에 속합니다. 장미, 사과, 복숭아도 같은 과!"},
  ],
  # GOBLIN (floor 2)
  [{"q":"역사상 가장 많이 팔린 비디오 게임은?","opts":["마인크래프트","테트리스","GTA 5"],"ans":"마인크래프트","exp":"마인크래프트는 3억 장 이상 팔려 역대 1위입니다!"},
   {"q":"빛의 속도에 가장 가까운 것은?","opts":["약 30만 km/s","약 3만 km/s","약 3억 km/s"],"ans":"약 30만 km/s","exp":"빛의 속도는 진공에서 약 299,792 km/s ≈ 30만 km/s입니다."},
   {"q":"인체에서 가장 큰 기관(organ)은?","opts":["간","폐","피부"],"ans":"피부","exp":"피부는 약 1.5~2㎡로 인체에서 가장 큰 단일 기관입니다!"},
   {"q":"뇌의 몇 %를 평소에 사용한다는 '10% 설'은?","opts":["사실이다","근거 없는 미신","뇌과학적으로 50%만 맞다"],"ans":"근거 없는 미신","exp":"뇌의 10%만 사용한다는 건 완전한 미신입니다. 뇌 전체가 활발히 사용됩니다."},
  ],
  # ORC (floor 3)
  [{"q":"대한민국 천연기념물 제1호는?","opts":["진도 진돗개","대구 도동 측백나무 숲","울릉 향나무"],"ans":"대구 도동 측백나무 숲","exp":"1962년 지정된 대구 동구 도동 측백나무 숲이 천연기념물 1호입니다."},
   {"q":"태양계에서 위성(달) 수가 가장 많은 행성은?","opts":["목성","토성","천왕성"],"ans":"토성","exp":"2023년 기준 토성은 146개 이상의 위성을 보유해 태양계 최다입니다!"},
   {"q":"모국어 사용자 수 1위 언어는?","opts":["영어","스페인어","만다린(중국어)"],"ans":"만다린(중국어)","exp":"모국어 기준 만다린 약 9억 명 이상으로 1위! 영어는 총 사용자 기준 1위예요."},
   {"q":"올림픽 오륜기의 색깔은 몇 가지?","opts":["4가지","5가지","6가지"],"ans":"5가지","exp":"파랑, 노랑, 검정, 초록, 빨강 5색! 흰 바탕 포함하면 모든 국가 국기 색을 포함합니다."},
  ],
  # UNDEAD (floor 4)
  [{"q":"귀가 완전히 먼 후 작곡한 베토벤 교향곡은?","opts":["운명(5번)","전원(6번)","합창(9번)"],"ans":"합창(9번)","exp":"완전히 청력을 잃은 채로 합창 교향곡을 완성했습니다. 경이로운 일이죠!"},
   {"q":"셰익스피어 4대 비극이 아닌 것은?","opts":["햄릿","로미오와 줄리엣","맥베스"],"ans":"로미오와 줄리엣","exp":"4대 비극은 햄릿·오셀로·맥베스·리어왕! 로미오와 줄리엣은 포함되지 않습니다."},
   {"q":"피카소의 대표작 '게르니카'가 비판한 것은?","opts":["1차 세계대전","스페인 내전 중 폭격","프랑스 혁명"],"ans":"스페인 내전 중 폭격","exp":"게르니카는 1937년 스페인 내전 당시 나치 독일의 게르니카 마을 폭격에 항의한 작품입니다."},
   {"q":"최초로 노벨상을 두 번 받은 사람은?","opts":["아인슈타인","마리 퀴리","라이너스 폴링"],"ans":"마리 퀴리","exp":"마리 퀴리는 물리학상(1903)과 화학상(1911)을 수상한 최초의 2회 노벨상 수상자입니다!"},
  ],
  # DEMON LORD (floor 5)
  [{"q":"실제로 존재하지 않는 화학 원소는?","opts":["아인슈타이늄(Es)","닥터륨(Dc)","오가네손(Og)"],"ans":"닥터륨(Dc)","exp":"아인슈타이늄(99번)과 오가네손(118번)은 실존 원소! 닥터륨은 허구입니다."},
   {"q":"블랙홀에서 빠져나올 수 있는 것은?","opts":["빛","중력파","아무것도 없다"],"ans":"중력파","exp":"블랙홀에서 빛조차 탈출 불가! 그러나 중력파는 시공간 파동이라 블랙홀 충돌에서도 방출됩니다."},
   {"q":"인간의 DNA와 가장 가까운 동물은?","opts":["침팬지","돌고래","문어"],"ans":"침팬지","exp":"침팬지는 인간과 약 98.7%의 DNA를 공유합니다. 가장 가까운 친척이죠!"},
   {"q":"슈뢰딩거의 고양이 실험이 설명하는 것은?","opts":["고양이의 수명","양자 중첩의 역설","상대성 이론"],"ans":"양자 중첩의 역설","exp":"상자 안 고양이는 관찰 전까지 살아있고 죽어있는 두 상태가 중첩된다는 양자역학의 역설입니다!"},
  ],
]

HITS_NEEDED = 3
MAX_HP = 5

def init():
    st.session_state.update({
        "mon_idx":0, "mon_hits":0, "qpool_idx":0,
        "player_hp":MAX_HP, "answered":False, "last_correct":None,
        "mon_dying":False,
    })

if "mon_idx" not in st.session_state: init()

mi   = st.session_state.mon_idx
hits = st.session_state.mon_hits
qi   = st.session_state.qpool_idx
php  = st.session_state.player_hp

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Noto+Sans+KR:wght@700&display=swap');
.stApp{background:#0d0d1a;}
.pix{font-family:'Press Start 2P',cursive;}
.battle{
  background:linear-gradient(180deg,#1a0830 0%,#0d0d2a 60%,#050a05 100%);
  border:4px solid #ffd700;padding:18px 24px;
  display:flex;justify-content:space-between;align-items:flex-end;
  min-height:230px;position:relative;
  box-shadow:0 0 30px rgba(255,215,0,.2);
}
.battle::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(transparent,transparent 3px,rgba(0,0,0,.1) 4px);}
.hud{display:flex;justify-content:space-between;align-items:center;margin:6px 0;}
.hudlbl{font-family:'Press Start 2P',cursive;font-size:9px;color:#bbb;}
.hpbg{background:#222;border:2px solid #444;border-radius:2px;height:14px;flex:1;margin:0 8px;overflow:hidden;}
.hpfill{height:100%;transition:width .4s;}
.qcard{background:rgba(0,0,0,.7);border:3px solid #5c6bc0;border-radius:4px;
  padding:14px;color:#fffde7;font-family:'Noto Sans KR',sans-serif;font-size:16px;
  font-weight:700;margin:10px 0;}
.res-ok{background:rgba(0,255,100,.1);border:2px solid #00e676;border-radius:4px;
  padding:10px;color:#00e676;font-family:'Press Start 2P',cursive;font-size:10px;text-align:center;margin:6px 0;}
.res-ng{background:rgba(244,67,54,.1);border:2px solid #f44336;border-radius:4px;
  padding:10px;color:#ff5252;font-family:'Press Start 2P',cursive;font-size:10px;text-align:center;margin:6px 0;}
.exp{background:rgba(255,255,255,.05);border-left:4px solid #ffd700;border-radius:0 4px 4px 0;
  padding:10px 14px;color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:14px;margin:6px 0;}
.stButton>button{width:100%;border-radius:4px;border:3px solid #5c6bc0;background:#0d0d2a;
  color:#fff;font-family:'Noto Sans KR',sans-serif;font-weight:700;font-size:16px;
  box-shadow:3px 3px 0 #5c6bc0;transition:all .15s;padding:12px 8px;}
.stButton>button:hover{background:#5c6bc0;box-shadow:none;transform:translate(3px,3px);}
@keyframes hatk{0%{transform:translateX(0) scaleX(1);}40%{transform:translateX(30px) scaleX(1.15);}100%{transform:translateX(0) scaleX(1);}}
@keyframes hhit{0%{transform:translateX(0);filter:none;}30%{transform:translateX(-22px);filter:brightness(3) hue-rotate(180deg);}100%{transform:translateX(0);filter:none;}}
@keyframes mhit{0%{transform:translateX(0);filter:none;}30%{transform:translateX(18px);filter:brightness(4) saturate(0);}100%{transform:translateX(0);filter:none;}}
@keyframes matk{0%{transform:translateX(0);}40%{transform:translateX(-26px) scaleX(1.2);}100%{transform:translateX(0) scaleX(1);}}
@keyframes flt{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
@keyframes mdie{0%{opacity:1;transform:scale(1);}100%{opacity:0;transform:scale(.3) translateY(30px);}}
.flt{display:inline-block;animation:flt 2.2s ease-in-out infinite;}
.hatk{display:inline-block;animation:hatk .5s ease forwards;}
.hhit{display:inline-block;animation:hhit .5s ease forwards;}
.mflt{display:inline-block;animation:flt 2.8s ease-in-out infinite;}
.mhit{display:inline-block;animation:mhit .5s ease forwards;}
.matk{display:inline-block;animation:matk .5s ease forwards;}
.mdie{display:inline-block;animation:mdie .8s ease forwards;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="pix" style="color:#ffd700;font-size:12px;text-align:center;padding:8px 0;text-shadow:0 0 10px #ffd700">⚔ 마왕의 성 ⚔</p>', unsafe_allow_html=True)

# ── GAME OVER ──
if php <= 0:
    st.markdown('<div style="text-align:center;padding:30px"><p class="pix" style="color:#f44336;font-size:20px;text-shadow:0 0 20px #f44336">💀 GAME OVER 💀</p></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="pix" style="color:#ffd700;font-size:10px;text-align:center">{mi+1}층에서 쓰러졌습니다</p>', unsafe_allow_html=True)
    if st.button("🔄 다시 시작", use_container_width=True): init(); st.rerun()
    st.stop()

# ── CLEAR ──
if mi >= len(MONSTERS):
    st.balloons()
    st.markdown('<div style="text-align:center;padding:30px"><p class="pix" style="color:#ffd700;font-size:16px;text-shadow:0 0 20px #ffd700">👑 DUNGEON CLEAR! 👑</p></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="pix" style="color:#f48fb1;font-size:10px;text-align:center">잔여 HP: {"❤️"*php}{"🖤"*(MAX_HP-php)}</p>', unsafe_allow_html=True)
    if st.button("🔄 다시 도전", use_container_width=True): init(); st.rerun()
    st.stop()

mon_name, mon_spr, mon_ico = MONSTERS[mi]
q_pool = QUIZ[mi]
q = q_pool[qi % len(q_pool)]
dying = st.session_state.mon_dying
lc = st.session_state.last_correct

hero_spr = HA if lc is True else (HH if lc is False else HI)
hero_anim = "hatk" if lc is True else ("hhit" if lc is False else "flt")
mon_anim  = "mdie" if dying else ("mhit" if lc is True else ("matk" if lc is False else "mflt"))

hero_svg_str = svg(hero_spr, 10)
mon_svg_str  = svg(mon_spr, 12)

mon_hp_bar = hits
mon_hp_pct = int(hits / HITS_NEEDED * 100)
mon_bar_col = "#f44336" if mon_hp_pct>=66 else ("#FF9800" if mon_hp_pct>=33 else "#4CAF50")
plr_pct = int(php/MAX_HP*100)
plr_bar_col = "#4CAF50" if plr_pct>60 else ("#FF9800" if plr_pct>30 else "#f44336")

floor_names = ["1층 슬라임 동굴","2층 고블린 땅굴","3층 오크 요새","4층 언데드 묘지","5층 마왕의 옥좌 👑"]
st.markdown(f'<p class="pix" style="color:#b39ddb;font-size:9px;text-align:center;margin-bottom:4px">{floor_names[mi]}</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class="battle">
  <div style="text-align:center">
    <div class="{hero_anim}">{hero_svg_str}</div>
    <p class="pix" style="color:#81d4fa;font-size:8px;margin-top:6px">용사</p>
  </div>
  <div class="pix" style="color:#f44336;font-size:20px;align-self:center;text-shadow:0 0 10px #f44336">VS</div>
  <div style="text-align:center">
    <div class="{mon_anim}">{mon_svg_str}</div>
    <p class="pix" style="color:#ef9a9a;font-size:8px;margin-top:6px">{mon_ico} {mon_name}</p>
  </div>
</div>
""", unsafe_allow_html=True)

# HP bars
dmg_bullets = "💥"*hits + "⬜"*(HITS_NEEDED-hits)
st.markdown(f"""
<div class="hud">
  <span class="hudlbl">용사 {"❤️"*php}{"🖤"*(MAX_HP-php)}</span>
  <span class="hudlbl" style="color:#ffd700">몬스터 {dmg_bullets} ({hits}/{HITS_NEEDED})</span>
</div>
<div style="height:10px;background:#222;border:2px solid #444;border-radius:2px;margin-bottom:8px;overflow:hidden">
  <div style="height:100%;width:{mon_hp_pct}%;background:{mon_bar_col};transition:width .4s"></div>
</div>
""", unsafe_allow_html=True)

# Result msg
if dying:
    st.markdown(f'<div class="res-ok">🏆 {mon_name} 격파! 다음 층으로!</div>', unsafe_allow_html=True)
elif lc is True:
    st.markdown(f'<div class="res-ok">✅ 크리티컬 히트! ({hits}/{HITS_NEEDED} 데미지)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif lc is False:
    st.markdown(f'<div class="res-ng">💥 오답! 몬스터의 역습! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)

# Question & buttons
if not dying:
    st.markdown(f'<div class="qcard">❓ {q["q"]}</div>', unsafe_allow_html=True)

if not st.session_state.answered:
    c1, c2, c3 = st.columns(3)
    for col, opt, sk in zip([c1,c2,c3], q["opts"], SKILLS):
        with col:
            if st.button(f"{sk} {opt}", key=f"o_{mi}_{qi}_{opt}"):
                correct = (opt == q["ans"])
                st.session_state.answered = True
                st.session_state.last_correct = correct
                if correct:
                    new_hits = hits + 1
                    st.session_state.mon_hits = new_hits
                    if new_hits >= HITS_NEEDED:
                        st.session_state.mon_dying = True
                else:
                    st.session_state.player_hp = max(0, php - 1)
                st.rerun()
else:
    if dying:
        label = "👑 최후의 결전!"  if mi == len(MONSTERS)-2 else ("🏆 클리어!" if mi >= len(MONSTERS)-1 else f"⚔️ {floor_names[mi+1] if mi+1<len(floor_names) else '다음 층'}으로!")
        if st.button(label, type="primary", use_container_width=True):
            nxt = mi + 1
            if nxt >= len(MONSTERS):
                st.session_state.mon_idx = nxt  # triggers clear screen
            else:
                st.session_state.mon_idx = nxt
                st.session_state.mon_hits = 0
                st.session_state.qpool_idx = 0
            st.session_state.answered = False
            st.session_state.last_correct = None
            st.session_state.mon_dying = False
            st.rerun()
    else:
        if st.button("▶ 다음 문제", type="primary", use_container_width=True):
            st.session_state.qpool_idx = qi + 1
            st.session_state.answered = False
            st.session_state.last_correct = None
            st.rerun()

st.markdown(f'<p class="pix" style="color:#333;font-size:8px;text-align:center;margin-top:10px">FLOOR {mi+1}/5 | HP {"❤"*php}</p>', unsafe_allow_html=True)
