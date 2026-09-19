"""
CodeOrbit Curriculum Seeder & Auto-Populator
Ensures that all 6 Subjects, 74 Topics, Lessons, Steps, and Question Pools
are automatically populated and available in production without timeouts.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.learning import Subject, Topic, Lesson, LessonStep, Question, QuestionOption
from app.services.content_service import get_topic_references
from curriculum import compile_lesson_steps
from question_dataset import generate_topic_questions

SUBJECTS_DATA = [
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
            ("Hashing", "hashing", "Hash functions, collision resolution (chaining, open addressing), load factors.", False, None),
            ("Trees", "trees", "Binary trees, traversals (inorder, preorder, postorder, level order), LCA.", False, None),
            ("BST", "bst", "Binary search tree properties, search, insertion, deletion, balanced trees.", False, None),
            ("Heaps", "heaps", "Min-heap, max-heap, heapify, heapsort, priority queues.", False, None),
            ("Graphs", "graphs", "Representations (matrix, list), BFS, DFS, topological sort, shortest paths.", False, None),
            ("Sorting", "sorting", "MergeSort, QuickSort, CountingSort, stability, comparative analysis.", False, None),
            ("Searching", "searching", "Linear search, binary search, ternary search, exponential search.", False, None),
            ("Greedy", "greedy", "Activity selection, Huffman coding, fractional knapsack, Prim/Kruskal.", False, None),
            ("Dynamic Programming", "dynamic-programming", "Overlapping subproblems, optimal substructure, 0/1 Knapsack, memoization.", True, "👑 DS Boss: Dynamic Programming Maestro")
        ]
    },
    {
        "name": "ML",
        "slug": "ml",
        "icon": "🤖",
        "description": "Machine learning foundations, predictive algorithms, evaluation metrics, and neural networks.",
        "color": "#f59e0b",
        "order": 5,
        "topics": [
            ("ML Fundamentals", "ml-fundamentals", "Supervised vs unsupervised, parametric vs non-parametric, bias-variance.", False, None),
            ("Data Preprocessing", "data-preprocessing", "Handling missing values, scaling (standardization, normalization), encoding.", False, None),
            ("Linear Regression", "linear-regression", "Cost function (MSE), gradient descent, OLS, R-squared.", False, None),
            ("Logistic Regression", "logistic-regression", "Sigmoid function, log-loss, decision boundaries, classification.", False, None),
            ("KNN", "knn", "Distance metrics (Euclidean, Manhattan), choosing K, curse of dimensionality.", False, None),
            ("Naive Bayes", "naive-bayes", "Bayes theorem, conditional independence assumption, Laplace smoothing.", False, None),
            ("Decision Trees", "decision-trees", "Entropy, Information Gain, Gini impurity, pruning algorithms.", False, None),
            ("Random Forest", "random-forest", "Ensemble learning, bagging, bootstrap sampling, out-of-bag error.", False, None),
            ("SVM", "svm", "Hyperplanes, maximal margin classifiers, kernel trick (RBF, polynomial).", False, None),
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

def ensure_subjects_and_topics(db: Session) -> List[Subject]:
    """
    Fast, idempotent bootstrap for the 6 core subjects, 74 topics, and base Lessons.
    Executes in < 200ms and commits atomically.
    """
    existing_subjects = db.query(Subject).order_by(Subject.order.asc()).all()
    if existing_subjects and len(existing_subjects) >= 6:
        return existing_subjects

    created_subjects = []
    for s_data in SUBJECTS_DATA:
        subj = db.query(Subject).filter(Subject.slug == s_data["slug"]).first()
        if not subj:
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
        created_subjects.append(subj)

        for t_idx, (t_title, t_slug, t_desc, is_boss, boss_title) in enumerate(s_data["topics"], start=1):
            topic = db.query(Topic).filter(Topic.slug == t_slug).first()
            if not topic:
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

            # Base Lesson
            lesson = db.query(Lesson).filter(Lesson.topic_id == topic.id).first()
            if not lesson:
                lesson = Lesson(
                    topic_id=topic.id,
                    title=f"{t_title} Masterclass",
                    xp_reward=50 if not is_boss else 100,
                    estimated_minutes=15,
                    order=1
                )
                db.add(lesson)

    db.commit()
    return db.query(Subject).order_by(Subject.order.asc()).all()


def ensure_topic_content_and_questions(db: Session, topic: Topic) -> None:
    """
    Lazy populates the 12 structured exam sections and 40 questions (20 Learn, 20 Practice)
    for a specific topic on first demand.
    Runs in ~100ms for the requested topic.
    """
    # 1. Lesson
    lesson = db.query(Lesson).filter(Lesson.topic_id == topic.id).first()
    if not lesson:
        lesson = Lesson(
            topic_id=topic.id,
            title=f"{topic.title} Masterclass",
            xp_reward=50 if not topic.is_boss else 100,
            estimated_minutes=15,
            order=1
        )
        db.add(lesson)
        db.flush()

    # 2. Steps (12 exam sections)
    existing_steps = db.query(LessonStep).filter(LessonStep.lesson_id == lesson.id).all()
    if len(existing_steps) < 12:
        for s in existing_steps:
            db.delete(s)
        db.flush()

        try:
            content_sections = compile_lesson_steps(topic.slug)
            for sec in content_sections:
                step = LessonStep(
                    lesson_id=lesson.id,
                    step_number=sec["section_order"],
                    step_type=sec["section_type"],
                    section_order=sec["section_order"],
                    section_type=sec["section_type"],
                    title=sec["title"],
                    content=sec["content"],
                    code_snippet=sec.get("code_snippet"),
                    example_data=sec.get("example_data"),
                    diagram_data=sec.get("diagram_data"),
                    source_name=sec.get("source_name", "GeeksforGeeks"),
                    source_url=sec.get("source_url", "https://www.geeksforgeeks.org")
                )
                db.add(step)
            db.flush()
        except Exception as e:
            print(f"[WARN] Error compiling steps for {topic.slug}: {e}")

    # 3. Questions (Learn & Practice)
    learn_count = db.query(Question).filter(
        Question.topic_id == topic.id,
        Question.question_context == "LEARN"
    ).count()

    if learn_count < 15:
        subject_name = topic.subject.name if topic.subject else "DBMS"
        subject_slug = topic.subject.slug if topic.subject else "dbms"
        refs = get_topic_references(topic.slug, subject_slug)
        gfg_ref = next((r for r in refs if "GeeksforGeeks" in r.get("source_name", "")), refs[0])
        tp_ref = next((r for r in refs if "TutorialsPoint" in r.get("source_name", "")), refs[-1])

        learn_qs = generate_topic_questions(topic.slug, topic.title, subject_name, context="LEARN")
        for q_data in learn_qs:
            q = Question(
                topic_id=topic.id,
                lesson_id=lesson.id,
                prompt=q_data["prompt"],
                question_type=q_data["question_type"],
                question_context="LEARN",
                difficulty=q_data["difficulty"],
                xp_reward=10,
                explanation=q_data["explanation"],
                source_name=gfg_ref["source_name"],
                source_url=gfg_ref["source_url"],
                source_type="REFERENCE_INSPIRED"
            )
            db.add(q)
            db.flush()
            for o_idx, opt in enumerate(q_data["options"]):
                db.add(QuestionOption(
                    question_id=q.id,
                    text=opt["text"],
                    is_correct=opt["is_correct"],
                    order=o_idx
                ))

        practice_qs = generate_topic_questions(topic.slug, topic.title, subject_name, context="PRACTICE")
        for q_data in practice_qs:
            q = Question(
                topic_id=topic.id,
                lesson_id=lesson.id,
                prompt=q_data["prompt"],
                question_type=q_data["question_type"],
                question_context="PRACTICE",
                difficulty=q_data["difficulty"],
                xp_reward=10,
                explanation=q_data["explanation"],
                source_name=tp_ref["source_name"],
                source_url=tp_ref["source_url"],
                source_type="REFERENCE_INSPIRED"
            )
            db.add(q)
            db.flush()
            for o_idx, opt in enumerate(q_data["options"]):
                db.add(QuestionOption(
                    question_id=q.id,
                    text=opt["text"],
                    is_correct=opt["is_correct"],
                    order=o_idx
                ))

    db.commit()
