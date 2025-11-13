# Automated AI-Powered Job Application Filler (Local, Offline)

## 🚀 Overview
This project is an intelligent, fully offline system designed to automate job applications. It leverages locally trained AI models, vector search, and browser automation to scan job boards, filter for eligibility, rank job descriptions, and auto-fill application forms.

- **Fully local and cost-free**: No reliance on OpenAI or external APIs
- **AI-driven**: Intelligent filtering and ranking
- **Multi-platform**: Cross-browser automation using Playwright
- **Secure**: Encrypted credential storage
- **Customizable**: Tray utility for real-time control and config

---

## 📁 Directory Structure
```bash
project_root/
├── automation/           # Playwright scripts & browser logic
├── config.yaml           # All filter, threshold, and runtime parameters
├── data/                 # Personal files (resumes, transcripts, projects)
│   ├── resume.pdf
│   ├── company_list.csv
│   └── ...
├── docs/                 # Projectplan.txt and other design docs
├── logs/                 # All logs and error screenshots
├── models/               # Trained AI models and embeddings
├── scripts/              # One-off training or indexing scripts
├── ui/                   # System tray application (PyQt/Go)
├── applied_jobs.db       # SQLite DB for persistent application tracking
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🛠️ Features
- **🧠 Local AI Models**: Semantic match between job descriptions and your profile
- **🔍 Intelligent Filtering**: Hard-coded + ML-based job eligibility filters
- **🧾 Form Automation**: Multi-step form support with resume upload and dynamic inputs
- **🔐 Secure Storage**: Local encrypted config and credential management
- **🖥️ Tray UI**: Monitor status, change filters, review ambiguous jobs

---

## ✅ Requirements
- Python 3.10+
- Playwright (`pip install playwright` + `playwright install`)
- GPU support for training (CUDA, etc.)
- Optional: SQLite3, PyQt5 (for tray UI)

---

## 🧪 Usage
```bash
# Step 1: Clone Repo
$ git clone https://github.com/yourname/auto-job-filler
$ cd auto-job-filler

# Step 2: Install Environment
$ pip install -r requirements.txt
$ playwright install

# Step 3: Run Setup Scripts
$ python scripts/embed_personal_docs.py
$ python scripts/train_fit_model.py

# Step 4: Start Tray & Automation
$ python ui/tray_app.py
```

---

## 📋 Configuration
- `config.yaml`: Control job filters, resume paths, and thresholds
- `company_list.csv`: Company name, careers URL, completion flag
- `secrets.yaml`: Encrypted credentials (loaded at runtime)

---

## 📈 Logs and Monitoring
- Logs are saved to `logs/run.log`
- Application screenshots saved on each attempt
- Failed jobs logged with exception stack

---

## 💡 Future Roadmap
- Auto-update company list via job board scraping
- Resume generator using LLMs
- Feedback learning loop (improve model with rejections)

---

## 📜 License
MIT License

---

## 🙋 Contact
Developed by Kartavya | Reach out via issues or discussions in the repository

