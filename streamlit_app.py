import streamlit as st
import streamlit.components.v1 as components
import random, os, base64, pathlib, time, json, html as _html

st.set_page_config(page_title="마왕의 성", page_icon="⚔️", layout="centered")

def img_to_b64(path):
    p = pathlib.Path(path)
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return ""

_DIR = pathlib.Path(__file__).parent
OPENING_B64   = img_to_b64(_DIR / "quiz_opening.png")
ENDING_B64    = img_to_b64(_DIR / "quiz_ending.png")
GAMEOVER_B64  = img_to_b64(_DIR / "quiz_gameover.png")
BATTLE_BG_B64 = img_to_b64(_DIR / "battle_bg.png")
LB_PATH = _DIR / "leaderboard.json"

def load_lb():
    if LB_PATH.exists():
        try: return json.loads(LB_PATH.read_text(encoding="utf-8"))
        except: return []
    return []

def save_lb(lb):
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:5]
    LB_PATH.write_text(json.dumps(lb, ensure_ascii=False), encoding="utf-8")

# ────────────────────────────────────────────────────────────
# 업그레이드 도트 스프라이트 (더 많은 색상 · 디테일 · 음영)
# ────────────────────────────────────────────────────────────
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
    'l':'#64B5F6','L':'#1976D2','w':'#FFCCBC',
    'i':'#FF7043','I':'#BF360C','d':'#FFB74D','D':'#F57C00',
    'k':'#222','h':'#CE93D8','y':'#FFF176',
    'r':'#EF5350',
}

def svg(rows, px=10):
    mw = max(len(r) for r in rows)
    out = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            c = P.get(ch)
            if c:
                out.append(f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}" fill="{c}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{mw*px}" height="{len(rows)*px}" '
            f'style="image-rendering:pixelated;display:block;">{"".join(out)}</svg>')

# 용사 (아이들 / 공격 / 피격) — 더 큰 크기, 더 많은 색상
HERO_IDLE = [
    "....KccccK....",
    "...KcCCCCcK...",
    "...KcCCCCcK...",
    "..KKnnnnnnKK..",
    "..KnKnnnnKnK..",
    "..KnnwnnwnnK..",
    "..KnnmmmnnK...",
    "..KnnnnnnnK...",
    ".KBBBBBBBBK...",
    ".KBbBYBBbBK...",
    ".KBBBBBBBBKsS.",
    ".KBBBBBBBBKsS.",
    "..KBBBBBBK....",
    "..KBK..KBK....",
    "..KBK..KBK....",
    "..KTK..KTK....",
]
HERO_ATK = [
    "....KccccK........",
    "...KcCCCCcK.......",
    "...KcCCCCcK.......",
    "..KKnnnnnnKK......",
    "..KnKnnnnK.K......",
    "..KnnwnnwnnK......",
    "..KnmmmmmnnK......",
    "..KnnnnnnnKsSSSSS.",
    ".KBBBBBBBBKSSSSSS.",
    ".KBbBYBBbBKssssss.",
    ".KBBBBBBBBKssss...",
    "..KBBBBBBK........",
    "..KBK..KBK........",
    "..KBK..KBK........",
    "..KTK..KTK........",
]
HERO_HIT = [
    "....KccccK....",
    "...KcCCCCcK...",
    "...KcCCCCcK...",
    "..KKnnnnnnKK..",
    "..KnKKnnKKnK..",
    "..KnnwnnwnnK..",
    "..KnKKKKKnnK..",
    "..KnnnnnnnK...",
    ".KBBBBBBBBK...",
    ".KBbBYBBbBK...",
    ".KBBBBBBBBK...",
    "..KBBBBBBK....",
    "..KBK..KBK....",
    "..KBK..KBK....",
    "..KTK..KTK....",
]

SLIME_SPR = [
    "....KKKK....",
    "..KGGGGGK...",
    ".KGGgGGGGGK.",
    "KGGGGGGGGgGK",
    "KGGeGGGGeGGK",
    "KGGgGGGGgGGK",
    "KGGGGGGGGGgK",
    "KGKWWWWWWKgK",
    ".KGGGGGGgGK.",
    "..KGGGGGGK..",
    "..KGK..KGK..",
]
GOB_SPR = [
    "...KKKKKKK...",
    "..KJjjjJjjK..",
    ".KJjjJJjjjJK.",
    "KJjKWgKWgjjJK",
    "KJjKOgKOgjjJK",
    ".KJjjJJjjjJK.",
    ".KJjKwKwKjJK.",
    "..KKpBpBpKK..",
    "...KjjjjjK...",
    "..KjK...KjK..",
    "..KJK...KJK..",
]
ORC_SPR = [
    "...KOOOOOOKKK.",
    "..KOOoOOOoOOK.",
    ".KOOOOOOOOoOK.",
    ".KOKnKKKnKOK..",
    ".KOOOOOOOoOK..",
    ".KOKwwKwwKOK..",
    "KKAAAAAAAAKKK.",
    "KAaAAAAaAAAaK.",
    "KAAARRRRAAAAaK",
    "..KAK...KAK...",
    "..KOKK.KKOK...",
    "..KtKK.KKtK...",
]
UND_SPR = [
    "..KVVVVVVVKK..",
    ".KVVvVVVvVVK..",
    ".KVVVVVVVvVK..",
    ".KVKuVVKuVvK..",
    ".KVVVVVVVvVK..",
    ".KVKKKKKKvVK..",
    "KKAAAAAAAAAKK.",
    "KAaAAAAaAAAaK.",
    "KAARRRRAAAAaK.",
    "..KAK...KAK...",
    "..KVKK.KKVK...",
    "..KuKK.KKuK...",
]
DEM_SPR = [
    "FKK......KKF..",
    "FKZZzZZzZZKF..",
    "KZZZzZZzZZZZK.",
    "KZKZZZZZZKZzK.",
    "KZKxZZKxZZZZK.",
    "KZzZZZZZZZzZK.",
    "KZKHZzHZZZZZK.",
    ".KZZZZZZZZZK..",
    "KZXxXxXxXZZK..",
    "KZZZXxXZZZZK..",
    "..KZK...KZK...",
    "..KZKF.FKZK...",
    "..KfKK.KKfK...",
]

MONSTERS = [
    ("슬라임", SLIME_SPR, "💚"),
    ("고블린", GOB_SPR, "👺"),
    ("오크전사", ORC_SPR, "💪"),
    ("언데드", UND_SPR, "💀"),
    ("마왕", DEM_SPR, "😈"),
]
SKILLS = ["🔥","⚔️","🌪️"]

REWARDS = [
    ("🗡️ 슬라임 단검", "정답 시 코인 +5 보너스!", "coin_bonus"),
    ("🛡️ 고블린 방패", "오답 1회 데미지 무효!", "shield"),
    ("💪 오크의 완력", "4층부터 몬스터 2타 격파!", "power_hit"),
    ("👻 유령 망토",   "힌트 포션 1개 추가!", "hint_bonus"),
    ("👑 마왕의 왕관", "클리어 시 코인 2배!", "coin_double"),
]

COMBO_MSG = ["","","🔥 2콤보! 잘한다!","⚡ 3콤보! 천재인가?!","🌟 4콤보! 무적이야!","💎 5콤보!! 전설의 용사!!","🏆 6콤보!!! 역대급!!!"]
ENCOURAGE = ["괜찮아! 다시 도전해보자! 💪","아깝다! 다음엔 맞출 수 있어! 🍀","실수는 누구나 해! 힘내! ⭐","틀려도 괜찮아, 새로운 걸 배웠잖아! 📚","용사는 포기하지 않아! 🗡️"]

