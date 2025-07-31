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

# ✅ TOKYO FM ロゴの表示
tfm_logo = Image.open("tokyofm_4c_small.jpg")
st.image(tfm_logo, width=100)

# ✅ キャッチコピー（太字＆スタイリッシュ）
st.markdown(
    """
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 26pt; font-weight: bold; margin-top: 5px; margin-bottom: -10px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ メインロゴの表示（AIrlytics）
logo = Image.open("AIrlytics.png")
st.image(logo, use_container_width=True)

# ✅ CSS（フォント拡大＋背景色など）
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 12px !important;
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

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

# ✅ 入力UI
st.markdown("### 🔍 曜日と時間帯を選択してください")
weekday = st.selectbox("曜日を選んでください", df["曜日"].unique(), index=df["曜日"].unique().tolist().index("月"))
hour = st.slider("時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# ✅ クラスター情報の定義
cluster_info = {
    1: {
        "text": "クラスタ1：都内在住の働く中高年男女...
...（中略：すでに反映済みのテキスト）...
    }
}

# ✅ 該当クラスタ検索
match = df[(df["曜日"] == weekday) & (df["開始時"] == hour)]

if not match.empty:
    cluster = int(match.iloc[0]["推定クラスタ"])
    st.success(f"✅ {weekday}曜 {hour}時台 は『クラスター {cluster}』です")

    # ✅ クラスター詳細を表示
    info = cluster_info.get(cluster)
    if info:
        st.markdown(f"### 💡 クラスター{cluster}とは？")
        st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)

        try:
            cluster_img = Image.open(info["img"])
            st.image(cluster_img, caption=f"クラスタ{cluster}のイメージ", width=300)
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

    # ✅ 同じクラスターの他時間帯表示
    weekday_order = ["月", "火", "水", "木", "金", "土", "日"]
    df["曜日"] = pd.Categorical(df["曜日"], categories=weekday_order, ordered=True)

    others = df[(df["推定クラスタ"] == cluster) & ~((df["曜日"] == weekday) & (df["開始時"] == hour))]
    if not others.empty:
        st.markdown("📍 同じクラスターの他の時間帯（曜日順）：")
        others_sorted = others.sort_values(by=["曜日", "開始時"])
        for _, row in others_sorted.iterrows():
            st.markdown(f"- {row['曜日']} {row['開始時']}時台")
else:
    st.warning("⚠️ 該当するクラスタが見つかりませんでした。")
