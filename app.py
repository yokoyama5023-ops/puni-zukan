import streamlit as st
import requests

# --- Firebase設定 ---
FIREBASE_URL = "https://punipuni-charchecker-default-rtdb.firebaseio.com/"

st.set_page_config(page_title="ぷにぷに攻略Wiki", page_icon="🔍", layout="wide")

if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# --- 同期機能 ---
def save_to_firebase(code):
    if len(code) != 8: return
    url = f"{FIREBASE_URL}users/{code}.json"
    data = {"owned_ids": list(st.session_state.owned_set)}
    requests.put(url, json=data)
    st.success("保存完了")

def load_from_firebase(code):
    if len(code) != 8: return
    url = f"{FIREBASE_URL}users/{code}.json"
    res = requests.get(url)
    if res.status_code == 200 and res.json():
        st.session_state.owned_set = set(res.json().get('owned_ids', []))
        st.rerun()

# --- UIデザイン (文字間隔と行間をギュッと詰めました) ---
st.markdown("""
<style>
.puni-card {
    background-color: white; border-radius: 12px 12px 0 0;
    display: flex; border: 2px solid #eee;
    background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    padding: 12px; min-height: 140px; /* パディングを減らし、高さを抑制 */
}
.card-left { display: flex; flex-direction: column; align-items: center; width: 85px; margin-right: 15px; }
.puni-img { width: 80px; height: 80px; object-fit: contain; }
.info-area { flex: 1; }
.char-name { font-size: 1.1em; color: #333; font-weight: 900; line-height: 1.1; margin-bottom: 4px; }
.rank-label { background: #333; color: white; padding: 1px 6px; border-radius: 4px; font-size: 0.7em; }
.detail-grid { display: grid; grid-template-columns: 1fr; gap: 2px; margin-top: 8px; }

/* 💡 文字間隔と行間の調整ポイント */
.detail-item { 
    background: transparent !important; 
    border-left: 2px solid rgba(0,0,0,0.1); 
    padding: 1px 8px; 
    font-size: 0.78em; /* 文字を少し小さく */
    font-weight: 900; 
    line-height: 1.15; /* 行間を詰めました */
    letter-spacing: -0.03em; /* 文字間隔を少し狭めました */
}
div.stButton > button { border-radius: 0 0 12px 12px !important; height: 35px; font-size: 0.8em !important; }
</style>
""", unsafe_allow_html=True)

st.title("📚 ぷにぷに攻略図鑑")

# 同期エリア
with st.expander("🔄 同期"):
    c1, c2, c3 = st.columns([2,1,1])
    user_code = c1.text_input("8文字コード", label_visibility="collapsed")
    if c2.button("📤 保存"): save_to_firebase(user_code)
    if c3.button("📥 読込"): load_from_firebase(user_code)

TRIBE_COLORS = {"イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6", "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999", "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF"}

# --- キャラデータ ---
char_list = [
    {"id": "1344", "name": "うんめい", "rank": "UZ+", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/31001344.png", "hissatsu": "全消し&デカぷに技ゲージUP", "skill1": "つなげてサイズアップ", "skill2": "技ゲージ満タンでスタート", "center": "イナイレHP14%・攻6%UP", "trait": "イナズマイレブン"},
    {"id": "30430045", "name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "全消し&デカぷに生成", "skill1": "サイズアップ", "skill2": None, "center": None, "trait": None},
]

# --- 表示 ---
search_query = st.text_input("🔍 検索", "")
filtered_list = [c for c in char_list if search_query in c['name']]

cols = st.columns(2)
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        s1 = f'<div class="detail-item"><b>スキル1:</b> {char.get("skill1")}</div>' if char.get("skill1") else ""
        s2 = f'<div class="detail-item"><b>スキル2:</b> {char.get("skill2")}</div>' if char.get("skill2") else ""
        ct = f'<div class="detail-item"><b>効果:</b> {char.get("center")}</div>' if char.get("center") else ""
        tr = f'<div class="detail-item"><b>特徴:</b> {char.get("trait")}</div>' if char.get("trait") else ""
        
        st.markdown(f'''<div class="puni-card" style="--tc: {color};"><div class="card-left"><img src="{char["img"]}" class="puni-img"></div><div class="info-area"><span class="rank-label">{char["rank"]}</span><div class="char-name">{char["name"]} <span style="font-size: 0.6em; color: {color};">{char["tribe"]}族</span></div><div class="detail-grid"><div class="detail-item"><b>技:</b> {char["hissatsu"]}</div>{s1}{s2}{ct}{tr}</div></div></div>''', unsafe_allow_html=True)
        st.button("所持済み" if is_owned else "未所持", key=char['id'], use_container_width=True, type="primary" if is_owned else "secondary")