# ────────────────────────────────────────────────────────────
# 퀴즈 풀 (확장)
# ────────────────────────────────────────────────────────────
QUIZ_POOL = [
  # 1층 — 생활/음식/자연 상식
  [{"q":"딸기의 달콤한 빨간 부위는 식물학적으로?","opts":["열매(과육)","꽃받침(화탁)","씨앗"],"ans":"꽃받침(화탁)","exp":"우리가 먹는 붉은 부위는 꽃받침이 발달한 것! 진짜 열매는 표면의 작은 씨앗들입니다."},
   {"q":"낙타 혹 속에 가득 들어있는 것은?","opts":["물","지방","근육"],"ans":"지방","exp":"낙타의 혹은 지방 저장소! 이 지방 분해로 에너지와 수분을 얻습니다."},
   {"q":"바나나는 나무에서 자란다?","opts":["맞다","틀리다, 풀이다","틀리다, 덩굴이다"],"ans":"틀리다, 풀이다","exp":"바나나는 나무가 아니라 세계 최대의 '풀'입니다! 줄기처럼 보이는 건 잎이 말린 거예요."},
   {"q":"꿀은 절대 상하지 않는다?","opts":["맞다","틀리다","1년만 보관 가능"],"ans":"맞다","exp":"꿀은 수분이 적고 산성이라 세균이 살 수 없어요. 3000년 전 이집트 꿀도 먹을 수 있었답니다!"},
   {"q":"세계에서 가장 매운 고추는?","opts":["하바네로","캐롤라이나 리퍼","청양고추"],"ans":"캐롤라이나 리퍼","exp":"캐롤라이나 리퍼는 220만 스코빌! 청양고추(1만)의 200배 이상입니다."},
   {"q":"토마토는 과일일까 채소일까?","opts":["과일","채소","둘 다"],"ans":"둘 다","exp":"식물학적으로는 과일(열매), 요리·법적으로는 채소로 분류됩니다. 미국 대법원이 1893년 채소로 판결했어요!"}],

  # 2층 — 과학/우주/기술
  [{"q":"빛의 속도에 가장 가까운 것은?","opts":["약 30만 km/s","약 3만 km/s","약 3억 km/s"],"ans":"약 30만 km/s","exp":"빛의 속도는 진공에서 약 299,792 km/s ≈ 30만 km/s입니다."},
   {"q":"인체에서 가장 큰 기관(organ)은?","opts":["간","폐","피부"],"ans":"피부","exp":"피부는 약 1.5~2㎡로 인체에서 가장 큰 단일 기관입니다!"},
   {"q":"태양에서 지구까지 빛이 도달하는 시간은?","opts":["약 8분","약 1시간","약 1초"],"ans":"약 8분","exp":"정확히는 약 8분 20초! 태양-지구 거리 약 1.5억 km를 빛의 속도로 나눈 값이에요."},
   {"q":"다이아몬드와 연필심(흑연)의 공통점은?","opts":["같은 원소(탄소)","같은 경도","같은 색"],"ans":"같은 원소(탄소)","exp":"둘 다 순수한 탄소! 원자 배열만 다릅니다. 다이아몬드는 정사면체, 흑연은 층상 구조예요."},
   {"q":"물이 얼면 부피가?","opts":["늘어난다","줄어든다","변하지 않는다"],"ans":"늘어난다","exp":"물은 얼면 부피가 약 9% 커집니다. 그래서 얼음이 물에 뜨는 거예요!"},
   {"q":"번개와 천둥 중 실제로 먼저 발생하는 것은?","opts":["동시에 발생","번개가 먼저","천둥이 먼저"],"ans":"동시에 발생","exp":"동시에 발생하지만 빛이 소리보다 빨라서 번개가 먼저 보이는 것입니다!"}],

  # 3층 — 지리/역사/문화
  [{"q":"대한민국 천연기념물 제1호는?","opts":["진도 진돗개","대구 도동 측백나무 숲","울릉 향나무"],"ans":"대구 도동 측백나무 숲","exp":"1962년 지정된 대구 동구 도동 측백나무 숲이 천연기념물 1호입니다."},
   {"q":"세계에서 가장 큰 사막은?","opts":["사하라 사막","남극 대륙","고비 사막"],"ans":"남극 대륙","exp":"사막은 '강수량이 적은 지역'! 남극은 연 강수량 50mm 미만으로 세계 최대 사막이에요."},
   {"q":"올림픽 오륜기의 색깔은 몇 가지?","opts":["4가지","5가지","6가지"],"ans":"5가지","exp":"파랑, 노랑, 검정, 초록, 빨강 5색! 흰 바탕 포함하면 모든 국가 국기 색을 포함합니다."},
   {"q":"피라미드를 만든 사람들은?","opts":["노예","일반 노동자","외계인"],"ans":"일반 노동자","exp":"최근 연구에 따르면 피라미드는 노예가 아닌 급여를 받는 노동자들이 건설했습니다!"},
   {"q":"세계에서 가장 긴 강은?","opts":["아마존 강","나일 강","양쯔 강"],"ans":"나일 강","exp":"나일 강은 약 6,650km로 세계 최장! 아마존은 유량 1위, 나일은 길이 1위입니다."},
   {"q":"한글을 만든 왕은?","opts":["세종대왕","태종","정조"],"ans":"세종대왕","exp":"1443년 세종대왕이 훈민정음을 창제했습니다. 세계적으로도 인정받는 과학적 문자 체계!"}],

  # 4층 — 예술/음악/문학
  [{"q":"셰익스피어 4대 비극이 아닌 것은?","opts":["햄릿","로미오와 줄리엣","맥베스"],"ans":"로미오와 줄리엣","exp":"4대 비극은 햄릿·오셀로·맥베스·리어왕! 로미오와 줄리엣은 포함되지 않습니다."},
   {"q":"최초로 노벨상을 두 번 받은 사람은?","opts":["아인슈타인","마리 퀴리","라이너스 폴링"],"ans":"마리 퀴리","exp":"마리 퀴리는 물리학상(1903)과 화학상(1911)을 수상한 최초의 2회 수상자입니다!"},
   {"q":"'별이 빛나는 밤'을 그린 화가는?","opts":["피카소","고흐","모네"],"ans":"고흐","exp":"빈센트 반 고흐가 1889년 생레미 정신병원에서 그린 작품입니다."},
   {"q":"'해리포터' 시리즈의 작가는?","opts":["J.K. 롤링","J.R.R. 톨킨","C.S. 루이스"],"ans":"J.K. 롤링","exp":"J.K. 롤링이 1997년부터 2007년까지 7편을 출간했습니다. 전 세계 5억 부 이상 판매!"},
   {"q":"피아노의 흰 건반과 검은 건반은 총 몇 개?","opts":["76개","88개","100개"],"ans":"88개","exp":"표준 피아노는 흰 건반 52개 + 검은 건반 36개 = 총 88개입니다!"},
   {"q":"모나리자가 전시된 미술관은?","opts":["대영박물관","루브르 박물관","메트로폴리탄"],"ans":"루브르 박물관","exp":"프랑스 파리의 루브르 박물관에 전시되어 있습니다. 매년 600만 명이 관람해요!"}],

  # 5층 — 최종 보스: 어려운 상식
  [{"q":"실제로 존재하지 않는 화학 원소는?","opts":["아인슈타이늄(Es)","닥터륨(Dc)","오가네손(Og)"],"ans":"닥터륨(Dc)","exp":"아인슈타이늄(99번)과 오가네손(118번)은 실존 원소! 닥터륨은 허구입니다."},
   {"q":"인간의 DNA와 가장 가까운 동물은?","opts":["침팬지","돌고래","문어"],"ans":"침팬지","exp":"침팬지는 인간과 약 98.7%의 DNA를 공유합니다. 가장 가까운 친척이죠!"},
   {"q":"지구에서 가장 깊은 곳은?","opts":["마리아나 해구","에베레스트 반대편","북극 해저"],"ans":"마리아나 해구","exp":"마리아나 해구의 챌린저 해연은 약 11,034m! 에베레스트를 넣어도 2km 남습니다."},
   {"q":"인간의 뼈는 총 몇 개?","opts":["106개","206개","306개"],"ans":"206개","exp":"성인 기준 206개! 아기는 약 270개로 태어나지만 성장하며 뼈가 합쳐집니다."},
   {"q":"1광년은 어떤 단위?","opts":["시간","거리","질량"],"ans":"거리","exp":"1광년은 빛이 1년간 가는 거리, 약 9.46조 km입니다. 시간 단위가 아니에요!"},
   {"q":"옥수수 한 줄의 알갱이 수는 항상?","opts":["짝수","홀수","상관없다"],"ans":"짝수","exp":"옥수수 알갱이는 항상 짝수 줄! 씨앗이 쌍으로 발달하는 식물 구조 때문입니다."}],
]

