# BrandDistinct



**BrandDistinct** is an AI-powered brand evaluation platform that measures how well content reflects a brand's unique identity. It helps marketers, content creators, and businesses validate brand consistency, identify generic messaging, and generate improved brand-aligned content using AI.

---

## Problem Statement

Many AI-generated marketing materials sound generic and fail to capture a brand's unique voice, personality, and values. BrandDistinct AI solves this problem by analyzing content against a structured Brand DNA framework and providing measurable brand distinctiveness scores, evidence-based insights, and AI-generated improvements.

---

## Key Features

* Brand DNA extraction from company websites
* Brand Distinctiveness Scoring Framework (BDSF)
* AI-powered content evaluation using Claude
* Genericness detection and penalty scoring
* Evidence-based brand alignment analysis
* Content rewriting and optimization recommendations
* Interactive evaluation dashboard

---

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* Axios

### Backend

* FastAPI
* Python 3.11+
* Pydantic
* Anthropic Claude API

### AI Components

* Claude for Brand DNA extraction
* Claude for relevance validation
* Claude for content evaluation
* Claude for content rewriting

---

## Prerequisites & Requirements

Before running the project, ensure the following are installed:

### Required Software

* Python 3.11 or later
* Node.js 18 or later
* npm 9 or later
* Git

### Operating Systems

* Windows 10/11
* Linux
* macOS

### Required API Keys

* Anthropic Claude API Key

Create a `.env` file inside the backend directory:

```env
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-5
```

---

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/navathara/branddistinct.git
cd branddistinct
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

---

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Usage Examples

### 1. Brand Discovery

Enter a company website URL:

```text
https://www.python.org
```

The system extracts:

* Brand Identity
* Personality
* Communication Style
* Audience
* Visual Identity
* Values

---

### 2. Content Evaluation

Submit content such as:

```text
Python empowers developers to turn ideas into working software quickly through its clean, readable, and intuitive syntax.
```

The system returns:

```text
Overall Score: 70/100
Identity Alignment: 88
Distinctiveness: 82
Consistency: 62
Audience Resonance: 82
Values Alignment: 85
```

along with evidence, recommendations, and genericness analysis.

---

### 3. Content Rewriting

The Rewrite Engine automatically generates a more brand-aligned version of the content using Claude.

Example:

```text
Original:
Python is a good programming language.

Rewritten:
Python empowers developers with a simple yet powerful platform for building innovative solutions across web development, AI, automation, and data science.
```

---

## AI Architecture

### Claude-Based Pipeline

1. Brand Discovery

   * Extract Brand DNA from website content

2. Relevance Validation

   * Check whether submitted content is relevant to the brand

3. Content Evaluation

   * Evaluate content across six Brand DNA dimensions

4. Deterministic Scoring

   * Calculate BDSF scores
   * Apply genericness penalties
   * Generate confidence metrics

5. Content Rewriting

   * Generate improved brand-aligned content

---

## License Information

This project is licensed under the **MIT License**.

See the full license here:

```text
LICENSE
```
