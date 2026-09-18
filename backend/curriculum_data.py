"""
CodeOrbit Curriculum Data Service
Exposes verified academic curriculum sections for all 74 core CS topics.
Delegates to curriculum package aggregator.
Zero generic filler permitted.
"""

from typing import Dict, List, Any
from curriculum import compile_lesson_steps, get_academic_topic, get_topic_quick_reference, TOPIC_ACADEMIC_DATA

def get_content_for_topic(topic_slug: str, topic_title: str = "", subject_name: str = "") -> List[Dict[str, Any]]:
    """
    Returns the 12 complete exam-oriented sections for the given topic.
    Fails with ValueError if the topic is not part of the verified curriculum.
    """
    return compile_lesson_steps(topic_slug)
