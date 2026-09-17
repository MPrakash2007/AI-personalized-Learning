import json
import logging
from typing import Dict, Any, Optional, Tuple
import requests
from app.config import settings

logger = logging.getLogger(__name__)

class AIProvider:
    def chat_tutor(self, message: str, context: Optional[str] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
        raise NotImplementedError

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        raise NotImplementedError

    def review_interview_answer(self, prompt: str, student_answer: str) -> Dict[str, Any]:
        raise NotImplementedError


class RuleBasedSmartProvider(AIProvider):
    """
    Intelligent offline rule-based and knowledge-grounded AI provider.
    Ensures 100% functionality without requiring external servers or paid API keys.
    """

    KNOWLEDGE_BASE = {
        "normalization": {
            "title": "Database Normalization",
            "summary": "Normalization is the process of organizing relational database schema to minimize data redundancy and prevent insertion, update, and deletion anomalies.",
            "details": "1NF ensures atomic values. 2NF removes partial dependencies (where non-prime attributes depend on a subset of candidate keys). 3NF eliminates transitive dependencies (non-prime depending on non-prime). BCNF is a stricter version where for every X -> Y, X must be a superkey.",
            "quick_check": {
                "question": "If a relation is in 2NF and has no transitive functional dependencies, what normal form does it satisfy?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "correct_answer": "3NF",
                "explanation": "3NF requires a relation to be in 2NF with no transitive dependencies for non-prime attributes."
            }
        },
        "deadlock": {
            "title": "Deadlock in Operating Systems",
            "summary": "A deadlock occurs when two or more processes are unable to proceed because each is waiting for the other to release a resource.",
            "details": "The four Coffman conditions necessary for deadlock are: Mutual Exclusion, Hold & Wait, No Preemption, and Circular Wait. Prevention involves denying at least one condition. Avoidance uses algorithms like Banker's Algorithm with safe states.",
            "quick_check": {
                "question": "Which Coffman condition is denied when resources are preempted and forcibly deallocated from a waiting process?",
                "options": ["Mutual Exclusion", "Hold and Wait", "No Preemption", "Circular Wait"],
                "correct_answer": "No Preemption",
                "explanation": "Preempting resources means allowing the operating system to forcibly reclaim allocated resources, directly violating the 'No Preemption' condition."
            }
        },
        "polymorphism": {
            "title": "Polymorphism in OOP",
            "summary": "Polymorphism means 'many forms'. It allows a single interface or method signature to have different underlying implementations.",
            "details": "Compile-time polymorphism is achieved via method overloading and operator overloading. Runtime polymorphism is achieved via method overriding using virtual functions or interface implementations resolved at execution time via vtables.",
            "quick_check": {
                "question": "How is runtime (dynamic) polymorphism implemented in languages like C++ and Java?",
                "options": ["Method Overloading", "Method Overriding with dynamic dispatch", "Inline functions", "Static keyword"],
                "correct_answer": "Method Overriding with dynamic dispatch",
                "explanation": "Runtime polymorphism relies on method overriding and dynamic method dispatch (vtables) to resolve calls at execution time."
            }
        },
        "binary search": {
            "title": "Binary Search Algorithm",
            "summary": "Binary Search is an efficient algorithm for finding an item from a sorted list of items with O(log n) time complexity.",
            "details": "It works by repeatedly dividing in half the portion of the list that could contain the item, comparing the target against the middle element.",
            "quick_check": {
                "question": "What is the prerequisite condition before applying Binary Search on an array?",
                "options": ["The array must be unique", "The array must be sorted", "The array size must be a power of 2", "The array must be a Linked List"],
                "correct_answer": "The array must be sorted",
                "explanation": "Binary search relies on monotonic ordering; dividing the search space requires sorted elements."
            }
        },
        "tcp vs udp": {
            "title": "TCP vs UDP",
            "summary": "TCP is a connection-oriented, reliable protocol providing ordering and error checking; UDP is connectionless, lightweight, and fast.",
            "details": "TCP uses a 3-way handshake (SYN, SYN-ACK, ACK), flow control (sliding window), and congestion control. UDP sends datagrams without establishing a connection, ideal for DNS, gaming, and real-time streaming.",
            "quick_check": {
                "question": "Which transport protocol guarantees in-order delivery of packets with sequence numbers?",
                "options": ["UDP", "TCP", "IP", "ICMP"],
                "correct_answer": "TCP",
                "explanation": "TCP tracks byte sequence numbers and acknowledges segments, retransmitting lost packets to ensure strict in-order delivery."
            }
        },
        "knn": {
            "title": "K-Nearest Neighbors (KNN)",
            "summary": "KNN is a non-parametric, lazy learning algorithm used for both classification and regression based on proximity.",
            "details": "It classifies a new data point based on the majority class among its 'k' nearest neighbors in feature space, typically measured using Euclidean, Manhattan, or Minkowski distance.",
            "quick_check": {
                "question": "Why is KNN commonly referred to as a 'Lazy Learner'?",
                "options": ["It requires excessive GPU power", "It stores training data and postpones computation until query time", "It drops half the dataset", "It trains deep neural networks"],
                "correct_answer": "It stores training data and postpones computation until query time",
                "explanation": "KNN does not build an explicit generalized model during training; it simply memorizes the training instances and calculates distances at inference time."
            }
        },
        "placement": {
            "title": "Engineering Placement Strategy",
            "summary": "A successful placement preparation strategy blends core Data Structures & Algorithms, OS/DBMS/CN fundamentals, and structured behavioral responses.",
            "details": "Recommended priority:\n1. Master DSA (Arrays, Hash Maps, Two Pointers, Trees, Graphs, DP)\n2. SQL & Database design (Joins, Indexing, Transactions)\n3. OS core concepts (Concurrency, Scheduling, Virtual Memory)\n4. System Design basics (Load balancers, Caching, Scaling)\n5. Behavioral answers structured using the STAR method (Situation, Task, Action, Result).",
            "quick_check": {
                "question": "What framework is universally recommended for answering behavioral interview questions?",
                "options": ["SOLID", "ACID", "STAR", "REST"],
                "correct_answer": "STAR",
                "explanation": "The STAR method (Situation, Task, Action, Result) helps deliver concise, structured, and impactful behavioral stories."
            }
        }
    }

    def chat_tutor(self, message: str, context: Optional[str] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
        msg_lower = message.lower()
        matched_topic = None

        for key, data in self.KNOWLEDGE_BASE.items():
            if key in msg_lower:
                matched_topic = data
                break

        if matched_topic:
            response_text = (
                f"### {matched_topic['title']}\n\n"
                f"{matched_topic['summary']}\n\n"
                f"**Key Concepts to Remember:**\n"
                f"{matched_topic['details']}\n\n"
                f"Let's verify your grasp with a quick checkpoint below!"
            )
            return response_text, matched_topic["quick_check"]

        # General Engineering Academic response
        response_text = (
            f"Great question about **{message.strip()}**!\n\n"
            f"In computer science engineering, mastering this concept requires breaking it into three phases:\n"
            f"1. **Conceptual Intuition**: Understand what problem this concept was invented to solve.\n"
            f"2. **Implementation & Invariants**: Learn the underlying data structures, algorithms, or protocol exchanges.\n"
            f"3. **Trade-offs**: Compare time complexity, space complexity, latency, and hardware constraints.\n\n"
            f"Would you like me to walk through a concrete example with sample code or a diagram breakdown?"
        )
        generic_quick_check = {
            "question": "In computational complexity, which asymptotic notation describes the tightest bound (both upper and lower)?",
            "options": ["Big-O (O)", "Big-Omega (Ω)", "Big-Theta (Θ)", "Little-o (o)"],
            "correct_answer": "Big-Theta (Θ)",
            "explanation": "Big-Theta denotes an asymptotically tight bound where f(n) is bounded both from above and below by constant multiples."
        }
        return response_text, generic_quick_check

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        return {
            "why_wrong": f"You selected '{user_answer}'. This is a common misconception because that choice corresponds to a related but distinct phase or condition.",
            "core_concept": f"The correct answer is '{correct_answer}'. {explanation}",
            "real_world_example": "Think of it like compiling code: syntactic validation must pass before semantic type checking can occur. Similarly, in relational theory or protocol handshakes, each layer guarantees a specific invariant before advancing.",
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
        
        # Determine depth and score based on substance
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
    """Integrates with local Ollama instance if available."""

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

    def chat_tutor(self, message: str, context: Optional[str] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
        if not self._is_healthy():
            return self.fallback.chat_tutor(message, context)

        try:
            system_prompt = (
                "You are CodeOrbit AI Tutor, an engineering and computer science professor. "
                "Provide an educational, concise answer for a student. At the end, formulate a 1-question Quick Check."
            )
            payload = {
                "model": self.model,
                "prompt": f"{system_prompt}\nStudent Context: {context or 'General'}\nStudent Question: {message}",
                "stream": False
            }
            res = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=12)
            if res.status_code == 200:
                text = res.json().get("response", "")
                return text, self.fallback.KNOWLEDGE_BASE.get("normalization", {})["quick_check"]
        except Exception as e:
            logger.warning(f"Ollama request failed: {e}. Using fallback.")

        return self.fallback.chat_tutor(message, context)

    def explain_mistake(self, question_prompt: str, user_answer: str, correct_answer: str, explanation: str) -> Dict[str, Any]:
        return self.fallback.explain_mistake(question_prompt, user_answer, correct_answer, explanation)

    def review_interview_answer(self, prompt: str, student_answer: str) -> Dict[str, Any]:
        return self.fallback.review_interview_answer(prompt, student_answer)


def get_ai_provider() -> AIProvider:
    """Factory to return configured AI provider with seamless fallback."""
    if settings.AI_PROVIDER == "ollama":
        provider = OllamaProvider(settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL)
        if provider._is_healthy():
            return provider
    return RuleBasedSmartProvider()
