"""
Generates the complete 12-topic DBMS curriculum module with all required exam sections.
"""
import os

DBMS_MODULE_CODE = '''"""
CodeOrbit Curriculum Data — DBMS (Database Management Systems)
Comprehensive, exam-oriented content for all 12 DBMS topics.
"""

from typing import Dict, Any

DBMS_CURRICULUM: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # 1. DBMS Fundamentals
    # -------------------------------------------------------------------------
    "dbms-fundamentals": {
        "title": "DBMS Fundamentals",
        "subject": "dbms",
        "exam_definition": (
            "A Database Management System (DBMS) is specialized system software that provides an interface "
            "for creating, storing, retrieving, updating, and managing data in a database while enforcing "
            "security, data integrity, concurrency control, and automated recovery."
        ),
        "remember": "DBMS = Software system used to manage, query, and protect databases.",
        "core_concept": (
            "Traditional file systems suffer from severe data redundancy, inconsistency, and lack of concurrency. "
            "A DBMS solves these issues by decoupling applications from physical storage through a centralized catalog, "
            "standardized declarative query interface (SQL), and strict ACID guarantees. It ensures that multiple users "
            "can query and update data simultaneously without data corruption."
        ),
        "key_points": [
            "Data Abstraction: Hides low-level physical storage details across 3 distinct schema levels.",
            "Data Independence: Allows modifying physical storage or logical schemas without breaking user applications.",
            "Minimal Redundancy: Centralized schema avoids repeating the same data across multiple disparate files.",
            "Concurrency Control: Enables simultaneous multi-user access without race conditions or lost updates.",
            "Crash Recovery: Write-Ahead Logging (WAL) and checkpointing ensure full recovery after power/system failures.",
            "Security & Integrity Constraints: Enforces role-based permissions and domain/referential business rules."
        ],
        "classification": {
            "title": "Classification of Database Management Systems",
            "items": [
                {"name": "Hierarchical DBMS", "desc": "Tree-like parent-child structure (e.g., IBM IMS). 1:N relationships only."},
                {"name": "Network DBMS", "desc": "Graph-based structure with record types and set types (e.g., IDMS). M:N allowed."},
                {"name": "Relational DBMS (RDBMS)", "desc": "Tables (relations) with rows (tuples) and columns (attributes) based on relational algebra (e.g., PostgreSQL, MySQL, Oracle)."},
                {"name": "Object-Oriented DBMS (OODBMS)", "desc": "Integrates OOP objects, classes, and inheritance directly into persistent storage."},
                {"name": "NoSQL DBMS", "desc": "Non-relational distributed databases (Key-Value, Document, Columnar, Graph) optimized for horizontal scalability."}
            ]
        },
        "how_it_works": {
            "title": "DBMS Query Execution Flow",
            "steps": [
                "User / Application sends declarative SQL query via API or CLI.",
                "Query Parser & Lexer validates SQL syntax and verifies referenced table/column names in Data Dictionary.",
                "Query Optimizer generates multiple execution plans, estimates I/O cost, and chooses the optimal plan.",
                "Query Execution Engine runs plan operators (Index Scan, Hash Join, Filter) interacting with Buffer Manager.",
                "Buffer Pool Manager checks RAM cache; if page is missing, fetches disk blocks from Storage Manager.",
                "Concurrency Control & Lock Manager grants shared/exclusive locks on tuples to guarantee serializability.",
                "Transaction & Recovery Manager writes changes to Write-Ahead Log (WAL) before persisting to disk."
            ],
            "diagram": (
                "User Query\\n"
                "    ↓\\n"
                "Parser & Semantic Checker\\n"
                "    ↓\\n"
                "Query Optimizer (Cost-based plan selection)\\n"
                "    ↓\\n"
                "Execution Engine (Index Scans, Joins)\\n"
                "    ↓\\n"
                "Buffer Pool / Storage Manager (Cache & Disk I/O)\\n"
                "    ↓\\n"
                "Physical Database & WAL Logs"
            )
        },
        "example": {
            "title": "University Database System",
            "scenario": (
                "Consider an engineering university managing 10,000 students. In a file system, Admissions, Hostels, "
                "and Accounts maintain separate Excel/CSV files. If Student 101 changes their phone number, Accounts has "
                "the old number while Admissions has the new one (Data Inconsistency).\\n\\n"
                "In a DBMS, a single centralized `Students` table is referenced by `Hostel_Allotments` and `Fee_Payments` "
                "via Foreign Keys. Updating `phone` in `Students` immediately reflects across all university departments."
            ),
            "code": (
                "-- Unified schema with referential constraint\\n"
                "CREATE TABLE Students (\\n"
                "    student_id INT PRIMARY KEY,\\n"
                "    name VARCHAR(100) NOT NULL,\\n"
                "    department VARCHAR(50),\\n"
                "    phone VARCHAR(15)\\n"
                ");\\n\\n"
                "CREATE TABLE Enrollments (\\n"
                "    enrollment_id INT PRIMARY KEY,\\n"
                "    student_id INT REFERENCES Students(student_id),\\n"
                "    course_code VARCHAR(10),\\n"
                "    semester VARCHAR(10)\\n"
                ");"
            )
        },
        "comparison": {
            "title": "File System vs DBMS",
            "headers": ["Feature", "File Processing System", "Database Management System (DBMS)"],
            "rows": [
                ["Data Redundancy", "High — same data duplicated across separate application files", "Minimal — centralized schema with foreign keys"],
                ["Data Inconsistency", "High — partial updates cause conflicting versions", "Low — ACID transactions enforce consistency"],
                ["Data Access", "Requires custom code (C++/Python scripts) for each query", "Declarative query language (SQL) with query optimizer"],
                ["Concurrency", "Crude file locking (blocks entire file for all users)", "Fine-grained row/page locking with MVCC"],
                ["Crash Recovery", "No built-in recovery; prone to permanent file corruption", "Write-Ahead Logging (WAL) and checkpoint rollback"],
                ["Data Independence", "None — changing file layout breaks all application code", "High — Three-Schema architecture provides logical & physical independence"]
            ]
        },
        "formulas": [
            {"name": "Three-Schema Architecture Levels", "formula": "External Level (Views) → Conceptual Level (Logical Schema) → Internal Level (Physical Storage)", "explanation": "Separates user interface from physical disk representation."},
            {"name": "Physical Data Independence", "formula": "Modifying Internal Schema does NOT affect Conceptual or External Schema", "explanation": "Changing disk indexing or SSD layout doesn't break SQL queries."},
            {"name": "Logical Data Independence", "formula": "Modifying Conceptual Schema does NOT affect External Views", "explanation": "Adding a new column to a table doesn't break existing user view queries."}
        ],
        "exam_tip": "Remember: Logical Data Independence is harder to achieve than Physical Data Independence because user application queries are directly tied to the logical structure of tables.",
        "common_confusion": {
            "wrong": "A database and a DBMS are the exact same thing.",
            "correct": "A database is the passive collection of organized data, while a DBMS is the active software system used to access, manage, and query that database.",
            "explanation": "PostgreSQL or MySQL is the DBMS software; the stored tables containing student data is the database."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Define Data Independence and name its two types.",
                "a": "Data Independence is the capacity to change schema at one level of a database system without having to change the schema at the next higher level. The two types are: (1) Physical Data Independence (modifying physical storage without changing logical schema) and (2) Logical Data Independence (modifying logical schema without changing external views)."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the ANSI/SPARC Three-Schema Architecture of a DBMS with a diagram.",
                "a": "The Three-Schema Architecture divides a database into three abstraction levels:\\n1. External Level (View Level): Describes part of the database relevant to a specific user group, hiding the rest.\\n2. Conceptual Level (Logical Level): Describes what data is stored across the entire database and the relationships among entities (tables, attributes, constraints).\\n3. Internal Level (Physical Level): Describes how data is physically stored on storage media (record layouts, block sizes, B-Tree indexes).\\nThis separation achieves Data Independence and protects applications from physical storage changes."
            },
            {
                "marks": "10-Mark Question",
                "q": "Compare File Systems with DBMS. Detail the primary advantages of DBMS and explain the role of the Database Administrator (DBA).",
                "a": "1. Comparison: DBMS minimizes redundancy, guarantees consistency via ACID transactions, provides fine-grained concurrency control, supports declarative SQL, and features automated WAL recovery, whereas file systems suffer from duplicate files, concurrency race conditions, and lack of data abstraction.\\n2. Advantages of DBMS: (a) Reduced data redundancy, (b) Data integrity enforcement, (c) Multi-user concurrency without anomalies, (d) Backup and automated crash recovery, (e) Granular access security via GRANT/REVOKE.\\n3. Role of DBA: The Database Administrator is responsible for: (a) Defining conceptual and physical schemas, (b) Granting user authorizations and role permissions, (c) Monitoring and tuning query performance (indexing, buffer sizes), (d) Formulating and testing disaster recovery and automated backup plans."
            }
        ],
        "revision_60s": [
            "DBMS is the software engine; database is the persistent collection of data.",
            "Three Schema Architecture: External (views) → Conceptual (logical entities) → Internal (physical disk storage).",
            "Physical Data Independence: Change storage layout (e.g. HDD to NVMe) without touching logical tables.",
            "Logical Data Independence: Add/alter logical tables without breaking existing external views.",
            "Key components: Query Parser, Cost-based Query Optimizer, Execution Engine, Buffer Pool, WAL Manager.",
            "DBA manages schema definition, role-based security, query optimization, and disaster recovery."
        ]
    },

    # -------------------------------------------------------------------------
    # 2. ER Model
    # -------------------------------------------------------------------------
    "er-model": {
        "title": "ER Model",
        "subject": "dbms",
        "exam_definition": (
            "The Entity-Relationship (ER) model is a high-level conceptual data model that represents "
            "the structural design of a database through entities, their attributes, and the relationships "
            "connecting them, independent of physical storage implementation."
        ),
        "remember": "ER Model = Conceptual blueprint representing entities, attributes, and relationships.",
        "core_concept": (
            "Before writing SQL DDL tables, database engineers map real-world requirements into an ER diagram. "
            "Real-world objects are modeled as entities, descriptive properties as attributes, and business interactions "
            "as relationships with cardinality constraints (1:1, 1:N, M:N). Weak entities depend on strong owner entities "
            "for identification."
        ),
        "key_points": [
            "Entity: Distinguishable real-world object (e.g., Student, Course, Department).",
            "Entity Set: A collection of similar entities sharing identical attributes.",
            "Key Attribute: Uniquely identifies an entity instance (underlined in ER diagram).",
            "Weak Entity: Cannot be uniquely identified by its own attributes alone; requires identifying relationship with a strong owner entity (double rectangle).",
            "Cardinality Ratio: Specifies maximum entity participations (1:1, 1:N, M:N).",
            "Participation Constraint: Total participation (double line) means every entity must participate; Partial participation (single line) means some may participate."
        ],
        "classification": {
            "title": "Types of Attributes in ER Modeling",
            "items": [
                {"name": "Simple Attribute", "desc": "Atomic value that cannot be divided further (e.g., Age, RollNumber)."},
                {"name": "Composite Attribute", "desc": "Can be subdivided into sub-parts (e.g., Name → First_Name, Last_Name; Address → City, Pin)."},
                {"name": "Single-Valued Attribute", "desc": "Holds exactly one value for each entity instance (e.g., Date_of_Birth)."},
                {"name": "Multi-Valued Attribute", "desc": "Can hold multiple values for a single entity (e.g., PhoneNumbers, Degrees). Drawn as double ellipse."},
                {"name": "Derived Attribute", "desc": "Calculated dynamically from another attribute (e.g., Age calculated from DOB). Drawn as dashed ellipse."},
                {"name": "Key Attribute", "desc": "Uniquely identifies each entity instance (e.g., Student_ID). Text is underlined."}
            ]
        },
        "how_it_works": {
            "title": "ER to Relational Mapping Rules",
            "steps": [
                "Map Strong Entity Set: Creates a distinct table; simple attributes become columns; key attribute becomes Primary Key.",
                "Map Weak Entity Set: Creates a table containing weak entity attributes + Primary Key of Owner Entity as Composite Primary Key.",
                "Map 1:1 Relationship: Place Primary Key of one side as Foreign Key in the other side (preferably the side with total participation).",
                "Map 1:N Relationship: Place Primary Key of the 1-side as Foreign Key in the N-side table.",
                "Map M:N Relationship: Create a new separate Junction Table containing Foreign Keys of both participating entity sets as a Composite Primary Key.",
                "Map Multi-Valued Attribute: Create a separate table with (Entity_PK, MultiValued_Attribute) as Composite Primary Key."
            ],
            "diagram": (
                "ER Diagram Notation:\\n"
                "Rectangle        → Entity Set\\n"
                "Double Rectangle → Weak Entity Set\\n"
                "Ellipse          → Attribute\\n"
                "Double Ellipse   → Multi-Valued Attribute\\n"
                "Dashed Ellipse   → Derived Attribute\\n"
                "Diamond          → Relationship Set\\n"
                "Double Diamond   → Identifying Relationship for Weak Entity\\n"
                "Double Line      → Total Participation"
            )
        },
        "example": {
            "title": "Student-Course Enrollment Model",
            "scenario": (
                "Students enroll in Courses (M:N relationship). An employee has Dependents (Weak Entity). "
                "Student has attributes: `Roll_No` (Key), `Name` (Composite), `Phone` (Multi-Valued), `DOB` (Stored), `Age` (Derived).\\n"
                "Relational Mapping produces 3 tables for Student-Course:\\n"
                "1. `Students(roll_no PK, first_name, last_name, dob)`\\n"
                "2. `Student_Phones(roll_no FK, phone, PRIMARY KEY(roll_no, phone))`\\n"
                "3. `Courses(course_id PK, title, credits)`\\n"
                "4. `Enrollments(roll_no FK, course_id FK, semester, PRIMARY KEY(roll_no, course_id))`"
            ),
            "code": (
                "-- Relational implementation of M:N relationship with junction table\\n"
                "CREATE TABLE Students (\\n"
                "    roll_no INT PRIMARY KEY,\\n"
                "    first_name VARCHAR(50),\\n"
                "    last_name VARCHAR(50),\\n"
                "    dob DATE\\n"
                ");\\n\\n"
                "-- Multi-valued attribute mapped to separate table\\n"
                "CREATE TABLE Student_Phones (\\n"
                "    roll_no INT REFERENCES Students(roll_no) ON DELETE CASCADE,\\n"
                "    phone VARCHAR(15),\\n"
                "    PRIMARY KEY (roll_no, phone)\\n"
                ");\\n\\n"
                "-- Junction table for M:N relationship\\n"
                "CREATE TABLE Enrollments (\\n"
                "    roll_no INT REFERENCES Students(roll_no),\\n"
                "    course_id INT REFERENCES Courses(course_id),\\n"
                "    grade CHAR(2),\\n"
                "    PRIMARY KEY (roll_no, course_id)\\n"
                ");"
            )
        },
        "comparison": {
            "title": "Strong Entity Set vs Weak Entity Set",
            "headers": ["Feature", "Strong Entity Set", "Weak Entity Set"],
            "rows": [
                ["Primary Key", "Has its own primary key formed from its own attributes", "Does not have a primary key; has a partial key (discriminator)"],
                ["Diagram Notation", "Single rectangle", "Double rectangle"],
                ["Relationship", "Connected via standard diamond", "Connected to owner entity via double diamond (identifying relationship)"],
                ["Participation", "Can have partial or total participation", "Always has TOTAL participation with its owner entity"],
                ["Relational PK", "Its own key attribute", "Combination of Owner Entity PK + its own Partial Key (Discriminator)"]
            ]
        },
        "formulas": [
            {"name": "Derived Attribute Rule", "formula": "Derived_Attribute = f(Stored_Attribute)", "explanation": "Never physically store derived attributes if they can be dynamically computed from existing fields."},
            {"name": "M:N Mapping Rule", "formula": "Minimum Tables = 3 (EntityA Table + EntityB Table + Junction Table)", "explanation": "An M:N relationship can never be compressed into fewer than 3 tables without duplicating data."}
        ],
        "exam_tip": "Remember: A derived attribute is represented by a DASHED ellipse, while a multi-valued attribute is represented by a DOUBLE ellipse. Weak entities have DOUBLE rectangles and always exhibit TOTAL participation.",
        "common_confusion": {
            "wrong": "An entity and an attribute are interchangeable.",
            "correct": "An entity represents an independent real-world object (e.g. Student), while an attribute is a property that describes that entity (e.g. Student_ID, GPA).",
            "explanation": "If an object has its own independent attributes, it should be modeled as an entity, not an attribute."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is a Weak Entity Set and how is it represented in an ER diagram?",
                "a": "A weak entity set is an entity set that does not possess sufficient attributes to form a primary key on its own. It depends on a strong identifying entity set for identification. In an ER diagram, it is represented by a double rectangle, and its identifying relationship is represented by a double diamond."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the rules for converting an ER diagram into Relational Tables.",
                "a": "1. Strong Entity Set: Maps to a table with simple attributes as columns and key attribute as Primary Key.\\n2. Composite Attributes: Flattened into their simple components (e.g., Name → First_Name, Last_Name).\\n3. Multi-Valued Attributes: Mapped to a separate table with composite PK (Owner PK + Attribute).\\n4. 1:N Relationship: The primary key of the '1' side is placed as a Foreign Key in the 'N' side table.\\n5. M:N Relationship: Mapped to a distinct junction table containing Foreign Keys of both entity sets as a composite Primary Key."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the different types of attributes and cardinality ratios in ER modeling with suitable diagrams and examples.",
                "a": "1. Attribute Types:\\n- Simple: Atomic values (Roll_No).\\n- Composite: Subdivided into parts (Address → City, State, Zip).\\n- Single-Valued vs Multi-Valued: Single value (DOB) vs multiple values (PhoneNumbers, double ellipse).\\n- Stored vs Derived: Stored in DB (DOB) vs calculated on the fly (Age = current_date - DOB, dashed ellipse).\\n- Key Attribute: Underlined unique identifier.\\n2. Cardinality Ratios:\\n- 1:1: Citizen has one Passport (placed as FK in Passport).\\n- 1:N: Department employs many Employees (Dept_ID placed as FK in Employee).\\n- M:N: Students enroll in Courses (Requires separate junction table `Enrollments`).\\n3. Participation Constraints:\\n- Total: Every entity instance must participate (double line, e.g., Employee MUST belong to a Department).\\n- Partial: Some instances participate (single line, e.g., Not every employee manages a department)."
            }
        ],
        "revision_60s": [
            "ER Model components: Entities (objects), Attributes (properties), Relationships (associations).",
            "Symbols: Rectangle (Entity), Double Rect (Weak Entity), Ellipse (Attribute), Double Ellipse (Multivalued), Dashed Ellipse (Derived), Diamond (Relationship).",
            "Weak entity has a discriminator (dashed underline) and requires owner PK for identification.",
            "1:N mapping: Put Primary Key of 1-side into N-side table as Foreign Key.",
            "M:N mapping: Requires 3 tables (Table A, Table B, and Junction Table with composite PK).",
            "Derived attributes should be computed dynamically via queries, not stored statically."
        ]
    },

    # -------------------------------------------------------------------------
    # 3. Relational Model
    # -------------------------------------------------------------------------
    "relational-model": {
        "title": "Relational Model",
        "subject": "dbms",
        "exam_definition": (
            "The Relational Model represents data in the form of two-dimensional tables called Relations, "
            "where each row represents a Tuple of related data values and each column represents an Attribute "
            "governed by mathematical Set Theory and Relational Algebra."
        ),
        "remember": "Relation = Table, Tuple = Row, Attribute = Column, Domain = Permissible value pool.",
        "core_concept": (
            "Proposed by E.F. Codd in 1970, the relational model replaced complex pointer-based navigational models. "
            "All data is held in normalized relations. Mathematical Relational Algebra defines procedural operators "
            "(Selection, Projection, Join, Cartesian Product) that take relations as inputs and produce relations as outputs."
        ),
        "key_points": [
            "Relation: A 2D table of values with a unique name in the schema.",
            "Tuple: A single row representing an entity instance. Tuples are unordered and unique.",
            "Attribute: A named column describing a property of the relation.",
            "Degree: The total number of attributes (columns) in the relation.",
            "Cardinality: The total number of tuples (rows) currently in the relation.",
            "Domain: The set of atomic, allowable values for a specific attribute.",
            "Relational Constraints: Domain Constraint, Key Constraint, Entity Integrity, Referential Integrity."
        ],
        "classification": {
            "title": "Fundamental Relational Integrity Constraints",
            "items": [
                {"name": "Domain Constraint", "desc": "Every value in a column must be an atomic value from the attribute's defined domain (e.g., Age must be positive integer)."},
                {"name": "Key Constraint", "desc": "Every relation must have at least one candidate key that uniquely identifies every tuple (no two rows have identical candidate key values)."},
                {"name": "Entity Integrity Constraint", "desc": "No Primary Key value can be NULL because it identifies tuples in the relation."},
                {"name": "Referential Integrity Constraint", "desc": "A Foreign Key must either match a valid Primary Key value in the referenced relation, or be entirely NULL."}
            ]
        },
        "how_it_works": {
            "title": "Core Relational Algebra Operators",
            "steps": [
                "Selection (σ): Unary operator that filters rows based on a predicate condition (e.g., σ_gpa>8.5(Students)).",
                "Projection (π): Unary operator that selects specific columns and removes duplicate rows (e.g., π_name,dept(Students)).",
                "Cartesian Product (⨯): Binary operator combining each tuple of R with every tuple of S. Degree = deg(R)+deg(S), Cardinality = card(R)*card(S).",
                "Set Union (∪), Intersection (∩), Difference (-): Valid only on Union-Compatible relations (same degree and corresponding domains).",
                "Natural Join (⨝): Combines tuples from two relations having equal values on common attributes and eliminates duplicate join columns."
            ],
            "diagram": (
                "Relational Algebra Mathematical Notation:\\n"
                "σ_condition(Relation)   → Filter Rows\\n"
                "π_col1,col2(Relation)   → Select Columns\\n"
                "R ⨝_condition S         → Theta Join\\n"
                "R ⨝ S                   → Natural Join\\n"
                "R ⨯ S                   → Cartesian Product\\n"
                "ρ_NewName(Relation)     → Rename Operator"
            )
        },
        "example": {
            "title": "Relational Algebra Query Resolution",
            "scenario": (
                "Given `Students(sid, name, gpa, dept)` and `Courses(cid, cname, dept)`:\\n"
                "To find names of all Computer Science students with GPA > 8.0:\\n"
                "Relational Algebra: `π_name(σ_dept='CS' ∧ gpa>8.0 (Students))`\\n"
                "SQL Equivalent:\\n"
                "SELECT name FROM Students WHERE dept = 'CS' AND gpa > 8.0;"
            ),
            "code": (
                "-- Relational Algebra to SQL translation\\n"
                "-- π_name, cname (Students ⨝_Students.dept=Courses.dept Courses)\\n"
                "SELECT s.name, c.cname\\n"
                "FROM Students s\\n"
                "JOIN Courses c ON s.dept = c.dept\\n"
                "WHERE s.gpa >= 8.5;"
            )
        },
        "comparison": {
            "title": "Relational Algebra vs Relational Calculus",
            "headers": ["Feature", "Relational Algebra", "Relational Calculus"],
            "rows": [
                ["Paradigm", "Procedural query language", "Declarative (non-procedural) query language"],
                ["Query Style", "Specifies HOW to retrieve data (step-by-step operators)", "Specifies WHAT data to retrieve without execution steps"],
                ["Formal Basis", "Set-theoretic algebra and operators (σ, π, ⨝)", "First-Order Predicate Calculus (TRC and DRC)"],
                ["Usage", "Internal representation used by DBMS Query Optimizers", "Theoretical foundation for declarative languages like SQL"]
            ]
        },
        "formulas": [
            {"name": "Cartesian Product Cardinality", "formula": "|R ⨯ S| = |R| × |S|", "explanation": "The number of rows in R ⨯ S is the product of their respective row counts."},
            {"name": "Cartesian Product Degree", "formula": "Degree(R ⨯ S) = Degree(R) + Degree(S)", "explanation": "The number of columns in R ⨯ S is the sum of their columns."},
            {"name": "Selection Cardinality Range", "formula": "0 ≤ |σ_cond(R)| ≤ |R|", "explanation": "Selection filters between zero and all rows."}
        ],
        "exam_tip": "Remember: The Projection operator (π) in mathematical Relational Algebra automatically eliminates duplicate rows, whereas SQL SELECT preserves duplicates unless DISTINCT is specified.",
        "common_confusion": {
            "wrong": "Degree and Cardinality mean the same thing in a relation.",
            "correct": "Degree is the number of COLUMNS (attributes), while Cardinality is the number of ROWS (tuples).",
            "explanation": "If a table has 5 columns and 100 rows, Degree = 5 and Cardinality = 100."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the Entity Integrity Constraint?",
                "a": "The Entity Integrity constraint states that no primary key value can be NULL. This is because the primary key is used to uniquely identify individual tuples in a relation; if it were NULL, the DBMS could not distinguish the tuple from others."
            },
            {
                "marks": "5-Mark Question",
                "q": "Define the fundamental operators of Relational Algebra.",
                "a": "The five fundamental operators are:\\n1. Selection (σ): Selects tuples satisfying a specified predicate condition.\\n2. Projection (π): Selects specified columns and removes duplicate rows.\\n3. Cartesian Product (⨯): Combines each row of one relation with all rows of another.\\n4. Set Union (∪): Produces a relation containing all tuples present in either relation (requires union compatibility).\\n5. Set Difference (-): Produces tuples in the first relation that are not in the second."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the four primary Relational Integrity Constraints with examples of violations and how the DBMS handles them.",
                "a": "1. Domain Constraint: Column values must belong to the declared domain. Violation: Inserting 'ABC' into an INTEGER column.\\n2. Key Constraint: Candidate keys must be unique. Violation: Inserting two students with Roll_No = 101.\\n3. Entity Integrity Constraint: Primary Key attributes cannot be NULL. Violation: INSERT INTO Students(roll_no) VALUES(NULL) is rejected.\\n4. Referential Integrity Constraint: Foreign Key must reference an existing PK or be NULL. Violation: Inserting an enrollment with non-existent student_id. Handled via ON DELETE CASCADE (deletes child rows), ON DELETE SET NULL, or ON DELETE RESTRICT (rejects parent deletion)."
            }
        ],
        "revision_60s": [
            "Relation = Table; Tuple = Row; Attribute = Column.",
            "Degree = Number of columns; Cardinality = Number of rows.",
            "Entity Integrity: Primary Key cannot be NULL.",
            "Referential Integrity: Foreign Key must match an existing PK or be NULL.",
            "Projection (π) eliminates duplicate tuples in pure Relational Algebra.",
            "Cartesian product has Degree = deg(R)+deg(S) and Cardinality = card(R)*card(S)."
        ]
    },

    # -------------------------------------------------------------------------
    # 4. Keys
    # -------------------------------------------------------------------------
    "keys": {
        "title": "Keys",
        "subject": "dbms",
        "exam_definition": (
            "A Key in a relational database is an attribute or set of attributes that uniquely identifies "
            "tuples within a relation, prevents duplicate entries, and establishes referential relationships between tables."
        ),
        "remember": "Candidate Key = Minimal Superkey. Primary Key = Selected Candidate Key. Superkey ⊇ Candidate Key.",
        "core_concept": (
            "Without keys, relations would allow identical rows, violating the fundamental definition of a mathematical relation. "
            "A Superkey uniquely identifies rows but may contain extra columns. A Candidate Key is a minimal superkey with no redundant columns. "
            "Database designers select exactly one candidate key as the Primary Key. A Foreign Key references a Primary Key in another table."
        ),
        "key_points": [
            "Superkey: Any combination of attributes that uniquely identifies a row (may contain redundant attributes).",
            "Candidate Key: A minimal superkey; removing any attribute destroys uniqueness.",
            "Primary Key: Exactly one candidate key chosen by the DBA to uniquely identify tuples (cannot be NULL).",
            "Alternate Key: Any candidate key that was NOT chosen as the primary key.",
            "Foreign Key: Attribute in one table that references the Primary Key of another table (enforces referential integrity).",
            "Composite Key: A key composed of two or more attributes together."
        ],
        "classification": {
            "title": "Hierarchy of Database Keys",
            "items": [
                {"name": "Superkey (SK)", "desc": "Superset of attributes uniquely identifying a row (e.g. {Roll_No, Phone, Name})."},
                {"name": "Candidate Key (CK)", "desc": "Minimal superkey with zero redundant attributes (e.g. {Roll_No}, {Email})."},
                {"name": "Primary Key (PK)", "desc": "The single designated candidate key used for indexing and entity integrity (NO NULL allowed)."},
                {"name": "Alternate Key (AK)", "desc": "Remaining candidate keys (CK - PK)."},
                {"name": "Foreign Key (FK)", "desc": "References primary key in another table; can contain NULLs and duplicate values."}
            ]
        },
        "how_it_works": {
            "title": "Key Resolution & Referential Integrity Actions",
            "steps": [
                "Step 1: Identify all functional dependencies in relation R.",
                "Step 2: Find attribute closures (X+) to determine all Superkeys.",
                "Step 3: Strip extraneous attributes to determine Candidate Keys (minimal closures).",
                "Step 4: Designate the most compact, stable candidate key as the Primary Key.",
                "Step 5: Create Foreign Key constraints with appropriate referential trigger actions:\n  - ON DELETE CASCADE: Deletes child rows when parent is deleted.\n  - ON DELETE SET NULL: Sets child foreign key to NULL.\n  - ON DELETE RESTRICT / NO ACTION: Blocks parent deletion if child rows exist."
            ],
            "diagram": (
                "Key Inclusion Hierarchy:\\n"
                "+---------------------------------------------------+\\n"
                "| Superkeys (e.g. {Roll}, {Roll, Name}, {Email, Name})|\\n"
                "|   +---------------------------------------------+   |\\n"
                "|   | Candidate Keys (e.g. {Roll}, {Email})       |   |\\n"
                "|   |   +-----------------------+ +-------------+ |   |\\n"
                "|   |   | Primary Key ({Roll})  | | Alternate   | |   |\\n"
                "|   |   | (Unique, NOT NULL)    | | Key ({Email})| |   |\\n"
                "|   |   +-----------------------+ +-------------+ |   |\\n"
                "|   +---------------------------------------------+   |\\n"
                "+---------------------------------------------------+"
            )
        },
        "example": {
            "title": "Student & Department Key Architecture",
            "scenario": (
                "Consider `Students(roll_no, email, aadhaar_no, name, dept_id)`:\\n"
                "- Superkeys: {roll_no}, {email}, {aadhaar_no}, {roll_no, name}, {email, name}\\n"
                "- Candidate Keys: {roll_no}, {email}, {aadhaar_no} (each minimal and unique)\\n"
                "- Primary Key chosen: `roll_no`\\n"
                "- Alternate Keys: `email`, `aadhaar_no`\\n"
                "- Foreign Key: `dept_id` referencing `Departments(dept_id)`"
            ),
            "code": (
                "CREATE TABLE Departments (\\n"
                "    dept_id INT PRIMARY KEY,\\n"
                "    dept_name VARCHAR(50) NOT NULL\\n"
                ");\\n\\n"
                "CREATE TABLE Students (\\n"
                "    roll_no INT PRIMARY KEY,              -- Chosen Primary Key\\n"
                "    email VARCHAR(100) UNIQUE NOT NULL,   -- Alternate Key (Unique Constraint)\\n"
                "    aadhaar_no VARCHAR(12) UNIQUE,        -- Alternate Key\\n"
                "    name VARCHAR(50) NOT NULL,\\n"
                "    dept_id INT REFERENCES Departments(dept_id) ON DELETE RESTRICT -- Foreign Key\\n"
                ");"
            )
        },
        "comparison": {
            "title": "Primary Key vs Candidate Key vs Foreign Key",
            "headers": ["Feature", "Primary Key", "Candidate Key", "Foreign Key"],
            "rows": [
                ["Uniqueness", "Must be strictly unique", "Must be strictly unique", "Can contain duplicate values (e.g. many students in 1 dept)"],
                ["NULL Allowed?", "Never (violates Entity Integrity)", "Never allowed in candidate key attributes", "Yes (unless defined with NOT NULL)"],
                ["Count per Table", "Exactly ONE", "One or more possible", "Zero, one, or multiple allowed"],
                ["Selected From", "Selected from candidate keys", "Minimal superkeys", "Points to primary key of another table"],
                ["Purpose", "Identify row uniquely", "Candidate to identify row", "Enforce referential relationship across tables"]
            ]
        },
        "formulas": [
            {"name": "Candidate Key Invariant", "formula": "If K is Candidate Key, then K+ = R and ∀ A ∈ K, (K - {A})+ ≠ R", "explanation": "Closure of K must cover all attributes, and no proper subset of K can cover all attributes."},
            {"name": "Alternate Key Set", "formula": "Alternate_Keys = Candidate_Keys \\ {Primary_Key}", "explanation": "Alternate keys are simply unused candidate keys."}
        ],
        "exam_tip": "Remember: Every Candidate Key is a Superkey, but every Superkey is NOT a Candidate Key. A Candidate Key is strictly a MINIMAL Superkey.",
        "common_confusion": {
            "wrong": "A foreign key must always point to a column with the exact same name.",
            "correct": "A foreign key must reference a column that is a Primary Key (or Unique) with a matching data type; the column names can be completely different.",
            "explanation": "e.g. `Orders.customer_ref` can reference `Customers.cust_id`."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the difference between a Super Key and a Candidate Key?",
                "a": "A Super Key is any set of attributes that uniquely identifies a row in a relation (it may include redundant attributes). A Candidate Key is a minimal Super Key, meaning no proper subset of it can uniquely identify a row."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Foreign Keys and the various ON DELETE referential actions.",
                "a": "A Foreign Key is an attribute in a child table that references the Primary Key of a parent table to maintain referential integrity. When a parent row is deleted, the DBMS enforces one of three actions:\\n1. ON DELETE CASCADE: Automatically deletes all child rows referencing the deleted parent.\\n2. ON DELETE SET NULL: Sets the foreign key value in child rows to NULL.\\n3. ON DELETE RESTRICT / NO ACTION: Rejects the parent deletion if any dependent child rows exist."
            },
            {
                "marks": "10-Mark Question",
                "q": "Given a relation R(A, B, C, D, E) with FDs F = {A -> BC, CD -> E, B -> D, E -> A}. Find all candidate keys.",
                "a": "Step 1: Identify attributes that never appear on the right-hand side of any FD. Here, all attributes appear on RHS.\\nStep 2: Check closure of single attributes:\\n- A+ = {A, B, C, D, E} (Since A->BC, B->D, CD->E). A covers all attributes and is minimal. Hence, A is a Candidate Key.\\n- E+ = {E, A, B, C, D} (Since E->A, and A covers all). E is a Candidate Key.\\n- (CD)+ = {C, D, E, A, B} (Since CD->E, E->A, A covers all). CD is a Candidate Key.\\n- (BC)+: Since B->D, (BC)+ = (BCD)+ = {B, C, D, E, A}. BC is a Candidate Key.\\nConclusion: The candidate keys for relation R are: {A}, {E}, {CD}, and {BC}."
            }
        ],
        "revision_60s": [
            "Superkey = any set of columns uniquely identifying a row.",
            "Candidate Key = minimal superkey with no redundant columns.",
            "Primary Key = selected candidate key; CANNOT be NULL.",
            "Alternate Keys = all candidate keys not chosen as the primary key.",
            "Foreign Key = points to PK of another table; can be NULL.",
            "ON DELETE CASCADE deletes child records; ON DELETE RESTRICT blocks deletion."
        ]
    },

    # -------------------------------------------------------------------------
    # 5. SQL Basics
    # -------------------------------------------------------------------------
    "sql-basics": {
        "title": "SQL Basics",
        "subject": "dbms",
        "exam_definition": (
            "Structured Query Language (SQL) is the standard declarative domain-specific language used for "
            "defining, querying, modifying, and controlling access to data held in a relational database management system."
        ),
        "remember": "SQL is Declarative: You tell the DBMS WHAT data you want, not HOW to retrieve it.",
        "core_concept": (
            "SQL is structured into distinct sub-languages based on operational scope: DDL (structure), DML (data), "
            "DCL (permissions), and TCL (transaction boundaries). Understanding the behavioral differences between "
            "similar statements like DELETE, TRUNCATE, and DROP is one of the most heavily tested exam concepts."
        ),
        "key_points": [
            "DDL (Data Definition Language): CREATE, ALTER, DROP, TRUNCATE, RENAME. Modifies schema definitions (auto-commit).",
            "DML (Data Manipulation Language): SELECT, INSERT, UPDATE, DELETE. Operates on table records (can be rolled back).",
            "DCL (Data Control Language): GRANT, REVOKE. Controls user authorizations and security privileges.",
            "TCL (Transaction Control Language): COMMIT, ROLLBACK, SAVEPOINT. Controls transaction atomicity.",
            "SQL Data Types: INT, BIGINT, NUMERIC(p,s), VARCHAR(n), CHAR(n), DATE, TIMESTAMP, BOOLEAN."
        ],
        "classification": {
            "title": "Sub-languages of SQL",
            "items": [
                {"name": "DDL", "desc": "Commands that define and modify the database structure. Changes are permanent and cannot be rolled back."},
                {"name": "DML / DQL", "desc": "Commands that manipulate data values in existing relations (SELECT is often classified as DQL)."},
                {"name": "DCL", "desc": "Commands used by DBAs to grant or revoke operational privileges to database user accounts."},
                {"name": "TCL", "desc": "Commands that manage transaction state and control rollback points."}
            ]
        },
        "how_it_works": {
            "title": "SQL Command Categories and Lifecycles",
            "steps": [
                "DDL Execution: Acquires metadata locks, modifies Data Dictionary tables, allocates physical storage segments, auto-commits.",
                "DML Execution: Checks table schema, evaluates WHERE filter conditions, updates buffer pool pages, writes undo/redo log records.",
                "TCL Execution: COMMIT flushes WAL logs to disk making changes durable; ROLLBACK uses undo logs to reverse uncommitted modifications."
            ],
            "diagram": (
                "SQL Architecture Hierarchy:\\n"
                "             SQL Sub-Languages\\n"
                "   ┌─────────┬──────────┬──────────┬─────────┐\\n"
                "  DDL       DML        DCL        TCL       DQL\\n"
                " CREATE    INSERT     GRANT      COMMIT    SELECT\\n"
                " ALTER     UPDATE     REVOKE     ROLLBACK\\n"
                " DROP      DELETE                SAVEPOINT\\n"
                " TRUNCATE"
            )
        },
        "example": {
            "title": "Schema Definition & Manipulation Walkthrough",
            "scenario": (
                "Creating an employee table, adding an index, inserting rows, and demonstrating rollback:"
            ),
            "code": (
                "-- DDL: Define structure\\n"
                "CREATE TABLE Employees (\\n"
                "    emp_id INT PRIMARY KEY,\\n"
                "    name VARCHAR(50) NOT NULL,\\n"
                "    salary NUMERIC(10,2) CHECK (salary > 0)\\n"
                ");\\n\\n"
                "-- DML: Insert and Update records\\n"
                "INSERT INTO Employees VALUES (101, 'Aditi Rao', 85000.00);\\n"
                "UPDATE Employees SET salary = 92000.00 WHERE emp_id = 101;\\n\\n"
                "-- TCL: Commit transaction\\n"
                "COMMIT;"
            )
        },
        "comparison": {
            "title": "DELETE vs TRUNCATE vs DROP",
            "headers": ["Feature", "DELETE", "TRUNCATE", "DROP"],
            "rows": [
                ["Command Type", "DML (Data Manipulation)", "DDL (Data Definition)", "DDL (Data Definition)"],
                ["Action", "Removes specified rows satisfying WHERE clause", "Removes ALL rows, resets high-water mark", "Deletes entire table schema and data permanently"],
                ["WHERE Clause", "Supported (e.g. WHERE id = 5)", "Not supported (always empties whole table)", "Not applicable"],
                ["Rollback", "Can be rolled back in a transaction", "Cannot be rolled back in most databases (auto-commits)", "Cannot be rolled back"],
                ["Speed & Logging", "Slow — logs row deletions individually in WAL", "Very Fast — deallocates entire data pages", "Instantaneous — drops schema metadata"],
                ["Triggers", "Fires ON DELETE triggers", "Does NOT fire DELETE triggers", "Does NOT fire triggers"]
            ]
        },
        "formulas": [
            {"name": "CHAR vs VARCHAR", "formula": "CHAR(n) = Fixed length (padded with spaces); VARCHAR(n) = Variable length up to n", "explanation": "Use CHAR for fixed-width codes like ISO country codes ('IN', 'US'); use VARCHAR for names and emails."}
        ],
        "exam_tip": "Remember: TRUNCATE is a DDL command, not DML. It is faster than DELETE because it deallocates whole data pages rather than logging row-by-row deletions.",
        "common_confusion": {
            "wrong": "TRUNCATE and DELETE without a WHERE clause do the exact same thing.",
            "correct": "Both leave an empty table, but TRUNCATE is DDL (resets auto-increment IDs, deallocates pages, no row logging, cannot be rolled back in MySQL/Oracle), whereas DELETE is DML (logs every row, fires triggers, can be rolled back).",
            "explanation": "Exam questions often test why TRUNCATE is drastically faster than DELETE on a 10-million row table."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the difference between DDL and DML?",
                "a": "DDL (Data Definition Language) commands like CREATE, ALTER, and DROP define and modify the schema structure of the database and auto-commit. DML (Data Manipulation Language) commands like INSERT, UPDATE, and DELETE modify data values within existing tables and can be rolled back."
            },
            {
                "marks": "5-Mark Question",
                "q": "Compare DELETE, TRUNCATE, and DROP commands in SQL.",
                "a": "1. DELETE is a DML command that removes specific rows using a WHERE clause, logs each row deletion, fires triggers, and can be rolled back.\n2. TRUNCATE is a DDL command that removes all rows by deallocating data pages, resets identity seeds, does not fire triggers, and is much faster than DELETE.\n3. DROP is a DDL command that completely destroys both the table data and its schema definition from the system catalog."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the structure of SQL commands with categories, syntax, constraints, and transaction management.",
                "a": "1. DDL: CREATE TABLE, ALTER TABLE, DROP TABLE, TRUNCATE TABLE. Used to manage schema definitions.\n2. DML: INSERT INTO, UPDATE SET, DELETE FROM. Used to manipulate rows.\n3. DQL: SELECT column FROM table WHERE condition. Used for data retrieval.\n4. DCL: GRANT privilege ON object TO user; REVOKE privilege FROM user. Controls role security.\n5. TCL: COMMIT (persists state), ROLLBACK (undoes uncommitted work), SAVEPOINT (partial rollback point).\n6. Integrity Constraints in SQL: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY REFERENCES, CHECK, DEFAULT."
            }
        ],
        "revision_60s": [
            "DDL: CREATE, ALTER, DROP, TRUNCATE (Schema changes, Auto-commit).",
            "DML: INSERT, UPDATE, DELETE (Record changes, Rollbackable).",
            "DCL: GRANT, REVOKE (Permissions).",
            "TCL: COMMIT, ROLLBACK, SAVEPOINT (Transactions).",
            "DELETE removes selected rows; TRUNCATE deallocates all pages; DROP destroys table.",
            "CHAR is fixed-width (padded); VARCHAR is variable-width."
        ]
    },

    # -------------------------------------------------------------------------
    # 6. SQL Queries
    # -------------------------------------------------------------------------
    "sql-queries": {
        "title": "SQL Queries",
        "subject": "dbms",
        "exam_definition": (
            "SQL Queries are declarative data manipulation statements (DQL) that filter, aggregate, group, "
            "and transform relational data to answer analytical questions using logical clause execution pipelines."
        ),
        "remember": "Logical Order of Execution: FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.",
        "core_concept": (
            "Writing correct SQL requires understanding the difference between the physical syntax order and the "
            "logical execution order of a query. In exams, questions frequently test WHERE vs HAVING: WHERE filters rows "
            "BEFORE grouping, while HAVING filters aggregated groups AFTER GROUP BY. Aggregate functions ignore NULL values, "
            "except for COUNT(*)."
        ),
        "key_points": [
            "Logical Execution Order: FROM → ON → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.",
            "Aggregate Functions: COUNT(), SUM(), AVG(), MIN(), MAX(). All ignore NULLs except COUNT(*).",
            "GROUP BY: Collapses tuples sharing identical group-by values into single summary rows.",
            "HAVING: Filters aggregated groups based on conditions involving aggregate functions.",
            "WHERE vs HAVING: WHERE cannot filter on aggregate functions (e.g. WHERE AVG(salary) > 50000 is ILLEGAL).",
            "Pattern Matching: LIKE with '%' (zero or more chars) and '_' (exactly one char)."
        ],
        "classification": {
            "title": "SQL Aggregate & Scalar Functions",
            "items": [
                {"name": "Aggregate Functions", "desc": "Operate on a column across multiple rows to return a single value: COUNT, SUM, AVG, MIN, MAX."},
                {"name": "Scalar Functions", "desc": "Operate on individual values row-by-row: UPPER(), LOWER(), LENGTH(), ROUND(), COALESCE()."},
                {"name": "Date Functions", "desc": "EXTRACT(YEAR FROM date), NOW(), DATE_DIFF()."}
            ]
        },
        "how_it_works": {
            "title": "Step-by-Step Logical Query Processing Pipeline",
            "steps": [
                "1. FROM & JOIN: Locate participating tables, evaluate ON predicates, generate joined virtual table.",
                "2. WHERE: Evaluate row-level filtering conditions; discard rows evaluating to FALSE or NULL.",
                "3. GROUP BY: Partition remaining rows into groups having identical values in group-by expressions.",
                "4. HAVING: Evaluate group-level filter predicates against aggregates (e.g., COUNT(*) > 5).",
                "5. SELECT: Project requested columns or aggregate expressions, assign aliases.",
                "6. DISTINCT: Eliminate duplicate rows from the projected result set.",
                "7. ORDER BY: Sort final rows ascending (ASC, default) or descending (DESC).",
                "8. LIMIT / OFFSET: Return specified subset of rows for pagination."
            ],
            "diagram": (
                "SQL Query Processing Pipeline:\\n"
                "FROM & JOIN  → Identify input tables\\n"
                "    ↓\\n"
                "WHERE        → Filter individual rows\\n"
                "    ↓\\n"
                "GROUP BY     → Form groups\\n"
                "    ↓\\n"
                "HAVING       → Filter groups using aggregates\\n"
                "    ↓\\n"
                "SELECT       → Compute expressions & aliases\\n"
                "    ↓\\n"
                "DISTINCT     → Remove duplicates\\n"
                "    ↓\\n"
                "ORDER BY     → Sort output rows\\n"
                "    ↓\\n"
                "LIMIT/OFFSET → Paginate results"
            )
        },
        "example": {
            "title": "Department Salary Aggregation Query",
            "scenario": (
                "Find all departments that have more than 3 employees earning over $40,000, "
                "and display the department name along with the average salary, sorted by average salary descending:"
            ),
            "code": (
                "SELECT department, AVG(salary) AS avg_sal, COUNT(*) AS emp_count\\n"
                "FROM Employees\\n"
                "WHERE salary > 40000            -- Filter rows BEFORE grouping\\n"
                "GROUP BY department             -- Group remaining rows\\n"
                "HAVING COUNT(*) > 3             -- Filter groups AFTER grouping\\n"
                "ORDER BY avg_sal DESC;          -- Sort final results"
            )
        },
        "comparison": {
            "title": "WHERE Clause vs HAVING Clause",
            "headers": ["Feature", "WHERE Clause", "HAVING Clause"],
            "rows": [
                ["Applies To", "Individual rows before grouping", "Aggregated groups after GROUP BY"],
                ["Aggregate Functions", "CANNOT contain aggregate functions (e.g. WHERE AVG(sal)>50k is invalid)", "CAN contain aggregate functions (e.g. HAVING COUNT(*)>3)"],
                ["Execution Order", "Executes BEFORE GROUP BY", "Executes AFTER GROUP BY"],
                ["Can be used without GROUP BY?", "Yes", "Yes (treats the entire table as a single aggregate group)"],
                ["Performance", "Faster — reduces number of rows before aggregation", "Slower — operates on aggregated groups"]
            ]
        },
        "formulas": [
            {"name": "COUNT(*) vs COUNT(column)", "formula": "COUNT(*) counts all rows; COUNT(col) counts rows where col IS NOT NULL", "explanation": "If a column has 10 rows and 2 NULLs, COUNT(*) = 10 while COUNT(col) = 8."},
            {"name": "AVG Calculation", "formula": "AVG(col) = SUM(col) / COUNT(col)", "explanation": "NULL values are completely omitted from both the numerator and denominator."}
        ],
        "exam_tip": "Remember: The WHERE clause executes BEFORE the GROUP BY clause. Therefore, you can NEVER use aggregate functions like COUNT(), SUM(), or AVG() inside a WHERE clause!",
        "common_confusion": {
            "wrong": "COUNT(*) and COUNT(column_name) always return the identical result.",
            "correct": "COUNT(*) counts total tuples including rows containing NULLs, whereas COUNT(col) counts only rows where the specified column is NOT NULL.",
            "explanation": "If an employee has bonus = NULL, COUNT(*) counts them, but COUNT(bonus) ignores them."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Why can aggregate functions not be used in a WHERE clause?",
                "a": "Because the WHERE clause filters individual rows during step 2 of query processing, before rows are grouped and aggregated in step 3. Aggregate functions compute values across groups, which only exist after the GROUP BY step; therefore, aggregate filters must be placed in the HAVING clause."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the difference between WHERE and HAVING with a suitable example.",
                "a": "1. WHERE filters individual rows before grouping takes place. It cannot use aggregate functions.\n2. HAVING filters groups of rows after aggregation has been performed.\nExample:\nSELECT dept_id, AVG(salary)\nFROM Employees\nWHERE status = 'Active'         -- WHERE filters active rows\nGROUP BY dept_id\nHAVING AVG(salary) > 60000;     -- HAVING filters departments with avg salary > 60000."
            },
            {
                "marks": "10-Mark Question",
                "q": "Detail the logical execution order of an SQL query and write queries for 3 practical analytical scenarios.",
                "a": "1. Execution Order: FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.\n2. Queries:\n(a) Find second highest salary:\nSELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);\n(b) Departments where average salary > company average:\nSELECT dept_id, AVG(salary) FROM Employees GROUP BY dept_id HAVING AVG(salary) > (SELECT AVG(salary) FROM Employees);\n(c) Count of students enrolled in more than 2 courses:\nSELECT student_id, COUNT(course_id) FROM Enrollments GROUP BY student_id HAVING COUNT(course_id) > 2;"
            }
        ],
        "revision_60s": [
            "Execution order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.",
            "WHERE filters rows before grouping; HAVING filters groups after aggregation.",
            "Aggregate functions (SUM, AVG, MIN, MAX, COUNT) ignore NULLs.",
            "COUNT(*) counts all rows; COUNT(column) ignores NULLs in that column.",
            "LIKE '%' matches any number of characters; '_' matches exactly one character.",
            "ORDER BY defaults to ASC (ascending); DESC sorts descending."
        ]
    }
}
'''

with open(os.path.join(os.path.dirname(__file__), "curriculum", "dbms.py"), "w", encoding="utf-8") as f:
    f.write(DBMS_MODULE_CODE)

print("DBMS module written successfully with initial 6 topics.")
