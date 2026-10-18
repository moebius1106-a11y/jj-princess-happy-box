import streamlit as st
import random
import hashlib

# 1. 頁面基本配置（針對 iPhone 視窗與 LINE 瀏覽器最佳化）
st.set_page_config(
    page_title="👑 真真公主的解壓美食盲盒",
    page_icon="👑",
    layout="centered"
)

# 2. iPhone WebKit 深度優化與真楨美學專屬配色加固 CSS
st.markdown("""
<style>
/* 徹底鎖定 iOS 淺色渲染，防止 iPhone 深色模式反轉造成字體反白隱形 */
:root {
    color-scheme: light !important;
    -webkit-color-scheme: light !important;
}

/* 適配 iPhone 頂部動態島 / 瀏海與底部安全區域 (Home Bar) */
.block-container {
    padding-top: max(0.8rem, env(safe-area-inset-top)) !important;
    padding-bottom: max(3.5rem, env(safe-area-inset-bottom)) !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
    -webkit-text-size-adjust: 100% !important;
}

/* 隱藏官方雜項與浮水印 */
#MainMenu, footer, header, [data-testid="manage-app-button"], div[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}

/* iOS 專屬字體平滑與觸控反饋，消除雙擊放大延遲 */
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

/* 摺疊面板 (Expander) 標題顯色加固 */
.streamlit-expanderHeader, div[data-testid="stExpander"] summary span, div[data-testid="stExpander"] details summary {
    color: #C2255C !important;
    font-weight: 700 !important;
    font-size: 0.96rem !important;
}
div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1.5px solid #F3DFE3 !important;
    margin-bottom: 14px !important;
    box-shadow: 0 4px 14px rgba(224, 138, 157, 0.1) !important;
}

/* 單選按鈕文字顯色加固 */
div[role="radiogroup"] label p, div[role="radiogroup"] label span {
    color: #4A3E3D !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}
.stRadio > label {
    color: #C2255C !important;
    font-weight: 700 !important;
}

/* 徹底修正 Radio 單選圓圈變黑問題 */
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

/* 盲盒卡片效果 */
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

/* 抽卡按鈕 */
.stButton>button {
    background: linear-gradient(135deg, #E08A9D 0%, #D47A8F 100%) !important;
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    border-radius: 24px !important;
    border: none !important;
    padding: 13px 20px !important;
    box-shadow: 0 6px 18px rgba(224, 138, 157, 0.35) !important;
    width: 100% !important;
    touch-action: manipulation !important;
    transition: transform 0.08s ease;
}
.stButton>button:active {
    transform: scale(0.96) !important;
}

/* 脆（Threads）按鈕 */
.threads-btn {
    display: block;
    background: #2D2426;
    color: #FFFFFF !important;
    text-align: center;
    padding: 12px 14px;
    border-radius: 18px;
    font-weight: 700;
    text-decoration: none;
    margin-top: 8px;
    font-size: 0.92rem;
    touch-action: manipulation;
}

/* LINE 專屬呼叫按鈕樣式 */
.line-call-btn {
    display: block;
    width: 100%;
    background: linear-gradient(135deg, #E08A9D 0%, #C2255C 100%);
    color: #FFFFFF !important;
    text-align: center;
    padding: 14px 18px;
    border-radius: 26px;
    font-weight: 800;
    text-decoration: none !important;
    font-size: 0.98rem;
    box-shadow: 0 6px 20px rgba(194, 37, 92, 0.3);
    touch-action: manipulation;
    transition: transform 0.08s ease;
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

# 4. 精選靜態母庫（含 SSR 專屬卡）
STATIC_CARDS = [
    {
        "type": "ssr",
        "tag": "👑 專屬特權・SSR 稀有卡",
        "title": "🍲 台南私房好料隨傳隨到探店券",
        "content": "恭喜真真公主抽到稀有 SSR！\n【兌換權利】：\n只要公主想吃，不管是台南排隊名店、隱藏甜點、深夜罪惡牛肉湯還是火鍋，好友無條件出動陪吃探店，排隊與熱量全由好友吸收！🚗💨",
        "img": ""
    },
    {
        "type": "ssr",
        "tag": "👑 專屬特權・SSR 稀有卡",
        "title": "🍰 專屬下午茶與手搖補血券",
        "content": "恭喜真真公主抽到限量 SSR！\n【兌換權利】：\n今天店裡忙翻、帶小孩血壓飆高想喝甜的？出示此截圖，好友立刻奉上好茶甜點，真真公主只要張嘴負責吃，好好回血放空！🧁",
        "img": ""
    },
    {
        "type": "ssr",
        "tag": "👑 專屬特權・SSR 稀有卡",
        "title": "🛡️ 專屬出氣筒與無限順毛券",
        "content": "恭喜真真公主抽到頂級 SSR！\n【兌換權利】：\n今日不論心情多煩、遇到什麼鳥事想吐槽，好友無條件站妳這邊同仇敵愾，不講大道理、全心全意把真真公主哄開心為止！🌸",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🍜 台南吃貨地圖",
        "title": "排隊也是一種懂吃儀式",
        "content": "『拉麵要排隊？沒關係！』\n只要湯頭夠濃郁、叉燒夠嫩，等待都是值得的。\n跟懂吃的好友邊聊天邊等位子，不知不覺就輪到我們，大口喝湯吃肉的瞬間，整天的疲勞直接歸零！",
        "img": ""
    },
    {
        "type": "dog",
        "tag": "🐶 柴犬頑固現場",
        "title": "散步終點站：就地躺平",
        "content": "走到了十字路口，柴柴突然決定：『我今天就走到這裡了。』\n脖子直接縮成雙下巴麻糬，四隻腳像塗了強力膠焊死在柏油路上，人類只能尷尬地在路人圍觀下把一整坨肉抱回家！",
        "img": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80"
    },
    {
        "type": "cat",
        "tag": "🐱 貓界霸王條款",
        "title": "可以摸，但只能摸三下",
        "content": "第一下：呼嚕呼嚕好舒服～\n第二下：本宮准你摸。\n第三下：一口咬住人類的手！\n『大膽！誰准你摸第四下的！』（咬完兩秒後又用頭蹭你的手心討肉泥）",
        "img": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=600&auto=format&fit=crop&q=80"
    }
]

# 5. 分類專屬的「萬向矩陣語意庫」（徹底避免跨類混雜與重複）
CORPUS = {
    "food": {
        "titles": ["台南吃貨的深夜救贖", "舌尖上的回血儀式", "今天不談減肥只談快樂", "永康隱藏美食私房話", "甜點是仙女的充電寶"],
        "openings": [
            "剛結束一天緊湊的預約客人，走出店門口肚子咕嚕嚕抗議",
            "深夜滑著 IG，滿螢幕都在推台南在地現切溫體牛肉湯",
            "突然超級想吃熱騰騰又香氣逼人的排隊拉麵濃郁湯頭",
            "下午店務告一段落，靈魂極度渴望一塊現烤焦糖布丁或法式千層",
            "晚餐時間到了，腦袋瞬間進入選擇障礙的放空模式"
        ],
        "twists": [
            "這時候喝一口鮮甜滾燙的牛肉高湯，所有疲憊真的瞬間被徹底融化！",
            "炭佐麻里的烤肉滋滋作響，大口嚼肉的爽快感是任何保養品都換不來的！",
            "阿力海滿滿的生蠔、龍蝦跟哈根達斯，就是犒賞女強人最棒的禮物！",
            "來一杯酸甜生津的仙楂烏龍，微糖微冰，整個人都神清氣爽起來了！",
            "巷弄老宅剛出爐的肉桂捲，那股肉桂黑糖香氣直接把好心情補到滿格！"
        ],
        "actions": [
            "只要真真公主翻牌子，專屬好友隨時開車出動，排隊買單全包！🚗",
            "今晚熱量由好朋友全額吸收，公主只負責開心地把委屈吃回來！✨",
            "吃飽飽才是正經事，明天的事交給明天的智慧，今晚先犒賞自己！🌸",
            "放下手機好好大快朵頤，這家店已經收錄在我們的私房必吃清單了！🍲"
        ],
        "tags": ["#台南私房美食 #把委屈吃回來 #懂吃好友隨傳隨到 #炭佐麻里魂"]
    },
    "dog": {
        "titles": ["汪星人的逆天腦迴路", "小狗勾能有什麼壞心眼", "毛茸茸的治癒力量", "散步是假躺平是真", "廚房雷達已上線"],
        "openings": [
            "散步走到一半，柴犬突然兩眼放空，四隻腳像水泥灌漿焊死在地上",
            "在房間輕輕撕開零食包裝袋，明明在客廳熟睡的狗勾 0.1 秒瞬移出現在面前",
            "回家一開門，發現拖鞋被啃爛，旁邊有一隻貼著海豹耳狂搖尾巴的無辜犯人",
            "柯基興高采烈衝向樓梯，結果小短腿在半空中瘋狂空踩，像個小吐司麵包",
            "二哈做錯事被抓包，居然站直身子對著妳仰天長嘯『嗷嗚嗚嗚』比妳還激動"
        ],
        "twists": [
            "看牠那一臉『拖鞋是自己裂開的，我只是在幫妳驗貨』的表情，真的氣到笑出來！",
            "把整顆毛茸茸的大頭塞進妳手心磨蹭，眼神水汪汪，瞬間什麼氣都消了～",
            "看著牠那圓滾滾的屁屁一扭一扭地晃過來，整天的煩惱立刻被丟到九霄雲外！",
            "牠直接整隻四腳朝天翻開肚皮裝死，妳只能認命地連狗帶肉一把抱回家！"
        ],
        "actions": [
            "果然吸狗才是世界上最有效的退火良藥，心情瞬間變美麗！🐾",
            "真真公主今天要是被瑣事惹煩了，就該看看小狗的傻樣好好笑一場！🐶",
            "小狗只知道全世界妳最棒，跟著牠一起傻笑放空就對了！💖"
        ],
        "tags": ["#汪星搞笑日常 #柴犬拒否犬 #吸狗解千愁 #萌寵治癒系"]
    },
    "cat": {
        "titles": ["貓咪的統治哲學", "愚蠢人類的必修課", "凌晨三點的貓界跑酷", "紙箱大於一切", "主子的傲嬌守則"],
        "openings": [
            "花大錢買了超豪華羊毛保暖貓窩，主子轉身鑽進裝包裹的破爛髒紙箱",
            "明明貓碗裡還有半碗乾乾，橘貓卻坐在碗旁邊發出彷彿三天沒吃飯的哭嚎",
            "半夜三點整座房子都在睡，貓咪突然連線外星信號在走廊進行直線衝刺賽跑",
            "主子主動跳上來翻肚皮呼嚕呼嚕，結果摸到第四下突然神速咬妳一口！",
            "黑貓整隻融入黑色地毯，不開燈差點踩到一對突然睜開的金色大電眼"
        ],
        "twists": [
            "咬完之後牠又立刻用下巴磨蹭妳的指尖，完美演繹什麼叫『只許本宮任性』！",
            "那種居高臨下俯視人類的蔑視眼神，莫名其妙就能治好妳一整天的精神內耗！",
            "在牠眼裡，妳不是女強人也不是媽媽，妳只是負責開罐罐的專屬僕人～",
            "整隻貓像一灘融化的液體癱在沙發上，讓人忍不住想跟著一起徹底躺平！"
        ],
        "actions": [
            "學學貓咪的態度：愛誰誰，老娘開心最重要！✨",
            "真真公主今天也給自己發一張『貓咪特權令』，只想放空誰都別管！🐱",
            "吸一口貓香，所有煩人的雜事直接灰飛煙滅～🌸"
        ],
        "tags": ["#傲嬌主子 #貓咪迷惑行為 #像貓一樣過生活 #真真專屬療癒"]
    },
    "kid": {
        "titles": ["當媽修煉成仙手冊", "捏緊大腿的深呼吸藝術", "親生的保命符", "寫作業的渡劫現場", "開學倒數計時中"],
        "openings": [
            "剛換好乾淨衣服準備出門，臭小孩突然把整杯水或果汁精準翻倒在名牌包上",
            "寫作業前十分鐘母慈子孝，開始寫作業三分鐘心律不整、血壓飆破大氣層",
            "在外面一轉頭發現小孩像脫韁野馬亂衝，嚇得心臟差點從喉嚨跳出來",
            "剛把家裡客廳收拾乾淨，五分鐘後地板又鋪滿了樂高和撕碎的圖畫紙",
            "問他一句『剛剛講的三遍有聽懂嗎？』，他用無辜大眼眨呀眨說『媽媽妳說什麼？』"
        ],
        "twists": [
            "深呼吸！手放開！千萬別把大腿掐青了，心裡默念三次：自己生的！自己生的！",
            "這根本不是小孩調皮，這是上天派來磨練真真公主早日得道成仙的劫難！",
            "轉身去泡一杯冰涼好茶，告訴自己：成績如浮雲，少爆一條血管能多活十年！",
            "生氣是在拿別人的錯誤懲罰自己，仙女是絕對不能長出法令紋的！"
        ],
        "actions": [
            "今天先記大過一次！罰好友等會帶真真公主去吃炭佐麻里大口嚼肉出氣！🥩",
            "小孩今晚面壁，真真公主負責吃香喝辣，好友全程當妳的專屬出氣筒！🛡️",
            "當媽已經是用盡洪荒之力了，今天功課擺一邊，今晚公主先好好放空！🌸"
        ],
        "tags": ["#當媽修煉日常 #捏大腿保命 #自己生的別生氣 #好友全力出氣"]
    },
    "meme": {
        "titles": ["碳基生物系統重啟中", "下班後的融化布丁", "現代女人的標準矛盾", "滑手機的時光黑洞", "明日減肥復明日"],
        "openings": [
            "一踏進家門甩掉高跟鞋的那一秒，整個人像沒有骨頭一樣癱死在沙發上",
            "打開衣櫃明明塞得滿滿當當，但每天早上依舊覺得自己像裸體一樣沒衣服穿",
            "下定決心今晚十點半一定要躺平，結果一滑脆回過神已經半夜一點半",
            "明明肚子好撐，但看到甜點菜單時，大腦立刻啟動第二個隱藏胃袋",
            "遇到煩心事的第一反應不是生氣，而是立刻打開外送 App 看有沒有好吃的"
        ],
        "twists": [
            "『我這不是在偷懶，我是在進行人體系統的硬體降溫與磁碟重組！』",
            "二十支口紅在直男眼裡全是紅色，但在真真公主眼裡每支都有專屬的靈魂！",
            "世界上所有的煩惱，在剛出爐的起司瀑布跟酥脆炸雞面前，通通都要立正站好！",
            "晚上的時間才真正屬於我自己，雖然明天起床會後悔，但當下真的好爽啊！"
        ],
        "actions": [
            "放鬆放空是合法權利，今晚讓全世界圍著真真公主轉！✨",
            "今天誰惹妳不高興，截圖丟過來，好友幫妳無情吐槽到底！😂",
            "人生苦短，及時行樂，吃好睡飽才是霸氣女老闆的王道！👑"
        ],
        "tags": ["#爆笑脆文 #下班格式化 #明天再減肥 #真真公主的放空宇宙"]
    }
}

# 6. 核心生成器：保證 50 抽絕對零重複的動態組裝引擎
def generate_dynamic_card(category: str):
    # 若是「無限宇宙」，隨機從各類別抽取元素跨界融合
    if category == "infinite":
        pool_key = random.choice(["food", "dog", "cat", "kid", "meme"])
        data = CORPUS[pool_key]
        tag_name = "🌌 無限宇宙・動態漫遊"
        card_type = "infinite"
    else:
        data = CORPUS.get(category, CORPUS["food"])
        tag_map = {
            "food": "🍜 台南吃貨地圖",
            "dog": "🐶 汪星爆笑日常",
            "cat": "🐱 傲嬌主子哲學",
            "kid": "🧒 當媽修煉吐槽",
            "meme": "😂 爆笑生活迷因"
        }
        tag_name = tag_map.get(category, "✨ 動態生成")
        card_type = category

    title = random.choice(data["titles"])
    op = random.choice(data["openings"])
    tw = random.choice(data["twists"])
    ac = random.choice(data["actions"])
    tg = random.choice(data["tags"])

    content = f"『{op}。』\n\n{tw}\n\n{ac}\n\n{tg}"

    return {
        "type": card_type,
        "tag": tag_name,
        "title": title,
        "content": sanitize_text(content),
        "img": ""
    }

# 初始化 Session State
if "history_hashes" not in st.session_state:
    st.session_state.history_hashes = []

if "current_card" not in st.session_state:
    st.session_state.current_card = STATIC_CARDS[0]

# 7. 頂部標題區
st.markdown("""
<div style="text-align: center; margin-bottom: 14px;">
    <div style="font-size: 2.2rem;">👑</div>
    <div style="color: #C2255C; font-size: 1.45rem; font-weight: 800; letter-spacing: 0.5px;">真真公主的解壓美食盲盒</div>
    <div style="color: #8C6D77; font-size: 0.88rem; margin-top: 4px;">🌌 萬張無限動態生成！台南好店、吸貓嚕狗與爆笑解氣專區 🌸</div>
</div>
""", unsafe_allow_html=True)

# 8. 小孩不乖．媽媽專屬發洩順毛區（急速直出）
with st.expander("🤬 小孩不乖？媽媽專屬發洩順毛區（點開來吐苦水）", expanded=True if "cure_result" in st.session_state else False):
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
                    f"『小孩居然敢搞這齣：【{kid_trouble}】？！簡直造反啦！好友立刻開出退火單：罰小孩面壁，罰好友帶真真公主去吃阿力海生蠔龍蝦吃到飽！把受的委屈全在餐桌上討回來！』\n\n#專屬退火單 #把委屈吃回來",
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

# 9. 盲盒分類抽卡機制
theme_filter = st.radio(
    "真真公主今天想翻什麼牌子？",
    ["🌌 無限宇宙模式（10,000+ 種動態組裝）", "🍜 美食探店與好味", "🐶 萌犬爆笑現場", "🐱 傲嬌主子日常", "🧒 當媽修煉吐槽", "😂 爆笑生活迷因"],
    horizontal=True
)

def pick_next_card():
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

    # 15% 機率抽靜態 SSR 特權卡（給她驚喜感）
    if random.random() < 0.15:
        ssr_cards = [c for c in STATIC_CARDS if c["type"] == "ssr"]
        chosen = random.choice(ssr_cards)
        chosen_hash = hashlib.md5(chosen["content"].encode('utf-8')).hexdigest()
        if chosen_hash not in st.session_state.history_hashes:
            st.session_state.history_hashes.append(chosen_hash)
            if len(st.session_state.history_hashes) > 60:
                st.session_state.history_hashes.pop(0)
            return chosen

    # 動態組裝，強制 60 抽去重檢驗（保證絕不重複）
    attempts = 0
    while attempts < 30:
        attempts += 1
        card = generate_dynamic_card(target_cat)
        card_hash = hashlib.md5(card["content"].encode('utf-8')).hexdigest()
        if card_hash not in st.session_state.history_hashes:
            st.session_state.history_hashes.append(card_hash)
            # 維護長度 60 的去重隊列
            if len(st.session_state.history_hashes) > 60:
                st.session_state.history_hashes.pop(0)
            return card

    return card

# 抽卡按鈕
if st.button("✨ 點我開盲盒！抽取真真專屬快樂 ✨"):
    st.session_state.current_card = pick_next_card()

# 10. 開出的卡片展示
card = st.session_state.current_card
tag_class = f"tag-{card['type']}" if f"tag-{card['type']}" in ["tag-food", "tag-dog", "tag-cat", "tag-kid", "tag-meme", "tag-infinite", "tag-ssr"] else "tag-food"

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

# 11. 脆（Threads）療癒直達專區
with st.expander("🌀 還是想去脆上晃晃？點這裡直達熱門療癒話題", expanded=False):
    st.caption("為真真公主過濾掉無聊吵架，精選 Threads 上最受歡迎的美食與毛孩傳送門：")
    st.markdown('<a href="https://www.threads.net/search?q=%E5%8F%B0%E5%8D%97%E7%BE%8E%E9%A3%9F&serp_type=default" target="_blank" class="threads-btn">🍜 前往 Threads 查看最新【台南私房美食推薦】</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E5%8F%AF%E6%84%9B%E5%B0%8F%E7%8B%97&serp_type=default" target="_blank" class="threads-btn">🐶 前往 Threads 查看最新【汪星人搞笑日常】</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E8%B2%93%E5%92%AA%E5%A5%BD%E7%AC%91&serp_type=default" target="_blank" class="threads-btn">🐱 前往 Threads 查看最新【傲嬌貓貓迷惑行為】</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E7%88%86%E7%AC%91%E8%BF%B7%E5%9B%A0&serp_type=default" target="_blank" class="threads-btn">😂 前往 Threads 查看最新【爆笑迷因廢文】</a>', unsafe_allow_html=True)

# 12. 專屬好友直達通道
line_direct_url = "https://line.me/ti/p/3u_xwcKRUB"

st.markdown(f"""
<div style="margin-top: 25px; margin-bottom: 25px;">
    <a href="{line_direct_url}" target="_blank" rel="noopener noreferrer" class="line-call-btn">
        💌 抽完了還是無聊或肚子餓？點此召喚專屬好友出動陪吃聊聊 🍵
    </a>
</div>
""", unsafe_allow_html=True)