MATH_POOL = [
  # 1층 — 기초 연산
  [{"q":"7 × 8 은?","opts":["54","56","64"],"ans":"56","exp":"구구단 7단! 7 × 8 = 56 입니다."},
   {"q":"100 - 45 은?","opts":["45","55","65"],"ans":"55","exp":"100 - 45 = 55 입니다."},
   {"q":"12 + 15 + 8 은?","opts":["35","33","32"],"ans":"35","exp":"12 + 8 = 20, 20 + 15 = 35!"},
   {"q":"48 ÷ 6 은?","opts":["7","8","9"],"ans":"8","exp":"구구단 6단! 6 × 8 = 48 입니다."},
   {"q":"3의 4배에서 5를 빼면?","opts":["7","12","15"],"ans":"7","exp":"3 × 4 = 12, 12 - 5 = 7!"},
   {"q":"(5 + 3) × 2 는?","opts":["11","16","13"],"ans":"16","exp":"괄호 먼저! 8 × 2 = 16 입니다."}],

  # 2층 — 분수/소수/비율
  [{"q":"1/2 + 1/4 는?","opts":["2/6","3/4","1/8"],"ans":"3/4","exp":"1/2은 2/4입니다. 2/4 + 1/4 = 3/4!"},
   {"q":"1.5 + 2.3 은?","opts":["3.8","4.8","3.5"],"ans":"3.8","exp":"소수점 자리를 맞춰 더하면 3.8 입니다."},
   {"q":"1시간의 1/3은 몇 분?","opts":["15분","20분","30분"],"ans":"20분","exp":"1시간은 60분. 60 ÷ 3 = 20분!"},
   {"q":"백분율 50%를 분수로 나타내면?","opts":["1/2","1/4","1/5"],"ans":"1/2","exp":"50%는 50/100, 약분하면 1/2 입니다!"},
   {"q":"0.25를 백분율(%)로 나타내면?","opts":["2.5%","25%","250%"],"ans":"25%","exp":"소수에 100을 곱하면 백분율! 0.25 × 100 = 25%"},
   {"q":"1에서 1/3을 빼면?","opts":["1/3","2/3","0"],"ans":"2/3","exp":"1은 3/3이므로, 3/3 - 1/3 = 2/3!"}],

  # 3층 — 도형 및 측정
  [{"q":"삼각형의 세 내각의 합은?","opts":["180도","360도","90도"],"ans":"180도","exp":"모든 삼각형의 내각의 합은 항상 180도입니다."},
   {"q":"하루는 총 몇 분일까?","opts":["720분","1440분","3600분"],"ans":"1440분","exp":"24시간 × 60분 = 1440분입니다!"},
   {"q":"정사각형의 한 변의 길이가 5cm일 때, 둘레는?","opts":["15cm","20cm","25cm"],"ans":"20cm","exp":"정사각형은 네 변이 같습니다. 5 × 4 = 20cm!"},
   {"q":"1킬로미터(km)는 몇 미터(m)?","opts":["100m","1000m","10000m"],"ans":"1000m","exp":"kilo(킬로)는 1000을 의미합니다. 1km = 1000m!"},
   {"q":"직각(Right angle)은 몇 도입니까?","opts":["45도","90도","180도"],"ans":"90도","exp":"수직으로 만나는 각도인 직각은 90도입니다."},
   {"q":"원의 중심을 지나는 선분의 이름은?","opts":["반지름","지름","원주"],"ans":"지름","exp":"원에 있는 선분 중 가장 긴 선분이 바로 '지름'입니다!"}],

  # 4층 — 패턴과 논리
  [{"q":"2, 4, 8, 16 다음 숫자는?","opts":["24","32","64"],"ans":"32","exp":"앞의 숫자에 2를 곱하는 패턴! 16 × 2 = 32."},
   {"q":"1, 4, 9, 16 다음 숫자는?","opts":["25","24","20"],"ans":"25","exp":"제곱수 패턴! 1²=1, 2²=4, 3²=9, 4²=16, 5²=25!"},
   {"q":"모든 홀수에 2를 곱하면 어떤 수가 될까?","opts":["홀수","짝수","알 수 없음"],"ans":"짝수","exp":"어떤 정수든 2를 곱하면 무조건 짝수가 됩니다!"},
   {"q":"1부터 10까지 모두 더하면?","opts":["50","55","60"],"ans":"55","exp":"가우스의 덧셈법: (1+10)×5 = 55 입니다."},
   {"q":"x + 5 = 12 일 때, x의 값은?","opts":["6","7","8"],"ans":"7","exp":"양변에서 5를 빼면 x = 12 - 5 = 7 입니다."},
   {"q":"고양이 3마리와 거미 2마리의 다리는 총 몇 개?","opts":["20개","24개","28개"],"ans":"28개","exp":"고양이(4)×3=12, 거미(8)×2=16.  12+16 = 28개!"}],

  # 5층 — 마왕의 까다로운 수학
  [{"q":"소수(Prime number) 중 유일한 짝수는?","opts":["2","4","짝수 소수는 없다"],"ans":"2","exp":"소수는 1과 자기 자신만으로 나누어지는 수! 2는 유일한 짝수 소수입니다."},
   {"q":"어떤 수를 0으로 나누면 어떻게 될까?","opts":["0","1","계산할 수 없다"],"ans":"계산할 수 없다","exp":"수학에서 0으로 나누는 것(Division by zero)은 정의되지 않습니다!"},
   {"q":"-3 × -5 의 결과는?","opts":["-15","15","-8"],"ans":"15","exp":"음수 곱하기 음수는 양수가 됩니다! (- × - = +)"},
   {"q":"π(파이)의 대략적인 값은?","opts":["3.14","3.41","3.12"],"ans":"3.14","exp":"원주율(파이)은 약 3.14159... 입니다."},
   {"q":"루트 81 (√81) 은 얼마입니까?","opts":["7","8","9"],"ans":"9","exp":"9의 제곱이 81이므로, √81 = 9 입니다."},
   {"q":"100의 10%의 10%는?","opts":["1","10","0.1"],"ans":"1","exp":"100의 10%는 10, 그 10의 10%는 1입니다!"}],
]

DUNGEONS = {
    "🧠 기본 상식 던전": QUIZ_POOL,
    "🧮 수학 기초 던전": MATH_POOL
}


