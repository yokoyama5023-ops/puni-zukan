import streamlit as st
import requests
import json

# --- 1. データベース設定 ---
API_KEY = "$2a$10$3UVxy8N1SsumxzLDKnBXbOtj8/Z22KvizDX2YOpahQIqy2JN9ORye"
BIN_ID = "678b7764e41b4d34e47a1924" # データの置き場所ID（自動で作成されます）

# --- 2. ページ設定 ---
st.set_page_config(page_title="ぷにぷに同期図鑑", layout="wide")

if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# --- 3. 同期機能（保存と読み込み） ---
def save_data(code):
    if len(code) < 4:
        st.error("セーブコードは4文字以上にしてください")
        return
    url = f"https://api.jsonbin.io/v3/b"
    headers = {"Content-Type": "application/json", "X-Master-Key": API_KEY, "X-Bin-Name": code}
    data = {"owned_ids": list(st.session_state.owned_set)}
    
    with st.spinner('保存中...'):
        # 実際には既存のBinを探して更新する処理が必要ですが、
        # 今回はシンプルに「新しいデータを送る」仕組みとして構成しています。
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            st.success(f"コード '{code}' で保存しました！")
        else:
            st.error("保存に失敗しました。キーを確認してください。")

def load_data(code):
    # 特定のコード(Bin Name)で検索して読み込む
    url = "https://api.jsonbin.io/v3/b/678b7764e41b4d34e47a1924" # 固定ID（簡易版）
    headers = {"X-Master-Key": API_KEY}
    
    with st.spinner('読み込み中...'):
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            st.session_state.owned_set = set(res.json()['record']['owned_ids'])
            st.success("読み込み完了！")
            st.rerun()
        else:
            st.error("データが見つかりませんでした。")

# --- 4. UIデザイン（CSS） ---
st.markdown("""
<style>
.puni-card {
    background-color: white; border-radius: 12px 12px 0 0;
    display: flex; border: 2px solid #eee;
    background: linear-gradient(150deg, #ffffff 65%, var(--tc, #f0f0f0) 65.5%) !important;
    padding: 20px; min-height: 180px;
}
.card-left { width: 110px; margin-right: 20px; }
.puni-img { width: 100px; height: 100px; object-fit: contain; }
.char-name { font-size: 1.4em; color: #333; font-weight: 900; }
.rank-label { background: #333; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
div.stButton > button { border-radius: 0 0 12px 12px !important; font-weight: 900 !important; height: 45px; }
div.stButton > button[kind="primary"] { background-color: #f0c05a !important; color: white !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("📚 ぷにぷに同期図鑑")

# --- 5. 同期エリア ---
st.subheader("🔄 データの同期（PC・スマホ共通）")
col_code, col_btn_s, col_btn_l = st.columns([2, 1, 1])
with col_code:
    save_code = st.text_input("英数8文字のセーブコードを入力", placeholder="例: PUNI2026", max_chars=20)
with col_btn_s:
    if st.button("📤 ネットに保存", use_container_width=True):
        save_data(save_code)
with col_btn_l:
    if st.button("📥 データを読込", use_container_width=True):
        load_data(save_code)

st.divider()

# --- 6. 検索と表示 ---
char_list = [
    {"id": "30430045", "name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png"},
    {"id": "30430046", "name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png"},
    {"id": "30420015", "name": "エルゼメキア", "rank": "ZZZ", "tribe": "ブキミー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420015.png"},
    {"id": "30430001", "name": "輪廻", "rank": "ZZZ", "tribe": "エンマ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430001.png"},
    {"id": "30420042", "name": "ガラピョン", "rank": "ZZ", "tribe": "ニョロロン", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420042.png"}
]

TRIBE_COLORS = {"イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6", "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999", "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF"}

search_query = st.text_input("🔍 キャラクターを検索", "")
filtered_list = [c for c in char_list if search_query in c['name']]

cols = st.columns(2)
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char.get('tribe',''), "#ccc")
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        st.markdown(f'<div class="puni-card" style="--tc: {color};"><div class="card-left"><img src="{char["img"]}" class="puni-img"></div><div class="info-area"><span class="rank-label">{char["rank"]}</span><div class="char-name">{char["name"]}</div></div></div>', unsafe_allow_html=True)
        if is_owned:
            if st.button("所持済み", key=f"btn_{char['id']}", use_container_width=True, type="primary"):
                st.session_state.owned_set.remove(char['id'])
                st.rerun()
        else:
            if st.button("未所持", key=f"btn_{char['id']}", use_container_width=True):
                st.session_state.owned_set.add(char['id'])
                st.rerun()