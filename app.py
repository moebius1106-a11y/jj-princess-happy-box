import streamlit as st
import random
import time
import os
import re

# 嘗試載入 AI 套件（若環境未設定 Key，會自動無縫切換至豐富預設庫，絕不報錯）
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# 1. 頁面基本配置（針對 iPhone 視窗與 LINE 瀏覽器最佳化）
st.set_page_config(
    page_title="👑 真真公主的解壓美食盲盒",
    page_icon="👑",
    layout="centered"
)

# 2. 真楨美學專屬配色加固 CSS（優雅莫蘭迪玫瑰粉、香檳裸杏、大地可可棕）
st.markdown("""
<style>
:root {
    color-scheme: light !important;
    -webkit-color-scheme: light !important;
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

body {
    -webkit-font-smoothing: antialiased;
    -webkit-tap-highlight-color: transparent !important;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Helvetica Neue", sans-serif;
    color: #4A3E3D !important;
    background-color: #FAF6F3 !important;
}
.stApp {
    background: linear-gradient(180deg, #FDF9F8 0%, #F5ECE9 100%) !important;
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

/* 抽卡與操作按鈕 */
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
    touch-action: manipulation;
    transition: transform 0.08s ease;
}
.stButton>button:active {
    transform: scale(0.96) !important;
}

div[role="radiogroup"] label {
    color: #4A3E3D !important;
    font-size: 0.9rem !important;
}

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
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    font-size: 0.92rem;
    touch-action: manipulation;
}
.threads-btn:active {
    opacity: 0.85;
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
    text-decoration: none;
    font-size: 0.98rem;
    box-shadow: 0 6px 20px rgba(194, 37, 92, 0.3);
    touch-action: manipulation;
    transition: transform 0.08s ease, opacity 0.08s ease;
}
.line-call-btn:active {
    transform: scale(0.97);
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# 3. 專屬安全淨化器（自動攔截並替換任何非真真或越界稱謂）
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

# 4. 精選核心卡池資料庫（海量基底）
BASE_CARDS = [
    # ─── 🍜 大台南私房吃貨與甜點地圖 ───
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
        "tag": "🍤 巷弄炸物解壓法",
        "title": "宵夜的酥脆治癒力",
        "content": "夜深人靜店裡收工後，來一份剛起鍋的香酥雞、魷魚圈配九層塔！\n咬下去卡滋卡滋的聲音，就是所有煩惱被嚼碎的聲音。熱量什麼的明天再說，今晚真真公主開心最重要！",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🍮 老宅老靈魂甜點",
        "title": "躲進台南小巷吃布丁",
        "content": "找一家藏在台南神農街或永康巷弄裡的靜謐老宅咖啡，點一杯手沖咖啡配上苦甜適中的焦糖布丁。\n靠在木椅上放空看窗外，沒有繁瑣的雜事，只有專屬於妳的安靜與甜美。",
        "img": ""
    },
    {
        "type": "food",
        "tag": "🦞 阿力海的頂級盛宴",
        "title": "海鮮自由的快樂體驗",
        "content": "現煎生蠔、焗烤龍蝦、鮮甜螃蟹還有哈根達斯吃到飽！\n坐在寬敞舒適的一樓座位，拿著滿滿一盤頂級海味，慢慢剝蝦、大口吃肉，這才是犒賞自己最棒的儀式感！",
        "img": ""
    },

    # ─── 🐶 汪星人爆笑日常 ───
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
        "type": "dog",
        "tag": "🐶 柯基短腿大隊",
        "title": "樓梯是柯基永遠的痛",
        "content": "遇到三階以上的樓梯：\n大腦：『衝啊！』\n小短腿：『撲騰撲騰（懸空抓空氣）』。\n最後屁屁像顆烤吐司一扭一扭地等著人類連狗帶屁股提上去～",
        "img": ""
    },
    {
        "type": "dog",
        "tag": "🐶 二哈拆遷辦",
        "title": "哈士奇的獨特腦迴路",
        "content": "別的狗狗做錯事會心虛低頭。\n哈士奇做錯事會直接站在沙發殘骸上對妳仰天長嘯：『嗷嗚嗚嗚！是沙發先動手的！妳為什麼要怪一隻無辜的狼！』讓妳氣到笑出腹肌！",
        "img": ""
    },
    {
        "type": "dog",
        "tag": "🐶 狗狗美食雷達",
        "title": "廚房撕開包裝紙的瞬間",
        "content": "在房間撕開零食包裝的聲音大概只有 5 分貝。\n但在隔壁睡得像小豬的狗勾，能在 0.01 秒內飄移進廚房，坐在妳面前眼神發光：『見者有份，這是這家裡的規矩！』",
        "img": ""
    },
    {
        "type": "dog",
        "tag": "🐶 臘腸短腿哲學",
        "title": "被窩裡的探頭熱狗",
        "content": "天冷時的臘腸：\n整條鑽進被窩只露出一顆黑鼻頭呼吸。\n你想拉開被子？牠會用整條長身軀死死夾住床墊，喉嚨發出呼嚕警告：『誰都別想叫本熱狗起床！』",
        "img": "https://images.unsplash.com/photo-1597633425046-08f5110420b5?w=600&auto=format&fit=crop&q=80"
    },

    # ─── 🐱 傲嬌主子迷惑行為 ───
    {
        "type": "cat",
        "tag": "🐱 貓咪物理學",
        "title": "豪華貓窩 vs 破紙箱",
        "content": "人類花了上千元買了豪華羊毛保暖貓窩 ❌\n快遞送來的沾滿灰塵破紙箱 ⭕\n貓咪：『愚蠢的人類，別用你俗氣的審美來衡量我尊貴的紙箱城堡。』",
        "img": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80"
    },
    {
        "type": "cat",
        "tag": "🐱 貓界霸王條款",
        "title": "可以摸，但只能摸三下",
        "content": "第一下：呼嚕呼嚕好舒服～\n第二下：本宮准你摸。\n第三下：一口咬住人類的手！\n『大膽！誰准你摸第四下的！』（咬完兩秒後又用頭蹭你的手心討肉泥）",
        "img": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=600&auto=format&fit=crop&q=80"
    },
    {
        "type": "cat",
        "tag": "🐱 半夜迷惑跑酷",
        "title": "凌晨三點的貓咪奧運會",
        "content": "白天：睡得像一灘融化在地上的死水，怎麼戳都沒反應。\n凌晨 3:15：突然在大腦連線到外星信號，從客廳直線衝刺飛上衣櫃，再踩著人類的肚子起跳！『起床看我奔馳，人類！』",
        "img": ""
    },
    {
        "type": "cat",
        "tag": "🐱 橘貓大食怪",
        "title": "十隻橘貓九隻胖",
        "content": "還有一隻正在壓垮磅秤的路上！\n碗裡明明還有半碗飼料，橘貓依然坐在碗旁對妳發出悲慘的叫聲，彷彿牠已經三天三夜沒吃過一口飯一樣！",
        "img": ""
    },
    {
        "type": "cat",
        "tag": "🐱 賓士貓的精神狀態",
        "title": "貓界的極限運動員",
        "content": "賓士貓從來不好好走路。\n牠們的人生信條就是：『能用牆壁借力反彈，就絕不用四腳著地。』看牠在客廳瘋狂彈跳，莫名其妙就能治好妳一整天的心情不好！",
        "img": ""
    },

    # ─── 🧒 小孩不乖．當媽修煉吐槽 ───
    {
        "type": "kid",
        "tag": "🧒 當媽修煉日常",
        "title": "捏著大腿告訴自己：我生的！",
        "content": "當臭小孩把整杯水倒進包包裡、或者出門亂跑讓妳嚇得半死時：\n深呼吸、手放開、千萬別捏青了大腿！\n這不是小孩的錯，這是上天派來磨練真真公主成仙的考驗！今天先記大過，等會吃頓好料全部補回來！",
        "img": ""
    },
    {
        "type": "kid",
        "tag": "🧒 帶娃哲學",
        "title": "只要還在呼吸就是好媽媽",
        "content": "今天沒耐心？沒關係！\n今天想發脾氣？很正常！\n當媽已經是用盡洪荒之力了，偶爾當個只想躺平吃甜點的任性仙女，全世界都會站在妳這邊！",
        "img": ""
    },
    {
        "type": "kid",
        "tag": "🧒 寫作業地獄",
        "title": "不寫作業母慈子孝",
        "content": "一寫作業雞飛狗跳！\n『媽媽這題怎麼寫？』『我剛剛不是講了三次了嗎？』\n這時候別急著爆血管，轉身去泡杯熱茶，告訴自己：成績如浮雲，親情最重要，放過小孩也放過自己！",
        "img": ""
    },

    # ─── 😂 爆笑脆文與生活迷因 ───
    {
        "type": "meme",
        "tag": "😂 脆上爆紅共鳴",
        "title": "下班後的系統重啟",
        "content": "『我下班後不是在偷懶，我是在進行碳基生物的系統格式化。』\n一進家門鞋子一脫，整個人像沒有骨頭的布丁一樣融化在沙發上一動不動，連伸手拿充電線都覺得那是極限運動！",
        "img": "https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?w=600&auto=format&fit=crop&q=80"
    },
    {
        "type": "meme",
        "tag": "😂 吃貨人生哲學",
        "title": "遇到煩惱的標準SOP",
        "content": "步驟一：先深呼吸，告訴自己都是小事。\n步驟二：打開手機發送美食清單給知己好友。\n步驟三：『走！這家看起來超讚，今晚吃爆它！』\n結論：世界上沒有一頓好料解決不了的煩惱，如果有，就兩頓！",
        "img": ""
    },

    # ─── 👑 真真公主專屬特權好友卡（SSR 系列） ───
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
        "type": "ssr",
        "tag": "👑 專屬特權・SSR 稀有卡",
        "title": "💻 網站與技術疑難雜症免死卡",
        "content": "恭喜真真公主抽到技術支援 SSR！\n【兌換權利】：\n店裡網站、程式碼、宣傳排版遇到任何問號？免煩惱，一鍵召喚專屬工程師好友全包搞定，真真公主只管美美地經營！✨",
        "img": ""
    },
    {
        "type": "ssr",
        "tag": "👑 專屬特權・SSR 稀有卡",
        "title": "🍗 深夜熱量無罪代吸卡",
        "content": "恭喜真真公主抽到深夜放縱 SSR！\n【兌換權利】：\n今晚就是想吃炸雞、想吃麻辣鍋？出示此卡，好友陪妳放肆吃，所有發胖脂肪由好友全額認領，公主只負責吸收快樂！🎉",
        "img": ""
    }
]

# 5. 語義工廠：隨機生成萬種不重複原創卡片（無限卡池核心引擎）
def generate_procedural_card(category: str):
    situations = [
        "剛忙完一整天的店務坐進沙發",
        "明明肚子餓卻完全想不出要吃哪家",
        "臭小孩又在旁邊挑戰理智線底線",
        "深夜十二點滑著脆，發現大家都在發宵夜文",
        "下定決心要早睡，結果靈魂突然神清氣爽",
        "走進台南巷弄意外聞到超香的烘焙甜點味"
    ]
    twists = [
        "這時候如果有人端出一碗滾燙鮮嫩的溫體牛肉湯，整個人都會昇華！",
        "深吸一口氣，告訴自己：仙女是不跟凡間瑣事計較的～",
        "這世界上只有兩件事不能妥協：美食的溫度，以及真真公主的心情！",
        "拉麵要吃硬麵濃湯，生活要過得隨性自在！",
        "管它明天幾點起，先把想喝的手搖飲點起來！"
    ]
    actions = [
        "專屬好朋友隨時待命，只要公主一聲令下，探店車隊立刻出發！🚗",
        "今天所有的不愉快，就交給炭佐麻里的烤肉替妳滋滋作響全部烤散！🥩",
        "放空發呆是合法權利，今晚誰都別想打擾真真公主！✨",
        "熱量與煩惱好友全包，真真公主只管笑得美美的就好！🌸"
    ]
    
    s = random.choice(situations)
    t = random.choice(twists)
    a = random.choice(actions)
    
    title_pool = ["公主的深夜食堂哲學", "台南吃貨的終極修煉", "專屬放空急救配方", "仙女的退火指南", "懂吃知己的召喚術"]
    
    return {
        "type": category if category in ["food", "dog", "cat", "kid", "meme"] else "food",
        "tag": "✨ 無限卡池・專屬生成",
        "title": random.choice(title_pool),
        "content": f"『{s}。』\n\n{t}\n\n{a}",
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

# 7. AI 調用邏輯（ChatGPT 與 Gemini 雙引擎）
def get_ai_response(prompt_text, engine="gemini"):
    gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    openai_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    
    if engine == "gemini" and gemini_key and genai:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt_text)
            return sanitize_text(response.text)
        except Exception:
            pass

    if engine == "openai" and openai_key and openai:
        try:
            client = openai.OpenAI(api_key=openai_key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=400
            )
            return sanitize_text(completion.choices[0].message.content)
        except Exception:
            pass

    fallback_pool = [
        "『今天臭小孩惹真真公主生氣？來，好友替妳開出診斷單：罰小孩面壁五分鐘，罰好友帶真真公主去吃炭佐麻里大口嚼肉！大口咬下去那一秒，世界又恢復美麗了！』\n\n#真真專屬順毛 #把委屈吃回來",
        "『不管是把水倒進包包還是出門亂跑，記住八字箴言：自己生的，大腿放鬆！今晚就當一灘無憂無慮的爛泥巴，吃飽飽好好睡，明天又是一條好漢！』\n\n#媽媽不生氣保命符 #好友全力支持",
        "『拉麵湯頭要濃，生活步調要鬆。今天什麼家務跟工作都別管，點一杯微糖微冰的仙楂烏龍，打開電視放空，讓全世界都圍著真真公主轉！』\n\n#放空是合法權利 #美食解千愁"
    ]
    return sanitize_text(random.choice(fallback_pool))

# 8. 小孩不乖．媽媽專屬發洩順毛區（Expander 功能模組）
with st.expander("🤬 小孩不乖？媽媽專屬發洩順毛區（點開來吐苦水）", expanded=False):
    st.caption("把今天臭小子/小妞幹的蠢事寫下來，讓專屬 AI 與好友全力幫妳出氣解壓！")
    kid_trouble = st.text_input("今天他又做了什麼讓妳血壓飆高？", placeholder="例如：把整罐水翻倒在包包裡、出門亂跑找半天...")
    ai_choice = st.radio("選擇吐槽解氣風格：", ["✨ 溫柔撫平順毛 (Gemini)", "🔥 毒舌幽默同仇敵愾 (ChatGPT)"], horizontal=True)
    
    if st.button("💢 幫我狠狠吐槽＋順毛！"):
        if not kid_trouble:
            st.warning("真真公主先寫下一句他做了什麼，馬上替妳出氣！")
        else:
            with st.spinner("好友與 AI 正在為真真公主調製退火靈藥...🍵"):
                style_prompt = (
                    f"妳是真真公主最好的知己好友與後盾。真真公主今天因為小孩的這件事氣炸了：『{kid_trouble}』。\n"
                    "請站在真真公主這邊，狠狠吐槽小孩的蠢事，並用極度幽默、溫暖、接地氣的語氣哄她開解，"
                    "提醒她放開捏大腿的手、別氣壞身體，並提議用台南美食（例如炭佐麻里、甜點、拉麵或牛肉湯）來慰勞她。\n"
                    "禁止使用任何說教、不要叫她多體諒小孩，只准寵溺和站在她這邊！字數在 150 字以內。"
                )
                engine_type = "openai" if "ChatGPT" in ai_choice else "gemini"
                vent_result = get_ai_response(style_prompt, engine=engine_type)
                
                st.markdown(f"""
                <div class="card-box" style="border: 2px solid #E08A9D !important; background: #FFFBFB !important;">
                    <span class="card-tag tag-kid">👑 真真公主專屬退火出氣單</span>
                    <div class="card-title">臭小孩退散！公主消氣～</div>
                    <div class="card-content">{vent_result}</div>
                </div>
                """, unsafe_allow_html=True)

# 9. 盲盒分類抽卡機制（動態結合：核心精選 ＋ 語義工廠 ＋ 即時 AI）
if "drawn_history" not in st.session_state:
    st.session_state.drawn_history = []

if "current_card" not in st.session_state:
    st.session_state.current_card = random.choice(BASE_CARDS)

theme_filter = st.radio(
    "真真公主今天想翻什麼牌子？",
    ["🎲 全都要（萬張無限抽）", "🍜 美食探店與好味", "🐶 萌犬爆笑現場", "🐱 傲嬌主子日常", "🧒 當媽修煉吐槽", "😂 爆笑生活迷因", "🤖 AI 即時無限生成"],
    horizontal=True
)

def pick_next_card():
    # 模式 1：AI 即時無限生成
    if "AI" in theme_filter:
        prompt = (
            "請為『真真公主』寫一張短篇療癒幽默卡片。主題可圍繞大台南美食探店、可愛貓狗迷惑行為、當媽崩潰吐槽或下班放空。"
            "口吻要幽默、真誠、像極度懂吃的知己好友，字數約 80-120 字，排版加上趣味 hashtag。"
        )
        content = get_ai_response(prompt, engine="gemini")
        return {
            "type": "ai",
            "tag": "🤖 AI 即時靈魂創作",
            "title": "真真公主今日限定快樂",
            "content": content,
            "img": ""
        }

    # 模式 2：分類篩選
    cat_map = {
        "美食": "food",
        "萌犬": "dog",
        "主子": "cat",
        "當媽": "kid",
        "迷因": "meme"
    }
    target_type = None
    for k, v in cat_map.items():
        if k in theme_filter:
            target_type = v
            break

    # 50% 機率抽母庫精品，50% 機率由語義工廠全新演算組合（確保真正玩不完）
    dice = random.random()
    if target_type:
        candidates = [c for c in BASE_CARDS if c["type"] in [target_type, "ssr"]]
    else:
        candidates = BASE_CARDS

    if dice > 0.45 or not candidates:
        card = generate_procedural_card(target_type or "food")
    else:
        card = random.choice(candidates)

    # 雙重安全淨化
    card["title"] = sanitize_text(card["title"])
    card["content"] = sanitize_text(card["content"])
    return card

# 抽卡按鈕
if st.button("✨ 點我開盲盒！抽取真真專屬快樂 ✨"):
    with st.spinner("正在從萬張星空中為真真公主捕捉快樂能量...🐾"):
        time.sleep(0.12)
        st.session_state.current_card = pick_next_card()
    st.rerun()

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

# 12. 專屬好友直達通道（雙協議加固版：支援原生 LINE 喚醒）
line_official_url = "https://line.me/R/ti/p/~3u_xwcKRUB"

st.markdown(f"""
<div style="margin-top: 25px; margin-bottom: 25px;">
    <a href="{line_official_url}" target="_blank" rel="noopener noreferrer" class="line-call-btn">
        💌 抽完了還是無聊或肚子餓？點此召喚專屬好友出動陪吃聊聊 🍵
    </a>
</div>
""", unsafe_allow_html=True)
