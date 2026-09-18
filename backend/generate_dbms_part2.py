"""
Appends topics 7 to 12 to backend/curriculum/dbms.py.
"""
import os

DBMS_PART2 = '''
    # -------------------------------------------------------------------------
    # 7. SQL Joins
    # -------------------------------------------------------------------------
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
            "LEFT (OUTER) JOIN: Returns all records from the left table, and matched records from the right table (NULL if no match).",
            "RIGHT (OUTER) JOIN: Returns all records from the right table, and matched records from the left table.",
            "FULL (OUTER) JOIN: Returns all records when there is a match in either left or right table.",
            "CROSS JOIN: Returns Cartesian Product (m × n rows); no join condition required.",
            "SELF JOIN: A regular join where a table is joined with itself using table aliases (e.g. Employee-Manager hierarchy)."
        ],
        "classification": {
            "title": "Types of SQL Joins",
            "items": [
                {"name": "Inner Join", "desc": "Strict equality match (or theta comparison) on both sides."},
                {"name": "Left Outer Join", "desc": "Preserves all left tuples; pads right attributes with NULL."},
                {"name": "Right Outer Join", "desc": "Preserves all right tuples; pads left attributes with NULL."},
                {"name": "Full Outer Join", "desc": "Preserves all tuples from both tables regardless of match."},
                {"name": "Cross Join", "desc": "Unconditional combination of all tuples from both relations."},
                {"name": "Natural Join", "desc": "Automatically joins on all columns with identical names and types."}
            ]
        },
        "how_it_works": {
            "title": "Join Algorithms & Mechanics in RDBMS",
            "steps": [
                "1. Nested Loop Join: For each row in outer table, scans inner table. Optimal when outer table is small and inner table has index.",
                "2. Hash Join: Builds in-memory hash table on join key of smaller table, then probes with larger table. Ideal for large, unsorted datasets.",
                "3. Sort-Merge Join: Sorts both relations on join key, then scans simultaneously. Highly efficient when inputs are already sorted (e.g. clustered index)."
            ],
            "diagram": (
                "Venn Diagram Representations of Joins:\\n"
                "  [Table A] ∩ [Table B]      → INNER JOIN (Overlapping region only)\\n"
                "  [Table A] ∪ (A ∩ B)        → LEFT JOIN (All Table A + Overlap)\\n"
                "  (A ∩ B) ∪ [Table B]        → RIGHT JOIN (All Table B + Overlap)\\n"
                "  [Table A] ∪ [Table B]      → FULL OUTER JOIN (Everything from both)"
            )
        },
        "example": {
            "title": "Employee & Department Join Queries",
            "scenario": (
                "Given `Employees(emp_id, name, dept_id)` and `Departments(dept_id, dept_name)`:\\n"
                "- Find all employees and their department names, including employees without a department (LEFT JOIN):"
            ),
            "code": (
                "-- LEFT JOIN: Preserves employees without assigned departments\\n"
                "SELECT e.emp_id, e.name, d.dept_name\\n"
                "FROM Employees e\\n"
                "LEFT JOIN Departments d ON e.dept_id = d.dept_id;\\n\\n"
                "-- SELF JOIN: Employee and Manager hierarchy\\n"
                "SELECT e.name AS Employee, m.name AS Manager\\n"
                "FROM Employees e\\n"
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
            "correct": "In an INNER JOIN, filtering in ON vs WHERE produces identical results; but in a LEFT JOIN, conditions in the ON clause filter the right table BEFORE joining (preserving left rows), while conditions in WHERE filter the final joined result (discarding left rows).",
            "explanation": "e.g. `LEFT JOIN B ON A.id = B.id AND B.status = 'Active'` keeps all A rows, but `WHERE B.status = 'Active'` removes A rows where B is NULL."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is a Self Join and when is it used?",
                "a": "A Self Join is a regular join in which a table is joined with itself using distinct table aliases. It is commonly used to model recursive or hierarchical relationships, such as finding an employee's manager within an Employees table (where manager_id references emp_id)."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the difference between INNER JOIN, LEFT OUTER JOIN, and FULL OUTER JOIN with examples.",
                "a": "1. INNER JOIN returns only records that have matching keys in both tables. Unmatched rows from either table are omitted.\n2. LEFT OUTER JOIN returns all records from the left table; matching records from the right table are joined, while unmatched right columns are filled with NULL.\n3. FULL OUTER JOIN returns all records from both tables; where matches exist, rows are combined; where no match exists, missing sides are padded with NULL."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the three primary join algorithms used by DBMS execution engines and analyze their time complexities.",
                "a": "1. Nested Loop Join: Iterates over outer relation R and for each tuple searches inner relation S. Cost: O(|R| × |S|) without index; O(|R| × log|S|) with B-Tree index on S. Best for small outer tables.\n2. Hash Join: Builds an in-memory hash table on the join key of the smaller relation, then scans the larger relation to probe the hash table. Cost: O(|R| + |S|). Best for large, unsorted equijoins.\n3. Sort-Merge Join: Sorts both relations on join key (cost O(|R|log|R| + |S|log|S|)), then performs a linear merge pass (cost O(|R| + |S|)). Highly optimal when inputs are already sorted by clustered indexes."
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

    # -------------------------------------------------------------------------
    # 8. Nested Queries
    # -------------------------------------------------------------------------
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
            "EXISTS / NOT EXISTS: Evaluates to TRUE/FALSE; highly optimized because it short-circuits on first match.",
            "Subquery in FROM Clause: Known as an inline view or derived table; must be given a table alias."
        ],
        "classification": {
            "title": "Subquery Operators in SQL",
            "items": [
                {"name": "IN / NOT IN", "desc": "Tests whether a value matches any member of the subquery result set."},
                {"name": "EXISTS / NOT EXISTS", "desc": "Boolean test checking if subquery returns at least one row. Ignores column values."},
                {"name": "ANY / SOME", "desc": "Compares value to each value in list; true if condition holds for AT LEAST ONE value (e.g. > ANY)."},
                {"name": "ALL", "desc": "Compares value to all values in list; true only if condition holds for ALL values (e.g. > ALL)."}
            ]
        },
        "how_it_works": {
            "title": "Correlated vs Non-Correlated Subquery Execution",
            "steps": [
                "Non-Correlated: DBMS executes inner query once → caches result set in temporary buffer → evaluates outer query against cached result.",
                "Correlated: Outer query fetches row 1 → binds outer values into inner query → inner query executes and returns result → outer query tests condition → repeats for row 2, 3, ... N."
            ],
            "diagram": (
                "Subquery Execution Flow:\\n"
                "Non-Correlated: [Inner Query] ──(Executes Once)──> [Result Set] ──> [Outer Query]\\n\\n"
                "Correlated:     [Outer Row i] ──(Binds values)──> [Inner Query]\\n"
                "                      ^                                 │\\n"
                "                      └───────(Returns T/F or Val)──────┘ (Repeats N times)"
            )
        },
        "example": {
            "title": "Employees Earning Above Department Average",
            "scenario": (
                "Find employees who earn more than the average salary of their respective department. "
                "This requires a correlated subquery because the average salary depends on the department of the outer row:"
            ),
            "code": (
                "-- Correlated Subquery: inner query references outer table 'e1'\\n"
                "SELECT e1.name, e1.department, e1.salary\\n"
                "FROM Employees e1\\n"
                "WHERE e1.salary > (\\n"
                "    SELECT AVG(e2.salary)\\n"
                "    FROM Employees e2\\n"
                "    WHERE e2.department = e1.department\\n"
                ");\\n\\n"
                "-- Subquery using EXISTS: Students who enrolled in CS101\\n"
                "SELECT s.name\\n"
                "FROM Students s\\n"
                "WHERE EXISTS (\\n"
                "    SELECT 1 FROM Enrollments e\\n"
                "    WHERE e.student_id = s.student_id AND e.course_code = 'CS101'\\n"
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
            "correct": "If a subquery returns even a single NULL value, `NOT IN` evaluates to UNKNOWN for all outer rows, returning ZERO results! In contrast, `NOT EXISTS` handles NULLs safely without unexpected empty results.",
            "explanation": "Exam trick: `WHERE id NOT IN (SELECT id FROM T)` returns empty if T contains any row where id IS NULL."
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
                "a": "1. IN evaluates the subquery, returns a list of values, and checks whether the outer value matches any element. It performs poorly on large subquery results and fails if NULLs exist in a NOT IN query.\n2. EXISTS tests for the existence of rows in the subquery. It returns TRUE as soon as the first matching row is found (short-circuit evaluation), making it significantly faster for large datasets. It also safely ignores NULL values in subquery columns."
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
            "NOT IN fails and returns 0 rows if the subquery returns any NULL value! Use NOT EXISTS instead."
        ]
    },

    # -------------------------------------------------------------------------
    # 9. Normalization
    # -------------------------------------------------------------------------
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
            "Functional Dependency (X → Y): Attribute X uniquely determines attribute Y. If t1[X] = t2[X], then t1[Y] must equal t2[Y].",
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
                "2. Identify Prime Attributes (attributes belonging to any candidate key) and Non-Prime Attributes.",
                "3. Check 2NF: If any FD has Proper Subset of Candidate Key → Non-Prime Attribute, relation violates 2NF.",
                "4. Check 3NF: For every FD X → Y, verify if X is a Superkey OR Y is a Prime Attribute. If neither, violates 3NF.",
                "5. Check BCNF: For every FD X → Y, verify if X is a Superkey. If any determinant X is not a superkey, violates BCNF.",
                "6. Decompose violating relation into lossless sub-relations preserving dependencies where possible."
            ],
            "diagram": (
                "Normal Form Inclusion Hierarchy:\\n"
                "┌───────────────────────────────────────┐\\n"
                "│  1NF (Atomic Attributes)              │\\n"
                "│   ┌───────────────────────────────────┤\\n"
                "│   │  2NF (No Partial Dependency)      │\\n"
                "│   │   ┌───────────────────────────────┤\\n"
                "│   │   │  3NF (No Transitive Dep)      │\\n"
                "│   │   │   ┌───────────────────────────┤\\n"
                "│   │   │   │  BCNF (Determinant is SK) │\\n"
                "│   │   │   └───────────────────────────┘\\n"
                "└───┴───┴───────────────────────────────┘"
            )
        },
        "example": {
            "title": "Normalization from Unnormalized to BCNF",
            "scenario": (
                "Given relation `Student_Course(roll_no, course_code, student_name, course_name, instructor, inst_office)`:\\n"
                "- Candidate Key: {roll_no, course_code}\\n"
                "- FDs:\\n"
                "  1. roll_no → student_name (Partial dependency: roll_no is subset of composite key! Violates 2NF)\\n"
                "  2. course_code → course_name, instructor (Partial dependency: Violates 2NF)\\n"
                "  3. instructor → inst_office (Transitive dependency: non-key determines non-key! Violates 3NF)\\n\\n"
                "Decomposition into 3NF/BCNF:\\n"
                "1. `Students(roll_no PK, student_name)`\\n"
                "2. `Courses(course_code PK, course_name, instructor)`\\n"
                "3. `Instructors(instructor PK, inst_office)`\\n"
                "4. `Enrollments(roll_no FK, course_code FK, PRIMARY KEY(roll_no, course_code))`"
            ),
            "code": (
                "-- Fully normalized BCNF schema\\n"
                "CREATE TABLE Instructors (\\n"
                "    instructor VARCHAR(50) PRIMARY KEY,\\n"
                "    inst_office VARCHAR(20)\\n"
                ");\\n\\n"
                "CREATE TABLE Courses (\\n"
                "    course_code VARCHAR(10) PRIMARY KEY,\\n"
                "    course_name VARCHAR(100),\\n"
                "    instructor VARCHAR(50) REFERENCES Instructors(instructor)\\n"
                ");\\n\\n"
                "CREATE TABLE Enrollments (\\n"
                "    roll_no INT REFERENCES Students(roll_no),\\n"
                "    course_code VARCHAR(10) REFERENCES Courses(course_code),\\n"
                "    PRIMARY KEY (roll_no, course_code)\\n"
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
                "a": "1. Definitions: 1NF requires atomic values; 2NF eliminates partial dependencies; 3NF eliminates transitive dependencies (X is SK or Y is prime); BCNF requires every determinant to be a superkey.\n2. Candidate Key finding for R:\n- Attributes not on RHS: A, E. Closure of (AE):\n  AE+ = {A, E, B, C, D} (A->B, E->C, BC->D). AE covers all attributes and is minimal. Candidate Key = {AE}.\n- Prime attributes: {A, E}; Non-prime attributes: {B, C, D}.\n3. Testing Normal Forms:\n- Check A -> B: A is a proper subset of candidate key {AE}, and B is a non-prime attribute. This is a PARTIAL DEPENDENCY!\nConclusion: Because A -> B violates 2NF, the highest normal form of relation R is 1NF."
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

    # -------------------------------------------------------------------------
    # 10. Transactions
    # -------------------------------------------------------------------------
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
            "Atomicity: 'All or Nothing' execution managed by the Recovery Manager using Undo Logs.",
            "Consistency: Preserves database invariants and integrity constraints (e.g. Total sum of balances remains constant).",
            "Isolation: Concurrent transactions execute without seeing each other's uncommitted intermediate states (Concurrency Control Manager).",
            "Durability: Committed updates survive subsequent power outages and system crashes (Redo Logs / WAL).",
            "Transaction States: Active → Partially Committed → Committed; or Active/Partially Committed → Failed → Aborted.",
            "Conflict Serializability: A schedule is conflict serializable if its precedence graph has NO cycles."
        ],
        "classification": {
            "title": "Transaction States & Lifecycle",
            "items": [
                {"name": "Active", "desc": "Initial state; transaction is actively executing read and write operations."},
                {"name": "Partially Committed", "desc": "Final statement executed, but updates are still in volatile buffer memory, not yet flushed to disk."},
                {"name": "Committed", "desc": "Transaction successfully completed; changes permanently recorded in Write-Ahead Log (WAL)."},
                {"name": "Failed", "desc": "Discovery that normal execution cannot proceed (hardware crash, arithmetic error, or concurrency abort)."},
                {"name": "Aborted", "desc": "Transaction rolled back; database restored to state prior to transaction start."}
            ]
        },
        "how_it_works": {
            "title": "Precedence Graph Conflict Serializability Algorithm",
            "steps": [
                "1. For each transaction Ti in schedule S, create a node labeled Ti.",
                "2. Identify all conflicting operations on the same data item Q:\n  - Ti reads Q and Tj writes Q (Read-Write conflict)\n  - Ti writes Q and Tj reads Q (Write-Read conflict)\n  - Ti writes Q and Tj writes Q (Write-Write conflict)",
                "3. If Ti's conflicting operation occurs before Tj's operation in the schedule, draw a directed edge Ti → Tj.",
                "4. Check for cycles: If the Precedence Graph has NO CYCLES, schedule S is Conflict Serializable.",
                "5. If serializable, topological sort of the graph yields the equivalent serial schedule (e.g. T1 → T2 → T3)."
            ],
            "diagram": (
                "Transaction State Transition Diagram:\\n"
                "      [Active]\\n"
                "       /    \\\\\\n"
                "      /      \\\\ (Error / Abort)\\n"
                "     v        v\\n"
                "[Partially   [Failed]\\n"
                " Committed]     │\\n"
                "     │ (WAL)    v\\n"
                "     v      [Aborted]\\n"
                " [Committed]"
            )
        },
        "example": {
            "title": "Bank Fund Transfer Transaction",
            "scenario": (
                "Transfer $500 from Account A ($1000) to Account B ($2000):\\n"
                "T1: Read(A); A = A - 500; Write(A); Read(B); B = B + 500; Write(B); Commit;\\n\\n"
                "If system crashes after Write(A) but before Write(B):\\n"
                "- Without Atomicity: $500 disappeared (Inconsistency).\\n"
                "- With Atomicity: Recovery manager reads Undo log, restores A back to $1000, and aborts T1."
            ),
            "code": (
                "-- SQL Transaction Block\\n"
                "BEGIN TRANSACTION;\\n"
                "    UPDATE Accounts SET balance = balance - 500 WHERE account_id = 'A';\\n"
                "    UPDATE Accounts SET balance = balance + 500 WHERE account_id = 'B';\\n"
                "    -- Integrity check\\n"
                "    IF (SELECT balance FROM Accounts WHERE account_id = 'A') < 0 THEN\\n"
                "        ROLLBACK;\\n"
                "    ELSE\\n"
                "        COMMIT;\\n"
                "    END IF;"
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
                "a": "ACID stands for:\n1. Atomicity: All operations succeed or none do (All-or-Nothing).\n2. Consistency: Database remains in a valid state adhering to all integrity constraints.\n3. Isolation: Concurrent transactions execute independently without interference.\n4. Durability: Committed changes permanently survive subsequent system crashes."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the Precedence Graph method for testing Conflict Serializability.",
                "a": "1. Construct a directed graph G = (V, E) where each node represents a transaction Ti in the schedule.\n2. Add a directed edge Ti → Tj if Ti executes an operation that conflicts with a subsequent operation in Tj on the same data item (Read-Write, Write-Read, or Write-Write).\n3. Test the graph for cycles using Depth First Search (DFS).\n4. If the graph contains no cycles, the schedule is Conflict Serializable, and a topological sort of the graph gives the equivalent serial schedule. If a cycle exists, the schedule is non-serializable."
            },
            {
                "marks": "10-Mark Question",
                "q": "Test whether the schedule S: r1(X), r2(Y), w1(X), r1(Y), w2(Y), w1(Y) is conflict serializable. If yes, find equivalent serial schedule.",
                "a": "Conflicting pairs in S:\n1. On item X: r1(X) before w1(X) (same transaction T1, no edge).\n2. On item Y:\n- r2(Y) before r1(Y) (Read-Read, no conflict).\n- r2(Y) before w1(Y): T2 reads Y before T1 writes Y → Edge T2 → T1.\n- r1(Y) before w2(Y): T1 reads Y before T2 writes Y → Edge T1 → T2!\nCycle Analysis:\nWe have edge T2 → T1 and edge T1 → T2, forming a DIRECTED CYCLE: T1 ⇆ T2.\nConclusion: Because the precedence graph contains a cycle between T1 and T2, the schedule S is NOT Conflict Serializable."
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

    # -------------------------------------------------------------------------
    # 11. Concurrency Control
    # -------------------------------------------------------------------------
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
            "Concurrency Anomalies: Lost Update (W-W), Dirty Read / Temporary Update (W-R), Non-Repeatable Read (R-W), Phantom Read.",
            "Lock Types: Shared Lock (S-Lock / Read Lock, multiple readers allowed) and Exclusive Lock (X-Lock / Write Lock, exactly one writer).",
            "Two-Phase Locking (2PL): Growing Phase (only acquire locks) → Shrinking Phase (only release locks). Guarantees serializability.",
            "Strict 2PL: Releases Exclusive locks only AFTER transaction commits or aborts (prevents Cascading Rollback).",
            "Rigorous 2PL: Releases ALL locks (Shared and Exclusive) only after commit/abort.",
            "Deadlock: A state where two or more transactions are waiting indefinitely for locks held by each other.",
            "Deadlock Handling: Deadlock Prevention (Wait-Die, Wound-Wait) and Deadlock Detection (Wait-For Graph cycles)."
        ],
        "classification": {
            "title": "Concurrency Control Protocols",
            "items": [
                {"name": "Lock-Based Protocols", "desc": "Uses S/X locks with 2PL, Strict 2PL, or Rigorous 2PL to prevent conflicting access."},
                {"name": "Timestamp-Based Protocols", "desc": "Assigns unique timestamp TS(T) at start; ensures serial order matches timestamp order using Thomas Write Rule."},
                {"name": "Validation / Optimistic Protocols", "desc": "Transactions execute without locking in local memory; validated before commit (Read, Validate, Write phases)."},
                {"name": "Multiversion Concurrency Control (MVCC)", "desc": "Maintains multiple versions of rows so readers never block writers and writers never block readers."}
            ]
        },
        "how_it_works": {
            "title": "Deadlock Prevention Schemes (Wait-Die vs Wound-Wait)",
            "steps": [
                "Assume older transaction T_old has smaller timestamp TS(T_old) < TS(T_young).",
                "Wait-Die Scheme (Non-preemptive):\n  - If T_old requests resource held by T_young → T_old is allowed to WAIT.\n  - If T_young requests resource held by T_old → T_young DIES (aborts and restarts).",
                "Wound-Wait Scheme (Preemptive):\n  - If T_old requests resource held by T_young → T_old WOUNDS T_young (preempts and aborts T_young).\n  - If T_young requests resource held by T_old → T_young is allowed to WAIT."
            ],
            "diagram": (
                "Two-Phase Locking (2PL) Phases:\\n"
                "Lock Count\\n"
                "    ▲           [Lock Point]\\n"
                "    │              /\\ \\n"
                "    │             /  \\ \\n"
                "    │  GROWING   /    \\   SHRINKING\\n"
                "    │   PHASE   /      \\    PHASE\\n"
                "    │(Acquires)/        \\(Releases)\\n"
                "    │         /          \\ \\n"
                "    └────────┴────────────┴──────► Time\\n"
                "       Start            Commit"
            )
        },
        "example": {
            "title": "Dirty Read & Strict 2PL Resolution",
            "scenario": (
                "Dirty Read Scenario:\\n"
                "T1 writes balance = $500. T2 reads balance = $500 and issues a loan. "
                "T1 then aborts and rolls back to balance = $100! T2 made a decision on invalid data (Dirty Read).\\n\\n"
                "Strict 2PL Prevention:\\n"
                "Under Strict 2PL, T1 holds its Exclusive Lock on balance until it commits or aborts. "
                "T2 is blocked from reading balance until T1 finishes, completely eliminating dirty reads."
            ),
            "code": (
                "-- Strict 2PL Lock Flow\\n"
                "-- T1:\\n"
                "LOCK-X (Account_A);\\n"
                "Write(Account_A);\\n"
                "-- T2 requests LOCK-S (Account_A) -> BLOCKED by DBMS Lock Manager\\n"
                "COMMIT; -- T1 commits, and only now releases LOCK-X\\n"
                "-- T2 is unblocked and acquires LOCK-S safely"
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
            "explanation": "If T1 holds Lock(A) and requests Lock(B), while T2 holds Lock(B) and requests Lock(A), both follow 2PL rules but result in deadlock."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the Dirty Read problem in database concurrency?",
                "a": "A Dirty Read (Temporary Update problem) occurs when transaction T2 reads a data item that has been updated by an uncommitted transaction T1. If T1 subsequently fails and rolls back, the data read by T2 never existed in the database, leading to inconsistent or incorrect state."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Two-Phase Locking (2PL) and differentiate between Basic 2PL, Strict 2PL, and Rigorous 2PL.",
                "a": "Two-Phase Locking (2PL) divides locking into two distinct phases: (1) Growing Phase where locks can only be acquired, and (2) Shrinking Phase where locks can only be released.\n1. Basic 2PL: Locks can be released at any time during shrinking phase. Prone to cascading aborts.\n2. Strict 2PL: All Exclusive (X) locks must be held until transaction commit/abort. Prevents cascading aborts and guarantees strict schedules.\n3. Rigorous 2PL: All locks (both Shared and Exclusive) are held until transaction commit/abort. Guarantees serialization in exact commit order."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain Deadlock detection using Wait-For Graphs and detail the Wait-Die and Wound-Wait deadlock prevention algorithms.",
                "a": "1. Wait-For Graph (WFG): Directed graph where nodes represent active transactions. A directed edge Ti → Tj exists if Ti is waiting for a lock currently held by Tj. A cycle in the WFG indicates a Deadlock. When detected, the DBMS selects a victim transaction to abort and roll back.\n2. Deadlock Prevention using Timestamps (older transaction has smaller timestamp):\n- Wait-Die (Non-preemptive): If an older transaction requests a resource held by a younger transaction, the older is allowed to wait. If a younger transaction requests a resource held by an older, the younger dies (aborts and restarts).\n- Wound-Wait (Preemptive): If an older transaction requests a resource held by a younger transaction, the older 'wounds' (aborts and preempts) the younger. If a younger requests a resource held by an older, the younger waits."
            }
        ],
        "revision_60s": [
            "Concurrency anomalies: Lost Update, Dirty Read, Unrepeatable Read, Phantom Read.",
            "Shared Lock (S) = Read only; Exclusive Lock (X) = Read & Write.",
            "2PL has Growing Phase (acquire only) and Shrinking Phase (release only).",
            "2PL guarantees serializability, but DOES NOT prevent deadlocks.",
            "Strict 2PL holds X-locks until commit to prevent cascading rollbacks.",
            "Wait-Die: Older waits, younger dies. Wound-Wait: Older wounds (preempts), younger waits."
        ]
    },

    # -------------------------------------------------------------------------
    # 12. Indexing and Recovery
    # -------------------------------------------------------------------------
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
            "Scanning every disk block in a 50-million row table takes minutes. An index provides an auxiliary search structure "
            "ordered by key. B+ Trees are the universal indexing standard in databases because all leaf nodes are at the exact same depth "
            "and are doubly linked for sequential range scans. For fault tolerance, Write-Ahead Logging (WAL) mandates that log records "
            "must hit persistent disk before dirty data pages are flushed, enabling ARIES recovery (Analysis, Redo, Undo)."
        ),
        "key_points": [
            "Primary Index: Defined on an ordered data file sorted on the Primary Key.",
            "Clustering Index: Defined on an ordered data file sorted on a non-key ordering attribute.",
            "Secondary Index: Defined on an unordered file; can be created on any candidate key or non-key column.",
            "Dense Index: Contains an index entry for EVERY search key value in the data file.",
            "Sparse Index: Contains index entries for only some search values (typically one per data block).",
            "B+ Tree Properties: Balanced tree; leaf nodes store all data pointers and are linked; internal nodes store routing keys.",
            "Write-Ahead Logging (WAL): Log records must be written to disk BEFORE the corresponding dirty database page is written to disk.",
            "Checkpointing: Periodically flushes all dirty pages to disk and writes a checkpoint record to truncate log replay time."
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
                "1. Analysis Phase: Scans log forward from the last checkpoint to identify active uncommitted transactions and dirty buffer pages at crash time.",
                "2. Redo Phase: Scans forward from the oldest unwritten page LSN; reapplies all logged updates (committed and uncommitted) to restore pre-crash state ('repeats history').",
                "3. Undo Phase: Scans backward from the end of the log; rolls back all updates made by active transactions that never committed before the crash, writing Compensation Log Records (CLRs)."
            ],
            "diagram": (
                "B+ Tree Index Structure:\\n"
                "             [ 50 | 100 ]            ← Root Node\\n"
                "            /     │      \\\\n"
                "      [ 20 | 35 ] [ 70 ] [ 120 | 150 ] ← Internal Routing Nodes\\n"
                "      /    │   \\   ...     ...\\n"
                "   [Leaves store all data pointers & linked list: L1 <-> L2 <-> L3 <-> L4]"
            )
        },
        "example": {
            "title": "B+ Tree Search vs Range Scan",
            "scenario": (
                "Query: `SELECT * FROM Employees WHERE salary BETWEEN 50000 AND 80000;`\\n"
                "1. Traverse B+ Tree from root to leaf node matching salary = 50000 in O(log_m N) block I/O reads.\\n"
                "2. Follow the leaf node doubly-linked list sequentially until salary > 80000.\\n"
                "This avoids traversing tree branches repeatedly, making range scans blazing fast."
            ),
            "code": (
                "-- Creating B-Tree / B+ Tree Indexes in SQL\\n"
                "CREATE TABLE Employees (\\n"
                "    emp_id INT PRIMARY KEY,               -- Clustered / Primary B+ Tree Index\\n"
                "    email VARCHAR(100) UNIQUE,            -- Unique Secondary B+ Tree Index\\n"
                "    department_id INT,\\n"
                "    salary NUMERIC(10,2)\\n"
                ");\\n\\n"
                "-- Secondary index for fast range queries\\n"
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
                "a": "The Write-Ahead Logging (WAL) protocol mandates that any update made to a database page in buffer memory must have its corresponding log record written and flushed to non-volatile disk BEFORE the dirty page itself is allowed to be written to disk.\nThis ensures that if a crash occurs mid-execution:\n1. The Redo log can reapply committed changes that were not yet flushed to data files (Durability).\n2. The Undo log can reverse uncommitted modifications that were partially written to disk (Atomicity)."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the ARIES recovery algorithm detailing the Analysis, Redo, and Undo phases.",
                "a": "ARIES (Algorithms for Recovery and Isolation Exploiting Semantics) handles crash recovery in three sequential phases:\n1. Analysis Phase: Scans the log forward from the most recent Checkpoint to determine the state at crash time: identifies all active transactions (the Transaction Table) and dirty pages in memory (the Dirty Page Table).\n2. Redo Phase: 'Repeats history' by scanning forward from the smallest PageLSN in the Dirty Page Table to the crash point, reapplying all logged updates (for both committed and uncommitted transactions) to restore the exact pre-crash state.\n3. Undo Phase: Scans backward from the crash point, rolling back all operations performed by active transactions that never committed before the crash. For each undone operation, a Compensation Log Record (CLR) is written to prevent repeated work if another crash occurs during recovery."
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
'''

with open(os.path.join(os.path.dirname(__file__), "curriculum", "dbms.py"), "a", encoding="utf-8") as f:
    f.write(DBMS_PART2)

print("Appended topics 7-12 to DBMS module successfully.")
