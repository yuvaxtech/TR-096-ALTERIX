import pandas as pd

def compute_fairness(df: pd.DataFrame):
    """
    Compute selection rates and disparate impact ratio.
    Disparate Impact Ratio = (selection rate of group) / (selection rate of highest group)
    Ratio < 0.8 → potential adverse impact (80% rule, EEOC guideline)
    """
    df = df.copy()
    if "shortlisted" in df.columns:
        df["shortlist_rate"] = df["shortlisted"] / df["applied"]
    else:
        df["shortlist_rate"] = 0.0

    if "hired" in df.columns:
        df["hire_rate"] = df["hired"] / df["applied"]
    else:
        df["hire_rate"] = 0.0

    max_hire_rate = df["hire_rate"].max()
    if max_hire_rate > 0:
        df["disparate_impact"] = df["hire_rate"] / max_hire_rate
    else:
        df["disparate_impact"] = 1.0

    df["shortlist_rate"] = df["shortlist_rate"].round(3)
    df["hire_rate"]      = df["hire_rate"].round(3)
    df["disparate_impact"] = df["disparate_impact"].round(3)

    return df


def overall_fairness_verdict(df_result: pd.DataFrame):
    """Return Fair / Potential Bias based on 80% rule."""
    if "disparate_impact" not in df_result.columns or df_result.empty:
        return ("fair", 1.0)
    min_di = df_result["disparate_impact"].min()
    return ("fair", min_di) if min_di >= 0.80 else ("biased", min_di)
