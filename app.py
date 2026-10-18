import streamlit as st
import random
import hashlib
import datetime

# 1. 頁面基本配置（針對 iPhone 視窗與 LINE 瀏覽器最佳化）
st.set_page_config(
    page_title="👑 真真公主的解壓美食盲盒",
    page_icon="👑",
    layout="centered"
)

# 2. iPhone WebKit 深度優化與真楨美學專屬配色加固 CSS
st.markdown("""
<style>
:root {
    color-scheme: light !important;
    -webkit-color-scheme: light !important;
}

.block-container {
    padding-top: max(0.6rem, env(safe-area-inset-top)) !important;
    padding-bottom: max(3.5rem, env(safe-area-inset-bottom)) !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
    -webkit-text-size-adjust: 100% !important;
}

#MainMenu, footer, header, [data-testid="manage-app-button"], div[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}

html, body, [class*="css"], .stApp {
    color: #4A3E3D !important;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Helvetica Neue", sans-serif;
    -webkit-font-smoothing: antialiased;
    -webkit-tap-highlight-color: transparent !important;
    touch-action: manipulation !important;
}

.stApp {
    background: linear-gradient(180deg, #FDF9F8 0%, #F5ECE9 100%) !important;
}

/* 頂部 iPhone / LINE 貼心指引框 */
.safari-tip-box {
    background: #FFF9FA;
    border: 1px dashed #E08A9D;
    border-radius: 12px;
    padding: 8px 12px;
    text-align: center;
    font-size: 0.82rem;
    color: #8C6D77;
    margin-bottom: 12px;
}
.safari-tip-highlight {
    color: #C2255C;
    font-weight: 700;
}

/* 頂部公主守護橫幅 */
.care-banner {
    background: linear-gradient(135deg, #FFF0F3 0%, #FFE3E8 100%) !important;
    border: 1.5px solid #F3DFE3 !important;
    border-radius: 18px !important;
    padding: 12px 16px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 4px 14px rgba(224, 138, 157, 0.15) !important;
    text-align: center;
}
.care-banner-tag {
    font-size: 0.85rem;
    font-weight: 800;
    color: #C2255C;
    margin-bottom: 4px;
}
.care-banner-msg {
    font-size: 0.92rem;
    color: #4A3E3D;
    line-height: 1.45;
}

/* 收合選單標題單行優化 */
.streamlit-expanderHeader, div[data-testid="stExpander"] summary span, div[data-testid="stExpander"] details summary {
    color: #C2255C !important;
    font-weight: 700 !important;
    font-size: 0.94rem !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1.5px solid #F3DFE3 !important;
    margin-bottom: 14px !important;
    box-shadow: 0 4px 14px rgba(224, 138, 157, 0.1) !important;
}

div[role="radiogroup"] label p, div[role="radiogroup"] label span {
    color: #4A3E3D !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}
.stRadio > label {
    color: #C2255C !important;
    font-weight: 700 !important;
}

div[role="radiogroup"] > label div:first-child {
    background-color: #FFFFFF !important;
    border: 2px solid #E08A9D !important;
}
div[role="radiogroup"] > label[data-checked="true"] div:first-child,
div[role="radiogroup"] input:checked + div {
    border-color: #C2255C !important;
    background-color: #C2255C !important;
}
div[role="radiogroup"] svg {
    fill: #C2255C !important;
}

.card-box {
    background: #FFFFFF !important;
    padding: 22px 18px !important;
    border-radius: 22px !important;
    box-shadow: 0 8px 24px rgba(224, 138, 157, 0.18) !important;
    border: 1.5px solid #F3DFE3 !important;
    margin-bottom: 16px !important;
    text-align: center;
    -webkit-transform: translateZ(0);
}

.card-tag {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 18px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 10px;
}
.tag-food { background-color: #FFE8D6; color: #D9480F; border: 1px solid #FFD8A8; }
.tag-dog { background-color: #FFF3BF; color: #D9480F; }
.tag-cat { background-color: #EBFBEE; color: #2B8A3E; }
.tag-kid { background-color: #FFE3E8; color: #C2255C; border: 1px solid #FFC9C9; }
.tag-meme { background-color: #E7F5FF; color: #1971C2; }
.tag-infinite { background-color: #F8F0FC; color: #845EF7; border: 1px solid #E599F7; }
.tag-ssr { background-color: #FFF0F3; color: #C2255C; border: 1.5px dashed #E08A9D; }
.tag-care { background-color: #FFE3EC; color: #C2255C; border: 1.5px solid #FFCCD5; }

.card-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #C2255C;
    margin-bottom: 10px;
}
.card-content {
    font-size: 1rem;
    color: #4A3E3D !important;
    line-height: 1.75;
    margin: 10px 0;
    white-space: pre-wrap;
    text-align: left;
    background: #FCF8F7;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #F3DFE3;
}

.stButton>button {
    background: linear-gradient(135deg, #E08A9D 0%, #D47A8F 100%) !important;
    color: #FFFFFF !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    border-radius: 24px !important;
    border: none !important;
    padding: 12px 18px !important;
    box-shadow: 0 6px 18px rgba(224, 138, 157, 0.35) !important;
    width: 100% !important;
    touch-action: manipulation !important;
    transition: transform 0.08s ease;
    white-space: nowrap !important;
}
.stButton>button:active {
    transform: scale(0.96) !important;
}

/* 脆按鈕：強制單行、邊距優化、緊湊字距 */
.threads-btn {
    display: block;
    background: #2D2426;
    color: #FFFFFF !important;
    text-align: center;
    padding: 11px 8px;
    border-radius: 18px;
    font-weight: 700;
    text-decoration: none !important;
    margin-top: 8px;
    font-size: 0.88rem;
    touch-action: manipulation;
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: ellipsis;
    letter-spacing: -0.2px;
}

/* 召喚按鈕：強制單行顯示 */
.line-call-btn {
    display: block;
    width: 100%;
    background: linear-gradient(135deg, #E08A9D 0%, #C2255C 100%);
    color: #FFFFFF !important;
    text-align: center;
    padding: 13px 10px;
    border-radius: 26px;
    font-weight: 800;
    text-decoration: none !important;
    font-size: 0.92rem;
    box-shadow: 0 6px 20px rgba(194, 37, 92, 0.3);
    touch-action: manipulation;
    transition: transform 0.08s ease;
    white-space: nowrap !important;
    letter-spacing: -0.2px;
}
.line-call-btn:active {
    transform: scale(0.97);
}
</style>
""", unsafe_allow_html=True)

