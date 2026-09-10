# AI Resume Analyzer & Interview Agent — Project Overview

> **A concise, comprehensive technical summary of the system architecture, core capabilities, execution pipeline, and setup.**

---

## 1. Project Summary

The **AI Resume Analyzer & Mock Interview Agent** is an end-to-end intelligent career preparation assistant. Built with **Streamlit**, **LangChain (LCEL)**, and **Google Gemini**, the system transforms a candidate's static PDF resume into an actionable career optimization suite:

1. **ATS Analysis**: Evaluates resume compliance against modern Applicant Tracking System rubrics.
2. **Skill Taxonomy Extraction**: Categorizes technical skills across 8 domains with confidence levels, proficiency signals, and evidence citations.
3. **Adaptive Mock Interview & Evaluation**: Simulates real-time technical interviews with dynamic difficulty, contextual follow-ups, multi-metric scoring (0–10), and ideal model answers.
4. **Resume Rewriting & HTML Export**: Tailors resumes to specific job descriptions using metric-driven accomplishment formulas (Google XYZ) and renders styled, downloadable HTML resumes.

---

## 2. System Architecture & Tech Stack

```
[ PDF Resume ] ──► [ PyMuPDF Parser ] ──► [ Text Cleaning ]
                                                  │
                  ┌───────────────────────────────┴───────────────────────────────┐
                  ▼                                                               ▼
        [ ATS Analysis Chain ]                                          [ Skill Taxonomy Chain ]
         (with_structured_output)                                        (with_structured_output)
                  │                                                               │
                  └───────────────────────────────┬───────────────────────────────┘
                                                  ▼
                                       [ Streamlit Session State ]
                                                  │
                 ┌────────────────────────────────┴────────────────────────────────┐
                 ▼                                                                 ▼
      [ Adaptive Mock Interview ]                                       [ Role-Tailored Rewrite ]
     • Dynamic Question Generator                                      • ATS Keyword Optimization
     • Rubric Answer Evaluator (0–10)                                  • Google XYZ Accomplishments
     • Ideal Answer Generation                                         • Responsive HTML Resume Export
```

### Technology Stack

| Layer | Tool / Library | Role |
| :--- | :--- | :--- |
| **Frontend / UI** | `streamlit` | Reactive UI, session state management, metric dashboards, HTML preview |
| **LLM Orchestration** | `langchain`, `langchain-core` | LCEL pipeline routing, prompt formatting, Pydantic structured output |
| **Language Models** | `langchain-google-genai` | Google Gemini (`gemini-flash-latest` with fallback chains & exponential backoff) |
| **Data Validation** | `pydantic` | Type-safe JSON schemas enforcing strict structured model outputs |
| **Document Ingestion** | `pymupdf` (`fitz`) | High-fidelity in-memory PDF binary parsing |
| **Text Processing** | Python `re` | Whitespace normalization and noise removal |
| **Config & Secrets** | `python-dotenv` | Environment variable isolation (`GEMINI_API_KEY`, model selection) |

---

## 3. Core Modules & Pipeline Details

