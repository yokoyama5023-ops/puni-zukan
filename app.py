import streamlit as st
import requests

# --- 1. Firebase設定 ---
FIREBASE_URL = "https://punipuni-charchecker-default-rtdb.firebaseio.com/"

# --- 2. ページ設定 ---
st.set_page_config(page_title="ぷにぷに攻略Wiki", page_icon="🔍", layout="wide")

if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# --- 3. 同期機能 ---
def save_to_firebase(code):
    if len(code) != 8:
        st.warning("8文字ちょうどで入力してください")
        return
    url = f"{FIREBASE_URL}users/{code}.json"
    data = {"owned_ids": list(st.session_state.owned_set)}
    res = requests.put(url, json=data)
    if res.status_code == 200:
        st.success("保存しました")

def load_from_firebase(code):
    if len(code) != 8:
        st.warning("8文字ちょうどで入力してください")
        return
    url = f"{FIREBASE_URL}users/{code}.json"
    res = requests.get(url)
    if res.status_code == 200 and res.json():
        data = res.json()
        st.session_state.owned_set = set(data.get('owned_ids', []))
        st.rerun()

# --- 4. UIデザイン ---
st.markdown("""
<style>
.puni-card {
    background-color: white; border-radius: 12px 12px 0 0;
    display: flex; border: 2px solid #eee;
    background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    padding: 20px; min-height: 180px;
}
.card-left { display: flex; flex-direction: column; align-items: center; width: 120px; margin-right: 20px; }
.char-id { font-size: 1.4em; color: #333; font-weight: 900; margin-bottom: 5px; line-height: 1.1; }
.puni-img { width: 100px; height: 100px; object-fit: contain; }
.release-info { margin-top: 8px; font-size: 0.65em; color: #666; text-align: center; line-height: 1.2; font-weight: 700; }
.info-area { flex: 1; }
.char-name { font-size: 1.4em; color: #333; font-weight: 900; }
.rank-label { background: #333; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
.detail-grid { display: grid; grid-template-columns: 1fr; gap: 6px; margin-top: 15px; }
.detail-item { background: transparent !important; border-left: 2px solid rgba(0,0,0,0.1); padding: 2px 10px; font-size: 0.85em; font-weight: 900; line-height: 1.4; }
div.stButton > button { border-radius: 0 0 12px 12px !important; border: 2px solid #eee !important; border-top: none !important; font-weight: 900 !important; height: 45px; }
div.stButton > button[kind="primary"] { background-color: #f0c05a !important; color: white !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("ぷにぷに攻略図鑑")

with st.expander("PC・スマホ同期"):
    c1, c2, c3 = st.columns([2,1,1])
    user_code = c1.text_input("8文字コード", placeholder="PUNI2024", label_visibility="collapsed")
    if c2.button("保存", use_container_width=True): save_to_firebase(user_code)
    if c3.button("読込", use_container_width=True): load_from_firebase(user_code)

TRIBE_COLORS = {"イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6", "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999", "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF"}

# --- 5. キャラデータ（全項目あり・完全版） ---
char_list = [
    {
        "id": "1344", 
        "name": "うんめい", 
        "rank": "UZ+", 
        "tribe": "イサマシ", 
        "img": "https://rsc.yokai-punipuni.jp/images/chara/body/31001344.png", 
        "hissatsu": "全消し&デカぷに技ゲージUP", 
        "skill1": "つなげてサイズアップ", 
        "skill2": "技ゲージ満タンでスタート",
        "center": "イナイレHP14%・攻6%UP",
        "trait": "イナズマイレブン",
        "release_date": "2024/01/17",
        "event_name": "イナズマイレブンコラボ第3弾"
    },
    {
        "id": "4480", 
        "name": "大血戦スターエルゼメキア", 
        "rank": "UZ", 
        "tribe": "プリチー", 
        "img": "https://rsc.yokai-punipuni.jp/images/chara/body/33004168.png", 
        "hissatsu": "ぷに全消し(自分が消えるほど強力)", 
        "skill1": "自身の妖怪ぷにを出しやすくする", 
        "skill2": "フィーバーインで技ゲージがたまる",
        "center": "",
        "trait": "妖怪学園Y",
        "release_date": "",
        "event_name": ""
    },
]

# --- 6. 表示ロジック（空欄ガード付き） ---
search_query = st.text_input("キャラクターを検索", "")
filtered_list = [c for c in char_list if search_query in c['name']]

cols = st.columns(2)
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        # 各項目が空文字 "" じゃない時だけ HTML を作る仕組み
        s1 = f'<div class="detail-item"><b>スキル1:</b> {char["skill1"]}</div>' if char.get("skill1") else ""
        s2 = f'<div class="detail-item"><b>スキル2:</b> {char["skill2"]}</div>' if char.get("skill2") else ""
        ct = f'<div class="detail-item"><b>効果:</b> {char["center"]}</div>' if char.get("center") else ""
        tr = f'<div class="detail-item"><b>特徴:</b> {char["trait"]}</div>' if char.get("trait") else ""
        
        # 日付とイベント名、どちらかがあれば表示
        rel_h = ""
        if char.get("release_date") or char.get("event_name"):
            rel_h = f'<div class="release-info">{char.get("release_date", "")}<br>{char.get("event_name", "")}</div>'
        
        st.markdown(f'''
            <div class="puni-card" style="--tc: {color};">
                <div class="card-left">
                    <div class="char-id">{char["id"]}</div>
                    <img src="{char["img"]}" class="puni-img">
                    {rel_h}
                </div>
                <div class="info-area">
                    <span class="rank-label">{char["rank"]}</span>
                    <div class="char-name">{char["name"]} <span style="font-size: 0.6em; color: {color};">{char["tribe"]}族</span></div>
                    <div class="detail-grid">
                        <div class="detail-item"><b>技:</b> {char["hissatsu"]}</div>
                        {s1}{s2}{ct}{tr}
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("所持済み" if is_owned else "未所持", key=char['id'], use_container_width=True, type="primary" if is_owned else "secondary"):
            if is_owned: st.session_state.owned_set.remove(char['id'])
            else: st.session_state.owned_set.add(char['id'])
            st.rerun()