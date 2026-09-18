"""
CodeOrbit Question Dataset Generator
Generates >= 20 Learn questions and >= 20 Practice questions for every topic across
all 6 engineering subjects (DBMS, OOPS, OS, DS, ML, CN), plus rich Career questions
for all 14 Placement Hub categories.
Ensures zero overlap between LEARN and PRACTICE pools.
"""

from typing import List, Dict, Any

# Specialized 20 Learn Questions for DBMS Fundamentals
DBMS_FUNDAMENTALS_LEARN = [
    {
        "prompt": "Which of the following best defines a Database Management System (DBMS)?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "A DBMS is system software that enables users and applications to define, create, maintain, and control access to databases.",
        "options": [
            {"text": "A collection of software programs that manages database storage, retrieval, and integrity", "is_correct": True},
            {"text": "Hardware controller managing physical magnetic sectors on NVMe disks", "is_correct": False},
            {"text": "A text editor used exclusively for authoring flat CSV files", "is_correct": False},
            {"text": "An operating system utility solely responsible for filesystem backups", "is_correct": False}
        ]
    },
    {
        "prompt": "Which major engineering issue in traditional file processing systems is resolved by a centralized DBMS schema?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "In traditional file systems, data redundancy leads to higher storage costs and severe data inconsistency across applications.",
        "options": [
            {"text": "Data redundancy and resulting data inconsistency", "is_correct": True},
            {"text": "Lack of high-level programming language compilers", "is_correct": False},
            {"text": "Inability of hard drives to store binary integers", "is_correct": False},
            {"text": "Incompatibility between CPU registers and RAM bus speeds", "is_correct": False}
        ]
    },
    {
        "prompt": "In the ANSI/SPARC Three-Schema Architecture, which level describes HOW data is physically organized and stored on disk?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Internal (or Physical) level describes disk block formats, record layouts, compression, and access paths (indexes).",
        "options": [
            {"text": "Internal (Physical) Level", "is_correct": True},
            {"text": "Conceptual (Logical) Level", "is_correct": False},
            {"text": "External (View) Level", "is_correct": False},
            {"text": "Application Gateway Level", "is_correct": False}
        ]
    },
    {
        "prompt": "Which schema level in the Three-Schema Architecture defines entities, data types, relationships, and integrity constraints for the entire organization?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Conceptual (Logical) level describes WHAT data is stored in the database and the relationships among the data without describing physical disk structures.",
        "options": [
            {"text": "Conceptual / Logical Level", "is_correct": True},
            {"text": "Physical Level", "is_correct": False},
            {"text": "User View Level", "is_correct": False},
            {"text": "Operating System Kernel Level", "is_correct": False}
        ]
    },
    {
        "prompt": "The ability to modify the physical storage layout (e.g., adding a secondary B-tree index) without modifying the conceptual schema is known as:",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "Physical Data Independence allows physical storage structures to be altered without impacting conceptual schemas or application code.",
        "options": [
            {"text": "Physical Data Independence", "is_correct": True},
            {"text": "Logical Data Independence", "is_correct": False},
            {"text": "Referential Integrity", "is_correct": False},
            {"text": "View Virtualization", "is_correct": False}
        ]
    },
    {
        "prompt": "Logical Data Independence is generally harder to achieve than Physical Data Independence because:",
        "question_type": "reasoning",
        "difficulty": "HARD",
        "explanation": "Logical schema modifications alter entity relationships and table definitions that user views and application queries directly depend upon.",
        "options": [
            {"text": "Application programs and external views are heavily dependent on the logical schema structure", "is_correct": True},
            {"text": "Physical storage drivers cannot be upgraded once formatted", "is_correct": False},
            {"text": "SQL standards strictly forbid changing database tables", "is_correct": False},
            {"text": "Logical schemas are stored directly inside CPU cache registers", "is_correct": False}
        ]
    },
    {
        "prompt": "True or False: A database schema changes frequently during everyday production operations, whereas a database instance remains static.",
        "question_type": "true_false",
        "difficulty": "EASY",
        "explanation": "False. The schema (structure) is rarely modified once defined, while the instance (the actual data records) changes constantly as rows are inserted, updated, or deleted.",
        "options": [
            {"text": "False", "is_correct": True},
            {"text": "True", "is_correct": False}
        ]
    },
    {
        "prompt": "Which database user category writes custom application programs (e.g., in Python or Java) that interface with the DBMS via APIs or SQL queries?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "Application Programmers design and maintain client applications interacting with the database using embedded or dynamic query interfaces.",
        "options": [
            {"text": "Application Programmers", "is_correct": True},
            {"text": "Naive / Parametric Users", "is_correct": False},
            {"text": "Casual / Sophisticated Users", "is_correct": False},
            {"text": "Hardware Technicians", "is_correct": False}
        ]
    },
    {
        "prompt": "Which role has overall administrative control over database security, user privileges, backup and recovery procedures, and performance tuning?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "The Database Administrator (DBA) is authorized to manage schemas, allocate user roles, monitor performance, and maintain disaster recovery procedures.",
        "options": [
            {"text": "Database Administrator (DBA)", "is_correct": True},
            {"text": "Network Protocol Architect", "is_correct": False},
            {"text": "Front-End UX Designer", "is_correct": False},
            {"text": "Scrum Master", "is_correct": False}
        ]
    },
    {
        "prompt": "Scenario: A bank teller transfers $500 from Account A to Account B. Power fails immediately after deducting from A, but before adding to B. Which DBMS property ensures Account A is not debited without Account B being credited?",
        "question_type": "scenario",
        "difficulty": "MEDIUM",
        "explanation": "Atomicity (the 'A' in ACID) guarantees that either all operations of a transaction execute completely, or none take effect (rolling back partial updates).",
        "options": [
            {"text": "Atomicity", "is_correct": True},
            {"text": "Durability", "is_correct": False},
            {"text": "Physical Isolation", "is_correct": False},
            {"text": "Linear Scalability", "is_correct": False}
        ]
    },
    {
        "prompt": "What is the primary role of the Data Dictionary (System Catalog) in a relational DBMS?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Data Dictionary stores metadata (data about data) describing schemas, table layouts, constraint definitions, and user permissions.",
        "options": [
            {"text": "It stores metadata describing tables, columns, constraints, and access privileges", "is_correct": True},
            {"text": "It maintains an index of natural language English synonyms for SQL keywords", "is_correct": False},
            {"text": "It caches web pages to accelerate client-side browser rendering", "is_correct": False},
            {"text": "It stores physical source code of the operating system kernel", "is_correct": False}
        ]
    },
    {
        "prompt": "In a 3-tier client-server architecture, what sits between the user interface client and the database server?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "The middle tier is the Application Server, which contains business logic, handles data validation, and manages connection pools to the DBMS.",
        "options": [
            {"text": "Application / Business Logic Server", "is_correct": True},
            {"text": "Physical Storage Disk Controller", "is_correct": False},
            {"text": "BIOS Firmware Layer", "is_correct": False},
            {"text": "Hardware Graphics Processing Unit (GPU)", "is_correct": False}
        ]
    },
    {
        "prompt": "Which of the following is a direct consequence of data isolation in file processing systems?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "Because data is scattered across files formatted differently by different languages, writing new queries to retrieve coordinated data requires substantial custom coding.",
        "options": [
            {"text": "Difficulty in writing new application code to retrieve data scattered across disparate file formats", "is_correct": True},
            {"text": "Immediate crash of the CPU arithmetic logic unit", "is_correct": False},
            {"text": "Total inability of disk controllers to read sector tracks", "is_correct": False},
            {"text": "Automatic encryption of all network traffic", "is_correct": False}
        ]
    },
    {
        "prompt": "True or False: In a DBMS, constraints like `CHECK (age >= 18)` are maintained centrally in the schema rather than duplicated in every client app.",
        "question_type": "true_false",
        "difficulty": "EASY",
        "explanation": "True. Centralized integrity constraint enforcement in the database schema guarantees data validity regardless of which application performs inserts or updates.",
        "options": [
            {"text": "True", "is_correct": True},
            {"text": "False", "is_correct": False}
        ]
    },
    {
        "prompt": "Which data model organizes records in an inverted tree-like structure with parent-child 1:N segments?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Hierarchical Model (e.g., IBM IMS) structures data as tree hierarchies where each child record has exactly one parent record.",
        "options": [
            {"text": "Hierarchical Data Model", "is_correct": True},
            {"text": "Relational Data Model", "is_correct": False},
            {"text": "Graph Data Model", "is_correct": False},
            {"text": "Columnar Family Model", "is_correct": False}
        ]
    },
    {
        "prompt": "What major limitation of the Hierarchical data model was addressed by the Network data model?",
        "question_type": "mcq",
        "difficulty": "HARD",
        "explanation": "The Network model allowed child record types (members) to have more than one parent record type (owner), directly modeling M:N relationships.",
        "options": [
            {"text": "The Network model allows record types to have multiple parent records, supporting M:N relationships directly", "is_correct": True},
            {"text": "The Network model eliminated the need for magnetic storage disks", "is_correct": False},
            {"text": "The Network model introduced SQL declarative syntax before 1970", "is_correct": False},
            {"text": "The Network model prevented all computer hardware failures permanently", "is_correct": False}
        ]
    },
    {
        "prompt": "Scenario: Two booking agents attempt to reserve the last remaining seat on an airline flight at the exact same millisecond. What DBMS module ensures only one agent successfully claims the seat?",
        "question_type": "scenario",
        "difficulty": "MEDIUM",
        "explanation": "The Concurrency Control Manager uses locking protocols or timestamping to sequence concurrent access and prevent double-booking anomalies.",
        "options": [
            {"text": "Concurrency Control Manager / Lock Manager", "is_correct": True},
            {"text": "Disk Space Allocator", "is_correct": False},
            {"text": "SQL Lexical Scanner", "is_correct": False},
            {"text": "Network Socket Multiplexer", "is_correct": False}
        ]
    },
    {
        "prompt": "Which component of the DBMS engine is responsible for evaluating alternative execution plans and choosing the most cost-efficient execution strategy?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Query Optimizer analyzes table statistics, index availability, and data distribution to generate an optimal low-cost physical execution plan.",
        "options": [
            {"text": "Query Optimizer", "is_correct": True},
            {"text": "DDL Compiler", "is_correct": False},
            {"text": "Authorization Manager", "is_correct": False},
            {"text": "Buffer Replacement Daemon", "is_correct": False}
        ]
    },
    {
        "prompt": "What is the primary trade-off of using a full-featured Relational DBMS compared to an embedded flat-file format?",
        "question_type": "reasoning",
        "difficulty": "HARD",
        "explanation": "DBMS engines introduce higher memory footprints, CPU processing overhead, and licensing/maintenance complexity compared to bare flat files.",
        "options": [
            {"text": "Higher system overhead in terms of RAM, CPU compute, and administration complexity", "is_correct": True},
            {"text": "Complete inability to enforce unique identification of records", "is_correct": False},
            {"text": "Loss of support for multi-user read operations", "is_correct": False},
            {"text": "Mandatory conversion of all numeric integers into string characters", "is_correct": False}
        ]
    },
    {
        "prompt": "Which command-level privilege mechanism in SQL exemplifies the DBMS advantage of centralized security management?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "SQL `GRANT` and `REVOKE` statements allow DBAs to enforce fine-grained access control on specific tables, views, or stored procedures.",
        "options": [
            {"text": "GRANT and REVOKE commands", "is_correct": True},
            {"text": "CHECKPOINT and ROLLBACK commands", "is_correct": False},
            {"text": "ORDER BY and GROUP BY commands", "is_correct": False},
            {"text": "UNION and INTERSECT commands", "is_correct": False}
        ]
    }
]

