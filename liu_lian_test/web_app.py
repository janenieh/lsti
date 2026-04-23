import streamlit as st
from app import (
    load_questions,
    load_scoring,
    load_personas,
    calculate_scores,
    determine_result,
)

# =========================
# 页面基础设置
# =========================
st.set_page_config(
    page_title="LSTI - 刘恋粉丝人格测试",
    page_icon="🎤",
    layout="centered"
)

st.markdown("""
<style>
/* ===== 全局背景 ===== */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background-color: #adc48a;
}

/* ===== 主内容区：微透明卡片 ===== */
.block-container {
    max-width: 760px;
    margin: 0 auto;
    padding-top: 0.2rem !important;
    padding-bottom: 0.6rem !important;
    padding-left: 0.6rem;
    padding-right: 0.6rem;

    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);

    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

/* ===== 深色文字，避免夜间模式问题 ===== */
html, body, .stApp,
h1, h2, h3, h4, h5,
p, span, div,
label,
[data-testid="stMarkdownContainer"],
[data-testid="stText"] {
    color: #1a1a1a !important;
}

/* ===== 标题与段落 ===== */
h1, h2, h3 {
    margin-top: 0.25rem !important;
    margin-bottom: 0.45rem !important;
    line-height: 1.25 !important;
}

h1 {
    font-size: 1.8rem !important;
}

p {
    margin-bottom: 0.55rem !important;
    line-height: 1.55 !important;
}

.stProgress {
    margin-top: 0.35rem;
    margin-bottom: 0.55rem;
}

hr {
    margin-top: 0.6rem !important;
    margin-bottom: 0.75rem !important;
}

/* ===== 最强制的按钮样式：直接作用到所有 button ===== */
button {
    width: 100% !important;
    display: block !important;
    min-height: 44px !important;
    padding: 8px 12px !important;
    margin: 0 0 4px 0 !important;

    border-radius: 12px !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    background: rgba(255, 255, 255, 0.92) !important;
    color: #1a1a1a !important;

    font-size: 15px !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    text-align: left !important;
    box-sizing: border-box !important;
}

/* 按钮内文字 */
button p, button span {
    margin: 0 !important;
    color: #1a1a1a !important;
    text-align: left !important;
}

/* hover / focus */
button:hover {
    border-color: rgba(0, 0, 0, 0.22) !important;
    background: rgba(255, 255, 255, 0.98) !important;
}

button:focus {
    box-shadow: 0 0 0 0.15rem rgba(120, 150, 80, 0.18) !important;
}

/* 手机上 columns 保持横排 */
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 0.5rem !important;
        align-items: stretch !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
    }

    .block-container {
        max-width: 100%;
        padding-top: 0.2rem !important;
        padding-bottom: 0.6rem !important;
        padding-left: 0.6rem;
        padding-right: 0.6rem;
        background: rgba(255, 255, 255, 0.74);
        border-radius: 14px;
    }

    h1 {
        font-size: 1.45rem !important;
    }

    h2 {
        font-size: 1.2rem !important;
    }

    h3 {
        font-size: 1.05rem !important;
    }

    p {
        font-size: 0.97rem !important;
    }

    button {
        min-height: 42px !important;
        padding: 7px 10px !important;
        font-size: 14px !important;
        margin-bottom: 3px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# 兼容旧版 streamlit
if hasattr(st, "rerun"):
    RERUN = st.rerun
else:
    RERUN = st.experimental_rerun

# =========================
# 结果图片映射（避免中文文件名）
# 需要保证 images 文件夹里有这些图片
# =========================
IMAGE_MAP = {
    "A": "A.png",
    "B": "B.png",
    "C": "C.png",
    "F": "F.png",
    "G": "G.png",
    "H": "H.png",
    "巡演特种兵": "tour.png",
    "潜伏型抢票机器人": "stealth.png",
    "LLDG": "lldg.png"
}

# =========================
# 读取数据
# =========================
questions_df = load_questions().reset_index(drop=True)
scoring_df = load_scoring()
personas = load_personas()

OPTION_MAP = {
    "A": "opt_a",
    "B": "opt_b",
    "C": "opt_c",
    "D": "opt_d",
}

# =========================
# session_state 初始化
# =========================
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "result_code" not in st.session_state:
    st.session_state.result_code = None

if "result_scores" not in st.session_state:
    st.session_state.result_scores = None


# =========================
# 结果页模式
# =========================
if st.session_state.show_result:
    result_code = st.session_state.result_code
    persona = personas.get(result_code)

    if persona is None:
        st.error(f"未找到对应人格文案（result_code={result_code}）")
    else:
        image_file = IMAGE_MAP.get(result_code)

        if image_file is None:
            st.error(f"未配置图片映射：{result_code}")
        else:
            image_path = f"images/{image_file}"

            try:
                # ===== 只显示图片 =====
                st.image(image_path, use_column_width=True)
            except Exception:
                st.error(f"缺少图片文件：{image_path}")

    # ===== 重新测试按钮 =====
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    if st.button("重新测试"):
        st.session_state.current_index = 0
        st.session_state.answers = {}
        st.session_state.show_result = False
        st.session_state.result_code = None
        st.session_state.result_scores = None
        RERUN()

    st.stop()

# =========================
# 答题页模式
# =========================

# 如果之前答过，默认选中原答案；否则无选中内容
# ========= 否则显示答题页 =========
total_questions = len(questions_df)
idx = st.session_state.current_index
row = questions_df.iloc[idx]

qid = str(row["qid"]).strip()
question = row["question"]

st.title("LSTI - 刘恋粉丝人格测试")
st.caption("DEPLOY CHECK 2026-04-24 v1")
st.caption(f"第 {idx + 1} / {total_questions} 题")

progress = (idx + 1) / total_questions
st.progress(progress)

st.markdown("---")
st.markdown(f"## {qid}")
st.write(question)

# 当前已选答案（如果有）
current_answer = st.session_state.answers.get(qid, None)

# ===== 选项按钮区（四个大按钮） =====
for opt in ["A", "B", "C", "D"]:
    label = row[OPTION_MAP[opt]]

    # 已选中的项前面加标记
    button_text = f"✅ {label}" if current_answer == opt else label

    if st.button(button_text, key=f"{qid}_{opt}"):
        st.session_state.answers[qid] = opt
        RERUN()

st.markdown("---")

# ===== 翻页按钮区 =====
if idx < total_questions - 1:
    col1, col2 = st.columns(2)

    with col1:
        if idx > 0:
            if st.button("← 上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

    with col2:
        if st.button("下一题 →", key=f"next_{qid}"):
            if qid not in st.session_state.answers:
                st.warning("请先选择一个选项再进入下一题。")
            else:
                st.session_state.current_index += 1
                RERUN()

else:
    col1, col2 = st.columns(2)

    with col1:
        if idx > 0:
            if st.button("← 上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

    with col2:
        if st.button("提交测试", key=f"submit_{qid}"):
            if qid not in st.session_state.answers:
                st.warning("请先完成当前题目再提交测试。")
            else:
                unanswered = [
                    str(r["qid"]).strip()
                    for _, r in questions_df.iterrows()
                    if str(r["qid"]).strip() not in st.session_state.answers
                ]

                if unanswered:
                    st.error(f"你还有 {len(unanswered)} 题未作答。")
                else:
                    scores = calculate_scores(st.session_state.answers, scoring_df)
                    result_code = determine_result(scores)

                    st.session_state.result_code = result_code
                    st.session_state.result_scores = scores
                    st.session_state.show_result = True
                    RERUN()