def platformer_html(opts, disabled_opt=None, blind_opt=None, time_limit=15):
    """Generate HTML/JS for the Mario-style answer selection platformer."""
    # Build display labels
    labels_js = []
    for i, opt in enumerate(opts):
        if blind_opt and opt == blind_opt:
            labels_js.append('"???"')
        else:
            labels_js.append(f'"{opt}"')
    disabled_idx = -1
    if disabled_opt:
        for i, opt in enumerate(opts):
            if opt == disabled_opt:
                disabled_idx = i
                break

    html = f"""
<div id="platformer-wrap" style="text-align:center;">
<canvas id="gc" width="640" height="340" tabindex="1"
  style="border:3px solid #ffd700;border-radius:8px;background:#1a1a2e;
  image-rendering:pixelated;display:block;margin:0 auto;outline:none;
  max-width:100%;cursor:pointer;"></canvas>
<p style="color:#888;font-family:'Noto Sans KR',sans-serif;font-size:13px;margin-top:6px;">
  ⬅️➡️ 이동 · ⬆️/Space 점프 · 정답 플랫폼 위에 올라서세요!</p>
</div>
<script>
(function(){{
const C=document.getElementById('gc');
const X=C.getContext('2d');
const W=C.width, H=C.height;
const labels=[{','.join(labels_js)}];
const disIdx={disabled_idx};
const TL={time_limit};
let startT=Date.now();
// Hero
let hx=W/2-12, hy=H-60, hvx=0, hvy=0;
const HW=24, HH=32, GRAV=0.6, JUMP=-11, SPD=4.5;
let onGround=false, facing=1;
// Platforms: left/center/right at varying heights
const plats=[
  {{x:60, y:H-150, w:160, h:22, idx:0}},
  {{x:240, y:H-210, w:160, h:22, idx:1}},
  {{x:420, y:H-150, w:160, h:22, idx:2}},
];
// Ground
const groundY=H-28;
// Selection
let selIdx=-1, selTimer=0;
const SEL_TIME=0.8;
let answered=false;
// Keys
const keys={{}};
C.addEventListener('keydown',e=>{{keys[e.key]=true;e.preventDefault();}});
C.addEventListener('keyup',e=>{{keys[e.key]=false;}});
C.addEventListener('click',()=>C.focus());
C.focus();

function drawBricks(x,y,w,h){{
  // brick texture
  const bw=20,bh=11;
  for(let row=0;row<Math.ceil(h/bh);row++){{
    let ox=(row%2===1)?bw/2:0;
    for(let col=-1;col<Math.ceil(w/bw)+1;col++){{
      let bx=x+col*bw+ox, by=y+row*bh;
      if(bx+bw<=x||bx>=x+w||by+bh<=y||by>=y+h) continue;
      X.save();
      X.beginPath(); X.rect(x,y,w,h); X.clip();
      X.fillStyle='#8B4513'; X.fillRect(bx,by,bw-1,bh-1);
      X.fillStyle='#A0522D'; X.fillRect(bx+1,by+1,bw-3,bh-3);
      X.fillStyle='#6B3410'; X.fillRect(bx,by+bh-1,bw,1);
      X.fillStyle='#6B3410'; X.fillRect(bx+bw-1,by,1,bh);
      X.restore();
    }}
  }}
}}

function drawHero(x, y, f){{
  X.save();
  X.translate(x+HW/2, y);
  if(f<0) X.scale(-1,1);
  // head
  X.fillStyle='#FF3322'; X.fillRect(-10,-2,20,6);  // hat
  X.fillStyle='#CC1100'; X.fillRect(-8,-2,16,3);
  X.fillStyle='#FDBCB4'; X.fillRect(-8,4,16,10);  // face
  X.fillStyle='#111'; X.fillRect(-5,6,3,3);        // eye left
  X.fillStyle='#111'; X.fillRect(3,6,3,3);          // eye right
  // body
  X.fillStyle='#1565C0'; X.fillRect(-9,14,18,12);  // body
  X.fillStyle='#FFD700'; X.fillRect(-3,16,6,3);     // belt
  // legs
  X.fillStyle='#1565C0';
  if(!onGround){{
    X.fillRect(-8,26,6,8); X.fillRect(2,26,6,8);
  }} else {{
    let legOff=Math.sin(Date.now()/100)*2;
    X.fillRect(-8,26,6,8+legOff); X.fillRect(2,26,6,8-legOff);
  }}
  X.fillStyle='#3E2723'; X.fillRect(-9,33,7,3); X.fillRect(2,33,7,3); // shoes
  X.restore();
}}

function drawGround(){{
  X.fillStyle='#2d5a1e';
  X.fillRect(0,groundY,W,H-groundY);
  X.fillStyle='#3a7a28';
  X.fillRect(0,groundY,W,4);
  // grass tufts
  X.fillStyle='#4CAF50';
  for(let i=0;i<W;i+=18){{
    X.fillRect(i,groundY-2,3,4);
    X.fillRect(i+8,groundY-3,2,5);
  }}
}}

function drawTimer(){{
  let elapsed=(Date.now()-startT)/1000;
  let pct=Math.max(0,1-elapsed/TL);
  let barW=W-40;
  X.fillStyle='rgba(0,0,0,0.5)'; X.fillRect(18,8,barW+4,14);
  X.strokeStyle='#555'; X.lineWidth=1; X.strokeRect(18,8,barW+4,14);
  let r=Math.floor(255*(1-pct)), g=Math.floor(255*pct);
  X.fillStyle=`rgb(${{r}},${{g}},80)`;
  X.fillRect(20,10,barW*pct,10);
  X.fillStyle='#fff'; X.font='bold 9px "Press Start 2P",monospace';
  X.textAlign='center';
  X.fillText(Math.ceil(TL-elapsed)+'s',W/2,19);
  return elapsed>=TL;
}}

function drawLabel(p){{
  let col=p.idx===disIdx?'rgba(255,60,60,0.85)':'rgba(255,255,255,0.95)';
  let bgCol=p.idx===disIdx?'rgba(180,30,30,0.7)':'rgba(0,0,0,0.7)';
  X.fillStyle=bgCol;
  let tw=X.measureText(labels[p.idx]).width+16;
  X.fillRect(p.x+p.w/2-tw/2, p.y-24, tw, 20);
  X.strokeStyle=p.idx===disIdx?'#f44336':'#ffd700';
  X.lineWidth=2;
  X.strokeRect(p.x+p.w/2-tw/2, p.y-24, tw, 20);
  X.fillStyle=col; X.font='bold 13px "Noto Sans KR",sans-serif';
  X.textAlign='center'; X.textBaseline='middle';
  X.fillText(p.idx===disIdx?'🚫 '+labels[p.idx]:labels[p.idx], p.x+p.w/2, p.y-14);
  if(selIdx===p.idx){{
    let prog=selTimer/SEL_TIME;
    X.fillStyle='rgba(76,175,80,0.4)';
    X.fillRect(p.x, p.y-2, p.w*prog, 4);
    X.fillStyle='#69f0ae'; X.font='bold 11px "Noto Sans KR"';
    X.fillText(Math.ceil((SEL_TIME-selTimer)*10)/10+'s', p.x+p.w/2, p.y-32);
  }}
}}

function update(dt){{
  // input
  if(keys['ArrowLeft']||keys['a']) {{ hvx=-SPD; facing=-1; }}
  else if(keys['ArrowRight']||keys['d']) {{ hvx=SPD; facing=1; }}
  else hvx*=0.7;
  if(Math.abs(hvx)<0.3) hvx=0;
  if((keys['ArrowUp']||keys[' ']||keys['w']) && onGround){{
    hvy=JUMP; onGround=false;
  }}
  // physics
  hvy+=GRAV;
  hx+=hvx; hy+=hvy;
  // ground
  onGround=false;
  if(hy+HH>=groundY){{hy=groundY-HH; hvy=0; onGround=true;}}
  // walls
  if(hx<0) hx=0; if(hx+HW>W) hx=W-HW;
  // platform collision (only when falling)
  if(hvy>=0){{
    for(let p of plats){{
      if(hx+HW>p.x+4 && hx<p.x+p.w-4 && hy+HH>=p.y && hy+HH<=p.y+p.h+8){{
        hy=p.y-HH; hvy=0; onGround=true;
        break;
      }}
    }}
  }}
  // selection detection
  let curPlat=-1;
  for(let p of plats){{
    if(hx+HW>p.x+4 && hx<p.x+p.w-4 && Math.abs((hy+HH)-p.y)<4 && p.idx!==disIdx){{
      curPlat=p.idx; break;
    }}
  }}
  if(curPlat>=0 && curPlat===selIdx){{
    selTimer+=dt;
    if(selTimer>=SEL_TIME && !answered){{
      answered=true;
      // Send answer to Streamlit
      const url=new URL(window.top.location.href);
      url.searchParams.set('ans_idx',curPlat);
      window.top.location.href=url.toString();
    }}
  }} else {{
    selIdx=curPlat; selTimer=0;
  }}
}}

let lastT=performance.now();
function loop(now){{
  let dt=(now-lastT)/1000; lastT=now;
  if(dt>0.1) dt=0.1;
  if(!answered){{
    update(dt);
    let timeUp=false;
    // draw
    X.clearRect(0,0,W,H);
    // bg gradient
    let grd=X.createLinearGradient(0,0,0,H);
    grd.addColorStop(0,'#0d0d2a'); grd.addColorStop(1,'#1a1a3e');
    X.fillStyle=grd; X.fillRect(0,0,W,H);
    // stars
    X.fillStyle='#fff';
    for(let i=0;i<30;i++){{
      let sx=(i*137+50)%W, sy=(i*97+20)%(groundY-30);
      let sz=1+((i*3)%2);
      X.globalAlpha=0.3+((Math.sin(now/1000+i)*0.3));
      X.fillRect(sx,sy,sz,sz);
    }}
    X.globalAlpha=1;
    drawGround();
    // platforms
    for(let p of plats){{
      drawBricks(p.x,p.y,p.w,p.h);
      drawLabel(p);
    }}
    drawHero(hx,hy,facing);
    timeUp=drawTimer();
    if(timeUp && !answered){{
      answered=true;
      const url=new URL(window.top.location.href);
      url.searchParams.set('ans_idx','-1');
      window.top.location.href=url.toString();
    }}
  }}
  requestAnimationFrame(loop);
}}
requestAnimationFrame(loop);
}})();
</script>
"""
    return html

