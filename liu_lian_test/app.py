import json
import random
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

DIMS = ["A", "B", "C", "D", "E", "F", "G", "H"]

PERSONA_MAP = {
    "A": "A",
    "B": "B",
    "C": "C",
    "F": "F",
    "G": "G",
    "H": "H",
}


def load_questions() -> pd.DataFrame:
    df = pd.read_csv(BASE_DIR / "questions.csv")
    df["qid"] = df["qid"].astype(str).str.strip()
    return df


def load_scoring() -> pd.DataFrame:
    df = pd.read_csv(BASE_DIR / "scoring.csv")
    df = df.dropna(subset=["qid", "opt"])

    df["qid"] = df["qid"].astype(str).str.strip()
    df["opt"] = df["opt"].astype(str).str.strip().str.upper()
    df["main_dim"] = df["main_dim"].astype(str).str.strip()

    if "sub_dim" in df.columns:
        df["sub_dim"] = df["sub_dim"].astype(str).str.strip()

    return df


def load_personas() -> dict:
    with open(BASE_DIR / "personas.json", "r", encoding="utf-8") as f:
        return json.load(f)


def init_scores() -> dict:
    return {dim: 0 for dim in DIMS}


def apply_answer(scores: dict, row: pd.Series) -> None:
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


def calculate_scores(answers: dict, scoring_df: pd.DataFrame) -> dict:
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

        apply_answer(scores, match.iloc[0])

    return scores


def get_sorted_dims(scores: dict) -> list:
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def check_lldg(scores: dict) -> bool:
    mean_score = sum(scores.values()) / len(scores)
    sorted_items = get_sorted_dims(scores)

    if len(sorted_items) < 3:
        return False

    top2_score = sorted_items[1][1]
    top3_score = sorted_items[2][1]

    return (
        scores["D"] >= top3_score and
        scores["F"] >= mean_score and
        scores["A"] >= mean_score and
        scores["E"] >= mean_score
    )


def resolve_tie(candidates: list[str]) -> str:
    return random.choice(candidates)


def determine_result(scores: dict) -> str:
    if check_lldg(scores):
        return "LLDG"

    max_score = max(scores.values())
    top_candidates = [dim for dim, score in scores.items() if score == max_score]
    top1_dim = resolve_tie(top_candidates)

    if top1_dim == "D":
        if scores["E"] >= scores["D"] * 0.6:
            return "巡演特种兵"
        return "潜伏型抢票机器人"

    if top1_dim == "E":
        mean_score = sum(scores.values()) / len(scores)
        if scores["D"] >= mean_score:
            return "巡演特种兵"
        return "潜伏型抢票机器人"

    return PERSONA_MAP.get(top1_dim, top1_dim)


def print_result(result_code: str, personas: dict, scores: dict) -> None:
    print("\n========== 测试结果 ==========")

    persona = personas.get(result_code)
    if persona is None:
        print(f"结果：未找到对应人格文案（result_code={result_code}）")
    else:
        print(f"结果：{persona.get('name', result_code)}")
        print(f"一句话：{persona.get('summary', '')}")

    print("\n8维分数：")
    for dim, score in scores.items():
        print(f"{dim}: {score}")


def validate_answers(answers: dict, questions_df: pd.DataFrame) -> None:
    valid_qids = set(questions_df["qid"].astype(str).str.strip().tolist())

    for qid, opt in answers.items():
        if qid not in valid_qids:
            raise ValueError(f"答案文件中存在未知题号：{qid}")
        if str(opt).strip().upper() not in ["A", "B", "C", "D"]:
            raise ValueError(f"答案文件中 {qid} 的答案非法：{opt}")


def run_from_answer_file(answer_file: str) -> None:
    questions_df = load_questions()
    scoring_df = load_scoring()
    personas = load_personas()

    with open(answer_file, "r", encoding="utf-8") as f:
        answers = json.load(f)

    validate_answers(answers, questions_df)

    scores = calculate_scores(answers, scoring_df)
    result_code = determine_result(scores)
    print_result(result_code, personas, scores)


def main() -> None:
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
        run_from_answer_file(sys.argv[1])
    else:
        main()
