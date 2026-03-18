import streamlit as st
import random, os, base64, pathlib

st.set_page_config(page_title="마왕의 성", page_icon="⚔️", layout="centered")

def img_to_b64(path):
    p = pathlib.Path(path)
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return ""

_DIR = pathlib.Path(__file__).parent
OPENING_B64  = img_to_b64(_DIR / "quiz_opening.png")
ENDING_B64   = img_to_b64(_DIR / "quiz_ending.png")
GAMEOVER_B64 = img_to_b64(_DIR / "quiz_gameover.png")

# 캐릭터 이미지 로드
HERO_B64    = img_to_b64(_DIR / "sprite_hero.png")
SLIME_B64   = img_to_b64(_DIR / "sprite_slime.png")
GOBLIN_B64  = img_to_b64(_DIR / "sprite_goblin.png")
ORC_B64     = img_to_b64(_DIR / "sprite_orc.png")
UNDEAD_B64  = img_to_b64(_DIR / "sprite_undead.png")
DEMON_B64   = img_to_b64(_DIR / "sprite_demon.png")

MONSTERS = [
    ("슬라임", SLIME_B64, "💚"),
    ("고블린", GOBLIN_B64, "👺"),
    ("오크전사", ORC_B64, "💪"),
    ("언데드", UNDEAD_B64, "💀"),
    ("마왕", DEMON_B64, "😈"),
]
SKILLS = ["🔥","⚔️","🌪️"]

REWARDS = [
    ("🗡️ 슬라임 단검", "정답 시 코인 +5 보너스!", "coin_bonus"),
    ("🛡️ 고블린 방패", "오답 1회 데미지 무효!", "shield"),
    ("💪 오크의 완력", "다음 몬스터 2타 격파!", "power_hit"),
    ("👻 유령 망토",   "힌트 포션 1개 추가!", "hint_bonus"),
    ("👑 마왕의 왕관", "클리어 시 코인 2배!", "coin_double"),
]

COMBO_MSG = ["","","🔥 2콤보! 잘한다!","⚡ 3콤보! 천재인가?!","🌟 4콤보! 무적이야!","💎 5콤보!! 전설의 용사!!","🏆 6콤보!!! 역대급!!!"]
ENCOURAGE = ["괜찮아! 다시 도전해보자! 💪","아깝다! 다음엔 맞출 수 있어! 🍀","실수는 누구나 해! 힘내! ⭐","틀려도 괜찮아, 새로운 걸 배웠잖아! 📚","용사는 포기하지 않아! 다시 가보자! 🗡️"]

