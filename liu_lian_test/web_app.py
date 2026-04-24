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
    max-width: 760px;
    margin: 0 auto;
    padding-top: 1rem !important;
    padding-bottom: 0.8rem !important;
    padding-left: 1.1rem !important;
    padding-right: 1.1rem !important;

    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);

    border-radius: 22px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
}

h1 {
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
    margin-top: 0.1rem !important;
    margin-bottom: 0.4rem !important;
}

h2 {
    font-size: 1.25rem !important;
    margin-top: 0.4rem !important;
    margin-bottom: 0.55rem !important;
}

p {
    font-size: 1rem !important;
    line-height: 1.48 !important;
    margin-bottom: 0.55rem !important;
}

.stProgress {
    margin-top: 0.25rem;
    margin-bottom: 0.45rem;
}

hr {
    margin-top: 0.55rem !important;
    margin-bottom: 0.65rem !important;
    border-color: rgba(0, 0, 0, 0.10) !important;
}

button {
    width: min(100%, 390px) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    min-height: 44px !important;
    padding: 8px 14px !important;
    margin: 0 auto 7px auto !important;

    border-radius: 16px !important;
    border: 1px solid rgba(120, 140, 100, 0.22) !important;
    background: rgba(255, 255, 255, 0.92) !important;
    color: #1f241d !important;

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
    color: #1f241d !important;
}

button:hover {
    border-color: rgba(108, 132, 82, 0.55) !important;
    background: rgba(246, 250, 240, 0.98) !important;
}

button:focus {
    box-shadow: 0 0 0 0.16rem rgba(120, 150, 80, 0.18) !important;
}

/* 导航按钮单独收窄 */
div[data-testid="stHorizontalBlock"] {
    max-width: 220px !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 0.45rem !important;
    justify-content: center !important;
}

div[data-testid="stHorizontalBlock"] button {
    width: 100% !important;
    min-height: 40px !important;
    padding: 6px 8px !important;
    font-size: 0.9rem !important;
    margin-bottom: 0 !important;
}

/* 手机端 */
@media (max-width: 768px) {
    .block-container {
        max-width: 100%;
        padding-top: 0.9rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        border-radius: 20px;
    }

    h1 {
        font-size: 1.35rem !important;
        margin-bottom: 0.35rem !important;
    }

    h2 {
        font-size: 1.15rem !important;
    }

    p {
        font-size: 0.98rem !important;
        line-height: 1.45 !important;
    }

    button {
        width: min(100%, 350px) !important;
        min-height: 42px !important;
        padding: 7px 10px !important;
        font-size: 0.96rem !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="stHorizontalBlock"] {
        max-width: 200px !important;
        gap: 0.4rem !important;
    }

    div[data-testid="stHorizontalBlock"] button {
        min-height: 38px !important;
        font-size: 0.88rem !important;
        padding: 6px 7px !important;
    }
}


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

    st.title("LSTI")
    st.caption("刘恋粉丝人格测试")
    st.caption(f"第 {idx + 1} / {total_questions} 题")
    st.progress((idx + 1) / total_questions)

    st.markdown("---")

    st.markdown(f"## {qid}")
    st.write(row["question"])

    current_answer = st.session_state.answers.get(qid)

    for opt in ["A", "B", "C", "D"]:
        label = row[OPTION_MAP[opt]]

        if current_answer == opt:
            st.markdown(
                """
                <style>
                div[data-testid="stButton"]:has(button[kind="secondary"]) button {
                    transition: all 0.15s ease;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        button_text = f"{label} · 已选" if current_answer == opt else label

        if st.button(button_text, key=f"{qid}_{opt}"):
            st.session_state.answers[qid] = opt
            RERUN()

        # 选中态：用按钮后的局部样式覆盖
        if current_answer == opt:
            st.markdown(
                f"""
                <style>
                div[data-testid="stButton"]:has(button[aria-label="{button_text}"]) button {{
                    background: rgba(173, 196, 138, 0.85) !important;
                    border-color: rgba(108, 132, 82, 0.70) !important;
                    font-weight: 700 !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    if idx < total_questions - 1:
        col1, col2 = st.columns(2)

        with col1:
            if idx > 0 and st.button("上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

        with col2:
            if st.button("下一题", key=f"next_{qid}"):
                if qid not in st.session_state.answers:
                    st.warning("请选择一个选项")
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
            if st.button("提交", key=f"submit_{qid}"):
                if qid not in st.session_state.answers:
                    st.warning("先完成当前题目再提交")
                else:
                    unanswered = [qid for qid in ALL_QIDS if qid not in st.session_state.answers]

                    if unanswered:
                        st.error(f"你还有 {len(unanswered)} 题未作答。")
                    else:
                        scores = calculate_scores(st.session_state.answers, scoring_df)
                        result_code = determine_result(scores)
                        st.session_state.result_code = result_code
                        st.session_state.show_result = True
                        RERUN()

if st.session_state.show_result:
    render_result_page()
else:
    render_question_page()
