import streamlit as st
from PIL import Image
import pandas as pd

# ページ設定
st.set_page_config(
    page_title="AIrlytics",
    page_icon="📻",
    layout="centered"
)

# モバイル表示最適化
st.markdown("""
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    </head>
""", unsafe_allow_html=True)

# ロゴとキャッチコピー
tfm_logo = Image.open("tokyofm_4c_small.jpg")
st.image(tfm_logo, width=100)

st.markdown("""
<div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
            font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
    ラジオの空気を可視化する、エアリティクス
</div>
""", unsafe_allow_html=True)

st.image("AIrlytics.png", use_container_width=True)

# 説明文
st.markdown("""
<div style='text-align: center; font-family: Meiryo, sans-serif;
            font-size: 10pt; margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
    AIrlyticsは、ラジオの聴取行動を可視化し、<br>
    クラスターごとの特徴を分析するインサイトツールです。<br>
    2024年度の聴取率調査結果（2024年4月～2025年2月の計6回）<br>
    を基に7つのクラスターを作成し、聴取時間に落とし込みました。
</div>
""", unsafe_allow_html=True)

# データ読み込み
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()
expected_columns = ["曜日", "開始時", "推定クラスタ"]
missing_cols = [col for col in expected_columns if col not in df.columns]
if missing_cols:
    st.error(f"❌ エラー：CSVに以下の列がありません → {missing_cols}")
    st.stop()

# UI選択
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("📅 曜日を選んでください（複数選択可）", options=day_labels, default=["月"])
if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選択してください。")
    st.stop()
hour = st.slider("🕒 時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# クラスター情報（画像と説明）
cluster_info = {
    1: {"text": "...", "img": "cluster_1.png"},
    2: {"text": "...", "img": "cluster_2.png"},
    3: {"text": "...", "img": "cluster_3.png"},
    4: {"text": "...", "img": "cluster_4.png"},
    5: {"text": "...", "img": "cluster_5.png"},
    6: {"text": "...", "img": "cluster_6.png"},
    7: {"text": "...", "img": "cluster_7.png"},
}

# 一致するクラスター表示
match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]
if not match.empty:
    cluster = int(match.iloc[0]["推定クラスタ"])
    st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")

    # 詳細表示
    info = cluster_info.get(cluster)
    if info:
        st.markdown(f"<div id='cluster{cluster}'></div>", unsafe_allow_html=True)
        st.markdown(f"### 💡 クラスター{cluster}とは？")
        st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
        try:
            st.image(Image.open(info["img"]), caption=f"クラスター{cluster}のイメージ", width=300)
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

    # 📌 マトリクスHTML表
    weekday_order = ["月", "火", "水", "木", "金", "土", "日"]
    hour_range = list(range(5, 30))
    df["曜日"] = pd.Categorical(df["曜日"], categories=weekday_order, ordered=True)

    matrix_html = """
    <style>
    .matrix-table {
        border-collapse: collapse;
        font-size: 11pt;
        margin-top: 10px;
    }
    .matrix-table th, .matrix-table td {
        border: 1px solid #ccc;
        padding: 5px;
        text-align: center;
    }
    .check-icon {
        color: green;
        font-weight: bold;
    }
    .cluster-link {
        font-size: 10pt;
        color: #444;
        text-decoration: underline;
    }
    </style>
    <table class="matrix-table">
        <tr><th>曜日</th>""" + "".join([f"<th>{h}</th>" for h in hour_range]) + "</tr>"

    for day in weekday_order:
        matrix_html += f"<tr><td>{day}</td>"
        for h in hour_range:
            subset = df[(df["曜日"] == day) & (df["開始時"] == h)]
            if not subset.empty:
                c_id = int(subset.iloc[0]["推定クラスタ"])
                if c_id == cluster:
                    matrix_html += "<td><span class='check-icon'>✅</span></td>"
                else:
                    matrix_html += f"<td><a href='#cluster{c_id}' class='cluster-link'>{c_id}</a></td>"
            else:
                matrix_html += "<td>-</td>"
        matrix_html += "</tr>"
    matrix_html += "</table>"

    st.markdown("### 📌 同じクラスターの他の時間帯 (曜日×時間帯)")
    st.markdown(matrix_html, unsafe_allow_html=True)

else:
    st.warning("⚠️ 該当するクラスターが見つかりませんでした。")
