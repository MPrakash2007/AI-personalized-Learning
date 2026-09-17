import os
import sys
import json
from datetime import datetime, timezone, timedelta, date

# Ensure app package is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from app.database import SessionLocal, Base, engine
from app.models.user import User, UserPreferences, LearningStreak, XPTransaction
from app.models.learning import (
    Subject, Topic, Lesson, LessonStep, Question, QuestionOption,
    UserQuestionAttempt, TopicProgress, Bookmark
)
from app.models.gamification import (
    Achievement, UserAchievement, DailyQuest, UserDailyQuest,
    Challenge, ChallengeAttempt
)
from app.models.analytics import StudyPlan, Note, AIRecommendation
from app.models.career import CareerQuestion, InterviewAttempt
from app.auth.security import hash_password

def seed_database():
    print("🌟 Initializing CodeOrbit database schema...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_sub = db.query(Subject).first()
        if existing_sub:
            print("Database already contains records. Clearing and reseeding for pristine demo state...")
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)

        print("🚀 Seeding Subjects and Topics...")
        subjects_data = [
            {
                "name": "DBMS",
                "slug": "dbms",
                "icon": "🗄️",
                "description": "Databases from ER diagrams to relational normalization and query optimization.",
                "color": "#06b6d4",
                "order": 1,
                "topics": [
                    ("DBMS Fundamentals", "dbms-fundamentals", "Architecture, data models, schema vs instance, 3-tier architecture.", False, None),
                    ("ER Model", "er-model", "Entities, attributes, relationships, cardinality, and ER-to-relational mapping.", False, None),
                    ("Relational Model", "relational-model", "Tuples, domains, relational algebra, operations, and integrity constraints.", False, None),
                    ("Keys", "keys", "Super keys, candidate keys, primary keys, foreign keys, alternate keys.", False, None),
                    ("SQL Basics", "sql-basics", "DDL, DML, DCL, basic SELECT, WHERE, operators, and data types.", False, None),
                    ("SQL Queries", "sql-queries", "GROUP BY, HAVING, Aggregate functions, ORDER BY, string functions.", False, None),
                    ("SQL Joins", "sql-joins", "INNER, LEFT, RIGHT, FULL OUTER, CROSS, and self joins.", False, None),
                    ("Nested Queries", "nested-queries", "Correlated and non-correlated subqueries, IN, EXISTS, ANY, ALL.", False, None),
                    ("Normalization", "normalization", "1NF, 2NF, 3NF, BCNF, lossless join, and dependency preservation.", False, None),
                    ("Transactions", "transactions", "ACID properties, transaction states, schedules, serializability.", False, None),
                    ("Concurrency Control", "concurrency-control", "Locking protocols, 2PL, Timestamp ordering, and deadlocks in databases.", False, None),
                    ("Indexing and Recovery", "indexing-and-recovery", "B-trees, B+ trees, dense/sparse indexing, WAL, and checkpoint recovery.", True, "👑 DBMS Boss: Indexing & Recovery Architect")
                ]
            },
            {
                "name": "OOPS",
                "slug": "oops",
                "icon": "🧩",
                "description": "Object-Oriented Programming principles, design patterns, and SOLID architecture.",
                "color": "#8b5cf6",
                "order": 2,
                "topics": [
                    ("OOP Fundamentals", "oop-fundamentals", "Paradigms, comparison with procedural programming, advantages.", False, None),
                    ("Classes and Objects", "classes-and-objects", "State, behavior, identity, memory allocation on heap/stack.", False, None),
                    ("Constructors", "constructors", "Default, parameterized, copy constructors, destructor lifecycles.", False, None),
                    ("Encapsulation", "encapsulation", "Data hiding, access specifiers (private, protected, public), getters and setters.", False, None),
                    ("Inheritance", "inheritance", "Single, multiple, multilevel, hierarchical, hybrid, and diamond problem.", False, None),
                    ("Polymorphism", "polymorphism", "Compile-time (overloading) vs runtime (overriding, vtables).", False, None),
                    ("Abstraction", "abstraction", "Abstract classes, pure virtual functions, conceptual modeling.", False, None),
                    ("Interfaces", "interfaces", "Multiple inheritance via interfaces, default methods, loose coupling.", False, None),
                    ("Exception Handling", "exception-handling", "Try-catch-finally, checked vs unchecked exceptions, custom errors.", False, None),
                    ("Generics", "generics", "Type safety, template metaprogramming, bounded wildcards.", False, None),
                    ("SOLID Principles", "solid-principles", "Single Responsibility, Open-Closed, Liskov, Interface Segregation, Dependency Inversion.", True, "👑 OOPS Boss: SOLID Architecture Master")
                ]
            },
            {
                "name": "OS",
                "slug": "os",
                "icon": "⚙️",
                "description": "Operating system internals, process concurrency, memory management, and file systems.",
                "color": "#ec4899",
                "order": 3,
                "topics": [
                    ("Operating System Fundamentals", "os-fundamentals", "Dual-mode operations, system calls, kernels (monolithic vs micro).", False, None),
                    ("Processes", "processes", "Process Control Block (PCB), context switching, state diagrams, fork().", False, None),
                    ("Threads", "threads", "User vs kernel threads, thread pools, multi-threading models.", False, None),
                    ("CPU Scheduling", "cpu-scheduling", "FCFS, SJF, Round Robin, Priority, Multi-level feedback queues.", False, None),
                    ("Process Synchronization", "process-synchronization", "Critical section, Peterson's solution, Semaphores, Mutex, Monitors.", False, None),
                    ("Deadlocks", "deadlocks", "Four Coffman conditions, Banker's algorithm, prevention and detection.", False, None),
                    ("Memory Management", "memory-management", "Contiguous allocation, paging, segmentation, internal/external fragmentation.", False, None),
                    ("Virtual Memory", "virtual-memory", "Demand paging, page faults, FIFO, LRU, Optimal page replacement.", False, None),
                    ("File Systems", "file-systems", "File organization, inode structure, allocation methods, directories.", False, None),
                    ("I/O Systems", "io-systems", "Polling, interrupts, DMA, disk scheduling (SSTF, SCAN, C-LOOK).", False, None),
                    ("Protection and Security", "protection-and-security", "Access matrix, authentication, buffer overflows, kernel defense.", True, "👑 OS Boss: Kernel Protection Master")
                ]
            },
            {
                "name": "DS",
                "slug": "ds",
                "icon": "🌳",
                "description": "Essential data structures, asymptotic complexity, trees, graphs, and algorithm design.",
                "color": "#10b981",
                "order": 4,
                "topics": [
                    ("Complexity Analysis", "complexity-analysis", "Big-O, Big-Omega, Big-Theta, recurrence relations, Master theorem.", False, None),
                    ("Arrays", "arrays", "Prefix sums, two pointers, sliding window, memory alignment.", False, None),
                    ("Strings", "strings", "String matching, KMP algorithm, Rabin-Karp, palindrome optimizations.", False, None),
                    ("Linked Lists", "linked-lists", "Singly, doubly, circular, Floyd's cycle detection, reverse in K-groups.", False, None),
                    ("Stacks", "stacks", "LIFO, monotonic stack, parenthesis validation, infix-to-postfix.", False, None),
                    ("Queues", "queues", "FIFO, circular queues, deques, priority queues, BFS foundations.", False, None),
                    ("Hashing", "hashing", "Hash functions, collision resolution (chaining, open addressing), load factor.", False, None),
                    ("Trees", "trees", "Binary trees, traversals (pre, in, post, level-order), height, diameter.", False, None),
                    ("BST", "bst", "Binary Search Tree properties, insertion, deletion, LCA, validation.", False, None),
                    ("Heaps", "heaps", "Min-heap, max-heap, heapify, heapsort, median in a stream.", False, None),
                    ("Graphs", "graphs", "Representations, BFS, DFS, topological sort, bipartite checking.", False, None),
                    ("Sorting", "sorting", "Quicksort, Mergesort, Countingsort, stability, lower bounds.", False, None),
                    ("Searching", "searching", "Binary search on answers, ternary search, exponential search.", False, None),
                    ("Greedy Algorithms", "greedy-algorithms", "Activity selection, fractional knapsack, Huffman coding.", False, None),
                    ("Backtracking", "backtracking", "N-Queens, Sudoku solver, subset generation, permutations.", False, None),
                    ("Dynamic Programming", "dynamic-programming", "Memoization vs tabulation, knapsack, LCS, LIS, matrix chain multiplication.", True, "👑 DS Boss: Dynamic Programming Grandmaster")
                ]
            },
            {
                "name": "ML",
                "slug": "ml",
                "icon": "🧠",
                "description": "Machine learning foundations, supervised and unsupervised modeling, and evaluation.",
                "color": "#f59e0b",
                "order": 5,
                "topics": [
                    ("ML Fundamentals", "ml-fundamentals", "Supervised, unsupervised, reinforcement learning, bias-variance tradeoff.", False, None),
                    ("Data Preprocessing", "data-preprocessing", "Handling missing values, feature scaling, one-hot encoding, train/test split.", False, None),
                    ("Linear Regression", "linear-regression", "Cost function, gradient descent, ordinary least squares, multi-variable.", False, None),
                    ("Logistic Regression", "logistic-regression", "Sigmoid function, binary cross-entropy, decision boundary, odds ratio.", False, None),
                    ("KNN", "knn", "K-Nearest Neighbors, distance metrics, curse of dimensionality.", False, None),
                    ("Naive Bayes", "naive-bayes", "Bayes theorem, conditional independence assumption, text classification.", False, None),
                    ("Decision Trees", "decision-trees", "Entropy, Information Gain, Gini impurity, pruning.", False, None),
                    ("Random Forest", "random-forest", "Ensemble methods, bagging, bootstrap aggregation, out-of-bag error.", False, None),
                    ("SVM", "svm", "Support Vector Machines, margins, kernel trick (RBF, polynomial).", False, None),
                    ("Clustering", "clustering", "K-Means, elbow method, silhouette score, hierarchical clustering.", False, None),
                    ("Model Evaluation", "model-evaluation", "Confusion matrix, precision, recall, F1-score, ROC-AUC, cross-validation.", True, "👑 ML Boss: Model Evaluation Maestro")
                ]
            },
            {
                "name": "CN",
                "slug": "cn",
                "icon": "🌐",
                "description": "Computer networks, protocol layers, routing, TCP/IP flow control, and web architecture.",
                "color": "#3b82f6",
                "order": 6,
                "topics": [
                    ("Networking Fundamentals", "networking-fundamentals", "Network topologies, transmission modes, packet vs circuit switching.", False, None),
                    ("OSI Model", "osi-model", "Seven layers, data encapsulation, PDU, headers and trailers.", False, None),
                    ("TCP/IP", "tcp-ip", "Four layers, IP suite, comparison with OSI model.", False, None),
                    ("Physical Layer", "physical-layer", "Bandwidth, Nyquist & Shannon theorems, guided vs unguided media.", False, None),
                    ("Data Link Layer", "data-link-layer", "Framing, error detection (CRC, parity), flow control (Stop-and-Wait, Go-Back-N).", False, None),
                    ("IP Addressing", "ip-addressing", "IPv4 classes, private vs public IP, IPv6 format.", False, None),
                    ("Subnetting", "subnetting", "CIDR notation, subnet masks, network and broadcast addresses.", False, None),
                    ("Routing", "routing", "Distance Vector, Link State, Dijkstra's algorithm, OSPF, BGP.", False, None),
                    ("TCP", "tcp", "3-way handshake, sliding window, congestion control (Slow Start, AIMD).", False, None),
                    ("UDP", "udp", "Datagram header, connectionless transport, comparison with TCP.", False, None),
                    ("HTTP/HTTPS", "http-https", "Request/response methods, status codes, cookies, SSL/TLS handshake.", False, None),
                    ("DNS", "dns", "Domain Name System resolution hierarchy, root servers, DNS caching.", False, None),
                    ("Application Layer", "application-layer", "FTP, SMTP, POP3, IMAP, DHCP protocol workflows.", False, None),
                    ("Network Security", "network-security", "Firewalls, symmetric vs asymmetric encryption, RSA, digital signatures.", True, "👑 CN Boss: Network Security Sentinel")
                ]
            }
        ]

        created_subjects = {}
        created_topics = {}

        for s_idx, s_data in enumerate(subjects_data):
            subj = Subject(
                name=s_data["name"],
                slug=s_data["slug"],
                icon=s_data["icon"],
                description=s_data["description"],
                color=s_data["color"],
                order=s_data["order"]
            )
            db.add(subj)
            db.flush()
            created_subjects[subj.slug] = subj

            for t_idx, (t_title, t_slug, t_desc, is_boss, boss_title) in enumerate(s_data["topics"], start=1):
                topic = Topic(
                    subject_id=subj.id,
                    title=t_title,
                    slug=t_slug,
                    description=t_desc,
                    order=t_idx,
                    is_boss=is_boss,
                    boss_title=boss_title
                )
                db.add(topic)
                db.flush()
                created_topics[t_slug] = topic

                # Seed a lesson for each topic
                lesson = Lesson(
                    topic_id=topic.id,
                    title=f"Core Masterclass: {t_title}",
                    xp_reward=50 if not is_boss else 100,
                    estimated_minutes=8,
                    order=1
                )
                db.add(lesson)
                db.flush()

                # Seed 6 Structured Steps for the lesson
                steps_data = [
                    (1, "understand", f"1. Understand: {t_title}", f"Gain foundational conceptual clarity on {t_title}. Learn the primary motivations, key terminology, and how this fits into engineering systems architecture.", None),
                    (2, "example", f"2. Real-World Example: {t_title}", f"Consider a production system: how does {t_title} prevent bugs, reduce latency, or enforce structural integrity under high load?", "-- Implementation Demonstration\n// Practical code pattern or schema definition"),
                    (3, "practice", f"3. Hands-on Practice: {t_title}", f"Interactive checkpoint: test your understanding of core properties before moving into advanced scenarios.", None),
                    (4, "apply", f"4. Apply to Engineering Systems", f"Analyze trade-offs, space-time complexities, and failure modes when deploying {t_title} in large-scale software.", None),
                    (5, "challenge", f"5. Challenge Checkpoint", f"A timed, high-stakes question to stretch your reasoning skills and ensure deep mastery.", None),
                    (6, "quiz", f"6. Topic Mastery Quiz", f"Final assessment. Solve comprehensive multiple-choice and scenario problems to unlock the next milestone.", None)
                ]

                for s_num, s_type, s_title, s_content, s_code in steps_data:
                    step = LessonStep(
                        lesson_id=lesson.id,
                        step_number=s_num,
                        step_type=s_type,
                        title=s_title,
                        content=s_content,
                        code_snippet=s_code
                    )
                    db.add(step)

        db.commit()
        print("✅ Subjects, Topics, and Lesson Steps seeded successfully.")

        # Seed Realistic High-Quality Questions across the topics
        print("🧠 Seeding Realistic Questions across multiple task types...")
        sample_questions = [
            # DBMS - Normalization
            {
                "topic_slug": "normalization",
                "prompt": "Which normal form removes partial functional dependencies on candidate keys?",
                "type": "mcq",
                "difficulty": "MEDIUM",
                "xp": 10,
                "explanation": "Second Normal Form (2NF) ensures that every non-prime attribute is fully functionally dependent on any candidate key of the relation, thereby eliminating partial dependency.",
                "options": [
                    ("1NF", False, "1NF only enforces atomicity of attribute values."),
                    ("2NF", True, "2NF directly eliminates partial dependencies on composite keys."),
                    ("3NF", False, "3NF removes transitive dependencies."),
                    ("BCNF", False, "BCNF is a stricter form of 3NF requiring every determinant to be a superkey.")
                ]
            },
            {
                "topic_slug": "normalization",
                "prompt": "In a relational schema R(A, B, C) with Functional Dependencies {A -> B, B -> C}, which normal form is violated?",
                "type": "mcq",
                "difficulty": "HARD",
                "xp": 15,
                "explanation": "Here, A is a candidate key. A -> B and B -> C creates a transitive dependency A -> C through non-prime attribute B. Therefore, R violates 3NF.",
                "options": [
                    ("Violates 1NF", False, "Values are atomic."),
                    ("Violates 2NF", False, "There is no partial dependency because A is a single attribute."),
                    ("Violates 3NF due to Transitive Dependency", True, "A -> B and B -> C creates a transitive dependency for non-key attribute C."),
                    ("Satisfies BCNF", False, "B is not a superkey in B -> C, so it cannot be BCNF.")
                ]
            },
            # DBMS - SQL Joins
            {
                "topic_slug": "sql-joins",
                "prompt": "Which SQL JOIN returns all rows from the left table, and matching rows from the right table, filling with NULL when there is no match?",
                "type": "mcq",
                "difficulty": "EASY",
                "xp": 5,
                "explanation": "LEFT JOIN (or LEFT OUTER JOIN) preserves all tuples from the left relation, padding unmatched right relation attributes with NULL.",
                "options": [
                    ("INNER JOIN", False, "Returns only tuples that have matches in both relations."),
                    ("LEFT OUTER JOIN", True, "Returns all left rows with NULL filled for non-matching right rows."),
                    ("CROSS JOIN", False, "Produces Cartesian product."),
                    ("RIGHT OUTER JOIN", False, "Preserves right rows instead.")
                ]
            },
            # DBMS - SQL Queries (SQL Challenge)
            {
                "topic_slug": "sql-queries",
                "prompt": "Write or select the correct SQL clause to filter aggregated groups having an average salary greater than 75,000:",
                "type": "sql_challenge",
                "difficulty": "MEDIUM",
                "xp": 15,
                "code_snippet": "SELECT department, AVG(salary) \nFROM employees \nGROUP BY department \n/* MISSING CLAUSE */ ;",
                "explanation": "HAVING filters groups created by GROUP BY, while WHERE filters individual rows before grouping.",
                "options": [
                    ("WHERE AVG(salary) > 75000", False, "WHERE cannot be applied directly on aggregate functions."),
                    ("HAVING AVG(salary) > 75000", True, "HAVING is evaluated after aggregation to filter groups."),
                    ("ORDER BY AVG(salary) > 75000", False, "ORDER BY specifies sort order, not filtering."),
                    ("FILTER BY AVG(salary) > 75000", False, "FILTER BY is not standard ANSI SQL syntax for groups.")
                ]
            },
            # OOPS - Polymorphism
            {
                "topic_slug": "polymorphism",
                "prompt": "Which OOP concept allows the same interface or method signature to have different underlying implementations?",
                "type": "mcq",
                "difficulty": "EASY",
                "xp": 5,
                "explanation": "Polymorphism ('many forms') allows an entity to take different forms at compile-time or runtime via overloading or overriding.",
                "options": [
                    ("Encapsulation", False, "Encapsulation binds data and methods together."),
                    ("Inheritance", False, "Inheritance derives attributes and methods from base classes."),
                    ("Polymorphism", True, "Polymorphism enables dynamic dispatch and uniform interfaces."),
                    ("Abstraction", False, "Abstraction hides internal details.")
                ]
            },
            # OS - CPU Scheduling
            {
                "topic_slug": "cpu-scheduling",
                "prompt": "Which CPU scheduling algorithm preempts running processes when their allocated time slice (quantum) expires?",
                "type": "mcq",
                "difficulty": "EASY",
                "xp": 5,
                "explanation": "Round Robin (RR) assigns a fixed time quantum per process in a cyclic FIFO queue.",
                "options": [
                    ("First-Come, First-Served (FCFS)", False, "FCFS is non-preemptive."),
                    ("Shortest Job First (SJF)", False, "Non-preemptive unless SRTF."),
                    ("Round Robin (RR)", True, "Round Robin uses a fixed time quantum with timer preemption."),
                    ("Priority Scheduling (Non-preemptive)", False, "Runs until process terminates or yields.")
                ]
            },
            # OS - Deadlocks
            {
                "topic_slug": "deadlocks",
                "prompt": "Which of the following is NOT one of the four Coffman conditions necessary for a deadlock?",
                "type": "mcq",
                "difficulty": "MEDIUM",
                "xp": 10,
                "explanation": "The four Coffman conditions are: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, and 4) Circular Wait. Process Preemption actually prevents deadlock.",
                "options": [
                    ("Mutual Exclusion", False, "This is an essential condition."),
                    ("Circular Wait", False, "This is an essential condition."),
                    ("No Preemption", False, "This is an essential condition."),
                    ("Process Preemption", True, "Process Preemption breaks condition 3 and prevents deadlocks.")
                ]
            },
            # DS - Complexity Analysis
            {
                "topic_slug": "complexity-analysis",
                "prompt": "What is the average and worst-case time complexity of Binary Search on a sorted array of size n?",
                "type": "mcq",
                "difficulty": "EASY",
                "xp": 5,
                "explanation": "Binary search halves the search range at each step: n, n/2, n/4, ..., 1. Hence, T(n) = O(log n).",
                "options": [
                    ("O(n)", False, "Linear search is O(n)."),
                    ("O(n log n)", False, "Sorting algorithms like mergesort are O(n log n)."),
                    ("O(log n)", True, "Binary search runs in logarithmic time O(log n)."),
                    ("O(1)", False, "Hash lookups are O(1) average, not binary search.")
                ]
            },
            # DS - Dynamic Programming
            {
                "topic_slug": "dynamic-programming",
                "prompt": "What two core properties must an algorithmic problem possess to be solvable using Dynamic Programming?",
                "type": "mcq",
                "difficulty": "HARD",
                "xp": 15,
                "explanation": "Dynamic Programming requires: 1) Optimal Substructure (optimal solution to problem contains optimal solutions to subproblems), and 2) Overlapping Subproblems (subproblems are revisited multiple times).",
                "options": [
                    ("Greedy choice property & Independent subproblems", False, "Greedy problems have independent subproblems."),
                    ("Optimal substructure & Overlapping subproblems", True, "These two define the fundamental applicability of DP."),
                    ("Divide and conquer & Disjoint sets", False, "Divide and conquer works on non-overlapping subproblems."),
                    ("Monotonic queue & Bipartite topology", False, "Unrelated structural properties.")
                ]
            },
            # ML - KNN
            {
                "topic_slug": "knn",
                "prompt": "Which algorithm is commonly used for nearest-neighbor classification based on distance metrics in feature space?",
                "type": "mcq",
                "difficulty": "EASY",
                "xp": 5,
                "explanation": "K-Nearest Neighbors (KNN) classifies an unknown instance based on the majority label of its k closest neighbors.",
                "options": [
                    ("KNN", True, "K-Nearest Neighbors relies on proximity in Euclidean/Manhattan space."),
                    ("K-Means", False, "K-Means is an unsupervised clustering algorithm."),
                    ("Linear Regression", False, "Used for continuous numeric prediction."),
                    ("PCA", False, "Principal Component Analysis is dimensionality reduction.")
                ]
            },
            # CN - TCP
            {
                "topic_slug": "tcp",
                "prompt": "Which transport layer protocol provides reliable, connection-oriented, and in-order byte stream delivery?",
                "type": "mcq",
                "difficulty": "EASY",
                "xp": 5,
                "explanation": "TCP establishes a virtual connection using a 3-way handshake and guarantees reliability via acknowledgements and sequence tracking.",
                "options": [
                    ("UDP", False, "UDP is connectionless and best-effort."),
                    ("TCP", True, "TCP guarantees reliable in-order transport."),
                    ("IP", False, "IP is network layer, best-effort packet delivery."),
                    ("ARP", False, "ARP resolves IP addresses to MAC addresses.")
                ]
            },
            # CN - IP Addressing & Subnetting
            {
                "topic_slug": "subnetting",
                "prompt": "What is the usable number of host addresses available in a /28 IPv4 subnet?",
                "type": "mcq",
                "difficulty": "MEDIUM",
                "xp": 10,
                "explanation": "A /28 subnet leaves 32 - 28 = 4 host bits. 2^4 = 16 total IP addresses. Subtracting network address and broadcast address yields 16 - 2 = 14 usable host IPs.",
                "options": [
                    ("16", False, "16 is the total IP count including network and broadcast."),
                    ("14", True, "2^(32-28) - 2 = 14 usable host addresses."),
                    ("30", False, "/27 provides 30 hosts."),
                    ("6", False, "/29 provides 6 hosts.")
                ]
            }
        ]

        for q_data in sample_questions:
            topic = created_topics.get(q_data["topic_slug"])
            if not topic:
                continue

            q = Question(
                topic_id=topic.id,
                prompt=q_data["prompt"],
                question_type=q_data["type"],
                difficulty=q_data["difficulty"],
                xp_reward=q_data["xp"],
                explanation=q_data["explanation"],
                code_snippet=q_data.get("code_snippet"),
                is_important=True
            )
            db.add(q)
            db.flush()

            for o_idx, (o_text, is_corr, o_exp) in enumerate(q_data["options"], start=1):
                opt = QuestionOption(
                    question_id=q.id,
                    text=o_text,
                    is_correct=is_corr,
                    explanation=o_exp,
                    order=o_idx
                )
                db.add(opt)

        db.commit()
        print("✅ Questions and options seeded successfully.")

        # Seed Achievements
        print("🏅 Seeding System Achievements...")
        achievements_data = [
            ("streak_7", "7 Day Streak", "Learned 7 consecutive days without missing a beat.", "🔥", "streak", 50),
            ("streak_30", "30 Day Master", "Maintained an unbroken 30-day learning journey.", "⚡", "streak", 150),
            ("xp_100", "Centurion", "Earned your first 100 XP on CodeOrbit.", "🎯", "xp", 25),
            ("xp_1000", "Kilobyte Scholar", "Surpassed 1,000 XP through lessons and challenges.", "🚀", "xp", 75),
            ("xp_2500", "Orbit Elite", "Reached 2,500 XP and joined the platform elite.", "💎", "xp", 100),
            ("first_mastery", "Concept Master", "Reached 85%+ mastery in your first engineering topic.", "🧠", "learning", 50),
            ("master_5", "Polymath", "Mastered 5 distinct topics across computer science.", "🏅", "learning", 120),
            ("first_boss", "Boss Slayer", "Defeated your first Major Milestone Boss Challenge.", "👑", "challenge", 100),
            ("perfect_10", "Flawless Decathlon", "Achieved 10 perfect scores on topic quizzes.", "✨", "quiz", 80),
            ("ai_tutor_10", "Curious Mind", "Collaborated with CodeOrbit AI Tutor 10 times.", "🤖", "ai", 40)
        ]

        created_achievements = {}
        for code, title, desc, icon, cat, xp_rew in achievements_data:
            ach = Achievement(
                code=code,
                title=title,
                description=desc,
                icon=icon,
                category=cat,
                xp_reward=xp_rew
            )
            db.add(ach)
            db.flush()
            created_achievements[code] = ach

        db.commit()

        # Seed Daily Quests
        print("🎯 Seeding Daily Quests...")
        daily_quests_data = [
            ("Complete 3 lessons", "lessons", 3, 30),
            ("Answer 10 questions", "questions", 10, 40),
            ("Review 1 weak concept", "review", 1, 30),
            ("Earn 100 XP today", "xp", 100, 50),
        ]
        created_quests = []
        for q_title, q_type, q_target, q_xp in daily_quests_data:
            dq = DailyQuest(
                title=q_title,
                quest_type=q_type,
                target_count=q_target,
                xp_reward=q_xp
            )
            db.add(dq)
            db.flush()
            created_quests.append(dq)
        db.commit()

        # Seed Challenges
        print("🏆 Seeding Challenges...")
        challenges_data = [
            ("DBMS SQL Sprint", "daily", created_subjects["dbms"].id, "Race against the clock to write joins and aggregations in under 10 minutes.", 10, 75, 5),
            ("DSA Speed Challenge", "weekly", created_subjects["ds"].id, "High-intensity array manipulation and search algorithms challenge.", 15, 120, 7),
            ("OS Concept Challenge", "weekly", created_subjects["os"].id, "Deadlock avoidance, scheduling mathematics, and virtual memory page faults.", 12, 100, 6),
            ("CN Networking Challenge", "monthly", created_subjects["cn"].id, "Comprehensive protocol examination from subnetting to socket architecture.", 20, 150, 10),
            ("DBMS SQL Boss Challenge", "boss", created_subjects["dbms"].id, "👑 Epic Boss Challenge: Solve SQL Joins, Aggregation, Subqueries, and Normalization design.", 25, 200, 8)
        ]
        for c_title, c_type, c_subj, c_desc, c_dur, c_xp, c_qcount in challenges_data:
            ch = Challenge(
                title=c_title,
                challenge_type=c_type,
                subject_id=c_subj,
                description=c_desc,
                duration_minutes=c_dur,
                xp_reward=c_xp,
                questions_count=c_qcount
            )
            db.add(ch)
        db.commit()

        # Seed Career Hub Questions
        print("💼 Seeding Placement & Career Questions...")
        career_data = [
            (
                "dsa", "Arrays", "Google", "MEDIUM",
                "Two Sum / Pair Target Sum",
                "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may not use the same element twice. Time complexity must be O(n).",
                None, "Hash Map Approach", "Store the complement `target - num` in a hash table with its index as you iterate.", 30
            ),
            (
                "dsa", "Trees", "Amazon", "MEDIUM",
                "Lowest Common Ancestor in Binary Tree",
                "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q. The LCA is defined as the lowest node that has both p and q as descendants.",
                None, "Post-order Recursion", "Recursively search left and right subtrees. If both return non-null, root is LCA.", 35
            ),
            (
                "dsa", "Dynamic Programming", "Microsoft", "HARD",
                "Longest Increasing Subsequence",
                "Given an integer array nums, return the length of the longest strictly increasing subsequence. Optimize from O(n^2) to O(n log n).",
                None, "Patience Sorting / Binary Search", "Maintain tails array where tails[i] stores the smallest tail of all increasing subsequences of length i+1.", 45
            ),
            (
                "mcq", "DBMS", "Service Companies", "MEDIUM",
                "Difference between TRUNCATE and DELETE",
                "Which statement correctly compares TRUNCATE and DELETE in relational databases?",
                json.dumps([
                    "DELETE is DDL while TRUNCATE is DML",
                    "TRUNCATE is faster because it deallocates data pages without row-by-row logging, whereas DELETE logs each deleted tuple",
                    "TRUNCATE can be filtered with a WHERE clause",
                    "DELETE resets the auto-increment identity seed while TRUNCATE does not"
                ]),
                "TRUNCATE is faster because it deallocates data pages without row-by-row logging, whereas DELETE logs each deleted tuple",
                "TRUNCATE is a DDL operation that drops storage extents, making it drastically faster than DML DELETE.", 20
            ),
            (
                "interview_tech", "System Design & Architecture", "Product Companies", "HARD",
                "Design a Scalable URL Shortener (e.g. TinyURL)",
                "Explain the end-to-end architecture of a URL shortening service handling 100M new URLs/month. Address base62 encoding vs hashing, database choice (SQL vs NoSQL), caching layer with Redis, and unique ID generation.",
                None, None, "Highlight unique ID generation (Snowflake ID or counter service), Base62 conversion, write-through caching, and 301 vs 302 redirects.", 40
            ),
            (
                "interview_hr", "Behavioral", "All Companies", "EASY",
                "Tell me about a challenging project bug and how you resolved it.",
                "Describe a situation in a college or internship project where you encountered an unexpected system failure or concurrency bug. How did you diagnose, debug, and resolve the root cause?",
                None, None, "Use the STAR method: Situation (project context), Task (what failed), Action (profiling, logs, debugger), Result (restored stability and lessons learned).", 30
            )
        ]
        for c_cat, c_sub, c_comp, c_diff, c_title, c_prob, c_opts, c_ans, c_hint, c_xp in career_data:
            cq = CareerQuestion(
                category=c_cat,
                sub_topic=c_sub,
                company_tag=c_comp,
                difficulty=c_diff,
                title=c_title,
                problem_statement=c_prob,
                options_json=c_opts,
                correct_answer=c_ans,
                solution_hint=c_hint,
                xp_reward=c_xp
            )
            db.add(cq)
        db.commit()

        # Seed Demo User
        print("👤 Seeding Populated Demo User (demo@codeorbit.local)...")
        demo_user = User(
            email="demo@codeorbit.local",
            hashed_password=hash_password("Demo@123"),
            full_name="Alex Rivera",
            college="National Institute of Technology",
            degree="B.Tech",
            branch="Computer Science & Engineering",
            graduation_year=2026,
            avatar_url="https://api.dicebear.com/7.x/bottts/svg?seed=AlexOrbit",
            is_admin=True,
            level=12,
            xp=2450,
            gems=450,
            onboarding_completed=True
        )
        db.add(demo_user)
        db.flush()

        # User Preferences
        demo_prefs = UserPreferences(
            user_id=demo_user.id,
            programming_level="Intermediate",
            preferred_subjects="DBMS,DS,OS",
            daily_target_minutes=45,
            career_goal="Placement preparation",
            theme="dark",
            sound_effects=True,
            daily_reminder=True
        )
        db.add(demo_prefs)

        # 7-day streak
        today = datetime.now(timezone.utc).date()
        demo_streak = LearningStreak(
            user_id=demo_user.id,
            current_streak=7,
            longest_streak=14,
            last_activity_date=today,
            freeze_count=2,
            weekly_history="M,T,W,T,F,S,S"
        )
        db.add(demo_streak)

        # Seed topic progress for demo user
        dbms_topics = db.query(Topic).filter(Topic.subject_id == created_subjects["dbms"].id).order_by(Topic.order.asc()).all()

        # 1. DBMS Fundamentals: Mastered (88%)
        p1 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[0].id,
            status="MASTERED",
            mastery_score=92.0,
            accuracy=95.0,
            recent_accuracy=90.0,
            attempts_count=12,
            correct_count=11,
            completed_steps=6,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=6)
        )
        # 2. ER Model: Mastered (85%)
        p2 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[1].id,
            status="MASTERED",
            mastery_score=88.0,
            accuracy=88.0,
            recent_accuracy=85.0,
            attempts_count=10,
            correct_count=9,
            completed_steps=6,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=5)
        )
        # 3. Relational Model: Mastered (85%)
        p3 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[2].id,
            status="COMPLETED",
            mastery_score=85.0,
            accuracy=85.0,
            recent_accuracy=80.0,
            attempts_count=8,
            correct_count=7,
            completed_steps=6,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=4)
        )
        # 4. Keys: Mastered (85%)
        p4 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[3].id,
            status="COMPLETED",
            mastery_score=85.0,
            accuracy=85.0,
            recent_accuracy=85.0,
            attempts_count=7,
            correct_count=6,
            completed_steps=6,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=3)
        )
        # 5. SQL Basics: Mastered (90%)
        p5 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[4].id,
            status="COMPLETED",
            mastery_score=82.0,
            accuracy=80.0,
            recent_accuracy=85.0,
            attempts_count=6,
            correct_count=5,
            completed_steps=6,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        # 6. SQL Queries: Mastered (76%)
        p6 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[5].id,
            status="COMPLETED",
            mastery_score=76.0,
            accuracy=75.0,
            recent_accuracy=78.0,
            attempts_count=5,
            correct_count=4,
            completed_steps=5,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        # 7. SQL Joins: In Progress (74%)
        p7 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[6].id,
            status="IN_PROGRESS",
            mastery_score=74.0,
            accuracy=74.0,
            recent_accuracy=70.0,
            attempts_count=6,
            correct_count=4,
            completed_steps=4,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(hours=8)
        )
        # 8. Normalization: Weak Concept (43% accuracy for AI Recommendation demo!)
        p9 = TopicProgress(
            user_id=demo_user.id,
            topic_id=dbms_topics[8].id,
            status="IN_PROGRESS",
            mastery_score=43.0,
            accuracy=43.0,
            recent_accuracy=40.0,
            attempts_count=7,
            correct_count=3,
            completed_steps=3,
            total_steps=6,
            last_practiced_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        db.add_all([p1, p2, p3, p4, p5, p6, p7, p9])

        # Add question attempts for Normalization to reflect real mistakes in DB
        norm_questions = db.query(Question).filter(Question.topic_id == dbms_topics[8].id).all()
        for q in norm_questions:
            att = UserQuestionAttempt(
                user_id=demo_user.id,
                question_id=q.id,
                topic_id=dbms_topics[8].id,
                selected_answer="1NF",
                is_correct=False,
                time_taken_seconds=34
            )
            db.add(att)

        # Unlock Achievements for demo user
        db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["streak_7"].id))
        db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["xp_100"].id))
        db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["xp_1000"].id))
        db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["first_mastery"].id))

        # Assign today's quests
        for dq in created_quests:
            cur = 2 if dq.quest_type == "lessons" else (6 if dq.quest_type == "questions" else 50)
            db.add(UserDailyQuest(
                user_id=demo_user.id,
                quest_id=dq.id,
                current_count=cur,
                is_completed=False,
                quest_date=today
            ))

        # Study Planner tasks
        db.add(StudyPlan(
            user_id=demo_user.id,
            title="DBMS – Normalization Deep Dive",
            subject_name="DBMS",
            topic_name="Normalization",
            scheduled_time="5:00 PM",
            scheduled_date=today,
            is_completed=False
        ))
        db.add(StudyPlan(
            user_id=demo_user.id,
            title="DS – Trees Traversal Practice",
            subject_name="DS",
            topic_name="Trees",
            scheduled_time="6:00 PM",
            scheduled_date=today,
            is_completed=False
        ))
        db.add(StudyPlan(
            user_id=demo_user.id,
            title="Placement – DSA Two Sum & LCA",
            subject_name="Placement",
            topic_name="DSA Track",
            scheduled_time="7:30 PM",
            scheduled_date=today,
            is_completed=True
        ))

        # Study Notes
        db.add(Note(
            user_id=demo_user.id,
            subject_id=created_subjects["dbms"].id,
            topic_id=dbms_topics[8].id,
            title="Normalization Rules & Anomalies Summary",
            content="""# Normalization Key Takeaways
- **1NF**: Atomic attributes, no repeating groups.
- **2NF**: In 1NF + No partial dependency (non-prime depending on subset of candidate key).
- **3NF**: In 2NF + No transitive dependency (non-prime depending on another non-prime).
- **BCNF**: For every functional dependency X -> Y, X must be a superkey.""",
            tags="normalization,dbms,bcnf,acid"
        ))
        db.add(Note(
            user_id=demo_user.id,
            subject_id=created_subjects["os"].id,
            topic_id=None,
            title="Operating System Deadlock Checklist",
            content="""### 4 Coffman Conditions
1. Mutual Exclusion
2. Hold & Wait
3. No Preemption
4. Circular Wait
*If any ONE condition is denied, deadlocks cannot occur!*""",
            tags="os,deadlocks,concurrency"
        ))

        # AI Recommendations
        db.add(AIRecommendation(
            user_id=demo_user.id,
            category="needs_attention",
            title="Practice Functional Dependencies",
            reason="You have answered 4 of the last 7 normalization questions incorrectly (43% accuracy).",
            estimated_minutes=8,
            action_url="/learn/dbms/normalization",
            subject_id=created_subjects["dbms"].id,
            topic_id=dbms_topics[8].id,
            is_active=True
        ))
        db.add(AIRecommendation(
            user_id=demo_user.id,
            category="due_for_review",
            title="Review ER-to-Relational Mapping",
            reason="It has been 5 days since you reviewed ER Model concepts. Quick review prevents memory decay.",
            estimated_minutes=5,
            action_url="/smart-review",
            subject_id=created_subjects["dbms"].id,
            topic_id=dbms_topics[1].id,
            is_active=True
        ))
        db.add(AIRecommendation(
            user_id=demo_user.id,
            category="ready_to_advance",
            title="Continue SQL Joins Lesson",
            reason="You're 65% through SQL Joins. Complete step 5 & 6 to unlock Nested Queries.",
            estimated_minutes=10,
            action_url="/learn/dbms/sql-joins",
            subject_id=created_subjects["dbms"].id,
            topic_id=dbms_topics[6].id,
            is_active=True
        ))
        db.add(AIRecommendation(
            user_id=demo_user.id,
            category="recommended_challenge",
            title="DBMS SQL Boss Sprint",
            reason="You have completed 6 DBMS topics. Test your comprehensive skills against the SQL Boss Challenge.",
            estimated_minutes=15,
            action_url="/challenges",
            subject_id=created_subjects["dbms"].id,
            is_active=True
        ))

        # Leaderboard Peers (to populate realistic competitive leaderboard)
        peers = [
            ("Priya Sharma", "priya@codeorbit.local", "IIT Bombay", 15, 3400, 18, 92.0),
            ("Rohan Verma", "rohan@codeorbit.local", "BITS Pilani", 14, 2950, 12, 86.5),
            ("Ananya Iyer", "ananya@codeorbit.local", "NIT Trichy", 13, 2680, 9, 81.0),
            ("Vikram Patel", "vikram@codeorbit.local", "IIIT Hyderabad", 11, 2210, 5, 74.0),
            ("Sneha Roy", "sneha@codeorbit.local", "Delhi Technological University", 10, 1950, 4, 69.5),
            ("Karan Mehta", "karan@codeorbit.local", "Jadavpur University", 9, 1680, 3, 62.0),
        ]
        for p_name, p_email, p_col, p_lvl, p_xp, p_strk, p_mast in peers:
            peer_u = User(
                email=p_email,
                hashed_password=hash_password("Demo@123"),
                full_name=p_name,
                college=p_col,
                degree="B.Tech",
                branch="Computer Science",
                graduation_year=2026,
                avatar_url=f"https://api.dicebear.com/7.x/bottts/svg?seed={p_name.replace(' ', '')}",
                level=p_lvl,
                xp=p_xp,
                gems=200,
                onboarding_completed=True
            )
            db.add(peer_u)
            db.flush()
            db.add(LearningStreak(
                user_id=peer_u.id,
                current_streak=p_strk,
                longest_streak=p_strk + 4,
                last_activity_date=today,
                weekly_history="M,T,W,T,F,S,S"
            ))

        db.commit()
        print("🎉 Database seeding completed successfully!")
        print("Demo credentials: demo@codeorbit.local / Demo@123")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding error: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
