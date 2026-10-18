import streamlit as st
import random
import time

# 1. 頁面基本配置（針對 iPhone 視窗與 LINE 瀏覽器最佳化）
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

/* 全局深可可色字體，徹底防止白色隱形 */
html, body, [class*="css"], .stApp {
    color: #4A3E3D !important;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Helvetica Neue", sans-serif;
}
.stApp {
    background: linear-gradient(180deg, #FDF9F8 0%, #F5ECE9 100%) !important;
}

/* 摺疊面板 (Expander) 標題顯色 */
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
    line-height: 1.7;
    margin: 10px 0;
    white-space: pre-wrap;
    text-align: left;
    background: #FCF8F7;
    padding: 15px;
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
    padding: 12px 20px !important;
    box-shadow: 0 6px 18px rgba(224, 138, 157, 0.35) !important;
    width: 100% !important;
    transition: transform 0.08s ease;
}
.stButton>button:active {
    transform: scale(0.96) !important;
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

# 5. 多維矩陣動態無限生成引擎（Procedural Matrix Generator：10,000+ 種梗文零延遲運算）
def generate_matrix_infinite_card(category: str = "infinite"):
    openings = [
        "剛忙完一整天的店務坐進沙發",
        "明明肚子餓卻完全想不出要吃哪家",
        "臭小孩又在旁邊挑戰理智線底線",
        "深夜十二點滑著手機，發現全台南都在發宵夜文",
        "走進台南巷弄意外聞到超濃郁的現烤甜點香",
        "下定決心今天要當個早睡的乖寶寶",
        "一開門發現家裡主子又在用看愚蠢人類的眼神盯著妳",
        "站在衣櫃前發呆了十分鐘，覺得今天又沒有衣服穿"
    ]
    twists = [
        "這時候如果能來一碗滾燙鮮嫩的溫體牛肉湯，整個人都會瞬間昇華！",
        "深吸一口氣，告訴自己：仙女是不跟凡間瑣事計較的～",
        "這世界上只有兩件事不能妥協：美食的溫度，以及真真公主的心情！",
        "拉麵要吃硬麵濃湯，生活要過得隨性自在！",
        "突然驚覺：減肥永遠是明天的事，當下的快樂才是真實的！",
        "決定立刻啟動『碳基生物系統格式化』，在沙發上融化成一灘布丁！",
        "轉念一想：世界上沒有一頓好料解決不了的煩惱，如果有，就兩頓！"
    ]
    actions = [
        "專屬好朋友隨時待命，只要公主一聲令下，探店車隊立刻出發！🚗",
        "今天所有的不愉快，就交給炭佐麻里的烤肉替妳滋滋作響全部烤散！🥩",
        "放空發呆是合法權利，今晚誰都別想打擾真真公主！✨",
        "熱量與煩惱好友全包，真真公主只管笑得美美的就好！🌸",
        "點一杯微糖微冰的仙楂烏龍，打開電視，讓全世界都圍著公主轉！🍵",
        "換上平底鞋，今晚帶妳去台南老宅吃那家只有內行人才知道的焦糖布丁！🍮"
    ]
    hashtags = [
        "#真真公主限定 #台南吃貨後盾 #懂吃好友隨時在線",
        "#放空是神聖權利 #今天不當大人 #美食治癒一切",
        "#把委屈全部吃回來 #仙女不生氣 #專屬開心能量",
        "#阿力海探店倒數 #炭佐麻里烤肉魂 #熱量好友全認領"
    ]
    titles = [
        "👑 公主的深夜食堂急救哲學",
        "🍜 台南巷弄吃貨的終極修煉",
        "🧘‍♀️ 仙女專屬的急速退火指南",
        "🐾 毛孩迷惑行為大賞",
        "🍰 甜點與胃的秘密空間",
        "🛡️ 知己好朋友的召喚術"
    ]

    o = random.choice(openings)
    t = random.choice(twists)
    a = random.choice(actions)
    h = random.choice(hashtags)
    title = random.choice(titles)

    return {
        "type": "infinite",
        "tag": "⚡ 動態無限生成・全新段子",
        "title": title,
        "content": f"『{o}。』\n\n{t}\n\n{a}\n\n{h}",
        "img": ""
    }

# 6. 頂部標題區
st.markdown("""
<div style="text-align: center; margin-bottom: 14px;">
    <div style="font-size: 2.2rem;">👑</div>
    <div style="color: #C2255C; font-size: 1.45rem; font-weight: 800; letter-spacing: 0.5px;">真真公主的解壓美食盲盒</div>
    <div style="color: #8C6D77; font-size: 0.88rem; margin-top: 4px;">萬張無限動態生成！台南好店、吸貓嚕狗與爆笑解氣專區 🌸</div>
</div>
""", unsafe_allow_html=True)

# 7. 小孩不乖．媽媽專屬發洩順毛區（急速零延遲響應版）
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

# 8. 盲盒分類抽卡機制（動態無限生成引擎＋精選母庫）
if "current_card" not in st.session_state:
    st.session_state.current_card = random.choice(BASE_CARDS)

theme_filter = st.radio(
    "真真公主今天想翻什麼牌子？",
    ["⚡ 萬張動態無限抽（永不重複）", "🍜 美食探店與好味", "🐶 萌犬爆笑現場", "🐱 傲嬌主子日常", "🧒 當媽修煉吐槽", "😂 爆笑生活迷因"],
    horizontal=True
)

def pick_next_card():
    # 模式 1：萬張動態無限抽
    if "無限" in theme_filter:
        return generate_matrix_infinite_card("infinite")

    # 模式 2：分類篩選
    cat_map = {"美食": "food", "萌犬": "dog", "主子": "cat", "當媽": "kid", "迷因": "meme"}
    target_type = None
    for k, v in cat_map.items():
        if k in theme_filter:
            target_type = v
            break

    # 40% 機率抽母庫精品，60% 機率由矩陣引擎演算全新段子
    dice = random.random()
    if target_type:
        candidates = [c for c in BASE_CARDS if c["type"] in [target_type, "ssr"]]
    else:
        candidates = BASE_CARDS

    if dice > 0.4 or not candidates:
        card = generate_matrix_infinite_card(target_type or "food")
    else:
        card = random.choice(candidates)

    card["title"] = sanitize_text(card["title"])
    card["content"] = sanitize_text(card["content"])
    return card

# 抽卡按鈕（零延遲響應架構）
if st.button("✨ 點我開盲盒！抽取真真專屬快樂 ✨"):
    st.session_state.current_card = pick_next_card()

# 9. 開出的卡片展示
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

# 10. 脆（Threads）療癒直達專區
with st.expander("🌀 還是想去脆上晃晃？點這裡直達熱門療癒話題", expanded=False):
    st.caption("為真真公主過濾掉無聊吵架，精選 Threads 上最受歡迎的美食與毛孩傳送門：")
    st.markdown('<a href="https://www.threads.net/search?q=%E5%8F%B0%E5%8D%97%E7%BE%8E%E9%A3%9F&serp_type=default" target="_blank" class="threads-btn">🍜 前往 Threads 查看最新【台南私房美食推薦】</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E5%8F%AF%E6%84%9B%E5%B0%8F%E7%8B%97&serp_type=default" target="_blank" class="threads-btn">🐶 前往 Threads 查看最新【汪星人搞笑日常】</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E8%B2%93%E5%92%AA%E5%A5%BD%E7%AC%91&serp_type=default" target="_blank" class="threads-btn">🐱 前往 Threads 查看最新【傲嬌貓貓迷惑行為】</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.threads.net/search?q=%E7%88%86%E7%AC%91%E8%BF%B7%E5%9B%A0&serp_type=default" target="_blank" class="threads-btn">😂 前往 Threads 查看最新【爆笑迷因廢文】</a>', unsafe_allow_html=True)

# 11. 專屬好友直達通道
line_direct_url = "https://line.me/ti/p/3u_xwcKRUB"

st.markdown(f"""
<div style="margin-top: 25px; margin-bottom: 25px;">
    <a href="{line_direct_url}" target="_blank" rel="noopener noreferrer" class="line-call-btn">
        💌 抽完了還是無聊或肚子餓？點此召喚專屬好友出動陪吃聊聊 🍵
    </a>
</div>
""", unsafe_allow_html=True)
