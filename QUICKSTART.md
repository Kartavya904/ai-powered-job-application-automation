# Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Git
- GPU (optional, for faster AI model training)

## Installation

### Windows (PowerShell)

```powershell
# Run the setup script
.\setup_environment.ps1
```

### Linux/Mac

```bash
# Make script executable
chmod +x setup_environment.sh

# Run the setup script
./setup_environment.sh
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Initial Setup

### 1. Add Your Documents

Place your personal documents in the `data/` directory:
- Resume (PDF or DOCX): `data/resume.pdf`
- Transcripts, project descriptions, etc.
- These files will be parsed and embedded for semantic search

### 2. Configure Your Preferences

Edit `config.yaml` to set:
- Target job titles
- Location preferences
- Remote work preference
- Visa sponsorship requirements
- AI model settings

### 3. Add Target Companies

Edit `data/company_list.csv` with your target companies:
```csv
Name,URL,Completed
Google,https://careers.google.com/jobs,false
Microsoft,https://careers.microsoft.com/us/en,false
```

### 4. Embed Your Documents

Run the embedding script to create vector embeddings of your profile:

```bash
python scripts/embed_personal_docs.py
```

This will:
- Parse all documents in `data/`
- Create `data/profile.json`
- Generate vector embeddings
- Save to `models/faiss_index.bin`

### 5. Train Fit Model (Optional)

For now, the system uses vector similarity for fit scoring. To train a custom classifier:

```bash
python scripts/train_fit_model.py
```

Note: This requires labeled training data (job descriptions with your fit scores).

## Next Steps

The following components are still to be implemented:
- **Phase 1**: Job search automation (Playwright scripts)
- **Phase 2**: AI fit scoring and ranking
- **Phase 3**: Form auto-fill automation
- **Phase 4**: System tray UI
- **Phase 5**: Credential vault and database

## Project Structure

```
project_root/
├── automation/          # Browser automation scripts (to be implemented)
├── data/                # Your personal documents
├── logs/                # Application logs
├── models/              # AI models and embeddings
├── scripts/             # Core scripts (parsing, embedding, etc.)
├── ui/                  # System tray UI (to be implemented)
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Troubleshooting

### Import Errors

If you get import errors, make sure:
1. Virtual environment is activated
2. All dependencies are installed: `pip install -r requirements.txt`
3. You're running scripts from the project root directory

### Playwright Issues

If Playwright browsers aren't installed:
```bash
playwright install
```

### GPU Support

For faster embeddings, install GPU-enabled versions:
```bash
# Uninstall CPU version
pip uninstall faiss-cpu

# Install GPU version (requires CUDA)
pip install faiss-gpu
```

## Support

For issues or questions, please open an issue in the repository.

