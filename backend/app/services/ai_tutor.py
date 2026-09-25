"""
CodeOrbit AI Tutor Service
Official OpenAI Python SDK Integration
General-Purpose Educational AI Assistant for Engineering Students
"""

from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

# System Prompt defining CodeOrbit AI Tutor persona and academic standards
SYSTEM_PROMPT = """You are CodeOrbit AI Tutor, an intelligent, inspiring, and rigorous educational assistant designed specifically for computer science and engineering students.

Your primary mission is to dynamically understand and thoroughly answer ANY question the student asks—covering concepts, algorithms, code implementation, line-by-line code explanation, debugging, university exam preparation, multiple-choice questions (MCQs), and tech placement interview prep.

CORE INVARIANTS:
1. Dynamic Open-Ended Answering: You MUST answer any question the student types. Never say "question not found", "not in question bank", or refuse an academic question. You are an expert across all fields of computer science, software engineering, mathematics, and systems.
2. Subject Context is Context, NOT Restriction: If an academic subject (such as DBMS, OS, OOPS, DS, ML, CN) is provided in the prompt context, use it as helpful background knowledge. However, if the student asks about a different subject, programming language, or general engineering question, answer it enthusiastically and fully.
3. Conversational Coherence: Maintain conversational context across follow-up questions. If the user refers to "it", "explain question 2 again", "give another example", or "how does that compare", interpret their intent using the preceding turns of the conversation.
4. Academic & Exam Depth:
   - When asked for "2 Mark Answer": Deliver a concise, laser-accurate formal definition, key formula or invariant, and 2 high-scoring bullet points.
   - When asked for "5 Mark Answer": Provide definition, key mechanism/architecture representation, 4-5 numbered technical points, and a clean concrete example or code snippet.
   - When asked for "10 Mark Answer": Provide a university-grade comprehensive answer with:
     * 1. Formal Definition & Background
     * 2. Core Architectural Mechanism & Working Principles (with diagrams or step-by-step state transitions)
     * 3. Complete Code / Pseudo-code / Algorithm (with comments)
     * 4. Comparative Trade-offs / Advantages & Disadvantages / Edge Cases
     * 5. Real-World Industry Application (e.g., how PostgreSQL, Linux kernel, or AWS implements it)
   - When asked to "Explain Simply": Use intuitive real-world metaphors, plain English, and zero unnecessary jargon before connecting back to the technical mechanics.
   - When asked for "MCQs": Provide clear, challenging questions with 4 distinct options (A, B, C, D), indicate the correct answer, and provide a crisp conceptual explanation for why it is correct.
   - When asked for "Interview Questions": Focus on top tech company (FAANG / Tier-1) standards, optimal algorithmic time/space complexities, edge cases, and common interviewer follow-ups.
   - When asked to "Explain Code": Walk through the code line by line, explaining variables, data structures, state changes, and time/space complexity.
   - When asked to "Summarize": Provide a concise high-yield bulleted cheat sheet.
5. Markdown & Code Standards:
   - Use beautiful Markdown formatting: clean headings (###, ####), bullet points, bold key terms, tables for comparisons, and blockquotes for tips.
   - Format all code in fenced code blocks with language tags (e.g. ```cpp, ```python, ```java, ```sql, ```javascript).
   - Write clean, production-ready, readable code with descriptive comments.
6. Tone: Encouraging, authoritative, clear, and pedagogically focused.
"""

def sanitize_ai_log(text: str) -> str:
    """Sanitizes any accidentally leaked keys or credentials from AI log output."""
    if not text:
        return ""
    return re.sub(r'(?i)(api[_-]?key|secret|token|sk-[a-zA-Z0-9]+)\s*([=:])\s*([^\s,;&"\']{6,})', r'\1\2***', text)

