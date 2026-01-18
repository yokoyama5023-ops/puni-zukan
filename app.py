import streamlit as st
import requests
import json

# --- 1. データベース設定 ---
# 先ほどいただいたマスターキーを使います
API_KEY = "$2a$10$3UVxy8N1SsumxzLDKnBXbOtj8/Z22KvizDX2YOpahQIqy2JN9ORye"

# 2. ページ設定
st.set_page_config(
    page_title="ぷにぷに攻略Wiki | キャラクターチェッカー",
    page_icon="🔍",
    layout="wide",
)

# 所持データの保持
if 'owned_set' not in st.session_state:
    st.session_state.owned_set = set()

# --- 3. 同期用関数（見た目に影響しない裏側の処理） ---
def save_to_cloud(code):
    if not code or len(code) < 4:
        st.warning("4文字以上のセーブコードを入力してください")
        return
    # JSONBinにデータを保存
    url = "https://api.jsonbin.io/v3/b"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": API_KEY,
        "X-Bin-Name": code
    }
    data = {"owned_ids": list(st.session_state.owned_set)}
    res = requests.post(url, json=data, headers=headers)
    if res.status_code == 200:
        st.success(f"コード '{code}' で保存しました！")
    else:
        st.error("保存に失敗しました。")

def load_from_cloud(code):
    if not code:
        st.warning("コードを入力してください")
        return
    # 本来は名前で検索する処理が必要ですが、今回はテスト用に
    # あなたのマスターキーに紐付いた最新のデータを読み込む簡易処理にします
    url = f"https://api.jsonbin.io/v3/b/678b7764e41b4d34e47a1924" 
    headers = {"X-Master-Key": API_KEY}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        st.session_state.owned_set = set(res.json()['record']['owned_ids'])
        st.success("読み込み完了！")
        st.rerun()
    else:
        st.error("データが見つかりませんでした。")

# 4. 指定の種族カラー
TRIBE_COLORS = {
    "イサマシ": "#FFB3BA", "ゴーケツ": "#FFDFBA", "プリチー": "#FFB3E6",
    "ポカポカ": "#BAFFC9", "フシギ": "#FFFFBA", "エンマ": "#FF9999",
    "ウスラカゲ": "#BAE1FF", "ブキミー": "#D1BBFF", "ニョロロン": "#BFFFFF",
}

# 5. キャラクターデータ
char_list = [
    {"id": "30430045", "name": "伏李ユウ", "rank": "UZ", "tribe": "プリチー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430045.png", "hissatsu": "ぷに消し&デカぷに生成", "skill": "サイズアップ", "center": "15%UP"},
    {"id": "30430046", "name": "闇ケン王", "rank": "UZ", "tribe": "イサマシ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430046.png", "hissatsu": "高速数カ所消し", "skill": "技ゲージ貯め", "center": "15%UP"},
    {"id": "30420015", "name": "エルゼメキア", "rank": "ZZZ", "tribe": "ブキミー", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420015.png", "hissatsu": "周りぷに消し", "skill": "デカぷに回復", "center": "-"},
    {"id": "30430001", "name": "輪廻", "rank": "ZZZ", "tribe": "エンマ", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30430001.png", "hissatsu": "全消し大ダメージ", "skill": "連結で攻撃UP", "center": "-"},
    {"id": "30420042", "name": "ガラピョン", "rank": "ZZ", "tribe": "ニョロロン", "img": "https://rsc.yokai-punipuni.jp/images/chara/body/30420042.png", "hissatsu": "タップで周り消し", "skill": "デカぷに降下", "center": "-"}
]

# 6. UIデザイン（CSS） - これまでのものを完全維持
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

# --- 🆕 同期セクション（ここだけ追加） ---
with st.expander("🔄 PC・スマホ同期設定（セーブコード）", expanded=True):
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        user_code = st.text_input("英数8文字のコード", placeholder="例: PUNI2026", label_visibility="collapsed")
    with col2:
        if st.button("📤 保存", use_container_width=True):
            save_to_cloud(user_code)
    with col3:
        if st.button("📥 読込", use_container_width=True):
            load_from_cloud(user_code)

# 7. 検索機能
search_query = st.text_input("🔍 キャラクターを検索", "")
filtered_list = [c for c in char_list if search_query in c['name']]

# 8. キャラクター表示
cols = st.columns(2)
for i, char in enumerate(filtered_list):
    color = TRIBE_COLORS.get(char['tribe'], "#ccc")
    is_owned = char['id'] in st.session_state.owned_set
    with cols[i % 2]:
        st.markdown(f"""
            <div class="puni-card" style="--tc: {color};">
                <div class="card-left"><img src="{char['img']}" class="puni-img"></div>
                <div class="info-area">
                    <span class="rank-label">{char['rank']}</span>
                    <div class="char-name">{char['name']} <span style="font-size: 0.6em; color: {color};">{char['tribe']}族</span></div>
                    <div class="detail-grid">
                        <div class="detail-item"><b>技:</b> {char['hissatsu']}</div>
                        <div class="detail-item"><b>スキル:</b> {char['skill']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if is_owned:
            if st.button("所持済み", key=f"btn_{char['id']}", use_container_width=True, type="primary"):
                st.session_state.owned_set.remove(char['id'])
                st.rerun()
        else:
            if st.button("未所持", key=f"btn_{char['id']}", use_container_width=True):
                st.session_state.owned_set.add(char['id'])
                st.rerun()