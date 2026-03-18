import streamlit as st
import random, os, base64, pathlib

st.set_page_config(page_title="마왕의 성", page_icon="⚔️", layout="centered")

def img_to_b64(path):
    p = pathlib.Path(path)
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return ""

_DIR = pathlib.Path(__file__).parent
OPENING_B64 = img_to_b64(_DIR / "quiz_opening.png")
ENDING_B64  = img_to_b64(_DIR / "quiz_ending.png")

P = {
    '.':None,'K':'#111','W':'#FFF',
    'c':'#CC1100','C':'#FF3322','n':'#FDBCB4','m':'#8B4513',
    'B':'#1565C0','b':'#1E88E5','Y':'#FFD700','S':'#E0E0E0','s':'#9E9E9E',
    'T':'#3E2723','t':'#6D4C41','R':'#E53935',
    'G':'#2ECC40','g':'#1A8026','e':'#FFEE00',
    'j':'#5D9B3A','J':'#3A6B20','p':'#7B1FA2','q':'#4A148C',
    'O':'#D84315','o':'#BF360C','A':'#546E7A','a':'#78909C',
    'U':'#E0E0E0','u':'#9E9E9E','V':'#1A237E','v':'#283593',
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

SLIME_SPR = ["..GGGGGG..","GGGGGgGGGG","GGGGGGGGgG",
    "GGeGGGGeGG","GGgGGGGgGG","GGGGGGGGgG","GKWWWWWWKg",".GGGGGGgG.","GGG.GG.GGG"]
GOB_SPR = [".KKKKKKKKK.",".JjjjJjjjJ.",".JjKJJKjjJ.",
    "JjKWGKWGjjJ","JjKOGKOGjjJ",".JjJJJJjJ.",".JjKwKwKjJ.","..KpBpBpK..","..KjK.KjK.",
    "..KjK.KjK..","..KJKkKJK.."]
ORC_SPR = ["..KOOOOKKK","KOOoOOOoOOK","KOOOOOOOoOK",
    "KOKnKKnKOK","KOOOOOOOoOK","KOKwKwKOOK","KAAAAAAAAK.","KAaAAAaAAK.","KAARRRAAaK.",
    "..KAK.KAK..","..KOKKOK...","..KtKKKtK.."]
UND_SPR = [".KVVVVVVVk.","KVVvVVVvVVK","KVVVVVVVvVK",
    "KVKuVKuVvK","KVVVVVVVvVK","KVKKKKKKvVK","KAAAAAAAAK.","KAaAAaAAaK.","KAARRAAaAK.",
    "..KAK.KAK..","..KVKKVK...","..KuKKKuK.."]
DEM_SPR = ["FKZZzZZKF.","KZZzZZzZZK","KZKZZZZZKZK",
    "KZKxZKxZZK","KZzZZZZZZK","KZKHZzHZZK",".KZZZZZZK..","KZXxXxXZZK","KZZXxXZZZK",
    "..KZK.KZK..","..KZKFKZK..","..KfKKKfK.."]

MONSTERS = [("슬라임",SLIME_SPR,"💚"),("고블린",GOB_SPR,"👺"),
            ("오크전사",ORC_SPR,"💪"),("언데드",UND_SPR,"💀"),("마왕",DEM_SPR,"😈")]
SKILLS = ["🔥","⚔️","🌪️"]

# 몬스터별 보상 아이템
REWARDS = [
    ("🗡️ 슬라임 단검", "슬라임을 처치하고 끈적한 단검을 얻었다!"),
    ("🛡️ 고블린 방패", "고블린이 쓰던 방패를 빼앗았다!"),
    ("💪 오크의 완력", "오크의 힘이 용사에게 깃들었다!"),
    ("👻 유령 망토", "언데드의 신비로운 망토를 획득했다!"),
    ("👑 마왕의 왕관", "전설의 왕관을 손에 넣었다!"),
]

# 콤보 칭찬 메시지
COMBO_MSG = ["","","🔥 2콤보! 잘한다!","⚡ 3콤보! 천재인가?!","🌟 4콤보! 무적이야!",
             "💎 5콤보!! 전설의 용사!!","🏆 6콤보!!! 역대급!!!"]
# 오답 격려 메시지
ENCOURAGE = ["괜찮아! 다시 도전해보자! 💪","아깝다! 다음엔 맞출 수 있어! 🍀",
             "실수는 누구나 해! 힘내! ⭐","틀려도 괜찮아, 새로운 걸 배웠잖아! 📚",
             "용사는 포기하지 않아! 다시 가보자! 🗡️"]

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
        "combo":0, "max_combo":0,
        "coins":0, "total_correct":0, "total_wrong":0,
        "hints_left":MAX_HINTS, "hint_used_this_q":False,
        "collected_items":[],
        "encourage_msg":"",
    })

