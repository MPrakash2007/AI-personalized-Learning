"""
Generates complete, exam-oriented academic dataset for all 12 DBMS topics.
Saves to backend/curriculum/data/dbms.json.
"""
import os
import json

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dbms.json"))

DBMS_TOPICS = {
    "dbms-fundamentals": {
        "title": "DBMS Fundamentals",
        "subject": "dbms",
        "exam_definition": (
            "A Database Management System (DBMS) is specialized system software that provides an interface "
            "for creating, storing, retrieving, updating, and managing data in a database while enforcing "
            "security, data integrity, concurrency control, and automated crash recovery."
        ),
        "remember": "DBMS = Software system used to manage, query, and protect databases.",
        "core_concept": (
            "Traditional file processing systems suffer from data redundancy, inconsistency, lack of atomicity, "
            "and poor concurrency control. A DBMS eliminates these bottlenecks through a centralized data catalog, "
            "declarative query interface (SQL), and ACID transaction guarantees. It provides three levels of abstraction "
            "separating user applications from physical disk layouts."
        ),
        "key_points": [
            "Data Abstraction: Hides physical storage details across View, Conceptual, and Internal levels.",
            "Data Independence: Allows altering storage or logical schemas without rewriting application queries.",
            "Minimal Redundancy: Centralized schema avoids duplicate data files across departments.",
            "Concurrency Control: Enables simultaneous multi-user access without race conditions or lost updates.",
            "Crash Recovery: Write-Ahead Logging (WAL) and checkpointing restore consistency after power failures.",
            "Integrity Constraints: Enforces domain rules, primary keys, foreign keys, and user permissions."
        ],
        "classification": {
            "title": "Classification of Database Management Systems",
            "items": [
                {"name": "Hierarchical DBMS", "desc": "Tree-like parent-child structure (e.g. IBM IMS). 1:N relationships only."},
                {"name": "Network DBMS", "desc": "Graph-based structure with record types and set types (e.g. IDMS). M:N allowed."},
                {"name": "Relational DBMS (RDBMS)", "desc": "Tables (relations) with rows and columns based on relational algebra (e.g. PostgreSQL, MySQL)."},
                {"name": "Object-Oriented DBMS", "desc": "Stores objects, classes, and inheritance directly in persistent storage."},
                {"name": "NoSQL DBMS", "desc": "Non-relational distributed databases (Key-Value, Document, Columnar, Graph) optimized for horizontal scalability."}
            ]
        },
        "how_it_works": {
            "title": "DBMS Query Processing Pipeline",
            "steps": [
                "1. User Query: User/application issues a declarative SQL query.",
                "2. Parser & Lexer: Validates SQL syntax and checks table/column existence in the Data Dictionary.",
                "3. Query Optimizer: Generates alternative execution plans, estimates I/O cost, and chooses the optimal plan.",
                "4. Execution Engine: Executes relational operators (Index Scan, Hash Join, Filter) interacting with Buffer Manager.",
                "5. Buffer Pool Manager: Checks RAM buffer cache; if page is absent, reads disk blocks via Storage Manager.",
                "6. Concurrency Control: Grants Shared or Exclusive locks to guarantee serializable isolation.",
                "7. Recovery Manager: Flushes Write-Ahead Log (WAL) records before committing changes to disk."
            ],
            "diagram": "User Query → Parser → Query Optimizer → Execution Engine → Buffer Pool Manager → Physical Storage & WAL"
        },
        "example": {
            "title": "University Database System Architecture",
            "scenario": (
                "In a file system, Admissions, Accounts, and Hostels each maintain separate Excel/CSV files. "
                "Updating a student's address in Admissions leaves obsolete data in Accounts.\n"
                "In a DBMS, a single centralized `Students` table is referenced by `Enrollments` and `Fee_Receipts`. "
                "Updating student address once immediately reflects across all university departments."
            ),
            "code": (
                "-- Unified schema with referential constraint\n"
                "CREATE TABLE Students (\n"
                "    student_id INT PRIMARY KEY,\n"
                "    name VARCHAR(100) NOT NULL,\n"
                "    department VARCHAR(50)\n"
                ");\n\n"
                "CREATE TABLE Enrollments (\n"
                "    enrollment_id INT PRIMARY KEY,\n"
                "    student_id INT REFERENCES Students(student_id),\n"
                "    course_code VARCHAR(10)\n"
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
            {"name": "Three-Schema Levels", "formula": "External Level (Views) → Conceptual Level (Logical Schema) → Internal Level (Physical Storage)", "explanation": "ANSI/SPARC architecture separates user views from disk block layout."},
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
                "a": "The Three-Schema Architecture divides a database into three abstraction levels:\n1. External Level (View Level): Describes part of the database relevant to a specific user group, hiding the rest.\n2. Conceptual Level (Logical Level): Describes what data is stored across the entire database and the relationships among entities (tables, attributes, constraints).\n3. Internal Level (Physical Level): Describes how data is physically stored on storage media (record layouts, block sizes, B-Tree indexes).\nThis separation achieves Data Independence and protects applications from physical storage changes."
            },
            {
                "marks": "10-Mark Question",
                "q": "Compare File Systems with DBMS. Detail the primary advantages of DBMS and explain the role of the Database Administrator (DBA).",
                "a": "1. Comparison: DBMS minimizes redundancy, guarantees consistency via ACID transactions, provides fine-grained concurrency control, supports declarative SQL, and features automated WAL recovery, whereas file systems suffer from duplicate files, concurrency race conditions, and lack of data abstraction.\n2. Advantages of DBMS: (a) Reduced data redundancy, (b) Data integrity enforcement, (c) Multi-user concurrency without anomalies, (d) Backup and automated crash recovery, (e) Granular access security via GRANT/REVOKE.\n3. Role of DBA: The Database Administrator is responsible for: (a) Defining conceptual and physical schemas, (b) Granting user authorizations and role permissions, (c) Monitoring and tuning query performance (indexing, buffer sizes), (d) Formulating and testing disaster recovery and automated backup plans."
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
                "ER Diagram Symbols:\n"
                "Rectangle: Entity Set | Double Rectangle: Weak Entity Set\n"
                "Ellipse: Attribute | Double Ellipse: Multi-Valued | Dashed Ellipse: Derived\n"
                "Diamond: Relationship | Double Diamond: Identifying Relationship | Double Line: Total Participation"
            )
        },
        "example": {
            "title": "Student-Course Enrollment Model",
            "scenario": (
                "Students enroll in Courses (M:N relationship). An employee has Dependents (Weak Entity).\n"
                "Relational Mapping produces 3 tables for Student-Course:\n"
                "1. Students(roll_no PK, first_name, last_name, dob)\n"
                "2. Student_Phones(roll_no FK, phone, PRIMARY KEY(roll_no, phone))\n"
                "3. Courses(course_id PK, title, credits)\n"
                "4. Enrollments(roll_no FK, course_id FK, semester, PRIMARY KEY(roll_no, course_id))"
            ),
            "code": (
                "CREATE TABLE Students (\n"
                "    roll_no INT PRIMARY KEY,\n"
                "    name VARCHAR(50),\n"
                "    dob DATE\n"
                ");\n\n"
                "CREATE TABLE Enrollments (\n"
                "    roll_no INT REFERENCES Students(roll_no),\n"
                "    course_id INT REFERENCES Courses(course_id),\n"
                "    PRIMARY KEY (roll_no, course_id)\n"
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
                "a": "1. Strong Entity Set: Maps to a table with simple attributes as columns and key attribute as Primary Key.\n2. Composite Attributes: Flattened into their simple components.\n3. Multi-Valued Attributes: Mapped to a separate table with composite PK (Owner PK + Attribute).\n4. 1:N Relationship: The primary key of the '1' side is placed as a Foreign Key in the 'N' side table.\n5. M:N Relationship: Mapped to a distinct junction table containing Foreign Keys of both entity sets as a composite Primary Key."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the different types of attributes and cardinality ratios in ER modeling with suitable diagrams and examples.",
                "a": "1. Attribute Types:\n- Simple: Atomic values (Roll_No).\n- Composite: Subdivided into parts (Address → City, State, Zip).\n- Single-Valued vs Multi-Valued: Single value (DOB) vs multiple values (PhoneNumbers, double ellipse).\n- Stored vs Derived: Stored in DB (DOB) vs calculated on the fly (Age = current_date - DOB, dashed ellipse).\n- Key Attribute: Underlined unique identifier.\n2. Cardinality Ratios:\n- 1:1: Citizen has one Passport.\n- 1:N: Department employs many Employees.\n- M:N: Students enroll in Courses (Requires separate junction table Enrollments)."
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
                {"name": "Domain Constraint", "desc": "Every value in a column must be an atomic value from the attribute's defined domain."},
                {"name": "Key Constraint", "desc": "Every relation must have at least one candidate key that uniquely identifies every tuple."},
                {"name": "Entity Integrity Constraint", "desc": "No Primary Key value can be NULL because it identifies tuples in the relation."},
                {"name": "Referential Integrity Constraint", "desc": "A Foreign Key must either match a valid Primary Key in the referenced relation, or be NULL."}
            ]
        },
        "how_it_works": {
            "title": "Core Relational Algebra Operators",
            "steps": [
                "Selection (σ): Unary operator that filters rows based on a predicate condition (e.g., σ_gpa>8.5(Students)).",
                "Projection (π): Unary operator that selects specific columns and removes duplicate rows (e.g., π_name,dept(Students)).",
                "Cartesian Product (⨯): Combines each tuple of R with every tuple of S. Degree = deg(R)+deg(S), Cardinality = card(R)*card(S).",
                "Set Union (∪), Intersection (∩), Difference (-): Valid only on Union-Compatible relations.",
                "Natural Join (⨝): Combines tuples from two relations having equal values on common attributes."
            ],
            "diagram": "σ (Filter Rows) | π (Select Columns) | ⨯ (Cartesian Product) | ⨝ (Join) | ρ (Rename)"
        },
        "example": {
            "title": "Relational Algebra Query Resolution",
            "scenario": (
                "Given `Students(sid, name, gpa, dept)` and `Courses(cid, cname, dept)`:\n"
                "To find names of all Computer Science students with GPA > 8.0:\n"
                "Relational Algebra: `π_name(σ_dept='CS' ∧ gpa>8.0 (Students))`\n"
                "SQL: SELECT name FROM Students WHERE dept = 'CS' AND gpa > 8.0;"
            ),
            "code": (
                "-- Relational Algebra to SQL translation\n"
                "SELECT s.name, c.cname\n"
                "FROM Students s\n"
                "JOIN Courses c ON s.dept = c.dept\n"
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
                "a": "The five fundamental operators are: (1) Selection (σ), (2) Projection (π), (3) Cartesian Product (⨯), (4) Set Union (∪), and (5) Set Difference (-)."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the four primary Relational Integrity Constraints with examples of violations and how the DBMS handles them.",
                "a": "1. Domain Constraint: Column values must belong to declared domain.\n2. Key Constraint: Candidate keys must be strictly unique.\n3. Entity Integrity: Primary Key cannot be NULL.\n4. Referential Integrity: Foreign Key must match an existing PK or be NULL. Violations are handled via ON DELETE CASCADE, ON DELETE SET NULL, or ON DELETE RESTRICT."
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
            "title": "Key Resolution & Referential Actions",
            "steps": [
                "Step 1: Identify all functional dependencies in relation R.",
                "Step 2: Find attribute closures (X+) to determine all Superkeys.",
                "Step 3: Strip extraneous attributes to determine Candidate Keys (minimal closures).",
                "Step 4: Designate the most compact, stable candidate key as the Primary Key.",
                "Step 5: Create Foreign Key constraints with referential actions (ON DELETE CASCADE, ON DELETE SET NULL, ON DELETE RESTRICT)."
            ],
            "diagram": "Superkeys ⊇ Candidate Keys ⊇ Primary Key + Alternate Keys"
        },
        "example": {
            "title": "Student & Department Key Architecture",
            "scenario": (
                "Consider `Students(roll_no, email, aadhaar_no, name, dept_id)`:\n"
                "- Superkeys: {roll_no}, {email}, {aadhaar_no}, {roll_no, name}, {email, name}\n"
                "- Candidate Keys: {roll_no}, {email}, {aadhaar_no} (each minimal and unique)\n"
                "- Primary Key chosen: `roll_no`\n"
                "- Alternate Keys: `email`, `aadhaar_no`\n"
                "- Foreign Key: `dept_id` referencing `Departments(dept_id)`"
            ),
            "code": (
                "CREATE TABLE Departments (\n"
                "    dept_id INT PRIMARY KEY,\n"
                "    dept_name VARCHAR(50) NOT NULL\n"
                ");\n\n"
                "CREATE TABLE Students (\n"
                "    roll_no INT PRIMARY KEY,\n"
                "    email VARCHAR(100) UNIQUE NOT NULL,\n"
                "    name VARCHAR(50) NOT NULL,\n"
                "    dept_id INT REFERENCES Departments(dept_id) ON DELETE RESTRICT\n"
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
                "a": "A Foreign Key is an attribute in a child table that references the Primary Key of a parent table to maintain referential integrity. When a parent row is deleted, the DBMS enforces one of three actions:\n1. ON DELETE CASCADE: Automatically deletes all child rows referencing the deleted parent.\n2. ON DELETE SET NULL: Sets the foreign key value in child rows to NULL.\n3. ON DELETE RESTRICT / NO ACTION: Rejects the parent deletion if any dependent child rows exist."
            },
            {
                "marks": "10-Mark Question",
                "q": "Given a relation R(A, B, C, D, E) with FDs F = {A -> BC, CD -> E, B -> D, E -> A}. Find all candidate keys.",
                "a": "Step 1: Check closure of single attributes:\n- A+ = {A, B, C, D, E} (A is Candidate Key).\n- E+ = {E, A, B, C, D} (E is Candidate Key).\n- (CD)+ = {C, D, E, A, B} (CD is Candidate Key).\n- (BC)+: Since B->D, (BC)+ = (BCD)+ = {B, C, D, E, A} (BC is Candidate Key).\nConclusion: Candidate keys are {A}, {E}, {CD}, and {BC}."
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
                {"name": "DDL", "desc": "Commands that define and modify database structure (auto-commits)."},
                {"name": "DML / DQL", "desc": "Commands that manipulate data values in existing relations."},
                {"name": "DCL", "desc": "Commands used by DBAs to grant or revoke operational privileges."},
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
            "diagram": "SQL Sub-Languages: DDL (CREATE, ALTER, DROP, TRUNCATE) | DML (INSERT, UPDATE, DELETE) | DQL (SELECT) | DCL (GRANT, REVOKE) | TCL (COMMIT, ROLLBACK)"
        },
        "example": {
            "title": "Schema Definition & Manipulation Walkthrough",
            "scenario": "Creating an employee table, inserting rows, updating salaries, and demonstrating commit:",
            "code": (
                "-- DDL: Define structure\n"
                "CREATE TABLE Employees (\n"
                "    emp_id INT PRIMARY KEY,\n"
                "    name VARCHAR(50) NOT NULL,\n"
                "    salary NUMERIC(10,2) CHECK (salary > 0)\n"
                ");\n\n"
                "-- DML: Insert and Update records\n"
                "INSERT INTO Employees VALUES (101, 'Aditi Rao', 85000.00);\n"
                "UPDATE Employees SET salary = 92000.00 WHERE emp_id = 101;\n"
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
            {"name": "CHAR vs VARCHAR", "formula": "CHAR(n) = Fixed length (padded); VARCHAR(n) = Variable length up to n", "explanation": "Use CHAR for fixed-width codes ('IN', 'US'); use VARCHAR for names and emails."}
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
                "a": "1. DELETE is DML that removes specific rows using a WHERE clause, logs each row deletion, fires triggers, and can be rolled back.\n2. TRUNCATE is DDL that removes all rows by deallocating data pages, resets identity seeds, does not fire triggers, and is much faster.\n3. DROP is DDL that completely destroys both table data and schema definition."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the structure of SQL commands with categories, syntax, constraints, and transaction management.",
                "a": "1. DDL: CREATE TABLE, ALTER TABLE, DROP TABLE, TRUNCATE TABLE.\n2. DML: INSERT INTO, UPDATE SET, DELETE FROM.\n3. DQL: SELECT column FROM table WHERE condition.\n4. DCL: GRANT, REVOKE.\n5. TCL: COMMIT, ROLLBACK, SAVEPOINT.\n6. Integrity Constraints in SQL: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY REFERENCES, CHECK, DEFAULT."
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
            "diagram": "FROM & JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT"
        },
        "example": {
            "title": "Department Salary Aggregation Query",
            "scenario": "Find departments with > 3 employees earning over $40,000, and display avg salary sorted descending:",
            "code": (
                "SELECT department, AVG(salary) AS avg_sal, COUNT(*) AS emp_count\n"
                "FROM Employees\n"
                "WHERE salary > 40000            -- Filter rows BEFORE grouping\n"
                "GROUP BY department             -- Group remaining rows\n"
                "HAVING COUNT(*) > 3             -- Filter groups AFTER grouping\n"
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
                "a": "1. WHERE filters individual rows before grouping takes place. It cannot use aggregate functions.\n2. HAVING filters groups of rows after aggregation has been performed.\nExample:\nSELECT dept_id, AVG(salary)\nFROM Employees\nWHERE status = 'Active'\nGROUP BY dept_id\nHAVING AVG(salary) > 60000;"
            },
            {
                "marks": "10-Mark Question",
                "q": "Detail the logical execution order of an SQL query and write queries for 3 practical analytical scenarios.",
                "a": "1. Execution Order: FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.\n2. Practical Queries:\n(a) Second highest salary: SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);\n(b) Departments where avg salary > company average: SELECT dept_id, AVG(salary) FROM Employees GROUP BY dept_id HAVING AVG(salary) > (SELECT AVG(salary) FROM Employees);\n(c) Students enrolled in > 2 courses: SELECT student_id, COUNT(course_id) FROM Enrollments GROUP BY student_id HAVING COUNT(course_id) > 2;"
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
    },

    "sql-joins": {
        "title": "SQL Joins",
        "subject": "dbms",
        "exam_definition": (
            "An SQL Join is a relational operation used to combine rows from two or more tables "
            "based on a related column between them (typically Primary Key and Foreign Key)."
        ),
        "remember": "INNER = Intersection; LEFT = All Left + Matched Right; FULL = Union of both.",
        "core_concept": (
            "Relations store normalized data across separate tables to prevent redundancy. Joins reassemble "
            "this data during query execution. An INNER JOIN preserves only matching rows. Outer Joins (LEFT, RIGHT, FULL) "
            "preserve unmatched rows from one or both tables, filling missing attributes with NULL. A CROSS JOIN produces "
            "the Cartesian Product of two tables."
        ),
        "key_points": [
            "INNER JOIN: Returns records that have matching values in both tables.",
            "LEFT (OUTER) JOIN: Returns all records from left table, and matched records from right table (NULL if no match).",
            "RIGHT (OUTER) JOIN: Returns all records from right table, and matched records from left table.",
            "FULL (OUTER) JOIN: Returns all records when there is a match in either left or right table.",
            "CROSS JOIN: Returns Cartesian Product (m × n rows); no join condition required.",
            "SELF JOIN: A regular join where a table is joined with itself using table aliases."
        ],
        "classification": {
            "title": "Types of SQL Joins",
            "items": [
                {"name": "Inner Join", "desc": "Strict equality match on both sides."},
                {"name": "Left Outer Join", "desc": "Preserves all left tuples; pads right attributes with NULL."},
                {"name": "Right Outer Join", "desc": "Preserves all right tuples; pads left attributes with NULL."},
                {"name": "Full Outer Join", "desc": "Preserves all tuples from both tables regardless of match."},
                {"name": "Cross Join", "desc": "Unconditional Cartesian combination of all tuples."},
                {"name": "Natural Join", "desc": "Automatically joins on all columns with identical names and types."}
            ]
        },
        "how_it_works": {
            "title": "Join Algorithms & Mechanics in RDBMS",
            "steps": [
                "1. Nested Loop Join: For each row in outer table, scans inner table. Optimal when outer table is small and inner has index.",
                "2. Hash Join: Builds in-memory hash table on join key of smaller table, then probes with larger table.",
                "3. Sort-Merge Join: Sorts both relations on join key, then scans simultaneously. Highly efficient on pre-sorted data."
            ],
            "diagram": "Venn Diagrams: INNER (A ∩ B) | LEFT (All A + A ∩ B) | RIGHT (All B + A ∩ B) | FULL (A ∪ B)"
        },
        "example": {
            "title": "Employee & Department Join Queries",
            "scenario": "Demonstrating LEFT JOIN to preserve unassigned employees, and SELF JOIN for manager hierarchy:",
            "code": (
                "-- LEFT JOIN: Preserves employees without assigned departments\n"
                "SELECT e.emp_id, e.name, d.dept_name\n"
                "FROM Employees e\n"
                "LEFT JOIN Departments d ON e.dept_id = d.dept_id;\n\n"
                "-- SELF JOIN: Employee and Manager hierarchy\n"
                "SELECT e.name AS Employee, m.name AS Manager\n"
                "FROM Employees e\n"
                "LEFT JOIN Employees m ON e.manager_id = m.emp_id;"
            )
        },
        "comparison": {
            "title": "INNER JOIN vs LEFT JOIN vs FULL OUTER JOIN",
            "headers": ["Feature", "INNER JOIN", "LEFT OUTER JOIN", "FULL OUTER JOIN"],
            "rows": [
                ["Unmatched Left Rows", "Discarded", "Preserved (Right cols padded with NULL)", "Preserved (Right cols padded with NULL)"],
                ["Unmatched Right Rows", "Discarded", "Discarded", "Preserved (Left cols padded with NULL)"],
                ["Result Row Count", "≤ min(|A|, |B|)", "≥ |A|", "≥ max(|A|, |B|)"],
                ["Venn Diagram", "Intersection only", "Entire Left Circle", "Both Circles combined"],
                ["Typical Use Case", "Find only active enrollments", "Find all students even if not enrolled", "Reconcile two external financial accounts"]
            ]
        },
        "formulas": [
            {"name": "Cross Join Row Count", "formula": "|A CROSS JOIN B| = |A| × |B|", "explanation": "If Table A has 10 rows and Table B has 5 rows, Cross Join produces 50 rows."},
            {"name": "Inner Join Bounds", "formula": "0 ≤ |A ⨝ B| ≤ |A| × |B|", "explanation": "Inner join produces at most |A|*|B| rows if all join keys match."}
        ],
        "exam_tip": "Remember: In a LEFT JOIN, if an unmatched row from the left table has no corresponding match on the right, all right-table columns in that row evaluate to NULL.",
        "common_confusion": {
            "wrong": "ON clause and WHERE clause behave identically in all joins.",
            "correct": "In an INNER JOIN, filtering in ON vs WHERE produces identical results; but in a LEFT JOIN, conditions in ON filter the right table before joining, while conditions in WHERE filter the final joined result.",
            "explanation": "LEFT JOIN B ON A.id = B.id AND B.status = 'Active' keeps all A rows, but WHERE B.status = 'Active' drops A rows where B is NULL."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is a Self Join and when is it used?",
                "a": "A Self Join is a regular join in which a table is joined with itself using distinct table aliases. It is commonly used to model recursive or hierarchical relationships, such as finding an employee's manager within an Employees table."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the difference between INNER JOIN, LEFT OUTER JOIN, and FULL OUTER JOIN with examples.",
                "a": "1. INNER JOIN returns only records that have matching keys in both tables.\n2. LEFT OUTER JOIN returns all records from the left table; matching records from right table are joined, while unmatched right columns are filled with NULL.\n3. FULL OUTER JOIN returns all records from both tables; missing sides are padded with NULL."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the three primary join algorithms used by DBMS execution engines and analyze their time complexities.",
                "a": "1. Nested Loop Join: For each outer tuple, scans inner relation. Cost: O(|R| × |S|) without index; O(|R| × log|S|) with index.\n2. Hash Join: Builds in-memory hash table on smaller relation, then probes with larger relation. Cost: O(|R| + |S|).\n3. Sort-Merge Join: Sorts both relations on join key, then performs a linear merge pass. Cost: O(|R|log|R| + |S|log|S|)."
            }
        ],
        "revision_60s": [
            "INNER JOIN = Intersection of matching keys.",
            "LEFT JOIN = All left table rows + matched right table rows (NULL if no match).",
            "RIGHT JOIN = All right table rows + matched left table rows.",
            "FULL JOIN = All rows from both tables combined.",
            "CROSS JOIN = Cartesian product (Row Count = |A| * |B|).",
            "Join algorithms: Nested Loop (index friendly), Hash Join (large equijoins), Sort-Merge (pre-sorted data)."
        ]
    },

    "nested-queries": {
        "title": "Nested Queries",
        "subject": "dbms",
        "exam_definition": (
            "A Nested Query (Subquery) is a SQL query enclosed within parentheses and embedded inside "
            "another SQL statement (SELECT, INSERT, UPDATE, or DELETE) to compute intermediate result sets."
        ),
        "remember": "Correlated Subquery = Inner query references outer query row-by-row. Non-Correlated = Evaluates once.",
        "core_concept": (
            "Subqueries allow breaking complex multi-step analytical questions into modular nested logic. "
            "Non-correlated subqueries execute once independently, and their result is used by the outer query. "
            "Correlated subqueries reference columns from the outer query, meaning the inner query must be re-evaluated "
            "for every candidate row of the outer query. EXISTS tests for existence of rows and stops searching as soon "
            "as the first match is found."
        ),
        "key_points": [
            "Single-Row Subquery: Returns exactly one row and one column; used with =, <, >, <=, >= operators.",
            "Multi-Row Subquery: Returns multiple rows; used with IN, NOT IN, ANY/SOME, ALL operators.",
            "Correlated Subquery: References outer query column; executes once per outer row.",
            "Non-Correlated Subquery: Self-contained; executes once for the entire query.",
            "EXISTS / NOT EXISTS: Evaluates to TRUE/FALSE; short-circuits on first match.",
            "Subquery in FROM Clause: Known as an inline view or derived table; must be given a table alias."
        ],
        "classification": {
            "title": "Subquery Operators in SQL",
            "items": [
                {"name": "IN / NOT IN", "desc": "Tests whether a value matches any member of the subquery result set."},
                {"name": "EXISTS / NOT EXISTS", "desc": "Boolean test checking if subquery returns at least one row."},
                {"name": "ANY / SOME", "desc": "True if condition holds for AT LEAST ONE value in subquery result."},
                {"name": "ALL", "desc": "True only if condition holds for ALL values in subquery result."}
            ]
        },
        "how_it_works": {
            "title": "Correlated vs Non-Correlated Subquery Execution",
            "steps": [
                "Non-Correlated: DBMS executes inner query once → caches result set in temporary buffer → evaluates outer query against cached result.",
                "Correlated: Outer query fetches row 1 → binds outer values into inner query → inner query executes and returns result → outer query tests condition → repeats for all outer rows."
            ],
            "diagram": "Non-Correlated: Inner Query (Once) → Outer Query | Correlated: Outer Row i ⇄ Inner Query (N times)"
        },
        "example": {
            "title": "Employees Earning Above Department Average",
            "scenario": "Find employees who earn more than the average salary of their respective department using correlated subquery:",
            "code": (
                "-- Correlated Subquery: inner query references outer table 'e1'\n"
                "SELECT e1.name, e1.department, e1.salary\n"
                "FROM Employees e1\n"
                "WHERE e1.salary > (\n"
                "    SELECT AVG(e2.salary)\n"
                "    FROM Employees e2\n"
                "    WHERE e2.department = e1.department\n"
                ");"
            )
        },
        "comparison": {
            "title": "Correlated Subquery vs Non-Correlated Subquery",
            "headers": ["Feature", "Non-Correlated Subquery", "Correlated Subquery"],
            "rows": [
                ["Dependency", "Independent of outer query", "Dependent on outer query (references outer column)"],
                ["Execution Count", "Executes exactly ONCE", "Executes N times (once for every outer row)"],
                ["Standalone Run", "Can be executed separately by itself", "Cannot be executed standalone (missing outer column)"],
                ["Performance", "Fast — result set can be cached", "Slower — O(N × M) without query optimizer unnesting"],
                ["Example Operator", "WHERE salary > (SELECT AVG(sal) FROM Emp)", "WHERE salary > (SELECT AVG(sal) FROM Emp e2 WHERE e2.dept = e1.dept)"]
            ]
        },
        "formulas": [
            {"name": "> ANY / SOME Operator", "formula": "x > ANY (S) ≡ x > MIN(S)", "explanation": "x is greater than at least one element in S if it is greater than the minimum element."},
            {"name": "> ALL Operator", "formula": "x > ALL (S) ≡ x > MAX(S)", "explanation": "x is greater than every element in S if it is greater than the maximum element."}
        ],
        "exam_tip": "Remember: `x > ANY (subquery)` is logically equivalent to `x > MIN(subquery)`, and `x > ALL (subquery)` is logically equivalent to `x > MAX(subquery)`.",
        "common_confusion": {
            "wrong": "NOT IN and NOT EXISTS behave identically when NULL values are present in the subquery.",
            "correct": "If a subquery returns even a single NULL value, `NOT IN` evaluates to UNKNOWN for all outer rows, returning ZERO results! In contrast, `NOT EXISTS` handles NULLs safely.",
            "explanation": "Exam trap: WHERE id NOT IN (SELECT id FROM T) returns empty if T contains any row where id IS NULL."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is a Correlated Subquery?",
                "a": "A correlated subquery is a nested subquery that references one or more columns from the outer query. Because of this dependency, it cannot be evaluated independently and must be executed repeatedly for each row processed by the outer query."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the difference between EXISTS and IN operators in SQL subqueries.",
                "a": "1. IN evaluates the subquery, returns a list of values, and checks whether the outer value matches any element. It fails if NULLs exist in a NOT IN query.\n2. EXISTS tests for the existence of rows in the subquery. It returns TRUE as soon as the first matching row is found (short-circuit evaluation) and safely ignores NULLs."
            },
            {
                "marks": "10-Mark Question",
                "q": "Write SQL queries for: (a) 2nd highest salary using subquery, (b) Employees earning above their department average, (c) Customers with no orders using NOT EXISTS.",
                "a": "(a) Second Highest Salary:\nSELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);\n(b) Employees earning above department average:\nSELECT e1.name, e1.salary FROM Employees e1 WHERE e1.salary > (SELECT AVG(e2.salary) FROM Employees e2 WHERE e2.dept_id = e1.dept_id);\n(c) Customers with no orders:\nSELECT c.customer_id, c.name FROM Customers c WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.customer_id);"
            }
        ],
        "revision_60s": [
            "Single-row subqueries use =, <, >; multi-row subqueries use IN, ANY, ALL.",
            "Non-correlated subqueries execute once; correlated subqueries execute once per outer row.",
            "EXISTS short-circuits on first match and returns boolean TRUE/FALSE.",
            "> ANY is equivalent to > MIN; > ALL is equivalent to > MAX.",
            "NOT IN fails and returns 0 rows if subquery returns NULL! Use NOT EXISTS instead."
        ]
    },

    "normalization": {
        "title": "Normalization",
        "subject": "dbms",
        "exam_definition": (
            "Database Normalization is a systematic technique of organizing relational database schemas "
            "using Functional Dependencies to eliminate data redundancy, prevent insertion/update/deletion anomalies, "
            "and ensure lossless join decomposition with dependency preservation."
        ),
        "remember": "1NF: Atomic values; 2NF: No partial dependency; 3NF: No transitive dependency; BCNF: Every determinant is superkey.",
        "core_concept": (
            "Unnormalized database designs create severe anomalies: Insertion Anomaly (cannot insert a course without a student), "
            "Deletion Anomaly (deleting a student accidentally deletes the course), and Update Anomaly (updating department office requires "
            "modifying thousands of rows). Normalization systematically decomposes tables into smaller, well-structured relations "
            "until higher normal forms (1NF, 2NF, 3NF, BCNF) are achieved."
        ),
        "key_points": [
            "Functional Dependency (X → Y): Attribute X uniquely determines attribute Y.",
            "Prime Attribute: An attribute that is part of ANY candidate key. Non-Prime: An attribute not in any candidate key.",
            "1NF (First Normal Form): All attribute values must be atomic; no repeating groups or multi-valued attributes.",
            "2NF (Second Normal Form): In 1NF and NO Partial Dependency (no non-prime attribute depends on a proper subset of a candidate key).",
            "3NF (Third Normal Form): In 2NF and NO Transitive Dependency. For every X → Y, either X is a Superkey OR Y is a Prime Attribute.",
            "BCNF (Boyce-Codd Normal Form): Stricter version of 3NF. For every non-trivial FD X → Y, X MUST be a Superkey.",
            "Lossless Decomposition: R decomposed into R1, R2 is lossless if and only if (R1 ∩ R2) → R1 OR (R1 ∩ R2) → R2."
        ],
        "classification": {
            "title": "The Hierarchy of Normal Forms",
            "items": [
                {"name": "1NF", "desc": "Domain of attributes must include only atomic (indivisible) values. No multi-valued sets."},
                {"name": "2NF", "desc": "1NF + Full Functional Dependency. Eliminates partial dependency on composite candidate keys."},
                {"name": "3NF", "desc": "2NF + Eliminates transitive dependencies (Non-key → Non-key). Allows X is Superkey OR Y is Prime."},
                {"name": "BCNF", "desc": "3NF + Eliminates all anomalies from overlapping candidate keys. For every X → Y, X must be a Superkey."}
            ]
        },
        "how_it_works": {
            "title": "Testing Normal Forms Step-by-Step",
            "steps": [
                "1. Find all Candidate Keys of relation R using attribute closures.",
                "2. Identify Prime Attributes (attributes in any candidate key) and Non-Prime Attributes.",
                "3. Check 2NF: If any FD has Proper Subset of Candidate Key → Non-Prime Attribute, relation violates 2NF.",
                "4. Check 3NF: For every FD X → Y, verify if X is a Superkey OR Y is a Prime Attribute. If neither, violates 3NF.",
                "5. Check BCNF: For every FD X → Y, verify if X is a Superkey. If any determinant X is not a superkey, violates BCNF.",
                "6. Decompose violating relation into lossless sub-relations preserving dependencies where possible."
            ],
            "diagram": "1NF (Atomic) ⊇ 2NF (No Partial Dep) ⊇ 3NF (No Transitive Dep) ⊇ BCNF (Determinant is Superkey)"
        },
        "example": {
            "title": "Normalization from Unnormalized to BCNF",
            "scenario": (
                "Given relation `Student_Course(roll_no, course_code, student_name, course_name, instructor, inst_office)`:\n"
                "- Candidate Key: {roll_no, course_code}\n"
                "- FDs:\n"
                "  1. roll_no → student_name (Partial dependency: roll_no is subset of composite key! Violates 2NF)\n"
                "  2. course_code → course_name, instructor (Partial dependency: Violates 2NF)\n"
                "  3. instructor → inst_office (Transitive dependency: non-key determines non-key! Violates 3NF)\n\n"
                "Decomposition into 3NF/BCNF:\n"
                "1. Students(roll_no PK, student_name)\n"
                "2. Courses(course_code PK, course_name, instructor)\n"
                "3. Instructors(instructor PK, inst_office)\n"
                "4. Enrollments(roll_no FK, course_code FK, PRIMARY KEY(roll_no, course_code))"
            ),
            "code": (
                "-- Fully normalized BCNF schema\n"
                "CREATE TABLE Instructors (\n"
                "    instructor VARCHAR(50) PRIMARY KEY,\n"
                "    inst_office VARCHAR(20)\n"
                ");\n\n"
                "CREATE TABLE Courses (\n"
                "    course_code VARCHAR(10) PRIMARY KEY,\n"
                "    course_name VARCHAR(100),\n"
                "    instructor VARCHAR(50) REFERENCES Instructors(instructor)\n"
                ");\n\n"
                "CREATE TABLE Enrollments (\n"
                "    roll_no INT REFERENCES Students(roll_no),\n"
                "    course_code VARCHAR(10) REFERENCES Courses(course_code),\n"
                "    PRIMARY KEY (roll_no, course_code)\n"
                ");"
            )
        },
        "comparison": {
            "title": "3NF vs BCNF",
            "headers": ["Feature", "Third Normal Form (3NF)", "Boyce-Codd Normal Form (BCNF)"],
            "rows": [
                ["Condition on X → Y", "X is a Superkey OR Y is a Prime Attribute", "X MUST be a Superkey (no exceptions)"],
                ["Redundancy", "Slight redundancy possible when overlapping CKs exist", "Zero redundancy from functional dependencies"],
                ["Dependency Preservation", "Always guaranteed to preserve all functional dependencies", "NOT always possible to preserve dependencies"],
                ["Lossless Join", "Always guaranteed", "Always guaranteed"],
                ["Strictness", "Less strict than BCNF", "Stricter form of 3NF (every BCNF relation is in 3NF)"]
            ]
        },
        "formulas": [
            {"name": "Lossless Join Decomposition Condition", "formula": "(R1 ∩ R2) → R1  OR  (R1 ∩ R2) → R2", "explanation": "The common attributes between decomposed relations must form a Superkey of at least one relation."},
            {"name": "Dependency Preservation Condition", "formula": "(F1 ∪ F2)+ = F+", "explanation": "The closure of functional dependencies in sub-relations must cover all original dependencies."}
        ],
        "exam_tip": "Remember: 3NF allows X → Y if Y is a PRIME attribute (even if X is not a superkey). BCNF does NOT allow this — in BCNF, X must ALWAYS be a superkey without exception!",
        "common_confusion": {
            "wrong": "Any relation can always be decomposed into BCNF while preserving all functional dependencies.",
            "correct": "Lossless join decomposition is always possible in BCNF, but dependency preservation is NOT always possible in BCNF. If dependency preservation is mandatory, 3NF is preferred.",
            "explanation": "Classical GATE question: Relation with overlapping candidate keys (e.g. AB->C, C->B) can achieve BCNF only by dropping AB->C dependency."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is a Partial Dependency and which Normal Form eliminates it?",
                "a": "A Partial Dependency occurs when a non-prime attribute is functionally dependent on a proper subset of a composite candidate key (rather than the full key). Second Normal Form (2NF) eliminates partial dependencies."
            },
            {
                "marks": "5-Mark Question",
                "q": "Differentiate between 3NF and BCNF with a counterexample.",
                "a": "In 3NF, for every functional dependency X → Y, either X is a Superkey OR Y is a Prime Attribute. In BCNF, X must be a Superkey, with no exception for prime attributes.\nExample: R(A, B, C) with FDs {AB → C, C → B}. Candidate keys are AB and AC. For C → B, C is not a superkey, but B is a prime attribute (part of candidate key AB). Therefore, R is in 3NF, but NOT in BCNF because determinant C is not a superkey."
            },
            {
                "marks": "10-Mark Question",
                "q": "Define 1NF, 2NF, 3NF, and BCNF. Given R(A, B, C, D, E) with F = {A -> B, BC -> D, E -> C}. Determine the highest normal form.",
                "a": "1. Definitions: 1NF requires atomic values; 2NF eliminates partial dependencies; 3NF eliminates transitive dependencies; BCNF requires every determinant to be a superkey.\n2. Candidate Key: Attributes not on RHS: A, E. Closure of (AE): AE+ = {A, E, B, C, D}. Candidate Key = {AE}.\n- Prime attributes: {A, E}; Non-prime: {B, C, D}.\n3. Testing: Check A -> B: A is a proper subset of candidate key {AE}, and B is non-prime. This is a Partial Dependency!\nConclusion: Violates 2NF, so highest normal form is 1NF."
            }
        ],
        "revision_60s": [
            "Normalization eliminates insertion, update, and deletion anomalies.",
            "1NF: Atomic values only (no lists or composite attributes).",
            "2NF: In 1NF + No partial dependency (subset of CK → non-prime).",
            "3NF: In 2NF + No transitive dependency (X is Superkey OR Y is Prime).",
            "BCNF: For every non-trivial X → Y, X must be a Superkey.",
            "Lossless decomposition: Common attributes must form a superkey of R1 or R2.",
            "3NF always guarantees dependency preservation; BCNF may not."
        ]
    },

    "transactions": {
        "title": "Transactions",
        "subject": "dbms",
        "exam_definition": (
            "A Transaction in a DBMS is a logical unit of database processing that includes one or more database "
            "access operations (reads and writes) that must be executed atomically to transition the database from "
            "one consistent state to another consistent state."
        ),
        "remember": "ACID: Atomicity (All or None), Consistency (Rules valid), Isolation (Independent), Durability (Persistent).",
        "core_concept": (
            "Transactions protect databases against system crashes and concurrent interference. If a bank transfer "
            "debits Account A and credits Account B, the two steps cannot be partially executed. ACID properties "
            "guarantee that either all operations succeed or all are rolled back. Schedules determine the execution order "
            "of multiple concurrent transactions, and Conflict Serializability guarantees that concurrent execution is "
            "equivalent to some serial schedule."
        ),
        "key_points": [
            "Atomicity: 'All or Nothing' execution managed by Recovery Manager using Undo Logs.",
            "Consistency: Preserves database invariants and integrity constraints.",
            "Isolation: Concurrent transactions execute without seeing each other's uncommitted intermediate states.",
            "Durability: Committed updates survive subsequent power outages and system crashes (WAL).",
            "Transaction States: Active → Partially Committed → Committed; or Active/Partially Committed → Failed → Aborted.",
            "Conflict Serializability: A schedule is conflict serializable if its precedence graph has NO cycles."
        ],
        "classification": {
            "title": "Transaction States & Lifecycle",
            "items": [
                {"name": "Active", "desc": "Initial state; transaction is actively executing read and write operations."},
                {"name": "Partially Committed", "desc": "Final statement executed, but updates are in volatile RAM buffer, not yet flushed to disk."},
                {"name": "Committed", "desc": "Transaction successfully completed; changes permanently recorded in Write-Ahead Log (WAL)."},
                {"name": "Failed", "desc": "Discovery that normal execution cannot proceed (system crash or abort)."},
                {"name": "Aborted", "desc": "Transaction rolled back; database restored to state prior to transaction start."}
            ]
        },
        "how_it_works": {
            "title": "Precedence Graph Conflict Serializability Algorithm",
            "steps": [
                "1. For each transaction Ti in schedule S, create a node labeled Ti.",
                "2. Identify all conflicting operations on the same data item Q (Read-Write, Write-Read, Write-Write).",
                "3. If Ti's conflicting operation occurs before Tj's operation in the schedule, draw a directed edge Ti → Tj.",
                "4. Check for cycles: If the Precedence Graph has NO CYCLES, schedule S is Conflict Serializable.",
                "5. If serializable, topological sort of the graph yields the equivalent serial schedule (e.g. T1 → T2 → T3)."
            ],
            "diagram": "State Flow: Active → Partially Committed → Committed | Active → Failed → Aborted"
        },
        "example": {
            "title": "Bank Fund Transfer Transaction",
            "scenario": (
                "Transfer $500 from Account A ($1000) to Account B ($2000):\n"
                "T1: Read(A); A = A - 500; Write(A); Read(B); B = B + 500; Write(B); Commit;\n"
                "If system crashes after Write(A) but before Write(B), Atomicity rolls back A to $1000 using Undo logs."
            ),
            "code": (
                "BEGIN TRANSACTION;\n"
                "    UPDATE Accounts SET balance = balance - 500 WHERE account_id = 'A';\n"
                "    UPDATE Accounts SET balance = balance + 500 WHERE account_id = 'B';\n"
                "    COMMIT;"
            )
        },
        "comparison": {
            "title": "Conflict Serializability vs View Serializability",
            "headers": ["Feature", "Conflict Serializability", "View Serializability"],
            "rows": [
                ["Condition", "Conflict equivalent to a serial schedule by swapping non-conflicting ops", "View equivalent to a serial schedule (initial reads, updated writes, final writes match)"],
                ["Complexity", "Polynomial time O(V + E) using Precedence Graph cycle detection", "NP-Complete problem"],
                ["Blind Writes", "Does not handle blind writes flexibly", "Can recognize serializability even in the presence of blind writes"],
                ["Relationship", "Every Conflict Serializable schedule is View Serializable", "View Serializable is a superset (not all view serializable schedules are conflict serializable)"]
            ]
        },
        "formulas": [
            {"name": "Conflict Operations Condition", "formula": "I_i(Q) and I_j(Q) conflict ⟺ i ≠ j AND (at least one operation is Write(Q))", "explanation": "Two operations conflict if they belong to different transactions, access the same item, and at least one is a Write."},
            {"name": "Cycle Detection Rule", "formula": "No Cycles in Precedence Graph ⟺ Schedule is Conflict Serializable", "explanation": "A directed cycle indicates mutually incompatible temporal dependencies."}
        ],
        "exam_tip": "Remember: Two operations conflict if and only if: (1) They belong to DIFFERENT transactions, (2) They access the SAME data item, and (3) AT LEAST ONE of them is a WRITE operation. Read-Read NEVER conflicts!",
        "common_confusion": {
            "wrong": "Read-Read operations cause conflicts in concurrent schedules.",
            "correct": "Two concurrent Read operations on the same data item NEVER conflict because neither modifies data; order of reads does not affect outcome.",
            "explanation": "Only Read-Write, Write-Read, and Write-Write operations produce conflicting pairs."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Define the ACID properties of a database transaction.",
                "a": "ACID stands for: (1) Atomicity (All-or-Nothing execution via undo logs), (2) Consistency (Preserves database integrity rules), (3) Isolation (Transactions execute independently without seeing intermediate states), (4) Durability (Committed updates survive subsequent crashes via WAL)."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the Precedence Graph method for testing Conflict Serializability.",
                "a": "1. Construct directed graph G = (V, E) where nodes represent transactions Ti.\n2. Add directed edge Ti → Tj if Ti executes an operation that conflicts with a subsequent operation in Tj on the same data item (RW, WR, WW).\n3. If the graph contains NO cycles, the schedule is Conflict Serializable. A topological sort gives the equivalent serial schedule. If a cycle exists, the schedule is non-serializable."
            },
            {
                "marks": "10-Mark Question",
                "q": "Test whether the schedule S: r1(X), r2(Y), w1(X), r1(Y), w2(Y), w1(Y) is conflict serializable.",
                "a": "Conflicting pairs in S on item Y:\n- r2(Y) before w1(Y): T2 reads Y before T1 writes Y → Edge T2 → T1.\n- r1(Y) before w2(Y): T1 reads Y before T2 writes Y → Edge T1 → T2.\nCycle Analysis:\nWe have edge T2 → T1 and edge T1 → T2, forming a DIRECTED CYCLE: T1 ⇆ T2.\nConclusion: Because the precedence graph contains a cycle between T1 and T2, schedule S is NOT Conflict Serializable."
            }
        ],
        "revision_60s": [
            "ACID: Atomicity (Undo log), Consistency (Rules), Isolation (Locks/2PL), Durability (Redo log).",
            "Active → Partially Committed (in RAM) → Committed (flushed to WAL).",
            "Failed → Aborted (Rolled back to original state).",
            "Conflicting operations: Same item, different transactions, at least one WRITE.",
            "Precedence graph has no cycles ⟺ Conflict Serializable.",
            "Every Conflict Serializable schedule is View Serializable, but not vice-versa."
        ]
    },

    "concurrency-control": {
        "title": "Concurrency Control",
        "subject": "dbms",
        "exam_definition": (
            "Concurrency Control is the management of simultaneous transaction execution in a multi-user DBMS "
            "to prevent concurrency anomalies (dirty reads, lost updates, unrepeatable reads, phantoms) "
            "and guarantee serializability through locking protocols, timestamp ordering, or multiversioning."
        ),
        "remember": "2PL guarantees Conflict Serializability, but may suffer from Deadlocks.",
        "core_concept": (
            "Uncontrolled interleaving of concurrent transactions causes serious data anomalies: Lost Updates "
            "(two writers overwrite each other), Dirty Reads (reading uncommitted data that gets rolled back), and "
            "Non-repeatable Reads. Concurrency protocols resolve this. Two-Phase Locking (2PL) enforces a Growing Phase "
            "(locks acquired) and a Shrinking Phase (locks released). Timestamp Ordering uses transaction start times "
            "to enforce serializability without locks."
        ),
        "key_points": [
            "Concurrency Anomalies: Lost Update (W-W), Dirty Read (W-R), Non-Repeatable Read (R-W), Phantom Read.",
            "Lock Types: Shared Lock (S-Lock / Read Lock) and Exclusive Lock (X-Lock / Write Lock).",
            "Two-Phase Locking (2PL): Growing Phase (acquire locks) → Shrinking Phase (release locks). Guarantees serializability.",
            "Strict 2PL: Releases Exclusive locks only AFTER transaction commits or aborts (prevents Cascading Rollback).",
            "Rigorous 2PL: Releases ALL locks only after commit/abort.",
            "Deadlock: A state where two or more transactions wait indefinitely for locks held by each other.",
            "Deadlock Handling: Prevention (Wait-Die, Wound-Wait) and Detection (Wait-For Graph cycles)."
        ],
        "classification": {
            "title": "Concurrency Control Protocols",
            "items": [
                {"name": "Lock-Based Protocols", "desc": "Uses S/X locks with 2PL, Strict 2PL, or Rigorous 2PL to prevent conflicting access."},
                {"name": "Timestamp-Based Protocols", "desc": "Assigns unique timestamp TS(T) at start; ensures serial order matches timestamp order."},
                {"name": "Validation / Optimistic Protocols", "desc": "Transactions execute without locking in local memory; validated before commit."},
                {"name": "Multiversion Concurrency Control (MVCC)", "desc": "Maintains multiple versions of rows so readers never block writers."}
            ]
        },
        "how_it_works": {
            "title": "Deadlock Prevention Schemes (Wait-Die vs Wound-Wait)",
            "steps": [
                "Assume older transaction T_old has smaller timestamp TS(T_old) < TS(T_young).",
                "Wait-Die Scheme (Non-preemptive):\n  - If T_old requests resource held by T_young → T_old is allowed to WAIT.\n  - If T_young requests resource held by T_old → T_young DIES (aborts and restarts).",
                "Wound-Wait Scheme (Preemptive):\n  - If T_old requests resource held by T_young → T_old WOUNDS T_young (preempts and aborts T_young).\n  - If T_young requests resource held by T_old → T_young is allowed to WAIT."
            ],
            "diagram": "2PL: Growing Phase (Acquire Only) → Lock Point → Shrinking Phase (Release Only)"
        },
        "example": {
            "title": "Dirty Read & Strict 2PL Resolution",
            "scenario": (
                "T1 writes balance = $500. T2 reads balance = $500 and issues loan. T1 aborts and rolls back to $100 (Dirty Read).\n"
                "Under Strict 2PL, T1 holds Exclusive Lock on balance until commit/abort. T2 is blocked until T1 completes."
            ),
            "code": (
                "-- Strict 2PL Lock Flow\n"
                "LOCK-X (Account_A);\n"
                "Write(Account_A);\n"
                "-- T2 requests LOCK-S (Account_A) -> BLOCKED by Lock Manager\n"
                "COMMIT; -- T1 commits, and only now releases LOCK-X"
            )
        },
        "comparison": {
            "title": "Wait-Die vs Wound-Wait Deadlock Prevention",
            "headers": ["Scenario", "Wait-Die (Non-preemptive)", "Wound-Wait (Preemptive)"],
            "rows": [
                ["Older requests younger", "Older WAITS for younger", "Older WOUNDS (aborts/preempts) younger"],
                ["Younger requests older", "Younger DIES (aborts and restarts)", "Younger WAITS for older"],
                ["Starvation", "Possible if transaction repeatedly dies", "No starvation — older transactions naturally take priority"],
                ["Number of Aborts", "Generally higher aborts", "Fewer aborts as older transactions preempt quickly"]
            ]
        },
        "formulas": [
            {"name": "Strict 2PL Invariant", "formula": "Exclusive Locks held until COMMIT / ABORT", "explanation": "Guarantees strict schedule and prevents cascading rollbacks."},
            {"name": "Wait-For Graph Cycle Condition", "formula": "Directed Cycle in WFG ⟺ Deadlock Exists", "explanation": "Transactions in cycle are mutually blocked waiting for locks."}
        ],
        "exam_tip": "Remember: 2PL guarantees Conflict Serializability, but it does NOT prevent Deadlocks! Strict 2PL prevents Cascading Rollbacks by holding Exclusive locks until commit.",
        "common_confusion": {
            "wrong": "Two-Phase Locking (2PL) prevents deadlocks from occurring.",
            "correct": "2PL guarantees serializability, but deadlocks CAN STILL OCCUR under 2PL. Deadlock prevention/detection mechanisms (Wait-For Graph, Wait-Die) are needed separately.",
            "explanation": "If T1 holds Lock(A) and requests Lock(B), while T2 holds Lock(B) and requests Lock(A), both follow 2PL rules but deadlock."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the Dirty Read problem in database concurrency?",
                "a": "A Dirty Read occurs when transaction T2 reads a data item that has been updated by an uncommitted transaction T1. If T1 subsequently fails and rolls back, the data read by T2 never existed in the database, leading to an inconsistent state."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Two-Phase Locking (2PL) and differentiate between Basic 2PL, Strict 2PL, and Rigorous 2PL.",
                "a": "2PL divides locking into: (1) Growing Phase (acquire locks only) and (2) Shrinking Phase (release locks only).\n1. Basic 2PL: Locks released at any time during shrinking phase. Prone to cascading aborts.\n2. Strict 2PL: Exclusive (X) locks held until commit/abort. Prevents cascading aborts.\n3. Rigorous 2PL: All locks (S and X) held until commit/abort."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain Deadlock detection using Wait-For Graphs and detail the Wait-Die and Wound-Wait deadlock prevention algorithms.",
                "a": "1. Wait-For Graph (WFG): Directed graph where nodes represent active transactions. An edge Ti → Tj indicates Ti is waiting for a lock held by Tj. A cycle in WFG indicates Deadlock. Victim is selected and aborted.\n2. Wait-Die (Non-preemptive): Older waits for younger; younger dies when requesting older.\n3. Wound-Wait (Preemptive): Older wounds (preempts/aborts) younger; younger waits for older."
            }
        ],
        "revision_60s": [
            "Concurrency anomalies: Lost Update, Dirty Read, Unrepeatable Read, Phantom Read.",
            "Shared Lock (S) = Read only; Exclusive Lock (X) = Read & Write.",
            "2PL has Growing Phase (acquire only) and Shrinking Phase (release only).",
            "2PL guarantees serializability, but DOES NOT prevent deadlocks.",
            "Strict 2PL holds X-locks until commit to prevent cascading rollbacks.",
            "Wait-Die: Older waits, younger dies. Wound-Wait: Older wounds, younger waits."
        ]
    },

    "indexing-and-recovery": {
        "title": "Indexing and Recovery",
        "subject": "dbms",
        "exam_definition": (
            "Indexing is a data structure technique (primarily B-Trees and B+ Trees) used to optimize query search latency "
            "from linear scan O(N) to logarithmic time O(log N). Crash Recovery is the automated mechanism using Write-Ahead Logging (WAL) "
            "and Checkpointing to restore database consistency after system crashes."
        ),
        "remember": "B+ Tree stores actual data pointers ONLY in leaf nodes (linked for fast range queries); internal nodes store only search keys.",
        "core_concept": (
            "Scanning every disk block in a large table is cost prohibitive. An index provides an auxiliary search structure "
            "ordered by key. B+ Trees are the universal indexing standard in databases because all leaf nodes are at the exact same depth "
            "and are doubly linked for sequential range scans. For fault tolerance, Write-Ahead Logging (WAL) mandates that log records "
            "must hit persistent disk before dirty data pages are flushed, enabling ARIES recovery (Analysis, Redo, Undo)."
        ),
        "key_points": [
            "Primary Index: Defined on an ordered data file sorted on the Primary Key (Sparse).",
            "Clustering Index: Defined on an ordered data file sorted on a non-key ordering attribute.",
            "Secondary Index: Defined on an unordered file; dense index created on candidate keys or non-key columns.",
            "Dense Index: Contains an index entry for EVERY search key value in the data file.",
            "Sparse Index: Contains index entries for only some search values (typically one per data block).",
            "B+ Tree Properties: Balanced tree; leaf nodes store all data pointers and are linked; internal nodes store routing keys.",
            "Write-Ahead Logging (WAL): Log records must be written to disk BEFORE corresponding dirty page is flushed.",
            "Checkpointing: Periodically flushes all dirty pages to disk and writes checkpoint record to truncate log replay time."
        ],
        "classification": {
            "title": "Types of Database Indexes",
            "items": [
                {"name": "Primary Index", "desc": "Sparse index on ordered primary key file."},
                {"name": "Clustering Index", "desc": "Index on ordered non-key column; points to first block of each cluster."},
                {"name": "Secondary Index", "desc": "Dense index on unordered columns; points to record pointers or bucket blocks."},
                {"name": "B-Tree Index", "desc": "Self-balancing tree storing search keys and data record pointers in both internal and leaf nodes."},
                {"name": "B+ Tree Index", "desc": "Stores data pointers exclusively in leaves; leaves linked sequentially for fast range scans."}
            ]
        },
        "how_it_works": {
            "title": "ARIES Crash Recovery Protocol (3 Phases)",
            "steps": [
                "1. Analysis Phase: Scans log forward from last checkpoint to identify active uncommitted transactions and dirty buffer pages.",
                "2. Redo Phase: Scans forward from oldest unwritten page LSN; reapplies all logged updates to restore pre-crash state ('repeats history').",
                "3. Undo Phase: Scans backward from log end; rolls back all updates made by active transactions that never committed before crash."
            ],
            "diagram": "B+ Tree: Root → Internal Routing Keys → Leaf Nodes (Data pointers + Doubly Linked List)"
        },
        "example": {
            "title": "B+ Tree Search vs Range Scan",
            "scenario": (
                "Query: SELECT * FROM Employees WHERE salary BETWEEN 50000 AND 80000;\n"
                "1. Traverse B+ Tree from root to leaf node matching salary = 50000 in O(log_m N) block I/O reads.\n"
                "2. Follow the leaf node doubly-linked list sequentially until salary > 80000."
            ),
            "code": (
                "CREATE TABLE Employees (\n"
                "    emp_id INT PRIMARY KEY,               -- Primary B+ Tree Index\n"
                "    email VARCHAR(100) UNIQUE,            -- Unique Secondary B+ Tree Index\n"
                "    salary NUMERIC(10,2)\n"
                ");\n"
                "CREATE INDEX idx_emp_salary ON Employees(salary);"
            )
        },
        "comparison": {
            "title": "B-Tree vs B+ Tree",
            "headers": ["Feature", "B-Tree", "B+ Tree"],
            "rows": [
                ["Data Pointer Location", "Stored in both internal nodes and leaf nodes", "Stored ONLY in leaf nodes"],
                ["Internal Node Capacity", "Lower (stores keys + record pointers)", "Higher (stores search keys and node pointers only)"],
                ["Tree Height (Fan-out)", "Taller (lower fan-out)", "Shorter (higher fan-out, fewer disk I/O reads)"],
                ["Range Queries", "Slow — requires in-order tree traversal across branches", "Extremely Fast — sequential scan along linked leaf nodes"],
                ["Search Time", "Variable (faster if key found in root/internal node)", "Uniform O(log_m N) — every search traverses to a leaf node"]
            ]
        },
        "formulas": [
            {"name": "B+ Tree Node Capacity (Order m)", "formula": "Max Keys = m - 1; Max Pointers = m; Min Keys = ⌈m/2⌉ - 1", "explanation": "Every node (except root) must remain at least half full."},
            {"name": "Search I/O Complexity", "formula": "I/O Reads = O(log_m N)", "explanation": "Where m is fan-out (typically 100–500) and N is total indexed tuples."}
        ],
        "exam_tip": "Remember: In a B+ Tree, data pointers are stored EXCLUSIVELY in the leaf nodes, and all leaf nodes are connected via a linked list. This makes range queries significantly faster in B+ Trees than in B-Trees!",
        "common_confusion": {
            "wrong": "A Dense Index has fewer entries than a Sparse Index.",
            "correct": "A Dense Index has an entry for EVERY search key in the database file, whereas a Sparse Index has entries for only some keys (usually one per physical disk block).",
            "explanation": "Dense index is larger but faster; Sparse index is compact and requires ordered data."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Why are B+ Trees preferred over B-Trees for database indexing?",
                "a": "B+ Trees store data pointers only in leaf nodes, allowing internal nodes to hold more routing keys (higher fan-out) and resulting in a shorter tree with fewer disk I/O operations. Furthermore, all leaf nodes in a B+ Tree are doubly linked, enabling extremely fast sequential range queries."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the Write-Ahead Logging (WAL) protocol and its role in crash recovery.",
                "a": "The Write-Ahead Logging (WAL) protocol mandates that any update made to a database page in buffer memory must have its corresponding log record written and flushed to non-volatile disk BEFORE the dirty page itself is allowed to be written to disk.\nThis ensures that if a crash occurs mid-execution, Redo logs can reapply committed changes, and Undo logs can reverse uncommitted modifications."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the ARIES recovery algorithm detailing the Analysis, Redo, and Undo phases.",
                "a": "ARIES recovery executes in three sequential phases:\n1. Analysis Phase: Scans log forward from most recent checkpoint to determine active transactions and dirty pages at crash time.\n2. Redo Phase: Scans forward from oldest unwritten page LSN, reapplying all logged updates ('repeats history').\n3. Undo Phase: Scans backward from crash point, rolling back all operations performed by active transactions that never committed before the crash and writing Compensation Log Records (CLRs)."
            }
        ],
        "revision_60s": [
            "Primary Index: On ordered primary key file (Sparse).",
            "Clustering Index: On ordered non-key column.",
            "Secondary Index: On unordered columns (Dense).",
            "B+ Tree stores data pointers ONLY in leaf nodes; leaves are linked for range scans.",
            "B+ Tree has higher fan-out and shorter depth than B-Tree.",
            "WAL: Log record must hit disk BEFORE dirty data page is written.",
            "ARIES recovery has 3 phases: Analysis (inspects crash state), Redo (repeats history), Undo (rolls back losers)."
        ]
    }
}

def main():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(DBMS_TOPICS, f, indent=2)
    print(f"Generated complete DBMS dataset with {len(DBMS_TOPICS)} topics at: {DATA_PATH}")

if __name__ == "__main__":
    main()
