# 🪐 CodeOrbit — AI Personalized Learning Platform for Engineering Students

> **A futuristic, gamified, and AI-personalized learning platform designed specifically for Computer Science & Engineering students.** Master core CS subjects, conquer algorithmic problem sets, train with an AI mock interview panel, and track your campus placement readiness.

---

## 📸 Design Aesthetics & User Experience

CodeOrbit is built with a **dark cyber-lunar purple aesthetic (`#090514`)**, rounded glassmorphism cards, glowing neon borders, circular subject badges, animated progress rings, particle confetti fanfare, and responsive layouts.

- **Color Palette**: Deep Obsidian Navy (`#090514`), Cyber Violet (`#7c3aed`), Electric Cyan (`#06b6d4`), Lunar Indigo (`#4f46e5`), Amber Flame (`#f59e0b`), and Emerald (`#10b981`).
- **Sidebar Architecture**: Features the 6 structured navigation sections:
  1. **LEARNING**: Learn, Practice Arena, Smart Review, Question Bank
  2. **AI**: AI Tutor, AI Recommendations
  3. **GAMIFICATION**: Daily Quests, Challenges, Achievements, Leaderboard
  4. **PERFORMANCE**: Progress Analytics, Study Planner
  5. **CAREER**: Placement Hub (DSA Tracks, AI Mock Interview Simulator, Company Guides)
  6. **PERSONAL**: My Notes, Profile, Settings

---

## 📚 6 Core Engineering Subjects & Visual Learning Paths

CodeOrbit includes **75 comprehensive academic topics** organized into visual node-based learning paths across 6 pillars:

