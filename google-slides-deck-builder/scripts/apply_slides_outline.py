#!/usr/bin/env python3
import argparse
import json
import re
from typing import List, Dict


def normalize_bullets(bullets: List[str]) -> str:
    cleaned = [re.sub(r"\s+", " ", b).strip() for b in bullets if b and b.strip()]
    return "\n".join(f"• {b}" for b in cleaned)


def main():
    p = argparse.ArgumentParser(description="Append slides from outline JSON to a Google Slides deck")
    p.add_argument("--presentation-id", required=True)
    p.add_argument("--outline-json", required=True)
    p.add_argument("--service-account", required=True)
    args = p.parse_args()

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except Exception as e:
        raise SystemExit(f"Missing Google API deps: {e}")

    with open(args.outline_json, "r", encoding="utf-8") as f:
        outline = json.load(f)

    slides: List[Dict] = outline.get("slides", [])
    if not slides:
        raise SystemExit("outline-json has no slides")

    creds = service_account.Credentials.from_service_account_file(
        args.service_account,
        scopes=["https://www.googleapis.com/auth/presentations"],
    )
    service = build("slides", "v1", credentials=creds, cache_discovery=False)

    # preflight get
    pres = service.presentations().get(presentationId=args.presentation_id).execute()
    title = pres.get("title", "")
    print(f"Connected presentation: {title}")

    requests = []

    for idx, s in enumerate(slides, start=1):
        sid = f"auto_slide_{idx}"
        title_id = f"auto_title_{idx}"
        body_id = f"auto_body_{idx}"

        requests.append({
            "createSlide": {
                "objectId": sid,
                "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"}
            }
        })

        # Find placeholders after creation not directly deterministic; easiest: use createShape + insertText
        requests.append({
            "createShape": {
                "objectId": title_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": sid,
                    "size": {
                        "height": {"magnitude": 60, "unit": "PT"},
                        "width": {"magnitude": 620, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 40,
                        "translateY": 25,
                        "unit": "PT",
                    },
                },
            }
        })
        requests.append({"insertText": {"objectId": title_id, "text": s.get("title", "")}})
        requests.append({
            "updateTextStyle": {
                "objectId": title_id,
                "textRange": {"type": "ALL"},
                "style": {"bold": True, "fontSize": {"magnitude": 28, "unit": "PT"}},
                "fields": "bold,fontSize",
            }
        })

        requests.append({
            "createShape": {
                "objectId": body_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": sid,
                    "size": {
                        "height": {"magnitude": 320, "unit": "PT"},
                        "width": {"magnitude": 620, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 40,
                        "translateY": 110,
                        "unit": "PT",
                    },
                },
            }
        })

        body_text = normalize_bullets(s.get("bullets", []))
        requests.append({"insertText": {"objectId": body_id, "text": body_text}})
        requests.append({
            "updateTextStyle": {
                "objectId": body_id,
                "textRange": {"type": "ALL"},
                "style": {"fontSize": {"magnitude": 18, "unit": "PT"}},
                "fields": "fontSize",
            }
        })

    service.presentations().batchUpdate(
        presentationId=args.presentation_id,
        body={"requests": requests}
    ).execute()

    print(f"Added {len(slides)} slides")


if __name__ == "__main__":
    main()
