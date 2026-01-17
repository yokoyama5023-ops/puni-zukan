import streamlit as st

# 1. ページ設定
st.set_page_config(
    page_title="ぷにぷに攻略Wiki | キャラクターチェッカー",
    page_icon="🔍",
    layout="wide",
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

# 4. キャラクターデータ
char_list = [
    {"name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し&デカぷに生成", "skill": "サイズアップ", "center": "15%UP"},
    {"name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png", "hissatsu": "高速数カ所消し", "skill": "技ゲージ貯め", "center": "15%UP"},
    {"name": "エルゼメキア", "rank": "ZZZ", "tribe": "ブキミー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420015.png", "hissatsu": "周りぷに消し", "skill": "デカぷに回復", "center": "-"},
    {"name": "輪廻", "rank": "ZZZ", "tribe": "エンマ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430001.png", "hissatsu": "全消し大ダメージ", "skill": "連結で攻撃UP", "center": "-"},
    {"name": "ガラピョン", "rank": "ZZ", "tribe": "ニョロロン", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420042.png", "hissatsu": "タップで周り消し", "skill": "デカぷに降下", "center": "-"}
]

# 5. UIデザイン（CSS） - 崩れにくい柔軟な設計
st.markdown("""
    <style>
    /* カード全体の枠組み */
    .puni-card {
        background-color: white;
        border-radius: 12px 12px 0 0;
        display: flex;
        flex-direction: row; /* 横並び */
        border: 2px solid #eee;
        padding: 15px;
        gap: 15px;
        min-height: 140px; /* 高さを少し抑える */
    }
    .card-left { flex: 0 0 80px; text-align: center; }
    .puni-img { width: 80px; height: 80px; object-fit: contain; }
    .info-area { flex: 1; }
    .char-name { font-size: 1.2em; color: #333; font-weight: 900; }
    .rank-label { background: #333; color: white; padding: 1px 6px; border-radius: 4px; font-size: 0.8em; }
    
    .detail-grid { margin-top: 8px; font-size: 0.8em; line-height: 1.4; }
    
    /* ボタンの共通デザイン */
    div.stButton > button {
        border-radius: 0 0 12px 12px !important;
        border: 2px solid #eee !important;
        border-top: none !important;
        font-weight: 900 !important;
        height: 40px;
        background-color: white;
        color: #666;
        margin-bottom: 15px; /* 下に余白を作る */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 ぷにぷに攻略図鑑")

# 6. 検索
search_query = st.text_input("🔍 キャラクターを検索", "")
filtered_list = [c for c in char_list if search_query in c['name']]

# 7. 表示
cols = st.columns(2) # 2列表示
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['name'] in st.session_state.owned_set
    
    with cols[i % 2]:
        # カードHTML
        st.markdown(f"""
            <div class="puni-card" style="background: linear-gradient(150deg, #ffffff 75%, {color} 75.5%) !important;">
                <div class="card-left"><img src="{char['img']}" class="puni-img"></div>
                <div class="info-area">
                    <span class="rank-label">{char['rank']}</span>
                    <span style="font-size: 0.8em; color: {color}; font-weight: bold;">{char['tribe']}族</span>
                    <div class="char-name">{char['name']}</div>
                    <div class="detail-grid">
                        <b>技:</b> {char['hissatsu']}<br>
                        <b>スキル:</b> {char['skill']}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ボタンのラベル
        btn_label = "✅ 所持済み" if is_owned else "未所持"

        # 所持済みなら黄色くする
        if is_owned:
            st.markdown(f"""
                <style>
                div:has(> button[key="btn_{char['name']}"]) button {{
                    background-color: #f0c05a !important;
                    color: white !important;
                    border-color: #e0b04a !important;
                }}
                </style>
            """, unsafe_allow_html=True)

        if st.button(btn_label, key=f"btn_{char['name']}", use_container_width=True):
            if is_owned:
                st.session_state.owned_set.remove(char['name'])
            else:
                st.session_state.owned_set.add(char['name'])
            st.rerun()