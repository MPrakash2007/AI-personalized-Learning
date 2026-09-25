"""
CodeOrbit Retrieval Service (Local RAG)
Searches database topics, lesson content sections, curriculum academic datasets,
and question explanations to construct grounded academic context for AI Tutor queries.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.learning import Topic, Lesson, LessonStep, Question, Subject
from app.services.content_service import get_topic_references
from curriculum import TOPIC_ACADEMIC_DATA

# High-frequency CS engineering acronyms and subtopic alias mapping
ACRONYM_MAP: Dict[str, str] = {
    "acid": "transactions",
    "2pl": "concurrency-control",
    "two phase locking": "concurrency-control",
    "bcnf": "normalization",
    "1nf": "normalization",
    "2nf": "normalization",
    "3nf": "normalization",
    "er diagram": "er-model",
    "super key": "keys",
    "candidate key": "keys",
    "foreign key": "keys",
    "group by": "sql-queries",
    "having": "sql-queries",
    "join": "sql-joins",
    "subquery": "nested-queries",
    "b tree": "indexing-and-recovery",
    "b+ tree": "indexing-and-recovery",
    "solid": "solid-principles",
    "vtable": "polymorphism",
    "overriding": "polymorphism",
    "overloading": "polymorphism",
    "pcb": "processes",
    "context switch": "processes",
    "round robin": "cpu-scheduling",
    "sjf": "cpu-scheduling",
    "fcfs": "cpu-scheduling",
    "semaphore": "process-synchronization",
    "mutex": "process-synchronization",
    "critical section": "process-synchronization",
    "banker": "deadlocks",
    "coffman": "deadlocks",
    "paging": "memory-management",
    "segmentation": "memory-management",
    "tlb": "virtual-memory",
    "page fault": "virtual-memory",
    "lru": "virtual-memory",
    "fifo": "virtual-memory",
    "kmp": "strings",
    "floyd": "linked-lists",
    "dijkstra": "graphs",
    "mst": "greedy",
    "prim": "greedy",
    "kruskal": "greedy",
    "knapsack": "dynamic-programming",
    "quicksort": "sorting",
    "mergesort": "sorting",
    "binary search": "searching",
    "bayes": "naive-bayes",
    "entropy": "decision-trees",
    "gini": "decision-trees",
    "kmeans": "clustering",
    "k-means": "clustering",
    "confusion matrix": "model-evaluation",
    "roc": "model-evaluation",
    "auc": "model-evaluation",
    "crc": "data-link-layer",
    "framing": "data-link-layer",
    "cidr": "subnetting",
    "ospf": "routing",
    "bgp": "routing",
    "handshake": "tcp",
    "slow start": "tcp",
    "aimd": "tcp",
    "tls": "http-https",
    "ssl": "http-https",
    "rsa": "network-security",
    "firewall": "network-security",
}

def search_educational_knowledge(
    db: Session,
    query: str,
    subject_slug: Optional[str] = None,
    limit: int = 5
) -> Dict[str, Any]:
    """
    Search database for relevant topics, lesson sections, and questions.
    Constructs high-yield educational context for AI responses.
    """
    clean_query = query.strip().lower()
    STOPWORDS = {"and", "the", "for", "with", "how", "what", "why", "can", "explain", "give", "tell", "about", "does", "from", "into", "that", "this", "which", "are", "was", "were", "been"}
    raw_terms = [t for t in clean_query.split() if len(t) > 2]
    terms = [t for t in raw_terms if t not in STOPWORDS]
    if not terms:
        terms = raw_terms or [clean_query]

    # Check for direct alias hit
    target_slug = None
    for acronym, mapped_slug in ACRONYM_MAP.items():
        if acronym in clean_query:
            target_slug = mapped_slug
            break

    # Filter by subject if specified
    subject_obj = None
    if subject_slug and subject_slug != "general":
        subject_obj = db.query(Subject).filter(Subject.slug == subject_slug.lower()).first()

    # 1. Search Topics
    topic_query = db.query(Topic)
    if subject_obj:
        topic_query = topic_query.filter(Topic.subject_id == subject_obj.id)
    
    topic_filters = [Topic.title.ilike(f"%{clean_query}%"), Topic.slug.ilike(f"%{clean_query}%")]
    if target_slug:
        topic_filters.insert(0, Topic.slug == target_slug)
        
    for t in terms:
        topic_filters.append(Topic.title.ilike(f"%{t}%"))
        topic_filters.append(Topic.description.ilike(f"%{t}%"))
    
    matching_topics = topic_query.filter(or_(*topic_filters)).limit(limit).all()

    # Prioritize exact target_slug if present
    if target_slug:
        target_topic = topic_query.filter(Topic.slug == target_slug).first()
        if target_topic:
            matching_topics = [target_topic] + [top for top in matching_topics if top.id != target_topic.id]
            matching_topics = matching_topics[:limit]

    # 2. Search Lesson Steps (content sections)
    step_query = db.query(LessonStep).join(Lesson).join(Topic)
    if subject_obj:
        step_query = step_query.filter(Topic.subject_id == subject_obj.id)
    
    step_filters = [LessonStep.title.ilike(f"%{clean_query}%"), LessonStep.content.ilike(f"%{clean_query}%")]
    for t in terms:
        step_filters.append(LessonStep.title.ilike(f"%{t}%"))
        step_filters.append(LessonStep.content.ilike(f"%{t}%"))

    matching_steps = step_query.filter(or_(*step_filters)).limit(limit).all()

    # 3. Search Questions & Explanations
    q_query = db.query(Question).join(Topic)
    if subject_obj:
        q_query = q_query.filter(Topic.subject_id == subject_obj.id)
    
    q_filters = [Question.prompt.ilike(f"%{clean_query}%"), Question.explanation.ilike(f"%{clean_query}%")]
    for t in terms:
        q_filters.append(Question.prompt.ilike(f"%{t}%"))
        q_filters.append(Question.explanation.ilike(f"%{t}%"))

    matching_questions = q_query.filter(or_(*q_filters)).limit(limit).all()

    # Retrieve curated academic dataset for the primary matching topic
    primary_slug = None
    academic_data = None
    if target_slug and target_slug in TOPIC_ACADEMIC_DATA:
        primary_slug = target_slug
        academic_data = TOPIC_ACADEMIC_DATA.get(primary_slug)
    elif matching_topics:
        primary_slug = matching_topics[0].slug
        academic_data = TOPIC_ACADEMIC_DATA.get(primary_slug)
    elif target_slug:
        primary_slug = target_slug
        academic_data = TOPIC_ACADEMIC_DATA.get(primary_slug)

    # Aggregate references
    sources = []
    seen_urls = set()

    if academic_data and academic_data.get("references"):
        for r in academic_data["references"]:
            if r["source_url"] not in seen_urls:
                seen_urls.add(r["source_url"])
                sources.append(r)

    for top in matching_topics:
        refs = get_topic_references(top.slug)
        for r in refs:
            if r["source_url"] not in seen_urls:
                seen_urls.add(r["source_url"])
                sources.append(r)

    # Format structured context string for AI prompt
    context_blocks = []
    
    if matching_topics:
        context_blocks.append("### Relevant Curriculum Topics:")
        for t in matching_topics:
            subj_name = t.subject.name if t.subject else "Engineering"
            context_blocks.append(f"- **{t.title}** ({subj_name}): {t.description}")

    if matching_steps:
        context_blocks.append("\n### Academic Content Sections:")
        for s in matching_steps[:4]:
            context_blocks.append(f"#### {s.title} ({s.section_type})\n{s.content[:400]}...")
            if s.code_snippet:
                context_blocks.append(f"```\n{s.code_snippet}\n```")

    if matching_questions:
        context_blocks.append("\n### Verified Conceptual Questions:")
        for q in matching_questions[:3]:
            context_blocks.append(f"- Question: {q.prompt}\n  Explanation: {q.explanation}")

    context_str = "\n".join(context_blocks)

    # Pick best candidate for Quick Check
    quick_check = None
    if matching_questions:
        best_q = matching_questions[0]
        options = [opt.text for opt in best_q.options]
        correct_opt = next((opt.text for opt in best_q.options if opt.is_correct), options[0] if options else "A")
        quick_check = {
            "question": best_q.prompt,
            "options": options if options else ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": correct_opt,
            "explanation": best_q.explanation
        }
    elif academic_data and academic_data.get("faqs"):
        # Synthesize quick check from first FAQ if no DB question match
        faq_item = academic_data["faqs"][0]
        if faq_item.get("q"):
            quick_check = {
                "question": faq_item["q"],
                "options": [
                    faq_item.get("a", "")[:80],
                    "Incorrect concept definition",
                    "Applies to an unrelated system component",
                    "None of the above"
                ],
                "correct_answer": faq_item.get("a", "")[:80],
                "explanation": faq_item.get("a", "")
            }

    return {
        "query": query,
        "subject": subject_slug,
        "matching_topics": [
            {"id": t.id, "title": t.title, "slug": t.slug, "subject": t.subject.name if t.subject else "DBMS"}
            for t in matching_topics
        ],
        "primary_slug": primary_slug,
        "academic_data": academic_data,
        "context_str": context_str,
        "sources": sources[:4],
        "quick_check": quick_check,
        "has_content": bool(matching_topics or matching_steps or matching_questions or academic_data)
    }