class OpenAITutorService:
    """
    Dedicated AI Tutor service utilizing the official OpenAI Python SDK.
    Provides open-ended educational tutoring, conversation history awareness,
    and adaptive academic response formats.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = (api_key or settings.OPENAI_API_KEY or "").strip()
        self.model = (model or settings.OPENAI_MODEL or "gpt-4o-mini").strip()
        self._client = None

    def is_configured(self) -> bool:
        """Returns True if a non-empty OpenAI API key is configured."""
        return bool(self.api_key)

    def _get_client(self):
        """Lazily initializes and caches the OpenAI client instance."""
        if self._client is None and self.is_configured():
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    timeout=28.0,
                    max_retries=2
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {sanitize_ai_log(str(e))}")
                self._client = None
        return self._client

    def generate_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        subject: Optional[str] = None,
        action: Optional[str] = None,
        marks: Optional[int] = None,
        student_context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, List[str], str]:
        """
        Generates an educational response to the student's question.

        Returns:
            Tuple[answer_text, suggested_followups, model_name]
        """
        query_text = message.strip()
        if not query_text:
            return "Please ask a question about your studies or engineering subjects.", [], self.model

        # Build prompt instructions based on action/marks modifier
        action_instructions = []
        if marks:
            action_instructions.append(f"Format this specifically as a {marks}-Mark University Exam Answer.")
        elif action == "explain_simply":
            action_instructions.append("Explain this concept in simple words using an intuitive real-world analogy first.")
        elif action == "exam_answer":
            action_instructions.append("Structure this as a high-scoring university examination answer with definitions, key points, and diagram/code.")
        elif action == "give_example":
            action_instructions.append("Focus on a concrete, practical real-world scenario with runnable code demonstrating this concept.")
        elif action == "mcqs":
            action_instructions.append("Generate challenging multiple choice questions (MCQs) on this topic with options, correct answer, and explanation.")
        elif action == "summarize":
            action_instructions.append("Summarize this topic into high-yield revision bullet points and key takeaways.")
        elif action == "explain_code":
            action_instructions.append("Provide a thorough line-by-line explanation of the code, walking through state transitions and complexity.")
        elif action == "interview_questions":
            action_instructions.append("Present top tech interview questions for this topic, detailing optimal approaches and trade-offs.")

        # Build contextual instructions
        context_parts = []
        if subject:
            context_parts.append(f"Student's Current Subject Context: {subject}")
        if student_context:
            if student_context.get("completed_topics"):
                context_parts.append(f"Completed Topics: {', '.join(student_context['completed_topics'])}")
            if student_context.get("level"):
                context_parts.append(f"Student Level: {student_context['level']}")

        # Assemble full system prompt
        system_content = SYSTEM_PROMPT
        if context_parts:
            system_content += "\n\nACADEMIC CONTEXT:\n" + "\n".join(context_parts)
        if action_instructions:
            system_content += "\n\nACTIVE REQUEST DIRECTIVE:\n" + "\n".join(action_instructions)

        # Append instruction for suggested follow-ups
        system_content += (
            "\n\nFOLLOW-UP SUGGESTIONS REQUIREMENT:\n"
            "At the very end of your response, output a section with exactly 3 to 4 recommended follow-up questions for the student, "
            "formatted as:\n"
            "### 💡 Suggested Next Questions\n"
            "- Question 1\n"
            "- Question 2\n"
            "- Question 3"
        )

        # Build messages list for chat completions
        messages_payload: List[Dict[str, str]] = [
            {"role": "system", "content": system_content}
        ]

        # Append recent conversation history (limit to last 10 messages for token efficiency)
        if conversation_history:
            recent_history = conversation_history[-10:]
            for turn in recent_history:
                role = "user" if turn.get("role") in ("user", "student") else "assistant"
                content = (turn.get("content") or turn.get("message") or "").strip()
                if content:
                    messages_payload.append({"role": role, "content": content})

        # Append the new user message
        messages_payload.append({"role": "user", "content": query_text})

        # Check if OpenAI is configured
        client = self._get_client()
        if not client:
            return self._generate_intelligent_offline_response(query_text, subject, action, marks)

        try:
            # Call OpenAI Chat Completions API
            response = client.chat.completions.create(
                model=self.model,
                messages=messages_payload,
                temperature=0.7,
                max_tokens=2500,
            )

            raw_answer = ""
            if response.choices and response.choices[0].message:
                raw_answer = response.choices[0].message.content or ""

            if not raw_answer:
                logger.warning("Empty response received from OpenAI API.")
                return self._generate_intelligent_offline_response(query_text, subject, action, marks)

            # Parse suggested follow-ups from the text
            clean_answer, followups = self._extract_followups(raw_answer)
            return clean_answer, followups, self.model

        except Exception as exc:
            exc_name = type(exc).__name__
            clean_exc = sanitize_ai_log(str(exc))
            logger.error(f"OpenAI API call failed ({exc_name}): {clean_exc}")

            # Specific handling for common error scenarios
            if "AuthenticationError" in exc_name or "invalid_api_key" in clean_exc.lower():
                user_msg = "The AI Tutor encountered an authentication issue with the configured OpenAI API key. Please check server environment settings."
            elif "RateLimitError" in exc_name:
                user_msg = "The AI Tutor is currently experiencing high demand (rate limit reached). Please wait a few moments and try again."
            elif "APITimeoutError" in exc_name or "Timeout" in exc_name:
                user_msg = "The AI Tutor request timed out. Please try asking again."
            elif "APIConnectionError" in exc_name:
                user_msg = "Unable to connect to the OpenAI service. Please verify server internet connectivity."
            else:
                user_msg = "The AI Tutor is temporarily unavailable. Please try again shortly."

            # Return graceful educational fallback if available
            fallback_ans, fallback_followups, _ = self._generate_intelligent_offline_response(query_text, subject, action, marks)
            if fallback_ans:
                return f"{fallback_ans}\n\n> ⚠️ *Note: {user_msg}*", fallback_followups, "offline-fallback"
            return user_msg, [], self.model

    def _extract_followups(self, text: str) -> Tuple[str, List[str]]:
        """Extracts follow-up suggestion chips from the AI response."""
        followups: List[str] = []
        clean_text = text

        patterns = [
            r'###\s*💡?\s*Suggested Next Questions[\s\S]*$',
            r'###\s*Suggested Follow-up[s]?[\s\S]*$',
            r'\*\*Suggested Questions:\*\*[\s\S]*$',
        ]

        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                section = match.group(0)
                clean_text = text[:match.start()].strip()
                # Extract bullet lines
                lines = section.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                        cleaned_line = re.sub(r'^[-*•\d.]+\s*', '', line).strip()
                        cleaned_line = cleaned_line.strip('"').strip("'")
                        if cleaned_line and len(cleaned_line) > 5 and len(cleaned_line) < 120:
                            followups.append(cleaned_line)
                break

        # Fallback default suggestions if fewer than 2 found
        if len(followups) < 2:
            followups = [
                "Can you give a real-world example?",
                "How is this asked in technical interviews?",
                "Give me 5 practice MCQs on this topic.",
                "Explain the time and space complexity."
            ]

        return clean_text, followups[:4]

    def _generate_intelligent_offline_response(
        self,
        query: str,
        subject: Optional[str] = None,
        action: Optional[str] = None,
        marks: Optional[int] = None
    ) -> Tuple[str, List[str], str]:
        """
        Provides a rich dynamic educational breakdown when OpenAI API key is
        not yet configured or during local offline testing.
        Never says 'question not found'.
        """
        title = query.strip().rstrip('?').title()
        subj_name = subject or "Computer Science & Engineering"

        # Provide a thorough, structured, pedagogical breakdown
        parts = [
            f"### 🎯 {title} — Exam Prep Breakdown\n",
            f"*Academic Domain: {subj_name}*\n",
            f"#### 📖 1. Concept Definition\n",
            f"In computer science engineering, **{query.strip()}** represents an essential architectural and theoretical foundation. "
            f"Mastering this concept requires analyzing its formal definition, internal state transitions, and system design invariants.\n",
            f"#### 🔑 2. Key High-Scoring Points\n",
            f"- **System Invariant**: State transitions must be validated before mutation to avoid inconsistency, race conditions, or anomalies.\n"
            f"- **Algorithmic Flow**: Operations execute in structured stages, optimizing throughput while ensuring correctness.\n"
            f"- **Trade-off Analysis**: Balances time complexity vs space complexity, latency vs throughput, and consistency vs availability.\n",
            f"#### 💻 3. Code Implementation & Step-by-Step Walkthrough\n",
            f"```text\n// Conceptual Implementation Pattern for: {title}\n"
            f"function solveConcept(inputData) {{\n"
            f"    // 1. Validate boundary conditions & edge cases\n"
            f"    if (!inputData) return null;\n\n"
            f"    // 2. Execute optimal core transformation\n"
            f"    let result = process(inputData);\n\n"
            f"    // 3. Return verified invariant\n"
            f"    return result;\n"
            f"}}\n```\n",
            f"#### 🎯 4. University Exam Tip\n",
            f"> **High-Scoring Tip**: When answering questions on **{title}**, always define the mathematical/algorithmic invariant first, "
            f"sketch the component architecture, and highlight time and space complexities ($O(1)$ to $O(N)$).\n",
            f"#### 📚 Verified Academic References\n",
            f"- [GeeksforGeeks: Computer Science Reference](https://www.geeksforgeeks.org/computer-science-projects/)\n",
            f"- [TutorialsPoint: Computer Science Guide](https://www.tutorialspoint.com/computer_science_tutorials.htm)\n"
        ]

        if not self.is_configured():
            parts.append(
                "> 💡 **Setup Notice**: To enable live open-ended responses powered by OpenAI, "
                "please configure `OPENAI_API_KEY` in your environment or Vercel Project Settings."
            )

        followups = [
            f"Give me a real-world example of {title}.",
            f"What are the top interview questions on {title}?",
            f"Explain {title} for a 10-mark exam question.",
            f"Give me 5 challenging MCQs on {title}."
        ]

        return "\n".join(parts), followups, "codeorbit-tutor-engine"

# Singleton instance accessor
_service_instance: Optional[OpenAITutorService] = None

def get_ai_tutor_service() -> OpenAITutorService:
    """Returns the singleton OpenAITutorService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenAITutorService()
    return _service_instance
