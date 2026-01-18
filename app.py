import streamlit as st
import requests
import json

# --- 1. Firebase設定 ---
# ここにFirebaseの「Realtime Database URL」を貼り付けます
# 例: "https://your-project-id.firebaseio.com/"
FIREBASE_URL = "あなたのFirebaseデータベースURL"

# --- 2. ページ設定（UI維持） ---
st.set_page_config(page_title="ぷにぷに攻略Wiki | キャラクターチェッカー", page_icon="🔍", layout="wide")

if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# --- 3. 同期機能 (Firebase版) ---
def save_to_firebase(code):
    if len(code) != 8:
        st.warning("8文字ちょうどで入力してください")
        return
    url = f"{FIREBASE_URL}/users/{code}.json"
    data = {"owned_ids": list(st.session_state.owned_set)}
    res = requests.put(url, json=data) # PUTで上書き保存
    if res.status_code == 200:
        st.success(f"コード '{code}' で保存完了！")
    else:
        st.error("保存失敗。FirebaseのURLを確認してください。")

def load_from_firebase(code):
    if len(code) != 8:
        st.warning("8文字ちょうどで入力してください")
        return
    url = f"{FIREBASE_URL}/users/{code}.json"
    res = requests.get(url)
    if res.status_code == 200 and res.json():
        st.session_state.owned_set = set(res.json().get('owned_ids', []))
        st.success("同期完了！")
        st.rerun()
    else:
        st.error("データが見つかりません。")

# --- 4. UIデザイン（CSS） - 元のデザインを完全復元 ---
st.markdown("""
<style>
.puni-card {
    background-color: white; border-radius: 12px 12px 0 0;
    display: flex; border: 2px solid #eee;
    background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    padding: 20px; min-height: 180px;
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
    font-weight: 900 !important; height: 45px;
}
div.stButton > button[kind="primary"] {
    background-color: #f0c05a !important; color: white !important; border: none !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 ぷにぷに最強攻略図鑑")

# 同期エリア（UIを邪魔しない開閉式）
with st.expander("🔄 PC・スマホ同期（8文字コード）", expanded=True):
    c1, c2, c3 = st.columns([2,1,1])
    user_code = c1.text_input("コード入力", placeholder="ABC12345", label_visibility="collapsed")
    if c2.button("📤 保存", use_container_width=True): save_to_firebase(user_code)
    if c3.button("📥 読込", use_container_width=True): load_from_firebase(user_code)

TRIBE_COLORS = {"イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6", "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999", "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF"}

# キャラデータ（元に戻しました）
char_list = [
    {"id": "30430045", "name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し&デカぷに生成", "skill": "サイズアップ"},
    {"id": "30430046", "name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png", "hissatsu": "高速数カ所消し", "skill": "技ゲージ貯め"},
]

# 表示
search_query = st.text_input("🔍 キャラクターを検索", "")
cols = st.columns(2)
for i, char in enumerate([c for c in char_list if search_query in c['name']]):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        st.markdown(f'<div class="puni-card" style="--tc: {color};"><div class="card-left"><img src="{char["img"]}" class="puni-img"></div><div class="info-area"><span class="rank-label">{char["rank"]}</span><div class="char-name">{char["name"]}</div><div class="detail-grid"><div class="detail-item"><b>技:</b> {char["hissatsu"]}</div><div class="detail-item"><b>スキル:</b> {char["skill"]}</div></div></div></div>', unsafe_allow_html=True)
        if st.button("所持済み" if is_owned else "未所持", key=char['id'], use_container_width=True, type="primary" if is_owned else "secondary"):
            if is_owned: st.session_state.owned_set.remove(char['id'])
            else: st.session_state.owned_set.add(char['id'])
            st.rerun()