if "screen" not in st.session_state: init()

# ─── CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Noto+Sans+KR:wght@700&display=swap');
.stApp{background:#0d0d1a;}
.pix{font-family:'Press Start 2P',cursive;}
.battle{background:linear-gradient(180deg,#1a0830 0%,#0d0d2a 60%,#050a05 100%);
  border:4px solid #ffd700;padding:18px 24px;
  display:flex;justify-content:space-between;align-items:flex-end;
  min-height:230px;position:relative;box-shadow:0 0 30px rgba(255,215,0,.2);}
.battle::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(transparent,transparent 3px,rgba(0,0,0,.1) 4px);}
.hud{display:flex;justify-content:space-between;align-items:center;margin:6px 0;}
.hudlbl{font-family:'Press Start 2P',cursive;font-size:9px;color:#bbb;}
.qcard{background:rgba(0,0,0,.7);border:3px solid #5c6bc0;border-radius:4px;
  padding:14px;color:#fffde7;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700;margin:10px 0;}
.res-ok{background:rgba(0,255,100,.1);border:2px solid #00e676;border-radius:4px;
  padding:10px;color:#00e676;font-family:'Press Start 2P',cursive;font-size:10px;text-align:center;margin:6px 0;}
.res-ng{background:rgba(244,67,54,.1);border:2px solid #f44336;border-radius:4px;
  padding:10px;color:#ff5252;font-family:'Press Start 2P',cursive;font-size:10px;text-align:center;margin:6px 0;}
.exp{background:rgba(255,255,255,.05);border-left:4px solid #ffd700;border-radius:0 4px 4px 0;
  padding:10px 14px;color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:14px;margin:6px 0;}
.combo-box{background:linear-gradient(135deg,rgba(255,165,0,.2),rgba(255,215,0,.1));
  border:2px solid #ffa500;border-radius:6px;padding:8px;text-align:center;margin:4px 0;
  animation:comboPulse .6s ease-in-out;}
.coin-box{background:rgba(255,215,0,.1);border:1px solid #ffd700;border-radius:4px;
  padding:6px 12px;display:inline-block;margin:4px;}
.reward-box{background:linear-gradient(135deg,rgba(156,39,176,.2),rgba(103,58,183,.2));
  border:2px solid #ab47bc;border-radius:8px;padding:12px;text-align:center;margin:8px 0;
  animation:rewardPop .5s ease;}
.encourage{background:rgba(33,150,243,.1);border:1px solid #42a5f5;border-radius:6px;
  padding:8px 12px;color:#90caf9;font-family:'Noto Sans KR',sans-serif;font-size:14px;text-align:center;margin:4px 0;}
.items-bar{background:rgba(255,255,255,.05);border:1px solid #444;border-radius:4px;
  padding:6px 10px;display:flex;gap:8px;flex-wrap:wrap;margin:4px 0;}
.item-badge{background:#2d2d44;border:1px solid #666;border-radius:4px;padding:3px 8px;
  font-size:12px;color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;}
.progress-bar{background:rgba(0,0,0,.3);border-radius:10px;height:20px;margin:8px 0;overflow:hidden;
  border:2px solid #444;}
.progress-fill{height:100%;border-radius:8px;transition:width .5s;
  background:linear-gradient(90deg,#4CAF50,#8BC34A,#CDDC39,#FFC107,#FF9800);
  display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;
  font-family:'Press Start 2P',cursive;text-shadow:1px 1px 2px rgba(0,0,0,.5);}
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
@keyframes pulse{0%,100%{text-shadow:0 0 10px #ffd700;}50%{text-shadow:0 0 30px #ffd700,0 0 60px #ff9800;}}
@keyframes comboPulse{0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}}
@keyframes rewardPop{0%{transform:scale(0) rotate(-10deg);opacity:0;}100%{transform:scale(1) rotate(0);opacity:1;}}
.flt{display:inline-block;animation:flt 2.2s ease-in-out infinite;}
.hatk{display:inline-block;animation:hatk .5s ease forwards;}
.hhit{display:inline-block;animation:hhit .5s ease forwards;}
.mflt{display:inline-block;animation:flt 2.8s ease-in-out infinite;}
.mhit{display:inline-block;animation:mhit .5s ease forwards;}
.matk{display:inline-block;animation:matk .5s ease forwards;}
.mdie{display:inline-block;animation:mdie .8s ease forwards;}
.pulse{animation:pulse 1.5s ease-in-out infinite;}
</style>
""", unsafe_allow_html=True)

screen = st.session_state.screen

# ════════════════════════════════════════════════════════════
# 🎬 TITLE SCREEN
# ════════════════════════════════════════════════════════════
if screen == "title":
    if OPENING_B64:
        st.markdown(f'<img src="{OPENING_B64}" style="width:100%;border:4px solid #ffd700;border-radius:6px;box-shadow:0 0 40px rgba(255,215,0,.4);margin-bottom:8px">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px">
      <p class="pix pulse" style="color:#ffd700;font-size:15px;margin:0">⚔ 마왕의 성 ⚔</p>
      <p class="pix" style="color:#b39ddb;font-size:9px;margin-top:12px">QUIZ DUNGEON</p>
    </div>
    """, unsafe_allow_html=True)

    # 이름 입력
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        name = st.text_input("🦸 용사님의 이름을 입력하세요!", value="", max_chars=10,
                             placeholder="이름을 입력해주세요")

    st.markdown("""
    <div style="text-align:center;padding:4px 0 8px">
      <p style="color:#aaa;font-family:'Noto Sans KR',sans-serif;font-size:14px;margin-top:4px">
         퀴즈를 풀어 몬스터를 물리치고 마왕의 성을 정복하라!<br>
         <b>3번 정답</b>을 맞추면 몬스터를 격파합니다.<br>
         오답 시 <b>❤️ 한 개</b>가 깎입니다. HP 5개로 도전!<br><br>
         🧪 <b>힌트 포션</b>: 2회 사용 가능! 오답 하나를 없애줘요.<br>
         ⚡ <b>콤보 시스템</b>: 연속 정답 시 보너스 코인!<br>
         🎁 <b>보상 아이템</b>: 몬스터를 처치하면 아이템 획득!
      </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🗡️  게임 시작!", use_container_width=True, type="primary"):
            hero = name.strip() if name.strip() else "용사"
            st.session_state.hero_name = hero
            st.session_state.screen = "game"
            st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# 💀 GAME OVER
# ════════════════════════════════════════════════════════════
mi  = st.session_state.mon_idx
php = st.session_state.player_hp
hero_name = st.session_state.hero_name

if php <= 0:
    st.markdown(f"""
    <div style="text-align:center;padding:20px">
      <p class="pix" style="color:#f44336;font-size:20px;text-shadow:0 0 20px #f44336">💀 GAME OVER 💀</p>
      <p style="color:#aaa;font-family:'Noto Sans KR',sans-serif;font-size:15px">{hero_name}(이)가 {mi+1}층에서 쓰러졌습니다...</p>
      <p style="color:#bbb;font-family:'Noto Sans KR',sans-serif;font-size:13px">더 많은 상식을 쌓고 다시 도전하세요!</p>
      <p style="color:#ffd700;font-family:'Noto Sans KR',sans-serif;font-size:14px;margin-top:10px">
        📊 전적: 정답 {st.session_state.total_correct}개 | 오답 {st.session_state.total_wrong}개 | 💰 {st.session_state.coins} 코인 | ⚡ 최대콤보 {st.session_state.max_combo}
      </p>
    </div>""", unsafe_allow_html=True)
    if st.session_state.collected_items:
        items_html = " ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
        st.markdown(f'<div class="items-bar" style="justify-content:center">{items_html}</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔄 처음으로", use_container_width=True):
            init(); st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# 🏆 CLEAR SCREEN
# ════════════════════════════════════════════════════════════
if mi >= len(MONSTERS):
    st.balloons()
    if ENDING_B64:
        st.markdown(f'<img src="{ENDING_B64}" style="width:100%;border:4px solid #ffd700;border-radius:6px;box-shadow:0 0 40px rgba(255,215,0,.4);margin-bottom:8px">', unsafe_allow_html=True)
    rank = "S" if php==MAX_HP else ("A" if php>=4 else ("B" if php>=3 else ("C" if php>=2 else "D")))
    rank_color = {"S":"#FFD700","A":"#C0C0C0","B":"#CD7F32","C":"#78909C","D":"#f44336"}[rank]
    rank_title = {"S":"전설의 용사","A":"위대한 모험가","B":"숙련된 전사","C":"초보 영웅","D":"수습 용사"}[rank]
    tc = st.session_state.total_correct
    tw = st.session_state.total_wrong
    coins = st.session_state.coins
    mc = st.session_state.max_combo
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0">
      <p class="pix pulse" style="color:#ffd700;font-size:16px">👑 DUNGEON CLEAR! 👑</p>
      <p style="color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:16px;margin-top:10px">
         <b>{hero_name}</b>(이)가 마왕을 물리치고 성을 탈환했습니다!</p>
      <p class="pix" style="color:{rank_color};font-size:24px;margin:10px 0">RANK: {rank}</p>
      <p style="color:#b39ddb;font-family:'Noto Sans KR',sans-serif;font-size:14px">🏅 칭호: {rank_title}</p>
      <p style="color:#f48fb1;font-family:'Noto Sans KR',sans-serif;font-size:15px">
         잔여 HP: {"❤️"*php}{"🖤"*(MAX_HP-php)}</p>
    </div>""", unsafe_allow_html=True)

    # 전투 요약
    st.markdown(f"""
    <div style="background:rgba(255,255,255,.05);border:2px solid #5c6bc0;border-radius:8px;padding:16px;margin:8px 0">
      <p class="pix" style="color:#81d4fa;font-size:10px;text-align:center;margin-bottom:10px">📊 모험 기록</p>
      <div style="display:flex;justify-content:space-around;flex-wrap:wrap;gap:8px;text-align:center">
        <div class="coin-box"><span style="color:#4CAF50;font-size:18px;font-weight:bold">✅ {tc}</span><br><span style="color:#aaa;font-size:11px">정답</span></div>
        <div class="coin-box"><span style="color:#f44336;font-size:18px;font-weight:bold">❌ {tw}</span><br><span style="color:#aaa;font-size:11px">오답</span></div>
        <div class="coin-box"><span style="color:#ffd700;font-size:18px;font-weight:bold">💰 {coins}</span><br><span style="color:#aaa;font-size:11px">코인</span></div>
        <div class="coin-box"><span style="color:#ff9800;font-size:18px;font-weight:bold">⚡ {mc}</span><br><span style="color:#aaa;font-size:11px">최대콤보</span></div>
      </div>
    </div>""", unsafe_allow_html=True)

    # 수집 아이템
    if st.session_state.collected_items:
        st.markdown('<p class="pix" style="color:#ab47bc;font-size:9px;text-align:center;margin-top:10px">🎒 수집한 아이템</p>', unsafe_allow_html=True)
        items_html = " ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
        st.markdown(f'<div class="items-bar" style="justify-content:center">{items_html}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔄 다시 도전", use_container_width=True, type="primary"):
            init(); st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════
# ⚔️ GAME SCREEN
# ════════════════════════════════════════════════════════════
hits   = st.session_state.mon_hits
qi     = st.session_state.qpool_idx
dying  = st.session_state.mon_dying
lc     = st.session_state.last_correct
quiz   = st.session_state.shuffled_quiz
combo  = st.session_state.combo
coins  = st.session_state.coins

mon_name, mon_spr, mon_ico = MONSTERS[mi]
q_pool = quiz[mi]
q = q_pool[qi % len(q_pool)]

hero_spr  = HA if lc is True else (HH if lc is False else HI)
hero_anim = "hatk" if lc is True else ("hhit" if lc is False else "flt")
mon_anim  = "mdie" if dying else ("mhit" if lc is True else ("matk" if lc is False else "mflt"))

hero_svg_str = svg(hero_spr, 10)
mon_svg_str  = svg(mon_spr, 12)

mon_hp_pct  = int(hits/HITS_NEEDED*100)
mon_bar_col = "#f44336" if mon_hp_pct>=66 else ("#FF9800" if mon_hp_pct>=33 else "#4CAF50")

floor_names = ["1층 슬라임 동굴","2층 고블린 땅굴","3층 오크 요새","4층 언데드 묘지","5층 마왕의 옥좌 👑"]

# 전체 진행도
overall_pct = int((mi * HITS_NEEDED + hits) / (len(MONSTERS) * HITS_NEEDED) * 100)
st.markdown(f"""
<div class="progress-bar">
  <div class="progress-fill" style="width:{overall_pct}%">{overall_pct}%</div>
</div>""", unsafe_allow_html=True)

st.markdown(f'<p class="pix" style="color:#ffd700;font-size:10px;text-align:center;padding:4px 0;text-shadow:0 0 8px #ffd700">⚔ 마왕의 성 ⚔</p>', unsafe_allow_html=True)
st.markdown(f'<p class="pix" style="color:#b39ddb;font-size:9px;text-align:center;margin-bottom:4px">{floor_names[mi]}</p>', unsafe_allow_html=True)

# 상단 HUD: 코인 + 콤보 + 힌트
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin:4px 0">
  <span class="coin-box" style="font-size:12px">💰 {coins} 코인</span>
  <span class="coin-box" style="font-size:12px">⚡ {combo} 콤보</span>
  <span class="coin-box" style="font-size:12px">🧪 포션 {st.session_state.hints_left}개</span>
</div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="battle">
  <div style="text-align:center">
    <div class="{hero_anim}">{hero_svg_str}</div>
    <p class="pix" style="color:#81d4fa;font-size:8px;margin-top:6px">{hero_name}</p>
  </div>
  <div class="pix" style="color:#f44336;font-size:20px;align-self:center;text-shadow:0 0 10px #f44336">VS</div>
  <div style="text-align:center">
    <div class="{mon_anim}">{mon_svg_str}</div>
    <p class="pix" style="color:#ef9a9a;font-size:8px;margin-top:6px">{mon_ico} {mon_name}</p>
  </div>
</div>""", unsafe_allow_html=True)

dmg_bullets = "💥"*hits + "⬜"*(HITS_NEEDED-hits)
st.markdown(f"""
<div class="hud">
  <span class="hudlbl">{hero_name} {"❤️"*php}{"🖤"*(MAX_HP-php)}</span>
  <span class="hudlbl" style="color:#ffd700">몬스터 {dmg_bullets}</span>
</div>
<div style="height:10px;background:#222;border:2px solid #444;border-radius:2px;margin-bottom:8px;overflow:hidden">
  <div style="height:100%;width:{mon_hp_pct}%;background:{mon_bar_col};transition:width .4s"></div>
</div>""", unsafe_allow_html=True)

# 수집 아이템 표시
if st.session_state.collected_items:
    items_html = " ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
    st.markdown(f'<div class="items-bar">🎒 {items_html}</div>', unsafe_allow_html=True)

if dying:
    reward_name, reward_desc = REWARDS[mi]
    st.markdown(f'<div class="res-ok">🏆 {mon_name} 격파! 다음 층으로!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="reward-box"><span style="font-size:28px">{reward_name.split()[0]}</span><br><span style="color:#e0e0e0;font-family:\'Noto Sans KR\',sans-serif;font-size:13px">{reward_desc}</span></div>', unsafe_allow_html=True)
elif lc is True:
    st.markdown(f'<div class="res-ok">✅ 크리티컬 히트! ({hits}/{HITS_NEEDED} 데미지) +{10 + combo*5} 코인!</div>', unsafe_allow_html=True)
    if combo >= 2:
        cmsg = COMBO_MSG[min(combo, len(COMBO_MSG)-1)]
        st.markdown(f'<div class="combo-box"><span style="color:#ffa500;font-family:\'Press Start 2P\',cursive;font-size:11px">{cmsg}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif lc is False:
    st.markdown(f'<div class="res-ng">💥 오답! 몬스터의 역습! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="encourage">{st.session_state.encourage_msg}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)

if not dying:
    st.markdown(f'<div class="qcard">❓ {q["q"]}</div>', unsafe_allow_html=True)

if not st.session_state.answered:
    # 힌트 버튼
    if not st.session_state.hint_used_this_q and st.session_state.hints_left > 0:
        hcol1, hcol2, hcol3 = st.columns([1,2,1])
        with hcol2:
            if st.button(f"🧪 힌트 포션 사용 (남은 {st.session_state.hints_left}개)", key="hint_btn"):
                st.session_state.hints_left -= 1
                st.session_state.hint_used_this_q = True
                st.rerun()

    # 선택지 (힌트 사용 시 오답 하나 비활성화)
    opts = q["opts"]
    disabled_opt = None
    if st.session_state.hint_used_this_q:
        wrong_opts = [o for o in opts if o != q["ans"]]
        if wrong_opts:
            random.seed(f"{mi}_{qi}_hint")
            disabled_opt = random.choice(wrong_opts)

    c1,c2,c3 = st.columns(3)
    for col,opt,sk in zip([c1,c2,c3], opts, SKILLS):
        with col:
            is_disabled = (opt == disabled_opt)
            if is_disabled:
                st.button(f"🚫 ~~{opt}~~", key=f"o_{mi}_{qi}_{opt}", disabled=True)
            else:
                if st.button(f"{sk} {opt}", key=f"o_{mi}_{qi}_{opt}"):
                    correct = (opt == q["ans"])
                    st.session_state.answered = True
                    st.session_state.last_correct = correct
                    if correct:
                        new_combo = combo + 1
                        st.session_state.combo = new_combo
                        st.session_state.max_combo = max(st.session_state.max_combo, new_combo)
                        coin_gain = 10 + new_combo * 5
                        st.session_state.coins += coin_gain
                        st.session_state.total_correct += 1
                        nh = hits + 1
                        st.session_state.mon_hits = nh
                        if nh >= HITS_NEEDED:
                            st.session_state.mon_dying = True
                            reward_name, _ = REWARDS[mi]
                            st.session_state.collected_items.append(reward_name)
                            st.session_state.coins += 50  # 보스 보너스
                    else:
                        st.session_state.combo = 0
                        st.session_state.total_wrong += 1
                        st.session_state.player_hp = max(0, php-1)
                        st.session_state.encourage_msg = random.choice(ENCOURAGE)
                    st.rerun()
else:
    if dying:
        nxt = mi + 1
        label = "🏆 클리어!" if nxt>=len(MONSTERS) else (f"👑 최후의 결전!" if nxt==len(MONSTERS)-1 else f"⚔️ {floor_names[nxt]}으로!")
        if st.button(label, type="primary", use_container_width=True):
            st.session_state.mon_idx = nxt
            st.session_state.mon_hits = 0
            st.session_state.qpool_idx = 0
            st.session_state.answered = False
            st.session_state.last_correct = None
            st.session_state.mon_dying = False
            st.session_state.hint_used_this_q = False
            st.rerun()
    else:
        if st.button("▶ 다음 문제", type="primary", use_container_width=True):
            st.session_state.qpool_idx = qi+1
            st.session_state.answered = False
            st.session_state.last_correct = None
            st.session_state.hint_used_this_q = False
            st.rerun()

st.markdown(f'<p class="pix" style="color:#333;font-size:8px;text-align:center;margin-top:10px">FLOOR {mi+1}/5 | HP {"❤"*php} | 💰 {coins}</p>', unsafe_allow_html=True)
