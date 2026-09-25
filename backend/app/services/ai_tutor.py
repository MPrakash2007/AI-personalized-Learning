"""
CodeOrbit AI Tutor Service
Official OpenAI Python SDK Integration
Academic University-Level Tutor for Computer Science & Engineering Students
"""

from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

# Academic System Prompt defining CodeOrbit AI Tutor persona and standards
SYSTEM_PROMPT = """You are CodeOrbit AI Tutor, an academic tutor for university computer science and engineering students.

Your primary purpose is to explain academic subjects clearly, rigorously, and pedagogically for semester examinations and university coursework.

The user's question must be answered according to the SUBJECT and TOPIC supplied by the application context.

CORE ACADEMIC PRINCIPLES:
1. Academic Accuracy & Relevance:
   - Always answer the actual question the student asked.
   - Never replace an academic explanation with generic software engineering concepts.
   - Never discuss race conditions, state transitions, invariants, architecture, time complexity, or software engineering patterns unless they are actually relevant to the user's question.
   - Never fabricate a generic 'algorithmic flow' for a theoretical academic question.
   - Never output irrelevant JavaScript such as solveConcept(), process(), or placeholder implementations.

2. Subject-Aware Expertise:
   - DBMS: Focus on relational models, normalization (1NF, 2NF, 3NF, BCNF, 4NF/5NF), functional dependencies, update/insertion/deletion anomalies, lossless join decomposition, dependency preservation, candidate keys, superkeys, ACID properties, transactions, concurrency control (2PL, timestamps, serializability), indexing (B-trees, B+ trees), relational algebra, and SQL.
   - Machine Learning: Focus on Bayes theorem, Naive Bayes (conditional independence assumption, prior, likelihood, posterior, evidence, Laplace smoothing), classification processes, regression, decision trees, SVM, neural networks, loss functions, overfitting/underfitting, and evaluation metrics (confusion matrix, precision, recall, F1, ROC-AUC).
   - Operating Systems: Focus on process management, CPU scheduling algorithms, process synchronization (critical section, semaphores, mutex, monitors), deadlocks (definition, 4 necessary Coffman conditions: mutual exclusion, hold and wait, no preemption, circular wait; resource allocation graphs; deadlock prevention, avoidance with Banker's algorithm, detection & recovery), memory management (paging, segmentation, TLB, page replacement), and file systems.
   - Computer Networks: Focus on OSI and TCP/IP models, TCP (connection-oriented, 3-way handshake, 4-way teardown, sliding window flow control, congestion control algorithms), UDP, IP addressing (IPv4, IPv6, CIDR, subnetting), routing protocols (distance vector, link state, OSPF, BGP), DNS, and HTTP/HTTPS.
   - Object-Oriented Programming (OOPS): Focus on the 4 pillars (Inheritance, Polymorphism, Encapsulation, Abstraction), constructors/destructors, access specifiers, interfaces, abstract classes, method overriding vs overloading, dynamic binding, and design principles.
   - Data Structures & Algorithms (DSA): Focus on algorithm design, step-by-step traces, time and space complexity analysis (best, average, worst cases), data structures (arrays, linked lists, stacks, queues, trees, heaps, graphs, hash tables), searching, sorting, and dynamic programming.

3. Question-Type Awareness:
   Before generating the response, internally determine the type of question asked:
   - A. Definition question: Provide a formal, precise syllabus definition with 2-4 key characteristics.
   - B. Concept explanation: Explain why the concept is needed, its core mechanism, components, and real academic examples.
   - C. Compare / Difference question: Use a clean Markdown comparison table with explicit evaluation criteria columns.
   - D. Algorithm question: State the algorithm, step-by-step procedure, walk through an example trace, and specify time & space complexities.
   - E. Numerical / Problem-solving question: State given values, governing formula, step-by-step mathematical substitution, and clear final result with units/conclusions.
   - F. Programming / Code question: Provide syntactically correct, well-commented code in the requested language, followed by a concise explanation of logic and complexity.
   - G. Short-answer exam question (2-Mark): Concise formal definition and 2-4 high-scoring bullet points.
   - H. Long-answer exam question (5/10/15-Mark): Comprehensive structured answer with definitions, working mechanisms, types, examples, diagrams/tables in text, and exam-oriented points.
   - I. Follow-up question: Continue seamlessly from previous conversation turns without restarting or losing subject context.
   (Do NOT print this internal question-type classification label in your output).

4. Strict Code Generation Rules:
   - DO NOT generate code for theoretical questions unless:
     * The user explicitly asks for code (e.g. "Give SQL example for normalization", "Implement binary search in C++"), OR
     * Code/SQL is genuinely necessary to explain the requested concept (e.g., SQL queries for DBMS, code for DSA algorithms).
   - For theoretical questions (e.g. "Explain normalization in DBMS", "What is deadlock in OS"), use relational schema notations, mathematical formulas, state tables, or bulleted breakdowns—NOT programming code.
   - Never use fake placeholder code such as solveConcept(inputData) or process(inputData).
   - Never use meaningless pseudo-code simply to fill an implementation section.

5. Exam-Oriented Response Format:
   For standard university theory questions, organize the response logically using this structure where applicable:
   - **Definition**: Formal academic definition.
   - **Need / Motivation**: Why the concept is needed and the problems/anomalies it solves.
   - **Core Concept**: Fundamental principles and rules.
   - **Detailed Explanation / Types / Forms**: Numbered or categorized breakdown.
   - **Academic Example**: Concrete example (e.g., student/department relations for DBMS, process/resource states for OS).
   - **Advantages & Disadvantages / Limitations**: Balanced analytical points.
   - **Important Exam Points**: Key takeaways and high-scoring exam points.
   - **Conclusion**: Crisp summary.
   (Adapt naturally; do not rigidly include sections that do not apply).

6. Marks-Based Depth:
   - 2 Marks: Precise definition + 2 to 4 bullet points.
   - 5 Marks: Definition + explanation + example + important points.
   - 10 / 13 / 15 Marks: Thorough, multi-section answer with deep explanations, examples, comparison tables where relevant, and exam tips.
   - Unspecified: Balanced, medium-to-detailed answer optimal for university semester preparation.

7. No Fabricated Citations:
   - Never generate fake "Verified Academic References" or random fabricated URLs.
   - If external references were not provided in the input context, rely purely on verified academic computer science knowledge without inventing citations.

8. Conversational Continuity:
   - Maintain multi-turn context. If the student asks a follow-up like "Explain 2NF with example" or "Give me a simple example", resolve references to the subject and topic previously discussed.

9. Response Tone & Formatting:
   - Professional, encouraging, clear, and academically authoritative.
   - Use clean Markdown with headers (###, ####), bold technical keywords, bullet points, and tables.
"""

