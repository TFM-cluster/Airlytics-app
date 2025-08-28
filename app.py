import streamlit as st
from PIL import Image
import pandas as pd

# ✅ ページ設定
st.set_page_config(
    page_title="AIrlytics",
    page_icon="📻",
    layout="centered",
    initial_sidebar_state="auto"
)

# ✅ TOKYO FM ロゴ
tfm_logo = Image.open("tokyofm_4c_small.jpg")
st.image(tfm_logo, width=100)

# ✅ キャッチコピー
st.markdown("""
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
""", unsafe_allow_html=True)

# ✅ メインロゴ
logo = Image.open("AIrlytics.png")
st.image(logo, use_container_width=True)

# ✅ 説明文
st.markdown("""
    <div style='text-align: center; font-family: Meiryo, sans-serif;
                font-size: 10pt; margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
        AIrlyticsは、ラジオの聴取行動を可視化し、<br>
        クラスターごとの特徴を分析するインサイトツールです。<br>
        2024年度の聴取率調査結果（2024年4月～2025年2月の計6回）<br>
        を基に7つのクラスターを作成し、聴取時間に落とし込みました。
    </div>
""", unsafe_allow_html=True)

# ✅ CSV読み込み
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()

# ✅ 曜日と時間帯入力
st.markdown("### 🔍 曜日と時間帯を選択してください")
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("📅 曜日を選んでください（複数選択可）", options=day_labels, default=["月"])

if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選択してください。")
    st.stop()

hour = st.slider("🕒 時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# ✅ クラスター定義
cluster_info = {
    1: {"text": "クラスター1: 都内在住の働く中高年男女。通勤や夜にラジオを聴く。", "img": "cluster_1.png"},
    2: {"text": "クラスター2：男性若年層中心、平日朝と土曜夜に集中聴取。", "img": "cluster_2.png"},
    3: {"text": "クラスター3: 20~30代のアクティブ層。SNSとの親和性が高い。", "img": "cluster_3.png"},
    4: {"text": "クラスター4：中高年の女性主婦層。平日昼に生活情報などを聴取。", "img": "cluster_4.png"},
    5: {"text": "クラスター5：40代男性中心、趣味的に音楽・トークを聴取。", "img": "cluster_5.png"},
    6: {"text": "クラスター6：女性若年層、夜型傾向が強く深夜にラジオ聴取。", "img": "cluster_6.png"},
    7: {"text": "クラスター7：中高年の男性、週末朝のルーティンとして聴取。", "img": "cluster_7.png"},
}

# ✅ 対象抽出
match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]
if match.empty:
    st.warning("⚠️ 該当するクラスターが見つかりませんでした。")
    st.stop()

cluster = int(match.iloc[0]["推定クラスタ"])
st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")

# ✅ テーブル表示 (HTML + JSスクロール付き)
weekday_order = ["月", "火", "水", "木", "金", "土", "日"]
hour_range = list(range(5, 30))
df["曜日"] = pd.Categorical(df["曜日"], categories=weekday_order, ordered=True)

matrix_html = """
<style>
.table-matrix {
    border-collapse: collapse;
    margin-top: 10px;
}
.table-matrix th, .table-matrix td {
    border: 1px solid #ccc;
    text-align: center;
    padding: 5px;
}
.cluster-btn {
    background-color: #f2f2f2;
    border: none;
    padding: 3px 6px;
    font-size: 0.9em;
    color: #007bff;
    cursor: pointer;
    text-decoration: underline;
}
.check-icon {
    font-size: 1.2em;
    color: green;
}
</style>
<script>
function scrollToCluster(id) {
    const el = document.getElementById(id);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
    }
}
</script>
<table class="table-matrix">
<tr><th></th>""" + "".join(f"<th>{h}</th>" for h in hour_range) + "</tr>"

for day in weekday_order:
    matrix_html += f"<tr><td>{day}</td>"
    for h in hour_range:
        sub = df[(df["曜日"] == day) & (df["開始時"] == h)]
        if not sub.empty:
            c_id = int(sub.iloc[0]["推定クラスタ"])
            if c_id == cluster:
                matrix_html += "<td><span class='check-icon'>✅</span></td>"
            else:
                matrix_html += f"""<td><button class='cluster-btn' onclick="scrollToCluster('cluster{c_id}')">{c_id}</button></td>"""
        else:
            matrix_html += "<td></td>"
    matrix_html += "</tr>"
matrix_html += "</table>"

st.markdown("### 📌 同じクラスターの他の時間帯 (曜日×時間帯)")
st.markdown(matrix_html, unsafe_allow_html=True)

# ✅ クラスタ詳細表示
info = cluster_info.get(cluster)
if info:
    st.markdown(f"<div id='cluster{cluster}'></div>", unsafe_allow_html=True)
    st.markdown(f"### 💡 クラスター{cluster}とは？")
    st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
    try:
        cluster_img = Image.open(info["img"])
        st.image(cluster_img, caption=f"クラスター{cluster}のイメージ", width=300)
    except FileNotFoundError:
        st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")
