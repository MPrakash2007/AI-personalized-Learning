from __future__ import annotations
import json
import logging
from typing import Dict, Any, Optional, Tuple, List
import requests
from app.config import settings

logger = logging.getLogger(__name__)

class AIProvider:
    def chat_tutor(self, message: str, context: Optional[str] = None, retrieval_data: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[Dict[str, Any]], List[Dict[str, str]]]:
        raise NotImplementedError

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        raise NotImplementedError

    def review_interview_answer(self, prompt: str, student_answer: str) -> Dict[str, Any]:
        raise NotImplementedError


class RuleBasedSmartProvider(AIProvider):
    """
    Intelligent offline rule-based and retrieval-grounded AI provider.
    Synthesizes real curriculum content, dynamic quick checks, and verified source citations.
    """

    def chat_tutor(self, message: str, context: Optional[str] = None, retrieval_data: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[Dict[str, Any]], List[Dict[str, str]]]:
        msg_clean = message.strip()
        sources = retrieval_data.get("sources", []) if retrieval_data else []
        quick_check = retrieval_data.get("quick_check") if retrieval_data else None

        # 1. Grounded academic dataset from curriculum (Highest Fidelity)
        academic_data = retrieval_data.get("academic_data") if retrieval_data else None
        if academic_data and isinstance(academic_data, dict):
            topic_title = academic_data.get("title", msg_clean.title())
            definition = academic_data.get("exam_definition", "")
            remember = academic_data.get("remember", "")
            core_concept = academic_data.get("core_concept", "")
            key_points = academic_data.get("key_points", [])
            student_example = academic_data.get("example", {})
            exam_tip = academic_data.get("exam_tip", "")
            common_confusion = academic_data.get("common_confusion", {})
            faqs = academic_data.get("faqs", [])

            parts = [
                f"### 🎯 {topic_title} — Exam Prep Breakdown\n",
                f"#### 📖 1. Concept Definition\n{definition}\n",
            ]
            if remember:
                parts.append(f"**💡 What to Remember in Exam**: {remember}\n")

            if core_concept:
                parts.append(f"#### 💡 2. Core Mechanism\n{core_concept}\n")

            if key_points:
                parts.append("#### 🔑 3. Key High-Scoring Points")
                for kp in key_points:
                    if isinstance(kp, dict):
                        parts.append(f"- **{kp.get('title', '')}**: {kp.get('description', '')}")
                    else:
                        parts.append(f"- {kp}")
                parts.append("")

            if student_example and (student_example.get("code") or student_example.get("scenario")):
                parts.append("#### 💻 4. Code & Walkthrough")
                if student_example.get("scenario"):
                    parts.append(f"*{student_example['scenario']}*\n")
                if student_example.get("code"):
                    parts.append(f"```text\n{student_example['code']}\n```")

            if exam_tip:
                parts.append(f"#### 🎯 5. Exam Tip\n> **University Tip**: {exam_tip}\n")

            if common_confusion and common_confusion.get("wrong"):
                parts.append(
                    f"#### ⚠️ 6. Common Confusion\n"
                    f"- ❌ **Mistake**: {common_confusion.get('wrong')}\n"
                    f"- ✅ **Clarification**: {common_confusion.get('correct')}\n"
                )

            if faqs:
                faq_item = faqs[0]
                parts.append(
                    f"#### ❓ 7. Frequently Asked Exam Question ({faq_item.get('marks', '2-Mark')})\n"
                    f"**Q: {faq_item.get('q', '')}**\n"
                    f"**Answer**: {faq_item.get('a', '')}\n"
                )

            if sources:
                parts.append("#### 📚 Academic References")
                for s in sources:
                    parts.append(f"- [{s['source_name']}: {s['title']}]({s['source_url']})")

            return "\n".join(parts), quick_check, sources

        # 2. If retrieval service found matching DB topics or sections
        if retrieval_data and retrieval_data.get("has_content"):
            topics = retrieval_data.get("matching_topics", [])
            primary_topic = topics[0]["title"] if topics else msg_clean.title()
            context_str = retrieval_data.get("context_str", "")

            response_parts = [
                f"### 🧠 {primary_topic}\n",
                f"Here is a comprehensive breakdown based on the **CodeOrbit Engineering Curriculum**:\n"
            ]

            if context_str:
                response_parts.append(f"{context_str}\n")
            else:
                response_parts.append(
                    f"**Core Concept**: {primary_topic} is a foundational building block in computer science engineering. "
                    f"It provides the core theoretical and practical mechanisms for university semester examinations.\n"
                )

            response_parts.append(
                "**Key Engineering Takeaways:**\n"
                "- Understand the problem definition and theoretical mechanics.\n"
                "- Analyze time and space complexity trade-offs where applicable.\n"
                "- Verify understanding using the checkpoint question below.\n"
            )

            if sources:
                response_parts.append("\n**📚 Academic References:**")
                for s in sources:
                    response_parts.append(f"- [{s['source_name']}: {s['title']}]({s['source_url']})")

            response_text = "\n".join(response_parts)
            return response_text, quick_check, sources

        # 3. General Engineering Academic response (Clean, zero filler)
        response_text = (
            f"### 💡 {msg_clean.title()}\n\n"
            f"In computer science engineering, analyzing **{msg_clean}** requires evaluating three core dimensions:\n\n"
            f"1. **Conceptual Definition**: How is the concept formally defined in university syllabus and standards?\n"
            f"2. **Internal Mechanics**: How does the algorithm, kernel structure, protocol, or schema maintain correctness?\n"
            f"3. **Practical Trade-offs**: What are the trade-offs in throughput, latency, memory consumption, and concurrency?\n\n"
            f"Ask me about any specific topic in **DBMS, OOPS, OS, DS, ML, CN**, or technical campus interviews!"
        )
        generic_quick_check = {
            "question": "In computer systems architecture, what design principle ensures components communicate solely through well-defined interfaces?",
            "options": ["Abstraction / Modularity", "Tight Coupling", "Global State Mutation", "Unconstrained Inheritance"],
            "correct_answer": "Abstraction / Modularity",
            "explanation": "Abstraction and modular encapsulation isolate implementation details and maintain clean component boundaries."
        }
        fallback_sources = []
        return response_text, generic_quick_check, fallback_sources

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        return {
            "why_wrong": f"You selected '{user_answer}'. While common, this choice does not satisfy the necessary conditions or represents an earlier/different architectural stage.",
            "core_concept": f"The verified correct answer is '{correct_answer}'. {explanation}",
            "real_world_example": "In semester examinations, always verify the formal definition and fundamental conditions before choosing an option.",
            "similar_question": {
                "prompt": f"Related Concept Check: {question_prompt[:90]}...",
                "options": [
                    {"text": correct_answer, "is_correct": True},
                    {"text": "Alternative Theoretical Model", "is_correct": False},
                    {"text": "Standard Baseline Case", "is_correct": False},
                    {"text": "None of the above", "is_correct": False}
                ],
                "explanation": f"Notice how '{correct_answer}' satisfies the foundational constraints directly."
            }
        }

    def review_interview_answer(self, prompt: str, student_answer: str) -> Dict[str, Any]:
        word_count = len(student_answer.split())
        
        if word_count < 25:
            score = 55
            clarity = "Brief and somewhat abrupt. Consider providing more context."
            depth = "Surface-level. Missing concrete technical decisions and constraints."
            structure = "Single block of text. Needs clear problem-action-resolution structure."
            missing = "Concrete examples, trade-offs encountered, and quantifiable outcomes."
            suggestions = "Use the STAR technique: specify the Situation, your exact Task, the technical Actions taken, and the measurable Result."
        elif word_count < 70:
            score = 75
            clarity = "Clear and articulate phrasing."
            depth = "Good fundamental explanation, though edge cases could be deepened."
            structure = "Logical progression from context to solution."
            missing = "Discussion of alternative approaches considered or architectural trade-offs."
            suggestions = "Highlight why you chose this specific approach over alternatives (e.g. why Redis vs in-memory caching)."
        else:
            score = 90
            clarity = "Excellent communication, crisp terminology, and easy to follow."
            depth = "Thorough technical analysis demonstrating practical engineering experience."
            structure = "Structured storytelling with clear problem framing, actions, and results."
            missing = "Minor: mention post-launch monitoring or lessons learned."
            suggestions = "Ready for top-tier tech interviews! Keep concise when speaking live."

        return {
            "overall_score": score,
            "feedback_clarity": clarity,
            "feedback_depth": depth,
            "feedback_structure": structure,
            "feedback_missing": missing,
            "feedback_suggestions": suggestions,
            "xp_earned": 25
        }


