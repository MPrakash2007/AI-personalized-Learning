"""
Builds curriculum data for DBMS (12 topics) in JSON format.
"""
import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "curriculum", "data")
os.makedirs(DATA_DIR, exist_ok=True)

DBMS_DATA = {
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
            "Traditional file systems suffer from data redundancy, inconsistency, lack of atomicity, and poor concurrency. "
            "A DBMS solves these issues through a centralized catalog, standard declarative query language (SQL), "
            "and strict ACID properties. It separates user applications from physical storage media through three abstraction levels."
        ),
        "key_points": [
            "Data Abstraction: Hides physical storage details across View, Conceptual, and Internal levels.",
            "Data Independence: Enables altering storage or logical schemas without rewriting application code.",
            "Minimal Redundancy: Centralized logical relations avoid duplicate data files across departments.",
            "Concurrency Control: Allows multi-user concurrent querying without race conditions or lost updates.",
            "Crash Recovery: Write-Ahead Logging (WAL) and checkpoints ensure recovery from power or hardware failures.",
            "Integrity Constraints: Enforces domain rules, foreign keys, and role-based permissions."
        ],
        "classification": {
            "title": "Classification of Database Systems",
            "items": [
                {"name": "Hierarchical DBMS", "desc": "Tree structure with parent-child 1:N relationships (e.g., IBM IMS)."},
                {"name": "Network DBMS", "desc": "Graph structure with record types and set types allowing M:N (e.g., IDMS)."},
                {"name": "Relational DBMS (RDBMS)", "desc": "Tabular relations with primary/foreign keys based on relational algebra (e.g., PostgreSQL, MySQL)."},
                {"name": "Object-Oriented DBMS", "desc": "Stores complex objects with encapsulation, methods, and inheritance."},
                {"name": "NoSQL DBMS", "desc": "Distributed non-relational stores (Document, Key-Value, Columnar, Graph) for horizontal scale."}
            ]
        },
        "how_it_works": {
            "title": "DBMS Architecture & Query Pipeline",
            "steps": [
                "1. User Query: Application submits declarative SQL query.",
                "2. Parser & Lexer: Checks syntax, resolves table names against the Data Dictionary.",
                "3. Query Optimizer: Generates multiple query plans, estimates I/O costs, and selects the optimal plan.",
                "4. Execution Engine: Executes relational operators (Index Scan, Hash Join, Filter).",
                "5. Buffer Pool Manager: Checks RAM buffer cache; if absent, reads disk blocks via OS File Manager.",
                "6. Concurrency & Lock Manager: Acquires Shared/Exclusive locks to guarantee serializability.",
                "7. Recovery Manager: Flushes Write-Ahead Log (WAL) records before updating persistent storage."
            ],
            "diagram": "User SQL → Parser → Cost-Based Optimizer → Execution Engine → Buffer Pool → Storage & WAL Logs"
        },
        "example": {
            "title": "University Academic Management System",
            "scenario": (
                "In a traditional file system, Admissions, Accounts, and Hostels each maintain separate student files. "
                "Updating a student's address in Admissions leaves obsolete data in Accounts.\n"
                "In a DBMS, a centralized `Students` table is referenced by `Enrollments` and `Fee_Receipts`. "
                "A single UPDATE statement immediately reflects across all university subsystems."
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
                ["Data Independence", "None — changing file layout breaks application code", "High — Three-Schema architecture provides logical & physical independence"]
            ]
        },
        "formulas": [
            {"name": "Three-Schema Levels", "formula": "External (Views) → Conceptual (Logical) → Internal (Physical)", "explanation": "ANSI/SPARC architecture separates user views from disk block layout."},
            {"name": "Physical Independence", "formula": "Modifying Internal Schema does NOT affect Conceptual Schema", "explanation": "Upgrading to SSDs or adding B-Tree indexes does not alter SQL queries."},
            {"name": "Logical Independence", "formula": "Modifying Conceptual Schema does NOT affect External Views", "explanation": "Adding a new column to a table does not break existing user views."}
        ],
        "exam_tip": "Remember: Logical Data Independence is harder to achieve than Physical Data Independence because user queries are written directly against the logical schema structure.",
        "common_confusion": {
            "wrong": "A database and a DBMS are the exact same thing.",
            "correct": "A database is the passive structured collection of stored data; a DBMS is the active software engine used to access and manage that database.",
            "explanation": "PostgreSQL is the DBMS; your university student records are the database."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Define Data Independence and name its two types.",
                "a": "Data Independence is the ability to modify the schema at one level of a database system without altering the schema at the next higher level. The two types are: (1) Physical Data Independence and (2) Logical Data Independence."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the ANSI/SPARC Three-Schema Architecture of a DBMS.",
                "a": "The Three-Schema Architecture divides the database into three levels:\n1. External Level (View Level): Describes part of the database tailored to specific user groups.\n2. Conceptual Level (Logical Level): Describes what data is stored across the entire database, entity relationships, and constraints.\n3. Internal Level (Physical Level): Describes how data is physically laid out on disk blocks, including access paths, compression, and indexes.\nThis architecture isolates user applications from physical storage changes."
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
    }
}

with open(os.path.join(DATA_DIR, "dbms.json"), "w", encoding="utf-8") as f:
    json.dump(DBMS_DATA, f, indent=2)

print("Saved DBMS fundamentals & ER model to dbms.json")
