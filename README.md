# ⚖️ AI Recruitment Bias Auditor

A production-ready Streamlit web app that detects bias in job descriptions, 
rewrites them into inclusive language, and audits hiring pipeline fairness 
using the EEOC 80% Disparate Impact Rule.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Bias Detection | Scans job descriptions for 40+ gender, age, and exclusionary phrases |
| ✍️ Inclusive Rewrite | Rule-based rewrite engine that replaces biased language with neutral alternatives |
| 📊 Fairness Dashboard | Selection rate charts + Intersectionality Analysis + Disparate Impact Ratio |
| 📥 Export | Download rewritten JDs and full fairness reports as CSV |

---

## 🚀 Run Locally

### 1. Prerequisites
- Python 3.9 or higher
- pip

### 2. Clone / download the project
```bash
git clone https://github.com/YOUR_USERNAME/ai-bias-auditor.git
cd ai-bias-auditor
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📤 Upload to GitHub

```bash
# Initialise git (if not already)
git init

# Add all files
git add app.py requirements.txt README.md

# Commit
git commit -m "Initial commit: AI Recruitment Bias Auditor"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/ai-bias-auditor.git

# Push
git branch -M main
git push -u origin main
```

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Go to **https://share.streamlit.io** and sign in with GitHub
2. Click **"New app"**
3. Select your repository and set:
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**

Your app will be live at:  
`https://YOUR_USERNAME-ai-bias-auditor-app-XXXX.streamlit.app`

---

## 📁 Project Structure

```
ai-bias-auditor/
├── app.py            ← Main Streamlit UI frontend
├── requirements.txt  ← Python dependencies
├── README.md         ← This file
└── modules/          ← Extracted backend logic
    ├── bias_engine.py      ← NLP keyword scanning & rewrite rules
    ├── fairness_calc.py    ← Disparate impact & EEOC 80% algorithms
    ├── data.py             ← Sample datasets
    └── styles.py           ← Streamlit CSS overrides
```

---

## 📊 CSV Format for Hiring Data

Upload a CSV with these columns:

| Column | Type | Description |
|---|---|---|
| `gender` | string | e.g. Male, Female, Non-binary |
| `age_group` | string | e.g. 25-34, 35-44 (optional) |
| `applied` | int | Total applicants in group |
| `shortlisted` | int | Applicants shortlisted |
| `hired` | int | Applicants hired |

A sample dataset is built into the app (click "Use Sample Dataset").

---

## 🧠 How Bias Detection Works

- **40+ curated phrases** across gender-coded, age-coded, and exclusionary language
- Each phrase tagged with severity: `high / medium / low`
- Score aggregated: 3+ high → HIGH BIAS, 1 high or 2+ medium → MEDIUM BIAS
- Highlighted inline with colour-coded spans

## ⚖️ Fairness Metric

Disparate Impact Ratio = Group Hire Rate ÷ Highest Group Hire Rate

A ratio **below 0.80** triggers the EEOC adverse impact flag (80% Rule).

---

Built with ❤️ for fair hiring · Powered by Python + Streamlit