# 3. 專屬安全淨化器
def sanitize_text(text: str) -> str:
    replacements = {
        "LU寶貝": "真真公主",
        "LU 寶貝": "真真公主",
        "寶貝": "真真公主",
        "男朋友": "專屬好友",
        "男友": "專屬好友",
        "老公": "專屬好友",
        "情人": "知己好友",
        "情侶": "懂吃好友"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()

# 4. 公主專屬週期守護計算（底層安靜運行）
def get_care_status():
    """
    基準日：2026-10-13，以 28 天為週期默默計算
    11/6 落在週期第 25 天（正好對應生日前夕與順毛美食回血期）
    """
    base_date = datetime.date(2026, 10, 13)
    today = datetime.date.today()
    days_diff = (today - base_date).days
    cycle_day = (days_diff % 28) + 1  # 1 ~ 28 天

    if 1 <= cycle_day <= 5:
        return {
            "is_special": True,
            "banner_tag": "🌸 今日公主專屬・滿血回溫特權",
            "banner_msg": "今天全世界的事情都得靠邊站！溫熱好茶與暖胃甜品無上限供應，公主專心放空回血就好～🍵",
            "card_tag": "🌸 溫柔補血卡",
            "title": "今日指令：暖胃、放空、拒絕勞累",
            "content": "『肚子悶悶、電力剩 10%？』\n\n今天雜事自動消散！熱黑糖桂圓茶隨時在線，生冷飲料全面退散。\n公主今天只負責在沙發當融化布丁，好好休息，所有的辛苦好友罩妳！🌸\n\n#專屬補血模式 #今天只想徹底躺平 #暖暖的心情最好"
        }
    elif 13 <= cycle_day <= 16:
        return {
            "is_special": True,
            "banner_tag": "✨ 仙氣滿格・高光閃耀模式",
            "banner_msg": "今天真真公主自帶柔光濾鏡！水分補足、氣色滿分，走到哪裡都在發光～💖",
            "card_tag": "✨ 仙女高光卡",
            "title": "自帶頂級光芒的天使狀態",
            "content": "『今天鏡子裡的真真公主，美到完全不需要任何濾鏡！』\n\n靈感爆棚、氣場全開，但忙店務時記得多喝溫水補水。\n今天想吃哪家私房好料？隨時翻牌子，好朋友立刻幫妳安排到位！✨\n\n#真真公主自帶光芒 #今天狀態滿格 #多喝溫水保持仙氣"
        }
    elif 24 <= cycle_day <= 28:
        return {
            "is_special": True,
            "banner_tag": "👑 頂級順毛・零負擔特權",
            "banner_msg": "最近容易疲倦或火氣大？誰敢惹妳通通面壁，大餐與好心情專屬供應！🥩",
            "card_tag": "🛡️ 專屬避風港卡",
            "title": "誰敢惹公主？好友全額出氣",
            "content": "『最近偶爾覺得煩悶、沒耐心？千萬別生悶氣！』\n\n這是仙女系統在提醒妳需要高級蛋白質與大餐回血！\n阿力海生蠔龍蝦一樓好位已準備就緒，真真公主霸氣做東，好友負責把肚子空下來當快樂廢人！🔥\n\n#特級順毛模式 #吃肉補元氣 #全世界妳最重要"
        }
    else:
        return {
            "is_special": False,
            "banner_tag": "",
            "banner_msg": "",
            "card_tag": "",
            "title": "",
            "content": ""
        }

# 5. 超低機率 SSR 稀有特權卡
SSR_CARDS = [
    {
        "type": "ssr",
        "tag": "👑 奇蹟降臨・SSR 歐皇特權卡",
        "title": "🍲 台南私房好料隨傳隨到探店券",
        "content": "【千萬分之一機率歐皇認證】\n恭喜真真公主觸發稀有特權！\n只要公主想吃，不管是台南排隊名店、隱藏甜點、深夜罪惡牛肉湯還是麻辣鍋，好友無條件出動陪吃探店，排隊與熱量全由好友吸收！🚗💨",
        "img": ""
    },
    {
        "type": "ssr",
        "tag": "👑 奇蹟降臨・SSR 歐皇特權卡",
        "title": "🍰 專屬下午茶與手搖補血券",
        "content": "【千萬分之一機率歐皇認證】\n今天店裡忙翻、帶小孩血壓飆高想喝甜的？出示此截圖，好友立刻奉上仙楂烏龍與特調好茶甜點，真真公主只要張嘴負責吃，好好回血放空！🧁",
        "img": ""
    },
    {
        "type": "ssr",
        "tag": "👑 奇蹟降臨・SSR 歐皇特權卡",
        "title": "🛡️ 專屬出氣筒與無限順毛券",
        "content": "【千萬分之一機率歐皇認證】\n今日不論心情多煩、遇到什麼鳥事想吐槽，好友無條件站妳這邊同仇敵愾，不講大道理、全心全意把真真公主哄開心為止！🌸",
        "img": ""
    }
]

# 6. 上限極限擴充：萬向五維語料庫矩陣
CORPUS = {
    "food": {
        "titles": [
            "台南吃貨的深夜救贖", "舌尖上的回血儀式", "今天不談減肥只談快樂", 
            "永康隱藏美食私房話", "甜點是仙女的充電寶", "熱湯澆下去的溫柔瞬間",
            "炭火滋滋作響的解壓法", "海鮮自由的頂級快樂", "巷弄老宅的焦糖香氣", "懂吃靈魂的專屬地圖"
        ],
        "openings": [
            "剛結束一天緊湊的預約客人，走出店門口肚子咕嚕嚕抗議",
            "深夜滑著 IG，滿螢幕都在推台南在地現切溫體牛肉湯",
            "突然超級想吃熱騰騰又香氣逼人的排隊拉麵濃郁湯頭",
            "下午店務告一段落，靈魂極度渴望一塊現烤焦糖布丁或法式千層",
            "晚餐時間到了，腦袋瞬間進入選擇障礙的放空模式",
            "路過炭佐麻里聞到迷人的炭火香，理智線瞬間斷裂",
            "明明剛吃飽沒多久，嘴巴卻莫名其妙寂寞了起來",
            "經過台南永康老街，那股現炒鱔魚意麵的鑊氣直接把魂勾走",
            "天氣微涼的夜晚，胃裡只有一個念頭：熱騰騰的麻辣鴨血豆腐",
            "工作忙到忘記時間，回過神來只想用大餐狠狠犒賞自己"
        ],
        "twists": [
            "這時候喝一口鮮甜滾燙的牛肉高湯，所有疲憊真的瞬間被徹底融化！",
            "炭佐麻里的烤肉滋滋作響，大口嚼肉的爽快感是任何保養品都換不來的！",
            "阿力海滿滿的生蠔、龍蝦跟哈根達斯，真真公主親自訂的一樓好位，絕對吃得最舒適！",
            "來一杯酸甜生津的仙楂烏龍，微糖微冰，整個人都神清氣爽起來了！",
            "巷弄老宅剛出爐的肉桂捲，那股肉桂黑糖香氣直接把好心情補到滿格！",
            "咬下金黃酥脆的炸雞外皮，肉汁爆開的瞬間，所有煩惱通通立正站好！",
            "焦糖布丁滑進嘴裡的綿密甜味，就是對抗世界所有瑣事的最強盾牌！",
            "現切溫體牛肉沾上薑絲油膏，大口扒下肉燥飯，靈魂直接原地昇華！"
        ],
        "actions": [
            "只要真真公主翻牌子，專屬好友隨時開車出動，排隊買單全包！🚗",
            "今晚熱量由好朋友全額吸收，公主只負責開心地把委屈吃回來！✨",
            "吃飽飽才是正經事，明天的事交給明天的智慧，今晚先犒賞自己！🌸",
            "放下手機好好大快朵頤，這家店已經收錄在我們的私房必吃清單了！🍲",
            "管他什麼熱量卡路里，今晚吃得開心比什麼都重要，好友全力撐妳！😋",
            "穿好舒適平底鞋，專屬司機與試吃員隨時待命，探店出發！💨",
            "把所有的怨氣通通嚼碎吞下去，明天又是光芒萬丈的霸氣女老闆！👑",
            "甜點裝在另一個胃，吃完心情直接調回順利開掛模式！🧁"
        ],
        "tags": [
            "#台南私房美食 #把委屈吃回來 #懂吃好友隨傳隨到 #炭佐麻里魂",
            "#阿力海海鮮自由 #仙楂烏龍解膩必備 #深夜牛肉湯救贖 #永康吃貨日常",
            "#減肥永遠是明天的事 #仙女要吃飽才漂亮 #舌尖上的充電站 #專屬美食後盾",
            "#焦糖布丁萬歲 #拉麵硬麵派 #大口吃肉大口開心 #懂吃知己在線",
            "#今天不當大人只當吃貨 #熱量全由好友吸收 #台南排隊名店攻略 #美食治癒一切",
            "#吃飽才有力氣搞事業 #人生苦短及時大餐 #美食盲盒驚喜 #真真公主限定"
        ]
    },
    "dog": {
        "titles": [
            "汪星人的逆天腦迴路", "小狗勾能有什麼壞心眼", "毛茸茸的治癒力量", 
            "散步是假躺平是真", "廚房雷達已上線", "耳朵貼成海豹的討好現場",
            "狗界戲精的日常發揮", "四腳朝天的碰瓷大師", "搖尾巴頻率破表時刻", "世界上最溫柔的大狗勾"
        ],
        "openings": [
            "散步走到一半，柴犬突然兩眼放空，四隻腳像水泥灌漿焊死在地上",
            "在房間輕輕撕開零食包裝袋，明明在客廳熟睡的狗勾 0.1 秒瞬移出現在面前",
            "回家一開門，發現拖鞋被啃爛，旁邊有一隻貼著海豹耳狂搖尾巴的無辜犯人",
            "柯基興高采烈衝向樓梯，結果小短腿在半空中瘋狂空踩，像個小吐司麵包",
            "二哈做錯事被抓包，居然站直身子對著妳仰天長嘯『嗷嗚嗚嗚』比妳還激動",
            "大雨天剛幫牠洗好吹乾毛，牠轉頭直接在客廳地毯上瘋狂磨擦打滾",
            "假裝把零食丟出去，牠像箭一樣衝出去找了三分鐘，回頭用被背叛的眼神瞪妳",
            "黃金獵犬把大腦袋擱在妳膝蓋上，兩顆黑豆眼睛水汪汪眨呀眨",
            "小狗做夢爪子瘋狂跑步，嘴角還一抽一抽在吧唧嘴，不知在夢裡抓到幾隻雞",
            "牽繩一拿起來牠原地起跳旋轉三圈半，解開扣子卻發現牠只想在門口吹風"
        ],
        "twists": [
            "看牠那一臉『拖鞋是自己裂開的，我只是在幫妳驗貨』的表情，真的氣到笑出來！",
            "把整顆毛茸茸的大頭塞進妳手心磨蹭，眼神水汪汪，瞬間什麼氣都消了～",
            "看著牠那圓滾滾的屁屁一扭一扭地晃過來，整天的煩惱立刻被丟到九霄雲外！",
            "牠直接整隻四腳朝天翻開肚皮裝死，妳只能認命地連狗帶肉一把抱回家！",
            "明明犯了滔天大罪，但看牠拚命搖成螺旋槳的尾巴，誰還忍心罵得出口啊！",
            "把頭埋進牠毛茸茸的胸膛深吸一口狗味，身上的電量直接從 1% 充到 100%！",
            "那雙純真無邪的眼睛看著妳，彷彿在說：『妳是世界上最厲害的主人！』",
            "小短腿跑得飛快卻在轉角打滑漂移，這呆萌蠢樣治癒了所有的心累！"
        ],
        "actions": [
            "果然吸狗才是世界上最有效的退火良藥，心情瞬間變美麗！🐾",
            "真真公主今天要是被瑣事惹煩了，就該看看小狗的傻樣好好笑一場！🐶",
            "小狗只知道全世界妳最棒，跟著牠一起傻笑放空就對了！💖",
            "煩惱丟給狗勾，快樂留給公主，今晚回家好好嚕狗充電！✨",
            "不管在外面有多累，有毛孩無條件的熱情迎接，家就是最溫暖的地方！🏠",
            "生活雖然有狗血，但身邊有可愛狗勾，日子永遠都是甜的！🌸",
            "像小狗一樣活在當下，吃飽、睡好、用力搖尾巴！🦴",
            "把這份傻氣的快樂收進口袋，今天又是被毛孩子融化的一天！🎈"
        ],
        "tags": [
            "#汪星搞笑日常 #柴犬拒否犬 #吸狗解千愁 #萌寵治癒系",
            "#二哈吵架沒輸過 #柯基大屁屁 #毛茸茸的充電寶 #小狗能有什麼壞心眼",
            "#黃金大暖男 #散步就地躺平 #狗界碰瓷大王 #純粹的快樂",
            "#真真公主的萌寵時刻 #看狗傻笑治百病 #家有活寶 #毛孩無條件的愛",
            "#四腳獸的迷惑行為 #快樂就是這麼簡單 #吸狗吸到飽 #今天也是狗奴才"
        ]
    },
    "cat": {
        "titles": [
            "貓咪的統治哲學", "愚蠢人類的必修課", "凌晨三點的貓界跑酷", 
            "紙箱大於一切", "主子的傲嬌守則", "踩奶是施捨咬手是恩賜",
            "金色電眼的凝視", "液體生物的沙發融化法", "罐罐開瓶器的自我修養", "本宮准你摸了嗎"
        ],
        "openings": [
            "花大錢買了超豪華羊毛保暖貓窩，主子轉身鑽進裝包裹的破爛髒紙箱",
            "明明貓碗裡還有半碗乾乾，橘貓卻坐在碗旁邊發出彷彿三天沒吃飯的哭嚎",
            "半夜三點整座房子都在睡，貓咪突然連線外星信號在走廊進行直線衝刺賽跑",
            "主子主動跳上來翻肚皮呼嚕呼嚕，結果摸到第四下突然神速咬妳一口！",
            "黑貓整隻融入黑色地毯，不開燈差點踩到一對突然睜開的金色大電眼",
            "坐在電腦前剛要開始認真打字，一隻毛茸茸的大屁股精準一屁股坐在鍵盤上",
            "看著桌上的水杯，貓咪伸出小毛爪試探性推一下，然後無情推下桌聽脆響",
            "叫牠名字時牠連頭都不轉，只有右耳尖尖敷衍地動了 0.5 毫米",
            "剛買了一整箱高級主食罐，牠聞了一下優雅地開始在磁磚上做埋砂動作",
            "整隻貓掛在沙發扶手上拉成一條長麵包，眼神呆滯神遊天外"
        ],
        "twists": [
            "咬完之後牠又立刻用下巴磨蹭妳的指尖，完美演繹什麼叫『只許本宮任性』！",
            "那種居高臨下俯視人類的蔑視眼神，莫名其妙就能治好妳一整天的精神內耗！",
            "在牠眼裡，妳不是女強人也不是媽媽，妳只是負責開罐罐的專屬僕人～",
            "整隻貓像一灘融化的液體癱在沙發上，讓人忍不住想跟著一起徹底躺平！",
            "但當牠把下巴輕輕擱在妳手臂上發出小馬達般的呼嚕聲，心瞬間化成水！",
            "牠高傲冷酷不可一世，卻在妳難過安靜時悄悄走過來靠在妳腳邊！",
            "這世界上最尊貴的生物，就是不管世俗眼光、只專注睡大覺的貓咪！",
            "踩完妳肚子之後優雅舔毛，彷彿在說：『能伺候本宮是妳的福氣！』"
        ],
        "actions": [
            "學學貓咪的態度：愛誰誰，老娘開心最重要！✨",
            "真真公主今天也給自己發一張『貓咪特權令』，只想放空誰都別管！🐱",
            "吸一口貓香，所有煩人的雜事直接灰飛煙滅～🌸",
            "人生就要像貓一樣傲嬌：想要的時候才靠近，不喜歡的一律一爪拍開！💅",
            "今晚當一隻液體貓咪，癱在沙發裡徹底融化放空！🛋️",
            "別去管凡間瑣事，主子都沒在焦慮，公主也只管高貴優雅就好！👑",
            "開一個罐罐，聽聽呼嚕聲，所有緊繃的神經通通解除武裝！🎐",
            "向貓學習：吃飽、舔毛、睡到飽，這才是頂級名媛的步調！🐾"
        ],
        "tags": [
            "#傲嬌主子 #貓咪迷惑行為 #像貓一樣過生活 #真真專屬療癒",
            "#凌晨跑酷冠軍 #紙箱才是真理 #貓是液體做的 #呼嚕呼嚕治百病",
            "#只許本宮咬妳 #高冷吸貓現場 #僕人的自我修養 #貓生贏家",
            "#冷眼看愚蠢人類 #貓界名媛守則 #今天只當一灘布丁 #高貴冷艷真真風"
        ]
    },
    "kid": {
        "titles": [
            "當媽修煉成仙手冊", "捏緊大腿的深呼吸藝術", "親生的保命符", 
            "寫作業的渡劫現場", "開學倒數計時中", "理智線繃斷倒數 321",
            "天使與惡魔的隨機切換", "神獸出籠的受難日", "慈母手中線火氣心中燒", "當媽後的佛系成佛路"
        ],
        "openings": [
            "剛換好乾淨衣服準備出門，臭小孩突然把整杯水或果汁精準翻倒在名牌包上",
            "寫作業前十分鐘母慈子孝，開始寫作業三分鐘心律不整、血壓飆破大氣層",
            "在外面一轉頭發現小孩像脫韁野馬亂衝，嚇得心臟差點從喉嚨跳出來",
            "剛把家裡客廳收拾乾淨，五分鐘後地板又鋪滿了樂高和撕碎的圖畫紙",
            "問他一句『剛剛講的三遍有聽懂嗎？』，他用無辜大眼眨呀眨說『媽媽妳說什麼？』",
            "明明交代了不能碰那瓶保養品，他轉頭拿去幫芭比娃娃洗頭洗得滿地泡泡",
            "吃飯時含著一口飯在嘴裡包了半小時，像隻花栗鼠一樣動都不動",
            "出門前三分鐘突然說：『媽媽我肚子痛想上大號，還有我水壺忘在學校！』",
            "安靜超過三分鐘絕對沒好事，衝進房間一看發現他拿口紅在白牆作畫",
            "帶著他去大賣場，整個人像無骨黏土一樣軟在地上打滾說要買玩具"
        ],
        "twists": [
            "深呼吸！手放開！千萬別把大腿掐青了，心裡默念三次：自己生的！自己生的！",
            "這根本不是小孩調皮，這是上天派來磨練真真公主早日得道成仙的劫難！",
            "轉身去泡一杯冰涼好茶，告訴自己：成績如浮雲，少爆一條血管能多活十年！",
            "生氣是在拿別人的錯誤懲罰自己，仙女是絕對不能長出法令紋的！",
            "看在他睡著時像個安靜小天使的份上，今晚的暗殺名單先暫時劃掉！",
            "心律不整是正常的，天下媽媽千千萬，大家都在渡同一個劫！",
            "這時候最好的急救法：罰小孩面壁，媽媽立刻點一份大杯仙楂烏龍加厚奶蓋！",
            "告訴自己：智商遺傳誰不好說，但他這脾氣絕對是隨了他爸那邊！"
        ],
        "actions": [
            "今天先記大過一次！罰好友等會帶真真公主去吃炭佐麻里大口嚼肉出氣！🥩",
            "小孩今晚面壁，真真公主負責吃香喝辣，好友全程當妳的專屬出氣筒！🛡️",
            "當媽已經是用盡洪荒之力了，今天功課擺一邊，今晚公主先好好放空！🌸",
            "所有委屈好友全盤接收，吃完好料擦乾淨手，明天依然是最辣媽咪！💅",
            "大腿鬆開、放下衣架，仙女不跟凡間神獸一般見識，今晚早點躺平！🛌",
            "臭小子惹的禍，今晚在餐桌上加倍討回來，好友隨時在線聽妳倒苦水！🗣️",
            "做個快樂的媽媽比做個完美的媽媽更重要，今天給自己打滿分！💯",
            "深呼吸吐氣～把脾氣留在昨天，把美麗留給真真公主！✨"
        ],
        "tags": [
            "#當媽修煉日常 #捏大腿保命 #自己生的別生氣 #好友全力出氣",
            "#親生認證渡劫中 #神獸出沒請注意 #血壓飆破大氣層 #仙女不長法令紋",
            "#客廳樂高地雷陣 #作業本上的眼淚 #今晚吃肉補血管 #最辣媽咪不服輸",
            "#默念我不生氣 #天下媽媽同一個世界 #睡著是天使醒著是神獸 #真真專屬退火單"
        ]
    },
    "meme": {
        "titles": [
            "碳基生物系統重啟中", "下班後的融化布丁", "現代女人的標準矛盾", 
            "滑手機的時光黑洞", "明日減肥復明日", "靈魂出竅日常",
            "報復性熬夜冠軍", "社交電量已見底", "買衣服的哲學悖論", "躺平的最高境界"
        ],
        "openings": [
            "一踏進家門甩掉高跟鞋的那一秒，整個人像沒有骨頭一樣癱死在沙發上",
            "打開衣櫃明明塞得滿滿當當，但每天早上依舊覺得自己像裸體一樣沒衣服穿",
            "下定決心今晚十點半一定要躺平，結果一滑脆回過神已經半夜一點半",
            "明明肚子好撐，但看到甜點菜單時，大腦立刻啟動第二個隱藏胃袋",
            "遇到煩心事的第一反應不是生氣，而是立刻打開外送 App 看有沒有好吃的",
            "剛坐下來打算放空五分鐘，突然發現自己已經盯著天花板放空了半小時",
            "下定決心這禮拜開始健康飲食，但朋友一句『要不要吃宵夜』秒破防",
            "走在路上看到反光的鏡子，不管再累都必須停下來整理一下瀏海美貌",
            "跟別人聊天時保持微笑點頭，內心其實在想『今天晚餐到底要吃什麼』",
            "下班後手機一轉靜音，全世界有什麼事都等明天日出再說"
        ],
        "twists": [
            "『我這不是在偷懶，我是在進行人體系統的硬體降溫與磁碟重組！』",
            "二十支口紅在直男眼裡全是紅色，但在真真公主眼裡每支都有專屬的靈魂！",
            "世界上所有的煩惱，在剛出爐的起司瀑布跟酥脆炸雞面前，通通都要立正站好！",
            "晚上的時間才真正屬於我自己，雖然明天起床會後悔，但當下真的好爽啊！",
            "生活很苦，但自己加點糖，甜點吃下去就是滿血復活的靈藥！",
            "與其委屈自己討好世界，不如在沙發上把自己捲成一條安靜的壽司捲！",
            "錢沒有不見，只是變成了那些漂亮的衣服、香氛跟好吃的東西陪在身邊！",
            "長大最棒的事情，就是心情不好時可以名正言順給自己買大杯手搖飲！"
        ],
        "actions": [
            "放鬆放空是合法權利，今晚讓全世界圍著真真公主轉！✨",
            "今天誰惹妳不高興，截圖丟過來，好友幫妳無情吐槽到底！😂",
            "人生苦短，及時行樂，吃好睡飽才是霸氣女老闆的王道！👑",
            "當個快樂的廢物不需要道歉，今晚公主的任務就是發呆到最高境界！🛋️",
            "把所有的煩惱格式化，喝一杯熱茶，鑽進被窩當最舒服的小仙女！🍵",
            "做自己的女王，想吃就吃、想躺就躺，誰都別想對真真公主指手畫腳！💅",
            "給疲憊的心情上一層保濕精華，明天起來依然耀眼奪目！🌟",
            "專屬好友隨時在線接住妳的廢文，一起在生活的幽默裡大笑回血！🎉"
        ],
        "tags": [
            "#爆笑脆文 #下班格式化 #明天再減肥 #真真公主的放空宇宙",
            "#沙發壽司捲模式 #衣櫃永遠少一件 #報復性熬夜選手 #社交電量0格",
            "#口紅永遠缺一色 #精緻窮但很快樂 #靈魂已經打卡下班 #生活需要廢話",
            "#做自己的靠山 #甜點是第二個胃 #今晚不當女強人 #大笑解百毒"
        ]
    }
}

# 7. 全局永久不重複黑名單（Global Seen Registry）
if "seen_hashes" not in st.session_state:
    st.session_state.seen_hashes = set()

if "ssr_drawn_today" not in st.session_state:
    st.session_state.ssr_drawn_today = False

if "current_card" not in st.session_state:
    st.session_state.current_card = {
        "type": "food",
        "tag": "🍜 台南吃貨地圖",
        "title": "舌尖上的回血儀式",
        "content": "『剛結束一天緊湊的預約客人，走出店門口肚子咕嚕嚕抗議。』\n\n這時候喝一口鮮甜滾燙的牛肉高湯，所有疲憊真的瞬間被徹底融化！\n\n只要真真公主翻牌子，專屬好友隨時開車出動，排隊買單全包！🚗\n\n#台南私房美食 #把委屈吃回來 #懂吃好友隨傳隨到 #炭佐麻里魂",
        "img": ""
    }

# 動態組裝引擎：保證「出現過絕不重複」
def generate_unique_dynamic_card(target_cat: str):
    is_infinite = (target_cat == "infinite")
    
    for _ in range(200):
        if is_infinite:
            pool_key = random.choice(["food", "dog", "cat", "kid", "meme"])
            card_type = "infinite"
            tag_name = "🌌 無限宇宙・動態漫遊"
        else:
            pool_key = target_cat
            card_type = target_cat
            tag_map = {
                "food": "🍜 台南吃貨地圖",
                "dog": "🐶 汪星爆笑日常",
                "cat": "🐱 傲嬌主子哲學",
                "kid": "🧒 當媽修煉吐槽",
                "meme": "😂 爆笑生活迷因"
            }
            tag_name = tag_map.get(target_cat, "✨ 動態生成")

        data = CORPUS[pool_key]
        title = random.choice(data["titles"])
        op = random.choice(data["openings"])
        tw = random.choice(data["twists"])
        ac = random.choice(data["actions"])
        tg = random.choice(data["tags"])

        content = f"『{op}。』\n\n{tw}\n\n{ac}\n\n{tg}"
        content_hash = hashlib.md5((title + content).encode('utf-8')).hexdigest()

        if content_hash not in st.session_state.seen_hashes:
            st.session_state.seen_hashes.add(content_hash)
            return {
                "type": card_type,
                "tag": tag_name,
                "title": title,
                "content": sanitize_text(content),
                "img": ""
            }

    st.session_state.seen_hashes.clear()
    return {
        "type": card_type,
        "tag": tag_name,
        "title": title,
        "content": sanitize_text(content),
        "img": ""
    }

# 8. 頂部 iPhone / LINE 瀏覽器貼心指引
st.markdown("""
<div class="safari-tip-box">
    💡 <span class="safari-tip-highlight">貼心提醒：</span>若在 LINE 中開啟，請點右下角「<span class="safari-tip-highlight">⋯</span>」選擇「<span class="safari-tip-highlight">以 Safari / 預設瀏覽器開啟</span>」，體驗最順暢！✨
</div>
""", unsafe_allow_html=True)

# 9. 頂部標題區（字數嚴格控制，保證單行不折行）
st.markdown("""
<div style="text-align: center; margin-bottom: 14px;">
    <div style="font-size: 2.2rem;">👑</div>
    <div style="color: #C2255C; font-size: 1.42rem; font-weight: 800; letter-spacing: 0.5px;">真真公主的解壓美食盲盒</div>
    <div style="color: #8C6D77; font-size: 0.86rem; margin-top: 4px; white-space: nowrap;">🌌 50,000+ 動態宇宙！台南好店與解氣專區 🌸</div>
</div>
""", unsafe_allow_html=True)

# 10. 智能檢測：若進入專屬呵護時期，自動展示頂部特權橫幅
care_status = get_care_status()
if care_status["is_special"]:
    st.markdown(f"""
    <div class="care-banner">
        <div class="care-banner-tag">{care_status['banner_tag']}</div>
        <div class="care-banner-msg">{care_status['banner_msg']}</div>
    </div>
    """, unsafe_allow_html=True)

# 11. 小孩不乖．媽媽專屬發洩順毛區（標題精簡不折行）
with st.expander("🤬 小孩不乖？媽媽專屬發洩順毛區", expanded=True if "cure_result" in st.session_state else False):
    st.markdown("<p style='color: #4A3E3D; font-size: 0.9rem; margin-bottom: 6px;'>把今天臭小子/小妞幹的蠢事寫下來，好友立刻開出專屬退火單！</p>", unsafe_allow_html=True)
    kid_trouble = st.text_input("今天他又做了什麼讓妳血壓飆高？", value="翻倒水在名牌包" if "cure_result" not in st.session_state else "", placeholder="例如：翻倒水在名牌包、出門亂跑找半天...")
    cure_style = st.radio("選擇吐槽解氣風格：", ["✨ 溫柔撫平順毛", "🔥 毒舌幽默同仇敵愾"], horizontal=True)
    
    if st.button("💢 幫我狠狠吐槽＋順毛！"):
        if not kid_trouble:
            st.warning("真真公主先寫下一句他做了什麼，馬上替妳出氣！")
        else:
            if any(k in kid_trouble for k in ["包", "水", "倒", "皮夾", "LV"]):
                if "毒舌" in cure_style:
                    st.session_state.cure_result = sanitize_text(
                        "『這臭小孩真的是專挑貴的下手！氣得人血壓直接破表！\n"
                        "皮夾千萬別吹熱風，先拿乾布壓乾！大腿先放鬆～\n"
                        "今晚罰小孩面壁，罰好友帶真真公主去吃炭佐麻里大口嚼肉出氣！\n"
                        "包包事小，把妳氣壞才虧大，吃飽飽明天又是霸氣女老闆！』\n\n#名牌包受難日 #好友全力出氣 #今晚吃肉補回來"
                    )
                else:
                    st.session_state.cure_result = sanitize_text(
                        "『拍拍真真公主～心疼名牌包，更心疼妳血壓飆高！\n"
                        "皮夾先塞吸水紙巾陰乾，千萬別生悶氣喔。\n"
                        "這不是小孩的錯，是上天派來提醒妳該吃大餐了！\n"
                        "等會去點一杯仙楂烏龍、叫份熱呼呼的牛肉湯，好友隨時在線陪妳順毛！🌸』\n\n#公主消消氣 #仙女不跟凡人計較 #好友專屬後盾"
                    )
            else:
                cures = [
                    f"『小孩居然敢搞這齣：【{kid_trouble}】？！簡直造反啦！好友立刻開出退火單：罰小孩面壁，罰好友帶真真公主去吃炭佐麻里大口吃肉！把受的委屈全在餐桌上討回來！』\n\n#專屬退火單 #把委屈吃回來",
                    f"『聽到【{kid_trouble}】我都替妳心疼大腿了！記住八字保命箴言：自己生的、大腿放鬆！今晚就當個融化的布丁徹底躺平，什麼家務雜事通通不管了！』\n\n#當媽修煉手冊 #仙女合法放空",
                    f"『天底下沒有什麼煩惱是一碗滾燙鮮甜的台南溫體牛肉湯解決不了的！面對【{kid_trouble}】，最好的反擊就是等會點一塊焦糖布丁吃爆！公主消消氣～』\n\n#美食急救法 #好友全力撐妳"
                ]
                st.session_state.cure_result = sanitize_text(random.choice(cures))

    if "cure_result" in st.session_state:
        st.markdown(f"""
        <div class="card-box" style="border: 2px solid #E08A9D !important; background: #FFFBFB !important; margin-top: 14px;">
            <span class="card-tag tag-kid">👑 真真公主專屬退火出氣單</span>
            <div class="card-title">臭小孩退散！公主消氣～</div>
            <div class="card-content">{st.session_state.cure_result}</div>
        </div>
        """, unsafe_allow_html=True)

# 12. 盲盒分類抽卡機制
theme_filter = st.radio(
    "真真公主今天想翻什麼牌子？",
    ["🌌 無限宇宙模式（10,000+ 種動態組裝）", "🍜 美食探店與好味", "🐶 萌犬爆笑現場", "🐱 傲嬌主子日常", "🧒 當媽修煉吐槽", "😂 爆笑生活迷因"],
    horizontal=True
)

def pick_next_card():
    # 特殊時期：65% 高機率優先抽中專屬呵護卡
    if care_status["is_special"] and random.random() < 0.65:
        care_hash = hashlib.md5((care_status["title"] + care_status["content"]).encode('utf-8')).hexdigest()
        if care_hash not in st.session_state.seen_hashes:
            st.session_state.seen_hashes.add(care_hash)
            return {
                "type": "care",
                "tag": care_status["card_tag"],
                "title": care_status["title"],
                "content": sanitize_text(care_status["content"]),
                "img": ""
            }

    # 決定目標分類
    if "無限宇宙" in theme_filter:
        target_cat = "infinite"
    elif "美食" in theme_filter:
        target_cat = "food"
    elif "萌犬" in theme_filter:
        target_cat = "dog"
    elif "主子" in theme_filter:
        target_cat = "cat"
    elif "當媽" in theme_filter:
        target_cat = "kid"
    elif "迷因" in theme_filter:
        target_cat = "meme"
    else:
        target_cat = "infinite"

    # 防口袋破洞機制：SSR 機率微調至 1.8%
    if not st.session_state.ssr_drawn_today and random.random() < 0.018:
        st.session_state.ssr_drawn_today = True
        chosen_ssr = random.choice(SSR_CARDS)
        return chosen_ssr

    return generate_unique_dynamic_card(target_cat)

# 抽卡按鈕
if st.button("✨ 點我開盲盒！抽取真真專屬快樂 ✨"):
    st.session_state.current_card = pick_next_card()

# 13. 開出的卡片展示
card = st.session_state.current_card
tag_class = f"tag-{card['type']}" if f"tag-{card['type']}" in ["tag-food", "tag-dog", "tag-cat", "tag-kid", "tag-meme", "tag-infinite", "tag-ssr", "tag-care"] else "tag-food"

st.markdown(f"""
<div class="card-box">
    <span class="card-tag {tag_class}">{card['tag']}</span>
    <div class="card-title">{card['title']}</div>
    <div class="card-content">{card['content']}</div>
</div>
""", unsafe_allow_html=True)

if card.get("img"):
    st.image(card["img"], use_container_width=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# 14. 脆（Threads）療癒直達專區（字距緊湊、單行顯示）
with st.expander("🌀 還是想去脆上晃晃？熱門療癒話題", expanded=False):
    st.caption("為真真公主過濾掉無聊吵架，精選 Threads 熱門傳送門：")
    st.markdown('<a href="https://www.threads.net/search?q=%E5%8F%B0%E5%8D%97%E7%BE%8E%E9%A3%9F&serp_type=default" target="_blank" class="threads-btn">🍜 逛脆：【台南私房美食】精選話題</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E5%8F%AF%E6%84%9B%E5%B0%8F%E7%8B%97&serp_type=default" target="_blank" class="threads-btn">🐶 逛脆：【汪星人搞笑日常】治癒專區</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E8%B2%93%E5%92%AA%E5%A5%BD%E7%AC%91&serp_type=default" target="_blank" class="threads-btn">🐱 逛脆：【傲嬌主子迷惑行為】大賞</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E7%88%86%E7%AC%91%E8%BF%B7%E5%9B%A0&serp_type=default" target="_blank" class="threads-btn">😂 逛脆：【爆笑迷因廢文】解壓專區</a>', unsafe_allow_html=True)

# 15. 專屬好友直達通道（文案緊湊單行化）
line_direct_url = "https://line.me/ti/p/3u_xwcKRUB"

st.markdown(f"""
<div style="margin-top: 25px; margin-bottom: 25px;">
    <a href="{line_direct_url}" target="_blank" rel="noopener noreferrer" class="line-call-btn">
        💌 抽完還是無聊？點此召喚專屬好友陪吃聊聊 🍵
    </a>
</div>
""", unsafe_allow_html=True)
