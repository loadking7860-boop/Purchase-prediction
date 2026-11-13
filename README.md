\# Customer Purchase Prediction Platform



Predicts which customers are likely to purchase again in the next 90 days,

so marketing can target the top 20% most probable buyers.



\## Dataset

\- \*\*Source:\*\* \[Online Retail II, UCI ML Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

\- \*\*Licence:\*\* Research/educational use (see UCI page)

\- \*\*Download:\*\* Place `online\_retail\_II.xlsx` in `data/raw/` (not committed to git)



\## Setup

```bash

python -m venv venv

source venv/bin/activate        # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

```



\## Status

\- \[x] Milestone 1: Environment \& data inspection

\- \[x] Milestone 2: EDA

\- \[x] Milestone 3: Cleaning

\- \[ ] Milestone 4: SQL features

\- \[ ] Milestone 5: ML models

\- \[ ] Milestone 6: Evaluation

\- \[ ] Milestone 7: FastAPI

\- \[ ] Milestone 8: Tests

\- \[ ] Milestone 9: Dashboard

\- \[ ] Milestone 10: Docker

## Data cleaning rules



Run `python src/build\_cache.py` once, then `python src/clean.py`.



| Rule | Rows removed | Reason |

|---|---|---|

| Missing Customer ID | 243,007 | Cannot be used for customer-level modelling |

| Cancellation invoices (start with C) | 18,744 | Model predicts clean purchases, not returns |

| Quantity <= 0 | 0 | All negatives with a customer were already cancellations |

| Price <= 0 | 71 | Internal or free lines |



Result: 805,549 rows, 5,878 customers. Duplicate rows (3.22% of raw) are kept because they do not change a did-they-buy target. Non-product codes (POST, M, C2, ADJUST, BANK CHARGES, DOT, TEST001, TEST002, D, ADJUST2) are flagged in `is\_non\_product`, not removed.

