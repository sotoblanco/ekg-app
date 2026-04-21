#!/usr/bin/env python3
"""
Verify PDF is fully scanned (image-based) and get basic metadata.
"""
import pdfplumber

PDF = "/Users/soto/projects/app-ekg/318216295-Dubin-Rapid-Interpretation-of-EKGs-6th-Ed.pdf"
with pdfplumber.open(PDF) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    # Sample first page with image details
    p = pdf.pages[5]
    print(f"Images on page 6: {len(p.images)}")
    if p.images:
        img = p.images[0]
        print(f"Image size: {img.get('width')}x{img.get('height')}")
        print(f"Image keys: {list(img.keys())}")
