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

# ✅ スマホでピンチズームを許可する（viewportメタタグを上書き）
st.markdown("""
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    </head>
""", unsafe_allow_html=True)

# ✅ TOKYO FM ロゴの表示
tfm_logo = Image.open("tokyofm_4c_small.jpg")
st.image(tfm_logo, width=100)

# ✅ キャッチコピー
st.markdown(
    """
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif; font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ メインロゴの表示
logo = Image.open("AIrlytics.png")
st.image(logo, use_container_width=True)

# ✅ ロゴ下の説明文
st.markdown(
    """
    <div style='text-align: center; font-family: Meiryo, sans-serif; font-size: 10pt; margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
        AIrlyticsは、ラジオの聴取行動を可視化し、<br>
        クラスターごとの特徴を分析するインサイトツールです。<br>
        2024年度の聴取率調査結果（2024年4月～2025年2月の計6回）<br>
        を基に7つのクラスターを作成し、聴取時間に落とし込みました。<br>
        クラスター作成に使用した特徴量は、<br>
        性別、年齢、職業、エリア、ドライバー比率、聴取時間です。
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ CSV読み込み関数（キャッシュ）
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()

# ✅ 列名チェック
expected_columns = ["曜日", "開始時", "推定クラスタ"]
missing_cols = [col for col in expected_columns if col not in df.columns]
if missing_cols:
    st.error(f"❌ エラー：CSVに以下の列がありません → {missing_cols}")
    st.stop()

# ✅ 曜日と時間帯の入力UI
st.markdown("### 🔍 曜日と時間帯を選択してください")
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("📅 曜日を選んでください（複数選択可）", options=day_labels, default=["月"])
if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選択してください。")
    st.stop()

hour = st.slider("🕒 時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# ✅ クラスター情報定義（省略なし）
cluster_info = {
    1: {"text": "クラスター1: 都内在住の働く中高年男女。通勤や夜のリラックスタイムにラジオを聴く。情報番組、ニュース、トーク番組を好む傾向。", "img": "cluster_1.png"},
    2: {"text": "クラスター2：男性若年層中心、平日朝と土曜夜に集中聴取。性別：男性84%。年代：20代～30代。職業：会社員中心、大学生・専門職も。地域：東京都3割、神奈川・千葉も。", "img": "cluster_2.png"},
    3: {"text": "クラスター3: 通勤・通学や休憩時間に、情報やエンタメを積極的に取り入れる20~30代のアクティブ層。移動中や休憩時間中心に聴取、SNS親和性も高い。性別：男性84%。職業：会社員、大学生、専門職。地域：東京都・埼玉県。", "img": "cluster_3.png"},
    4: {"text": "クラスター4：圧倒的女性、主婦・中高齢層の平日昼間リスナー。生活情報や懐かしい音楽、テレビとの同時聴取も。性別：女性93%。年代：50代（47%）、60代（48%）。職業：専業主婦。地域：神奈川、東京。", "img": "cluster_4.png"},
    5: {"text": "クラスター5：40代前後の男性中心、夕方～夜にかけて聴取。仕事帰りや夜の趣味。音楽やトークバラエティ好き。10代（中学生で3割）も。性別：男性70%。年代：30～40代、10代も3割。職業：会社員、中学生31.3%、高校生2.3%。地域：東京・神奈川65%以上。", "img": "cluster_5.png"},
    6: {"text": "クラスター6：女性若年層、深夜型ユーザー。若い女性の夜更かしリスナー。性別：女性99%。年代：20代が最多（34%）、次いで30代・40代。職業：販売・サービス業や専門職。地域：東京都・神奈川県。", "img": "cluster_6.png"},
    7: {"text": "クラスター7：都内在住の男性中高年層、朝型で週末に集中。週末の朝にラジオ。性別：男性95%。年代：40～50代中心、60代も。職業：会社員、技術職、製造業系。地域：東京都。", "img": "cluster_7.png"}
}

# ✅ クラスター表示
match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]
if not match.empty:
    cluster = int(match.iloc[0]["推定クラスタ"])
    st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")
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

# ✅ マトリクス表示
weekday_order = ["月", "火", "水", "木", "金", "土", "日"]
hour_range = list(range(5, 30))
df["曜日"] = pd.Categorical(df["曜日"], categories=weekday_order, ordered=True)

same_cluster_df = df[(df["推定クラスタ"] == cluster)]
matrix_html = """
<style>
.table-matrix {
    border-collapse: collapse;
    margin-top: 10px;
}
.table-matrix th, .table-matrix td {
    border: 1px solid #ddd;
    text-align: center;
    padding: 5px;
}
.cluster-btn {
    background-color: #eee;
    border: none;
    padding: 3px 6px;
    font-size: 0.9em;
    color: #555;
    cursor: pointer;
    text-decoration: underline;
}
.check-icon {
    font-size: 1.1em;
    color: green;
}
</style>
<table class="table-matrix">
    <tr>
        <th></th>
"""
for h in hour_range:
    matrix_html += f"<th>{h}時台</th>"
matrix_html += "</tr>"

for day in weekday_order:
    matrix_html += f"<tr><td>{day}</td>"
    for h in hour_range:
        subset = df[(df["曜日"] == day) & (df["開始時"] == h)]
        if not subset.empty:
            c_id = int(subset.iloc[0]["推定クラスタ"])
            if c_id == cluster:
                matrix_html += "<td><span class='check-icon'>✅</span></td>"
            else:
                matrix_html += f"<td><a href='#cluster{c_id}'><button class='cluster-btn'>{c_id}</button></a></td>"
        else:
            matrix_html += "<td></td>"
    matrix_html += "</tr>"
matrix_html += "</table>"

st.markdown("### 📌 同じクラスターの他の時間帯 (曜日×時間帯)")
st.markdown(matrix_html, unsafe_allow_html=True)
