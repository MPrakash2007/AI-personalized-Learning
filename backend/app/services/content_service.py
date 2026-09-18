"""
CodeOrbit Content Service
Manages verified educational reference mappings (GeeksforGeeks, TutorialsPoint),
structured section schemas, and educational metadata for all 74 core CS topics.
"""

from typing import Dict, Any, List, Optional

# Verified reference sources
SOURCES = {
    "gfg": {
        "name": "GeeksforGeeks",
        "domain": "https://www.geeksforgeeks.org",
        "type": "REFERENCE"
    },
    "tutorialspoint": {
        "name": "TutorialsPoint",
        "domain": "https://www.tutorialspoint.com",
        "type": "REFERENCE"
    }
}

# Standard section types for comprehensive educational content
SECTION_TYPES = [
    "exam_definition",
    "core_concept",
    "key_points",
    "classification",
    "how_it_works",
    "example",
    "comparison",
    "formula",
    "exam_tip",
    "common_confusion",
    "important_questions",
    "revision_60s"
]

# Verified Subject Hub URLs (used as safe fallback when a subtopic is unspecified)
SUBJECT_HUB_URLS: Dict[str, Dict[str, str]] = {
    "dbms": {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/dbms/",
        "title": "DBMS Tutorial — GeeksforGeeks"
    },
    "oops": {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/",
        "title": "OOPS Concepts Tutorial — GeeksforGeeks"
    },
    "os": {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/operating-systems/",
        "title": "Operating Systems Tutorial — GeeksforGeeks"
    },
    "ds": {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/data-structures/",
        "title": "Data Structures Tutorial — GeeksforGeeks"
    },
    "ml": {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/machine-learning/",
        "title": "Machine Learning Tutorial — GeeksforGeeks"
    },
    "cn": {
        "source_name": "GeeksforGeeks",
        "source_url": "https://www.geeksforgeeks.org/computer-network-tutorials/",
        "title": "Computer Networks Tutorial — GeeksforGeeks"
    }
}