QUIZ_POOL = [
  [{"q":"딸기의 달콤한 빨간 부위는 식물학적으로?","opts":["열매(과육)","꽃받침(화탁)","씨앗"],"ans":"꽃받침(화탁)","exp":"우리가 먹는 붉은 부위는 꽃받침이 발달한 것! 진짜 열매는 표면의 작은 씨앗들입니다."},
   {"q":"낙타 혹 속에 가득 들어있는 것은?","opts":["물","지방","근육"],"ans":"지방","exp":"낙타의 혹은 지방 저장소! 이 지방 분해로 에너지와 수분을 얻습니다."},
   {"q":"세계 최초로 생긴 패스트푸드 프랜차이즈는?","opts":["맥도날드","버거킹","A&W 레스토랑"],"ans":"A&W 레스토랑","exp":"A&W는 1919년 시작! 맥도날드는 1940년이에요."},
   {"q":"딸기는 장미과의 식물이다?","opts":["참이다","거짓이다","장미과가 아닌 딸기과"],"ans":"참이다","exp":"딸기는 장미과(Rosaceae)에 속합니다. 장미, 사과, 복숭아도 같은 과!"}],
  [{"q":"역사상 가장 많이 팔린 비디오 게임은?","opts":["마인크래프트","테트리스","GTA 5"],"ans":"마인크래프트","exp":"마인크래프트는 3억 장 이상 팔려 역대 1위입니다!"},
   {"q":"빛의 속도에 가장 가까운 것은?","opts":["약 30만 km/s","약 3만 km/s","약 3억 km/s"],"ans":"약 30만 km/s","exp":"빛의 속도는 진공에서 약 299,792 km/s ≈ 30만 km/s입니다."},
   {"q":"인체에서 가장 큰 기관(organ)은?","opts":["간","폐","피부"],"ans":"피부","exp":"피부는 약 1.5~2㎡로 인체에서 가장 큰 단일 기관입니다!"},
   {"q":"뇌의 10% 설은?","opts":["사실이다","근거 없는 미신","50%만 맞다"],"ans":"근거 없는 미신","exp":"뇌의 10%만 사용한다는 건 완전한 미신! 뇌 전체가 활발히 사용됩니다."}],
  [{"q":"대한민국 천연기념물 제1호는?","opts":["진도 진돗개","대구 도동 측백나무 숲","울릉 향나무"],"ans":"대구 도동 측백나무 숲","exp":"1962년 지정된 대구 동구 도동 측백나무 숲이 천연기념물 1호입니다."},
   {"q":"태양계에서 위성(달) 수가 가장 많은 행성은?","opts":["목성","토성","천왕성"],"ans":"토성","exp":"2023년 기준 토성은 146개 이상의 위성을 보유해 태양계 최다입니다!"},
   {"q":"모국어 사용자 수 1위 언어는?","opts":["영어","스페인어","만다린(중국어)"],"ans":"만다린(중국어)","exp":"모국어 기준 만다린 약 9억 명 이상으로 1위! 영어는 총 사용자 기준 1위예요."},
   {"q":"올림픽 오륜기의 색깔은 몇 가지?","opts":["4가지","5가지","6가지"],"ans":"5가지","exp":"파랑, 노랑, 검정, 초록, 빨강 5색! 흰 바탕 포함하면 모든 국가 국기 색을 포함합니다."}],
  [{"q":"귀가 완전히 먼 후 베토벤이 작곡한 교향곡은?","opts":["운명(5번)","전원(6번)","합창(9번)"],"ans":"합창(9번)","exp":"완전히 청력을 잃은 채로 합창 교향곡을 완성했습니다. 경이로운 일이죠!"},
   {"q":"셰익스피어 4대 비극이 아닌 것은?","opts":["햄릿","로미오와 줄리엣","맥베스"],"ans":"로미오와 줄리엣","exp":"4대 비극은 햄릿·오셀로·맥베스·리어왕! 로미오와 줄리엣은 포함되지 않습니다."},
   {"q":"피카소 '게르니카'가 비판한 것은?","opts":["1차 세계대전","스페인 내전 중 폭격","프랑스 혁명"],"ans":"스페인 내전 중 폭격","exp":"게르니카는 1937년 스페인 내전 당시 나치 독일의 폭격에 항의한 작품입니다."},
   {"q":"최초로 노벨상을 두 번 받은 사람은?","opts":["아인슈타인","마리 퀴리","라이너스 폴링"],"ans":"마리 퀴리","exp":"마리 퀴리는 물리학상(1903)과 화학상(1911)을 수상한 최초의 2회 수상자입니다!"}],
  [{"q":"실제로 존재하지 않는 화학 원소는?","opts":["아인슈타이늄(Es)","닥터륨(Dc)","오가네손(Og)"],"ans":"닥터륨(Dc)","exp":"아인슈타이늄(99번)과 오가네손(118번)은 실존 원소! 닥터륨은 허구입니다."},
   {"q":"블랙홀에서 빠져나올 수 있는 것은?","opts":["빛","중력파","아무것도 없다"],"ans":"중력파","exp":"블랙홀에서 빛조차 탈출 불가! 그러나 중력파는 시공간 파동이라 방출됩니다."},
   {"q":"인간의 DNA와 가장 가까운 동물은?","opts":["침팬지","돌고래","문어"],"ans":"침팬지","exp":"침팬지는 인간과 약 98.7%의 DNA를 공유합니다. 가장 가까운 친척이죠!"},
   {"q":"슈뢰딩거의 고양이 실험이 설명하는 것은?","opts":["고양이의 수명","양자 중첩의 역설","상대성 이론"],"ans":"양자 중첩의 역설","exp":"관찰 전까지 살아있고 죽어있는 두 상태가 중첩된다는 양자역학의 역설입니다!"}],
]

HITS_NEEDED = 3
MAX_HP = 5
MAX_HINTS = 2

def init():
    shuffled = [random.sample(pool, len(pool)) for pool in QUIZ_POOL]
    st.session_state.update({
        "screen":"title",
        "mon_idx":0,"mon_hits":0,"qpool_idx":0,
        "player_hp":MAX_HP,"answered":False,"last_correct":None,
        "mon_dying":False,"shuffled_quiz":shuffled,
        "hero_name":"용사",
        "combo":0,"max_combo":0,
        "coins":0,"total_correct":0,"total_wrong":0,
        "hints_left":MAX_HINTS,"hint_used_this_q":False,
        "collected_items":[],"collected_effects":[],
        "encourage_msg":"",
        "shield_active":False,"shield_used":False,
    })

if "screen" not in st.session_state: init()
if "collected_effects" not in st.session_state: st.session_state.collected_effects = []
if "shield_active" not in st.session_state: st.session_state.shield_active = False
if "shield_used" not in st.session_state: st.session_state.shield_used = False