### 3.1 Document Ingestion (`services/`)
- **[pdf_parser.py](file:///services/pdf_parser.py)**: Extracts text from uploaded PDF buffers directly in memory using PyMuPDF.
- **[resume_extractor.py](file:///services/resume_extractor.py)**: Normalizes excessive line breaks, cleans artifact characters, and prepares raw text for LLM prompts.

### 3.2 ATS Evaluation (`chains/ats_chain.py` & `prompts/ats_prompt.md`)
- Extracts an objective ATS match score (0–100).
- Identifies critical resume strengths, formatting/metric weaknesses, high-impact missing industry keywords, and concrete recommendations.
- Output model: `ATSResponse`.

### 3.3 Skill Extraction & Profiling (`chains/skill_chain.py` & `prompts/skills_prompt.md`)
- Normalizes skills into 8 categorized groups:
  - *Programming Languages*, *Frameworks & Libraries*, *Databases*, *Cloud & DevOps*, *Tools & Platforms*, *AI & ML*, *Domains & Concepts*, *APIs & Protocols*.
- Extracts per-skill metadata: `confidence` (`HIGH`/`MEDIUM`/`LOW`), `proficiency_signal` (`PRIMARY`/`SECONDARY`/`MENTIONED`), and exact textual `evidence`.
- Identifies candidate name, target role, and suggested interview focus topics.
- Output model: `SkillExtractionResult`.

### 3.4 Adaptive Mock Interview (`chains/interview_chain.py`, `chains/evaluation_chain.py`)
- **Question Generation**: Formulates role-relevant technical questions parameterized by candidate skills and past question history to avoid repetition. Assigns difficulty (`EASY`, `MEDIUM`, `HARD`).
- **Answer Evaluation**: Multi-dimensional scoring on candidate responses:
  - Overall Score (0–10)
  - Technical Accuracy (0–10)
  - Clarity (0–10)
  - Identified Strengths, Critical Weaknesses, and Actionable Improvements
  - Synthesizes a high-scoring **Ideal Exemplar Answer**.
- Tracks aggregate interview statistics (total score, running average score, questions completed).

### 3.5 Resume Rewriter & HTML Formatter (`chains/rewrite_chain.py`, `chains/format_chain.py`)
- **Rewriter**: Accepts target job title and job description; restructures candidate history using the Google XYZ formula (*"Accomplished [X] as measured by [Y], by doing [Z]"*) to align with target role keywords.
- **HTML Formatter**: Compiles the structured resume into a self-contained, responsive, printable HTML document previewed directly in Streamlit and downloadable as `.html`.

---

## 4. Repository Structure

```plaintext
ai-resume-interview-agent/
│
├── app.py                     # Streamlit application entry point & UI orchestration
├── requirements.txt           # Python dependency definitions
├── .env.example               # Template for required environment variables
├── flow.md                    # Detailed architecture diagrams & LCEL sequence flows
├── todo.md                    # Project roadmap and checklist
├── PROJECT_OVERVIEW.md        # Concise project overview document (this file)
│
├── chains/                    # LangChain LCEL execution chains & Pydantic schemas
│   ├── ats_chain.py           # ATS scoring and gap analysis
│   ├── skill_chain.py         # 8-domain skill taxonomy extractor
│   ├── interview_chain.py     # Contextual question generator
│   ├── evaluation_chain.py    # Answer evaluation & feedback rubric
│   ├── rewrite_chain.py       # Resume restructuring & keyword tailoring
│   └── format_chain.py        # Clean HTML resume renderer
│
├── prompts/                   # Decoupled Markdown prompt repositories
│   ├── prompt_reader.py       # Prompt file loader utility
│   ├── ats_prompt.md          # ATS evaluation instructions
│   ├── skills_prompt.md       # Skill taxonomy extraction instructions
│   ├── interview_prompt.md    # Technical interviewer persona
│   ├── evaluation_prompt.md   # Scoring rubric & feedback formatting
│   ├── rewrite_prompt.md      # Resume rewriting guidelines (XYZ format)
│   └── format_prompt.md       # HTML styling & typography specifications
│
├── services/                  # Preprocessing & file extraction services
│   ├── pdf_parser.py          # PyMuPDF text reader
│   ├── resume_extractor.py    # Regex text cleaning
│   └── skill_extractor.py     # Skill helper definitions
│
├── utils/                     # Helper utilities
│   ├── formatting.py          # Output styling helpers
│   └── scoring.py             # Score computation logic
│
├── agents/                    # Future multi-agent orchestrator stubs
│   ├── ats_agent.py
│   ├── evaluatot_agent.py
│   ├── interviewer_agent.py
│   └── rewrite_agent.py
│
└── storage/                   # Future persistence stubs (MongoDB / Redis)
    ├── mongodb.py
    └── redis.py
```

---

## 5. Setup and Execution

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

### Installation Steps

1. **Clone / Navigate to repository**:
   ```bash
   cd ai-resume-interview-agent
   ```

2. **Configure virtual environment**:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-flash-latest
   ```

5. **Launch the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 6. Current Implementation Status & Roadmap

- [x] **In-Memory PDF Parsing**: Fast PyMuPDF document extraction.
- [x] **ATS Analysis Pipeline**: Scoring, gap analysis, and keyword matching.
- [x] **Taxonomic Skill Extraction**: 8-category skill breakdown with confidence ratings.
- [x] **Interactive Mock Interview**: Multi-question session state with real-time feedback.
- [x] **Resume Rewriting & HTML Export**: Target role tailoring and downloadable HTML.
- [x] **Model Fallbacks & Resilience**: Automatic retries on rate limits (429/503) with fallback models.
- [ ] **Persistent Storage**: Integration of Redis / MongoDB for interview session history and resume profiles.
- [ ] **Autonomous Multi-Agent Architecture**: Full migration from linear chains to decoupled agent orchestrators in `agents/`.
