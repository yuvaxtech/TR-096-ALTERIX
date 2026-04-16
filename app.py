"""
AI Recruitment Bias Auditor
A production-ready Streamlit app to detect and eliminate hiring bias.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import time
from datetime import datetime
import PyPDF2
from docx import Document
import streamlit.components.v1 as components

from modules.styles import CUSTOM_CSS
from modules.data import SAMPLE_CSV, SAMPLE_JD
from modules.bias_engine import detect_bias, bias_score, highlight_text, rewrite_jd
from modules.fairness_calc import compute_fairness, overall_fairness_verdict

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Bias Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ── INITIAL STATE & HELPERS ──
# ─────────────────────────────────────────────
if "scroll_to" not in st.session_state:
    st.session_state["scroll_to"] = None

def scroll_manager():
    if st.session_state["scroll_to"]:
        target = st.session_state["scroll_to"]
        js = f"""
        <script>
            setTimeout(() => {{
                const target = window.parent.document.getElementById('{target}');
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }}, 200);
        </script>
        """
        components.html(js, height=0)
        st.session_state["scroll_to"] = None

# ─────────────────────────────────────────────
# ── TOP NAVIGATION STEPPER ──
# ─────────────────────────────────────────────
def step_str(num, label, target_id):
    return f'<a href="#{target_id}" class="step-item active"><div class="step-number">{num}</div><span>{label}</span></a>'

st.markdown(f"""
<div class="stepper-container">
{step_str(1, "Job Description", "step-1")}
<div style="flex: 1; height: 1px; background: var(--border-color); margin: 0 15px;"></div>
{step_str(2, "Bias Analysis", "step-2")}
<div style="flex: 1; height: 1px; background: var(--border-color); margin: 0 15px;"></div>
{step_str(3, "Rewrite", "step-3")}
<div style="flex: 1; height: 1px; background: var(--border-color); margin: 0 15px;"></div>
{step_str(4, "Data Dashboard", "step-4")}
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ── HERO HEADER ──
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-tag">✨ AI-Powered Fairness</div>
        <h1>Recruitment Bias Auditor</h1>
        <p>Detect hidden bias in job descriptions, generate inclusive language rewrites, 
        and monitor your hiring pipeline for demographic disparities in one unified platform.</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── STEP 1: JOB DESCRIPTION UPLOAD ──
# ─────────────────────────────────────────────
st.markdown("<div id='step-1'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="glass-card">
    <div class="section-header">
        <div class="section-icon">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        </div>
        <h2 class="section-title">Upload Job Description</h2>
    </div>
""", unsafe_allow_html=True)

if "uploaded_jd_name" not in st.session_state:
    st.session_state["uploaded_jd_name"] = None
if "jd_input" not in st.session_state:
    st.session_state["jd_input"] = ""
if "jd_input_widget" not in st.session_state:
    st.session_state["jd_input_widget"] = ""

uploaded_jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"])
if uploaded_jd is not None:
    if st.session_state["uploaded_jd_name"] != uploaded_jd.name:
        try:
            if uploaded_jd.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(uploaded_jd)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\\n"
                st.session_state["jd_input"] = text.strip()
                st.session_state["jd_input_widget"] = text.strip()
            elif uploaded_jd.name.endswith(".docx"):
                doc = Document(uploaded_jd)
                text = "\\n".join([p.text for p in doc.paragraphs])
                st.session_state["jd_input"] = text.strip()
                st.session_state["jd_input_widget"] = text.strip()
            st.session_state["uploaded_jd_name"] = uploaded_jd.name
            st.toast("✅ Document parsed successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
else:
    st.session_state["uploaded_jd_name"] = None

col_input, col_controls = st.columns([3, 1])

def set_sample_jd():
    st.session_state["jd_input"] = SAMPLE_JD
    st.session_state["jd_input_widget"] = SAMPLE_JD

with col_input:
    jd_text = st.text_area(
        "Paste or edit your job description here",
        placeholder="e.g. We are looking for a young, energetic rockstar developer…",
        height=220,
        key="jd_input_widget",
    )
    st.session_state["jd_input"] = st.session_state["jd_input_widget"]

with col_controls:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("📋 Load Example", use_container_width=True, on_click=set_sample_jd)
    analyze_btn = st.button("🔍 Analyze for Bias", use_container_width=True, type="primary")

st.markdown("</div>", unsafe_allow_html=True)

if analyze_btn:
    if st.session_state["jd_input"].strip():
        with st.spinner("Analyzing semantics and searching for bias patterns..."):
            time.sleep(0.8)
        
        findings = detect_bias(st.session_state["jd_input"])
        st.session_state["jd_findings"] = findings
        st.session_state["jd_for_rewrite"] = st.session_state["jd_input"]
        st.toast("🔍 Analysis Complete!")
        st.session_state["scroll_to"] = "step-2"
    else:
        st.warning("Please enter or load a job description first.")


# ─────────────────────────────────────────────
# ── STEP 2: BIAS DETECTION RESULTS ──
# ─────────────────────────────────────────────
st.markdown("<div id='step-2'></div>", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div class="section-header">
        <div class="section-icon">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
        </div>
        <h2 class="section-title">Bias Detection Results</h2>
    </div>
""", unsafe_allow_html=True)

