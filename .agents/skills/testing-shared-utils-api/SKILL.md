---
name: testing-shared-utils-api
description: Test the crispy-couscous FastAPI backend end-to-end, especially refactors of shared helpers (find_by_id, find_by_attr, paginate, extract_product_fields). Use when verifying backend service/utility changes via HTTP endpoints.
---

# Testing crispy-couscous (产品B) FastAPI backend

Local-only FastAPI app, JSON file storage under `data/`, no DB and no API key required to boot.

## Setup / boot
```bash
pip install -r requirements.txt
python3 -m src.api.server   # serves 0.0.0.0:8000
curl -s http://localhost:8000/health   # {"status":"healthy",...}
```
Run the server in the background and tail `/tmp/server.log` (or wherever you redirect) to scan for runtime
errors — refactor bugs (e.g. a missing import) surface as `NameError`/traceback there, NOT as a boot failure,
because endpoints import lazily-used helpers only when hit.

## Testing is shell-based (curl), not UI
There is no frontend. Do NOT record. Exercise each helper through a real endpoint and collect curl output as text evidence.

## Data facts that matter
- Persisted JSON (`data/`): `product_knowledge` (~3), `listing_packages` (~2), `api_providers` (~9 seeded).
- **Seeded id keys are NOT `id`**: providers use `provider_id` (e.g. `openai_text`), call records use `call_id`,
  packages use `id`. A naive `[x['id'] for x]` probe returns null for providers/calls — use the right key.
- Orders and products are **in-memory** (per-session): create them via POST before testing lookups/pagination.

## Endpoint → helper map (for targeted refactor testing)
- `find_by_id`: `GET /api/listing/package/{id}` (hit real id → 200; fake → 404 "上架包不存在").
- `find_by_attr`: `GET /api/providers/{provider_id}` (hit seed `openai_text` → 200; fake → 404). This is the
  path that would crash if `knowledge_storage.py` were missing its `find_by_attr` import — always verify it.
- `paginate`: create 3 orders (`POST /api/orders`), then `GET /api/orders?user_id=u1&page=N&limit=2`; assert
  counts 2/1/0 and that page1 vs page2 ids are disjoint.
- `extract_product_fields` (+`find_by_id`): `POST /api/listing/generate-title`.
  - (a) supply explicit `product_info` and assert returned titles contain the supplied values (proves real
    extraction, not defaults). Dedup may yield 19 not 20 titles — that's expected.
  - (b) supply only a real `product_id` from `product_knowledge` (e.g. `687ed298-...`) and assert titles
    incorporate the stored record's fields (proves `find_by_id` hit).

## Gotchas
- `POST /api/providers/create` rejects non-placeholder keys with 400 ("不允许保存真实API Key") — expected guard.
  Use `api_key_placeholder` containing `sk-xxxxxxxx`/`placeholder`/`masked` if you need a create to succeed.
- No GitHub Actions CI (`.github/workflows` absent) — only Devin Review runs.

## Devin Secrets Needed
None. The app boots and all tested endpoints work with no API keys or external services.
