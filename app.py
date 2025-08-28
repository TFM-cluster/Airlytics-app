# ✅ 必要ライブラリ
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

# ✅ モバイルピンチズーム許可
st.markdown("""
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    </head>
""", unsafe_allow_html=True)

# ✅ ロゴ表示
st.image(Image.open("tokyofm_4c_small.jpg"), width=100)

# ✅ タイトル
st.markdown("""
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
""", unsafe_allow_html=True)

# ✅ メインロゴ
st.image(Image.open("AIrlytics.png"), use_container_width=True)

# ✅ 説明
st.markdown("""
    <div style='text-align: center; font-family: Meiryo, sans-serif; font-size: 10pt; margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
    AIrlyticsは、ラジオの聴取行動を可視化し、<br>
    クラスターごとの特徴を分析するインサイトツールです。<br>
    2024年度の聴取率調査結果をもとに、<br>
    7つのクラスターを作成し、聴取時間に落とし込みました。<br>
    特徴量：性別、年齢、職業、エリア、ドライバー比率、聴取時間
    </div>
""", unsafe_allow_html=True)

# ✅ CSV読み込み
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()

# ✅ 列名確認
expected_columns = ["曜日", "開始時", "推定クラスタ"]
missing_cols = [col for col in expected_columns if col not in df.columns]
if missing_cols:
    st.error(f"CSVに欠損している列があります: {missing_cols}")
    st.stop()

# ✅ 選択UI
weekday_order = ["月", "火", "水", "木", "金", "土", "日"]
day_labels = weekday_order
selected_days = st.multiselect("🗓️ 曜日を選択", options=day_labels, default=["月"])
if not selected_days:
    st.warning("曜日を1つ以上選択してください")
    st.stop()

hour = st.slider("🕒 時間 (5~29時)", 5, 29, 9)

# ✅ クラスター情報
def get_cluster_info():
    return {
        1: {"text": "<詳細省略>", "img": "cluster_1.png"},
        2: {"text": "<詳細省略>", "img": "cluster_2.png"},
        3: {"text": "<詳細省略>", "img": "cluster_3.png"},
        4: {"text": "<詳細省略>", "img": "cluster_4.png"},
        5: {"text": "<詳細省略>", "img": "cluster_5.png"},
        6: {"text": "<詳細省略>", "img": "cluster_6.png"},
        7: {"text": "<詳細省略>", "img": "cluster_7.png"},
    }
cluster_info = get_cluster_info()

# ✅ 表示ロジック
match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]
if not match.empty:
    cluster = int(match.iloc[0]["推定クラスタ"])
    st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")

    info = cluster_info.get(cluster)
    if info:
        st.markdown(f"<div id='cluster{cluster}'></div>", unsafe_allow_html=True)
        st.markdown(f"### 🔍 クラスター{cluster}とは？")
        st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
        try:
            st.image(Image.open(info["img"]), width=300)
        except FileNotFoundError:
            st.warning(f"画像が見つかりません: {info['img']}")

    # ✅ マトリクス生成
    st.markdown("### 🔢 同じクラスターの他の時間帯")
    hour_range = list(range(5, 30))
    df["曜日"] = pd.Categorical(df["曜日"], categories=weekday_order, ordered=True)
    matrix_html = """
    <style>
    .table-matrix { border-collapse: collapse; margin-top: 10px; }
    .table-matrix th, .table-matrix td { border: 1px solid #ddd; text-align: center; padding: 5px; }
    .cluster-btn { background-color: #eee; border: none; padding: 3px 6px; font-size: 0.9em; color: #555; cursor: pointer; text-decoration: underline; }
    .check-icon { font-size: 1.1em; color: green; }
    </style>
    <table class="table-matrix">
        <tr><th></th>
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
                    matrix_html += f"<td><a href='#cluster{c_id}'><button class='cluster-btn'>{c_id}</button></a></td>"
            else:
                matrix_html += "<td></td>"
        matrix_html += "</tr>"
    matrix_html += "</table>"
    st.markdown(matrix_html, unsafe_allow_html=True)
else:
    st.warning("⚠️ クラスターが見つかりませんでした。")
