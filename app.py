import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="ぷにぷに攻略Wiki", layout="wide")

# 2. 所持データの保存
if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# 3. 種族カラー
TRIBE_COLORS = {
    "イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6",
    "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999",
    "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF",
}

# 4. 強力なCSS注入
st.markdown("""
    <style>
    /* カード全体のデザイン */
    .puni-card {
        background: white;
        border-radius: 12px;
        border: 2px solid #eee;
        padding: 15px;
        display: flex;
        margin-bottom: 10px;
        background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    }
    .card-left { width: 100px; margin-right: 15px; text-align: center; }
    .puni-img { width: 80px; height: 80px; object-fit: contain; }
    
    /* チェックボックスをボタンに見せる魔法のCSS */
    div[data-testid="stCheckbox"] {
        background-color: #ffffff;
        border: 2px solid #eee;
        border-radius: 8px;
        padding: 5px 10px;
        transition: 0.3s;
        width: 100%;
    }
    /* チェックが入った（所持済み）の時の色：落ち着いた黄色 */
    div[data-testid="stCheckbox"]:has(input:checked) {
        background-color: #f0c05a !important;
        border-color: #e0b04a !important;
    }
    div[data-testid="stCheckbox"]:has(input:checked) label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 ぷにぷに最強攻略図鑑")

char_list = [
    {"name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し", "skill": "サイズアップ"},
    {"name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png", "hissatsu": "数カ所消し", "skill": "技ゲージ貯め"},
]

# 表示
cols = st.columns(2)
for i, char in enumerate(char_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    with cols[i % 2]:
        # カード部分
        st.markdown(f"""
            <div class="puni-card" style="--tc: {color};">
                <div class="card-left"><img src="{char['img']}" class="puni-img"></div>
                <div>
                    <b style="font-size:1.2em;">{char['name']}</b> <small>{char['tribe']}族</small><br>
                    <span style="background:#333;color:white;padding:2px 5px;border-radius:4px;">{char['rank']}</span><br>
                    <small>技: {char['hissatsu']}</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # チェックボックスをボタン化
        is_owned = char['name'] in st.session_state.owned_set
        checked = st.checkbox("所持済み" if is_owned else "未所持", value=is_owned, key=f"chk_{char['name']}")
        
        # 状態更新
        if checked != is_owned:
            if checked: st.session_state.owned_set.add(char['name'])
            else: st.session_state.owned_set.remove(char['name'])
            st.rerun()