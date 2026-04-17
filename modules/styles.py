CUSTOM_CSS = """
<style>
/* ── Design Tokens ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:              #0d0f14;
    --surface:         rgba(20, 23, 38, 0.75);
    --surface-solid:   #14172a;
    --border:          rgba(91, 184, 196, 0.12);
    --border-hi:       rgba(91, 184, 196, 0.38);
    --text-1:          #eef2f7;
    --text-2:          #7a8fa6;

    --accent:          #5bb8c4;
    --accent-dim:      rgba(91, 184, 196, 0.1);
    --accent-glow:     0 0 18px rgba(91, 184, 196, 0.18);

    --red:             #c94f5f;   --red-bg:   rgba(201,79,95,0.1);
    --amber:           #c8a84b;   --amber-bg: rgba(200,168,75,0.1);
    --green:           #4caf6e;   --green-bg: rgba(76,175,110,0.1);

    --radius:    12px;
    --blur:      blur(20px);
    --ease:      cubic-bezier(0.4, 0, 0.2, 1);
    --spring:    cubic-bezier(0.22, 1, 0.36, 1);
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}
.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 70% 50% at 15% 0%,   rgba(91,184,196,0.05) 0%, transparent 100%),
        radial-gradient(ellipse 60% 40% at 85% 100%,  rgba(100,50,180,0.04) 0%, transparent 100%);
    color: var(--text-1) !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Top bar ── */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(13,15,20,0.88);
    backdrop-filter: var(--blur);
    -webkit-backdrop-filter: var(--blur);
    border-bottom: 1px solid var(--border);
    padding: 11px 28px;
    position: sticky;
    top: 0;
    z-index: 999;
    margin-bottom: 0;
}
.top-bar-brand {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-1);
    letter-spacing: 0.2px;
    display: flex;
    align-items: center;
    gap: 7px;
}
.top-bar-step {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-2);
    text-transform: uppercase;
    letter-spacing: 1.8px;
    background: var(--accent-dim);
    border: 1px solid var(--border);
    padding: 4px 13px;
    border-radius: 20px;
    transition: color .2s var(--ease), border-color .2s var(--ease);
}
.top-bar-step:hover { color: var(--accent); border-color: var(--border-hi); }

/* ── Page transition ── */
@keyframes enterRight { from { opacity:0; transform:translateX(36px) } to { opacity:1; transform:none } }
@keyframes enterLeft  { from { opacity:0; transform:translateX(-36px)} to { opacity:1; transform:none } }
.page-enter-forward  { animation: enterRight .4s var(--spring) both !important; }
.page-enter-backward { animation: enterLeft  .4s var(--spring) both !important; }

/* ── Hero (page 1) ── */
@keyframes tagIn   { from { opacity:0; transform:translateY(-10px) } to { opacity:1; transform:none } }
@keyframes titleIn { from { opacity:0; filter:blur(8px) }           to { opacity:1; filter:blur(0) } }
@keyframes fadeUp  { from { opacity:0; transform:translateY(14px) } to { opacity:1; transform:none } }

.hero {
    text-align: center;
    padding: 24px 20px 16px;
    margin-bottom: 16px;
}
.hero-tag {
    display: inline-block;
    padding: 4px 14px;
    background: var(--accent-dim);
    color: var(--accent);
    border: 1px solid rgba(91,184,196,0.22);
    border-radius: 20px;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 700;
    margin-bottom: 14px;
    animation: tagIn .5s var(--ease) both .1s;
    transition: background .2s, border-color .2s, transform .2s;
}
.hero-tag:hover { background: rgba(91,184,196,0.16); transform: translateY(-1px); }
.hero h1 {
    font-size: 38px;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 14px;
    background: linear-gradient(100deg, #cdd8e8 20%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
    animation: titleIn .75s var(--spring) both .22s;
}
.hero p {
    color: var(--text-2);
    font-size: 15px;
    line-height: 1.7;
    max-width: 560px;
    margin: 0 auto;
    min-height: 48px;
    animation: fadeUp .6s var(--ease) both .5s;
}

/* ── Glass card ── */
@keyframes cardIn { from { opacity:0; transform:translateY(18px) } to { opacity:1; transform:none } }
.glass-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 32px;
    margin-bottom: 20px;
    backdrop-filter: var(--blur);
    -webkit-backdrop-filter: var(--blur);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: border-color .3s var(--ease), box-shadow .3s var(--ease), transform .3s var(--ease);
    animation: cardIn .5s var(--spring) both;
    will-change: transform;
}
.glass-card:hover {
    border-color: var(--border-hi);
    box-shadow: 0 10px 36px rgba(0,0,0,0.45), var(--accent-glow);
    transform: translateY(-3px);
}

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 13px;
    margin: 0 0 24px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    padding-bottom: 14px;
}
.section-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px; height: 40px;
    background: var(--surface-solid);
    border: 1px solid var(--accent);
    border-radius: 9px;
    color: var(--accent);
    transition: transform .25s var(--ease), box-shadow .25s var(--ease), border-color .25s var(--ease);
    flex-shrink: 0;
    cursor: default;
}
.section-icon:hover {
    transform: rotate(12deg) scale(1.12);
    box-shadow: 0 0 20px rgba(91,184,196,0.22);
    border-color: var(--border-hi);
}
.section-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-1);
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ── Text area ── */
.stTextArea textarea {
    background: rgba(20,23,38,0.85) !important;
    border: 1px solid rgba(91,184,196,0.18) !important;
    border-radius: 8px !important;
    color: var(--text-1) !important;
    font-family: inherit !important;
    padding: 14px !important;
    transition: border-color .2s var(--ease), box-shadow .2s var(--ease), background .2s var(--ease) !important;
}
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.28) !important; opacity:1 !important; }
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    background: rgba(12,36,44,0.92) !important;
    box-shadow: 0 0 0 3px rgba(91,184,196,0.1) !important;
    color: #fff !important;
}

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button, [data-testid="baseButton-primary"] {
    background: rgba(91,184,196,0.06) !important;
    color: var(--accent) !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: inset 0 0 0 1px rgba(91,184,196,0.2) !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: background .25s var(--ease), color .25s var(--ease),
                box-shadow .25s var(--ease), transform .15s var(--ease) !important;
}
.stButton > button:hover {
    background: rgba(91,184,196,0.15) !important;
    color: #fff !important;
    box-shadow: inset 0 0 0 1px var(--accent), 0 8px 24px rgba(91,184,196,0.25) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: inset 0 0 0 1px var(--accent) !important;
}

/* Prev / ghost button */
.nav-prev .stButton > button {
    background: transparent !important;
    color: var(--text-2) !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1) !important;
}
.nav-prev .stButton > button:hover {
    background: rgba(255,255,255,0.05) !important;
    color: var(--text-1) !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.25), 0 6px 16px rgba(0,0,0,0.3) !important;
}

/* ── File uploader ── */
.stFileUploader {
    background: rgba(0,0,0,0.18) !important;
    border: 1px dashed rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    transition: border-color .2s, background .2s;
}
.stFileUploader:hover {
    border-color: var(--accent) !important;
    background: rgba(91,184,196,0.02) !important;
}

/* ── Badges ── */
@keyframes shimmer {
    0%   { left:-80% }
    60%  { left:130% }
    100% { left:130% }
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 11px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    border: 1px solid transparent;
    position: relative;
    overflow: hidden;
    transition: transform .2s var(--ease);
}
.badge::after {
    content:'';
    position: absolute;
    top:0; left:-80%;
    width:45%; height:100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    animation: shimmer 3.5s ease infinite;
}
.badge:hover { transform: translateY(-1px); }
.badge-high   { background:var(--red-bg);   color:var(--red);   border-color:rgba(201,79,95,0.2);  }
.badge-medium { background:var(--amber-bg); color:var(--amber); border-color:rgba(200,168,75,0.2); }
.badge-low    { background:var(--green-bg); color:var(--green); border-color:rgba(76,175,110,0.2); }

/* ── Metric grid ── */
@keyframes metIn { from { opacity:0; transform:scale(0.93) translateY(8px) } to { opacity:1; transform:none } }
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px,1fr));
    gap: 12px;
    margin: 18px 0;
}
.metric-card {
    background: rgba(0,0,0,0.28);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: transform .3s var(--spring), box-shadow .3s var(--ease), border-color .3s var(--ease);
    animation: metIn .5s var(--spring) both;
    position: relative;
    overflow: hidden;
    will-change: transform;
}
.metric-card::before {
    content:'';
    position:absolute;
    top:-100%; left:-60%;
    width:50%; height:300%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.015), transparent);
    transform: skewX(-15deg);
    transition: left .7s ease;
}
.metric-card:hover::before { left: 170%; }
.metric-card:hover {
    transform: translateY(-7px) scale(1.01);
    border-color: var(--border-hi);
    box-shadow: 0 16px 32px rgba(0,0,0,0.45), var(--accent-glow);
}
.metric-val {
    font-size: 36px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
}
.metric-label {
    font-size: 10px;
    color: var(--text-2);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
}

/* ── Bias items ── */
.bias-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    border-radius: 7px;
    transition: background .18s var(--ease), padding-left .18s var(--ease);
    cursor: default;
}
.bias-item:hover { background: rgba(255,255,255,0.025); padding-left: 16px; }
.bias-item:last-child { border-bottom: none; }
.bias-word { font-weight: 700; font-size: 14px; min-width: 120px; }
.bias-reason { color: var(--text-2); font-size: 13px; line-height: 1.6; }

/* Inline highlight spans */
.bias-high   { background:var(--red-bg);   color:var(--red);   padding:1px 5px; border-radius:3px; font-weight:600; border:1px solid rgba(201,79,95,0.2); }
.bias-medium { background:var(--amber-bg); color:var(--amber); padding:1px 5px; border-radius:3px; font-weight:600; border:1px solid rgba(200,168,75,0.2); }

/* ── Rewrite box ── */
.rewrite-box {
    background: rgba(0,0,0,0.35);
    border: 1px solid var(--border-hi);
    border-radius: 10px;
    padding: 22px 26px;
    font-size: 14px;
    line-height: 1.8;
    color: var(--text-1);
    white-space: pre-wrap;
    animation: cardIn .4s var(--spring) both;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-hi), transparent);
    margin: 40px auto;
    width: 40%;
    border: none;
    opacity: 0.35;
}

/* ── UI Object Hover/Glow Flashlight System ── */
#cursor-flashlight {
    position: fixed;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    /* Creates a beautiful ambient glow that blends with the UI */
    background: radial-gradient(circle, rgba(91,184,196,0.15) 0%, rgba(91,184,196,0.05) 40%, transparent 70%);
    pointer-events: none;
    z-index: 9999;
    transform: translate(-50%, -50%);
    /* This makes the glow interact and brighten the borders and backgrounds of EVERYTHING under it */
    mix-blend-mode: color-dodge; 
    transition: width 0.2s, height 0.2s;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.25) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-2) !important;
    border-radius: 5px !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-size: 10px !important;
    transition: color .18s, background .18s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-1) !important; background: rgba(255,255,255,0.03) !important; }
.stTabs [aria-selected="true"] { background: var(--accent-dim) !important; color: var(--accent) !important; border: 1px solid var(--border) !important; }

/* ── Streamlit widget overrides ── */
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p, label {
    color: var(--text-1) !important;
}
[data-testid="stFileUploadDropzone"],
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploader"] section,
.stFileUploader section {
    background-color: rgba(0,0,0,0.3) !important;
}
[data-testid="stFileUploadDropzone"] *,
[data-testid="stFileUploaderDropzone"] *,
.stFileUploader section * { color: var(--text-1) !important; }

[data-testid="baseButton-secondary"],
[data-testid="stFileUploader"] button,
[data-testid="stDownloadButton"] button {
    background-color: transparent !important;
    color: var(--text-1) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    font-weight: 600 !important;
    transition: all .2s var(--ease) !important;
}
[data-testid="baseButton-secondary"]:hover,
[data-testid="stFileUploader"] button:hover {
    background-color: rgba(255,255,255,0.04) !important;
    border-color: var(--text-1) !important;
}
[data-testid="stException"] {
    background-color: var(--red-bg) !important;
    border: 1px solid var(--red) !important;
    color: #ffb3b3 !important;
}
div[data-testid="stDataFrame"] table { background-color: rgba(0,0,0,0.4) !important; color:#fff !important; }
div[data-testid="stDataFrame"] th    { background-color: var(--surface-solid) !important; border-bottom:2px solid var(--accent) !important; color:var(--accent) !important; }
div[data-testid="stDataFrame"] td    { border-bottom:1px solid rgba(255,255,255,0.04) !important; }
.stDataFrame { border:1px solid rgba(255,255,255,0.07) !important; border-radius:8px !important; }

</style>
"""
