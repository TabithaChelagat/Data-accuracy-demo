# Naivas Demo

From messy branch data to trusted commercial metrics. A single static page that generates synthetic branch sales, product-list and supplier-cost data in the browser (fixed seed), plants known defects, runs a rule-based cleaning pipeline, and reports the same sales before and after cleaning.

- Defects planted: code spelling variants, quantities in dozens, litres-versus-millilitres unit mix-ups, prices keyed ten times too high, unknown codes, negative quantities, and supplier costs that differ from the system cost
- Pipeline: code normalisation, unit standardising, price check against the product list, supplier-cost override, review queue for anything unsafe to guess
- Measured: recall, precision and exact-fix rate against the planted truth

All data is synthetic. No real Naivas data is used.

Deploy: import this repo in Vercel as a static project (no build step).

Built by Tabitha Chelagat.
