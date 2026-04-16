# ⚖️ AI Recruitment Bias Auditor
**Team TR-096-ALTERIX**  
*Submitted for the Tensor'26 Hackathon*

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![Fairness](https://img.shields.io/badge/AI_Ethics-Bias_Detection-success.svg)

An advanced, production-ready Streamlit web application designed to automatically detect hidden bias in job descriptions, surgically rewrite them into inclusive language, and meticulously audit hiring pipelines using the EEOC 80% Disparate Impact Rule.

---

## ✨ Standout Features

### 1. 🔍 Advanced Bias Detection
- Scans job descriptions (TXT, PDF, DOCX) for over 40+ gender-coded, ageist, and exclusionary industry phrases.
- Multi-tier severity tagging (`High`, `Medium`, `Low`) to provide clear impact scoring for HR teams.

### 2. ✍️ AI-Powered Inclusive Rewrite Engine
- A highly accurate rule-based replacement engine dynamically substitutes exclusionary phrases with welcoming, neutral alternatives.
- **Copy/Export Ready:** Seamlessly copy the optimized text to your clipboard or download a fully formatted PDF directly from the interface.

### 3. 📊 DEI Fairness Dashboard
- Tracks demographic disparities and selection rates across your entire historical hiring pipeline.
- Interactive **Plotly** data visualizations mapping intersectionality analysis.
- Live disparate impact metrics dynamically flagging groups that fall under the federal 80% threshold.

### 4. 🍏 Premium Apple-Inspired UI/UX
- A completely custom CSS engine overriding the native Streamlit UI.
- Features a pristine minimalist aesthetic: San Francisco typography, soft glassmorphism card elevations, sleek hover micro-animations, and pure white native components.

---

## 🛠 Tech Stack
- **Frontend/Framework:** Streamlit (with custom injected Apple-themed CSS and interactive JS DOM manipulations) 
- **Data Engineering:** Pandas, Python 3
- **Visualization:** Plotly
- **Document Processing:** PyPDF2 (PDF parsing), python-docx (Word parsing), FPDF2 (PDF generation)

---

## 🚀 Run it Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yuvaxtech/TR-096-ALTERIX.git
cd TR-096-ALTERIX
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Auditor
```bash
streamlit run app.py
```
*The app will automatically open in your browser at **http://localhost:8501***.

---

## 📁 Project Structure

```
TR-096-ALTERIX/
├── app.py            ← Main Streamlit User Interface & Flow logic
├── requirements.txt  ← Environment dependencies
├── README.md         ← Project documentation
└── modules/          ← Modularized backend logic structure
    ├── bias_engine.py      ← NLP keyword scanning & rewrite rules definitions
    ├── fairness_calc.py    ← Disparate impact & EEOC 80% mathematical models
    ├── data.py             ← Synthetic sample datasets for testing
    └── styles.py           ← Bulletproof custom CSS overrides & DOM styling
```

---

## 🗂 CSV Format for Dashboard Analytics

To analyze historical data, upload a CSV structured as follows:

| Column | Type | Description |
|---|---|---|
| `gender` | string | Demographic class (e.g., Male, Female) |
| `age_group` | string | Age classification (e.g., 25-34, 35-44) |
| `applied` | int | Total candidate volume in group |
| `shortlisted` | int | Total candidates advancing to interview |
| `hired` | int | Total candidates officially hired |

*(A verified sample dataset is built directly into the app so you can test it instantly!)*

---

*Built with ❤️ for fair, transparent, and unbiased hiring.*
