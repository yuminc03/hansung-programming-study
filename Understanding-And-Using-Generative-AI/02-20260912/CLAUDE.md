# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

This directory is one lesson (`02-20260912`) inside the larger `hansung-programming-study` monorepo, under the `Understanding-And-Using-Generative-AI` course track. It is a self-contained "vibe coding" exercise: a single-file Streamlit dashboard that assigns incoming customer/helpdesk inquiries to the right team by comparing sentence embeddings against a small FAQ set, with a confidence threshold that routes uncertain cases to a human instead of guessing.

There is no build system, package manifest, or test suite — this is teaching material, not a production app.

## Commands

```bash
pip install streamlit sentence-transformers scikit-learn pandas altair
streamlit run app.py
```

- First run downloads the `BAAI/bge-m3` embedding model (~2.2GB) and caches it; subsequent runs are fast.
- No linter, formatter, or test runner is configured. There is no `requirements.txt` — dependencies are only documented in `README.md` and this file.
- To open the companion notebook: `jupyter notebook 01_고객문의_자동배정_토큰화_임베딩_의미공간.ipynb` (needs `tiktoken`, `matplotlib` in addition to the packages above).

## Architecture

`app.py` is a single file split into four regions (see its own section comments):

1. **Constants** — `MODEL_NAME`, `DEFAULT_THRESHOLD` (0.55), `UNASSIGNED` label, `TOP_K`, and `FAQ_DATA` (the list of `[질문, 답변, 담당팀]` rows the whole app routes against).
2. **Resource loading** — `load_model_and_faq_vectors()` (`st.cache_resource`) loads the SentenceTransformer once per process and embeds the fixed FAQ set at the same time; `embed_inquiries()` (`st.cache_data`) embeds the user's pasted inquiries, keyed by the tuple of input lines so re-running with an unchanged inquiry list (e.g. only moving the threshold slider) skips recomputation. This caching exists because Streamlit reruns the whole script on every widget interaction.
3. **Assignment logic** (`parse_inquiries`, `assign_teams`, `style_result`, `build_top_chart`) — pure functions decoupled from the UI. `assign_teams` computes a cosine-similarity matrix (inquiries × FAQ), takes the top-`TOP_K` matches per inquiry, and assigns the top match's team only if its score clears `threshold`; otherwise the row is marked `UNASSIGNED` for human review. Because this logic never references Streamlit, swapping domains only requires replacing `FAQ_DATA`.
4. **UI** (`main()`) — sidebar (threshold slider + FAQ reference table), input textarea with example-fill/clear buttons, results table (color-highlighted `UNASSIGNED` rows), a per-inquiry top-3 bar chart with the threshold drawn as a rule line, per-team counts, and a UTF-8-BOM CSV download (for correct Hangul in Excel).

**Core invariant**: nearest-neighbor similarity search always returns _a_ best match even when nothing is actually relevant, so the threshold check in `assign_teams` (not the similarity ranking itself) is what distinguishes "most similar" from "similar enough." Any change to matching logic should preserve this human-in-the-loop fallback.

### Companion notebook

`01_고객문의_자동배정_토큰화_임베딩_의미공간.ipynb` is the conceptual walkthrough `app.py` is built from (originally framed around an online shopping mall FAQ set rather than the IT helpdesk one now in `app.py`): tokenization with `tiktoken` → embedding with `BAAI/bge-m3` → cosine similarity → threshold-gated assignment → a PCA scatter of the semantic space. Read it first when asked to explain _why_ the app works the way it does, not just what the code does.

### Prompt script

`바이브코딩_프롬프트_고객문의_자동배정_대시보드.txt` is the staged prompt sequence (STEP 0–5: explore → plan → implement → verify → adapt to a new domain → write up README) this exercise was built from. If asked to redo, extend, or re-target this exercise to a new domain (the file lists hospital triage, civil-complaint routing, real-estate inquiries as alternatives), follow this file's step structure rather than jumping straight to code.

## Working conventions

- `FAQ_DATA` is the only thing that should change when retargeting the dashboard to a new domain — the README explicitly calls out that the routing logic (`assign_teams`, `build_top_chart`, etc.) was not touched when the app was adapted from an online shopping mall to an internal IT helpdesk.
- `README.md` documents exact line references (e.g. `app.py:81`, `app.py:124`) for each pipeline stage; if you edit `app.py`, check whether those references still point to the right lines and update `README.md` if not.
- Keep `DEFAULT_THRESHOLD` changes deliberate: 0.55 was picked from the observed score distribution (correct matches cluster 0.55–0.93; irrelevant ones fall near 0.46), not derived analytically — document the reasoning in `README.md` if it changes.