class OllamaProvider(AIProvider):
    """Integrates with local Ollama instance if available, with retrieval grounding."""

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.fallback = RuleBasedSmartProvider()

    def _is_healthy(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def chat_tutor(self, message: str, context: Optional[str] = None, retrieval_data: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[Dict[str, Any]], List[Dict[str, str]]]:
        if not self._is_healthy():
            return self.fallback.chat_tutor(message, context, retrieval_data)

        try:
            grounding = retrieval_data.get("context_str", "") if retrieval_data else ""
            system_prompt = (
                "You are CodeOrbit AI Tutor, an engineering and computer science professor. "
                "Ground your answer strictly in the provided curriculum context when available. "
                "Provide an educational, concise answer formatted with markdown headings, key takeaways, and code/diagrams if relevant."
            )
            payload = {
                "model": self.model,
                "prompt": f"{system_prompt}\nAcademic Context: {grounding}\nStudent Context: {context or 'General'}\nStudent Question: {message}",
                "stream": False
            }
            res = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=12)
            if res.status_code == 200:
                text = res.json().get("response", "")
                sources = retrieval_data.get("sources", []) if retrieval_data else []
                quick_check = retrieval_data.get("quick_check") if retrieval_data else None
                return text, quick_check, sources
        except Exception as e:
            logger.warning(f"Ollama request failed: {e}. Using fallback.")

        return self.fallback.chat_tutor(message, context, retrieval_data)

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        return self.fallback.explain_mistake(question_prompt, user_answer, correct_answer, explanation)

    def review_interview_answer(self, prompt: str, student_answer: str) -> Dict[str, Any]:
        return self.fallback.review_interview_answer(prompt, student_answer)


