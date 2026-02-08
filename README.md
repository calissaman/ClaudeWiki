# ClaudeWiki

AI-powered answers backed by Wikipedia, using Claude and the MediaWiki API.

![Claude](https://img.shields.io/badge/Claude-Haiku%204.5-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Wikipedia-backed answers**: Claude searches Wikipedia to provide accurate, sourced information
- **Inline citations**: All answers include hyperlinks to Wikipedia sources
- **Safety guardrails**: Built-in protections for harmful content, misinformation, and sensitive topics
- **Evaluation suite**: 70 test cases across 7 dimensions with detailed scoring rubrics
- **Claude branding**: Clean UI with official Claude colors and Inter font

---

## Table of Contents

1. [Installation](#installation)
2. [Running the Website](#running-the-website)
3. [Demo Mode](#demo-mode-no-api-key-required)
4. [Evaluation Suite](#evaluation-suite)
5. [Project Structure](#project-structure)
6. [Development Tools](#development-tools)
7. [How It Works](#how-it-works)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [License](#license)
11. [Credits](#credits)

---

## Installation

### Step 1: Prerequisites

Ensure you have the following installed:

- **Python 3.8 or higher**
  ```bash
  python3 --version
  ```

- **pip** (Python package manager)
  ```bash
  pip --version
  ```

### Step 2: Clone or Download the Project

```bash
git clone <repository-url>
cd wikipedia-tool
```

Or download and extract the ZIP file, then navigate to the directory.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install anthropic requests flask
```

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | latest | Claude API client |
| `requests` | latest | HTTP requests to Wikipedia |
| `flask` | latest | Web server |

### Step 4: Get an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in to your account
3. Add billing credits (required for API access)
4. Navigate to **API Keys** in the sidebar
5. Click **Create Key**
6. Copy the key (starts with `sk-ant-api03-...`)

### Step 5: Set Your API Key

**Option A: Environment variable (recommended)**

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"
```

To make it permanent, add to your shell config:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Option B: Create a .env file**

```bash
echo 'ANTHROPIC_API_KEY=sk-ant-api03-your-key-here' > .env
```

---

## Running the Website

### Start the Server

```bash
python3 app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Access the Website

Open your browser and navigate to: **http://localhost:5000**

### Using ClaudeWiki

1. Type your question in the search box
2. Click **Ask Claude** or press Enter
3. Wait for Claude to search Wikipedia and generate an answer
4. View the response with inline Wikipedia citations
5. Check the logs section to see which Wikipedia articles were retrieved

### Sample Queries to Try

| Query | What it demonstrates |
|-------|---------------------|
| "Who invented the telephone?" | Historical facts with multiple contributors |
| "What is the population of Japan?" | Current statistics and data |
| "When did World War 2 end?" | Historical events with precise dates |
| "Who is Marie Curie?" | Biographical information |
| "What is climate change?" | Scientific topics with balanced viewpoints |
| "Is the Earth flat?" | Misinformation handling and correction |

---

## Demo Mode (No API Key Required)

Want to see how the Wikipedia API integration works without setting up an Anthropic API key? Try demo mode!

### Quick Test

```bash
python3 demo.py --quick
```

This verifies the Wikipedia API connection is working and shows a simple search example.

### Full Demo

```bash
python3 demo.py
```

This runs through several sample Wikipedia searches and shows exactly what data Claude would receive, including:
- Wikipedia API calls and responses
- Article content and URLs
- Search result formatting
- How tool calls are structured

### What Demo Mode Shows

Demo mode demonstrates:
- ✅ How Wikipedia searches are performed
- ✅ What data is retrieved from Wikipedia articles
- ✅ How results are formatted and structured
- ✅ Sample queries across different topics

**Note**: Demo mode only shows the Wikipedia search functionality. To experience the full ClaudeWiki tool with AI-powered answers, you'll need to:

1. Set your Anthropic API key (see [Installation](#installation))
2. Run the full application: `python3 app.py`
3. Open http://localhost:5000 in your browser

The full tool provides intelligent question understanding, multi-article synthesis, inline citations, and conversational follow-ups.

---

## Evaluation Suite

ClaudeWiki includes a comprehensive evaluation suite with **70 test cases** across **7 dimensions**.

### Evaluation Dimensions

| # | Dimension | Description | Cases |
|---|-----------|-------------|-------|
| 1 | Factual Accuracy | Correct retrieval and accurate facts | 10 |
| 2 | Faithfulness | Claims grounded in Wikipedia sources | 10 |
| 3 | Helpfulness | Structure, clarity, unit conversions, multi-hop | 10 |
| 4 | Conversational | Disambiguation and follow-up handling | 10 |
| 5 | Misinformation | False belief correction, bias handling | 10 |
| 6 | Safety | Harmful request refusal, jailbreak resistance | 10 |
| 7 | Multilingual | Non-English queries and edge cases | 10 |

### Running the Evaluation Suite

**Prerequisites**: The ClaudeWiki server must be running in another terminal.

```bash
# Terminal 1: Start the server
export ANTHROPIC_API_KEY="your-key-here"
python3 app.py

# Terminal 2: Run the evaluation
python3 run_eval.py --all --judge heuristic
```

### Evaluation Commands (run_eval.py)

```bash
# Run all 70 tests with heuristic scoring
python3 run_eval.py --all --judge heuristic

# Run a specific dimension with verbose output
python3 run_eval.py --dimension D3 --verbose

# Run a specific question type with model judge
python3 run_eval.py --question-type Q4 --judge model --judge-model claude-sonnet-4-5-20250929

# Combine dimension and question-type filters
python3 run_eval.py --dimension D1 --question-type Q3 --verbose

# Limit to first N tests after filtering
python3 run_eval.py --dimension D6 --limit 5 --verbose

# Save per-test results as JSONL
python3 run_eval.py --all --judge model --out results.jsonl
```

### Eval Suite Utilities (eval_suite.py)

```bash
# List all test cases
python3 eval_suite.py --list

# View scoring rubrics for each dimension
python3 eval_suite.py --rubrics

# Print distribution summary
python3 eval_suite.py
```

### Understanding Results

Each test case is scored 1-5 based on dimension-specific rubrics:

| Score | Meaning |
|-------|---------|
| 5 | Excellent - meets all criteria |
| 4 | Good - minor issues only |
| 3 | Acceptable - usable but has gaps |
| 2 | Poor - significant problems |
| 1 | Fail - critical issues or red flags |

**Pass criteria**: Score ≥ 3 AND no red flags detected

### Sample Output

```
======================================================================
[d1_001] PASS (Score: 5/5)
Dimension: Factual Accuracy & Retrieval Relevance
Query: What year did World War 2 end?
----------------------------------------------------------------------
Response: Based on Wikipedia, **World War 2 ended in 1945**...

Verification passed: ['1945', 'September', 'May']
Verification failed: []

Rationale: Basic historical fact with precise dates.
```

---

## Project Structure

```
wikipedia-tool/
├── app.py                          # Main Flask application with Claude integration
├── eval_suite.py                   # Evaluation suite (70 cases, 7 dimensions)
├── run_eval.py                     # Test runner for evaluation suite
├── demo.py                         # Demo mode (no API key required)
├── requirements.txt                # Python dependencies
├── .env                            # API key storage (create this yourself)
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── EVALUATION_RESULTS.md           # Test results and performance analysis
├── SUBAGENT_CODE_REVIEWER.md       # Code review subagent documentation
├── SUBAGENT_PROJECT_MANAGER.md     # Project verification subagent documentation
└── static/                         # Web UI files
    ├── index.html                  # Main HTML page
    ├── style.css                   # CSS styling (Claude colors, Inter font)
    └── app.js                      # Frontend JavaScript
```

---

## Development Tools

This project includes documentation for specialized AI subagents used during development to ensure code quality and project consistency.

### Code Reviewer Subagent

**File:** `SUBAGENT_CODE_REVIEWER.md`

The code reviewer subagent performs comprehensive code reviews and identifies improvement opportunities. During development, it reviewed `demo.py` and provided 10 actionable suggestions:

1. **Constants for Magic Numbers** - Replace hardcoded values with named constants
2. **Separate Data Fetching from Display** - Split concerns for better testability
3. **Type Hints** - Add type annotations using `typing` module
4. **Specific Error Handling** - Catch specific exceptions (Timeout, ConnectionError)
5. **Input Validation** - Add dedicated validation with clear error messages
6. **Progress Indicators** - Visual feedback (⏳/✅/❌) for better UX
7. **DRY Principle** - Extract repeated code into reusable functions
8. **Version Information** - Add `__version__` constant for tracking
9. **Better Exception Handling** - Handle KeyboardInterrupt and EOFError gracefully
10. **Enhanced Documentation** - Improve docstrings with examples

**Key Focus Areas:**
- Code quality and Python best practices (PEP 8, type hints)
- Performance optimizations and error handling
- Security considerations and input validation
- Maintainability (DRY principle, clear structure)
- User experience (progress indicators, helpful messages)

**How to Use:**
```python
# Using Claude Code CLI
Task(
    subagent_type="general-purpose",
    description="Review code for quality",
    prompt="Perform comprehensive code review focusing on best practices..."
)
```

### Project Manager Subagent

**File:** `SUBAGENT_PROJECT_MANAGER.md`

The project manager subagent verifies project structure, ensures documentation accuracy, and validates consistency between documentation and implementation.

**Verification Tasks:**
- ✅ Verify all files mentioned in README.md exist
- ✅ Check file descriptions match actual content
- ✅ Validate directory structure matches documentation
- ✅ Ensure evaluation suite documentation (70 cases) matches implementation
- ✅ Verify version consistency across files
- ✅ Identify missing or outdated documentation

**Example Verification Report:**
```
================================================================================
PROJECT MANAGER VERIFICATION REPORT
================================================================================

Files Verified: 12
✅ Found: 12
❌ Missing: 0

Documentation Accuracy:
✅ All file descriptions match actual content
✅ Evaluation suite has 70 test cases as documented
✅ All code examples are accurate and runnable

Project Structure:
✅ Directory organization matches documentation
✅ Configuration files present (.env.example)
✅ Dependencies documented in README

OVERALL STATUS: ✅ PASS
================================================================================
```

**How to Use:**
```python
# Using Claude Code CLI
Task(
    subagent_type="general-purpose",
    description="Verify project structure",
    prompt="Verify all files in README.md exist and descriptions are accurate..."
)
```

### Benefits

Both subagents use the Claude Code Task tool to spawn specialized agents that autonomously:
- **Code Reviewer**: Improves code quality, catches bugs, ensures best practices
- **Project Manager**: Maintains documentation accuracy, prevents drift between docs and code

These tools were instrumental in ensuring the ClaudeWiki project maintains high quality code and accurate documentation throughout development.

---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│  ClaudeWiki │────▶│  Claude API │
│  Question   │     │   (Flask)   │     │  (Haiku 4.5)│
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Wikipedia  │
                                        │  Tool Call  │
                                        └──────┬──────┘
                                               │
                                               ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   Answer    │◀────│  MediaWiki  │
                    │ with Sources│     │     API     │
                    └─────────────┘     └─────────────┘
```

### Flow

1. User submits a question via the web interface
2. Flask sends the question to Claude API with the `wikipedia_search` tool definition
3. Claude decides to search Wikipedia and generates a `wikipedia_search` tool call
4. Flask calls the backend function `search_wikipedia(query)`, which makes two MediaWiki HTTP requests:
   - **Search:** `action=query&list=search` with `srlimit=3` to find the top 3 matching titles
   - **Extract:** `action=query&prop=extracts` with all titles joined, to batch-fetch intro paragraphs
5. Claude receives the retrieved content and synthesizes an answer with inline citations
6. User sees the formatted answer with clickable Wikipedia links

> **Note:** `MAX_API_CALLS` in `app.py` limits the number of Claude API turns (i.e., `client.messages.stream` calls / tool-use loops), not the number of MediaWiki HTTP requests. Each Claude turn that invokes the tool triggers the two-step MediaWiki process above.

### Key Components

- **Flask Backend**: Handles HTTP requests, Claude API integration, Wikipedia searches
- **Claude API**: Processes questions, decides when to search, synthesizes answers
- **MediaWiki API**: Provides Wikipedia article content
- **Frontend**: Clean UI for question input and answer display

---

## Configuration

### System Prompt

The system prompt in `app.py` controls Claude's behavior:

- **Harmful request handling**: Brief refusals without repeating dangerous terms
- **Misinformation correction**: Lead with truth, avoid echoing false claims
- **Controversial topics**: Balanced, multi-perspective responses
- **Formatting**: Inline hyperlinks, bold emphasis, sources section

#### Example System Prompt Guidelines

```python
SYSTEM_PROMPT = """You are a helpful virtual assistant with access to Wikipedia...

HANDLING HARMFUL REQUESTS:
- For requests involving violence, weapons, illegal drugs, self-harm methods, hacking:
  Decline briefly and pivot immediately to a helpful alternative.
- Do NOT repeat, name, or describe the harmful request in your refusal.

MISINFORMATION AND FALSE PREMISES:
- When a question contains a false premise: Lead with the truth immediately.
- Do NOT repeat the false claim, even to deny it.
- State what IS true, not what isn't.
"""
```

To customize, edit the `SYSTEM_PROMPT` variable in `app.py`.

> **Naming note:** The tool schema exposed to Claude is named `wikipedia_search` (see `WIKIPEDIA_TOOL` in `app.py`), but the system prompt text currently references `search_wikipedia(query: str)`. The backend Python function that implements the tool is also called `search_wikipedia(query)`. This is a small naming inconsistency between the tool schema name and the system prompt; the tool works correctly regardless because Claude uses the schema name.

### MediaWiki API

Wikipedia's API is free and open - **no authentication required**. The tool searches English Wikipedia by default and retrieves article introductions.

#### API Configuration

- **Endpoint**: `https://en.wikipedia.org/w/api.php`
- **Format**: JSON
- **Actions used** (two requests per tool call):
  1. `action=query&list=search&srlimit=3` - Find top 3 articles matching search terms
  2. `action=query&prop=extracts&exintro=1` - Batch-fetch intro paragraphs for those titles
- **User-Agent**: Required by Wikipedia (set in code)

#### Customization Options

To search other Wikipedia editions, modify the base URL in `app.py`:

```python
# English (default)
base_url = "https://en.wikipedia.org/w/api.php"

# Spanish
base_url = "https://es.wikipedia.org/w/api.php"

# Japanese
base_url = "https://ja.wikipedia.org/w/api.php"
```

---

## Troubleshooting

### "No module named 'anthropic'"

```bash
pip install anthropic requests flask
```

### "Address already in use" (Port 5000)

```bash
# Option 1: Kill existing process
fuser -k 5000/tcp

# Option 2: Use a different port (edit app.py)
# Change the last line to:
app.run(debug=False, port=5001)
```

### "API Error: Invalid API Key"

- Verify `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
- Check the key hasn't expired in [console.anthropic.com](https://console.anthropic.com)
- Ensure you have credits in your Anthropic account

### "Connection failed" when running eval suite

Make sure the ClaudeWiki server is running in another terminal:

```bash
# Terminal 1
python3 app.py

# Terminal 2
python3 eval_suite.py --verbose
```

### Evaluation suite shows 0 cases run

The API key is not set. Export it before running:

```bash
export ANTHROPIC_API_KEY="your-key-here"
python3 app.py
```

### Wikipedia API not responding

- Check your internet connection
- Wikipedia API might be experiencing downtime (rare)
- Verify the User-Agent header is set correctly

### Demo mode not working

Demo mode doesn't require an API key. If it fails:

```bash
# Check Python version (needs 3.8+)
python3 --version

# Ensure requests is installed
pip install requests

# Run with error output
python3 demo.py --quick
```

---

## License

MIT License - feel free to use and modify.

---

## Credits

- **Claude** by Anthropic - AI assistant
- **Wikipedia** - Knowledge source via MediaWiki API
- **Inter** font by Rasmus Andersson
- **Flask** - Web framework
- **Python** - Programming language

Built with ❤️ using Claude Code
