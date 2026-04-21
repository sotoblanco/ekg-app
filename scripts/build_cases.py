#!/usr/bin/env python3
"""
Generate cases_data.js for app-ekg.
Selects the best-matched cases per chapter, ensuring structured report data.
Run: source .venv/bin/activate && python3 scripts/build_cases.py
"""

import json
import os
import re

CASES_DIR = "/Users/soto/projects/app-ekg/cases"
OUTPUT_JS = "/Users/soto/projects/app-ekg/cases_data.js"

# Topic -> Chapter mapping (for scoring)
CHAPTER_TOPIC_MAP = {
    1:  {"topics": [], "categories": ["Fundamentals"], "label": "Basic Principles"},
    2:  {"topics": [], "categories": ["Fundamentals"], "label": "Recording the EKG"},
    3:  {"topics": ["Normal Sinus Rhythm"], "categories": ["Fundamentals", "Rhythm"], "label": "Rate"},
    4:  {"topics": ["Premature Atrial Contractions"], "categories": ["Rhythm"], "label": "Rhythm"},
    5:  {"topics": ["Atrial Fibrillation", "Atrial Flutter"], "categories": ["Rhythm"], "label": "The P Wave"},
    6:  {"topics": ["AV Block"], "categories": ["Rhythm"], "label": "The PR Interval"},
    7:  {"topics": ["Right Bundle Branch Block", "Left Bundle Branch Block", "Wolff-Parkinson-White"],
         "categories": ["Rhythm"], "label": "The QRS Complex"},
    8:  {"topics": ["Pericarditis"], "categories": ["Diverse disease"], "label": "The ST Segment"},
    9:  {"topics": ["Long QT Syndrome", "Hyperkalemia", "Hypokalemia"],
         "categories": ["Diverse disease"], "label": "The T Wave"},
    10: {"topics": [], "categories": ["Axis"], "label": "Axis"},
    11: {"topics": ["Left Ventricular Hypertrophy", "Right Ventricular Hypertrophy"],
         "categories": ["Hypertrophy"], "label": "Hypertrophy"},
    12: {"topics": ["Myocardial Infarction"], "categories": ["Myocardial Infarction"], "label": "Infarction"},
    13: {"topics": ["Atrial Fibrillation", "Ventricular Tachycardia", "Ventricular Fibrillation",
                    "Supraventricular Tachycardia", "Atrial Flutter"],
         "categories": ["Rhythm"], "label": "Arrhythmias"},
}

MAX_CASES_PER_CHAPTER = 3


def load_case(case_folder):
    meta_path = os.path.join(CASES_DIR, case_folder, "metadata.json")
    img_path = os.path.join(CASES_DIR, case_folder, "ekg.gif")
    if not os.path.exists(meta_path) or not os.path.exists(img_path):
        return None
    with open(meta_path) as f:
        meta = json.load(f)
    meta["image_local"] = f"cases/{case_folder}/ekg.gif"
    return meta


def has_good_data(meta):
    """Return True if the case has usable clinical data."""
    has_history = bool(meta.get("clinical_history", "").strip())
    has_diagnosis = bool(meta.get("diagnosis", "").strip())
    report = meta.get("report", {})
    # Has at least impression or findings populated
    has_report = bool(report.get("impression", "").strip() or report.get("findings", "").strip())
    return has_history and has_diagnosis and has_report


def extract_impression(meta):
    """Extract or derive a clean impression string."""
    report = meta.get("report", {})
    imp = report.get("impression", "").strip()
    if imp:
        return imp
    # Fall back to extracting first sentence of diagnosis
    diag = meta.get("diagnosis", "")
    # Try to extract "Dx: ..." pattern
    m = re.match(r"Dx:\s*([^.]+\.?)", diag)
    if m:
        return m.group(1).strip()
    # Fall back to first sentence
    sentences = re.split(r'(?<=[.!?])\s+', diag)
    return sentences[0][:120] if sentences else "Unknown Diagnosis"


def truncate(text, max_words=70):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


