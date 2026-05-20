# GitHub Codespace Setup Guide
# RAG From Scratch Seminar

---

## PART 1 — CREATE AND PUBLISH THE REPO

### Step 1: Create the GitHub repo

```bash
# On your local machine (or any terminal with git + gh CLI):

# 1. Create a new directory and initialise git
mkdir rag-from-scratch
cd rag-from-scratch
git init

# 2. Create on GitHub using the GitHub CLI
gh repo create rag-from-scratch \
  --public \
  --description "Build a complete RAG system from scratch — seminar repo" \
  --clone

# OR if you prefer the website:
# Go to github.com → New Repository → Name: rag-from-scratch → Public → Create

# 3. After Cursor builds the repo files, push everything:
git add .
git commit -m "feat: initial RAG seminar repo"
git branch -M main
git push -u origin main
```

---

## PART 2 — GETTING API KEYS

### Gemini API Key (Primary — embeddings + generation)

**Where:** https://aistudio.google.com

**Steps:**
```
1. Go to aistudio.google.com
2. Sign in with any Google account
3. Click "Get API key" in the left sidebar
4. Click "Create API key in new project"
5. Copy the key (looks like: AIzaSy...)
```

**Free tier limits (as of 2026):**
- Gemini 2.5 Flash: 10 req/min, 250 req/day
- Gemini Flash-Lite: 15 req/min, 1,000 req/day
- No credit card required. No expiry.

**Note for EU attendees:** The Gemini free tier cannot serve EU/EEA users.
Use Groq as your primary instead.

---

### Groq API Key (Fast generation fallback)

**Where:** https://console.groq.com

**Steps:**
```
1. Go to console.groq.com
2. Sign up with Google, GitHub, or email (no credit card)
3. Click "API Keys" in the left sidebar
4. Click "Create API key"
5. Give it a name (e.g. "rag-seminar")
6. Copy the key (looks like: gsk_...)
```

**Free tier limits:**
- 30 req/min, 14,400 req/day
- llama-3.3-70b-versatile, Llama 4 Scout, and more
- No credit card required. No expiry.

---

### Cohere API Key (Neural reranking)

**Where:** https://dashboard.cohere.com

**Steps:**
```
1. Go to dashboard.cohere.com
2. Sign up with email, Google, or GitHub (no credit card)
3. Your trial key is AUTO-GENERATED on signup
4. Click "API Keys" in the sidebar
5. Copy the key (looks like: AbCdEf...)
```

**Free tier limits:**
- 1,000 API calls/month across ALL endpoints
- Includes: Rerank 3.5, Embed 4, Command R+
- Resets monthly. No expiry. Non-commercial only.

---

## PART 3 — OPEN IN CODESPACE

### Option A: One-click (after repo is published)

Click the Codespace badge in the README:
```
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR_USERNAME/rag-from-scratch?quickstart=1)
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Option B: From the GitHub repo page

```
1. Go to your repo on github.com
2. Click the green "Code" button
3. Click "Codespaces" tab
4. Click "Create codespace on main"
5. Wait ~3 minutes for setup to complete
```

### Option C: Direct URL

```
https://codespaces.new/YOUR_USERNAME/rag-from-scratch
```

---

## PART 4 — ADDING API KEYS TO CODESPACE

### Method 1: In the .env file (easiest for attendees)

After the Codespace opens, edit the `.env` file:

```bash
# In the Codespace terminal:
nano .env

# Or open .env in the VS Code editor and paste your keys:
GEMINI_API_KEY=AIzaSy_your_key_here
GROQ_API_KEY=gsk_your_key_here
COHERE_API_KEY=your_cohere_key_here
```

Save and verify:
```bash
make keys
```

### Method 2: GitHub Codespace secrets (recommended for instructors)

This pre-loads your keys into every Codespace you create:

```
1. Go to github.com/settings/codespaces
2. Click "New secret"
3. Name: GEMINI_API_KEY  Value: your_key
4. Repeat for GROQ_API_KEY and COHERE_API_KEY
5. Under "Repository access" → select your rag-from-scratch repo
```

Now every Codespace you open will have the keys automatically.

---

## PART 5 — VERIFY SETUP AND START

```bash
# Check what's available
make keys

