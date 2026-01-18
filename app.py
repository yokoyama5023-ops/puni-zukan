import streamlit as st
import requests

# --- Firebase設定 ---
FIREBASE_URL = "https://punipuni-charchecker-default-rtdb.firebaseio.com/"

st.set_page_config(page_title="ぷにぷに攻略Wiki | キャラチェッカー", page_icon="🔍", layout="wide")

if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

def save_to_firebase(code):
    if len(code) != 8: return
    url = f"{FIREBASE_URL}users/{code}.json"
    res = requests.put(url, json={"owned_ids": list(st.session_state.owned_set)})
    if res.status_code == 200: st.success(f"保存完了: {code}")

def load_from_firebase(code):
    if len(code) != 8: return
    url = f"{FIREBASE_URL}users/{code}.json"
    res = requests.get(url)
    if res.status_code == 200 and res.json():
        st.session_state.owned_set = set(res.json().get('owned_ids', []))
        st.rerun()

# CSS（センター効果用のスタイルを追加）
st.markdown("""
<style>
.puni-card {
    background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    border: 2px solid #eee; border-radius: 12px 12px 0 0; padding: 15px; min-height: 200px; display: flex;
}
.card-left { width: 100px; text-align: center; margin-right: 15px; }
.puni-img { width: 90px; height: 90px; object-fit: contain; }
.char-name { font-size: 1.2em; font-weight: 900; color: #333; }
.rank-label { background: #333; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
.detail-item { border-left: 3px solid var(--tc); padding-left: 8px; margin-top: 5px; font-size: 0.8em; font-weight: bold; }
.center-effect { background: #fff3cd; padding: 4px; border-radius: 4px; font-size: 0.75em; margin-top: 5px; border: 1px dashed #ffa000; }
</style>
""", unsafe_allow_html=True)

st.title("📚 ぷにぷに最強攻略図鑑")

# 同期機能
with st.expander("🔄 PC・スマホ同期"):
    c1, c2, c3 = st.columns([2,1,1])
    code = c1.text_input("8文字コード", max_chars=8)
    if c2.button("📤 保存"): save_to_firebase(code)
    if c3.button("📥 読込"): load_from_firebase(code)

TRIBE_COLORS = {"イサマシ": "#FFB3BA", "プリチー": "#FFB3E6", "ブキミー": "#D1BBFF"}

# スクショから読み取った最新データを含むリスト
char_list = [
    {
        "id": "1344", 
        "name": "うんめい", 
        "rank": "UZ+", 
        "tribe": "イサマシ", 
        "img": "https://rsc.yokai-punipuni.jp/images/chara/body/31001344.png", 
        "hissatsu": "天空のタクト", 
        "skill": "サイズアップ / 技ゲージ満タン開始",
        "center": "イナイレキャラのHP14%・攻撃6%UP"
    },
    {"id": "30430045", "name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し&デカぷに生成", "skill": "サイズアップ", "center": None},
]

cols = st.columns(2)
for i, char in enumerate(char_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        center_html = f'<div class="center-effect"><b>⭐センター:</b> {char["center"]}</div>' if char["center"] else ""
        st.markdown(f'''
        <div class="puni-card" style="--tc: {color};">
            <div class="card-left"><img src="{char["img"]}" class="puni-img"></div>
            <div class="info-area">
                <span class="rank-label">{char["rank"]}</span>
                <div class="char-name">{char["name"]}</div>
                <div class="detail-item"><b>技:</b> {char["hissatsu"]}</div>
                <div class="detail-item"><b>スキル:</b> {char["skill"]}</div>
                {center_html}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("所持済み" if is_owned else "未所持", key=char['id'], use_container_width=True, type="primary" if is_owned else "secondary"):
            if is_owned: st.session_state.owned_set.remove(char['id'])
            else: st.session_state.owned_set.add(char['id'])
            st.rerun()