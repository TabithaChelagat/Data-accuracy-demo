# Naivas Demo

A guided, live demo of an automated data-accuracy pipeline for retail branch sales. Open the page, click **Load the data**, then **Clean it**, then **Load the data again**. At each step the profit margin and the "Unmapped" sales are recalculated.

All data is practice data generated for this demo. No real Naivas data is used.

## What's in this repo
- `index.html`: the demo page (static; loads the CSVs below in the browser)
- `data/branch_sales.csv`: 3,840 messy sales lines (12 branches x 8 weeks x 40 products)
- `data/item_master.csv`, `data/supplier_costs.csv`: product list with system cost, and the supplier's latest cost
- `data/answer_key.csv`: the true values, used only to score the cleaning
- `generate_data.py`: creates the CSVs (fixed seed, same output every run)
- `clean.py`: applies the same cleaning rules as the page, prints the margin at each step and the scorecard, and writes `output/cleaned_sales.csv` and `output/review_queue.csv`

## Run it
`python3 generate_data.py && python3 clean.py` (Python 3, no extra packages). To view the page locally, serve the folder (for example `python3 -m http.server`) rather than opening the file directly, because the page fetches the CSVs.

## Mistakes planted
Code written several ways, quantities in dozens, size in litres instead of items, prices keyed ten times too high, unknown codes, negative quantities, and out-of-date system costs.

Built by Tabitha Chelagat.
