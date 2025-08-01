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

# ✅ キャッチコピー（太字＆スタイリッシュ）
st.markdown(
    """
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ メインロゴの表示（AIrlytics）
logo = Image.open("AIrlytics.png")
st.image(logo, use_container_width=True)

# ✅ ロゴ下の説明文（小さめのフォントに調整）
st.markdown(
    """
    <div style='text-align: center; font-family: Meiryo, sans-serif;
                font-size: 10pt; margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
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

# ✅ 曜日選択（トグルから multiselect に変更）
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("📅 曜日を選んでください（複数選択可）", options=day_labels, default=["月"])

if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選択してください。")
    st.stop()

# ✅ 時間帯スライダー
hour = st.slider("🕒 時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# ✅ クラスター情報の定義
cluster_info = {
    1: {
        "text": "クラスター1: 都内在住の働く中高年男女。\n"
                "通勤や夜のリラックスタイムにラジオを聴く。\n"
                "情報番組、ニュース、トーク番組を好む傾向。\n",
        "img": "cluster_1.png"
    },
    2: {
        "text": "クラスター2：男性若年層中心、平日朝と土曜夜に集中聴取\n"
                "性別：男性84%。\n"
                "年代：20代～30代が多数派。\n"
                "職業：会社員中心、大学生・専門職も少数いる。\n"
                "地域：東京都が3割、神奈川県と千葉県もバランスよくいる\n",
        "img": "cluster_2.png"
    },
    3: {
        "text": "クラスター3: 通勤・通学や休憩時間に、情報やエンタメを積極的に取り入れる20~30代のアクティブ層。\n"
                "移動中や休憩時間を中心に聴取、ネットやSNSとの親和性が強い層。\n"
                "性別：男性84%。\n"
                "年代：20代～30代が多数。\n"
                "職業：会社員中心、大学生、専門職も少数いる。\n"
                "地域：東京都と埼玉県\n",
        "img": "cluster_3.png"
    },
    4: {
        "text": "クラスター4：圧倒的女性、主婦・中高齢層の平日昼間リスナー\n"
                            "中高齢女性の専業主婦層。\n"
                            "家事や昼休憩時に聴く「生活情報」「懐かしい音楽」。\n"
                            "テレビと同時聴取の可能性。\n"
                "性別：女性93%。\n"
                "年代：50代（47%）→60代（48%）。\n"
                "職業：専業主婦が多い。\n"
                "地域：神奈川県が最多。次点で東京都。\n",
        "img": "cluster_4.png"
    },
    5: {
        "text": "クラスター5：40代前後の男性中心、夕方～夜にかけて聴取\n"
                            "仕事帰りや夜に趣味としてラジオ聴取するミドル層\n"
                            "音楽、トークバラエティ好き。\n"
                            "10代（中学生で3割）もいるクラスタ。\n"
                "性別：男性70%。\n"
                "年代：30～40代が多数、10代も3割いる。\n"
                "職業：会社員が多い、中学生31.3%、高校生2.3%。\n"
                "地域：東京都と神奈川県に集中（65%以上）。\n",
        "img": "cluster_5.png"
    },
    6: {
        "text": "クラスター6：女性若年層、深夜型ユーザー、若い女性の夜更かしリスナー。\n"
                "性別：女性99%。\n"
                "年代：20代が最多（34%）→30代、40代の順。\n"
                "職業：販売、サービス業や専門職が目立つ。\n"
                "地域：東京都、神奈川県に多い\n",
        "img": "cluster_6.png"
    },
    7: {
        "text": "クラスター7：都内在住の男性中高年層、朝型で週末に集中、週末の朝にラジオを聴く。\n"
                "性別：男性95%。\n"
                "年代：40代～50代中心、60代も一定数存在。\n"
                "職業：会社員、技術職・製造業系。\n"
                "地域：東京都が高め\n",
        "img": "cluster_7.png"
    }
}

# ✅ 該当クラスター検索
match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]

if not match.empty:
    cluster = int(match.iloc[0]["推定クラスタ"])
    st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")

    # ✅ クラスター詳細を表示
    info = cluster_info.get(cluster)
    if info:
        st.markdown(f"<div id='cluster{cluster}'></div>", unsafe_allow_html=True)  # ←アンカー追加
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

else:
    st.warning("⚠️ 該当するクラスターが見つかりませんでした。")