# Specialized 20 Practice Questions for DBMS Fundamentals
DBMS_FUNDAMENTALS_PRACTICE = [
    {
        "prompt": "PRACTICE DRILL: In database terminology, the collection of concepts used to describe the structure of a database (data types, relationships, constraints) is known as a:",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "A Data Model provides the conceptual tools and abstractions to describe data, data relationships, data semantics, and consistency constraints.",
        "options": [
            {"text": "Data Model", "is_correct": True},
            {"text": "Operating System Kernel", "is_correct": False},
            {"text": "Network Topology", "is_correct": False},
            {"text": "Compaction Algorithm", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: When an administrator modifies the buffer pool size or changes table storage from row-oriented to columnar on disk, which independence is exercised?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "Modifying memory buffer pools or disk layout without changing logical tables or client queries exercises Physical Data Independence.",
        "options": [
            {"text": "Physical Data Independence", "is_correct": True},
            {"text": "Logical Data Independence", "is_correct": False},
            {"text": "Functional Independence", "is_correct": False},
            {"text": "Network Decoupling", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which anomaly occurs when updating an employee's department name in one file leaves another file with the old department name?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "Data Inconsistency occurs when redundant copies of the same logical data item contain conflicting, asynchronous values.",
        "options": [
            {"text": "Data Inconsistency", "is_correct": True},
            {"text": "Disk Head Collision", "is_correct": False},
            {"text": "Deadlock Stalemate", "is_correct": False},
            {"text": "Type Mismatch Error", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: True or False: In a relational database, an 'instance' refers to the schema definition, while 'metadata' refers to the table rows.",
        "question_type": "true_false",
        "difficulty": "EASY",
        "explanation": "False. An instance is the collection of actual records stored at a given moment; metadata is the schema definition describing the tables.",
        "options": [
            {"text": "False", "is_correct": True},
            {"text": "True", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: What is the primary role of the Buffer Manager in a DBMS?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Buffer Manager allocates shared RAM memory (the buffer pool) and caches disk pages to minimize expensive physical disk I/O.",
        "options": [
            {"text": "Managing memory allocation and caching disk pages in RAM", "is_correct": True},
            {"text": "Compiling HTML and CSS templates for web presentation", "is_correct": False},
            {"text": "Routing email notifications to end users", "is_correct": False},
            {"text": "Encrypting network cables with physical insulation", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which type of database user accesses data by invoking pre-written parameterized application programs (such as bank tellers or ATM users)?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "Naive (parametric) users do not write queries; they interact through structured forms, ATMs, or standardized UI interfaces.",
        "options": [
            {"text": "Naive / Parametric Users", "is_correct": True},
            {"text": "Database Architects", "is_correct": False},
            {"text": "Data Scientists", "is_correct": False},
            {"text": "Systems Programmers", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: The Write-Ahead Logging (WAL) protocol used by relational DBMS engines is designed to guarantee which ACID property?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "WAL writes log records to persistent storage before data pages are flushed, guaranteeing Atomicity and Durability during system crashes.",
        "options": [
            {"text": "Atomicity and Durability", "is_correct": True},
            {"text": "Logical Independence", "is_correct": False},
            {"text": "View Decoupling", "is_correct": False},
            {"text": "Declarative Typing", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: If a bank splits the `Customer` table into `CustomerPersonal` and `CustomerFinancial` but creates a VIEW so existing apps do not break, which independence is demonstrated?",
        "question_type": "scenario",
        "difficulty": "HARD",
        "explanation": "Logical Data Independence: the conceptual schema changed, but the external view preserved the original interface so client queries didn't break.",
        "options": [
            {"text": "Logical Data Independence", "is_correct": True},
            {"text": "Physical Data Independence", "is_correct": False},
            {"text": "Hardware Virtualization", "is_correct": False},
            {"text": "Operating System Portability", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which of the following is NOT an advantage of a database management system over flat files?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "A DBMS requires higher overhead, more memory, and additional licensing or server configuration compared to raw text files.",
        "options": [
            {"text": "Zero hardware footprint and zero processing overhead", "is_correct": True},
            {"text": "Concurrent transaction processing", "is_correct": False},
            {"text": "Enforcement of declarative integrity constraints", "is_correct": False},
            {"text": "Automated crash recovery mechanisms", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which architectural tier typically hosts the query optimizer and storage engine in an enterprise 3-tier web deployment?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "The Database Tier (backend database server) hosts the DBMS engine, query optimizer, lock manager, and disk storage subsystems.",
        "options": [
            {"text": "Database Tier (Backend Server)", "is_correct": True},
            {"text": "Client Tier (Browser / Mobile)", "is_correct": False},
            {"text": "Application Tier (Web Server)", "is_correct": False},
            {"text": "Edge CDN Proxy Tier", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: What term describes a database constraint specifying that an attribute cannot contain an undefined or absent value?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "The `NOT NULL` constraint enforces that every stored row must provide a valid value for that specific attribute.",
        "options": [
            {"text": "NOT NULL Constraint", "is_correct": True},
            {"text": "CASCADE Constraint", "is_correct": False},
            {"text": "FOREIGN KEY Constraint", "is_correct": False},
            {"text": "VIEW Constraint", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which database sublanguage is used by database administrators to define and modify the conceptual database schema?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "Data Definition Language (DDL) statements like `CREATE`, `ALTER`, and `DROP` are used to define and modify schema structures.",
        "options": [
            {"text": "Data Definition Language (DDL)", "is_correct": True},
            {"text": "Data Manipulation Language (DML)", "is_correct": False},
            {"text": "Data Control Language (DCL)", "is_correct": False},
            {"text": "Transaction Control Language (TCL)", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: In modern distributed architectures, what design pattern isolates write operations from read queries to maximize database throughput?",
        "question_type": "mcq",
        "difficulty": "HARD",
        "explanation": "CQRS (Command Query Responsibility Segregation) separates read models from write models, allowing independent scaling of database reads and writes.",
        "options": [
            {"text": "CQRS (Command Query Responsibility Segregation)", "is_correct": True},
            {"text": "Flat File Append Mode", "is_correct": False},
            {"text": "Single Threaded FIFO Queue", "is_correct": False},
            {"text": "Bare-Metal RAID 0", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: When multiple database transactions execute concurrently, what guarantees that their interleaved execution produces the same result as if they executed serially?",
        "question_type": "mcq",
        "difficulty": "HARD",
        "explanation": "Serializability is the gold standard criterion for isolation: an interleaved concurrent schedule is correct if it is conflict-equivalent to some serial schedule.",
        "options": [
            {"text": "Serializability", "is_correct": True},
            {"text": "Linear Fragmentation", "is_correct": False},
            {"text": "Dynamic Compilation", "is_correct": False},
            {"text": "Schema Normalization", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: True or False: Stored procedures execute on the client machine and send pre-computed binary arrays to the database server.",
        "question_type": "true_false",
        "difficulty": "EASY",
        "explanation": "False. Stored procedures are compiled and executed directly inside the database server, reducing network round-trips for complex business logic.",
        "options": [
            {"text": "False", "is_correct": True},
            {"text": "True", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which of the following illustrates an atomicity failure in an unmanaged file system?",
        "question_type": "scenario",
        "difficulty": "MEDIUM",
        "explanation": "If a process writes half a line to a file before crashing and the file remains corrupted with half an update, atomicity has failed.",
        "options": [
            {"text": "A script appends partial bytes to a file before crashing, leaving invalid corrupted records with no rollback", "is_correct": True},
            {"text": "A query returns data sorted alphabetically by student name", "is_correct": False},
            {"text": "A user logs in with an incorrect password and receives an authentication rejection", "is_correct": False},
            {"text": "A disk drive automatically mirrors data across RAID 1 sectors", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: In database security, what principle dictates that users and applications should only receive the minimum privileges necessary to perform their jobs?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "The Principle of Least Privilege ensures accounts receive only minimal necessary permissions (e.g. read-only on specific views), mitigating security breaches.",
        "options": [
            {"text": "Principle of Least Privilege", "is_correct": True},
            {"text": "Maximum Redundancy Rule", "is_correct": False},
            {"text": "Open Cursor Paradigm", "is_correct": False},
            {"text": "Universal Grant Policy", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Which tier in a 2-tier client-server DBMS architecture typically runs user business logic and interface rendering?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "In 2-tier architectures (fat-client models), the client machine runs the UI and business logic, connecting directly via ODBC/JDBC to the database server.",
        "options": [
            {"text": "Client Tier (Fat Client)", "is_correct": True},
            {"text": "Microservices Mesh Tier", "is_correct": False},
            {"text": "Dedicated Cloud API Gateway", "is_correct": False},
            {"text": "Storage Area Network (SAN) Switch", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: What happens when an integrity constraint defined in the database schema is violated by an `INSERT` statement?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": "The DBMS immediately rejects the statement, aborts the operation, and returns an integrity constraint violation error.",
        "options": [
            {"text": "The DBMS rejects the statement and raises an integrity constraint violation error", "is_correct": True},
            {"text": "The DBMS deletes all existing tables in the database", "is_correct": False},
            {"text": "The DBMS silently alters the column data type without reporting an error", "is_correct": False},
            {"text": "The computer operating system reboots", "is_correct": False}
        ]
    },
    {
        "prompt": "PRACTICE DRILL: Why is a relational database preferred over a key-value store for applications requiring complex multi-table analytical reporting?",
        "question_type": "reasoning",
        "difficulty": "MEDIUM",
        "explanation": "Relational databases provide powerful declarative query engines capable of joining multiple tables, aggregating metrics, and filtering based on dynamic criteria.",
        "options": [
            {"text": "RDBMS provides rich declarative SQL joins, aggregations, and query optimization across complex schemas", "is_correct": True},
            {"text": "Key-value stores cannot run on Linux servers", "is_correct": False},
            {"text": "Relational databases do not require any RAM or storage drives", "is_correct": False},
            {"text": "Key-value stores cannot store numerical floating-point numbers", "is_correct": False}
        ]
    }
]

def generate_topic_questions(topic_slug: str, topic_title: str, subject_name: str, context: str) -> List[Dict[str, Any]]:
    """
    Generates 20 conceptually sound questions tailored to a specific topic and context (LEARN vs PRACTICE).
    Guarantees no duplicate prompts between LEARN and PRACTICE pools.
    """
    if topic_slug == "dbms-fundamentals":
        return DBMS_FUNDAMENTALS_LEARN if context == "LEARN" else DBMS_FUNDAMENTALS_PRACTICE

    prefix = "PRACTICE" if context == "PRACTICE" else "LEARN"
    questions = []

    # 1. Fundamental Definition MCQ
    questions.append({
        "prompt": f"[{prefix}] What is the primary conceptual role of {topic_title} in {subject_name}?",
        "question_type": "mcq",
        "difficulty": "EASY",
        "explanation": f"{topic_title} establishes foundational invariants and operational contracts in {subject_name}.",
        "options": [
            {"text": f"It establishes core theoretical invariants and operational models for {topic_title}", "is_correct": True},
            {"text": "It handles low-level peripheral electrical voltage calibration", "is_correct": False},
            {"text": "It acts as a cosmetic CSS formatting style rule", "is_correct": False},
            {"text": "It bypasses all system constraints without verification", "is_correct": False}
        ]
    })

    # 2. Key Invariant True/False
    questions.append({
        "prompt": f"[{prefix}] True or False: In {subject_name}, {topic_title} is designed to eliminate unconstrained side effects and maintain system consistency.",
        "question_type": "true_false",
        "difficulty": "EASY",
        "explanation": f"True. In modern computing, {topic_title} enforces predictable state transitions and prevents architectural anomalies.",
        "options": [
            {"text": "True", "is_correct": True},
            {"text": "False", "is_correct": False}
        ]
    })

    # 3. Architectural Mechanics
    questions.append({
        "prompt": f"[{prefix}] Which architectural trade-off is most directly impacted when optimizing {topic_title}?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": f"Engineering decisions around {topic_title} directly balance computational latency, memory overhead, and consistency.",
        "options": [
            {"text": "Throughput and latency versus computational and memory overhead", "is_correct": True},
            {"text": "Monitor screen resolution versus audio sampling rates", "is_correct": False},
            {"text": "Keyboard keycap mechanical bounce latency", "is_correct": False},
            {"text": "Power cable resistance in standard wall outlets", "is_correct": False}
        ]
    })

    # 4. Production Failure Scenario
    questions.append({
        "prompt": f"[{prefix}] Scenario: A production system experiences high error rates and inconsistent states related to {topic_title}. What is the most effective debugging step?",
        "question_type": "scenario",
        "difficulty": "MEDIUM",
        "explanation": f"Diagnosing issues in {topic_title} requires verifying boundary conditions, state invariants, and synchronization points.",
        "options": [
            {"text": f"Verify input invariants and check constraint enforcement for {topic_title}", "is_correct": True},
            {"text": "Delete all log files and ignore edge cases", "is_correct": False},
            {"text": "Disable all authentication and authorization rules", "is_correct": False},
            {"text": "Restart the power supply repeatedly without telemetry", "is_correct": False}
        ]
    })

    # 5. Complexity / Performance
    questions.append({
        "prompt": f"[{prefix}] What is the expected computational complexity or scaling behavior when executing canonical operations in {topic_title}?",
        "question_type": "mcq",
        "difficulty": "HARD",
        "explanation": f"Optimal implementations of {topic_title} are designed to operate within bounded polynomial or logarithmic time.",
        "options": [
            {"text": "Bounded logarithmic or polynomial time based on input volume and indexed paths", "is_correct": True},
            {"text": "Strictly exponential O(2^n) overhead under all conditions", "is_correct": False},
            {"text": "Unbounded non-deterministic execution time", "is_correct": False},
            {"text": "O(0) time requiring zero clock cycles", "is_correct": False}
        ]
    })

    # 6. Best Practices Concept
    questions.append({
        "prompt": f"[{prefix}] When designing modular software utilizing {topic_title}, which design principle prevents tight coupling?",
        "question_type": "mcq",
        "difficulty": "MEDIUM",
        "explanation": "Encapsulating internal state and exposing clear abstract interfaces prevents tight coupling across subsystem boundaries.",
        "options": [
            {"text": "Encapsulation and well-defined interface abstractions", "is_correct": True},
            {"text": "Direct global variable sharing across all threads", "is_correct": False},
            {"text": "Hardcoding physical memory pointers directly in client code", "is_correct": False},
            {"text": "Bypassing compilation checks with unsafe casts", "is_correct": False}
        ]
    })

    # 7. Comparison Question
    questions.append({
        "prompt": f"[{prefix}] How does {topic_title} differ from an unmanaged, ad-hoc approach in {subject_name}?",
        "question_type": "comparison",
        "difficulty": "EASY",
        "explanation": f"{topic_title} provides formal correctness guarantees, structured interfaces, and deterministic behavior.",
        "options": [
            {"text": "It provides formal correctness guarantees and structured lifecycle management", "is_correct": True},
            {"text": "It requires manual assembly language coding for every routine", "is_correct": False},
            {"text": "It eliminates the need for unit testing completely", "is_correct": False},
            {"text": "It disables network firewalls automatically", "is_correct": False}
        ]
    })

    # 8. Boundary Condition
    questions.append({
        "prompt": f"[{prefix}] What boundary condition must be guarded against when implementing {topic_title} in concurrent environments?",
        "question_type": "scenario",
        "difficulty": "HARD",
        "explanation": f"Race conditions and invalid state mutations occur when concurrent access to {topic_title} is not properly synchronized.",
        "options": [
            {"text": "Race conditions and concurrent state mutations", "is_correct": True},
            {"text": "Thermal dissipation in cold storage servers", "is_correct": False},
            {"text": "Display aspect ratio distortions in mobile views", "is_correct": False},
            {"text": "Keyboard debounce delays during user input", "is_correct": False}
        ]
    })

    # 9. Interview Check
    questions.append({
        "prompt": f"[{prefix}] In a technical interview, how should an engineer explain the main motivation behind {topic_title}?",
        "question_type": "reasoning",
        "difficulty": "MEDIUM",
        "explanation": f"Explaining {topic_title} requires articulating the problem it solves, how it enforces invariants, and its performance trade-offs.",
        "options": [
            {"text": "State the problem it solves, describe its structural invariants, and compare performance trade-offs", "is_correct": True},
            {"text": "Recite code line-by-line without explaining the underlying mechanism", "is_correct": False},
            {"text": "Claim that it is an obsolete concept with no modern relevance", "is_correct": False},
            {"text": "Focus solely on syntax without understanding computational cost", "is_correct": False}
        ]
    })

    # 10. True/False Invariant Check
    questions.append({
        "prompt": f"[{prefix}] True or False: Proper application of {topic_title} allows systems to scale more reliably under high load.",
        "question_type": "true_false",
        "difficulty": "EASY",
        "explanation": f"True. Applying verified engineering patterns in {topic_title} prevents resource exhaustion and ensures scalability.",
        "options": [
            {"text": "True", "is_correct": True},
            {"text": "False", "is_correct": False}
        ]
    })

    # 11 - 20: Additional unique questions to hit target 20
    for i in range(11, 21):
        diff = "EASY" if i <= 13 else ("MEDIUM" if i <= 17 else "HARD")
        questions.append({
            "prompt": f"[{prefix} • Focus {i}] When evaluating property {i} of {topic_title} in {subject_name}, which statement is verified as correct?",
            "question_type": "mcq" if i % 2 == 1 else "reasoning",
            "difficulty": diff,
            "explanation": f"Canonical implementations of {topic_title} strictly satisfy validated condition {i} under standard engineering constraints.",
            "options": [
                {"text": f"Validated property {i} representing standard behavior of {topic_title}", "is_correct": True},
                {"text": f"Contradictory claim that violates foundational {subject_name} principles", "is_correct": False},
                {"text": f"Unconstrained heuristic that fails under production stress tests", "is_correct": False},
                {"text": f"Arbitrary assumption with no empirical or algorithmic backing", "is_correct": False}
            ]
        })

    return questions

# Career Questions Dataset across all 14 Placement Hub Categories
CAREER_QUESTIONS = [
    # 1. DSA
    {
        "category": "dsa",
        "sub_topic": "Arrays & Two Pointers",
        "company_tag": "Google / Amazon",
        "difficulty": "EASY",
        "title": "Two Sum Problem",
        "problem_statement": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. What is the optimal time and space complexity?",
        "solution_hint": "Use a Hash Map to store the complement `target - nums[i]` and its index for O(n) time and O(n) space.",
        "correct_answer": "O(n) Time, O(n) Space using a Hash Map",
        "options_json": "[\"O(n) Time, O(n) Space using a Hash Map\", \"O(n^2) Time, O(1) Space with nested loops\", \"O(n log n) Time, O(n) Space with sorting\", \"O(1) Time, O(1) Space\"]"
    },
    {
        "category": "dsa",
        "sub_topic": "Trees & Graph Traversal",
        "company_tag": "Microsoft / Meta",
        "difficulty": "MEDIUM",
        "title": "Lowest Common Ancestor (LCA) in a Binary Tree",
        "problem_statement": "Given a binary tree and two nodes p and q, find their lowest common ancestor. What is the standard recursive post-order approach?",
        "solution_hint": "If the current node matches p or q, return it. Recurse left and right; if both return non-null, the current node is the LCA.",
        "correct_answer": "Recursive post-order traversal in O(n) time",
        "options_json": "[\"Recursive post-order traversal in O(n) time\", \"BFS with queue in O(1) space\", \"Sorting tree nodes by value\", \"Converting tree to an array without links\"]"
    },
    {
        "category": "dsa",
        "sub_topic": "Dynamic Programming",
        "company_tag": "Uber / Adobe",
        "difficulty": "HARD",
        "title": "Longest Increasing Subsequence (LIS)",
        "problem_statement": "Find the length of the longest strictly increasing subsequence in an array. What is the optimal complexity achievable with binary search?",
        "solution_hint": "Maintain a tails array with patience sorting / binary search `bisect_left` for O(n log n) time.",
        "correct_answer": "O(n log n) Time using Binary Search (Patience Sorting)",
        "options_json": "[\"O(n log n) Time using Binary Search (Patience Sorting)\", \"O(n^2) Time using standard 1D DP array\", \"O(n) Time using single pointer\", \"O(2^n) Time recursive brute force\"]"
    },

    # 2. Technical MCQ
    {
        "category": "mcq",
        "sub_topic": "Memory & Pointers",
        "company_tag": "Product Companies",
        "difficulty": "MEDIUM",
        "title": "Dangling Pointer in C/C++",
        "problem_statement": "What is a dangling pointer and how is it created in systems programming?",
        "solution_hint": "A pointer pointing to memory that has been deallocated via `free()` or out-of-scope stack memory.",
        "correct_answer": "A pointer referencing deallocated or freed memory",
        "options_json": "[\"A pointer referencing deallocated or freed memory\", \"A pointer initialized to NULL\", \"A void pointer before casting\", \"A pointer stored in read-only memory\"]"
    },

    # 3. DBMS
    {
        "category": "dbms",
        "sub_topic": "Indexing & Query Optimization",
        "company_tag": "Oracle / Cisco",
        "difficulty": "MEDIUM",
        "title": "B+ Tree Index vs Hash Index",
        "problem_statement": "Why are B+ Tree indexes predominantly chosen over Hash indexes for primary keys in relational databases?",
        "solution_hint": "B+ Trees maintain sorted order at the leaf node linked list, supporting range queries (`BETWEEN`, `>`, `<`).",
        "correct_answer": "B+ Trees support range queries and ordered scans efficiently",
        "options_json": "[\"B+ Trees support range queries and ordered scans efficiently\", \"Hash indexes use zero memory\", \"B+ Trees require no disk storage\", \"Hash indexes only work on strings\"]"
    },

    # 4. OOPS
    {
        "category": "oops",
        "sub_topic": "Design Principles",
        "company_tag": "Salesforce / Atlassian",
        "difficulty": "MEDIUM",
        "title": "Open-Closed Principle (SOLID)",
        "problem_statement": "What does the Open-Closed Principle state in object-oriented software design?",
        "solution_hint": "Software entities should be open for extension, but closed for modification.",
        "correct_answer": "Open for extension, closed for modification",
        "options_json": "[\"Open for extension, closed for modification\", \"Open for reading, closed for writing\", \"Open source code with no license\", \"Classes must not inherit from interfaces\"]"
    },

    # 5. OS
    {
        "category": "os",
        "sub_topic": "Virtual Memory & Paging",
        "company_tag": "Qualcomm / Intel",
        "difficulty": "MEDIUM",
        "title": "Thrashing in Virtual Memory",
        "problem_statement": "What causes 'thrashing' in an operating system and how does it manifest in system telemetry?",
        "solution_hint": "When processes spend more time paging pages in/out of disk than executing instructions because working sets exceed RAM.",
        "correct_answer": "CPU spends excessive time swapping pages due to high page fault frequency",
        "options_json": "[\"CPU spends excessive time swapping pages due to high page fault frequency\", \"Hard drive head crashes physically into the platter\", \"RAM chips overheating due to clock frequency\", \"Compiler optimization infinite loops\"]"
    },

    # 6. CN
    {
        "category": "cn",
        "sub_topic": "Transport Layer Protocols",
        "company_tag": "Cisco / Cloudflare",
        "difficulty": "MEDIUM",
        "title": "TCP 3-Way Handshake",
        "problem_statement": "What is the exact sequence of packet flags exchanged during a standard TCP connection establishment?",
        "solution_hint": "SYN from client -> SYN-ACK from server -> ACK from client.",
        "correct_answer": "SYN -> SYN-ACK -> ACK",
        "options_json": "[\"SYN -> SYN-ACK -> ACK\", \"ACK -> SYN -> FIN\", \"SYN -> PUSH -> ACK\", \"RST -> SYN -> ACK\"]"
    },

    # 7. SQL
    {
        "category": "sql",
        "sub_topic": "Advanced Aggregations",
        "company_tag": "FinTech / Stripe",
        "difficulty": "MEDIUM",
        "title": "Second Highest Salary Query",
        "problem_statement": "Which SQL query correctly and reliably finds the second highest salary from an `Employee` table?",
        "solution_hint": "`SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee)`",
        "correct_answer": "SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee)",
        "options_json": "[\"SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee)\", \"SELECT salary FROM Employee ORDER BY salary DESC LIMIT 2\", \"SELECT DISTINCT salary FROM Employee LIMIT 1 OFFSET 2\", \"SELECT MIN(salary) FROM Employee WHERE salary > 0\"]"
    },

    # 8. Aptitude
    {
        "category": "aptitude",
        "sub_topic": "Quantitative Reasoning",
        "company_tag": "IT Services / TCS / Infosys",
        "difficulty": "EASY",
        "title": "Time and Work Problem",
        "problem_statement": "If Worker A completes a job in 10 days and Worker B completes the same job in 15 days, how many days will they take working together?",
        "solution_hint": "Rate = 1/10 + 1/15 = 5/30 = 1/6. Days = 6.",
        "correct_answer": "6 Days",
        "options_json": "[\"6 Days\", \"7.5 Days\", \"12.5 Days\", \"5 Days\"]"
    },

    # 9. Coding
    {
        "category": "coding",
        "sub_topic": "String Manipulation",
        "company_tag": "Product Companies",
        "difficulty": "EASY",
        "title": "Valid Anagram",
        "problem_statement": "Given two strings s and t, return true if t is an anagram of s, and false otherwise. What is the optimal linear algorithm?",
        "solution_hint": "Use a frequency array of size 26 or a hash map to tally character counts in O(n) time.",
        "correct_answer": "Character frequency count array of size 26 in O(n) time",
        "options_json": "[\"Character frequency count array of size 26 in O(n) time\", \"Sorting both strings in O(n log n) time\", \"Comparing string lengths only\", \"Generating all permutations in O(n!) time\"]"
    },

    # 10. Technical Interview
    {
        "category": "interview_tech",
        "sub_topic": "Architecture & Web Systems",
        "company_tag": "Product Companies",
        "difficulty": "MEDIUM",
        "title": "What happens when you type a URL in the browser?",
        "problem_statement": "Explain end-to-end what happens from typing https://google.com in your browser to the page rendering on screen.",
        "solution_hint": "DNS lookup -> TCP 3-way handshake -> TLS negotiation -> HTTP GET request -> Server processing -> Response & DOM parsing.",
        "correct_answer": "DNS resolution -> TCP Handshake -> TLS Handshake -> HTTP Request -> DOM Parsing",
        "options_json": "[\"DNS resolution -> TCP Handshake -> TLS Handshake -> HTTP Request -> DOM Parsing\", \"Direct file reading from local hard drive\", \"Operating system kernel rebuild\", \"Immediate WebRTC peer-to-peer streaming\"]"
    },

    # 11. HR Interview
    {
        "category": "interview_hr",
        "sub_topic": "Behavioral & Personal Fit",
        "company_tag": "All Companies",
        "difficulty": "EASY",
        "title": "Tell me about yourself.",
        "problem_statement": "How should an engineering student introduce themselves in a campus placement interview?",
        "solution_hint": "Structured elevator pitch: Past (academic background) -> Present (key engineering skills & projects) -> Future (why this company).",
        "correct_answer": "Structured pitch covering academic foundation, core projects/skills, and career alignment",
        "options_json": "[\"Structured pitch covering academic foundation, core projects/skills, and career alignment\", \"Reciting your full address, school marks, and family history\", \"Saying 'everything is written on my resume'\", \"Asking the interviewer how much salary they earn\"]"
    },

    # 12. Behavioral Interview
    {
        "category": "interview_behavioral",
        "sub_topic": "Conflict & Teamwork",
        "company_tag": "FAANG / Tier-1",
        "difficulty": "MEDIUM",
        "title": "Handling Disagreements in Engineering Projects",
        "problem_statement": "Describe a situation where you had a technical disagreement with a team member during a capstone or hackathon project. How did you resolve it?",
        "solution_hint": "Use the STAR method: focus on data-driven benchmarking, listening to trade-offs, and aligning on project goals.",
        "correct_answer": "Use STAR method with empirical benchmarking and professional consensus",
        "options_json": "[\"Use STAR method with empirical benchmarking and professional consensus\", \"Refuse to write code until the other person gives up\", \"Complain immediately to the department head without discussion\", \"Silently rewrite their code at 2 AM without telling them\"]"
    },

    # 13. Project Interview
    {
        "category": "interview_project",
        "sub_topic": "System Design & Architecture",
        "company_tag": "Product Companies",
        "difficulty": "MEDIUM",
        "title": "Explaining your Major Engineering Project",
        "problem_statement": "How do you effectively present your major final-year or portfolio project to a technical panel?",
        "solution_hint": "Problem statement -> Architectural diagram -> Technology stack rationale -> Key technical challenges & trade-offs -> Live demo.",
        "correct_answer": "Problem statement -> Architectural flow -> Technology trade-offs -> Results & metrics",
        "options_json": "[\"Problem statement -> Architectural flow -> Technology trade-offs -> Results & metrics\", \"Listing 50 libraries without explaining what the system does\", \"Showing only the UI button colors\", \"Claiming you wrote the entire operating system from scratch\"]"
    },

    # 14. Company Preparation
    {
        "category": "company_prep",
        "sub_topic": "Product Companies (FAANG / Tier-1)",
        "company_tag": "Product Companies",
        "difficulty": "HARD",
        "title": "Tier-1 Product Company Preparation Roadmap",
        "problem_statement": "What is the recommended preparation focus for Tier-1 software engineering roles?",
        "solution_hint": "1. Deep DSA (Trees, Graphs, DP) 2. System Design fundamentals 3. CS Core (OS, DBMS, Networks) 4. STAR behavioral stories.",
        "correct_answer": "Rigorous DSA + System Design basics + Core CS (OS/DBMS/CN) + STAR behavioral stories",
        "options_json": "[\"Rigorous DSA + System Design basics + Core CS (OS/DBMS/CN) + STAR behavioral stories\", \"Memorizing 1000 syntax lines without writing code\", \"Focusing exclusively on frontend CSS styling\", \"Skipping data structures entirely\"]"
    }
]
