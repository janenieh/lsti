from pathlib import Path

import streamlit as st
from app import (
    load_questions,
    load_scoring,
    load_personas,
    calculate_scores,
    determine_result,
)

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="LSTI - 刘恋粉丝人格测试",
    page_icon="🎤",
    layout="centered"
)

if hasattr(st, "rerun"):
    RERUN = st.rerun
else:
    RERUN = st.experimental_rerun

IMAGE_MAP = {
    "A": "A.png",
    "B": "B.png",
    "C": "C.png",
    "F": "F.png",
    "G": "G.png",
    "H": "H.png",
    "巡演特种兵": "tour.png",
    "潜伏型抢票机器人": "stealth.png",
    "LLDG": "lldg.png",
}

OPTION_MAP = {
    "A": "opt_a",
    "B": "opt_b",
    "C": "opt_c",
    "D": "opt_d",
}

st.markdown("""
<style>
/* ===== 隐藏 Streamlit 默认元素 ===== */
header[data-testid="stHeader"] {
    display: none !important;
}
div[data-testid="stToolbar"] {
    display: none !important;
}
div[data-testid="stDecoration"] {
    display: none !important;
}
#MainMenu {
    visibility: hidden !important;
}
footer {
    visibility: hidden !important;
}
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* ===== 全局暗绿背景 ===== */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background:
        radial-gradient(circle at top right, rgba(232, 201, 135, 0.12), transparent 28%),
        radial-gradient(circle at bottom left, rgba(232, 201, 135, 0.07), transparent 30%),
        linear-gradient(180deg, #071b17 0%, #0a201b 45%, #061713 100%);
}

/* ===== 主卡片 ===== */
.block-container {
    max-width: 720px;
    margin: 0 auto;
    padding-top: 1rem !important;
    padding-bottom: 0.85rem !important;
    padding-left: 1.05rem !important;
    padding-right: 1.05rem !important;

    background: rgba(5, 22, 19, 0.92);
    border: 1px solid rgba(232, 201, 135, 0.42);
    border-radius: 20px;
    box-shadow:
        0 0 0 1px rgba(232, 201, 135, 0.10),
        0 14px 36px rgba(0, 0, 0, 0.42);
}

/* ===== 全局文字颜色 ===== */
html, body, .stApp,
h1, h2, h3, h4, h5,
p, span, div,
label,
[data-testid="stMarkdownContainer"],
[data-testid="stText"] {
    color: #f1d99a !important;
}

/* ===== 标题 ===== */
.brand-row {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    margin-bottom: 0.18rem;
}

.brand-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    line-height: 1;
    color: #f4d993;
}

.brand-cn {
    font-size: 1.35rem;
    font-weight: 650;
    letter-spacing: 0.04em;
    color: #f1d99a;
}

.brand-subtitle {
    font-size: 0.78rem;
    letter-spacing: 0.28em;
    color: rgba(232, 201, 135, 0.68);
    margin-bottom: 0.75rem;
}

/* ===== 进度 ===== */
.progress-text {
    font-size: 0.95rem;
    letter-spacing: 0.08em;
    color: #e8c987;
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
}

.stProgress {
    margin-top: 0.15rem;
    margin-bottom: 0.55rem;
}

.stProgress > div > div {
    background-color: rgba(232, 201, 135, 0.16) !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #f1d99a 0%, #c89f55 100%) !important;
}

/* ===== 分割线 ===== */
hr {
    border-color: rgba(232, 201, 135, 0.32) !important;
    margin-top: 0.65rem !important;
    margin-bottom: 0.75rem !important;
}

/* ===== 题号与题干 ===== */
.qid-title {
    font-size: 1.75rem;
    font-weight: 760;
    line-height: 1.15;
    color: #f4d993;
    margin: 0.25rem 0 0.5rem 0;
    letter-spacing: 0.04em;
}

.question-text {
    font-size: 1.03rem;
    line-height: 1.58;
    color: #f3dfad;
    margin-bottom: 0.85rem;
}

/* ===== 按钮：暗金线框风格 ===== */
button {
    width: min(100%, 420px) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    min-height: 48px !important;
    padding: 8px 14px !important;
    margin: 0 auto 10px auto !important;

    border-radius: 8px !important;
    border: 1px solid rgba(232, 201, 135, 0.55) !important;
    background: rgba(7, 28, 24, 0.92) !important;
    color: #f3dfad !important;

    font-size: 1rem !important;
    line-height: 1.35 !important;
    letter-spacing: 0.03em;
    white-space: normal !important;
    text-align: center !important;
    box-sizing: border-box !important;

    box-shadow:
        inset 0 0 12px rgba(232, 201, 135, 0.045),
        0 0 0 1px rgba(232, 201, 135, 0.03);
}

button p, button span {
    margin: 0 !important;
    width: 100% !important;
    color: #f3dfad !important;
    text-align: center !important;
}

button:hover {
    background: rgba(15, 42, 35, 0.98) !important;
    border-color: rgba(241, 217, 154, 0.9) !important;
}

button:focus {
    box-shadow:
        inset 0 0 12px rgba(232, 201, 135, 0.08),
        0 0 0 0.14rem rgba(232, 201, 135, 0.16) !important;
}

/* ===== 导航按钮单独收窄居中 ===== */
div[data-testid="stHorizontalBlock"] {
    max-width: 200px !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 0.45rem !important;
    justify-content: center !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
}

div[data-testid="stHorizontalBlock"] button {
    width: 100% !important;
    min-height: 38px !important;
    padding: 6px 8px !important;
    font-size: 0.88rem !important;
    margin-bottom: 0 !important;
}

/* ===== 提示框 ===== */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    background: rgba(232, 201, 135, 0.12) !important;
    border: 1px solid rgba(232, 201, 135, 0.28) !important;
}

/* ===== 手机端 ===== */
@media (max-width: 768px) {
    .block-container {
        max-width: 100%;
        padding-top: 0.85rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        border-radius: 18px;
    }

    .brand-row {
        gap: 0.55rem;
        margin-bottom: 0.12rem;
    }

    .brand-title {
        font-size: 2.05rem;
        letter-spacing: 0.04em;
    }

    .brand-cn {
        font-size: 1.02rem;
        letter-spacing: 0.02em;
    }

    .brand-subtitle {
        font-size: 0.65rem;
        letter-spacing: 0.22em;
        margin-bottom: 0.65rem;
    }

    .progress-text {
        font-size: 0.86rem;
        margin-bottom: 0.22rem;
    }

    .qid-title {
        font-size: 1.48rem;
        margin-top: 0.2rem;
        margin-bottom: 0.42rem;
    }

    .question-text {
        font-size: 1rem;
        line-height: 1.48;
        margin-bottom: 0.7rem;
    }

    button {
        width: min(100%, 360px) !important;
        min-height: 46px !important;
        padding: 7px 10px !important;
        font-size: 0.96rem !important;
        margin-bottom: 9px !important;
        border-radius: 8px !important;
    }

    div[data-testid="stHorizontalBlock"] {
    max-width: 220px !important;
    margin: 0 auto !important;
    display: flex !important;
    justify-content: center !important;
    gap: 0.4rem !important;
    }

    /* 额外稳定（防止某些版本偏移） */
    div[data-testid="stHorizontalBlock"] > div {
    display: flex;
    justify-content: center;
    }

    div[data-testid="stHorizontalBlock"] button {
        min-height: 38px !important;
        font-size: 0.86rem !important;
        padding: 6px 7px !important;
    }

    hr {
        margin-top: 0.55rem !important;
        margin-bottom: 0.65rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_questions():
    return load_questions().reset_index(drop=True)


@st.cache_data
def get_scoring():
    return load_scoring()


@st.cache_data
def get_personas():
    return load_personas()


questions_df = get_questions()
scoring_df = get_scoring()
personas = get_personas()

ALL_QIDS = questions_df["qid"].astype(str).str.strip().tolist()

st.session_state.setdefault("current_index", 0)
st.session_state.setdefault("answers", {})
st.session_state.setdefault("show_result", False)
st.session_state.setdefault("result_code", None)


def reset_test():
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.show_result = False
    st.session_state.result_code = None


def render_result_page():
    result_code = st.session_state.result_code
    image_file = IMAGE_MAP.get(result_code)

    if image_file is None:
        st.error(f"未配置图片映射：{result_code}")
    else:
        image_path = BASE_DIR / "images" / image_file
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.error(f"缺少图片文件：{image_path.name}")

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col2:
        if st.button("重新测试", key="restart_result"):
            reset_test()
            RERUN()

    st.stop()


def render_question_page():
    total_questions = len(questions_df)
    idx = st.session_state.current_index
    row = questions_df.iloc[idx]
    qid = str(row["qid"]).strip()

    # ===== 页头 =====
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-title">LSTI</div>
            <div class="brand-cn">刘恋粉丝人格测试</div>
        </div>
        <div class="brand-subtitle">LIAN SYSTEM TYPE INDICATOR</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='progress-text'>第 {idx + 1} / {total_questions} 题</div>",
        unsafe_allow_html=True
    )
    st.progress((idx + 1) / total_questions)

    st.markdown("---")

    # ===== 题目 =====
    st.markdown(f"<div class='qid-title'>{qid}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='question-text'>{row['question']}</div>",
        unsafe_allow_html=True
    )

    # ===== 选项 =====
    current_answer = st.session_state.answers.get(qid)

    for opt in ["A", "B", "C", "D"]:
        label = row[OPTION_MAP[opt]]
        button_text = f"🦋 {label}" if current_answer == opt else label

        if st.button(button_text, key=f"{qid}_{opt}"):
            st.session_state.answers[qid] = opt
            RERUN()

    st.markdown("---")

    # ===== 导航 =====
    if idx < total_questions - 1:
        col1, col2 = st.columns(2)

        with col1:
            if idx > 0 and st.button("← 上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

        with col2:
            if st.button("下一题 →", key=f"next_{qid}"):
                if qid not in st.session_state.answers:
                    st.warning("请先选一个选项再点下一题")
                else:
                    st.session_state.current_index += 1
                    RERUN()

    else:
        col1, col2 = st.columns(2)

        with col1:
            if idx > 0 and st.button("← 上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

        with col2:
            if st.button("提交", key=f"submit_{qid}"):
                if qid not in st.session_state.answers:
                    st.warning("先完成当前题目再提交")
                else:
                    unanswered = [
                        q for q in ALL_QIDS
                        if q not in st.session_state.answers
                    ]

                    if unanswered:
                        st.error(f"你还有 {len(unanswered)} 题未作答。")
                    else:
                        scores = calculate_scores(
                            st.session_state.answers,
                            scoring_df
                        )
                        result_code = determine_result(scores)

                        st.session_state.result_code = result_code
                        st.session_state.show_result = True
                        RERUN()


if st.session_state.show_result:
    render_result_page()
else:
    render_question_page()
