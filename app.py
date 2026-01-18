import streamlit as st
import requests

# --- 設定 ---
API_KEY = "$2a$10$3UVxy8N1SsumxzLDKnBXbOtj8/Z22KvizDX2YOpahQIqy2JN9ORye"

st.set_page_config(page_title="ぷにぷに同期図鑑", layout="wide")

if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# --- 同期ロジック（完全版） ---
def get_bin_id_by_name(name):
    """8文字の名前から、ネット上の住所(Bin ID)を探し出す"""
    url = "https://api.jsonbin.io/v3/b/list"
    headers = {"X-Master-Key": API_KEY}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        for b in res.json():
            if b.get('snippetMeta', {}).get('name') == name:
                return b['record']
    return None

def save_data(code):
    if len(code) != 8:
        st.warning("8文字ちょうどで入力してください")
        return
    
    data = {"owned_ids": list(st.session_state.owned_set)}
    existing_id = get_bin_id_by_name(code)
    
    if existing_id:
        # 上書き保存
        url = f"https://api.jsonbin.io/v3/b/{existing_id}"
        headers = {"Content-Type": "application/json", "X-Master-Key": API_KEY}
        res = requests.put(url, json=data, headers=headers)
    else:
        # 新規保存
        url = "https://api.jsonbin.io/v3/b"
        headers = {"Content-Type": "application/json", "X-Master-Key": API_KEY, "X-Bin-Name": code}
        res = requests.post(url, json=data, headers=headers)
        
    if res.status_code == 200:
        st.success(f"コード '{code}' に保存しました！")
    else:
        st.error("保存失敗。設定を確認してください。")

def load_data(code):
    if len(code) != 8:
        st.warning("8文字ちょうどで入力してください")
        return
        
    bin_id = get_bin_id_by_name(code)
    if not bin_id:
        st.error("データが見つかりません。先に保存してください。")
        return

    url = f"https://api.jsonbin.io/v3/b/{bin_id}"
    headers = {"X-Master-Key": API_KEY}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        st.session_state.owned_set = set(res.json()['record']['owned_ids'])
        st.success("同期しました！")
        st.rerun()

# --- 見た目（これまでのUIを維持） ---
st.markdown("""
<style>
.puni-card { background: white; border-radius: 12px 12px 0 0; border: 2px solid #eee; padding: 20px; min-height: 180px; display: flex; }
.puni-img { width: 100px; height: 100px; object-fit: contain; }
.char-name { font-size: 1.4em; font-weight: 900; }
div.stButton > button { border-radius: 0 0 12px 12px !important; font-weight: 900 !important; height: 45px; }
div.stButton > button[kind="primary"] { background-color: #f0c05a !important; color: white !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("📚 ぷにぷに同期図鑑")

# 同期エリア
with st.expander("🔄 同期設定", expanded=True):
    c1, c2, c3 = st.columns([2,1,1])
    code = c1.text_input("8文字のコード", placeholder="ABC12345", label_visibility="collapsed")
    if c2.button("📤 保存", use_container_width=True): save_data(code)
    if c3.button("📥 読込", use_container_width=True): load_data(code)

# キャラデータ
char_list = [
    {"id": "30430045", "name": "伏李ユウ", "rank": "UZ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png"},
    {"id": "30430046", "name": "闇ケン王", "rank": "UZ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png"}
]

# 表示
cols = st.columns(2)
for i, char in enumerate(char_list):
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        st.markdown(f'<div class="puni-card"><div><img src="{char["img"]}" class="puni-img"></div><div><div class="char-name">{char["name"]}</div></div></div>', unsafe_allow_html=True)
        if st.button("所持済み" if is_owned else "未所持", key=char['id'], use_container_width=True, type="primary" if is_owned else "secondary"):
            if is_owned: st.session_state.owned_set.remove(char['id'])
            else: st.session_state.owned_set.add(char['id'])
            st.rerun()