import streamlit as st
import random
import time
import os

# 嘗試載入 AI 套件
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# 1. 頁面基本配置
st.set_page_config(
    page_title="👑 真真公主的解壓美食盲盒",
    page_icon="👑",
    layout="centered"
)

# 2. 真楨美學專屬配色 CSS（嚴格加固文字顯色，杜絕白字隱形）
st.markdown("""
<style>
:root {
    color-scheme: light !important;
}

.block-container {
    padding-top: max(0.8rem, env(safe-area-inset-top)) !important;
    padding-bottom: max(3.5rem, env(safe-area-inset-bottom)) !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
}

#MainMenu, footer, header, [data-testid="manage-app-button"], div[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}

/* 全局深可可色字體，解決白色隱形問題 */
html, body, [class*="css"], .stApp {
    color: #4A3E3D !important;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Helvetica Neue", sans-serif;
}
.stApp {
    background: linear-gradient(180deg, #FDF9F8 0%, #F5ECE9 100%) !important;
}

/* 強制摺疊面板 (Expander) 標題顯色 */
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
}

/* 單選按鈕文字顯色 */
div[role="radiogroup"] label p, div[role="radiogroup"] label span {
    color: #4A3E3D !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}
.stRadio > label {
    color: #C2255C !important;
    font-weight: 700 !important;
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
.tag-ai { background-color: #F8F0FC; color: #845EF7; border: 1px solid #E599F7; }
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
    line-height: 1.7;
    margin: 10px 0;
    white-space: pre-wrap;
    text-align: left;
    background: #FCF8F7;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #F3DFE3;
}

/* 按鈕樣式 */
.stButton>button {
    background: linear-gradient(135deg, #E08A9D 0%, #D47A8F 100%) !important;
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    border-radius: 24px !important;
    border: none !important;
    padding: 12px 20px !important;
    box-shadow: 0 6px 18px rgba(224, 138, 157, 0.35) !important;
    width: 100% !important;
    transition: transform 0.08s ease;
}
.stButton>button:active {
    transform: scale(0.96) !important;
}

/* Threads 按鈕樣式 */
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
    return text

# 4. 精選核心卡池資料庫
BASE_CARDS = [
    {
        "type": "food",
        "tag": "🍜 台南吃貨地圖",
        "title": "排隊也是一種懂吃儀式",
        "content": "『拉麵要排隊？沒關係！』\n只要湯頭夠濃郁、叉燒夠嫩，等待都是值得的。\n跟懂吃的好友邊聊天邊等位子，不知不覺就輪到我們，大口喝湯吃肉的瞬間，整天的疲勞直接歸零！",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🥩 大餐回血指南",
        "title": "把委屈全部吃回來的正確方式",
        "content": "心情煩躁、被瑣事炸到血壓升高時：\n炭佐麻里的烤肉、阿力海的海鮮大餐，就是世界上最有效的解壓靈藥！\n在美食面前，所有惱人的事通通靠邊站，盤子裝滿、肉烤下去就對了！",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🍰 甜點是另一個胃",
        "title": "下午茶是女人的專屬充電站",
        "content": "正餐吃飽了那是胃的極限，但甜點裝在另一個獨立的開心胃裡！\n不管是香濃的法式千層、焦糖烤布丁，還是巷弄老宅的現烤肉桂捲，只要真真公主想吃，好友隨時出動探店！",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🍲 台南私房牛肉湯",
        "title": "凌晨與清晨的滾燙靈魂",
        "content": "台南人的浪漫在於那一碗鮮甜粉紅的溫體牛肉湯。\n熱高湯澆下去的瞬間香氣撲鼻，配上一碗肉燥飯與薑絲醬油膏，喝一口熱湯，整個人都被溫柔撫平了。",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🧋 台南好茶日常",
        "title": "手搖飲的心情急救法",
        "content": "不管是酸甜解膩的仙楂烏龍、香濃醇厚的鮮奶茶，還是微糖微冰的療癒特調，只要今天有點悶，來一杯冰涼的好茶，就是把生活調回順遂模式的魔法棒！",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🦞 阿力海的頂級盛宴",
        "title": "海鮮自由的快樂體驗",
        "content": "現煎生蠔、焗烤龍蝦、鮮甜螃蟹還有哈根達斯吃到飽！\n坐在寬敞舒適的一樓座位，拿著滿滿一盤頂級海味，慢慢剝蝦、大口吃肉，這才是犒賞自己最棒的儀式感！",
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
        "type": "dog",
        "tag": "🐶 黃金大暖男日常",
        "title": "世界上沒有壞心眼的大狗勾",
        "content": "拖鞋被咬爛了，被抓包時：\n耳朵向後貼成海豹、眼睛瞇成一條線，一邊傻笑一邊把毛茸茸的大爪子搭在妳手上踩兩下：『別生氣嘛～拖鞋是自己裂開的，我只是幫妳檢查材質！』",
        "img": ""
    },
    {
        "type": "cat",
        "tag": "🐱 貓界霸王條款",
        "title": "可以摸，但只能摸三下",
        "content": "第一下：呼嚕呼嚕好舒服～\n第二下：本宮准你摸。\n第三下：一口咬住人類的手！\n『大膽！誰准你摸第四下的！』（咬完兩秒後又用頭蹭你的手心討肉泥）",
        "img": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=600&auto=format&fit=crop&q=80"
    },
    {
        "type": "kid",
        "tag": "🧒 當媽修煉日常",
        "title": "捏著大腿告訴自己：我生的！",
        "content": "當臭小孩把整杯水倒進包包裡、或者出門亂跑讓妳嚇得半死時：\n深呼吸、手放開、千萬別捏青了大腿！\n這不是小孩的錯，這是上天派來磨練真真公主成仙的考驗！今天先記大過，等會吃頓好料全部補回來！",
        "img": ""
    },
    {
        "type": "meme",
        "tag": "😂 脆上爆紅共鳴",
        "title": "下班後的系統重啟",
        "content": "『我下班後不是在偷懶，我是在進行碳基生物的系統格式化。』\n一進家門鞋子一脫，整個人像沒有骨頭的布丁一樣融化在沙發上一動不動，連伸手拿充電線都覺得那是極限運動！",
        "img": "https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?w=600&auto=format&fit=crop&q=80"
    },
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
    }
]

# 5. 語義工廠：動態無限生成
def generate_procedural_card(category: str):
    situations = [
        "剛忙完一整天的店務坐進沙發",
        "明明肚子餓卻完全想不出要吃哪家",
        "臭小孩又在旁邊挑戰理智線底線",
        "深夜十二點滑著脆，發現大家都在發宵夜文",
        "走進台南巷弄意外聞到超香的烘焙甜點味"
    ]
    twists = [
        "這時候如果有人端出一碗滾燙鮮嫩的溫體牛肉湯，整個人都會昇華！",
        "深吸一口氣，告訴自己：仙女是不跟凡間瑣事計較的～",
        "這世界上只有兩件事不能妥協：美食的溫度，以及真真公主的心情！",
        "拉麵要吃硬麵濃湯，生活要過得隨性自在！"
    ]
    actions = [
        "專屬好朋友隨時待命，只要公主一聲令下，探店車隊立刻出發！🚗",
        "今天所有的不愉快，就交給炭佐麻里的烤肉替妳滋滋作響全部烤散！🥩",
        "放空發呆是合法權利，今晚誰都別想打擾真真公主！✨",
        "熱量與煩惱好友全包，真真公主只管笑得美美的就好！🌸"
    ]
    return {
        "type": category if category in ["food", "dog", "cat", "kid", "meme"] else "food",
        "tag": "✨ 無限卡池・專屬生成",
        "title": "真真公主的美食與放空哲學",
        "content": f"『{random.choice(situations)}。』\n\n{random.choice(twists)}\n\n{random.choice(actions)}",
        "img": ""
    }

# 6. 頂部標題區
st.markdown("""
<div style="text-align: center; margin-bottom: 14px;">
    <div style="font-size: 2.2rem;">👑</div>
    <div style="color: #C2255C; font-size: 1.45rem; font-weight: 800; letter-spacing: 0.5px;">真真公主的解壓美食盲盒</div>
    <div style="color: #8C6D77; font-size: 0.88rem; margin-top: 4px;">萬張無限卡池！台南好店、吸貓嚕狗與爆笑解氣專區 🌸</div>
</div>
""", unsafe_allow_html=True)

# 7. AI 雙引擎調用邏輯（包含 1.5 秒超時熔斷保護）
def call_ai_api(prompt_text: str, engine: str = "gemini") -> str:
    gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    openai_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

    if "Gemini" in engine and gemini_key and genai:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(prompt_text, request_options={"timeout": 1.5})
            if resp and resp.text:
                return sanitize_text(resp.text)
        except Exception:
            pass

    if "ChatGPT" in engine and openai_key and openai:
        try:
            client = openai.OpenAI(api_key=openai_key, timeout=1.5)
            comp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=220
            )
            if comp and comp.choices:
                return sanitize_text(comp.choices[0].message.content)
        except Exception:
            pass

    # 智慧備份智庫（若 API 逾時或未設定 Key，即時毫秒回傳）
    if any(k in prompt_text for k in ["包", "水", "倒", "皮夾", "LV"]):
        return sanitize_text(
            "『這臭小孩真的是專挑貴的下手！氣得人血壓飆高！\n"
            "皮夾先拿乾布壓乾、千萬別吹熱風！大腿先放鬆～\n"
            "今晚罰小孩面壁，罰好友帶真真公主去吃炭佐麻里大口嚼肉出氣！\n"
            "包包事小，把妳氣壞才虧大，吃飽飽明天又是霸氣女老闆！』\n\n#名牌包急救 #好友全力出氣 #今晚吃肉補回來"
        )
    return sanitize_text(
        "『臭小孩又在作亂？好友開出急速退火單：罰小孩罰站，罰好友帶真真公主去吃阿力海生蠔龍蝦吃到飽！把委屈全在餐桌上討回來！』\n\n#真真專屬退火單 #把委屈吃回來"
    )

# 8. 小孩不乖．媽媽專屬發洩順毛區（保留 AI 功能並修復顯色）
with st.expander("🤬 小孩不乖？媽媽專屬發洩順毛區（點開來吐苦水）", expanded=True if "cure_result" in st.session_state else False):
    st.markdown("<p style='color: #4A3E3D; font-size: 0.9rem; margin-bottom: 6px;'>把今天臭小子/小妞幹的蠢事寫下來，讓專屬 AI 與好友全力幫妳出氣解壓！</p>", unsafe_allow_html=True)
    kid_trouble = st.text_input("今天他又做了什麼讓妳血壓飆高？", value="翻倒水在名牌包" if "cure_result" not in st.session_state else "", placeholder="例如：翻倒水在名牌包、出門亂跑找半天...")
    ai_choice = st.radio("選擇吐槽解氣風格：", ["✨ 溫柔撫平順毛 (Gemini)", "🔥 毒舌幽默同仇敵愾 (ChatGPT)"], horizontal=True)
    
    if st.button("💢 幫我狠狠吐槽＋順毛！"):
        if not kid_trouble:
            st.warning("真真公主先寫下一句他做了什麼，馬上替妳出氣！")
        else:
            style_prompt = (
                f"妳是真真公主最好的知己好友。真真公主今天因為小孩這件事氣炸了：『{kid_trouble}』。\n"
                "請站在真真公主這邊，狠狠吐槽小孩的蠢事，並用極度幽默、溫暖的語氣哄她開解，"
                "提醒她放開捏大腿的手、別氣壞身體，並提議用台南美食（例如炭佐麻里、阿力海、牛肉湯）來慰勞她。\n"
                "禁止說教、字數 120 字以內。"
            )
            st.session_state.cure_result = call_ai_api(style_prompt, engine=ai_choice)

    if "cure_result" in st.session_state:
        st.markdown(f"""
        <div class="card-box" style="border: 2px solid #E08A9D !important; background: #FFFBFB !important; margin-top: 14px;">
            <span class="card-tag tag-kid">👑 真真公主專屬退火出氣單</span>
            <div class="card-title">臭小孩退散！公主消氣～</div>
            <div class="card-content">{st.session_state.cure_result}</div>
        </div>
        """, unsafe_allow_html=True)

# 9. 盲盒分類抽卡機制（復原 AI 即時生成選項）
if "current_card" not in st.session_state:
    st.session_state.current_card = random.choice(BASE_CARDS)

theme_filter = st.radio(
    "真真公主今天想翻什麼牌子？",
    ["🎲 全都要（萬張無限抽）", "🍜 美食探店與好味", "🐶 萌犬爆笑現場", "🐱 傲嬌主子日常", "🧒 當媽修煉吐槽", "😂 爆笑生活迷因", "🤖 AI 即時無限生成"],
    horizontal=True
)

def pick_next_card():
    # 模式 1：AI 即時生成
    if "AI" in theme_filter:
        ai_prompt = (
            "請為『真真公主』寫一張短篇療癒幽默卡片。主題圍繞大台南美食探店、可愛貓狗或下班放空。"
            "口吻幽默、真誠，像懂吃的知己好友，字數約 80-100 字，附帶趣味 hashtag。"
        )
        ai_text = call_ai_api(ai_prompt, engine="Gemini")
        return {
            "type": "ai",
            "tag": "🤖 AI 即時靈魂創作",
            "title": "真真公主今日限定快樂",
            "content": ai_text,
            "img": ""
        }

    # 模式 2：分類篩選
    cat_map = {"美食": "food", "萌犬": "dog", "主子": "cat", "當媽": "kid", "迷因": "meme"}
    target_type = None
    for k, v in cat_map.items():
        if k in theme_filter:
            target_type = v
            break

    dice = random.random()
    if target_type:
        candidates = [c for c in BASE_CARDS if c["type"] in [target_type, "ssr"]]
    else:
        candidates = BASE_CARDS

    if dice > 0.4 or not candidates:
        card = generate_procedural_card(target_type or "food")
    else:
        card = random.choice(candidates)

    card["title"] = sanitize_text(card["title"])
    card["content"] = sanitize_text(card["content"])
    return card

# 抽卡按鈕
if st.button("✨ 點我開盲盒！抽取真真專屬快樂 ✨"):
    st.session_state.current_card = pick_next_card()

# 10. 開出的卡片展示
card = st.session_state.current_card
tag_class = f"tag-{card['type']}" if f"tag-{card['type']}" in ["tag-food", "tag-dog", "tag-cat", "tag-kid", "tag-meme", "tag-ai", "tag-ssr"] else "tag-food"

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