if "jd_findings" not in st.session_state:
    st.info("💡 Paste a job description above and click 'Analyze for Bias' to view detailed metrics and highlights here.")
else:
    findings = st.session_state["jd_findings"]
    jd_source = st.session_state.get("jd_for_rewrite", "")
    score = bias_score(findings)

    badge_map = {
        "high":   ("badge-high",   "🔴 HIGH BIAS DETECTED"),
        "medium": ("badge-medium", "🟡 MEDIUM BIAS DETECTED"),
        "low":    ("badge-low",    "🟢 LOW BIAS / SAFE"),
    }
    badge_cls, badge_label = badge_map[score]

    st.markdown(f"""
    <div style="margin-bottom:24px; display:flex; justify-content:flex-end;">
        <span class="badge {badge_cls}">{badge_label}</span>
    </div>
    """, unsafe_allow_html=True)

    if findings:
        high_n   = sum(1 for f in findings if f["severity"] == "high")
        medium_n = sum(1 for f in findings if f["severity"] == "medium")
        low_n    = sum(1 for f in findings if f["severity"] == "low")

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-val" style="color:var(--status-high-color);">{high_n}</div>
                <div class="metric-label">High Severity Issues</div>
            </div>
            <div class="metric-card">
                <div class="metric-val" style="color:var(--status-medium-color);">{medium_n}</div>
                <div class="metric-label">Medium Severity Issues</div>
            </div>
            <div class="metric-card">
                <div class="metric-val" style="color:var(--status-low-color);">{low_n}</div>
                <div class="metric-label">Low Severity Issues</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        highlighted = highlight_text(jd_source, findings)
        st.markdown(f"""
        <div style="font-family:'Outfit', sans-serif; font-weight:600; font-size:16px; margin-bottom:12px; color:var(--text-primary)">Highlighted Document Viewer</div>
        <div style="background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); border-radius: 12px;
                    padding: 24px; font-size: 15px; line-height: 1.9; white-space: pre-wrap; margin-bottom: 24px; color: var(--text-secondary);">
        {highlighted}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-family:Outfit,sans-serif; font-weight:700; font-size:16px; margin-bottom:16px; color:var(--text-primary)'>Detailed Breakdowns</p>", unsafe_allow_html=True)
        for f in findings:
            c = "var(--status-high-color)" if f["severity"] == "high" else ("var(--status-medium-color)" if f["severity"] == "medium" else "var(--status-low-color)")
            st.markdown(f"""
            <div class="bias-item">
                <div class="bias-word" style="color:{c};">"{f['phrase']}"</div>
                <div>
                    <span class="badge badge-{'high' if f['severity']=='high' else 'medium' if f['severity']=='medium' else 'low'}"
                          style="font-size:10px; padding:3px 10px; margin-bottom:8px; display:inline-flex;">
                        {f['severity'].upper()}
                    </span>
                    <div class="bias-reason">{f['reason']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.success("🎉 No bias identified! The current textual framework appears inclusive and objective.")

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ── STEP 3: BIAS-FREE REWRITE ──
# ─────────────────────────────────────────────
st.markdown("<div id='step-3'></div>", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div class="section-header">
        <div class="section-icon">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
        </div>
        <h2 class="section-title">Inclusive Content Generator</h2>
    </div>
""", unsafe_allow_html=True)

rewrite_source = st.session_state.get("jd_for_rewrite", "")

col_r1, col_r2 = st.columns([3, 1])
with col_r1:
    rewrite_input = st.text_area(
        "Target Text to Neutralize",
        value=rewrite_source,
        height=160,
        key="rewrite_input_widget",
    )
with col_r2:
    st.markdown("<br>", unsafe_allow_html=True)
    rewrite_btn = st.button("✨ Generate Inclusive Version", use_container_width=True, type="primary")

if rewrite_btn and rewrite_input.strip():
    with st.spinner("Applying natural language neutrality rewriting…"):
        time.sleep(1) # UX feeling
        rewritten = rewrite_jd(rewrite_input)
        st.session_state["rewritten_jd"] = rewritten
        st.session_state["animate_rewrite"] = True

if "rewritten_jd" in st.session_state:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin:24px 0 16px;">
        <span class="badge badge-low">✅ INCLUSIVE AI OUTPUT</span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("animate_rewrite", False):
        safe_jd = st.session_state["rewritten_jd"].replace('`', '\\`').replace('$', '\\$').replace('\\n', '<br>')
        st.markdown(f'<div class="rewrite-box" id="typed-output"></div>', unsafe_allow_html=True)
        components.html(f"""
        <script>
            const text = `{safe_jd}`;
            const target = window.parent.document.getElementById('typed-output');
            if (target) {{
                let i = 0;
                function typeWriter() {{
                    if (i < text.length) {{
                        if (text.substr(i, 4) === "<br>") {{
                            target.innerHTML += "<br>";
                            i += 4;
                        }} else {{
                            target.innerHTML += text.charAt(i);
                            i++;
                        }}
                        setTimeout(typeWriter, 5);
                    }}
                }}
                typeWriter();
            }}
        </script>
        """, height=0)
        st.session_state["animate_rewrite"] = False
    else:
        st.markdown(f'<div class="rewrite-box">{st.session_state["rewritten_jd"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_copy, col_down = st.columns([1, 1])
    
    with col_copy:
        safe_jd_copy = st.session_state["rewritten_jd"].replace('`', '\\`').replace('$', '\\$').replace('\\n', '\\n')
        components.html(f"""
            <button onclick="navigator.clipboard.writeText(`{safe_jd_copy}`); this.innerText='✅ Copied!';" 
            style="width: 100%; box-sizing: border-box; padding: 10px 24px; background: #0066cc; color: white; border: none; border-radius: 10px; 
            cursor: pointer; font-size: 15px; font-weight: 500; font-family: -apple-system, BlinkMacSystemFont, sans-serif; transition: transform 0.2s, opacity 0.2s;">
            📋 Copy Text
            </button>
            <style>button:hover {{transform: scale(1.02); opacity: 0.9;}} button:active {{transform: scale(0.98);}}</style>
        """, height=60)
        
    with col_down:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 7, text=st.session_state["rewritten_jd"].encode('latin-1', 'replace').decode('latin-1'))
        pdf_bytes = bytes(pdf.output())
        
        st.download_button(
            label="⬇️ Download as PDF",
            data=pdf_bytes,
            file_name=f"inclusive_jd_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── STEP 4: HIRING DATA DASHBOARD ──
# ─────────────────────────────────────────────
st.markdown("<div id='step-4'></div>", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""<div class="glass-card">
<div class="section-header">
<div class="section-icon">
<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
</div>
<h2 class="section-title">Diversity & Fairness Dashboard</h2>
</div>
<p style="color:var(--text-secondary); margin-bottom: 24px;">
Audit historical hiring data using the <strong style="color:var(--text-primary);">EEOC 80% Disparate Impact Rule</strong>. 
Test for systemic bias using intersectional demographic groups (e.g. Female & Under 30).
</p>""", unsafe_allow_html=True)

col_up, col_sample = st.columns([3, 1])
with col_up:
    uploaded_file = st.file_uploader("Upload Applicant Data (CSV)", type=["csv"])
with col_sample:
    st.markdown("<br>", unsafe_allow_html=True)
    use_sample = st.button("🗂️ Use Verified Sample Dataset", use_container_width=True)

df_raw = None
demo_label = "Group"
target_label = "Favorable Rate"

if use_sample:
    df_raw = pd.read_csv(io.StringIO(SAMPLE_CSV))
    st.success("✅ Loaded pre-formatted sample dataset covering 12 intersectional groups.")
    demo_label = "Gender"
    target_label = "Hire Rate"
elif uploaded_file:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        required = {"gender", "applied", "shortlisted", "hired"}
        
        if required.issubset(set(df_uploaded.columns)):
            st.success(f"✅ Loaded native format with {len(df_uploaded)} rows.")
            df_raw = df_uploaded
            demo_label = "Gender"
            target_label = "Hire Rate"
        else:
            st.info("Raw multi-column dataset detected. Please configure semantic mapping below:")
            
            c1, c2, c3 = st.columns(3)
            file_id = getattr(uploaded_file, 'file_id', uploaded_file.name)
            with c1:
                demo_cols = st.multiselect(
                    "Demographic Matrix (Intersectional)", 
                    options=df_uploaded.columns, 
                    default=[df_uploaded.columns[0]],
                    key=f"demo_{file_id}"
                )
            with c2:
                target_col = st.selectbox(
                    "Target Funnel Stage", 
                    options=df_uploaded.columns, 
                    index=min(1, len(df_uploaded.columns)-1),
                    key=f"target_{file_id}"
                )
            with c3:
                fav_val = st.selectbox(
                    "Favorable Label", 
                    options=list(df_uploaded[target_col].dropna().unique()),
                    key=f"fav_{file_id}"
                )
                
            if demo_cols:
                demo_label = " · ".join(demo_cols)
                df_raw = df_uploaded.copy()
                df_raw['merged_group'] = df_raw[demo_cols].astype(str).agg(' · '.join, axis=1)
                
                df_raw = df_raw.groupby('merged_group').agg(
                    applied=(target_col, "count"),
                    hired=(target_col, lambda x: (x == fav_val).sum())
                ).reset_index().rename(columns={"merged_group": "gender"})
                df_raw["shortlisted"] = df_raw["hired"]
            else:
                st.warning("Please align at least one demographic feature.")
    except Exception as e:
        st.error(f"Integrity check failed: {e}")

if df_raw is not None:
    df_result = compute_fairness(df_raw)
    verdict, min_di = overall_fairness_verdict(df_result)

    overall_hire_rate = (df_result["hired"].sum() / df_result["applied"].sum() * 100) if df_result["applied"].sum() > 0 else 0
    avg_di = df_result["disparate_impact"].mean()

    v_html = '<span class="badge badge-low">✅ SYSTEM FAIRNESS PASS</span>' if verdict == "fair" else '<span class="badge badge-high">⚠️ SYSTEMIC BIAS DETECTED</span>'

    st.markdown(f"""<br>
<div style="background: rgba(0,0,0,0.15); border: 1px solid var(--border-color); border-radius: 16px; padding: 32px; margin-bottom: 24px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<h3 style="font-family:'Outfit', sans-serif; margin:0;">Analytics Overview</h3>
{v_html}
</div>
<div class="metric-grid">
<div class="metric-card" title="Percentage of all applicants moving to favorable stage">
<div class="metric-val" style="color:var(--accent-primary);">{overall_hire_rate:.1f}%</div>
<div class="metric-label">Pipeline Yield</div>
</div>
<div class="metric-card" title="Average equity score across all measured groups (1.00 is target)">
<div class="metric-val" style="color:{'var(--status-low-color)' if avg_di>=0.8 else 'var(--status-high-color)'};">{avg_di:.2f}</div>
<div class="metric-label">Mean Equality Ratio</div>
</div>
<div class="metric-card" title="The lowest performing group ratio (Alert if < 0.80)">
<div class="metric-val" style="color:{'var(--status-low-color)' if min_di>=0.8 else 'var(--status-high-color)'};">{min_di:.2f}</div>
<div class="metric-label">Min Disparate Impact</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
    
    if verdict == "biased":
        worst = df_result.loc[df_result['disparate_impact'].idxmin()]
        st.warning(f"**Human Insight**: Candidates in group **'{worst['gender']}'** are experiencing systemic adverse impact. They are selected at significantly lower rates than the majority group, bringing their equity score to {worst['disparate_impact']:.2f} (Target is ≥ 0.80).")
    else:
        st.success("**Human Insight**: The pipeline is operating fairly. All demographic groups observed pass the 80% structural discrimination test baseline.")

    tab_names = [f"📊 Volume by {demo_label}", "📈 Disparate Impact", "📋 Audit Export"]
    tab1, tab2, tab3 = st.tabs(tab_names)

    with tab1:
        gender_df = df_result.groupby("gender").agg(applied=("applied", "sum"), hired=("hired", "sum")).reset_index()
        gender_df["hire_rate_pct"] = (gender_df["hired"] / gender_df["applied"] * 100).round(1)

        colors = ["#007aff", "#34c759", "#ff9500", "#ff3b30", "#5856d6"] * 10
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=gender_df["gender"], y=gender_df["hire_rate_pct"],
            marker=dict(color=colors[:len(gender_df)], line=dict(color="rgba(0,0,0,0.05)", width=1)),
            text=[f"{v}%" for v in gender_df["hire_rate_pct"]], textposition="outside",
            textfont=dict(color="#1d1d1f", size=13, family="-apple-system, sans-serif"),
        ))
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="-apple-system, sans-serif", color="#3a3a3c", size=12),
            xaxis=dict(gridcolor="rgba(0,0,0,0.05)", title=demo_label),
            yaxis=dict(gridcolor="rgba(0,0,0,0.05)", title=f"{target_label} (%)"),
            margin=dict(l=10, r=10, t=30, b=10), height=360, hovermode="x"
        )
        st.plotly_chart(fig1, use_container_width=True, theme=None)

    with tab2:
        di_df = df_result.copy()
        di_df["group"] = di_df["gender"] + (" · " + di_df["age_group"] if "age_group" in df_result.columns and demo_label == "Gender" else "")
        di_df = di_df.sort_values("disparate_impact")

        bar_colors = ["#ff3b30" if v < 0.8 else "#34c759" for v in di_df["disparate_impact"]]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=di_df["group"], x=di_df["disparate_impact"], orientation="h",
            marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0.05)", width=1)),
            text=[f"{v:.2f}" for v in di_df["disparate_impact"]], textposition="outside",
            textfont=dict(color="#1d1d1f", size=12, family="-apple-system, sans-serif"),
            hovertemplate="<b>%{y}</b><br>Impact Score: %{x}<br><i>A score < 0.8 is considered biased.</i><extra></extra>"
        ))
        fig2.add_vline(x=0.8, line_dash="dash", line_color="#ff9500", line_width=2,
                        annotation_text=" 80% Threshold", annotation_font_color="#ff9500", annotation_font_size=12)
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="-apple-system, sans-serif", color="#3a3a3c", size=12),
            xaxis=dict(gridcolor="rgba(0,0,0,0.05)", range=[0, 1.15], title="Disparate Impact Ratio"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=40, t=10, b=10), height=max(320, len(di_df) * 35)
        )
        st.plotly_chart(fig2, use_container_width=True, theme=None)

    with tab3:
        display_df = df_result.copy()
        display_df["shortlist_rate"] = (display_df["shortlist_rate"] * 100).round(1).astype(str) + "%"
        display_df["hire_rate"]      = (display_df["hire_rate"]      * 100).round(1).astype(str) + "%"
        display_df = display_df.rename(columns={"gender": demo_label, "disparate_impact": "Disparate Impact"})

        def highlight_di(val):
            try: 
                return "background-color: rgba(255,77,109,0.2); color: #ff4d6d; font-weight: bold;" if float(val) < 0.8 else ""
            except: return ""
        st.dataframe(display_df.style.map(highlight_di, subset=["Disparate Impact"]), use_container_width=True, height=350)
        
        st.download_button("⬇️ Download Full Report", df_result.to_csv(index=False), f"fairness_report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

st.markdown("</div>", unsafe_allow_html=True)

# Call scroll manager at end
scroll_manager()

st.markdown("""
<div style="text-align:center; padding: 40px 0 20px; color:var(--text-secondary); font-size:13px;">
    <strong style="color:var(--accent-primary);">AI Recruitment Bias Auditor</strong> — Enterprise Edition
</div>
""", unsafe_allow_html=True)
