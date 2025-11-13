## Project Timeline: Automated AI-Powered Job Application Filler (Local)

### Overview
This file contains a comprehensive breakdown of the development of a fully local, autonomous job application filler using AI and automation tools. It includes:
- 300+ step timeline of actions broken down by hours
- Checkpoints for every major phase
- Milestones for completion

---

### Assumptions
- Project Duration: ~6-8 weeks (can be condensed or extended based on hours/day)
- Work Schedule: 4-6 focused hours/day assumed
- All work done locally with no OpenAI API
- GPU available for AI training

---

### Phase 0: Planning and Setup (Hours 1–20)

**Hour 1–3**: Project Scaffolding
- Set up `git` repository and GitHub repo
- Create folders: `/data`, `/scripts`, `/models`, `/ui`, `/automation`, `/logs`, `/docs`
- Create and commit `README.md`, `projectplan.txt`, `.gitignore`, and `requirements.txt`

**Hour 4–5**: Dependency Identification
- List all required Python/Rust/Go libraries
- Draft `environment.yaml` for Python virtualenv
- Install and test core packages: PyTorch, Transformers, Playwright, FAISS

**Hour 6–8**: Define Project Configs
- Draft `config.yaml` structure: job preferences, resume selection, thresholds
- Design CSV schema: `company_list.csv` with columns: Name, URL, Completed

**Hour 9–12**: Document Parsing Setup
- Write parsers for: PDF (PyMuPDF), DOCX (`python-docx`), TXT/MD (vanilla Python), JSON
- Test parsing of static files
- Store parsed content into structured `profile.json`

**Hour 13–15**: Version Control Setup
- Commit all working scripts
- Set up `dev` and `main` branches
- Push to GitHub and validate clean structure

**Hour 16–20**: Vector DB & Embedding Infra
- Set up FAISS store
- Load sample resume sections into vector index
- Write embedding interface using Sentence Transformers

> ✅ **Checkpoint 1**: Basic folder structure, config, file parsing, vector DB working

---

### Phase 1: Job Search Automation (Hours 21–80)

**Hour 21–30**: Playwright Browser Automation
- Install and configure Playwright (headless and headful)
- Write script to open careers page from `company_list.csv`
- Implement retry, wait, and error handlers

**Hour 31–40**: Careers Site Interaction
- Navigate career pages
- Identify search/filter components (job title, location)
- Simulate filter inputs (hardcoded first)

**Hour 41–50**: Job Listings Parsing
- Extract job title, location, ID, link, description snippet
- Store into `jobs.json`
- Handle pagination, infinite scroll, and delays

**Hour 51–60**: Rules-Based Filtering Logic
- Parse config.yaml and apply:
  - Remote only toggle
  - Visa sponsorship phrases filter
  - Title/keyword match
- Output filtered jobs into `filtered_jobs.json`

**Hour 61–70**: Failure Handling & Logging
- Log file structure
- Screenshot on failure (Playwright)
- Retry logic with backoff (max 3)

**Hour 71–80**: Scheduling Logic
- Add input prompt for N jobs per run
- Implement company queue with "completed" flag in CSV
- Multi-tab resume on CAPTCHA encounter

> ✅ **Checkpoint 2**: Automation can visit site, apply filters, collect job listings

---

### Phase 2: AI Modeling and Training (Hours 81–160)

**Hour 81–90**: Document Chunking & Embeddings
- Create chunks by section/topic from resume/docs
- Embed into FAISS vector store
- Query test: "Give me projects with ML" – return matching blocks

**Hour 91–105**: Fit Score Classifier Prep
- Gather training data: job-desc ↔ match/no-match
- Format into supervised pairs
- Train a small BERT model to predict fit probability
- Evaluate accuracy and F1

**Hour 106–120**: Fit Scoring Pipeline
- For each filtered job:
  - Compare against embedded profile
  - Get AI fit score (0–10 scale)
- Mark scores <3 as skipped

**Hour 121–130**: Re-ranking System
- Sort all matched jobs by score
- Tiebreakers: Company priority, keyword weight

**Hour 131–145**: Ambiguity Prompts
- If score in [3–5], flag as ambiguous
- Open tab for user review or queue

**Hour 146–160**: AI Evaluation Scripts
- Model re-train script
- Embedding update script (run weekly)
- Visual inspection tool for fit scores

> ✅ **Checkpoint 3**: Intelligent filtering, AI scoring, re-ranking, ambiguity logic

---

### Phase 3: Application Filling Automation (Hours 161–230)

**Hour 161–170**: Resume/Cover Letter Selector
- Load multiple resume files
- Link resume config per role type
- Allow inline cover letter injection from user files

**Hour 171–190**: Form Auto-Fill Layer
- Create input matcher: field label → data type (email, name, etc.)
- Auto-fill fields using Playwright locators
- Upload files via input[type="file"] handlers

**Hour 191–210**: Multi-Step Forms
- Detect form progress (Next/Continue buttons)
- Wait for new fields
- Auto-submit on final step

**Hour 211–220**: CAPTCHA Detection
- If CAPTCHA detected:
  - Pause automation
  - Open new tab to continue
  - Notify via UI

**Hour 221–230**: Logging + Screenshots
- Capture application summary JSON
- Save screenshot after each submit
- Store under `logs/applications/{company_job_id}.json`

> ✅ **Checkpoint 4**: Auto-fill and resume submission works end to end

---

### Phase 4: User Tray Interface (Hours 231–280)

**Hour 231–240**: System Tray Design
- Create tray app using PyQt5 or Go (Tauri/Fyne optional)
- Add menu for Pause/Resume/Config

**Hour 241–255**: Settings GUI
- Edit preferences (job titles, cities, filters)
- Resume selector
- Save to `config.yaml`

**Hour 256–270**: Job History Viewer
- Display `applied_jobs.json`
- Highlight ambiguous/skipped/pending
- Allow manual "Apply Now"

**Hour 271–280**: Real-Time Status
- Show tooltip: "Currently applying to IBM – Job 3 of 20"
- Tray popup on error/CAPTCHA
- Optional: dark mode toggle

> ✅ **Checkpoint 5**: Tray UI fully functional with settings and control

---

### Phase 5: Finishing Touches (Hours 281–320)

**Hour 281–290**: Credential Vault
- Add local encryption using Fernet for secrets
- Prompt user for master password

**Hour 291–300**: Application History DB
- Switch to SQLite for applied job store
- Add query API: `was_applied(company, title)`

**Hour 301–310**: Documentation & Packaging
- Update `README.md`
- Add sample configs and demo video/gifs
- Zip installer script

**Hour 311–320**: Final Testing
- Dry run with mock listings
- Random edge-case jobs
- Prepare release build and tag

> ✅ **Final Checkpoint**: MVP complete, packaged, ready for use

---

### Optional Advanced Features (Post-MVP)
- Auto-company crawler (from Handshake or LinkedIn)
- Self-updating AI fit model
- Dynamic resume generator
- Interview scheduling AI

---

### Project Completion
Estimated Completion: 6–8 weeks of part-time development
MVP Timeline: ~300–320 hours of development

Total Deliverables:
- CLI + Tray UI
- 3–4 AI models (embedder, classifier, re-ranker)
- Full test coverage for major scripts
- Persistent job log & history
- Personal document embedding & dynamic updates