# ─── CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Noto+Sans+KR:wght@400;700;900&display=swap');
.stApp{background:#0d0d1a;}
.pix{font-family:'Press Start 2P',cursive;}

/* 배틀 필드 */
.battle{
  background:linear-gradient(180deg,#1a0830 0%,#12102e 40%,#0a1a10 80%,#050a05 100%);
  border:5px solid #ffd700;padding:20px 16px;
  display:flex;justify-content:space-between;align-items:flex-end;
  min-height:300px;position:relative;
  box-shadow:0 0 50px rgba(255,215,0,.2),inset 0 -40px 60px rgba(0,0,0,.4);
  border-radius:10px;overflow:hidden;}
.battle::before{content:'';position:absolute;bottom:0;left:0;right:0;height:60px;
  background:linear-gradient(0deg,#1a2810,transparent);pointer-events:none;}
.battle::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(transparent,transparent 3px,rgba(0,0,0,.06) 4px);border-radius:10px;}

/* 캐릭터 이미지 */
.char-img{width:140px;height:140px;object-fit:contain;image-rendering:pixelated;
  filter:drop-shadow(0 4px 12px rgba(0,0,0,.5));}
.mon-img{width:160px;height:160px;object-fit:contain;image-rendering:pixelated;
  filter:drop-shadow(0 4px 16px rgba(255,0,0,.3));}

/* HUD */
.hud{display:flex;justify-content:space-between;align-items:center;margin:8px 0;}
.hudlbl{font-family:'Press Start 2P',cursive;font-size:11px;color:#ccc;}
.qcard{background:rgba(0,0,0,.75);border:3px solid #5c6bc0;border-radius:10px;
  padding:20px;color:#fffde7;font-family:'Noto Sans KR',sans-serif;font-size:20px;font-weight:700;margin:12px 0;line-height:1.6;}
.res-ok{background:rgba(0,255,100,.12);border:2px solid #00e676;border-radius:8px;
  padding:14px;color:#00e676;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;text-align:center;margin:8px 0;}
.res-ng{background:rgba(244,67,54,.12);border:2px solid #f44336;border-radius:8px;
  padding:14px;color:#ff5252;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;text-align:center;margin:8px 0;}
.res-shield{background:rgba(33,150,243,.15);border:2px solid #42a5f5;border-radius:8px;
  padding:14px;color:#64b5f6;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;text-align:center;margin:8px 0;}
.exp{background:rgba(255,255,255,.06);border-left:5px solid #ffd700;border-radius:0 8px 8px 0;
  padding:14px 18px;color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:16px;margin:8px 0;line-height:1.6;}
.combo-box{background:linear-gradient(135deg,rgba(255,165,0,.25),rgba(255,215,0,.15));
  border:2px solid #ffa500;border-radius:8px;padding:12px;text-align:center;margin:6px 0;
  animation:comboPulse .6s ease-in-out;}

/* HUD 바 */
.hud-bar{display:flex;justify-content:space-between;align-items:center;margin:8px 0;gap:8px;}
.hud-item{flex:1;text-align:center;padding:10px 6px;border-radius:10px;font-family:'Noto Sans KR',sans-serif;
  font-size:15px;font-weight:700;}
.hud-coin{background:rgba(255,193,7,.2);border:2px solid #ffc107;color:#ffd740;}
.hud-combo{background:rgba(255,152,0,.2);border:2px solid #ff9800;color:#ffab40;}
.hud-potion{background:rgba(76,175,80,.2);border:2px solid #4CAF50;color:#69f0ae;}
.hud-shield{background:rgba(33,150,243,.2);border:2px solid #42a5f5;color:#64b5f6;}

.reward-box{background:linear-gradient(135deg,rgba(156,39,176,.25),rgba(103,58,183,.25));
  border:2px solid #ab47bc;border-radius:12px;padding:16px;text-align:center;margin:10px 0;
  animation:rewardPop .5s ease;}
.effect-tag{display:inline-block;background:rgba(255,215,0,.12);border:1px solid #ffd740;border-radius:6px;
  padding:4px 10px;margin:2px 4px;font-size:12px;color:#ffd740;font-family:'Noto Sans KR',sans-serif;}
.encourage{background:rgba(33,150,243,.12);border:1px solid #42a5f5;border-radius:8px;
  padding:12px 16px;color:#90caf9;font-family:'Noto Sans KR',sans-serif;font-size:16px;text-align:center;margin:6px 0;}
.items-bar{background:rgba(255,255,255,.05);border:1px solid #555;border-radius:8px;
  padding:8px 12px;display:flex;gap:10px;flex-wrap:wrap;margin:6px 0;align-items:center;}
.item-badge{background:#2d2d44;border:1px solid #777;border-radius:6px;padding:5px 10px;
  font-size:14px;color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;}
.progress-bar{background:rgba(0,0,0,.3);border-radius:12px;height:26px;margin:10px 0;overflow:hidden;border:2px solid #555;}
.progress-fill{height:100%;border-radius:10px;transition:width .5s;
  background:linear-gradient(90deg,#4CAF50,#8BC34A,#CDDC39,#FFC107,#FF9800);
  display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff;
  font-family:'Press Start 2P',cursive;text-shadow:1px 1px 2px rgba(0,0,0,.5);}
.shop-card{background:rgba(255,255,255,.06);border:2px solid #7c4dff;border-radius:12px;
  padding:14px;text-align:center;transition:all .2s;}
.shop-card:hover{background:rgba(124,77,255,.15);border-color:#b388ff;}
.stButton>button{width:100%;border-radius:8px;border:3px solid #5c6bc0;background:#0d0d2a;
  color:#fff;font-family:'Noto Sans KR',sans-serif;font-weight:700;font-size:18px;
  box-shadow:3px 3px 0 #5c6bc0;transition:all .15s;padding:14px 10px;}
.stButton>button:hover{background:#5c6bc0;box-shadow:none;transform:translate(3px,3px);}

/* 애니메이션 */
@keyframes heroIdle{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes heroAtk{0%{transform:translateX(0) scale(1);}30%{transform:translateX(50px) scale(1.1);}60%{transform:translateX(30px) scale(1);}100%{transform:translateX(0) scale(1);}}
@keyframes heroHit{0%{transform:translateX(0);filter:none;}20%{transform:translateX(-30px);filter:brightness(2) hue-rotate(180deg);}50%{transform:translateX(-15px);filter:brightness(1.5);}100%{transform:translateX(0);filter:none;}}
@keyframes monIdle{0%,100%{transform:translateY(0) scale(1);}50%{transform:translateY(-6px) scale(1.02);}}
@keyframes monHit{0%{transform:translateX(0);filter:none;}20%{transform:translateX(30px);filter:brightness(3) saturate(0);}50%{transform:translateX(15px);filter:brightness(1.5) saturate(.5);}100%{transform:translateX(0);filter:none;}}
@keyframes monAtk{0%{transform:translateX(0) scale(1);}30%{transform:translateX(-40px) scale(1.15);}60%{transform:translateX(-20px) scale(1.05);}100%{transform:translateX(0) scale(1);}}
@keyframes monDie{0%{opacity:1;transform:scale(1) rotate(0);}50%{opacity:.5;transform:scale(.7) rotate(5deg);}100%{opacity:0;transform:scale(.2) rotate(10deg) translateY(40px);}}
@keyframes pulse{0%,100%{text-shadow:0 0 10px #ffd700;}50%{text-shadow:0 0 30px #ffd700,0 0 60px #ff9800;}}
@keyframes comboPulse{0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}}
@keyframes rewardPop{0%{transform:scale(0) rotate(-10deg);opacity:0;}100%{transform:scale(1) rotate(0);opacity:1;}}

.hero-idle{animation:heroIdle 2s ease-in-out infinite;}
.hero-atk{animation:heroAtk .6s ease forwards;}
.hero-hit{animation:heroHit .6s ease forwards;}
.mon-idle{animation:monIdle 2.5s ease-in-out infinite;}
.mon-hit{animation:monHit .6s ease forwards;}
.mon-atk{animation:monAtk .6s ease forwards;}
.mon-die{animation:monDie .8s ease forwards;}
.pulse{animation:pulse 1.5s ease-in-out infinite;}
</style>
""", unsafe_allow_html=True)

screen = st.session_state.screen

# ════════════════════════════════════════════════════════════
# 🎬 TITLE SCREEN
# ════════════════════════════════════════════════════════════
if screen == "title":
    if OPENING_B64:
        st.markdown(f'<img src="{OPENING_B64}" style="width:100%;border:4px solid #ffd700;border-radius:10px;box-shadow:0 0 40px rgba(255,215,0,.4);margin-bottom:8px">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px">
      <p class="pix pulse" style="color:#ffd700;font-size:22px;margin:0">⚔ 마왕의 성 ⚔</p>
      <p class="pix" style="color:#b39ddb;font-size:13px;margin-top:14px">QUIZ DUNGEON</p>
    </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        name = st.text_input("🦸 용사님의 이름을 입력하세요!", value="", max_chars=10, placeholder="이름을 입력해주세요")
    st.markdown("""
    <div style="text-align:center;padding:4px 0 8px">
      <p style="color:#ccc;font-family:'Noto Sans KR',sans-serif;font-size:15px;line-height:1.8">
         퀴즈를 풀어 몬스터를 물리치고 마왕의 성을 정복하라!<br>
         <b style="color:#ff8a80">3번 정답</b>을 맞추면 몬스터를 격파!<br>
         오답 시 <b style="color:#ff8a80">❤️ 한 개</b> 감소. HP 5개로 도전!<br><br>
         🧪 <b style="color:#69f0ae">힌트 포션</b> · ⚡ <b style="color:#ffab40">콤보</b> · 🛒 <b style="color:#b388ff">상점</b> · 🎁 <b style="color:#f48fb1">아이템</b>
      </p>
    </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🗡️  게임 시작!", use_container_width=True, type="primary"):
            st.session_state.hero_name = name.strip() if name.strip() else "용사"
            st.session_state.screen = "game"
            st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# 🛒 SHOP SCREEN
# ════════════════════════════════════════════════════════════
if screen == "shop":
    mi = st.session_state.mon_idx
    coins = st.session_state.coins
    floor_names = ["1층 슬라임 동굴","2층 고블린 땅굴","3층 오크 요새","4층 언데드 묘지","5층 마왕의 옥좌 👑"]
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0">
      <p class="pix" style="color:#b388ff;font-size:18px">🛒 마법 상점 🛒</p>
      <p style="color:#ccc;font-family:'Noto Sans KR',sans-serif;font-size:16px;margin-top:8px">다음 전투 전에 아이템을 구매하세요!</p>
      <p style="color:#ffd740;font-family:'Noto Sans KR',sans-serif;font-size:20px;font-weight:700;margin-top:6px">💰 보유 코인: {coins}</p>
    </div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="shop-card"><div style="font-size:36px">🧪</div>
          <p style="color:#69f0ae;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;margin:6px 0">힌트 포션</p>
          <p style="color:#aaa;font-size:13px;font-family:'Noto Sans KR',sans-serif">오답 하나 제거</p>
          <p style="color:#ffd740;font-size:15px;font-weight:700">💰 30 코인</p>
          <p style="color:#888;font-size:12px">현재 {st.session_state.hints_left}개</p></div>""", unsafe_allow_html=True)
        if st.button("🧪 구매" if coins>=30 else "🚫 부족", key="buy_hint", disabled=coins<30):
            st.session_state.coins -= 30; st.session_state.hints_left += 1; st.rerun()
    with c2:
        can2 = coins>=50 and st.session_state.player_hp<MAX_HP
        st.markdown(f"""<div class="shop-card"><div style="font-size:36px">❤️</div>
          <p style="color:#ff8a80;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;margin:6px 0">HP 회복약</p>
          <p style="color:#aaa;font-size:13px;font-family:'Noto Sans KR',sans-serif">HP 1칸 회복</p>
          <p style="color:#ffd740;font-size:15px;font-weight:700">💰 50 코인</p>
          <p style="color:#888;font-size:12px">{"❤️"*st.session_state.player_hp}{"🖤"*(MAX_HP-st.session_state.player_hp)}</p></div>""", unsafe_allow_html=True)
        l2 = "❤️ 구매" if can2 else ("💚 HP 가득" if st.session_state.player_hp>=MAX_HP else "🚫 부족")
        if st.button(l2, key="buy_hp", disabled=not can2):
            st.session_state.coins -= 50; st.session_state.player_hp = min(MAX_HP, st.session_state.player_hp+1); st.rerun()
    with c3:
        has_s = st.session_state.shield_active; can3 = coins>=40 and not has_s
        st.markdown(f"""<div class="shop-card"><div style="font-size:36px">🛡️</div>
          <p style="color:#64b5f6;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;margin:6px 0">보호막</p>
          <p style="color:#aaa;font-size:13px;font-family:'Noto Sans KR',sans-serif">오답 1회 무효</p>
          <p style="color:#ffd740;font-size:15px;font-weight:700">💰 40 코인</p>
          <p style="color:#888;font-size:12px">{"✅ 장착 중" if has_s else "❌ 미장착"}</p></div>""", unsafe_allow_html=True)
        if st.button("🛡️ 구매" if can3 else ("✅ 있음" if has_s else "🚫 부족"), key="buy_shield", disabled=not can3):
            st.session_state.coins -= 40; st.session_state.shield_active = True; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        nf = floor_names[mi] if mi<len(floor_names) else "최종 결전"
        if st.button(f"⚔️ {nf}으로 출발!", type="primary", use_container_width=True):
            st.session_state.screen = "game"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# 💀 GAME OVER
# ════════════════════════════════════════════════════════════
mi  = st.session_state.mon_idx
php = st.session_state.player_hp
hero_name = st.session_state.hero_name

if php <= 0:
    if GAMEOVER_B64:
        st.markdown(f'<img src="{GAMEOVER_B64}" style="width:100%;border:4px solid #f44336;border-radius:10px;box-shadow:0 0 40px rgba(244,67,54,.4);margin-bottom:10px">', unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;padding:20px">
      <p class="pix" style="color:#f44336;font-size:26px;text-shadow:0 0 20px #f44336">💀 GAME OVER 💀</p>
      <p style="color:#ccc;font-family:'Noto Sans KR',sans-serif;font-size:18px;margin-top:8px">{hero_name}(이)가 {mi+1}층에서 쓰러졌습니다...</p>
      <p style="color:#ffd700;font-family:'Noto Sans KR',sans-serif;font-size:15px;margin-top:12px">
        📊 정답 {st.session_state.total_correct} · 오답 {st.session_state.total_wrong} · 💰 {st.session_state.coins} · ⚡ 최대콤보 {st.session_state.max_combo}</p>
    </div>""", unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("🔄 처음부터 다시!", use_container_width=True): init(); st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# 🏆 CLEAR SCREEN
# ════════════════════════════════════════════════════════════
if mi >= len(MONSTERS):
    st.balloons()
    if ENDING_B64:
        st.markdown(f'<img src="{ENDING_B64}" style="width:100%;border:4px solid #ffd700;border-radius:10px;box-shadow:0 0 40px rgba(255,215,0,.4);margin-bottom:8px">', unsafe_allow_html=True)
    rank = "S" if php==MAX_HP else ("A" if php>=4 else ("B" if php>=3 else ("C" if php>=2 else "D")))
    rank_color = {"S":"#FFD700","A":"#C0C0C0","B":"#CD7F32","C":"#78909C","D":"#f44336"}[rank]
    rank_title = {"S":"전설의 용사","A":"위대한 모험가","B":"숙련된 전사","C":"초보 영웅","D":"수습 용사"}[rank]
    tc,tw = st.session_state.total_correct, st.session_state.total_wrong
    coins = st.session_state.coins * (2 if "coin_double" in st.session_state.collected_effects else 1)
    mc = st.session_state.max_combo
    st.markdown(f"""<div style="text-align:center;padding:16px 0">
      <p class="pix pulse" style="color:#ffd700;font-size:22px">👑 DUNGEON CLEAR! 👑</p>
      <p style="color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:20px;margin-top:12px"><b>{hero_name}</b>(이)가 마왕을 물리치고 성을 탈환했습니다!</p>
      <p class="pix" style="color:{rank_color};font-size:32px;margin:12px 0">RANK: {rank}</p>
      <p style="color:#b39ddb;font-family:'Noto Sans KR',sans-serif;font-size:16px">🏅 {rank_title}</p>
      <p style="color:#f48fb1;font-family:'Noto Sans KR',sans-serif;font-size:18px">HP: {"❤️"*php}{"🖤"*(MAX_HP-php)}</p>
    </div>""", unsafe_allow_html=True)
    coin_label = f"💰{coins}(2배!)" if "coin_double" in st.session_state.collected_effects else f"💰{coins}"
    st.markdown(f"""<div style="background:rgba(255,255,255,.05);border:2px solid #5c6bc0;border-radius:10px;padding:16px;margin:8px 0">
      <p class="pix" style="color:#81d4fa;font-size:11px;text-align:center;margin-bottom:12px">📊 모험 기록</p>
      <div style="display:flex;justify-content:space-around;flex-wrap:wrap;gap:8px;text-align:center">
        <div style="padding:8px 14px"><span style="color:#4CAF50;font-size:20px;font-weight:bold">✅{tc}</span><br><span style="color:#aaa;font-size:12px">정답</span></div>
        <div style="padding:8px 14px"><span style="color:#f44336;font-size:20px;font-weight:bold">❌{tw}</span><br><span style="color:#aaa;font-size:12px">오답</span></div>
        <div style="padding:8px 14px"><span style="color:#ffd700;font-size:20px;font-weight:bold">{coin_label}</span><br><span style="color:#aaa;font-size:12px">코인</span></div>
        <div style="padding:8px 14px"><span style="color:#ff9800;font-size:20px;font-weight:bold">⚡{mc}</span><br><span style="color:#aaa;font-size:12px">최대콤보</span></div>
      </div></div>""", unsafe_allow_html=True)
    if st.session_state.collected_items:
        items_html = " ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
        st.markdown(f'<p class="pix" style="color:#ab47bc;font-size:10px;text-align:center;margin-top:10px">🎒 수집 아이템</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="items-bar" style="justify-content:center">{items_html}</div>', unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("🔄 다시 도전", use_container_width=True, type="primary"): init(); st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# ⚔️ GAME SCREEN
# ════════════════════════════════════════════════════════════
hits  = st.session_state.mon_hits
qi    = st.session_state.qpool_idx
dying = st.session_state.mon_dying
lc    = st.session_state.last_correct
quiz  = st.session_state.shuffled_quiz
combo = st.session_state.combo
coins = st.session_state.coins

mon_name, mon_b64, mon_ico = MONSTERS[mi]
q_pool = quiz[mi]
q = q_pool[qi % len(q_pool)]

cur_hits_needed = 2 if ("power_hit" in st.session_state.collected_effects and mi > 2) else HITS_NEEDED

# 애니메이션 결정
hero_anim = "hero-atk" if lc is True else ("hero-hit" if lc is False else "hero-idle")
mon_anim  = "mon-die" if dying else ("mon-hit" if lc is True else ("mon-atk" if lc is False else "mon-idle"))

mon_hp_pct  = int(hits/cur_hits_needed*100)
mon_bar_col = "#f44336" if mon_hp_pct>=66 else ("#FF9800" if mon_hp_pct>=33 else "#4CAF50")

floor_names = ["1층 슬라임 동굴","2층 고블린 땅굴","3층 오크 요새","4층 언데드 묘지","5층 마왕의 옥좌 👑"]

# 진행도
overall_pct = int((mi*HITS_NEEDED+hits)/(len(MONSTERS)*HITS_NEEDED)*100)
st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{overall_pct}%">{overall_pct}%</div></div>', unsafe_allow_html=True)

st.markdown(f'<p class="pix" style="color:#ffd700;font-size:14px;text-align:center;padding:6px 0;text-shadow:0 0 10px #ffd700">⚔ 마왕의 성 ⚔</p>', unsafe_allow_html=True)
st.markdown(f'<p class="pix" style="color:#b39ddb;font-size:12px;text-align:center;margin-bottom:6px">{floor_names[mi]}</p>', unsafe_allow_html=True)

# HUD
shield_html = '<div class="hud-item hud-shield">🛡️ ON</div>' if st.session_state.shield_active else ""
st.markdown(f"""<div class="hud-bar">
  <div class="hud-item hud-coin">💰 {coins}</div>
  <div class="hud-item hud-combo">⚡ {combo}콤보</div>
  <div class="hud-item hud-potion">🧪 {st.session_state.hints_left}개</div>
  {shield_html}
</div>""", unsafe_allow_html=True)

# 패시브 효과
if st.session_state.collected_effects:
    em = {"coin_bonus":"🗡️코인+5","shield":"🛡️무효","power_hit":"💪2타","hint_bonus":"👻포션+1","coin_double":"👑2배"}
    eff_html = "".join([f'<span class="effect-tag">{em.get(e,e)}</span>' for e in st.session_state.collected_effects])
    st.markdown(f'<div style="text-align:center;margin:4px 0">{eff_html}</div>', unsafe_allow_html=True)

# 🎮 배틀 필드 (이미지 기반!)
hero_img_tag = f'<img src="{HERO_B64}" class="char-img">' if HERO_B64 else '<div style="font-size:60px">🦸</div>'
mon_img_tag  = f'<img src="{mon_b64}" class="mon-img">' if mon_b64 else f'<div style="font-size:60px">{mon_ico}</div>'

st.markdown(f"""
<div class="battle">
  <div style="text-align:center;z-index:1">
    <div class="{hero_anim}">{hero_img_tag}</div>
    <p class="pix" style="color:#81d4fa;font-size:11px;margin-top:8px">{hero_name}</p>
  </div>
  <div class="pix" style="color:#f44336;font-size:28px;align-self:center;text-shadow:0 0 16px #f44336;z-index:1">VS</div>
  <div style="text-align:center;z-index:1">
    <div class="{mon_anim}">{mon_img_tag}</div>
    <p class="pix" style="color:#ef9a9a;font-size:11px;margin-top:8px">{mon_ico} {mon_name}</p>
  </div>
</div>""", unsafe_allow_html=True)

dmg_bullets = "💥"*hits + "⬜"*(cur_hits_needed-hits)
st.markdown(f"""<div class="hud">
  <span class="hudlbl">{hero_name} {"❤️"*php}{"🖤"*(MAX_HP-php)}</span>
  <span class="hudlbl" style="color:#ffd700">{mon_name} {dmg_bullets}</span>
</div>
<div style="height:14px;background:#222;border:2px solid #444;border-radius:4px;margin-bottom:8px;overflow:hidden">
  <div style="height:100%;width:{mon_hp_pct}%;background:{mon_bar_col};transition:width .4s"></div>
</div>""", unsafe_allow_html=True)

if st.session_state.collected_items:
    items_html = " ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
    st.markdown(f'<div class="items-bar">🎒 {items_html}</div>', unsafe_allow_html=True)

# 결과 표시
if lc == "shielded":
    st.markdown(f'<div class="res-shield">🛡️ 보호막이 데미지를 막았다! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif dying:
    rn, rd, _ = REWARDS[mi]
    st.markdown(f'<div class="res-ok">🏆 {mon_name} 격파!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="reward-box"><span style="font-size:28px">{rn.split()[0]}</span><br><span style="color:#e0e0e0;font-family:\'Noto Sans KR\',sans-serif;font-size:14px">{rd}</span></div>', unsafe_allow_html=True)
elif lc is True:
    ce = "+5" if "coin_bonus" in st.session_state.collected_effects else ""
    st.markdown(f'<div class="res-ok">✅ 크리티컬 히트! ({hits}/{cur_hits_needed}) +{10+combo*5}코인 {ce}</div>', unsafe_allow_html=True)
    if combo >= 2:
        st.markdown(f'<div class="combo-box"><span style="color:#ffa500;font-family:\'Press Start 2P\',cursive;font-size:12px">{COMBO_MSG[min(combo,len(COMBO_MSG)-1)]}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif lc is False:
    st.markdown(f'<div class="res-ng">💥 오답! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="encourage">{st.session_state.encourage_msg}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)

if not dying:
    st.markdown(f'<div class="qcard">❓ {q["q"]}</div>', unsafe_allow_html=True)

if not st.session_state.answered:
    if not st.session_state.hint_used_this_q and st.session_state.hints_left > 0:
        hc1,hc2,hc3 = st.columns([1,2,1])
        with hc2:
            if st.button(f"🧪 힌트 사용 (남은 {st.session_state.hints_left}개)", key="hint_btn"):
                st.session_state.hints_left -= 1; st.session_state.hint_used_this_q = True; st.rerun()
    opts = q["opts"]; disabled_opt = None
    if st.session_state.hint_used_this_q:
        wrong = [o for o in opts if o != q["ans"]]
        if wrong: random.seed(f"{mi}_{qi}_h"); disabled_opt = random.choice(wrong)
    c1,c2,c3 = st.columns(3)
    for col,opt,sk in zip([c1,c2,c3], opts, SKILLS):
        with col:
            if opt == disabled_opt:
                st.button(f"🚫 {opt}", key=f"o_{mi}_{qi}_{opt}", disabled=True)
            elif st.button(f"{sk} {opt}", key=f"o_{mi}_{qi}_{opt}"):
                correct = (opt == q["ans"])
                st.session_state.answered = True
                if correct:
                    nc = combo+1; st.session_state.combo = nc
                    st.session_state.max_combo = max(st.session_state.max_combo, nc)
                    cg = 10 + nc*5 + (5 if "coin_bonus" in st.session_state.collected_effects else 0)
                    st.session_state.coins += cg; st.session_state.total_correct += 1
                    st.session_state.last_correct = True
                    nh = hits+1; st.session_state.mon_hits = nh
                    if nh >= cur_hits_needed:
                        st.session_state.mon_dying = True
                        rn, _, ek = REWARDS[mi]
                        st.session_state.collected_items.append(rn)
                        st.session_state.collected_effects.append(ek)
                        st.session_state.coins += 50
                        if ek == "hint_bonus": st.session_state.hints_left += 1
                        if ek == "shield" and not st.session_state.shield_active: st.session_state.shield_active = True
                else:
                    st.session_state.combo = 0; st.session_state.total_wrong += 1
                    if st.session_state.shield_active and not st.session_state.shield_used:
                        st.session_state.shield_active = False; st.session_state.shield_used = True
                        st.session_state.last_correct = "shielded"
                    else:
                        st.session_state.player_hp = max(0,php-1); st.session_state.last_correct = False
                    st.session_state.encourage_msg = random.choice(ENCOURAGE)
                st.rerun()
else:
    if dying:
        nxt = mi+1
        if nxt >= len(MONSTERS):
            if st.button("🏆 클리어!", type="primary", use_container_width=True):
                st.session_state.update({"mon_idx":nxt,"mon_hits":0,"qpool_idx":0,"answered":False,"last_correct":None,"mon_dying":False,"hint_used_this_q":False,"shield_used":False})
                st.rerun()
        else:
            if st.button("🛒 상점 → 다음 층!", type="primary", use_container_width=True):
                st.session_state.update({"mon_idx":nxt,"mon_hits":0,"qpool_idx":0,"answered":False,"last_correct":None,"mon_dying":False,"hint_used_this_q":False,"shield_used":False,"screen":"shop"})
                st.rerun()
    else:
        if st.button("▶ 다음 문제", type="primary", use_container_width=True):
            st.session_state.update({"qpool_idx":qi+1,"answered":False,"last_correct":None,"hint_used_this_q":False})
            st.rerun()
