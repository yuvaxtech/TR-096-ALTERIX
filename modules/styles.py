CUSTOM_CSS = """
<style>
/* ── Apple-inspired UI Tokens ── */
:root {
    --bg-color: #f2f2f7;
    --surface-color: rgba(255, 255, 255, 0.85);
    --surface-solid: #ffffff;
    --border-color: rgba(0, 0, 0, 0.15);
    --border-highlight: rgba(0, 0, 0, 0.25);
    --text-primary: #000000;
    --text-secondary: #3a3a3c;
    
    --accent-glow: transparent;
    --accent-primary: #0066cc;
    --accent-secondary: #34c759;
    
    --status-high-bg: rgba(255, 59, 48, 0.1);
    --status-high-color: #ff3b30;
    --status-medium-bg: rgba(255, 149, 0, 0.1);
    --status-medium-color: #ff9500;
    --status-low-bg: rgba(52, 199, 89, 0.1);
    --status-low-color: #34c759;

    --card-radius: 16px;
    --glass-blur: blur(20px);
}



/* ── Base ── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    letter-spacing: -0.015em;
}

.stApp {
    background: var(--bg-color) !important;
    color: var(--text-primary) !important;
    transition: background 0.3s ease;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Top Navigation/Stepper ── */
.stepper-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface-color);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-bottom: 1px solid var(--border-color);
    padding: 16px 24px;
    margin-bottom: 60px;
    position: sticky;
    top: 0;
    z-index: 999;
}
a.step-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 14px;
    color: var(--text-secondary);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    text-decoration: none !important;
    cursor: pointer;
}
a.step-item:hover {
    transform: translateY(-2px);
    color: var(--accent-primary) !important;
}
a.step-item:hover .step-number {
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    transform: scale(1.1);
}
.step-item.active {
    color: var(--text-primary);
}
.step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--surface-solid);
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
    font-size: 11px;
}
.step-item.active .step-number {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: white;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 60px 20px;
    margin-bottom: 20px;
    animation: fadeIn 0.8s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.hero h1 {
    font-size: 48px;
    font-weight: 700;
    line-height: 1.05;
    margin: 0 0 16px 0;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}
.hero p {
    color: var(--text-secondary);
    font-size: 18px;
    line-height: 1.5;
    max-width: 600px;
    margin: 0 auto;
    font-weight: 400;
}

/* ── Cards & Containers ── */
.glass-card {
    background: var(--surface-solid);
    border: 1px solid var(--border-color);
    border-radius: var(--card-radius);
    padding: 40px;
    margin-bottom: 40px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    animation: fadeInUp 0.6s ease both;
}
.glass-card:hover {
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.1);
    transform: translateY(-4px) scale(1.005);
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 0 0 32px 0;
}
.section-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    color: var(--text-primary);
}
.section-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.01em;
}

/* ── Streamlit Selectors Overrides ── */
.stTextArea textarea {
    background: var(--bg-color) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 15px !important;
    padding: 16px !important;
    transition: all 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2) !important;
}

.stButton > button, .stDownloadButton > button, [data-testid="baseButton-primary"] {
    background: var(--accent-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: scale(1.02) !important;
    opacity: 0.9 !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

.stFileUploader {
    background: var(--bg-color) !important;
    border: 1px dashed var(--border-color) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease;
}
.stFileUploader:hover {
    border-color: var(--text-secondary) !important;
}

/* ── Badges & Status Pills ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}
.badge-high   { background: var(--status-high-bg); color: var(--status-high-color); }
.badge-medium { background: var(--status-medium-bg); color: var(--status-medium-color); }
.badge-low    { background: var(--status-low-bg); color: var(--status-low-color); }

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin: 24px 0;
}
.metric-card {
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    transition: transform 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-highlight);
}
.metric-val {
    font-size: 40px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: -0.03em;
}
.metric-label {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
}

/* ── Result Highlight / Word List ── */
.bias-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid var(--border-color);
}
.bias-item:last-child {
    border-bottom: none;
}
.bias-word {
    font-weight: 600;
    font-size: 15px;
    min-width: 140px;
}
.bias-reason {
    color: var(--text-secondary);
    font-size: 14px;
    line-height: 1.5;
}

/* Highlighted Text Backgrounds */
.bias-high   { background: var(--status-high-bg); color: var(--status-high-color); padding: 2px 4px; border-radius: 4px; font-weight: 500; }
.bias-medium { background: var(--status-medium-bg); color: var(--status-medium-color); padding: 2px 4px; border-radius: 4px; font-weight: 500; }

/* Rewrite Box */
.rewrite-box {
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-primary);
    white-space: pre-wrap;
}

/* Gradient Section Separator */
.section-divider {
    height: 1px;
    background: var(--border-color);
    margin: 80px auto;
    width: 100px;
    border: none;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-color) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid var(--border-color) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface-solid) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* DataFrame */
.stDataFrame {
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Bulletproof Light Mode Forces */
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p, label {
    color: var(--text-primary) !important;
}
/* Sledgehammer for File Uploader Dropzone and texts */
[data-testid="stFileUploadDropzone"], 
[data-testid="stFileUploaderDropzone"], 
[data-testid="stFileUploader"] section, 
.stFileUploader section, 
[data-testid="stFileUploader"] div[data-testid="stVerticalBlock"] > div > div {
    background-color: var(--surface-solid) !important;
}
[data-testid="stFileUploadDropzone"] *, 
[data-testid="stFileUploaderDropzone"] *, 
.stFileUploader section * {
    color: var(--text-primary) !important;
}

/* Sledgehammer for "Browse files" & Download Buttons */
[data-testid="baseButton-secondary"], 
[data-testid="stFileUploader"] button, 
[data-testid="stDownloadButton"] button {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid rgba(0,0,0,0.2) !important;
    font-weight: 500 !important;
}
[data-testid="baseButton-secondary"]:hover, 
[data-testid="stFileUploader"] button:hover {
    background-color: #f2f2f7 !important;
    transform: scale(1.02) !important;
}

[data-testid="stException"] {
    background-color: var(--surface-solid) !important;
    color: var(--text-primary) !important;
}
</style>
"""
