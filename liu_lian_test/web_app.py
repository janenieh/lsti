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
    max-width: 1100px;
    margin: 0 auto;
    padding-top: 1.2rem !important;
    padding-bottom: 0.8rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;

    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);

    border-radius: 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

/* =========================
   文字颜色，避免夜间模式发白
   ========================= */
html, body, .stApp,
h1, h2, h3, h4, h5,
p, span, div,
label,
[data-testid="stMarkdownContainer"],
[data-testid="stText"] {
    color: #1a1a1a !important;
}

/* =========================
   标题与正文间距
   ========================= */
h1, h2, h3 {
    margin-top: 0.1rem !important;
    margin-bottom: 0.35rem !important;
    line-height: 1.2 !important;
}

h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
}

p {
    margin-bottom: 0.45rem !important;
    line-height: 1.5 !important;
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
    width: min(100%, 520px) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    min-height: 44px !important;
    padding: 8px 12px !important;
    margin: 0 auto 6px auto !important;

    border-radius: 14px !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    background: rgba(255, 255, 255, 0.92) !important;
    color: #1a1a1a !important;

    font-size: 16px !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    text-align: center !important;
    box-sizing: border-box !important;
}

button p, button span {
    margin: 0 !important;
    width: 100% !important;
    color: #1a1a1a !important;
    text-align: center !important;
}

@media (max-width: 768px) {
    button {
        width: min(100%, 360px) !important;
        min-height: 42px !important;
        padding: 7px 10px !important;
        font-size: 15px !important;
        margin-bottom: 5px !important;
    }

    /* 只控制上一题/下一题这一类 columns 行 */
    div[data-testid="stHorizontalBlock"] {
        max-width: 230px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 0.5rem !important;
        justify-content: center !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
    }

    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important;
        min-height: 40px !important;
        padding: 6px 8px !important;
        font-size: 14px !important;
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

    # 结果图只显示图片 + 重新测试按钮
    left, center, right = st.columns([1.2, 7.6, 1.2])

    with center:
        if image_file is None:
            st.error(f"未配置图片映射：{result_code}")
        else:
            image_path = BASE_DIR / "images" / image_file
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            else:
                st.error(f"缺少图片文件：{image_path.name}")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        nav_l, restart_col, nav_r = st.columns([3, 2, 3])
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
    st.title("LSTI - 刘恋粉丝人格测试")
    st.caption(f"第 {idx + 1} / {total_questions} 题")
    st.progress((idx + 1) / total_questions)

    st.markdown("---")

    # ===== 题目主体 =====
    st.markdown(f"## {qid}")
    st.write(row["question"])

    current_answer = st.session_state.answers.get(qid)

    # ===== 选项按钮：不用 columns，避免手机端横向溢出 =====
    for opt in ["A", "B", "C", "D"]:
        label = row[OPTION_MAP[opt]]
        button_text = f"✅ {label}" if current_answer == opt else label

        if st.button(button_text, key=f"{qid}_{opt}"):
            st.session_state.answers[qid] = opt
            RERUN()

    st.markdown("---")

    # ===== 导航按钮 =====
    if idx < total_questions - 1:
        col1, col2 = st.columns(2)

        with col1:
            if idx > 0 and st.button("上一题", key=f"prev_{qid}"):
                st.session_state.current_index -= 1
                RERUN()

        with col2:
            if st.button("下一题", key=f"next_{qid}"):
                if qid not in st.session_state.answers:
                    st.warning("请先选一个选项再点下一题")
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
