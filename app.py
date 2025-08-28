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

# ✅ スマホでピンチズームを許可する
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
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ メインロゴ
logo = Image.open("AIrlytics.png")
st.image(logo, use_container_width=True)

# ✅ 説明文
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

# ✅ CSV読込
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")
df = load_data()

# ✅ 必須列チェック
expected_columns = ["曜日", "開始時", "推定クラスタ"]
missing_cols = [col for col in expected_columns if col not in df.columns]
if missing_cols:
    st.error(f"❌ エラー：CSVに以下の列がありません → {missing_cols}")
    st.stop()

# ✅ クラスタ情報
cluster_info = {
    1: {"text": "クラスター1: 都内在住の働く中高年男女。\n通勤や夜のリラックスタイムにラジオを聴く。\n情報番組、ニュース、トーク番組を好む傾向。\n", "img": "cluster_1.png"},
    2: {"text": "クラスター2：男性若年層中心、平日朝と土曜夜に集中聴取\n性別：男性84%。\n年代：20代～30代が多数派。\n職業：会社員中心、大学生・専門職も少数。\n地域：東京都が3割、神奈川・千葉もバランス良し\n", "img": "cluster_2.png"},
    3: {"text": "クラスター3: 20~30代のアクティブ層。移動中や休憩時間に聴取、SNSとの親和性強い。\n", "img": "cluster_3.png"},
    4: {"text": "クラスター4：女性比率高く、主婦・中高年層。平日昼間の生活情報や懐かし音楽。\n", "img": "cluster_4.png"},
    5: {"text": "クラスター5：40代前後の男性中心、夕方〜夜の趣味時間に聴取。\n", "img": "cluster_5.png"},
    6: {"text": "クラスター6：女性若年層、深夜型ユーザー。\n", "img": "cluster_6.png"},
    7: {"text": "クラスター7：都内男性中高年、週末朝中心。\n", "img": "cluster_7.png"}
}

# ✅ セッション状態にクラスタ指定があれば優先表示
if "selected_cluster" in st.session_state:
    selected_cluster = st.session_state.selected_cluster
    info = cluster_info.get(selected_cluster)
    st.markdown(f"<div id='cluster{selected_cluster}'></div>", unsafe_allow_html=True)
    st.markdown(f"### 💡 クラスター{selected_cluster}とは？")
    st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
    try:
        img = Image.open(info["img"])
        st.image(img, caption=f"クラスター{selected_cluster}のイメージ", width=300)
    except FileNotFoundError:
        st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

# ✅ 入力UI
st.markdown("### 🔍 曜日と時間帯を選択してください")
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("📅 曜日", options=day_labels, default=["月"])
hour = st.slider("🕒 時間（5〜29）", min_value=5, max_value=29, value=9)

if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選んでください。")
    st.stop()

# ✅ 該当クラスタ検索
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
            img = Image.open(info["img"])
            st.image(img, caption=f"クラスター{cluster}のイメージ", width=300)
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

    # ✅ マトリクス表示
    st.markdown("### 📌 同じクラスターの他の時間帯 (曜日×時間帯)")
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
        matrix_html += f"<th>{h}時</th>"
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
                    btn_key = f"btn_{day}_{h}"
                    if st.button(f"{c_id}", key=btn_key):
                        st.session_state.selected_cluster = c_id
                        st.experimental_rerun()
                    matrix_html += f"<td><button class='cluster-btn'>{c_id}</button></td>"
            else:
                matrix_html += "<td>-</td>"
        matrix_html += "</tr>"
    matrix_html += "</table>"
    st.markdown(matrix_html, unsafe_allow_html=True)
else:
    st.warning("⚠️ データが見つかりませんでした。")
