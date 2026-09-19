"""
Tests for automatic curriculum bootstrapping and lazy topic content population.
"""

import pytest
from app.database import SessionLocal, Base, engine
from app.models.learning import Subject, Topic, Lesson, LessonStep, Question
from app.services.curriculum_seed import ensure_subjects_and_topics, ensure_topic_content_and_questions

@pytest.fixture
def clean_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_ensure_subjects_and_topics_creates_all(clean_db):
    subs = ensure_subjects_and_topics(clean_db)
    assert len(subs) == 6
    expected_slugs = {"dbms", "oops", "os", "ds", "ml", "cn"}
    assert {s.slug for s in subs} == expected_slugs

    total_topics = clean_db.query(Topic).count()
    assert total_topics == 74

def test_ensure_topic_content_and_questions(clean_db):
    topic = clean_db.query(Topic).filter(Topic.slug == "dbms-fundamentals").first()
    assert topic is not None

    ensure_topic_content_and_questions(clean_db, topic)
    lesson = clean_db.query(Lesson).filter(Lesson.topic_id == topic.id).first()
    assert lesson is not None

    steps = clean_db.query(LessonStep).filter(LessonStep.lesson_id == lesson.id).all()
    assert len(steps) >= 12

    learn_qs = clean_db.query(Question).filter(
        Question.topic_id == topic.id,
        Question.question_context == "LEARN"
    ).all()
    assert len(learn_qs) >= 15