def score_case(meta, topic_set, category_set):
    score = 0
    case_topics = set(meta.get("topics", []))
    case_category = meta.get("category", "")
    score += len(case_topics & topic_set) * 12
    if case_category in category_set:
        score += 6
    # Prefer cases with good structured data
    if has_good_data(meta):
        score += 8
    # Prefer accessible difficulty (2-3)
    diff = meta.get("difficulty", 3)
    score -= abs(diff - 2)
    return score


def build_all_impressions():
    """Collect all impressions to use as distractors in quiz."""
    impressions = []
    for d in sorted(os.listdir(CASES_DIR)):
        if not d.startswith("case_"):
            continue
        meta = load_case(d)
        if meta:
            imp = extract_impression(meta)
            if imp and len(imp) > 5:
                impressions.append(imp)
    return impressions


def build_chapter_cases(chapter_id, config, all_impressions):
    topic_set = set(config["topics"])
    category_set = set(config["categories"])

    scored = []
    case_dirs = sorted(
        [d for d in os.listdir(CASES_DIR) if d.startswith("case_") and os.path.isdir(os.path.join(CASES_DIR, d))],
        key=lambda x: int(x.split("_")[1])
    )

    for case_folder in case_dirs:
        meta = load_case(case_folder)
        if not meta:
            continue
        score = score_case(meta, topic_set, category_set)
        if score > 0:
            scored.append((score, meta))

    scored.sort(key=lambda x: (-x[0], x[1].get("difficulty", 3)))

    selected = []
    used_ids = set()

    for _, meta in scored:
        if len(selected) >= MAX_CASES_PER_CHAPTER:
            break
        cid = meta.get("case_id")
        if cid in used_ids:
            continue
        used_ids.add(cid)

        impression = extract_impression(meta)
        report = meta.get("report", {})

        # Build 4 quiz options: 1 correct + 3 distractors
        distractors = [
            imp for imp in all_impressions
            if imp.lower() != impression.lower() and len(imp) > 8
        ]
        # Pick 3 varied distractors
        import random
        random.seed(int(cid) * chapter_id)
        chosen_distractors = random.sample(distractors[:80], min(3, len(distractors[:80])))

        options = [impression] + chosen_distractors
        random.shuffle(options)
        correct_idx = options.index(impression)

        selected.append({
            "case_id": cid,
            "image": meta.get("image_local"),
            "clinical_history": meta.get("clinical_history", "").strip(),
            "diagnosis": truncate(meta.get("diagnosis", "No diagnosis available.")),
            "impression": impression,
            "report": {
                "rhythm": report.get("rhythm", ""),
                "rate": report.get("rate", ""),
                "axis": report.get("axis", ""),
                "intervals": report.get("intervals", ""),
                "findings": report.get("findings", ""),
                "impression": impression,
            },
            "topics": meta.get("topics", []),
            "difficulty": meta.get("difficulty", 3),
            "options": options,
            "correct_idx": correct_idx,
        })

    return selected


def main():
    print("Loading all impressions for distractor pool...")
    all_impressions = build_all_impressions()
    print(f"  {len(all_impressions)} impressions collected")

    all_chapter_cases = {}
    for ch_id, config in CHAPTER_TOPIC_MAP.items():
        cases = build_chapter_cases(ch_id, config, all_impressions)
        all_chapter_cases[ch_id] = cases
        print(f"Chapter {ch_id:2d} ({config['label']:25s}): {len(cases)} cases")

    js_content = (
        "// AUTO-GENERATED by scripts/build_cases.py\n"
        "// Do not edit manually.\n\n"
        f"const CASES_DB = {json.dumps(all_chapter_cases, indent=2, ensure_ascii=False)};\n"
    )

    with open(OUTPUT_JS, "w") as f:
        f.write(js_content)

    total = sum(len(v) for v in all_chapter_cases.values())
    print(f"\nDone. {total} total cases -> {OUTPUT_JS}")


if __name__ == "__main__":
    main()