class OpenAIProvider(AIProvider):
    """Integrates with OpenAI through the dedicated OpenAITutorService."""

    def __init__(self):
        from app.services.ai_tutor import get_ai_tutor_service
        self.tutor_service = get_ai_tutor_service()
        self.fallback = RuleBasedSmartProvider()

    def chat_tutor(self, message: str, context: Optional[str] = None, retrieval_data: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[Dict[str, Any]], List[Dict[str, str]]]:
        if self.tutor_service.is_configured():
            ans, followups, model = self.tutor_service.generate_response(message, subject=context)
            sources = retrieval_data.get("sources", []) if retrieval_data else []
            quick_check = retrieval_data.get("quick_check") if retrieval_data else None
            return ans, quick_check, sources
        return self.fallback.chat_tutor(message, context, retrieval_data)

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        return self.fallback.explain_mistake(question_prompt, user_answer, correct_answer, explanation)

    def review_interview_answer(self, prompt: str, student_answer: str) -> Dict[str, Any]:
        return self.fallback.review_interview_answer(prompt, student_answer)


def get_ai_provider() -> AIProvider:
    """Factory to return configured AI provider with seamless fallback."""
    provider = settings.get_ai_provider()
    if provider == "openai" or settings.get_openai_api_key():
        return OpenAIProvider()
    if provider == "ollama":
        ollama_prov = OllamaProvider(settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL)
        if ollama_prov._is_healthy():
            return ollama_prov
    return RuleBasedSmartProvider()

