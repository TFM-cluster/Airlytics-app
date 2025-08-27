# ✅ 必要ライブラリのインポート
import streamlit as st
from PIL import Image
import pandas as pd

# ✅ ページ設定
st.set_page_config(
    page_title="AIrlytics",
    page_icon="🎼",
    layout="centered",
    initial_sidebar_state="auto"
)

# ✅ スマホズーム許可
st.markdown("""
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    </head>
""", unsafe_allow_html=True)

# ✅ TOKYO FMロゴ
st.image(Image.open("tokyofm_4c_small.jpg"), width=100)

# ✅ タイトル・ロゴ
st.markdown("""
<div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif; font-size: 21pt; font-weight: bold;'>
    ラジオの空気を可視化する、エアリティクス
</div>
""", unsafe_allow_html=True)
st.image(Image.open("AIrlytics.png"), use_container_width=True)

# ✅ 説明文
st.markdown("""
<div style='text-align: center; font-family: Meiryo, sans-serif; font-size: 10pt; color: #333;'>
    AIrlyticsは、ラジオの聴取行動を可視化し、クラスターごとの特徴を分析するインサイトツールです。<br>
    2024年度の聴取率調査結果（2024年4月～2025年2月の計6回）を基に7つのクラスターを作成。<br>
    性別、年齢、職業、エリア、ドライバー比率、聴取時間などの特徴量を使用しています。
</div>
""", unsafe_allow_html=True)

# ✅ データ読み込み
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")
df = load_data()

# ✅ 列チェック
required_cols = ["曜日", "開始時", "推定クラスタ"]
if any(col not in df.columns for col in required_cols):
    st.error("❌ 必要な列が不足しています。")
    st.stop()

# ✅ UI部品
st.markdown("### 🔍 曜日と時間帯を選択してください")
days = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("🗕️ 曜日選択", options=days, default=["月"])
if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選択してください。")
    st.stop()
hour = st.slider("🕒 時間（5〜29時）", 5, 29, 9)

# ✅ クラスタ情報
cluster_info = {
    1: {"text": "クラスター1: 都内在住の働く中高年男女...", "img": "cluster_1.png"},
    2: {"text": "クラスター2: 男性若年層中心...", "img": "cluster_2.png"},
    3: {"text": "クラスター3: アクティブな20-30代中心...", "img": "cluster_3.png"},
    4: {"text": "クラスター4: 中高年女性・主婦中心...", "img": "cluster_4.png"},
    5: {"text": "クラスター5: 夜型ミドル層...", "img": "cluster_5.png"},
    6: {"text": "クラスター6: 若い女性の深夜リスナー...", "img": "cluster_6.png"},
    7: {"text": "クラスター7: 朝型中高年男性...", "img": "cluster_7.png"},
}

# ✅ マッチ探索（selected_cluster 優先）
if "selected_cluster" in st.session_state:
    cluster = st.session_state.selected_cluster
    match = df[df["推定クラスタ"] == cluster].head(1)
else:
    match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]
    cluster = int(match.iloc[0]["推定クラスタ"]) if not match.empty else None

if cluster:
    st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")
    info = cluster_info.get(cluster)
    if info:
        st.markdown(f"### 💡 クラスター{cluster}とは？")
        st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
        try:
            st.image(Image.open(info["img"]), caption=f"クラスター{cluster}のイメージ", width=300)
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

    # ✅ マトリクス表示
    st.markdown("### 📌 同じクラスターの他の時間帯 (曜日×時間帯)")
    hour_range = list(range(5, 30))
    df["曜日"] = pd.Categorical(df["曜日"], categories=days, ordered=True)
    df = df.sort_values(["曜日", "開始時"])

    for day in days:
        cols = st.columns(len(hour_range) + 1)
        cols[0].markdown(f"**{day}**")
        for i, h in enumerate(hour_range):
            subset = df[(df["曜日"] == day) & (df["開始時"] == h)]
            if not subset.empty:
                c_id = int(subset.iloc[0]["推定クラスタ"])
                if c_id == cluster:
                    cols[i + 1].markdown("✅")
                else:
                    if cols[i + 1].button(f"{c_id}", key=f"btn_{day}_{h}"):
                        st.session_state.selected_cluster = c_id
                        st.experimental_rerun()
            else:
                cols[i + 1].markdown("-")
else:
    st.warning("⚠️ 該当するクラスターが見つかりませんでした。")