# Expected output:
# ┌─────────────────────────────────────────────────────────┐
# │ RAG Seminar Configuration                               │
# ├──────────────┬────────────────┬────────────────────────-┤
# │ Gemini API   │ gemini-2.5...  │ ✓ Available             │
# │ Groq API     │ llama-3.3...   │ ✓ Available             │
# │ Cohere API   │ rerank-engl... │ ✓ Available             │
# │ Embeddings   │ text-embed...  │ API                     │
# │ Chunk size   │ 512            │                         │
# └──────────────┴────────────────┴─────────────────────────┘

# Start Jupyter for code-along
make nb
# → Opens Jupyter on port 8888 (VS Code will show a popup to open in browser)

# Start the Gradio app
make app
# → Opens Gradio on port 7860 (VS Code will show a popup to open in browser)

# Run all fallback scripts (no notebook needed)
make test

# Run RAGAS evaluation on SQuAD
make eval
```

---

## PART 6 — SHARING WITH ATTENDEES

Give attendees this URL to fork and open in their own Codespace:

```
https://github.com/YOUR_USERNAME/rag-from-scratch
```

Attendee flow (5 minutes total):
```
1. Go to the repo URL
2. Click "Fork" → creates their own copy
3. Click "Code" → "Codespaces" → "Create codespace on main"
4. Wait 3 minutes for auto-setup
5. Open .env → paste their API keys
6. Run: make keys → verify
7. Run: make nb → start Jupyter
8. Open notebooks/01_ingestion.ipynb → begin
```

---

## PART 7 — COMMANDS REFERENCE

```bash
# ── Setup ──────────────────────────────────────────────────
make setup          # Install UV + all deps + download data
make keys           # Show which API keys are configured
make download       # Re-download SQuAD data

# ── Development ────────────────────────────────────────────
make nb             # Start Jupyter (port 8888)
make app            # Start Gradio UI (port 7860)

# ── Testing ────────────────────────────────────────────────
make test           # Run all 5 fallback .py scripts
make eval           # Run RAGAS evaluation on SQuAD subset

# ── Maintenance ────────────────────────────────────────────
make clean          # Delete ChromaDB + cached data
uv add PACKAGE      # Add a new dependency
uv sync             # Re-sync after pyproject.toml changes

# ── Direct script execution ────────────────────────────────
uv run python scripts/01_ingestion.py
uv run python scripts/02_retrieval.py
uv run python scripts/03_generation.py
uv run python scripts/04_evaluation.py
uv run python scripts/05_advanced.py
uv run python scripts/run_all.py       # All at once

# ── Individual module testing ───────────────────────────────
uv run python -c "from src.config import print_config; print_config()"
uv run python -c "from src.utils.fallback import get_llm; print(get_llm())"
```

---

## PART 8 — TROUBLESHOOTING

### "UV not found"
```bash
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.bashrc
```

### "No kernel found" in Jupyter
```bash
uv run python -m ipykernel install --user --name=rag-seminar --display-name="RAG Seminar (Python 3.11)"
# Then restart Jupyter and select the "RAG Seminar" kernel
```

### "Rate limit exceeded" (429 error)
The system has exponential backoff built in. If you hit limits during the seminar:
- Switch to Groq (faster limit recovery)
- Reduce eval sample size in .env: EVAL_SAMPLE_SIZE=5
- Use local models: leave all API keys empty

### "ChromaDB collection already exists"
```bash
make clean    # Deletes .chroma_db
make test     # Rebuilds from scratch
```

### "Port already in use"
```bash
# Find and kill the process
lsof -i :7860
kill -9 <PID>
```

### EU users: Gemini not working
Set Groq as primary in `.env`:
```bash
GEMINI_API_KEY=      # leave empty
GROQ_API_KEY=gsk_your_key
# The system automatically falls back to Groq for generation
# And uses local sentence-transformers for embeddings
```
