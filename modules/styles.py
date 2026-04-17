CUSTOM_CSS = """
<style>
/* ── Deep Space & Neon UI Tokens ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root {
    --bg-color: #0d0f14;
    --surface-color: rgba(22, 25, 41, 0.6);
    --surface-solid: #161929;
    --border-color: rgba(91, 184, 196, 0.15);
    --border-highlight: rgba(91, 184, 196, 0.4);
    --text-primary: #f0f4f8;
    --text-secondary: #94a3b8;
    
    --accent-glow: 0 0 12px rgba(91, 184, 196, 0.25);
    --accent-primary: #5bb8c4;
    --accent-primary-dim: rgba(91, 184, 196, 0.15);
    --accent-secondary: #4caf6e;
    
    --status-high-bg: rgba(201, 79, 95, 0.15);
    --status-high-color: #c94f5f;
    --status-high-glow: 0 0 8px rgba(201, 79, 95, 0.3);
    
    --status-medium-bg: rgba(200, 168, 75, 0.15);
    --status-medium-color: #c8a84b;
    
    --status-low-bg: rgba(76, 175, 110, 0.15);
    --status-low-color: #4caf6e;
    
    --card-radius: 12px;
    --glass-blur: blur(24px);
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    letter-spacing: 0.02em;
}

.stApp {
    background: var(--bg-color) !important;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(91, 184, 196, 0.02) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(120, 60, 180, 0.02) 0%, transparent 50%);
    color: var(--text-primary) !important;
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
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
}
a.step-item {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
    font-size: 13px;
    color: var(--text-secondary);
    transition: all 0.3s ease;
    text-decoration: none !important;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 1px;
}
a.step-item:hover {
    color: var(--accent-primary) !important;
    text-shadow: 0 0 8px var(--accent-primary);
}
a.step-item.active {
    color: var(--accent-primary);
    text-shadow: 0 0 8px rgba(0, 243, 255, 0.5);
}
.step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: transparent;
    border: 1px solid var(--text-secondary);
    transition: all 0.3s ease;
    font-size: 12px;
    font-weight: 700;
}
.step-item.active .step-number {
    background: var(--accent-primary-dim);
    border-color: var(--accent-primary);
    color: var(--accent-primary);
    box-shadow: var(--accent-glow);
}
a.step-item:hover .step-number {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 60px 20px;
    margin-bottom: 40px;
    animation: pulseGlow 3s infinite alternate;
}
@keyframes pulseGlow {
    from { text-shadow: 0 0 8px rgba(91, 184, 196, 0.08); }
    to { text-shadow: 0 0 20px rgba(91, 184, 196, 0.2); }
}
.hero h1 {
    font-size: 56px;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 20px 0;
    background: linear-gradient(90deg, #d0dde8, var(--accent-primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}
.hero p {
    color: var(--text-secondary);
    font-size: 18px;
    line-height: 1.6;
    max-width: 650px;
    margin: 0 auto;
}
.hero-tag {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(110, 50, 180, 0.1);
    color: #9a6ecf;
    border: 1px solid rgba(110, 50, 180, 0.25);
    border-radius: 20px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 24px;
}

/* ── Cards & Containers ── */
.glass-card {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--card-radius);
    padding: 40px;
    margin-bottom: 40px;
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: all 0.4s ease;
}
.glass-card:hover {
    border-color: var(--accent-primary);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), var(--accent-glow);
    transform: translateY(-2px);
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 0 0 32px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 16px;
}
.section-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: var(--surface-solid);
    border: 1px solid var(--accent-primary);
    border-radius: 10px;
    color: var(--accent-primary);
    box-shadow: inset 0 0 8px rgba(91, 184, 196, 0.1);
}
.section-title {
    font-size: 24px;
    font-weight: 700;
    color: white;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ── Streamlit Selectors Overrides ── */
.stTextArea textarea {
    background: rgba(26, 27, 58, 0.85) !important;
    border: 1px solid rgba(140, 100, 210, 0.35) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: inherit !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}
.stTextArea textarea:focus {
    border-color: rgba(160, 120, 230, 0.7) !important;
    box-shadow: 0 0 12px rgba(140, 100, 210, 0.25), inset 0 2px 8px rgba(0,0,0,0.3) !important;
    background: rgba(30, 32, 68, 0.9) !important;
}

.stButton > button, .stDownloadButton > button, [data-testid="baseButton-primary"] {
    background: transparent !important;
    color: var(--accent-primary) !important;
    border: 1px solid var(--accent-primary) !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    box-shadow: inset 0 0 8px rgba(91, 184, 196, 0.06) !important;
}
.stButton > button:hover {
    background: var(--accent-primary) !important;
    color: #0d0f14 !important;
    box-shadow: 0 0 14px rgba(91, 184, 196, 0.35) !important;
}

.stFileUploader {
    background: rgba(0,0,0,0.3) !important;
    border: 1px dashed rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    transition: all 0.3s ease;
}
.stFileUploader:hover {
    border-color: var(--accent-primary) !important;
    background: rgba(91, 184, 196, 0.02) !important;
}

/* ── Badges & Status Pills ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 1px solid transparent;
}
.badge-high   { background: var(--status-high-bg); color: var(--status-high-color); border-color: rgba(201, 79, 95, 0.25); box-shadow: var(--status-high-glow); }
.badge-medium { background: var(--status-medium-bg); color: var(--status-medium-color); border-color: rgba(200, 168, 75, 0.25); }
.badge-low    { background: var(--status-low-bg); color: var(--status-low-color); border-color: rgba(76, 175, 110, 0.25); }

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin: 24px 0;
}
.metric-card {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 24px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
    border-color: var(--accent-primary);
    box-shadow: 0 10px 20px rgba(0,0,0,0.4), inset 0 0 10px rgba(91, 184, 196, 0.06);
}
.metric-val {
    font-size: 42px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 12px;
    font-family: 'Orbitron', 'Inter', sans-serif;
}
.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Result Highlight / Word List ── */
.bias-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 20px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.bias-item:last-child { border-bottom: none; }
.bias-word {
    font-weight: 700;
    font-size: 16px;
    min-width: 140px;
    text-shadow: 0 0 8px currentColor;
}
.bias-reason {
    color: var(--text-secondary);
    font-size: 14px;
    line-height: 1.6;
}

/* Highlighted Text Backgrounds */
.bias-high   { background: var(--status-high-bg); color: var(--status-high-color); padding: 2px 6px; border-radius: 4px; font-weight: 600; text-shadow: none; border: 1px solid rgba(201,79,95,0.25);}
.bias-medium { background: var(--status-medium-bg); color: var(--status-medium-color); padding: 2px 6px; border-radius: 4px; font-weight: 600; text-shadow: none; border: 1px solid rgba(200,168,75,0.25);}

/* Rewrite Box */
.rewrite-box {
    background: rgba(0,0,0,0.5);
    border: 1px solid var(--accent-primary);
    box-shadow: inset 0 0 12px rgba(91, 184, 196, 0.03);
    border-radius: 8px;
    padding: 30px;
    font-size: 16px;
    line-height: 1.8;
    color: var(--text-primary);
    white-space: pre-wrap;
}

/* Gradient Section Separator */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    margin: 80px auto;
    width: 60%;
    border: none;
    opacity: 0.3;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.4) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-size: 12px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-primary-dim) !important;
    color: var(--accent-primary) !important;
    border: 1px solid var(--accent-primary) !important;
    box-shadow: var(--accent-glow) !important;
}

/* DataFrame */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}

/* Sledgehammer Light Mode Forces -> Dark Mode Elements */
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p, label {
    color: var(--text-primary) !important;
}
/* File Uploader backgrounds */
[data-testid="stFileUploadDropzone"], 
[data-testid="stFileUploaderDropzone"], 
[data-testid="stFileUploader"] section, 
.stFileUploader section, 
[data-testid="stFileUploader"] div[data-testid="stVerticalBlock"] > div > div {
    background-color: rgba(0,0,0,0.4) !important;
}
[data-testid="stFileUploadDropzone"] *, 
[data-testid="stFileUploaderDropzone"] *, 
.stFileUploader section * {
    color: var(--text-primary) !important;
}

[data-testid="baseButton-secondary"], 
[data-testid="stFileUploader"] button, 
[data-testid="stDownloadButton"] button {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    font-weight: 600 !important;
}
[data-testid="baseButton-secondary"]:hover, 
[data-testid="stFileUploader"] button:hover {
    background-color: rgba(255,255,255,0.05) !important;
    border-color: var(--text-primary) !important;
}

[data-testid="stException"] {
    background-color: rgba(255,0,0,0.1) !important;
    border: 1px solid #ff0000 !important;
    color: #ffb3b3 !important;
}

/* Dataframe headers and rows */
div[data-testid="stDataFrame"] table {
    background-color: rgba(0,0,0,0.5) !important;
    color: #fff !important;
}
div[data-testid="stDataFrame"] th {
    background-color: #161929 !important;
    border-bottom: 2px solid var(--accent-primary) !important;
    color: var(--accent-primary) !important;
}
div[data-testid="stDataFrame"] td {
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

</style>
"""
