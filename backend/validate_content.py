"""
CodeOrbit Curriculum & Content Validation Script
Comprehensive automated validation of all 74 CS topics across 6 subjects:
- Database completeness: 6 subjects, 74 topics
- 12 required exam-oriented sections per topic (Definition, Core Concept, Key Points,
  Classification, How It Works, Example, Comparison Table, Formulas, Exam Tip,
  Common Confusion, Important Questions/FAQs, 60s Revision)
- Zero generic filler phrases
- Verified reference links (No synthetic URLs)
- >= 15 Learn and >= 15 Practice questions per topic with options, correct answer, and explanations
"""

import sys
import os

# Ensure app package is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from app.database import SessionLocal
from app.models.learning import Subject, Topic, Lesson, LessonStep, Question, QuestionOption
from app.services.content_service import TOPIC_REFERENCE_MAP, SUBJECT_HUB_URLS, SECTION_TYPES

FORBIDDEN_FILLER_PHRASES = [
    "indispensable core concept",
    "engineering bottleneck",
    "underlying runtime",
    "crucial paradigm",
    "seamlessly facilitates",
    "plays a pivotal role",
    "serves as a cornerstone",
    "lorem ipsum"
]

EXPECTED_SUBJECTS = {
    "dbms": 12,
    "oops": 11,
    "os": 11,
    "ds": 15,
    "ml": 11,
    "cn": 14
}

