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

# 5. UIデザイン（CSS）
st.markdown("""
<style>
.puni-card {
    background-color: white;
    border-radius: 12px 12px 0 0;
    display: flex;
    border: 2px solid #eee;
    background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    padding: 20px;
    min-height: 180px;
}
.card-left { display: flex; flex-direction: column; align-items: center; width: 110px; margin-right: 20px; }
.puni-img { width: 100px; height: 100px; object-fit: contain; }
.info-area { flex: 1; }
.char-name { font-size: 1.4em; color: #333; font-weight: 900; }
.rank-label { background: #333; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
.detail-grid { display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 15px; }
.detail-item { background: transparent !important; border-left: 2px solid rgba(0,0,0,0.1); padding: 2px 10px; font-size: 0.85em; font-weight: 900; }
div.stButton > button {
    border-radius: 0 0 12px 12px !important;
    border: 2px solid #eee !important;
    border-top: none !important;
    font-weight: 900 !important;
    height: 45px;
}
div.stButton > button[kind="primary"] {
    background-color: #f0c05a !important;
    color: white !important;
    border: none !important;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #e0b04a !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 ぷにぷに最強攻略図鑑")

# 6. 検索機能
search_query = st.text_input("🔍 キャラクターを検索", "")
filtered_list = [c for c in char_list if search_query in c['name']]

# 7. キャラクター表示
cols = st.columns(2)
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['name'] in st.session_state.owned_set
    with cols[i % 2]:
        # カードのHTML
        card_html = f"""
            <div class="puni-card" style="--tc: {color};">
                <div class="card-left"><img src="{char['img']}" class="puni-img"></div>
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
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # ボタンの表示
        if is_owned:
            if st.button("所持済み", key=f"btn_{char['name']}", use_container_width=True, type="primary"):
                st.session_state.owned_set.remove(char['name'])
                st.rerun()
        else:
            if st.button("未所持", key=f"btn_{char['name']}", use_container_width=True):
                st.session_state.owned_set.add(char['name'])
                st.rerun()