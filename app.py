# streamlit_app.py
import streamlit as st
from PIL import Image
import pandas as pd

# --- ページ設定 ---
st.set_page_config(
    page_title="AIrlytics",
    page_icon="📻",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- モバイルズーム対応 ---
st.markdown("""
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    </head>
""", unsafe_allow_html=True)

# --- ロゴ表示 ---
tfm_logo = Image.open("tokyofm_4c_small.jpg")
st.image(tfm_logo, width=100)

# --- キャッチコピー ---
st.markdown("""
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
""", unsafe_allow_html=True)

# --- メインロゴ ---
logo = Image.open("AIrlytics.png")
st.image(logo, use_container_width=True)

# --- 説明文 ---
st.markdown("""
    <div style='text-align: center; font-family: Meiryo, sans-serif; font-size: 10pt; margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
    AIrlyticsは、ラジオの聴取行動を可視化し、<br>
    クラスターごとの特徴を分析するインサイトツールです。<br>
    2024年度の聴取率調査結果をもとに7つのクラスターを作成しました。<br>
    性別、年齢、職業、地域、ドライバー比率、聴取時間を使用しています。
    </div>
""", unsafe_allow_html=True)

# --- CSV読み込み ---
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()

# --- 列名チェック ---
expected_columns = ["曜日", "開始時", "推定クラスタ"]
missing_cols = [col for col in expected_columns if col not in df.columns]
if missing_cols:
    st.error(f"❌ エラー：CSVに列がありません: {missing_cols}")
    st.stop()

# --- 曜日と時間帯 選択 ---
st.markdown("### 🔍 曜日と時間帯を選択")
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("🗓 曜日選択", options=day_labels, default=["月"])
if not selected_days:
    st.warning("⚠️ 1つ以上選んでください")
    st.stop()

hour = st.slider("🕒 時間選択 (5-29h)", min_value=5, max_value=29, value=9)

# --- クラスター情報定義 ---
cluster_info = {
    1: {"text": """クラスター1: 都内在住の働く中高年男女。
通勤や夜のリラックスタイムにラジオを聴く。
情報番組、ニュース、トーク番組を好む傾向。
""", "img": "cluster_1.png"},
    2: {"text": """クラスター2：男性若年層中心、平日朝と土曜夜に集中聴取
性別：男性84%。
年代：20代～30代が多数派。
職業：会社員中心、大学生・専門職も少数いる。
地域：東京都が3割、神奈川県と千葉県もバランスよくいる
""", "img": "cluster_2.png"},
    3: {"text": """クラスター3: 通勤・通学や休憩時間に、情報やエンタメを積極的に取り入れる20~30代のアクティブ層。
移動中や休憩時間を中心に聴取、ネットやSNSとの親和性が強い層。
性別：男性84%。
年代：20代～30代が多数。
職業：会社員中心、大学生、専門職も少数いる。
地域：東京都と埼玉県
""", "img": "cluster_3.png"},
    4: {"text": """クラスター4：圧倒的女性、主婦・中高齢層の平日昼間リスナー
中高齢女性の専業主婦層。
家事や昼休憩時に聴く「生活情報」「懐かしい音楽」。
テレビと同時聴取の可能性。
性別：女性93%。
年代：50代（47%）→60代（48%）。
職業：専業主婦が多い。
地域：神奈川県が最多。次点で東京都。
""", "img": "cluster_4.png"},
    5: {"text": """クラスター5：40代前後の男性中心、夕方～夜にかけて聴取
仕事帰りや夜に趣味としてラジオ聴取するミドル層
音楽、トークバラエティ好き。
10代（中学生で3割）もいるクラスタ。
性別：男性70%。
年代：30～40代が多数、10代も3割いる。
職業：会社員が多い、中学生31.3%、高校生2.3%。
地域：東京都と神奈川県に集中（65%以上）。
""", "img": "cluster_5.png"},
    6: {"text": """クラスター6：女性若年層、深夜型ユーザー、若い女性の夜更かしリスナー。
性別：女性99%。
年代：20代が最多（34%）→30代、40代の順。
職業：販売、サービス業や専門職が目立つ。
地域：東京都、神奈川県に多い
""", "img": "cluster_6.png"},
    7: {"text": """クラスター7：都内在住の男性中高年層、朝型で週末に集中、週末の朝にラジオを聴く。
性別：男性95%。
年代：40代～50代中心、60代も一定数存在。
職業：会社員、技術職・製造業系。
地域：東京都が高め
""", "img": "cluster_7.png"}
}

# --- クラスター検索&表示 ---
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
