"""
CodeOrbit Curriculum Aggregator
Loads verified academic curriculum datasets for all 74 core CS topics from curriculum/data/*.json.
Compiles 12 structured exam sections for lesson player and quick reference.
Zero generic filler permitted.
"""

import os
import json
import glob
from typing import Dict, Any, List, Optional
from app.services.content_service import get_topic_references

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Load all subject JSON files into unified dictionary
TOPIC_ACADEMIC_DATA: Dict[str, Dict[str, Any]] = {}

def _load_datasets():
    global TOPIC_ACADEMIC_DATA
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                TOPIC_ACADEMIC_DATA.update(data)
        except Exception as e:
            print(f"Error loading curriculum dataset {file_path}: {e}")

_load_datasets()


def get_academic_topic(topic_slug: str) -> Dict[str, Any]:
    """Retrieve raw academic structured data for a topic slug."""
    if topic_slug not in TOPIC_ACADEMIC_DATA:
        raise ValueError(f"Topic '{topic_slug}' not found in verified academic curriculum! Zero generic filler permitted.")
    return TOPIC_ACADEMIC_DATA[topic_slug]


def _format_markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """Format headers and rows into clean markdown table syntax."""
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, separator_line] + row_lines)


def compile_lesson_steps(topic_slug: str) -> List[Dict[str, Any]]:
    """
    Compiles the 12 structured exam sections for a topic.
    Returns list of section dicts ready for LessonStep insertion.
    """
    topic = get_academic_topic(topic_slug)
    title = topic.get("title", topic_slug)
    subject = topic.get("subject", "")
    
    # Fetch verified primary reference
    refs = get_topic_references(topic_slug, subject)
    primary_ref = refs[0] if refs else {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/computer-science-fundamentals/"
    }
    
    sections = []
    
    # 1. Exam Definition & Remember Block
    def_content = (
        f"### Exam Definition\n\n{topic['exam_definition']}\n\n"
        f"> **📌 Remember for Exams:**\n"
        f"> {topic.get('remember', '')}"
    )
    sections.append({
        "section_order": 1,
        "section_type": "exam_definition",
        "title": f"Exam Definition: {title}",
        "content": def_content,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 2. Core Concept & Technical Mechanics
    sections.append({
        "section_order": 2,
        "section_type": "core_concept",
        "title": f"Core Concept & Technical Mechanics",
        "content": topic.get("core_concept", ""),
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 3. Essential Technical Key Points
    key_points_text = "### Key Examination Points\n\n" + "\n".join([f"- **{pt.split(':')[0]}:**{':'.join(pt.split(':')[1:])}" if ':' in pt else f"- {pt}" for pt in topic.get("key_points", [])])
    sections.append({
        "section_order": 3,
        "section_type": "key_points",
        "title": f"Key Technical Points",
        "content": key_points_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 4. Classification & Taxonomy
    classification = topic.get("classification", {})
    class_items_text = f"### {classification.get('title', 'Types & Classifications')}\n\n" + "\n".join([f"- **{item['name']}**: {item['desc']}" for item in classification.get("items", [])])
    sections.append({
        "section_order": 4,
        "section_type": "classification",
        "title": classification.get("title", "Classifications & Types"),
        "content": class_items_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 5. How It Works (Step-by-Step & ASCII Diagram)
    how_it_works = topic.get("how_it_works", {})
    steps_text = f"### Execution Workflow\n\n" + "\n".join([f"{step}" for step in how_it_works.get("steps", [])])
    if how_it_works.get("diagram"):
        steps_text += f"\n\n```text\n{how_it_works['diagram']}\n```"
    sections.append({
        "section_order": 5,
        "section_type": "how_it_works",
        "title": how_it_works.get("title", "How It Works: Step-by-Step"),
        "content": steps_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 6. Student Example & Walkthrough
    example = topic.get("example", {})
    example_text = f"### Scenario\n{example.get('scenario', '')}\n\n"
    if example.get("code"):
        example_text += f"```java\n{example['code']}\n```"
    sections.append({
        "section_order": 6,
        "section_type": "example",
        "title": f"Example: {example.get('title', 'Practical Walkthrough')}",
        "content": example_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 7. Comparison Table
    comparison = topic.get("comparison", {})
    if comparison.get("headers") and comparison.get("rows"):
        comp_table = _format_markdown_table(comparison["headers"], comparison["rows"])
        comp_text = f"### Exam Comparison\n\n{comp_table}"
    else:
        comp_text = "No direct comparison required for this foundational topic."
    sections.append({
        "section_order": 7,
        "section_type": "comparison",
        "title": comparison.get("title", "Comparative Analysis"),
        "content": comp_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 8. Exam Formulas & Invariant Rules
    formulas = topic.get("formulas", [])
    if formulas:
        form_lines = []
        for f in formulas:
            form_lines.append(f"#### {f['name']}\n`{f['formula']}`\n- **Explanation:** {f['explanation']}\n")
        form_text = "### Core Formulas & Axioms\n\n" + "\n".join(form_lines)
    else:
        form_text = "Standard theoretical axioms apply."
    sections.append({
        "section_order": 8,
        "section_type": "formula",
        "title": "Exam Formulas & Invariant Rules",
        "content": form_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 9. 🎯 High-Yield Exam Tip
    exam_tip_text = (
        f"> 🎯 **High-Yield University Exam Tip:**\n>\n"
        f"> {topic.get('exam_tip', '')}\n>\n"
        f"> *Marking Scheme Advice:* Always state assumptions, define key mathematical terms, and draw the system architecture diagram to secure full marks."
    )
    sections.append({
        "section_order": 9,
        "section_type": "exam_tip",
        "title": "🎯 High-Yield Exam Tip",
        "content": exam_tip_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 10. ⚠️ Common Confusion & Pitfalls
    confusion = topic.get("common_confusion", {})
    conf_text = (
        f"### ❌ Common Misconception:\n"
        f"*{confusion.get('wrong', '')}*\n\n"
        f"### ✅ Accurate Technical Reality:\n"
        f"**{confusion.get('correct', '')}**\n\n"
        f"**Why this distinction matters:** {confusion.get('explanation', '')}"
    )
    sections.append({
        "section_order": 10,
        "section_type": "common_confusion",
        "title": "⚠️ Common Confusion & Pitfalls",
        "content": conf_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 11. University Exam Questions & Model Answers
    faqs = topic.get("faqs", [])
    faq_blocks = []
    for faq in faqs:
        faq_blocks.append(
            f"#### [{faq.get('marks', 'Exam Question')}] {faq['q']}\n"
            f"**Model Answer:**\n{faq['a']}\n"
        )
    faq_text = "### Frequently Asked University Questions\n\n" + "\n---\n".join(faq_blocks)
    sections.append({
        "section_order": 11,
        "section_type": "important_questions",
        "title": "University Exam Questions & Answers",
        "content": faq_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    # 12. ⚡ 60-Second Rapid Revision
    rev_points = topic.get("revision_60s", [])
    rev_text = "### ⚡ Rapid 60-Second Revision Sheet\n\n" + "\n".join([f"- [ ] {point}" for point in rev_points])
    sections.append({
        "section_order": 12,
        "section_type": "revision_60s",
        "title": "⚡ 60-Second Revision",
        "content": rev_text,
        "source_name": primary_ref["source_name"],
        "source_url": primary_ref["source_url"]
    })
    
    return sections


def get_topic_quick_reference(topic_slug: str) -> Dict[str, Any]:
    """
    Returns the structured payload for the Quick Reference modal.
    Directly powers GET /api/topics/{topic_slug}/quick-reference.
    """
    topic = get_academic_topic(topic_slug)
    subject = topic.get("subject", "")
    refs = get_topic_references(topic_slug, subject)
    
    return {
        "topic_slug": topic_slug,
        "title": topic.get("title", topic_slug),
        "subject": subject,
        "exam_definition": topic.get("exam_definition", ""),
        "remember": topic.get("remember", ""),
        "core_concept": topic.get("core_concept", ""),
        "key_points": topic.get("key_points", []),
        "classification": topic.get("classification", {}),
        "how_it_works": topic.get("how_it_works", {}),
        "example": topic.get("example", {}),
        "comparison": topic.get("comparison", {}),
        "formulas": topic.get("formulas", []),
        "exam_tip": topic.get("exam_tip", ""),
        "common_confusion": topic.get("common_confusion", {}),
        "faqs": topic.get("faqs", []),
        "revision_60s": topic.get("revision_60s", []),
        "references": refs
    }
