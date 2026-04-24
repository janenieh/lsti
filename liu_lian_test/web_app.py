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
    layout="wide"
)

# 新旧版兼容
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
    "LLDG": "lldg.png"
}

OPTION_MAP = {
    "A": "opt_a",
    "B": "opt_b",
    "C": "opt_c",
    "D": "opt_d",
}

st.markdown("""
<style>
/* =========================
   隐藏 Streamlit / Cloud 顶部工具条
   ========================= */
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

/* =========================
   全局背景
   ========================= */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background-color: #adc48a;
}

/* =========================
   页面主卡片
   ========================= */
.block-container {
    max-width: 720px;
    margin: 0 auto;
    padding-top: 0.75rem !important;
    padding-bottom: 0.65rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;

    background: rgba(255, 255, 255, 0.80);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);

    border-radius: 20px;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.07);
}

.brand-title {
    font-size: 2.15rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    line-height: 1.05;
    margin: 0 0 0.1rem 0;
    color: #1a1a1a;
}

.brand-subtitle {
    font-size: 0.95rem;
    font-weight: 500;
    color: rgba(26, 26, 26, 0.62);
    margin-bottom: 0.65rem;
}

.progress-text {
    font-size: 0.88rem;
    color: rgba(26, 26, 26, 0.58);
    margin-bottom: 0.25rem;
}

.stProgress {
    margin-top: 0.15rem;
    margin-bottom: 0.45rem;
}

hr {
    margin-top: 0.45rem !important;
    margin-bottom: 0.5rem !important;
    border-color: rgba(0, 0, 0, 0.10) !important;
}

.qid-title {
    font-size: 1.65rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0.25rem 0 0.45rem 0;
    color: #1a1a1a;
}

.question-text {
    font-size: 1.02rem;
    line-height: 1.45;
    margin-bottom: 0.65rem;
    color: #1a1a1a;
}

/* 进度条 */
.stProgress {
    margin-top: 0.25rem;
    margin-bottom: 0.6rem;
}

/* 分割线 */
hr {
    margin-top: 0.55rem !important;
    margin-bottom: 0.7rem !important;
    border-color: rgba(0, 0, 0, 0.12) !important;
}

/* =========================
   按钮统一样式
   ========================= */
button {
    width: min(100%, 390px) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    min-height: 48px !important;
    padding: 8px 14px !important;
    margin: 0 auto 12px auto !important;

    border-radius: 18px !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    background: rgba(255, 255, 255, 0.94) !important;
    color: #1a1a1a !important;

    font-size: 1rem !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    text-align: center !important;
    box-sizing: border-box !important;
}

button p, button span {
    margin: 0 !important;
    width: 100% !important;
    text-align: center !important;
    color: #1a1a1a !important;
}

button:hover {
    border-color: rgba(120, 140, 100, 0.28) !important;
    background: rgba(255, 255, 255, 0.98) !important;
}

button:focus {
    box-shadow: 0 0 0 0.14rem rgba(120, 150, 80, 0.15) !important;
}

@media (max-width: 768px) {
    .block-container {
        max-width: 100%;
        padding-top: 0.65rem !important;
        padding-bottom: 0.6rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        border-radius: 18px;
    }

    .brand-title {
        font-size: 1.9rem;
        letter-spacing: 0.03em;
    }

    .brand-subtitle {
        font-size: 0.88rem;
        margin-bottom: 0.55rem;
    }

    .progress-text {
        font-size: 0.82rem;
    }

    .qid-title {
        font-size: 1.45rem;
        margin-top: 0.2rem;
        margin-bottom: 0.35rem;
    }

    .question-text {
        font-size: 1rem;
        line-height: 1.42;
        margin-bottom: 0.55rem;
    }

    hr {
        margin-top: 0.38rem !important;
        margin-bottom: 0.45rem !important;
    }
}
    button {
        width: min(100%, 360px) !important;
        min-height: 46px !important;
        padding: 7px 10px !important;
        font-size: 0.98rem !important;
        margin-bottom: 10px !important;
        border-radius: 16px !important;
    }

    div[data-testid="stHorizontalBlock"] {
        max-width: 200px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 0.4rem !important;
        justify-content: center !important;
    }

    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important;
        min-height: 38px !important;
        padding: 6px 7px !important;
        font-size: 0.88rem !important;
        margin-bottom: 0 !important;
    }
}

    h1 {
        font-size: 1.55rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        font-size: 1.05rem !important;
    }

    p {
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }

    button {
        min-height: 44px !important;
        padding: 7px 10px !important;
        margin-bottom: 4px !important;
        font-size: 15px !important;
        border-radius: 14px !important;
    }

    /* 强制 columns 横向排列，避免上一题/下一题上下堆叠 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 0.45rem !important;
        align-items: stretch !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
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

    restart_left, restart_col, restart_right = st.columns([2.5, 2, 2.5])
    with restart_col:
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
   st.markdown("<div class='brand-title'>LSTI</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-subtitle'>刘恋粉丝人格测试</div>", unsafe_allow_html=True)
st.markdown(f"<div class='progress-text'>第 {idx + 1} / {total_questions} 题</div>", unsafe_allow_html=True)
st.progress((idx + 1) / total_questions)

    st.markdown("---")

    # ===== 题目 =====
    st.markdown(f"<div class='qid-title'>{qid}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='question-text'>{row['question']}</div>", unsafe_allow_html=True)

    # ===== 当前选中答案 =====
    current_answer = st.session_state.answers.get(qid)

    # ===== 选项按钮 =====
    for opt in ["A", "B", "C", "D"]:
        label = row[OPTION_MAP[opt]]

        # 选中显示 ✅
        if current_answer == opt:
            button_text = f"✅ {label}"
        else:
            button_text = label

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
                    st.warning("请先完成当前题目")
                else:
                    st.session_state.current_index += 1
                    RERUN()

    else:
        col1, col2 = st.columns(2)

        with col1:
            if idx > 0 and st.button("上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

        with col2:
            if st.button("提交测试", key=f"submit_{qid}"):
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
