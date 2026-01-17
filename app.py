import streamlit as st

# 1. ページ設定（1回だけにまとめます。SEO用メタタグもここに含めると良いです）
st.set_page_config(
    page_title="ぷにぷに攻略Wiki | キャラクターチェッカー",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="auto",
)

# 検索エンジン向けのキーワード設定
st.markdown(
    """
    <meta name="description" content="ぷにぷにのキャラクターランクや必殺技を瞬時に検索できる攻略サイトです。">
    <meta name="keywords" content="ぷにぷに, 攻略, キャラクター, ランク, 必殺技, Wiki">
    """,
    unsafe_allow_html=True
)

# 2. 所持データの保存
if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# 3. 指定の種族カラー
TRIBE_COLORS = {
    "イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6",
    "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999",
    "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF",
}

# 4. UIデザイン（CSS）
st.markdown("""
    <style>
    [data-testid="column"] {
        flex: 1 1 45% !important;
        min-width: 45% !important;
    }

    .puni-card {
        position: relative;
        background-color: white;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        border: 2px solid #eee;
        background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
        padding: 20px;
        min-height: 180px;
    }

    .card-left {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 110px;
        margin-right: 20px;
    }

    .puni-img {
        width: 100px;
        height: 100px;
        object-fit: contain;
    }

    .visual-btn {
        width: 100%;
        margin-top: 10px;
        padding: 6px 0;
        border-radius: 6px;
        border: 2px solid #ddd;
        background: #f9f9f9;
        color: #666;
        font-size: 0.75em;
        font-weight: 900;
        text-align: center;
    }
    .visual-btn.owned {
        background: #4CAF50 !important;
        color: white !important;
        border-color: #43A047 !important;
    }
　　.detail-item { 
        background: transparent !important; /* 背景を透明にします */
        border-left: 2px solid rgba(0,0,0,0.1); /* 左の線を少し細く、馴染む色にします */
        padding: 2px 10px; 
        font-size: 0.85em; 
        font-weight: 900;
        margin-bottom: 2px;
    }

    </style>
    """, unsafe_allow_html=True)

st.title("📚 ぷにぷに最強攻略図鑑")

# 5. 検索機能の追加
search_query = st.text_input("🔍 キャラクターを検索（名前の一部でもOK）", "")

char_list = [
    {"name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し&デカぷに生成", "skill": "サイズアップ", "center": "15%UP"},
    {"name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png", "hissatsu": "高速数カ所消し", "skill": "技ゲージ貯め", "center": "15%UP"},
    {"name": "エルゼメキア", "rank": "ZZZ", "tribe": "ブキミー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420015.png", "hissatsu": "周りぷに消し", "skill": "デカぷに回復", "center": "-"},
    {"name": "輪廻", "rank": "ZZZ", "tribe": "エンマ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430001.png", "hissatsu": "全消し大ダメージ", "skill": "連結で攻撃UP", "center": "-"},
    {"name": "ガラピョン", "rank": "ZZ", "tribe": "ニョロロン", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420042.png", "hissatsu": "タップで周り消し", "skill": "デカぷに降下", "center": "-"}
]

# 検索フィルタリング
filtered_list = [c for c in char_list if search_query in c['name']]

cols = st.columns(2)
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['name'] in st.session_state.owned_set
    
    with cols[i % 2]:
        # カードの表示
        st.markdown(f"""
            <div class="puni-card" style="--tc: {color};">
                <div class="card-left">
                    <img src="{char['img']}" class="puni-img">
                    <div class="visual-btn {'owned' if is_owned else ''}">
                        {'✓ 所持済み' if is_owned else '未所持'}
                    </div>
                </div>
                <div class="info-area">
                    <span class="rank-label">{char['rank']}</span>
                    <div class="char-name">{char['name']} <span style="font-size: 0.6em; color: {color};">{char['tribe']}族</span></div>
                    <div class="detail-grid">
                        <div class="detail-item"><b>技:</b> {char['hissatsu']}</div>
                        <div class="detail-item"><b>スキル:</b> {char['skill']}</div>
                        <div class="detail-item"><b>センター:</b> {char['center']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ボタンをカードの下に配置（透明ボタンが機能しない場合の確実な方法）
        button_label = "持ってる！を切り替える" if not is_owned else "持っていないに戻す"
        if st.button(button_label, key=f"btn_{char['name']}", use_container_width=True):
            if is_owned:
                st.session_state.owned_set.remove(char['name'])
            else:
                st.session_state.owned_set.add(char['name'])
            st.rerun()　このコードの持ってる！を切り替えるボタンを消し、未所持、所持ボタンそのものを押して切れ変えられるようにしたい