| Subject | Topics | Description |
| :--- | :---: | :--- |
| **Database Management Systems (DBMS)** | 14 Topics | ER modeling, relational algebra, SQL queries & joins, 1NF/2NF/3NF/BCNF normalization, transactions & ACID, B+ trees, concurrency control (2PL, timestamping). |
| **Object Oriented Programming (OOPS)** | 12 Topics | Encapsulation, abstraction, inheritance hierarchies, polymorphism, SOLID principles, design patterns (Singleton, Factory, Observer), UML diagrams. |
| **Operating Systems (OS)** | 13 Topics | Process lifecycles, CPU scheduling (FCFS, SJF, Round Robin), inter-process communication, semaphores, deadlock handling (Banker's Algorithm), virtual memory & paging. |
| **Data Structures & Algorithms (DSA)** | 15 Topics | Arrays, linked lists, stacks & queues, binary trees, AVL trees, graphs (BFS/DFS, Dijkstra), sorting algorithms, dynamic programming, space & time complexity. |
| **Machine Learning (ML)** | 11 Topics | Supervised vs unsupervised learning, linear & logistic regression, decision trees, neural networks & backpropagation, evaluation metrics (precision, recall, ROC-AUC), bias-variance trade-off. |
| **Computer Networks (CN)** | 10 Topics | OSI & TCP/IP models, data link framing & error detection (CRC), IP addressing & subnetting, routing protocols (OSPF, BGP), transport protocols (TCP 3-way handshake vs UDP), DNS, HTTP/HTTPS. |

---

## ⚡ Key Architectural Features

### 1. 6-Step Interactive Lesson Player
Every topic is structured into a pedagogically sound 6-step flow:
1. **Introduction & Core Intuition** — Real-world engineering context.
2. **Deep Dive & Mechanics** — Step-by-step internal architecture.
3. **Interactive Code & Implementation** — Syntax, pseudocode, and best practices.
4. **Visual Diagram / Architecture** — Memory layouts, tables, and packet flows.
5. **Interactive Checkpoint Task** — Instant feedback with live evaluation.
6. **Summary & Key Takeaways** — High-yield exam cheat sheet.

### 2. Multi-Format Interactive Question Engine
Supports 6 diverse problem modalities:
- **Multiple Choice Questions (MCQ)** with explanation reveals.
- **Multi-Select Checkbox Questions**.
- **Output & Dry-Run Prediction** (code snippets with inputs/outputs).
- **Bug & Vulnerability Identification** (spotting off-by-one errors, concurrency hazards).
- **SQL & Query Workbenches** (writing and validating SQL statements).
- **Fill-in-the-Blank & Conceptual Matching**.

### 3. "Explain My Mistake" AI Modal
When a student answers incorrectly:
- **Why Wrong**: Pinpoints the logical flaw in their selection.
- **Core Concept**: Succinctly restates the underlying CS rule.
- **Real-World Analogy**: Grounded in relatable engineering concepts (e.g., locking a public restroom stall for Mutual Exclusion).
- **Try Similar Question**: Dynamically loads an alternative question on the same topic.

### 4. Spaced Repetition Smart Review Engine
Calculates memory retention decay curves:
- Mastery `< 50%` $\rightarrow$ Review in **1 day**
- Mastery `50% – 70%` $\rightarrow$ Review in **3 days**
- Mastery `70% – 85%` $\rightarrow$ Review in **7 days**
- Mastery `> 85%` $\rightarrow$ Review in **14 days**

### 5. Multi-Factor AI Recommendation Engine
Deterministic scoring model evaluating:
$$\text{Priority} = (100 - \text{Mastery}) \times 0.4 + \text{DaysSinceReview} \times 0.25 + \text{RecentMistakes} \times 0.2 + \text{PrerequisitesMet} \times 0.15$$

Categorizes recommendations into:
- **Needs Attention** (low mastery or frequent mistakes)
- **Due for Review** (spaced repetition decay)
- **Ready to Advance** (unlocked next topic in learning path)
- **Recommended Challenge** (boss challenge ready)

### 6. Placement & Career Hub
- **DSA Tracks & Problem Sets**: Categorized by Arrays, Trees, Dynamic Programming, and Core CS with difficulty filtering (Easy, Medium, Hard).
- **AI Mock Interview Simulator**: Evaluates student explanations across 4 structured rubrics:
  - *Clarity & Articulation*
  - *Technical Depth & Completeness*
  - *Answer Structure*
  - *Blindspots & What You Missed*
- **Company Guides**: Tailored roadmaps and checklists for Tier-1 Product Companies (FAANG), IT Services, FinTech, and Startups.

### 7. Full Gamification Engine
- **XP & Levels**: Tuned so $2,450 \text{ XP} = \text{Level } 12$.
- **7-Day Streaks**: With freeze forgiveness and weekly activity trackers.
- **Daily Quests & Milestones**: "Complete 3 lessons", "Answer 10 questions", "Earn 100 XP".
- **Boss Challenges**: Time-limited assessments awarding exclusive badges.
- **Leaderboards**: Global, College-level, and Friends rankings.

---

## 🛠️ Technology Stack

- **Frontend**:
  - React 19 + Vite 8
  - Tailwind CSS v4 (configured with `@tailwindcss/vite`)
  - Lucide React (Clean, modern icons)
  - Recharts (Interactive XP and mastery analytics charts)
  - Framer Motion (Smooth transitions and modal animations)
  - Axios (JWT Bearer authenticated client)
  - Canvas Confetti (Particle explosions on quest completion)
- **Backend**:
  - FastAPI (Python 3.12)
  - SQLAlchemy ORM with SQLite database fallback (`codeorbit.db`)
  - PyJWT (Secure authentication tokens)
  - Passlib & Bcrypt (Password hashing)
  - Pytest + HTTPX (Comprehensive test suite)
- **AI Layer**:
  - `AIProvider` abstraction with local Ollama support.
  - Built-in zero-cost, 100% offline `RuleBasedSmartProvider` with curated engineering explanations, interactive Quick Checks, and interview critiques.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment and activate
python -m venv venv
.\venv\Scripts\activate      # Windows
# or: source venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Seed the database with all 6 subjects, 75 topics, questions, and demo user
python seed.py

# Start FastAPI backend server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
Web application will be live at: `http://localhost:5173/`

---

## 🔑 Pre-Seeded Demo Student Credentials

Click the **"Auto-fill Demo Student"** button on the Login page or use:

| Field | Value |
| :--- | :--- |
| **Email** | `demo@codeorbit.local` |
| **Password** | `Demo@123` |
| **Student** | Alex Rivera (Class of 2026, NIT) |
| **Stats** | 🔥 7-Day Streak \| ⚡ Level 12 (2,450 XP) \| 💎 450 Gems |

---

## 🧪 Testing & Verification

### Running Backend Unit Tests
```bash
# From workspace root
set PYTHONPATH=backend
.\backend\venv\Scripts\pytest.exe backend/tests/test_api.py -v
```
*8 passed in 4.73s (tests auth, subjects, topic progress, attempts, recommendations, AI tutor, review service, and placement hub).*

### Running E2E Proxy Integration Tests
```bash
# Verifies all endpoints through the Vite dev proxy
.\backend\venv\Scripts\python.exe backend/test_e2e_endpoints.py
```

---

## 🌐 Deploying to Vercel (Single Unified Project)

CodeOrbit is architected to deploy as a **single Vercel project** containing both the React + Vite frontend and the FastAPI serverless backend under one unified URL (e.g. `https://my-codeorbit.vercel.app`).

### A. How to Deploy the Repository to Vercel
1. Push your latest code to your GitHub repository:
   ```bash
   git push origin main
   ```
2. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** → **"Project"**.
3. Select your repository (`MPrakash2007/AI-personalized-Learning`).
4. Configure the project settings as described below.

### B. Root Directory
- **Root Directory**: Leave as `./` (Root directory of the repository).
- Do **NOT** select `frontend` or `backend` as the root directory. Vercel will build both via `vercel.json`.

### C. Build & Output Settings
The repository's `vercel.json` and root `package.json` automatically configure these settings. If prompted in the Vercel dashboard:
- **Framework Preset**: `Vite` (or `Other`)
- **Build Command**: `cd frontend && npm install && npm run build` (or leave default `npm run build`)
- **Output Directory**: `frontend/dist`
- **Install Command**: Leave default

### D. Required Environment Variables
In the Vercel Project Settings (**Settings** → **Environment Variables**), add:

| Variable Name | Required? | Example Value | Description |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | **Yes (Prod)** | `postgresql://user:pass@ep-xyz.neon.tech/neondb?sslmode=require` | Managed PostgreSQL connection string (Neon, Supabase, Vercel Postgres). |
| `JWT_SECRET` | **Yes (Prod)** | `openssl rand -hex 32` | Cryptographic secret key for signing session tokens. |
| `CORS_ORIGINS` | Optional | `https://my-codeorbit.vercel.app` | Comma-separated custom origins (Vercel preview URLs are allowed automatically). |
| `AI_PROVIDER` | Optional | `rule-based` | Defaults to `rule-based` (offline, zero API keys required). |

### E. How to Configure the Database
1. Provision a free PostgreSQL database:
   - **Neon**: [neon.tech](https://neon.tech) (recommended for instant serverless pooling)
   - **Supabase**: [supabase.com](https://supabase.com)
   - **Vercel Postgres**: Integrated via Vercel Marketplace
2. Copy your connection URI and paste it as `DATABASE_URL` in Vercel.
   - *Note: Both `postgres://` and `postgresql://` URI schemes are automatically normalized.*
3. **Automatic Initialization**: On the first request after deployment, CodeOrbit automatically detects an empty database and runs idempotent seeding for all 6 subjects, 74 topics, 12 exam sections per topic, and the demo user!

### F. How to Test the Deployed Application
1. **Frontend Navigation**:
   - Open your deployed URL: `https://<your-project>.vercel.app/`
   - Test direct SPA routes (no 404s): `/learn`, `/practice`, `/ai-tutor`, `/question-bank`, `/placement`, `/profile`.
2. **Backend API Health**:
   - Visit: `https://<your-project>.vercel.app/api`
   - Expected Response:
     ```json
     {
       "app": "CodeOrbit",
       "description": "AI Personalized Learning Platform for Engineering Students",
       "version": "1.0.0",
       "status": "online",
       "docs": "/docs"
     }
     ```
3. **Authentication & Features**:
   - Login with demo student: `demo@codeorbit.local` / `Demo@123`.
   - Open any subject (e.g. DBMS) and test the 12-section masterclass, Quick Reference modal, and topic quiz submission.

---

## 📜 License
Educational MIT License — Built for Computer Science & Engineering students worldwide.