# Verified topic-to-reference map for all 74 topics across 6 core subjects
TOPIC_REFERENCE_MAP: Dict[str, List[Dict[str, str]]] = {
    # =========================================================================
    # 1. DBMS (12 Topics)
    # =========================================================================
    "dbms-fundamentals": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-dbms-database-management-system-set-1/", "title": "Introduction to DBMS"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/dbms_overview.htm", "title": "DBMS Overview & Architecture"}
    ],
    "er-model": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-er-model/", "title": "Introduction of ER Model"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/er_model_basic_concepts.htm", "title": "ER Model Concepts"}
    ],
    "relational-model": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/relational-model-in-dbms/", "title": "Relational Model in DBMS"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/relational_data_model.htm", "title": "Relational Database Model"}
    ],
    "keys": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/types-of-keys-in-relational-model-candidate-super-primary-alternate-and-foreign-keys/", "title": "Types of Keys in Relational Model"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/dbms_keys.htm", "title": "DBMS Keys Explained"}
    ],
    "sql-basics": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/sql-ddl-dql-dml-dcl-tcl-commands/", "title": "SQL Commands (DDL, DML, DCL, TCL)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/sql/sql-syntax.htm", "title": "SQL Syntax & Basics"}
    ],
    "sql-queries": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/aggregate-functions-in-sql/", "title": "SQL Aggregate Functions and Group By"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/sql/sql-group-by.htm", "title": "SQL GROUP BY & HAVING Clause"}
    ],
    "sql-joins": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/sql-join-set-1-inner-left-right-and-full-joins/", "title": "SQL Joins (Inner, Left, Right, Full)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/sql/sql-using-joins.htm", "title": "SQL Joins Tutorial"}
    ],
    "nested-queries": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/nested-queries-in-sql/", "title": "Nested & Correlated Subqueries in SQL"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/sql/sql-sub-queries.htm", "title": "SQL Subqueries Guide"}
    ],
    "normalization": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-database-normalization/", "title": "Database Normalization (1NF to BCNF)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/database_normalization.htm", "title": "Database Normalization Rules"}
    ],
    "transactions": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/acid-properties-in-dbms/", "title": "ACID Properties & Transaction Schedules"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/dbms_transaction.htm", "title": "DBMS Transaction Overview"}
    ],
    "concurrency-control": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/concurrency-control-techniques-in-dbms/", "title": "Concurrency Control Techniques in DBMS"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/dbms_concurrency_control.htm", "title": "Concurrency Control Systems"}
    ],
    "indexing-and-recovery": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/", "title": "B-Trees, B+ Trees & Database Indexing"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/dbms/dbms_indexing.htm", "title": "Database Indexing & Recovery"}
    ],

    # =========================================================================
    # 2. OOPS (11 Topics)
    # =========================================================================
    "oop-fundamentals": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/", "title": "Object-Oriented Programming (OOPs) Concepts"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/object_oriented_analysis_design/ooad_object_oriented_principles.htm", "title": "OOP Principles"}
    ],
    "classes-and-objects": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/classes-objects-java/", "title": "Classes and Objects in Java"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_classes_objects.htm", "title": "C++ Classes and Objects"}
    ],
    "constructors": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/constructors-in-java/", "title": "Constructors in Java & OOP"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_constructor_destructor.htm", "title": "Constructors & Destructors"}
    ],
    "encapsulation": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/encapsulation-in-java/", "title": "Encapsulation in Java and OOP"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_data_encapsulation.htm", "title": "Data Encapsulation in C++"}
    ],
    "inheritance": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/inheritance-in-java/", "title": "Inheritance in Java & OOP"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_inheritance.htm", "title": "C++ Inheritance Types"}
    ],
    "polymorphism": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/polymorphism-in-java/", "title": "Polymorphism in Java (Overloading vs Overriding)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_polymorphism.htm", "title": "Polymorphism in C++"}
    ],
    "abstraction": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/abstraction-in-java-2/", "title": "Abstraction in Java & Abstract Classes"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_interfaces.htm", "title": "Data Abstraction in C++"}
    ],
    "interfaces": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/interfaces-in-java/", "title": "Interfaces in Java and Multiple Inheritance"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/java/java_interfaces.htm", "title": "Java Interfaces Tutorial"}
    ],
    "exception-handling": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/exceptions-in-java/", "title": "Exceptions in Java & Exception Handling"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_exceptions_handling.htm", "title": "C++ Exception Handling"}
    ],
    "generics": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/generics-in-java/", "title": "Generics in Java and Type Safety"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_templates.htm", "title": "C++ Templates & Generics"}
    ],
    "solid-principles": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/solid-principles-in-java/", "title": "SOLID Principles in Software Design"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/design_pattern/design_pattern_tutorial.htm", "title": "Design Patterns & SOLID"}
    ],

    # =========================================================================
    # 3. OS (11 Topics)
    # =========================================================================
    "os-fundamentals": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-operating-system-set-1/", "title": "Introduction to Operating System"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_overview.htm", "title": "Operating System Overview"}
    ],
    "processes": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-process-management/", "title": "Introduction of Process Management"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_processes.htm", "title": "OS Process States & PCB"}
    ],
    "threads": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/thread-in-operating-system/", "title": "Threads in Operating System"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_multi_threading.htm", "title": "OS Multithreading"}
    ],
    "cpu-scheduling": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/", "title": "CPU Scheduling in Operating Systems"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_process_scheduling_algorithms.htm", "title": "Process Scheduling Algorithms"}
    ],
    "process-synchronization": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-process-synchronization/", "title": "Process Synchronization and Semaphores"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_process_synchronization.htm", "title": "OS Process Synchronization"}
    ],
    "deadlocks": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/", "title": "Deadlocks in Operating System & Banker's Algorithm"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_deadlocks.htm", "title": "OS Deadlock Handling"}
    ],
    "memory-management": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/memory-management-in-operating-system/", "title": "Memory Management in Operating System"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_memory_management.htm", "title": "OS Memory Management Schemes"}
    ],
    "virtual-memory": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/virtual-memory-in-operating-system/", "title": "Virtual Memory in Operating System"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_virtual_memory.htm", "title": "OS Virtual Memory & Demand Paging"}
    ],
    "file-systems": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/file-systems-in-operating-system/", "title": "File Systems in Operating System"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_file_system.htm", "title": "OS File System Architecture"}
    ],
    "io-systems": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/i-o-hardware/", "title": "I/O Hardware & Disk Scheduling"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_io_hardware.htm", "title": "OS I/O Hardware Management"}
    ],
    "protection-and-security": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/protection-and-security-in-operating-system/", "title": "Protection and Security in Operating System"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/operating_system/os_security.htm", "title": "OS Security Principles"}
    ],

    # =========================================================================
    # 4. DS (15 Topics)
    # =========================================================================
    "complexity-analysis": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/understanding-time-complexity-simple-examples/", "title": "Understanding Time Complexity with Examples"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/asymptotic_analysis.htm", "title": "Asymptotic Analysis"}
    ],
    "arrays": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/array-data-structure/", "title": "Array Data Structure Guide"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/array_data_structure.htm", "title": "Arrays in DSA"}
    ],
    "strings": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/string-data-structure/", "title": "String Data Structure and Algorithms"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/cplusplus/cpp_strings.htm", "title": "Strings and String Operations"}
    ],
    "linked-lists": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/data-structures/linked-list/", "title": "Linked List Data Structure (Singly, Doubly, Circular)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/linked_list_program_in_c.htm", "title": "Linked Lists Tutorial"}
    ],
    "stacks": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/stack-data-structure/", "title": "Stack Data Structure and Applications"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/stack_algorithm.htm", "title": "Stack Algorithm & LIFO"}
    ],
    "queues": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/queue-data-structure/", "title": "Queue Data Structure (FIFO, Circular, Deque)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/dsa_queue.htm", "title": "Queue Operations in DSA"}
    ],
    "hashing": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/hashing-data-structure/", "title": "Hashing Data Structure and Collision Resolution"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/hash_data_structure.htm", "title": "Hash Table Data Structure"}
    ],
    "trees": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/binary-tree-data-structure/", "title": "Binary Tree Data Structure and Traversals"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/tree_data_structure.htm", "title": "Tree Data Structure Overview"}
    ],
    "bst": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/binary-search-tree-data-structure/", "title": "Binary Search Tree (BST) Operations"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/binary_search_tree.htm", "title": "Binary Search Tree Guide"}
    ],
    "heaps": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/heap-data-structure/", "title": "Heap Data Structure (Min-Heap, Max-Heap)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/heap_data_structure.htm", "title": "Heap Data Structure"}
    ],
    "graphs": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/", "title": "Graph Data Structure and Algorithms"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/graph_data_structure.htm", "title": "Graph Algorithms"}
    ],
    "sorting": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/sorting-algorithms/", "title": "Sorting Algorithms Analysis and Comparison"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/sorting_algorithms.htm", "title": "Sorting Techniques"}
    ],
    "searching": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/searching-algorithms/", "title": "Searching Algorithms (Linear, Binary, Ternary)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/linear_search_algorithm.htm", "title": "Searching Algorithms Overview"}
    ],
    "greedy": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/greedy-algorithms/", "title": "Greedy Algorithms Paradigm"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/greedy_algorithms.htm", "title": "Greedy Algorithms Tutorial"}
    ],
    "dynamic-programming": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/fundamentals-of-dynamic-programming/", "title": "Fundamentals of Dynamic Programming (Memoization & Tabulation)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_structures_algorithms/dynamic_programming.htm", "title": "Dynamic Programming Guide"}
    ],

    # =========================================================================
    # 5. ML (11 Topics)
    # =========================================================================
    "ml-fundamentals": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/machine-learning/", "title": "Machine Learning Fundamentals"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning/index.htm", "title": "Machine Learning Concepts"}
    ],
    "data-preprocessing": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/data-preprocessing-machine-learning-python/", "title": "Data Preprocessing for Machine Learning"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_data_preprocessing.htm", "title": "ML Data Preprocessing"}
    ],
    "linear-regression": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/ml-linear-regression/", "title": "Linear Regression in Machine Learning"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_linear_regression.htm", "title": "Linear Regression Tutorial"}
    ],
    "logistic-regression": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/understanding-logistic-regression/", "title": "Understanding Logistic Regression for Classification"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_classification_algorithms_logistic_regression.htm", "title": "Logistic Regression Algorithm"}
    ],
    "knn": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/k-nearest-neighbours/", "title": "K-Nearest Neighbours (KNN) Algorithm"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_knn_algorithm_finding_nearest_neighbors.htm", "title": "KNN Algorithm Guide"}
    ],
    "naive-bayes": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/naive-bayes-classifiers/", "title": "Naive Bayes Classifiers in Machine Learning"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_classification_algorithms_naive_bayes.htm", "title": "Naive Bayes Classification"}
    ],
    "decision-trees": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/decision-tree/", "title": "Decision Tree Algorithm Explained"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_classification_algorithms_decision_tree.htm", "title": "Decision Tree Algorithm"}
    ],
    "random-forest": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/random-forest-algorithm-in-machine-learning/", "title": "Random Forest Algorithm in Machine Learning"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_classification_algorithms_random_forest.htm", "title": "Random Forest Ensemble"}
    ],
    "svm": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/support-vector-machine-algorithm/", "title": "Support Vector Machine (SVM) Algorithm"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_classification_algorithms_support_vector_machine.htm", "title": "SVM Algorithm in Python"}
    ],
    "clustering": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/k-means-clustering-introduction/", "title": "K-Means Clustering Algorithm"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_clustering_algorithms_k_means.htm", "title": "Clustering Algorithms"}
    ],
    "model-evaluation": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/metrics-for-machine-learning-model/", "title": "Metrics for Machine Learning Model Evaluation"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/machine_learning_with_python/machine_learning_with_python_performance_metrics.htm", "title": "Performance Metrics in ML"}
    ],

    # =========================================================================
    # 6. CN (14 Topics)
    # =========================================================================
    "networking-fundamentals": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/basics-computer-networking/", "title": "Basics of Computer Networking"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/index.htm", "title": "Data Communication & Computer Network"}
    ],
    "osi-model": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/layers-of-osi-model/", "title": "Layers of OSI Model (7-Layer Architecture)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/osi_model.htm", "title": "OSI Reference Model"}
    ],
    "tcp-ip": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/tcp-ip-model/", "title": "TCP/IP Model Architecture and Protocols"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/tcp_ip_model.htm", "title": "TCP/IP Suite Overview"}
    ],
    "physical-layer": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/physical-layer-in-osi-model/", "title": "Physical Layer in OSI Model"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/physical_layer_introduction.htm", "title": "Physical Layer Fundamentals"}
    ],
    "data-link-layer": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-of-data-link-layer/", "title": "Introduction to Data Link Layer (Framing, Flow Control, Error Control)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/data_link_layer_introduction.htm", "title": "Data Link Layer Tutorial"}
    ],
    "ip-addressing": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/ip-addressing-introduction-and-classful-addressing/", "title": "IP Addressing (IPv4 Classful vs IPv6)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/network_layer_introduction.htm", "title": "Network Layer Addressing"}
    ],
    "subnetting": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/introduction-to-subnetting/", "title": "Introduction to Subnetting and CIDR"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/subnetting_in_computer_network.htm", "title": "Subnetting Guide"}
    ],
    "routing": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/routing-protocols-in-computer-network/", "title": "Routing Protocols in Computer Network (Distance Vector & Link State)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/routing_algorithms.htm", "title": "Routing Algorithms in CN"}
    ],
    "tcp": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/what-is-transmission-control-protocol-tcp/", "title": "Transmission Control Protocol (TCP 3-Way Handshake)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/transmission_control_protocol.htm", "title": "TCP Protocol Mechanics"}
    ],
    "udp": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/user-datagram-protocol-udp/", "title": "User Datagram Protocol (UDP Datagram Header)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/user_datagram_protocol.htm", "title": "UDP Protocol Guide"}
    ],
    "http-https": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/http-full-form/", "title": "HTTP and HTTPS Protocols (Request/Response & SSL/TLS)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/http/index.htm", "title": "HTTP Tutorial"}
    ],
    "dns": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/domain-name-system-dns-in-application-layer/", "title": "Domain Name System (DNS) in Application Layer"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/domain_name_system.htm", "title": "DNS Protocol Architecture"}
    ],
    "application-layer": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/application-layer-in-osi-model/", "title": "Application Layer in OSI Model (FTP, SMTP, DHCP)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/application_layer_introduction.htm", "title": "Application Layer Protocols"}
    ],
    "network-security": [
        {"source_name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/network-security-basics/", "title": "Network Security Basics (Firewalls & Cryptography)"},
        {"source_name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/data_communication_computer_network/network_security.htm", "title": "Network Security Tutorial"}
    ]
}


def get_topic_references(topic_slug: str, subject_slug: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Retrieve trusted, verified reference URLs for a given topic slug.
    Never generates synthetic unverified URLs like 'geeksforgeeks.org/{topic_slug}/'.
    If a specific topic is missing, gracefully falls back to the verified subject hub URL.
    """
    if topic_slug in TOPIC_REFERENCE_MAP:
        return TOPIC_REFERENCE_MAP[topic_slug]

    # Safe verified fallback: Return the subject's official tutorial hub
    if subject_slug and subject_slug in SUBJECT_HUB_URLS:
        return [SUBJECT_HUB_URLS[subject_slug]]

    # General computer science verified portal fallback
    return [
        {
            "source_name": "GeeksforGeeks",
            "source_url": "https://www.geeksforgeeks.org/computer-science-fundamentals/computer-science-subjects-interview-questions/",
            "title": "Computer Science Core Subjects — GeeksforGeeks"
        },
        {
            "source_name": "TutorialsPoint",
            "source_url": "https://www.tutorialspoint.com/computer_science_tutorials.htm",
            "title": "Computer Science Tutorials Library"
        }
    ]
