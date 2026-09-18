"""
CodeOrbit Seed Script
Supports:
  python seed.py          -> Idempotent seed (updates missing curriculum, questions, preserves user data)
  python seed.py --reset  -> Destructive reset (drops and recreates all tables)
Seeds:
  - 6 Subjects, 74 Topics
  - Rich educational content sections (from curriculum_data.py)
  - >= 20 Learn questions and >= 20 Practice questions per topic (from question_dataset.py)
  - Comprehensive Placement Hub Career questions across 14 categories
  - Demo user (demo@codeorbit.local / Demo@123) with streak and initial progress
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta

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

from curriculum_data import get_content_for_topic
from question_dataset import generate_topic_questions, CAREER_QUESTIONS
from app.services.content_service import get_topic_references

def seed_database(reset: bool = False):
    print("🌟 Initializing CodeOrbit database schema...")
    
    if reset:
        print("⚠️  --reset flag detected: Dropping all database tables for a fresh start...")
        Base.metadata.drop_all(bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Subjects & Topics Structure
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

        print("🚀 Seeding Subjects, Topics, Rich Content Sections, and Question Pools...")
        created_topics = {}

        for s_data in subjects_data:
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
                created_topics[t_slug] = topic

                # Seed/Update Lesson
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
                    db.flush()

                # Seed/Update Rich Content Sections
                # Seed/Update Rich Content Sections (12 required exam-oriented sections)
                existing_steps = db.query(LessonStep).filter(LessonStep.lesson_id == lesson.id).all()
                if len(existing_steps) < 12 or reset:
                    # Remove any legacy steps if re-seeding
                    for s in existing_steps:
                        db.delete(s)
                    db.flush()
                    
                    content_sections = get_content_for_topic(t_slug, t_title, subj.name)
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

                # Get verified references for this topic
                refs = get_topic_references(t_slug, subj.slug)
                gfg_ref = next((r for r in refs if "GeeksforGeeks" in r.get("source_name", "")), refs[0])
                tp_ref = next((r for r in refs if "TutorialsPoint" in r.get("source_name", "")), refs[-1])

                # Seed 20 LEARN Questions & 20 PRACTICE Questions
                existing_learn_q = db.query(Question).filter(
                    Question.topic_id == topic.id,
                    Question.question_context == "LEARN"
                ).count()
                
                if existing_learn_q < 15 or reset:
                    # Clear out existing for clean seeding if reset
                    if reset:
                        db.query(Question).filter(Question.topic_id == topic.id).delete()

                    learn_qs = generate_topic_questions(t_slug, t_title, subj.name, context="LEARN")
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

                existing_practice_q = db.query(Question).filter(
                    Question.topic_id == topic.id,
                    Question.question_context == "PRACTICE"
                ).count()

                if existing_practice_q < 15 or reset:
                    practice_qs = generate_topic_questions(t_slug, t_title, subj.name, context="PRACTICE")
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

                # Update any existing question with synthetic URLs to verified URLs
                for q in db.query(Question).filter(Question.topic_id == topic.id).all():
                    if f"/{t_slug}/" in (q.source_url or ""):
                        if q.question_context == "LEARN":
                            q.source_name = gfg_ref["source_name"]
                            q.source_url = gfg_ref["source_url"]
                        else:
                            q.source_name = tp_ref["source_name"]
                            q.source_url = tp_ref["source_url"]

        db.commit()
        print("✅ All 74 Topics seeded with rich content sections and 20+ Learn/Practice questions.")

        # 2. Seed Placement Hub Career Questions across all 14 categories
        print("💼 Seeding Placement Hub Career Questions across all 14 categories...")
        for cq in CAREER_QUESTIONS:
            exists = db.query(CareerQuestion).filter(CareerQuestion.title == cq["title"]).first()
            if not exists:
                db.add(CareerQuestion(
                    category=cq["category"],
                    sub_topic=cq["sub_topic"],
                    company_tag=cq["company_tag"],
                    difficulty=cq["difficulty"],
                    title=cq["title"],
                    problem_statement=cq["problem_statement"],
                    options_json=cq.get("options_json"),
                    correct_answer=cq.get("correct_answer"),
                    solution_hint=cq.get("solution_hint"),
                    xp_reward=25
                ))
        db.commit()
        print("✅ Placement Hub questions seeded successfully.")

        # 3. Gamification: Achievements, Quests, Challenges
        print("🏆 Seeding Achievements and Daily Quests...")
        achievements_data = [
            ("first_lesson", "Initiation", "Complete your first engineering lesson", "🎯", "bronze", 50),
            ("first_mastery", "Master of Core", "Attain 85%+ mastery in any topic", "⭐", "gold", 150),
            ("streak_7", "Relentless Orbit", "Maintain a 7-day study streak", "🔥", "gold", 200),
            ("questions_50", "Problem Solver", "Solve 50 practice questions accurately", "⚡", "silver", 100),
            ("boss_conqueror", "Titan Slayer", "Conquer a milestone Boss Challenge", "👑", "platinum", 300),
            ("ai_tutor_10", "Inquisitive Mind", "Ask 10 questions to the AI Tutor", "🤖", "silver", 75),
        ]
        created_achievements = {}
        for a_code, title, desc, icon, tier, xp in achievements_data:
            ach = db.query(Achievement).filter(Achievement.code == a_code).first()
            if not ach:
                ach = Achievement(code=a_code, title=title, description=desc, icon=icon, category=tier, xp_reward=xp)
                db.add(ach)
                db.flush()
            created_achievements[a_code] = ach

        quests_data = [
            ("Complete 2 Lessons", "lessons", 2, 60),
            ("Answer 10 Practice Questions", "questions", 10, 50),
            ("Earn 100 Study XP", "xp", 100, 40),
        ]
        created_quests = []
        for q_title, q_type, q_target, q_xp in quests_data:
            quest = db.query(DailyQuest).filter(DailyQuest.title == q_title).first()
            if not quest:
                quest = DailyQuest(title=q_title, quest_type=q_type, target_count=q_target, xp_reward=q_xp)
                db.add(quest)
                db.flush()
            created_quests.append(quest)

        # 4. Demo User setup (preserve progress if existing)
        print("👤 Setting up Demo Student Account (demo@codeorbit.local)...")
        demo_user = db.query(User).filter(User.email == "demo@codeorbit.local").first()
        today = datetime.now(timezone.utc).date()

        if not demo_user:
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

            demo_streak = LearningStreak(
                user_id=demo_user.id,
                current_streak=7,
                longest_streak=14,
                last_activity_date=today,
                freeze_count=2,
                weekly_history="M,T,W,T,F,S,S"
            )
            db.add(demo_streak)

            # Seed realistic completed topics for demo user:
            # DBMS Fundamentals, ER Model, Relational Model, Keys
            dbms_subj = db.query(Subject).filter(Subject.slug == "dbms").first()
            if dbms_subj:
                dbms_topics = db.query(Topic).filter(Topic.subject_id == dbms_subj.id).order_by(Topic.order.asc()).all()
                if len(dbms_topics) >= 4:
                    p1 = TopicProgress(
                        user_id=demo_user.id,
                        topic_id=dbms_topics[0].id,
                        status="MASTERED",
                        mastery_score=92.0,
                        accuracy=95.0,
                        recent_accuracy=90.0,
                        attempts_count=15,
                        correct_count=14,
                        completed_steps=12,
                        total_steps=12,
                        last_practiced_at=datetime.now(timezone.utc) - timedelta(days=2)
                    )
                    p2 = TopicProgress(
                        user_id=demo_user.id,
                        topic_id=dbms_topics[1].id,
                        status="COMPLETED",
                        mastery_score=85.0,
                        accuracy=88.0,
                        recent_accuracy=85.0,
                        attempts_count=12,
                        correct_count=10,
                        completed_steps=12,
                        total_steps=12,
                        last_practiced_at=datetime.now(timezone.utc) - timedelta(days=3)
                    )
                    p3 = TopicProgress(
                        user_id=demo_user.id,
                        topic_id=dbms_topics[2].id,
                        status="COMPLETED",
                        mastery_score=80.0,
                        accuracy=82.0,
                        recent_accuracy=80.0,
                        attempts_count=10,
                        correct_count=8,
                        completed_steps=12,
                        total_steps=12,
                        last_practiced_at=datetime.now(timezone.utc) - timedelta(days=4)
                    )
                    p4 = TopicProgress(
                        user_id=demo_user.id,
                        topic_id=dbms_topics[3].id,
                        status="COMPLETED",
                        mastery_score=78.0,
                        accuracy=80.0,
                        recent_accuracy=75.0,
                        attempts_count=8,
                        correct_count=6,
                        completed_steps=12,
                        total_steps=12,
                        last_practiced_at=datetime.now(timezone.utc) - timedelta(days=5)
                    )
                    db.add_all([p1, p2, p3, p4])

            # Seed User Achievements and Daily Quests
            if "first_lesson" in created_achievements:
                db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["first_lesson"].id))
            if "first_mastery" in created_achievements:
                db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["first_mastery"].id))
            if "streak_7" in created_achievements:
                db.add(UserAchievement(user_id=demo_user.id, achievement_id=created_achievements["streak_7"].id))

            for dq in created_quests:
                db.add(UserDailyQuest(
                    user_id=demo_user.id,
                    quest_id=dq.id,
                    current_count=1 if dq.quest_type == "lessons" else 5,
                    is_completed=False,
                    quest_date=today
                ))

            # Study Notes
            db.add(Note(
                user_id=demo_user.id,
                subject_id=dbms_subj.id if dbms_subj else None,
                topic_id=None,
                title="DBMS Fundamentals Revision Sheet",
                content="""# DBMS Key Principles
- **Three-Schema Architecture**: View Level, Logical Level, Physical Level.
- **Data Independence**: Modifying physical layout without breaking logical schemas or views.
- **ACID Invariants**: Atomicity, Consistency, Isolation, Durability.""",
                tags="dbms,architecture,acid"
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
    is_reset = "--reset" in sys.argv
    seed_database(reset=is_reset)