def sanitize_ai_log(text: str) -> str:
    """Sanitizes any accidentally leaked keys or credentials from AI log output."""
    if not text:
        return ""
    return re.sub(r'(?i)(api[_-]?key|secret|token|sk-[a-zA-Z0-9]+)\s*([=:])\s*([^\s,;&"\']{6,})', r'\1\2***', text)

class OpenAITutorService:
    """
    Dedicated AI Tutor service utilizing the official OpenAI Python SDK.
    Provides academic university-level tutoring, conversation history awareness,
    and exam-oriented pedagogical response formats.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._explicit_api_key = (api_key or "").strip()
        self._explicit_model = (model or "").strip()
        self._client = None
        self._cached_key = None

    @property
    def api_key(self) -> str:
        """Dynamically resolves the OpenAI API key."""
        if self._explicit_api_key:
            return self._explicit_api_key
        return settings.get_openai_api_key()

    @property
    def model(self) -> str:
        """Dynamically resolves the OpenAI model name."""
        if self._explicit_model:
            return self._explicit_model
        return settings.get_openai_model()

    def is_configured(self) -> bool:
        """Returns True if a non-empty OpenAI API key is configured."""
        return bool(self.api_key)

    def _get_client(self):
        """Lazily initializes and caches the OpenAI client instance."""
        current_key = self.api_key
        if not current_key:
            return None
        if self._client is None or getattr(self, "_cached_key", None) != current_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=current_key,
                    timeout=28.0,
                    max_retries=2
                )
                self._cached_key = current_key
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {sanitize_ai_log(str(e))}")
                self._client = None
        return self._client

    def generate_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        subject: Optional[str] = None,
        topic: Optional[str] = None,
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
            action_instructions.append(f"Answer Format: Format this specifically as a {marks}-Mark University Examination Question. Scale response depth and points appropriately.")
        elif action == "explain_simply":
            action_instructions.append("Directive: Explain this concept in simple words using an intuitive real-world analogy first, followed by clear academic explanation.")
        elif action == "exam_answer":
            action_instructions.append("Directive: Structure this as a high-scoring university examination answer with definitions, key points, and academic example.")
        elif action == "give_example":
            action_instructions.append("Directive: Focus on a concrete, practical academic example illustrating this specific concept clearly.")
        elif action == "mcqs":
            action_instructions.append("Directive: Generate 4 to 5 challenging multiple choice questions (MCQs) on this topic with options A-D, correct answer, and explanation.")
        elif action == "summarize":
            action_instructions.append("Directive: Summarize this topic into high-yield revision bullet points and key exam takeaways.")
        elif action == "explain_code":
            action_instructions.append("Directive: Provide a thorough line-by-line explanation of the code, walking through logic, data structures, and time/space complexity.")
        elif action == "interview_questions":
            action_instructions.append("Directive: Present top technical interview questions for this topic, detailing optimal approaches and key considerations.")

        # Build structured contextual instructions
        context_parts = []
        if subject:
            context_parts.append(f"Subject: {subject}")
        if topic:
            context_parts.append(f"Topic: {topic}")
        context_parts.append(f"Student Question: {query_text}")
        context_parts.append("Academic Level: University / Undergraduate Computer Science")
        context_parts.append("Purpose: Semester Examination Preparation & Technical Mastery")
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
            "\n\nSUGGESTED FOLLOW-UP QUESTIONS REQUIREMENT:\n"
            "At the very end of your response, output a section with exactly 3 to 4 recommended academic follow-up questions for the student, "
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
            return self._generate_intelligent_offline_response(query_text, subject=subject, topic=topic, action=action, marks=marks)

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
                return self._generate_intelligent_offline_response(query_text, subject=subject, topic=topic, action=action, marks=marks)

            # Parse suggested follow-ups from the text
            clean_answer, followups = self._extract_followups(raw_answer)
            return clean_answer, followups, self.model

        except Exception as exc:
            exc_name = type(exc).__name__
            clean_exc = sanitize_ai_log(str(exc))
            logger.error(f"OpenAI API call failed ({exc_name}): {clean_exc}")

            # Specific handling for common error scenarios without substituting generic templates
            if "AuthenticationError" in exc_name or "invalid_api_key" in clean_exc.lower() or "401" in clean_exc:
                user_msg = "AI Tutor authentication failed. Please verify the OpenAI API key configuration in settings."
            elif "RateLimitError" in exc_name or "429" in clean_exc or "insufficient_quota" in clean_exc.lower():
                user_msg = "The AI Tutor is temporarily experiencing high demand or reached its quota limit. Please try again shortly."
            elif "APITimeoutError" in exc_name or "Timeout" in exc_name:
                user_msg = "The AI Tutor request timed out. Please try again."
            elif "APIConnectionError" in exc_name:
                user_msg = "Unable to connect to the AI Tutor service. Please try again shortly."
            else:
                user_msg = "The AI Tutor is temporarily unavailable. Please try again shortly."

            error_followups = [
                "Try asking your question again",
                "Explain in simpler words",
                "Give me a short summary",
                "What is the exam syllabus for this subject?"
            ]
            return user_msg, error_followups, "service-notice"

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
                lines = section.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                        cleaned_line = re.sub(r'^[-*•\d.]+\s*', '', line).strip()
                        cleaned_line = cleaned_line.strip('"').strip("'")
                        if cleaned_line and len(cleaned_line) > 5 and len(cleaned_line) < 120:
                            followups.append(cleaned_line)
                break

        if len(followups) < 2:
            followups = [
                "Can you give a practical exam example?",
                "How is this asked in semester examinations?",
                "Give me 5 practice MCQs on this topic.",
                "Summarize the key exam points."
            ]

        return clean_text, followups[:4]

    def _find_matching_curriculum_topic(
        self,
        query: str,
        subject: Optional[str] = None,
        topic: Optional[str] = None
    ) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Finds matching curriculum topic from curated datasets for offline fallback."""
        try:
            from curriculum import TOPIC_ACADEMIC_DATA
            from app.services.retrieval_service import ACRONYM_MAP
        except ImportError:
            return None

        clean = query.strip().lower()

        # 1. Direct topic slug
        if topic:
            clean_topic = topic.strip().lower().replace(" ", "-")
            if clean_topic in TOPIC_ACADEMIC_DATA:
                return clean_topic, TOPIC_ACADEMIC_DATA[clean_topic]

        # 2. Check acronym map
        for acronym, slug in ACRONYM_MAP.items():
            if acronym in clean:
                if slug in TOPIC_ACADEMIC_DATA:
                    return slug, TOPIC_ACADEMIC_DATA[slug]

        # 3. Direct slug or title match
        for slug, data in TOPIC_ACADEMIC_DATA.items():
            slug_spaced = slug.replace("-", " ")
            title_lower = data.get("title", "").lower()
            if slug in clean or slug_spaced in clean or (title_lower and title_lower in clean):
                if subject and data.get("subject", "").lower() == subject.lower():
                    return slug, data
                elif not subject:
                    return slug, data

        # 4. Token match for high-yield keywords
        tokens = [t for t in re.split(r'[\s\-_,?.!]+', clean) if len(t) > 3]
        for token in tokens:
            for slug, data in TOPIC_ACADEMIC_DATA.items():
                if token == slug or token in slug.split("-"):
                    if subject and data.get("subject", "").lower() == subject.lower():
                        return slug, data
                    elif not subject:
                        return slug, data

        return None

    def _generate_intelligent_offline_response(
        self,
        query: str,
        subject: Optional[str] = None,
        topic: Optional[str] = None,
        action: Optional[str] = None,
        marks: Optional[int] = None
    ) -> Tuple[str, List[str], str]:
        """
        Provides a rich academic breakdown when OpenAI API key is
        not yet configured or during local offline testing.
        Never generates placeholder code or generic templates.
        """
        title = query.strip().rstrip('?').title()
        subj_name = subject or "Computer Science & Engineering"

        # Check for verified academic curriculum data
        match = self._find_matching_curriculum_topic(query, subject=subject, topic=topic)
        if match:
            matched_slug, academic_data = match
            t_title = academic_data.get("title", title)
            t_subj = academic_data.get("subject", subj_name).upper()

            parts = [
                f"### 📘 {t_title}\n\n",
                f"*Academic Subject: {t_subj}*\n\n",
                f"#### 📖 1. Concept Definition\n",
                f"{academic_data.get('exam_definition', '')}\n\n",
                f"#### 🎯 2. Why It Is Needed & Core Concept\n",
                f"{academic_data.get('core_concept', '')}\n\n",
            ]

            # Key Points or Classification
            classification = academic_data.get("classification")
            if classification and classification.get("items"):
                parts.append(f"#### 🔑 3. {classification.get('title', 'Key Forms & Classifications')}\n")
                for item in classification["items"]:
                    parts.append(f"- **{item['name']}**: {item['desc']}\n")
                parts.append("\n")
            elif academic_data.get("key_points"):
                parts.append(f"#### 🔑 3. Key Concepts\n")
                for kp in academic_data["key_points"][:5]:
                    parts.append(f"- {kp}\n")
                parts.append("\n")

            # Example if available
            example = academic_data.get("example")
            if example:
                scenario = example.get("scenario")
                if scenario:
                    parts.append(f"#### 💡 4. Academic Example ({example.get('title', 'Standard Relation')})\n")
                    parts.append(f"{scenario}\n\n")
                # Include code only if explicitly requested or if it's SQL / DSA
                if (action in ("give_example", "explain_code") or "code" in query.lower() or "sql" in query.lower() or "program" in query.lower()) and example.get("code"):
                    lang = "sql" if t_subj == "DBMS" else "python"
                    parts.append(f"```{lang}\n{example.get('code')}\n```\n\n")

            # Exam Tip / Remember
            remember = academic_data.get("remember")
            if remember:
                parts.append(f"#### 📝 5. Important Exam Points\n")
                parts.append(f"> **Exam Summary**: {remember}\n\n")
            elif academic_data.get("exam_tip"):
                parts.append(f"#### 📝 5. Important Exam Points\n")
                parts.append(f"> **Exam Tip**: {academic_data.get('exam_tip')}\n\n")

            # References if available from academic dataset or content service
            references = academic_data.get("references")
            if not references:
                try:
                    from app.services.content_service import get_topic_references
                    references = get_topic_references(matched_slug, t_subj.lower())
                except Exception:
                    references = None

            if references:
                parts.append("#### 📚 Academic References\n")
                for ref in references:
                    parts.append(f"- [{ref.get('source_name', 'Reference')}: {ref.get('title', 'Curriculum Resource')}]({ref.get('source_url', '#')})\n")
                parts.append("\n")

            if not self.is_configured():
                parts.append(
                    "> 💡 **Setup Notice**: Live open-ended answers are powered by OpenAI. "
                    "Configure `OPENAI_API_KEY` in your environment or Vercel project settings to enable dynamic AI responses.\n\n"
                )

            followups = [
                f"Explain {t_title} for a 10-mark exam question.",
                f"What are the main advantages and limitations of {t_title}?",
                f"Give me practice exam questions on {t_title}.",
                f"How is {t_title} related to other {t_subj} topics?"
            ]
            return "".join(parts), followups, "curriculum-academic"

        # General clean academic fallback when no specific curriculum topic matches
        parts = [
            f"### 📘 {title}\n\n",
            f"*Academic Subject: {subj_name}*\n\n",
            f"#### 📖 1. Concept Definition\n",
            f"In university computer science examinations, **{query.strip()}** is an essential topic under **{subj_name}**.\n\n",
            f"#### 🎯 2. Core Academic Framework\n",
            f"When answering semester exam questions on this topic, structure your response as follows:\n",
            f"1. **Definition**: State the standard syllabus definition and key terminology.\n",
            f"2. **Why/Need**: Explain the problem this concept addresses and why it is essential in {subj_name}.\n",
            f"3. **Working Principle**: Detail the steps, laws, or mechanisms governing it.\n",
            f"4. **Academic Example**: Provide a concrete example (such as a relational schema, state diagram, or algorithm trace).\n",
            f"5. **Exam Points**: Summarize key formulas, rules, and common semester exam pitfalls.\n\n",
        ]

        if not self.is_configured():
            parts.append(
                "> 💡 **Setup Notice**: Live open-ended answers are powered by OpenAI. "
                "Configure `OPENAI_API_KEY` in your environment or Vercel project settings to enable dynamic AI responses.\n\n"
            )

        followups = [
            f"Explain {title} in simple words.",
            f"Give an exam-oriented example for {title}.",
            f"What are the key points to remember for {title}?",
            f"What are common mistakes students make on {title}?"
        ]

        return "".join(parts), followups, "codeorbit-academic-tutor"


# Singleton instance accessor
_service_instance: Optional[OpenAITutorService] = None

def get_ai_tutor_service() -> OpenAITutorService:
    """Returns the singleton OpenAITutorService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenAITutorService()
    return _service_instance
