#!/usr/bin/env python3
"""
Extract text from Dubin EKG PDF. Identifies chapters and page structure.
"""

import pdfplumber
import json
import re
import sys

PDF_PATH = "/Users/soto/projects/app-ekg/318216295-Dubin-Rapid-Interpretation-of-EKGs-6th-Ed.pdf"

def extract_all_pages():
    results = []
    with pdfplumber.open(PDF_PATH) as pdf:
        total = len(pdf.pages)
        print(f"Total pages: {total}", file=sys.stderr)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            results.append({
                "page": i + 1,
                "text": text.strip()
            })
            if i < 30 or (i % 50 == 0):
                print(f"Page {i+1}: {text[:120].replace(chr(10), ' ')}", file=sys.stderr)
    return results

if __name__ == "__main__":
    pages = extract_all_pages()
    with open("/Users/soto/projects/app-ekg/scripts/raw_pages.json", "w") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(pages)} pages to raw_pages.json", file=sys.stderr)
