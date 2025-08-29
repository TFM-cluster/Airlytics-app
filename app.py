# 📦 必要ライブラリ
import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components

# ✅ ページ設定
st.set_page_config(
    page_title="AIrlytics",
    page_icon=Image.open("AIrlytics.png"),  #AIrlytics.png
    layout="centered",
    initial_sidebar_state="auto"
)

# ✅ AIrlyticsのアイコン（favicon）をスマホ対応としてHTMLで追加
st.markdown("""
<!-- 強制的にfaviconを設定する -->
<link rel="icon" href="https://yourdomain.com/AIrlytics.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="https://yourdomain.com/AIrlytics.png">
<link rel="manifest" href="/manifest.json">
""", unsafe_allow_html=True)

# ✅ スマホでピンチズームを許可
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
""", unsafe_allow_html=True)

# ✅ ロゴなど表示
st.image(Image.open("tokyofm_4c_small.jpg"), width=100)

st.markdown("""
    <div style='text-align: center; color: #3399cc; font-family: Meiryo, sans-serif;
                font-size: 21pt; font-weight: bold; margin-top: 10px; margin-bottom: -5px;'>
        ラジオの空気を可視化する、エアリティクス
    </div>
""", unsafe_allow_html=True)

st.image(Image.open("AIrlytics.png"), use_container_width=True)

st.markdown("""
    <div style='text-align: center; font-family: Meiryo, sans-serif; font-size: 10pt;
                margin-top: -5px; margin-bottom: 20px; line-height: 1.6; color: #333;'>
        AIrlyticsは、ラジオの聴取行動を可視化し、<br>
        クラスターごとの特徴を分析するインサイトツールです。<br>
        2024年度の聴取率調査結果（2024年4月～2025年2月の計6回）<br>
        を基に7つのクラスターを作成し聴取時間に落とし込みました。<br>
        クラスター作成に使用した特徴量は、<br>
        性別、年齢、職業、エリア、ドライバー比率、聴取時間です。
    </div>
""", unsafe_allow_html=True)

# ✅ データ読込
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()

# ✅ 入力UI
st.markdown("### 🔍 曜日と時間帯を選択してください")
day_labels = ["月", "火", "水", "木", "金", "土", "日"]
selected_days = st.multiselect("🔕️ 曜日を選んでください（複数選択可）", options=day_labels, default=["月"])
if not selected_days:
    st.warning("⚠️ 曜日を1つ以上選択してください。")
    st.stop()

hour = st.slider("🕒 時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# ✅ クラスター辞書
cluster_info = {
    1: {"text": "クラスター1: \n都内在住の働く中高年男女。\n通勤や夜のリラックスタイムにラジオを聴く。\n情報番組、ニュース、トーク番組を好む傾向。", "img": "cluster_1.png"},
    2: {"text": "クラスター2：\n男性若年層中心、平日朝と土曜夜に集中聴取\n性別：男性84%。\n年代：20代～30代が多数派。\n職業：会社員中心、大学生・専門職も少数いる。\n地域：東京都が3割、神奈川県と千葉県もバランスよくいる", "img": "cluster_2.png"},
    3: {"text": "クラスター3: \n通勤・通学や休憩時間に情報やエンタメを取り入れるアクティブ層。\n移動中や休憩中に聴取、SNSとの親和性が高い。\n性別：男性84%。\n年代：20代～30代。\n地域：東京都と埼玉県。", "img": "cluster_3.png"},
    4: {"text": "クラスター4：\n主婦・中高齢層の平日昼間リスナー。\n家事中や昼休憩に生活情報・懐メロを聴く。\n性別：女性93%。\n年代：50代〜60代。\n職業：専業主婦が多い。\n地域：神奈川・東京。", "img": "cluster_4.png"},
    5: {"text": "クラスター5：\n夕方〜夜に聴取する40代男性中心。\n音楽やトークを趣味的に楽しむ層。\n10代（中学生）も3割存在。\n職業：会社員中心、中学生31%。\n地域：東京・神奈川に集中。", "img": "cluster_5.png"},
    6: {"text": "クラスター6：\n深夜型の若年女性リスナー。\n性別：女性99%。\n年代：20〜30代。\n職業：販売、サービス業や専門職が多い。\n地域：東京都、神奈川県。", "img": "cluster_6.png"},
    7: {"text": "クラスター7：\n週末朝に集中する都内在住の中高年男性。\n性別：男性95%。\n年代：40代〜60代。\n職業：会社員、技術職など。\n地域：東京都が多い。", "img": "cluster_7.png"},
}

# ✅ クラスター検索
data_match = df[(df["曜日"].isin(selected_days)) & (df["開始時"] == hour)]
if not data_match.empty:
    cluster = int(data_match.iloc[0]["推定クラスタ"])
    st.success(f"✅ {', '.join(selected_days)}曜 {hour}時台 は『クラスター {cluster}』です")

    # クラスター説明（IDジャンプ用）
    st.markdown(f"<div id='cluster{cluster}'></div>", unsafe_allow_html=True)
    st.markdown(f"### 💡 クラスター{cluster}とは？")
    info = cluster_info.get(cluster)
    if info:
        st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
        try:
            st.image(Image.open(info["img"]), caption=f"クラスター{cluster}のイメージ", width=300)
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")

    # ✅ マトリクス生成
    weekday_order = ["月", "火", "水", "木", "金", "土", "日"]
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
                    matrix_html += f"""
                    <td><button class='cluster-btn' onclick=\"document.getElementById('cluster{c_id}').scrollIntoView({{behavior: 'smooth'}});\">{c_id}</button></td>
                    """
            else:
                matrix_html += "<td></td>"
        matrix_html += "</tr>"
    matrix_html += "</table>"

    st.markdown("""
    <div style='margin-bottom: 0px; font-size: 16pt; font-weight: bold; color: #333;'>📌 同じクラスターの他の時間帯 (曜日×時間帯)</div>
    """, unsafe_allow_html=True)
    components.html(matrix_html, height=380, scrolling=True)

# ✅ すべてのクラスターを表示
st.markdown("""
<div style='margin-top: 5px; font-size: 16pt; font-weight: bold; color: #333;'>🔎 全クラスター一覧</div>
""", unsafe_allow_html=True)
for cid in sorted(cluster_info.keys()):
    info = cluster_info[cid]
    st.markdown(f"<div id='cluster{cid}'></div>", unsafe_allow_html=True)
    with st.expander(f"クラスター{cid}の説明を見る"):
        st.markdown(f"<div style='white-space: pre-wrap;'>{info['text']}</div>", unsafe_allow_html=True)
        try:
            st.image(Image.open(info["img"]), caption=f"クラスター{cid}のイメージ", width=300)
        except FileNotFoundError:
            st.warning(f"⚠️ 画像ファイル『{info['img']}』が見つかりません。")









