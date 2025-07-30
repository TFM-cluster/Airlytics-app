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

# ✅ ロゴ画像の表示（TFMロゴ → メインロゴ）
tfm_logo = Image.open("tokyofm_4c_small.jpg")
st.image(tfm_logo, width=100)

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
        "text": "クラスタ1：都内在住の働く中高年男女。通勤や夜のリラックスタイムにラジオを聴く。情報番組、ニュース、トーク番組を好む傾向。\n"
                "性別：男性56％、女性43％で半々。\n"
                "年代：50代～60代で43%→次に40代。\n"
                "職業：会社員と専門職（自由業）が多く、安定層。\n"
                "地域：東京都中心（47％）→次点で神奈川\n"
                "聴取時間傾向：平日：8時~9時台、22時台／土日：7時~9時台、夜の23時にピーク",
        "img": "cluster_1.png"
    },
    2: {
        "text": "クラスタ2：ビジネスマン中心。通勤時間帯に情報収集。",
        "img": "cluster_2.png"
    },
    3: {
        "text": "クラスタ3：主婦層。午前中にトーク番組を聴く傾向。",
        "img": "cluster_3.png"
    },
    4: {
        "text": "クラスタ4：学生＋シニア混合。深夜帯のニッチな番組志向。",
        "img": "cluster_4.png"
    },
    5: {
        "text": "クラスタ5：若年社会人。夜のリラックスタイムにBGM志向。",
        "img": "cluster_5.png"
    },
    6: {
        "text": "クラスタ6：働く中高年。通勤・夜にニュースや情報番組を好む。",
        "img": "cluster_6.png"
    },
    7: {
        "text": "クラスタ7：週末型リスナー。週末朝のルーティン聴取。",
        "img": "cluster_7.png"
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
            st.image(cluster_img, caption=f"クラスタ{cluster}のイメージ", width=300)  # ← ここで画像サイズ指定
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

    # ✅ 同じクラスタの他時間帯表示
    others = df[(df["推定クラスタ"] == cluster) & ~((df["曜日"] == weekday) & (df["開始時"] == hour))]
    if not others.empty:
        st.markdown("📍 同じクラスターの他の時間帯：")
        for _, row in others.iterrows():
            st.markdown(f"- {row['曜日']} {row['開始時']}時台")
else:
    st.warning("⚠️ 該当するクラスタが見つかりませんでした。")
