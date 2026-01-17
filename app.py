import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="ぷにぷに攻略Wiki", layout="wide")

# 2. 所持データ保存
if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# 3. 種族カラー
TRIBE_COLORS = {
    "イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6",
    "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999",
    "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF",
}

# 4. キャラデータ
char_list = [
    {"name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し", "skill": "サイズアップ", "center": "15%UP"},
    {"name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png", "hissatsu": "高速消し", "skill": "技ゲージ貯め", "center": "15%UP"},
]

# 5. UIデザイン（CSS）
st.markdown("""
    <style>
    .puni-card {
        background-color: white; border-radius: 12px 12px 0 0;
        display: flex; border: 2px solid #eee; padding: 20px; min-height: 180px;
    }
    .card-left { width: 110px; margin-right: 20px; }
    .puni-img { width: 100px; height: 100px; object-fit: contain; }
    .info-area { flex: 1; }
    .char-name { font-size: 1.4em; color: #333; font-weight: 900; }
    .rank-label { background: #333; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
    
    /* ボタンの共通設定 */
    div.stButton > button {
        border-radius: 0 0 12px 12px !important;
        border: 2px solid #eee !important;
        border-top: none !important;
        font-weight: 900 !important; height: 45px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 ぷにぷに最強攻略図鑑")

# 6. 表示
cols = st.columns(2)
for i, char in enumerate(char_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['name'] in st.session_state.owned_set
    
    with cols[i % 2]:
        st.markdown(f"""
            <div class="puni-card" style="background: linear-gradient(150deg, #ffffff 65%, {color} 65.5%) !important;">
                <div class="card-left"><img src="{char['img']}" class="puni-img"></div>
                <div class="info-area">
                    <span class="rank-label">{char['rank']}</span>
                    <div class="char-name">{char['name']} <span style="font-size: 0.6em; color: {color};">{char['tribe']}族</span></div>
                    <div style="font-size: 0.8em; margin-top: 10px;">技: {char['hissatsu']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 色を強制上書きするCSS
        bg = "#f0c05a" if is_owned else "#ffffff"
        txt = "white" if is_owned else "#666"
        st.markdown(f"""<style>div:has(> button[key="btn_{char['name']}"]) button {{ background-color: {bg} !important; color: {txt} !important; }}</style>""", unsafe_allow_html=True)

        if st.button("✅ 所持済み" if is_owned else "未所持", key=f"btn_{char['name']}", use_container_width=True):
            if is_owned: st.session_state.owned_set.remove(char['name'])
            else: st.session_state.owned_set.add(char['name'])
            st.rerun()