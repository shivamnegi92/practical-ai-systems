# Catalog data and taxonomy

The public-facing catalog currently lives in the README for easy browsing. This directory contains stable source configuration and the reviewed input format used for the managed recent-discoveries section.

- `trend-sources.json` — discovery sources and what signals they can provide.
- `trend-additions.json` — temporary/reviewed structured additions consumed by `scripts/catalog_update.py`; it starts empty. Only entries with verified license, screened origin, current unarchived status, dated trend evidence, and non-duplicate URL pass validation.

The skill should not turn a weekly search into a firehose. Discovery reports live in `/updates/`; only user-approved additions belong in the catalog.
