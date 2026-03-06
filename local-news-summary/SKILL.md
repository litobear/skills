---
name: local-news-summary
description: Query current Yahoo Taiwan headlines from a local Playwright microservice and return a human-readable Chinese bullet summary without links. Use when the user asks for current news, 即時新聞, 頭條整理, or asks for summary mode news output.
---

# Local News Summary

Use the local API and return concise Traditional Chinese summaries.

## Steps

1. Call the local microservice:
   - `POST http://127.0.0.1:3400/v1/query`
   - JSON body:
     ```json
     {
       "provider": "yahoo-news",
       "action": "top_headlines",
       "params": { "limit": 5 },
       "timeoutMs": 20000
     }
     ```
2. If API fails, report failure reason in one short line and ask whether to retry.
3. If API succeeds, convert each headline into one human-readable bullet line.
4. Remove links from final output.
5. Prefer short, useful phrasing over raw headline dumps.

## Output format

- Title line: `目前即時新聞摘要：`
- Then numbered list `1.` `2.` ...
- No URLs in final response.
- Default 5 items unless user asks another count.

## Style

- Traditional Chinese.
- Clean and brief.
- Keep uncertainty explicit (e.g., if a title is promotional or unclear, label it as such).