HITS_NEEDED = 3
MAX_HP = 5
MAX_HINTS = 2
TIME_LIMIT = 15.0

def init(dungeon_name="🧠 기본 상식 던전"):
    pool_data = DUNGEONS.get(dungeon_name, QUIZ_POOL)
    shuffled = [random.sample(pool, len(pool)) for pool in pool_data]
    st.session_state.update({
        "screen":"title",
        "dungeon_name":dungeon_name,
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
        "q_start_time":0, "undead_revived":False,
        "demon_blind_opt":None, "chest_opened":False, "time_over":False
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

.battle{
  border:5px solid #ffd700;padding:24px 20px;
  display:flex;justify-content:space-between;align-items:flex-end;
  min-height:300px;position:relative;
  box-shadow:0 0 50px rgba(255,215,0,.2);
  border-radius:10px;overflow:hidden;
  background-color:#0a0a15;
  background-size:cover;background-position:center;}
.battle::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(transparent,transparent 3px,rgba(0,0,0,.04) 4px);
  border-radius:10px;z-index:0;}

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
.hud-bar{display:flex;justify-content:space-between;align-items:center;margin:8px 0;gap:8px;}
.hud-item{flex:1;text-align:center;padding:10px 6px;border-radius:10px;font-family:'Noto Sans KR',sans-serif;font-size:15px;font-weight:700;}
.hud-coin{background:rgba(255,193,7,.2);border:2px solid #ffc107;color:#ffd740;}
.hud-combo{background:rgba(255,152,0,.2);border:2px solid #ff9800;color:#ffab40;}
.hud-potion{background:rgba(76,175,80,.2);border:2px solid #4CAF50;color:#69f0ae;}
.hud-shield{background:rgba(33,150,243,.2);border:2px solid #42a5f5;color:#64b5f6;}
.reward-box{background:linear-gradient(135deg,rgba(156,39,176,.25),rgba(103,58,183,.25));
  border:2px solid #ab47bc;border-radius:12px;padding:16px;text-align:center;margin:10px 0;animation:rewardPop .5s ease;}
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
.stButton>button{width:100%;border-radius:8px;border:3px solid #5c6bc0;background:#0d0d2a;
  color:#fff;font-family:'Noto Sans KR',sans-serif;font-weight:700;font-size:18px;
  box-shadow:3px 3px 0 #5c6bc0;transition:all .15s;padding:14px 10px;}
.stButton>button:hover{background:#5c6bc0;box-shadow:none;transform:translate(3px,3px);}
@keyframes timerAnim{from{width:100%;background-color:#4CAF50;}50%{background-color:#FF9800;}to{width:0%;background-color:#f44336;}}
.timer-anim{height:8px; border-radius:4px; animation:timerAnim 15s linear forwards;}

@keyframes heroIdle{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes heroAtk{0%{transform:translateX(0);}40%{transform:translateX(40px) scale(1.1);}100%{transform:translateX(0);}}
@keyframes heroHit{0%{transform:translateX(0);filter:none;}30%{transform:translateX(-25px);filter:brightness(2.5) hue-rotate(180deg);}100%{transform:translateX(0);filter:none;}}
@keyframes monIdle{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
@keyframes monHit{0%{transform:translateX(0);filter:none;}30%{transform:translateX(25px);filter:brightness(3) saturate(0);}100%{transform:translateX(0);filter:none;}}
@keyframes monAtk{0%{transform:translateX(0);}40%{transform:translateX(-35px) scale(1.1);}100%{transform:translateX(0);}}
@keyframes monDie{0%{opacity:1;transform:scale(1);}50%{opacity:.4;transform:scale(.6);}100%{opacity:0;transform:scale(.2) translateY(40px);}}
@keyframes pulse{0%,100%{text-shadow:0 0 10px #ffd700;}50%{text-shadow:0 0 30px #ffd700,0 0 60px #ff9800;}}
@keyframes comboPulse{0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}}
@keyframes rewardPop{0%{transform:scale(0);opacity:0;}100%{transform:scale(1);opacity:1;}}
.hero-idle{display:inline-block;animation:heroIdle 2s ease-in-out infinite;}
.hero-atk{display:inline-block;animation:heroAtk .6s ease forwards;}
.hero-hit{display:inline-block;animation:heroHit .6s ease forwards;}
.mon-idle{display:inline-block;animation:monIdle 2.5s ease-in-out infinite;}
.mon-hit{display:inline-block;animation:monHit .6s ease forwards;}
.mon-atk{display:inline-block;animation:monAtk .6s ease forwards;}
.mon-die{display:inline-block;animation:monDie .8s ease forwards;}
.pulse{animation:pulse 1.5s ease-in-out infinite;}
</style>
""", unsafe_allow_html=True)

screen = st.session_state.screen

# ═══════════════ TITLE ═══════════════
if screen == "title":
    with st.sidebar:
        st.markdown(f'<p class="pix" style="color:#ffd700;font-size:16px;margin-bottom:8px">🗺️ 던전 선택</p>', unsafe_allow_html=True)
        st.markdown("<p style='color:#ccc;font-family:\"Noto Sans KR\",sans-serif;font-size:14px'>도전할 퀴즈 주제를 골라주세요!</p>", unsafe_allow_html=True)
        dungeon_choice = st.radio("던전 종류", list(DUNGEONS.keys()), label_visibility="collapsed")
        st.markdown("<hr style='border-color:#555'>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#b388ff;font-family:\"Noto Sans KR\",sans-serif;font-size:14px;font-weight:bold'>현재 선택:<br>&rsaquo; {dungeon_choice}</p>", unsafe_allow_html=True)

    if OPENING_B64:
        st.markdown(f'<img src="{OPENING_B64}" style="width:100%;border:4px solid #ffd700;border-radius:10px;box-shadow:0 0 40px rgba(255,215,0,.4);margin-bottom:8px">', unsafe_allow_html=True)
        
    lb = load_lb()
    if lb:
        lb_html = "<div style='background:rgba(0,0,0,0.5);border:2px solid #ffd700;border-radius:10px;padding:12px;margin:10px 0;text-align:center;'>\n <p style='color:#ffd700;font-family:\"Press Start 2P\",cursive;font-size:14px;margin-bottom:10px;'>🏆 명예의 전당 TOP 5 🏆</p>\n"
        colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#aaa", "#aaa"]
        for i, entry in enumerate(lb):
            rank_color = colors[i] if i < len(colors) else "#aaa"
            lb_html += f"<p style='color:{rank_color};margin:6px 0;font-family:\"Noto Sans KR\",sans-serif;font-weight:bold;'>{i+1}위: {entry['name']} <span style='font-size:13px;color:#eee'>- {entry['score']}점 (최대 {entry['combo']}콤보)</span></p>\n"
        lb_html += "</div>"
        st.markdown(lb_html, unsafe_allow_html=True)

    st.markdown("""<div style="text-align:center;padding:16px 0 8px">
      <p class="pix pulse" style="color:#ffd700;font-size:22px;margin:0">⚔ 마왕의 성 ⚔</p>
      <p class="pix" style="color:#b39ddb;font-size:13px;margin-top:14px">QUIZ DUNGEON</p>
    </div>""", unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2: name = st.text_input("🦸 용사님의 이름을 입력하세요!", value="", max_chars=10, placeholder="이름을 입력해주세요")
    st.markdown("""<div style="text-align:center;padding:4px 0 8px">
      <p style="color:#ccc;font-family:'Noto Sans KR',sans-serif;font-size:15px;line-height:1.8">
         퀴즈를 풀어 몬스터를 물리치고 마왕의 성을 정복하라!<br>
         <b style="color:#ff8a80">3번 정답</b>으로 몬스터 격파 · 오답 시 <b style="color:#ff8a80">❤️</b> 감소<br>
         🧪 <b style="color:#69f0ae">힌트</b> · ⚡ <b style="color:#ffab40">콤보</b> · 🛒 <b style="color:#b388ff">상점</b> · 🎁 <b style="color:#f48fb1">아이템</b>
      </p></div>""", unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("🗡️  게임 시작!", use_container_width=True, type="primary"):
            st.session_state.hero_name = name.strip() if name.strip() else "용사"
            init(dungeon_choice)
            st.session_state.hero_name = name.strip() if name.strip() else "용사" # init 덮어쓰기 복구
            st.session_state.screen = "game"; st.rerun()
    st.stop()

# ═══════════════ SHOP ═══════════════
if screen == "shop":
    mi=st.session_state.mon_idx; coins=st.session_state.coins
    floor_names=["1층 슬라임 동굴","2층 고블린 땅굴","3층 오크 요새","4층 언데드 묘지","5층 마왕의 옥좌 👑"]
    st.markdown(f"""<div style="text-align:center;padding:16px 0">
      <p class="pix" style="color:#b388ff;font-size:18px">🛒 마법 상점 🛒</p>
      <p style="color:#ffd740;font-family:'Noto Sans KR',sans-serif;font-size:20px;font-weight:700;margin-top:6px">💰 {coins} 코인</p>
      <div style="display:flex;justify-content:center;gap:16px;margin-top:8px">
        <span style="color:#69f0ae;font-size:14px">보유 포션: {st.session_state.hints_left}개</span>
        <span style="color:#ff8a80;font-size:14px">현재 HP: {st.session_state.player_hp}/{MAX_HP}</span>
      </div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown(f"""<div class="shop-card"><div style="font-size:36px">🧪</div>
          <p style="color:#69f0ae;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700">힌트 포션</p>
          <p style="color:#aaa;font-size:13px">오답 하나 제거</p>
          <p style="color:#ffd740;font-size:15px;font-weight:700">💰 30</p></div>""", unsafe_allow_html=True)
        if st.button("🧪 구매" if coins>=30 else "🚫 부족", key="bh", disabled=coins<30):
            st.session_state.coins-=30; st.session_state.hints_left+=1; st.rerun()
    with c2:
        can2=coins>=50 and st.session_state.player_hp<MAX_HP
        st.markdown(f"""<div class="shop-card"><div style="font-size:36px">❤️</div>
          <p style="color:#ff8a80;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700">HP 회복약</p>
          <p style="color:#aaa;font-size:13px">HP 1칸 회복</p>
          <p style="color:#ffd740;font-size:15px;font-weight:700">💰 50</p></div>""", unsafe_allow_html=True)
        if st.button("❤️ 구매" if can2 else ("💚 가득" if st.session_state.player_hp>=MAX_HP else "🚫 부족"), key="bhp", disabled=not can2):
            st.session_state.coins-=50; st.session_state.player_hp=min(MAX_HP,st.session_state.player_hp+1); st.rerun()
    with c3:
        hs=st.session_state.shield_active; can3=coins>=40 and not hs
        st.markdown(f"""<div class="shop-card"><div style="font-size:36px">🛡️</div>
          <p style="color:#64b5f6;font-family:'Noto Sans KR',sans-serif;font-size:16px;font-weight:700">보호막</p>
          <p style="color:#aaa;font-size:13px">오답 1회 무효</p>
          <p style="color:#ffd740;font-size:15px;font-weight:700">💰 40</p></div>""", unsafe_allow_html=True)
        if st.button("🛡️ 구매" if can3 else ("✅ 있음" if hs else "🚫 부족"), key="bs", disabled=not can3):
            st.session_state.coins-=40; st.session_state.shield_active=True; st.session_state.shield_used=False; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        nf=floor_names[mi] if mi<len(floor_names) else "최종"
        if st.button(f"⚔️ {nf}으로!", type="primary", use_container_width=True):
            if mi < len(MONSTERS) and random.random() < 0.3:
                st.session_state.screen="event"
            else:
                st.session_state.screen="game"
            st.rerun()
    st.stop()

# ═══════════════ EVENT (RANDOM BOX) ═══════════════
if screen == "event":
    st.markdown("""<div style="text-align:center;padding:20px;">
        <p class="pix pulse" style="color:#ffd700;font-size:24px;">🎁 비밀의 보물상자 발견!</p>
        <p style="color:#ccc;font-size:16px;margin-top:10px;">길을 걷던 중 반짝이는 상자를 발견했습니다.</p>
    </div>""", unsafe_allow_html=True)
    
    if st.session_state.chest_opened:
        r = random.Random(st.session_state.total_correct + st.session_state.coins)
        event_num = r.randint(1, 100)
        msg = ""
        bg_color = "rgba(76,175,80,0.2)"
        border = "#4CAF50"
        
        if event_num <= 40:
            msg = "💰 엄청난 보화가 들었다! (코인 +50)"
            st.session_state.coins += 50
        elif event_num <= 70:
            msg = "❤️ 신선한 과일이 들어있다! (HP +1)"
            st.session_state.player_hp = min(MAX_HP, st.session_state.player_hp + 1)
        elif event_num <= 85:
            msg = "🧪 오래된 힌트 포션을 얻었다! (포션 +1)"
            st.session_state.hints_left += 1
        else:
            msg = "💥 앗! 함정이다! 독가스가 뿜어져 나왔다! (HP -1)"
            bg_color = "rgba(244,67,54,0.2)"
            border = "#f44336"
            st.session_state.player_hp = max(0, st.session_state.player_hp - 1)
            
        st.markdown(f"""<div style="text-align:center;background:{bg_color};border:2px solid {border};border-radius:10px;padding:20px;margin:20px 0;">
            <p style="color:#fff;font-size:20px;font-weight:bold;">{msg}</p></div>""", unsafe_allow_html=True)
            
        col1,col2,col3=st.columns([1,2,1])
        with col2:
            if st.session_state.player_hp <= 0:
                if st.button("☠️ 게임 오버", type="primary", use_container_width=True):
                    st.session_state.screen = "game"; st.rerun()
            else:
                if st.button("▶ 다음 층으로", type="primary", use_container_width=True):
                    st.session_state.chest_opened = False
                    st.session_state.screen = "game"; st.rerun()
    else:
        st.markdown('<div style="text-align:center;font-size:80px;margin:10px 0;">📦</div>', unsafe_allow_html=True)
        col1,col2,col3=st.columns([1,2,1])
        with col2:
            if st.button("✨ 상자 열기", type="primary", use_container_width=True):
                st.session_state.chest_opened = True; st.rerun()
            if st.button("무시하고 지나간다", use_container_width=True):
                st.session_state.screen = "game"; st.rerun()
    st.stop()

# ═══════════════ GAME OVER ═══════════════
mi=st.session_state.mon_idx; php=st.session_state.player_hp; hero_name=st.session_state.hero_name
if php<=0:
    score = st.session_state.total_correct * 100 + st.session_state.coins * 2 + st.session_state.max_combo * 50
    if "lb_saved_go" not in st.session_state:
        lb = load_lb()
        lb.append({"name": hero_name, "score": score, "combo": st.session_state.max_combo})
        save_lb(lb)
        st.session_state.lb_saved_go = True
        
    if GAMEOVER_B64:
        st.markdown(f'<img src="{GAMEOVER_B64}" style="width:100%;border:4px solid #f44336;border-radius:10px;box-shadow:0 0 40px rgba(244,67,54,.4);margin-bottom:10px">', unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;padding:20px">
      <p class="pix" style="color:#f44336;font-size:26px;text-shadow:0 0 20px #f44336">💀 GAME OVER 💀</p>
      <p style="color:#ccc;font-family:'Noto Sans KR',sans-serif;font-size:18px;margin-top:8px">{hero_name}(이)가 <b>{mi+1}층</b>의 퀴즈에서 쓰러졌습니다...</p>
      <p style="color:#ffd700;font-family:'Noto Sans KR',sans-serif;font-size:16px;margin-top:12px;font-weight:bold;">최종 스코어: {score}점</p>
      <p style="color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:14px;margin-top:4px">
        📊 정답 {st.session_state.total_correct} · 오답 {st.session_state.total_wrong} · 💰 {st.session_state.coins} · ⚡최대콤보 {st.session_state.max_combo}</p>
    </div>""", unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("🔄 게임 다시 시작!", use_container_width=True): 
            dung = st.session_state.get("dungeon_name", "🧠 기본 상식 던전")
            init(dung); st.rerun()
    st.stop()

# ═══════════════ CLEAR ═══════════════
if mi>=len(MONSTERS):
    st.balloons()
    if ENDING_B64:
        st.markdown(f'<img src="{ENDING_B64}" style="width:100%;border:4px solid #ffd700;border-radius:10px;box-shadow:0 0 40px rgba(255,215,0,.4);margin-bottom:8px">', unsafe_allow_html=True)
    rank="S" if php==MAX_HP else ("A" if php>=4 else ("B" if php>=3 else ("C" if php>=2 else "D")))
    rc={"S":"#FFD700","A":"#C0C0C0","B":"#CD7F32","C":"#78909C","D":"#f44336"}[rank]
    rt={"S":"전설의 용사","A":"위대한 모험가","B":"숙련된 전사","C":"초보 영웅","D":"수습 용사"}[rank]
    tc,tw=st.session_state.total_correct,st.session_state.total_wrong
    coins=st.session_state.coins*(2 if "coin_double" in st.session_state.collected_effects else 1)
    
    score = tc * 100 + coins * 2 + st.session_state.max_combo * 50 + php * 200
    if "lb_saved_clear" not in st.session_state:
        lb = load_lb()
        lb.append({"name": hero_name, "score": score, "combo": st.session_state.max_combo})
        save_lb(lb)
        st.session_state.lb_saved_clear = True

    st.markdown(f"""<div style="text-align:center;padding:16px 0">
      <p class="pix pulse" style="color:#ffd700;font-size:22px">👑 DUNGEON CLEAR! 👑</p>
      <p style="color:#e0e0e0;font-family:'Noto Sans KR',sans-serif;font-size:20px;margin-top:12px"><b>{hero_name}</b>(이)가 마왕을 쓰러뜨렸습니다!</p>
      <p class="pix" style="color:{rc};font-size:32px;margin:12px 0">RANK: {rank}</p>
      <p style="color:#b39ddb;font-family:'Noto Sans KR',sans-serif;font-size:16px">🏅 {rt} · HP {"❤️"*php}{"🖤"*(MAX_HP-php)}</p>
      <p style="color:#FF9800;font-family:'Noto Sans KR',sans-serif;font-size:20px;margin-top:8px;font-weight:bold;">최종 스코어: {score}점</p>
      <p style="color:#ffd740;font-family:'Noto Sans KR',sans-serif;font-size:16px;margin-top:4px">
        ✅{tc} · ❌{tw} · 💰{coins} · ⚡{st.session_state.max_combo}콤보</p>
    </div>""", unsafe_allow_html=True)
    if st.session_state.collected_items:
        items_html=" ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
        st.markdown(f'<div class="items-bar" style="justify-content:center">🎒 {items_html}</div>', unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("🔄 다시 도전",use_container_width=True,type="primary"): 
            dung = st.session_state.get("dungeon_name", "🧠 기본 상식 던전")
            init(dung); st.rerun()
    st.stop()

# ═══════════════ GAME ═══════════════
hits=st.session_state.mon_hits; qi=st.session_state.qpool_idx; dying=st.session_state.mon_dying
lc=st.session_state.last_correct; quiz=st.session_state.shuffled_quiz; combo=st.session_state.combo; coins=st.session_state.coins

mon_name,mon_spr,mon_ico=MONSTERS[mi]
q_pool=quiz[mi]; q=q_pool[qi%len(q_pool)]

# ─── Platformer answer handler (query params) ───
_ans_param = st.query_params.get("ans_idx", None)
if _ans_param is not None and not st.session_state.answered:
    st.query_params.clear()
    ans_idx = int(_ans_param)
    opts = q["opts"]
    disabled_opt_qp = None
    if st.session_state.hint_used_this_q:
        wrong = [o for o in opts if o != q["ans"]]
        if wrong:
            random.seed(f"{mi}_{qi}_h")
            disabled_opt_qp = random.choice(wrong)
    if ans_idx < 0:  # time over
        correct = False
        st.session_state.time_over = True
    elif disabled_opt_qp and ans_idx < len(opts) and opts[ans_idx] == disabled_opt_qp:
        correct = False  # picked the disabled (hint) option somehow
    elif ans_idx < len(opts):
        correct = (opts[ans_idx] == q["ans"])
    else:
        correct = False
    st.session_state.answered = True
    if correct:
        st.session_state.demon_blind_opt = None
        nc = combo + 1; st.session_state.combo = nc
        st.session_state.max_combo = max(st.session_state.max_combo, nc)
        cg = 10 + nc * 5 + (5 if "coin_bonus" in st.session_state.collected_effects else 0)
        st.session_state.coins += cg; st.session_state.total_correct += 1
        st.session_state.last_correct = True
        nh = hits + 1
        if mi == 3 and not st.session_state.undead_revived and nh >= (4 if mi == 2 else HITS_NEEDED):
            st.session_state.undead_revived = True
            st.session_state.mon_hits = (4 if mi == 2 else HITS_NEEDED) - 1
        else:
            cur_h = 4 if mi == 2 else HITS_NEEDED
            if "power_hit" in st.session_state.collected_effects and mi > 2:
                cur_h = max(1, cur_h - 1)
            st.session_state.mon_hits = nh
            if nh >= cur_h:
                st.session_state.mon_dying = True
                rn, _, ek = REWARDS[mi]
                st.session_state.collected_items.append(rn)
                st.session_state.collected_effects.append(ek)
                st.session_state.coins += 50
                if ek == "hint_bonus": st.session_state.hints_left += 1
                if ek == "shield":
                    st.session_state.shield_active = True
                    st.session_state.shield_used = False
    else:
        st.session_state.demon_blind_opt = None
        st.session_state.combo = 0; st.session_state.total_wrong += 1
        if mi == 1:
            st.session_state.coins = max(0, st.session_state.coins - 10)
        if st.session_state.shield_active and not st.session_state.shield_used:
            st.session_state.shield_active = False; st.session_state.shield_used = True
            st.session_state.last_correct = "shielded"
        else:
            st.session_state.player_hp = max(0, php - 1); st.session_state.last_correct = False
        st.session_state.encourage_msg = random.choice(ENCOURAGE)
    st.rerun()

# Refresh after query param handling
hits=st.session_state.mon_hits; dying=st.session_state.mon_dying
lc=st.session_state.last_correct; combo=st.session_state.combo; coins=st.session_state.coins

# Gimmick: Orc has more HP
cur_hits_needed = 4 if mi == 2 else HITS_NEEDED
# Power Hit reduces HP
if "power_hit" in st.session_state.collected_effects and mi > 2:
    cur_hits_needed = max(1, cur_hits_needed - 1)

# Gimmick: Demon Blinds one option
if mi == 4 and st.session_state.demon_blind_opt is None:
    st.session_state.demon_blind_opt = random.choice(q["opts"])

import time
# Timer Logic
if st.session_state.q_start_time == 0:
    st.session_state.q_start_time = time.time()
elapsed = time.time() - st.session_state.q_start_time
is_time_over = elapsed > TIME_LIMIT

# 스프라이트 결정
hero_spr=HERO_ATK if lc is True else (HERO_HIT if lc is False else HERO_IDLE)
hero_anim="hero-atk" if lc is True else ("hero-hit" if lc is False else "hero-idle")
mon_anim="mon-die" if dying else ("mon-hit" if lc is True else ("mon-atk" if lc is False else "mon-idle"))

hero_svg_str=svg(hero_spr,12)
mon_svg_str=svg(mon_spr,13)

mon_hp_pct=int(hits/cur_hits_needed*100)
mon_bar_col="#f44336" if mon_hp_pct>=66 else ("#FF9800" if mon_hp_pct>=33 else "#4CAF50")
floor_names=["1층 슬라임 동굴","2층 고블린 땅굴","3층 오크 요새","4층 언데드 묘지","5층 마왕의 옥좌 👑"]

overall_pct=int((mi*HITS_NEEDED+hits)/(len(MONSTERS)*HITS_NEEDED)*100)
st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{overall_pct}%">{overall_pct}%</div></div>', unsafe_allow_html=True)
st.markdown(f'<p class="pix" style="color:#ffd700;font-size:14px;text-align:center;padding:6px 0;text-shadow:0 0 10px #ffd700">⚔ 마왕의 성 ⚔</p>', unsafe_allow_html=True)
st.markdown(f'<p class="pix" style="color:#b39ddb;font-size:12px;text-align:center;margin-bottom:6px">{floor_names[mi]}</p>', unsafe_allow_html=True)

if not dying and lc is None:
    st.markdown(f'<div style="background:#222;border-radius:4px;width:100%;height:10px;border:1px solid #555;margin-bottom:12px;"><div class="timer-anim" style="animation-delay: -{elapsed}s;"></div></div>', unsafe_allow_html=True)


shield_html='<div class="hud-item hud-shield">🛡️ ON</div>' if st.session_state.shield_active else ""
st.markdown(f"""<div class="hud-bar">
  <div class="hud-item hud-coin">💰 {coins}</div>
  <div class="hud-item hud-combo">⚡ {combo}콤보</div>
  <div class="hud-item hud-potion">🧪 {st.session_state.hints_left}개</div>
  {shield_html}
</div>""", unsafe_allow_html=True)

if st.session_state.collected_effects:
    em={"coin_bonus":"🗡️코인+5","shield":"🛡️무효","power_hit":"💪2타","hint_bonus":"👻포션+1","coin_double":"👑2배"}
    eff_html="".join([f'<span class="effect-tag">{em.get(e,e)}</span>' for e in st.session_state.collected_effects])
    st.markdown(f'<div style="text-align:center;margin:4px 0">{eff_html}</div>', unsafe_allow_html=True)

bg_style=f'background-image:url({BATTLE_BG_B64});' if BATTLE_BG_B64 else ''
floor_tints = [
    "rgba(0,50,0,0.5)", "rgba(50,50,0,0.5)", "rgba(50,0,0,0.5)", "rgba(20,0,50,0.6)", "rgba(80,0,20,0.7)"
]
tint = floor_tints[mi] if mi < len(floor_tints) else "rgba(0,0,0,0.5)"

st.markdown(f"""
<div class="battle" style="{bg_style}">
  <div style="position:absolute;inset:0;background:linear-gradient(0deg,{tint} 0%,rgba(0,0,0,0.1) 40%,rgba(0,0,0,0.3) 100%);pointer-events:none;z-index:0;"></div>
  <div style="text-align:center;z-index:1">
    <div class="{hero_anim}">{hero_svg_str}</div>
    <p class="pix" style="color:#81d4fa;font-size:11px;margin-top:8px">{hero_name}</p>
  </div>
  <div class="pix" style="color:#f44336;font-size:28px;align-self:center;text-shadow:0 0 16px #f44336;z-index:1">VS</div>
  <div style="text-align:center;z-index:1">
    <div class="{mon_anim}">{mon_svg_str}</div>
    <p class="pix" style="color:#ef9a9a;font-size:11px;margin-top:8px">{mon_ico} {mon_name}</p>
  </div>
</div>""", unsafe_allow_html=True)

dmg_bullets="💥"*hits+"⬜"*(cur_hits_needed-hits)
st.markdown(f"""<div class="hud">
  <span class="hudlbl">{hero_name} {"❤️"*php}{"🖤"*(MAX_HP-php)}</span>
  <span class="hudlbl" style="color:#ffd700">{mon_name} {dmg_bullets}</span>
</div>
<div style="height:14px;background:#222;border:2px solid #444;border-radius:4px;margin-bottom:8px;overflow:hidden">
  <div style="height:100%;width:{mon_hp_pct}%;background:{mon_bar_col};transition:width .4s"></div>
</div>""", unsafe_allow_html=True)

if st.session_state.collected_items:
    items_html=" ".join([f'<span class="item-badge">{it}</span>' for it in st.session_state.collected_items])
    st.markdown(f'<div class="items-bar">🎒 {items_html}</div>', unsafe_allow_html=True)

if lc=="shielded":
    st.markdown(f'<div class="res-shield">🛡️ 보호막이 데미지를 막았다! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif dying:
    rn,rd,_=REWARDS[mi]
    st.markdown(f'<div class="res-ok">🏆 {mon_name} 격파!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="reward-box"><span style="font-size:28px">{rn.split()[0]}</span><br><span style="color:#e0e0e0;font-family:\'Noto Sans KR\',sans-serif;font-size:14px">{rd}</span></div>', unsafe_allow_html=True)
elif lc is True:
    ce="+5" if "coin_bonus" in st.session_state.collected_effects else ""
    st.markdown(f'<div class="res-ok">✅ 히트! ({hits}/{cur_hits_needed}) +{10+combo*5}코인 {ce}</div>', unsafe_allow_html=True)
    if combo>=2: st.markdown(f'<div class="combo-box"><span style="color:#ffa500;font-family:\'Press Start 2P\',cursive;font-size:12px">{COMBO_MSG[min(combo,len(COMBO_MSG)-1)]}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)
elif lc is False:
    if st.session_state.get("time_over", False):
        st.markdown(f'<div class="res-ng">⏱️ 타임 오버! 늦었습니다. (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="res-ng">💥 오답! (정답: {q["ans"]})</div>', unsafe_allow_html=True)
    if mi == 1:
        st.markdown('<div class="encourage" style="color:#ff8a80;border-color:#ff5252">고블린이 코인을 빼앗아갔습니다! (-10코인)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="encourage">{st.session_state.encourage_msg}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="exp">💡 {q["exp"]}</div>', unsafe_allow_html=True)

if not dying:
    st.markdown(f'<div class="qcard"><span style="color:#ffd740;font-size:14px">Q{qi+1}.</span> <br>{q["q"]}</div>', unsafe_allow_html=True)

if not st.session_state.answered:
    if not st.session_state.hint_used_this_q and st.session_state.hints_left>0:
        hc1,hc2,hc3=st.columns([1,2,1])
        with hc2:
            if st.button(f"🧪 힌트 사용 (남은 {st.session_state.hints_left}개)", key="hint_btn"):
                st.session_state.hints_left-=1; st.session_state.hint_used_this_q=True; st.rerun()
    opts=q["opts"]; disabled_opt=None
    if st.session_state.hint_used_this_q:
        wrong=[o for o in opts if o!=q["ans"]]
        if wrong: random.seed(f"{mi}_{qi}_h"); disabled_opt=random.choice(wrong)
    blind_opt = st.session_state.demon_blind_opt if mi == 4 else None
    plat_html = platformer_html(opts, disabled_opt=disabled_opt, blind_opt=blind_opt, time_limit=int(TIME_LIMIT))
    escaped = _html.escape(plat_html)
    st.markdown(f'<iframe srcdoc="{escaped}" sandbox="allow-scripts allow-top-navigation allow-top-navigation-by-user-activation" style="width:100%;height:400px;border:none;" scrolling="no"></iframe>', unsafe_allow_html=True)
else:
    # 오답 시 정답을 강조해서 보여주기
    if not dying and lc is False:
         st.markdown(f'<div style="text-align:center;margin:8px 0"><span style="background:rgba(76,175,80,0.2);color:#69f0ae;padding:8px 16px;border-radius:20px;border:1px solid #4CAF50;font-weight:bold;font-family:\'Noto Sans KR\',sans-serif">🟢 올바른 정답: {q["ans"]}</span></div>', unsafe_allow_html=True)

    if dying:
        nxt=mi+1
        if nxt>=len(MONSTERS):
            if st.button("🏆 클리어!",type="primary",use_container_width=True):
                st.session_state.update({"mon_idx":nxt,"mon_hits":0,"qpool_idx":0,"answered":False,"last_correct":None,"mon_dying":False,"hint_used_this_q":False,"shield_used":False}); st.rerun()
        else:
            if st.button("🛒 상점 → 다음 층!",type="primary",use_container_width=True):
                st.session_state.update({"mon_idx":nxt,"mon_hits":0,"qpool_idx":0,"answered":False,"last_correct":None,"mon_dying":False,"hint_used_this_q":False,"shield_used":False,"screen":"shop"}); st.rerun()
    else:
        if st.button("▶ 다음 문제",type="primary",use_container_width=True):
            st.session_state.update({"qpool_idx":qi+1,"answered":False,"last_correct":None,"hint_used_this_q":False,"q_start_time":0}); st.rerun()
