import json
import sys
import random
import pandas as pd

# 固定 8 个维度
DIMS = ["A", "B", "C", "D", "E", "F", "G", "H"]

# 非 D 维度的人格映射
# 注意：D / E 不直接映射，D 需要结合 E 分叉；E 不能单独作为最终人格输出
PERSONA_MAP = {
    "A": "A",
    "B": "B",
    "C": "C",
    "F": "F",
    "G": "G",
    "H": "H"
}


def load_questions():
    return pd.read_csv("questions.csv")


def load_scoring():
    df = pd.read_csv("scoring.csv")
    # 自动忽略空行/缺题号选项的行
    df = df.dropna(subset=["qid", "opt"])
    # 清理字符串空格，避免 "Q01 " 这类问题
    df["qid"] = df["qid"].astype(str).str.strip()
    df["opt"] = df["opt"].astype(str).str.strip().str.upper()
    df["main_dim"] = df["main_dim"].astype(str).str.strip()
    if "sub_dim" in df.columns:
        df["sub_dim"] = df["sub_dim"].astype(str).str.strip()
    return df


def load_personas():
    with open("personas.json", "r", encoding="utf-8") as f:
        return json.load(f)


def init_scores():
    return {dim: 0 for dim in DIMS}


def apply_answer(scores, row):
    """
    主维度：+weight
    副维度：固定 +1（如果存在）
    """
    main_dim = row["main_dim"]
    weight = int(row["weight"])

    sub_dim = None
    if "sub_dim" in row and pd.notna(row["sub_dim"]):
        sub_dim_raw = str(row["sub_dim"]).strip()
        if sub_dim_raw and sub_dim_raw.lower() != "nan":
            sub_dim = sub_dim_raw

    scores[main_dim] += weight
    if sub_dim:
        scores[sub_dim] += 1


def calculate_scores(answers, scoring_df):
    """
    answers: dict，如 {"Q01":"A", "Q02":"C"}
    """
    scores = init_scores()

    for qid, opt in answers.items():
        qid = str(qid).strip()
        opt = str(opt).strip().upper()

        match = scoring_df[
            (scoring_df["qid"] == qid) &
            (scoring_df["opt"] == opt)
        ]

        if match.empty:
            raise ValueError(f"没有找到 {qid} - {opt} 的计分规则")

        row = match.iloc[0]
        apply_answer(scores, row)

    return scores


def get_sorted_dims(scores):
    """
    返回按分数从高到低排序后的列表：
    [('C', 18), ('G', 16), ...]
    """
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def check_lldg(scores):
    """
    LLDG 彩蛋触发规则：
    - D 在 Top2
    - F 在 Top3
    - A >= 平均值
    - E >= 平均值
    """
    mean_score = sum(scores.values()) / len(scores)
    sorted_items = get_sorted_dims(scores)

    top2_score = sorted_items[1][1]
    top3_score = sorted_items[2][1]

    if (
        scores["D"] >= top2_score and
        scores["F"] >= top3_score and
        scores["A"] >= mean_score and
        scores["E"] >= mean_score
    ):
        return True

    return False


def resolve_tie(candidates):
    """
    同分随机打破平局
    """
    return random.choice(candidates)


def determine_result(scores):
    """
    返回最终人格代码或人格名：
    - A/B/C/F/G/H 返回对应代码（再去 personas.json 取文案）
    - D 分叉为“巡演特种兵”或“潜伏型抢票机器人”
    - E 不能直接输出，也要折回线下人格
    - LLDG 优先级最高
    """
    # 先看彩蛋
    if check_lldg(scores):
        return "LLDG"

    # 找最高分（允许同分）
    max_score = max(scores.values())
    top_candidates = [dim for dim, score in scores.items() if score == max_score]
    top1_dim = resolve_tie(top_candidates)

    # D 要结合 E 分叉
    if top1_dim == "D":
        if scores["E"] >= scores["D"] * 0.6:
            return "巡演特种兵"
        else:
            return "潜伏型抢票机器人"

    # E 不能直接作为最终人格输出
    # 折回线下人格：
    # D 较高 → 巡演特种兵
    # 否则 → 潜伏型抢票机器人
    if top1_dim == "E":
        mean_score = sum(scores.values()) / len(scores)
        if scores["D"] >= mean_score:
            return "巡演特种兵"
        else:
            return "潜伏型抢票机器人"

    # 其他维度直接映射
    return PERSONA_MAP.get(top1_dim, top1_dim)


def print_result(result_code, personas, scores):
    print("\n========== 测试结果 ==========")

    persona = personas.get(result_code)

    if persona is None:
        print(f"结果：未找到对应人格文案（result_code={result_code}）")
    else:
        print(f"结果：{persona.get('name', result_code)}")
        print(f"一句话：{persona.get('summary', '')}")


def validate_answers(answers, questions_df):
    """
    简单校验答案文件里的题号是否合法
    """
    valid_qids = set(questions_df["qid"].astype(str).str.strip().tolist())

    for qid, opt in answers.items():
        if qid not in valid_qids:
            raise ValueError(f"答案文件中存在未知题号：{qid}")
        if str(opt).strip().upper() not in ["A", "B", "C", "D"]:
            raise ValueError(f"答案文件中 {qid} 的答案非法：{opt}")


def run_from_answer_file(answer_file):
    questions_df = load_questions()
    scoring_df = load_scoring()
    personas = load_personas()

    with open(answer_file, "r", encoding="utf-8") as f:
        answers = json.load(f)

    validate_answers(answers, questions_df)

    scores = calculate_scores(answers, scoring_df)
    result_code = determine_result(scores)
    print_result(result_code, personas, scores)


def main():
    questions_df = load_questions()
    scoring_df = load_scoring()
    personas = load_personas()

    answers = {}

    for _, row in questions_df.iterrows():
        qid = str(row["qid"]).strip()
        print(f"\n{qid}. {row['question']}")
        print(f"A. {row['opt_a']}")
        print(f"B. {row['opt_b']}")
        print(f"C. {row['opt_c']}")
        print(f"D. {row['opt_d']}")

        while True:
            ans = input("请选择 A / B / C / D：").strip().upper()
            if ans in ["A", "B", "C", "D"]:
                answers[qid] = ans
                break
            print("输入无效，请重新输入。")

    scores = calculate_scores(answers, scoring_df)
    result_code = determine_result(scores)
    print_result(result_code, personas, scores)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        answer_file = sys.argv[1]
        run_from_answer_file(answer_file)
    else:
        main()