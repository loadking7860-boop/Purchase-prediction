import time
from pathlib import Path
import pandas as pd

RAW_CACHE = Path("data/processed/retail_raw.pkl")
OUT_PATH = Path("data/processed/clean_transactions.parquet")

# Stock codes that are not real products (decided from the EDA)
NON_PRODUCT = {
    "POST", "DOT", "M", "C2", "ADJUST", "ADJUST2", "BANK CHARGES",
    "D", "AMAZONFEE", "S", "B", "TEST001", "TEST002",
}


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the cleaning rules decided in the EDA (notebook 01)."""
    df = df.copy()

    # Mixed int/str columns break Parquet, so make them plain strings
    df["invoice"] = df["invoice"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)

    log = [("start", len(df), 0)]

    def step(name, mask_keep):
        nonlocal df
        before = len(df)
        df = df[mask_keep(df)]
        log.append((name, len(df), before - len(df)))

    step("drop missing customer_id", lambda d: d["customer_id"].notna())
    step("drop cancellation invoices (start with C)", lambda d: ~d["invoice"].str.startswith("C"))
    step("drop quantity <= 0", lambda d: d["quantity"] > 0)
    step("drop price <= 0", lambda d: d["price"] > 0)

    df = df.copy()
    df["customer_id"] = df["customer_id"].astype("int64")
    df["revenue"] = df["quantity"] * df["price"]

    # Flag (do NOT drop) non-product codes. We decide what to do with them in Milestone 4.
    df["is_non_product"] = df["stock_code"].str.upper().isin(NON_PRODUCT)

    df = df.sort_values("invoice_date").reset_index(drop=True)

    print("Cleaning log:")
    for name, remaining, removed in log:
        print(f"  {name:<45} removed {removed:>9,}   remaining {remaining:>9,}")
    return df


def validate(df: pd.DataFrame) -> None:
    assert df["customer_id"].notna().all(), "null customer_id found"
    assert (df["quantity"] > 0).all(), "non-positive quantity found"
    assert (df["price"] > 0).all(), "non-positive price found"
    assert not df["invoice"].str.startswith("C").any(), "cancellation invoice found"
    print("All validation checks passed.")


if __name__ == "__main__":
    start = time.time()
    raw = pd.read_pickle(RAW_CACHE)
    clean = clean_transactions(raw)
    validate(clean)

    clean.to_parquet(OUT_PATH, index=False)

    print(f"\nSaved: {OUT_PATH}")
    print(f"Rows: {len(clean):,}")
    print(f"Customers: {clean['customer_id'].nunique():,}")
    print(f"Date range: {clean['invoice_date'].min()} -> {clean['invoice_date'].max()}")
    print(f"Non-product rows flagged: {clean['is_non_product'].sum():,}")
    print("Top non-product codes:")
    print(clean.loc[clean["is_non_product"], "stock_code"].value_counts().head(10))
    print(f"Done in {time.time() - start:.0f}s")