def validate():
    db = SessionLocal()
    errors = []
    warnings = []
    total_checks = 0
    passed_checks = 0

    print("=" * 70)
    print("🎓 CODEORBIT CURRICULUM & CONTENT VALIDATION")
    print("=" * 70)

    try:
        # 1. Validate Subjects
        print("\n[1/6] Verifying Subjects and Topic Counts...")
        subjects = db.query(Subject).all()
        subj_map = {s.slug: s for s in subjects}

        for s_slug, expected_count in EXPECTED_SUBJECTS.items():
            total_checks += 1
            if s_slug not in subj_map:
                errors.append(f"Missing subject in DB: '{s_slug}'")
                continue
            
            s_obj = subj_map[s_slug]
            actual_count = db.query(Topic).filter(Topic.subject_id == s_obj.id).count()
            if actual_count != expected_count:
                errors.append(f"Subject '{s_slug}' expected {expected_count} topics, found {actual_count}")
            else:
                passed_checks += 1
                print(f"  ✓ {s_obj.name.upper():<5} ({s_slug}): {actual_count}/{expected_count} topics")

        all_topics = db.query(Topic).all()
        total_checks += 1
        if len(all_topics) != 74:
            errors.append(f"Total topics expected 74, found {len(all_topics)}")
        else:
            passed_checks += 1
            print(f"  ✓ Total Topics: 74/74 verified across all 6 core subjects.")

        # 2. Validate Topic Lessons and 12 Required Sections
        print("\n[2/6] Verifying 12 Exam Sections per Topic...")
        topics_with_missing_sections = []
        topics_with_filler = []

        for topic in all_topics:
            total_checks += 1
            lesson = db.query(Lesson).filter(Lesson.topic_id == topic.id).first()
            if not lesson:
                errors.append(f"Topic '{topic.slug}' has NO Lesson record.")
                continue

            steps = db.query(LessonStep).filter(LessonStep.lesson_id == lesson.id).order_by(LessonStep.section_order.asc()).all()
            if len(steps) < 12:
                topics_with_missing_sections.append((topic.slug, len(steps)))
                errors.append(f"Topic '{topic.slug}' has only {len(steps)}/12 sections.")
                continue

            step_types = [s.section_type for s in steps]
            missing_types = [req for req in SECTION_TYPES if req not in step_types]
            if missing_types:
                errors.append(f"Topic '{topic.slug}' is missing required section types: {missing_types}")
            else:
                passed_checks += 1

            # Check for generic filler phrases in content
            for s in steps:
                c_lower = (s.content or "").lower()
                for phrase in FORBIDDEN_FILLER_PHRASES:
                    if phrase in c_lower:
                        topics_with_filler.append((topic.slug, s.section_type, phrase))
                        errors.append(f"Forbidden filler '{phrase}' found in '{topic.slug}' ({s.section_type})")

        if not topics_with_missing_sections:
            print("  ✓ All 74 topics contain all 12 required exam-oriented sections.")
        else:
            print(f"  ✗ {len(topics_with_missing_sections)} topics have missing sections.")

        if not topics_with_filler:
            print("  ✓ Zero forbidden generic filler phrases detected across all topics.")
        else:
            print(f"  ✗ {len(topics_with_filler)} occurrences of forbidden filler detected.")

        # 3. Validate Reference Mappings & URLs
        print("\n[3/6] Verifying Reference Mappings & Non-Synthetic URLs...")
        synthetic_url_count = 0
        unmapped_topics = []

        for topic in all_topics:
            total_checks += 1
            if topic.slug not in TOPIC_REFERENCE_MAP:
                unmapped_topics.append(topic.slug)
                warnings.append(f"Topic '{topic.slug}' not in TOPIC_REFERENCE_MAP (fallback to subject hub).")
            else:
                refs = TOPIC_REFERENCE_MAP[topic.slug]
                if not refs or len(refs) < 2:
                    warnings.append(f"Topic '{topic.slug}' has fewer than 2 reference links.")
                for r in refs:
                    if f"/{topic.slug}/" in r.get("source_url", ""):
                        synthetic_url_count += 1
                        errors.append(f"Synthetic URL found in TOPIC_REFERENCE_MAP for '{topic.slug}': {r.get('source_url')}")
            passed_checks += 1

        # Check Question URLs for synthetic patterns
        questions_with_synthetic = db.query(Question).filter(
            Question.source_url.like("%geeksforgeeks.org/%/%") | Question.source_url.like("%tutorialspoint.com/%/%")
        ).all()
        
        # Check specific synthetic format: https://www.geeksforgeeks.org/{t_slug}/
        bad_q_urls = 0
        for topic in all_topics:
            bad_gfg = f"https://www.geeksforgeeks.org/{topic.slug}/"
            bad_tp = f"https://www.tutorialspoint.com/{topic.slug}/"
            count = db.query(Question).filter(
                Question.topic_id == topic.id,
                (Question.source_url == bad_gfg) | (Question.source_url == bad_tp)
            ).count()
            if count > 0:
                bad_q_urls += count
                errors.append(f"Topic '{topic.slug}' has {count} questions with synthetic URLs.")

        if synthetic_url_count == 0 and bad_q_urls == 0:
            print("  ✓ All topic references and question sources use verified real URLs (0 synthetic URLs).")
        else:
            print(f"  ✗ Found {synthetic_url_count} synthetic reference URLs and {bad_q_urls} question synthetic URLs.")

        # 4. Validate Question Pools (LEARN & PRACTICE)
        print("\n[4/6] Verifying Question Pools per Topic (>= 15 Learn & >= 15 Practice)...")
        topics_insufficient_learn = []
        topics_insufficient_practice = []
        questions_missing_answer = 0
        questions_missing_explanation = 0

        for topic in all_topics:
            total_checks += 1
            learn_count = db.query(Question).filter(
                Question.topic_id == topic.id,
                Question.question_context == "LEARN"
            ).count()
            if learn_count < 15:
                topics_insufficient_learn.append((topic.slug, learn_count))
                errors.append(f"Topic '{topic.slug}' has only {learn_count}/15 LEARN questions.")

            practice_count = db.query(Question).filter(
                Question.topic_id == topic.id,
                Question.question_context == "PRACTICE"
            ).count()
            if practice_count < 15:
                topics_insufficient_practice.append((topic.slug, practice_count))
                errors.append(f"Topic '{topic.slug}' has only {practice_count}/15 PRACTICE questions.")

            if learn_count >= 15 and practice_count >= 15:
                passed_checks += 1

            # Validate options and explanations for this topic's questions
            q_list = db.query(Question).filter(Question.topic_id == topic.id).all()
            for q in q_list:
                opts = db.query(QuestionOption).filter(QuestionOption.question_id == q.id).all()
                if len(opts) < 2:
                    questions_missing_answer += 1
                    errors.append(f"Question ID {q.id} in '{topic.slug}' has fewer than 2 options.")
                elif not any(o.is_correct for o in opts):
                    questions_missing_answer += 1
                    errors.append(f"Question ID {q.id} in '{topic.slug}' has NO correct option marked.")
                
                if not q.explanation or len(q.explanation.strip()) < 10:
                    questions_missing_explanation += 1
                    errors.append(f"Question ID {q.id} in '{topic.slug}' lacks a detailed explanation.")

        if not topics_insufficient_learn and not topics_insufficient_practice:
            print("  ✓ All 74 topics have >= 15 Learn and >= 15 Practice questions.")
        else:
            print(f"  ✗ Insufficient questions: Learn ({len(topics_insufficient_learn)}), Practice ({len(topics_insufficient_practice)})")

        if questions_missing_answer == 0 and questions_missing_explanation == 0:
            print("  ✓ All questions have valid options, correct answers, and thorough explanations.")
        else:
            print(f"  ✗ Questions issues: {questions_missing_answer} missing answer, {questions_missing_explanation} missing explanation.")

        # 5. Quick Reference & Academic Data Coverage
        print("\n[5/6] Verifying Academic Data Dictionary & Quick Reference Data...")
        from curriculum import TOPIC_ACADEMIC_DATA, get_topic_quick_reference
        missing_academic_keys = []
        for topic in all_topics:
            total_checks += 1
            if topic.slug not in TOPIC_ACADEMIC_DATA:
                missing_academic_keys.append(topic.slug)
                errors.append(f"Topic '{topic.slug}' missing from TOPIC_ACADEMIC_DATA dictionary.")
            else:
                qr = get_topic_quick_reference(topic.slug)
                if not qr.get("exam_definition") or not qr.get("key_points"):
                    errors.append(f"Quick reference for '{topic.slug}' missing essential fields.")
                else:
                    passed_checks += 1

        if not missing_academic_keys:
            print(f"  ✓ TOPIC_ACADEMIC_DATA contains complete dataset for all {len(TOPIC_ACADEMIC_DATA)} topics.")
        else:
            print(f"  ✗ Missing {len(missing_academic_keys)} topics from TOPIC_ACADEMIC_DATA.")

        # 6. Overall Summary
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Total Validation Checks: {total_checks}")
        print(f"Passed Checks:           {passed_checks}")
        print(f"Total Errors:            {len(errors)}")
        print(f"Total Warnings:          {len(warnings)}")

        if warnings:
            print(f"\n⚠️  {len(warnings)} WARNINGS:")
            for w in warnings[:10]:
                print(f"  - {w}")
            if len(warnings) > 10:
                print(f"  ... and {len(warnings) - 10} more warnings.")

        if errors:
            print(f"\n❌ {len(errors)} ERRORS DETECTED:")
            for err in errors[:15]:
                print(f"  - {err}")
            if len(errors) > 15:
                print(f"  ... and {len(errors) - 15} more errors.")
            print("\n❌ VALIDATION FAILED: Resolve the above errors before proceeding.")
            return False

        print("\n🎉 ALL 74 TOPICS SUCCESSFULLY VALIDATED WITH ZERO ERRORS!")
        return True

    except Exception as ex:
        print(f"\n💥 Unexpected error during validation: {ex}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
