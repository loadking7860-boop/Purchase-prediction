import time
from pathlib import Path
import pandas as pd

start = time.time()

raw_path = next(Path("data/raw").glob("*.xlsx"))
print("Reading:", raw_path)
print("This takes 1-3 minutes. Do NOT press Ctrl+C.")

xls = pd.ExcelFile(raw_path)
frames = []
for s in xls.sheet_names:
    print("  reading sheet:", s, flush=True)
    frames.append(pd.read_excel(raw_path, sheet_name=s))
    print(f"  done ({time.time() - start:.0f}s elapsed)", flush=True)

df = pd.concat(frames, ignore_index=True)
df = df.rename(columns={
    "Invoice": "invoice",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "price",
    "Customer ID": "customer_id",
    "Country": "country",
})
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

out = Path("data/processed/retail_raw.pkl")
out.parent.mkdir(parents=True, exist_ok=True)
df.to_pickle(out)

print("\nSaved:", out)
print("Shape:", df.shape)
print(f"Total time: {time.time() - start:.0f}s")