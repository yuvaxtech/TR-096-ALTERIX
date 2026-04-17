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
# SESSION STATE
# ─────────────────────────────────────────────
for key, default in {
    "current_page": 1,
    "prev_page": 1,
    "uploaded_jd_name": None,
    "jd_input": "",
    "jd_input_widget": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def go_to(page: int):
    st.session_state.prev_page = st.session_state.current_page
    st.session_state.current_page = page


page = st.session_state.current_page
prev_page = st.session_state.prev_page
direction = "forward" if page >= prev_page else "backward"

# ─────────────────────────────────────────────
# PAGE TRANSITION — inject JS to animate container
# ─────────────────────────────────────────────
anim_class = "page-enter-forward" if direction == "forward" else "page-enter-backward"
components.html(f"""
<script>
(function() {{
    const block = window.parent.document.querySelector('.main .block-container');
    if (block) {{
        block.classList.remove('page-enter-forward', 'page-enter-backward');
        void block.offsetWidth;
        block.classList.add('{anim_class}');
    }}
}})();
</script>
""", height=0)

# ─────────────────────────────────────────────
# CURSOR FLASHLIGHT (Makes every object glow!)
# ─────────────────────────────────────────────
components.html("""
<script>
(function() {
    const doc = window.parent.document;
    const body = doc.body;

    // Only inject once
    if (doc.getElementById('cursor-flashlight')) return;

    const flashlight = doc.createElement('div');
    flashlight.id = 'cursor-flashlight';
    body.appendChild(flashlight);

    // ── Move handler
    doc.addEventListener('mousemove', (e) => {
        flashlight.style.left = e.clientX + 'px';
        flashlight.style.top  = e.clientY + 'px';
        
        // Trail particles
        if (Math.random() < 0.25) spawnParticle(e.clientX, e.clientY);
    });

    // ── Click burst
    doc.addEventListener('click', (e) => {
        for (let i = 0; i < 12; i++) spawnParticle(e.clientX, e.clientY, true);
    });

    function spawnParticle(x, y, burst = false) {
        const p = doc.createElement('div');
        const size = burst ? (Math.random() * 4 + 2) : (Math.random() * 2 + 1);
        const angle = Math.random() * Math.PI * 2;
        const dist = burst ? (Math.random() * 80 + 20) : (Math.random() * 25 + 5);
        const life = burst ? (Math.random() * 600 + 400) : (Math.random() * 500 + 300);
        const opacity = Math.random() * 0.5 + 0.3;
        
        p.style.cssText = `
            position: fixed;
            width: ${size}px; height: ${size}px;
            left: ${x}px; top: ${y}px;
            background: rgba(91,184,196, ${opacity});
            box-shadow: 0 0 ${size*2}px rgba(91,184,196,0.8);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9998;
            mix-blend-mode: screen;
        `;
        body.appendChild(p);

        let start = null;
        requestAnimationFrame(function tick(ts) {
            if (!start) start = ts;
            const t = Math.min((ts - start) / life, 1);
            const ease = 1 - Math.pow(1 - t, 3); // cubic ease out

            // Float upwards slightly while moving outwards
            const tx = Math.cos(angle) * dist * ease;
            const ty = Math.sin(angle) * dist * ease - (40 * t);
            
            p.style.transform = `translate(${tx}px, ${ty}px) scale(${1 - t})`;
            p.style.opacity = (opacity * (1 - t)).toFixed(2);

            if (t < 1) requestAnimationFrame(tick);
            else p.remove();
        });
    }

})();
</script>
""", height=0)

# ─────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────
step_labels = {1: "Job Description", 2: "Bias Analysis", 3: "Rewrite", 4: "Dashboard"}
st.markdown(f"""
<div class="top-bar">
    <span class="top-bar-brand">⚖️ AI Recruitment Bias Auditor</span>
    <span class="top-bar-step">Step {page} / 4 &mdash; {step_labels[page]}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO — page 1 only
# ─────────────────────────────────────────────
if page == 1:
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✦ AI-Powered Fairness Engine</div>
        <h1>Recruitment Bias Auditor</h1>
        <p id="hero-subtitle"></p>
    </div>
    """, unsafe_allow_html=True)
    components.html("""
    <script>
    (function() {
        const text = "Detect hidden bias in job descriptions, generate inclusive language rewrites, and monitor your hiring pipeline for demographic disparities — in one unified platform.";
        const el = window.parent.document.getElementById('hero-subtitle');
        if (!el) return;
        let i = 0;
        function type() {
            if (i < text.length) { el.textContent += text.charAt(i++); setTimeout(type, 20); }
        }
        setTimeout(type, 650);
    })();
    </script>
    """, height=0)

# ─────────────────────────────────────────────
# ══════════════  PAGE 1  ══════════════
# ─────────────────────────────────────────────
if page == 1:
    st.markdown("""
    <div class="glass-card">
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
            </div>
            <h2 class="section-title">Upload Job Description</h2>
        </div>
    """, unsafe_allow_html=True)

    uploaded_jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_jd is not None:
        if st.session_state.uploaded_jd_name != uploaded_jd.name:
            try:
                if uploaded_jd.name.endswith(".pdf"):
                    reader = PyPDF2.PdfReader(uploaded_jd)
                    text = "".join(p.extract_text() + "\n" for p in reader.pages)
                    st.session_state.jd_input = text.strip()
                    st.session_state.jd_input_widget = text.strip()
                elif uploaded_jd.name.endswith(".docx"):
                    doc = Document(uploaded_jd)
                    text = "\n".join(p.text for p in doc.paragraphs)
                    st.session_state.jd_input = text.strip()
                    st.session_state.jd_input_widget = text.strip()
                st.session_state.uploaded_jd_name = uploaded_jd.name
                st.toast("✅ Document parsed successfully!")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    else:
        st.session_state.uploaded_jd_name = None

    def set_sample_jd():
        st.session_state.jd_input = SAMPLE_JD
        st.session_state.jd_input_widget = SAMPLE_JD

    col_input, col_controls = st.columns([3, 1])
    with col_input:
        st.text_area(
            "Paste or edit your job description here",
            placeholder="e.g. We are looking for a young, energetic rockstar developer…",
            height=220,
            key="jd_input_widget",
        )
        st.session_state.jd_input = st.session_state.jd_input_widget

    with col_controls:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📋 Load Example", use_container_width=True, on_click=set_sample_jd)
        analyze_btn = st.button("🔍 Analyze for Bias", use_container_width=True, type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_btn:
        if st.session_state.jd_input.strip():
            with st.spinner("Analyzing semantics and searching for bias patterns..."):
                time.sleep(0.8)
            findings = detect_bias(st.session_state.jd_input)
            st.session_state.jd_findings = findings
            st.session_state.jd_for_rewrite = st.session_state.jd_input
            st.toast("🔍 Analysis Complete!")
            go_to(2)
            st.rerun()
        else:
            st.warning("Please enter or load a job description first.")

    # ── Bottom Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    _, next_col = st.columns([3, 1])
    with next_col:
        if st.button("Next → Bias Analysis", use_container_width=True, key="p1_next"):
            go_to(2)
            st.rerun()


# ─────────────────────────────────────────────
# ══════════════  PAGE 2  ══════════════
# ─────────────────────────────────────────────
elif page == 2:
    st.markdown("""
    <div class="glass-card">
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                  <line x1="11" y1="8" x2="11" y2="14"></line>
                  <line x1="8" y1="11" x2="14" y2="11"></line>
                </svg>
            </div>
            <h2 class="section-title">Bias Detection Results</h2>
        </div>
    """, unsafe_allow_html=True)

    if "jd_findings" not in st.session_state:
        st.info("💡 Go to **Step 1**, paste a job description, and click 'Analyze for Bias'.")
    else:
        findings  = st.session_state.jd_findings
        jd_source = st.session_state.get("jd_for_rewrite", "")
        score     = bias_score(findings)

        badge_map = {
            "high":   ("badge-high",   "🔴 HIGH BIAS DETECTED"),
            "medium": ("badge-medium", "🟡 MEDIUM BIAS DETECTED"),
            "low":    ("badge-low",    "🟢 LOW BIAS / SAFE"),
        }
        badge_cls, badge_label = badge_map[score]
        st.markdown(f"""
        <div style="margin-bottom:24px;display:flex;justify-content:flex-end;">
            <span class="badge {badge_cls}">{badge_label}</span>
        </div>""", unsafe_allow_html=True)

        if findings:
            high_n   = sum(1 for f in findings if f["severity"] == "high")
            medium_n = sum(1 for f in findings if f["severity"] == "medium")
            low_n    = sum(1 for f in findings if f["severity"] == "low")

            st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-val" style="color:var(--status-high-color);">{high_n}</div>
                    <div class="metric-label">High Severity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val" style="color:var(--status-medium-color);">{medium_n}</div>
                    <div class="metric-label">Medium Severity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val" style="color:var(--status-low-color);">{low_n}</div>
                    <div class="metric-label">Low Severity</div>
                </div>
            </div>""", unsafe_allow_html=True)

            highlighted     = highlight_text(jd_source, findings)
            safe_highlighted = highlighted.replace('\n', '<br>')
            st.markdown(f"""
<div style="font-family:'Inter',sans-serif;font-weight:600;font-size:16px;margin-bottom:12px;
     color:var(--text-primary)">Highlighted Document Viewer</div>
<div style="background:rgba(0,0,0,0.2);border:1px solid var(--border-color);border-radius:12px;
     padding:24px;font-size:15px;line-height:1.9;margin-bottom:24px;color:var(--text-secondary);">
{safe_highlighted}
</div>""", unsafe_allow_html=True)

            st.markdown("<p style='font-family:Inter,sans-serif;font-weight:700;font-size:16px;"
                        "margin-bottom:16px;color:var(--text-primary)'>Detailed Breakdowns</p>",
                        unsafe_allow_html=True)
            for f in findings:
                c = ("var(--status-high-color)"   if f["severity"] == "high"
                     else "var(--status-medium-color)" if f["severity"] == "medium"
                     else "var(--status-low-color)")
                sev = f["severity"]
                st.markdown(f"""
                <div class="bias-item">
                    <div class="bias-word" style="color:{c};">"{f['phrase']}"</div>
                    <div>
                        <span class="badge badge-{sev}"
                              style="font-size:10px;padding:3px 10px;margin-bottom:8px;display:inline-flex;">
                            {sev.upper()}
                        </span>
                        <div class="bias-reason">{f['reason']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("🎉 No bias identified! The text appears inclusive and objective.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Bottom Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    prev_col, next_col = st.columns(2)
    with prev_col:
        if st.button("← Job Description", use_container_width=True, key="p2_prev"):
            go_to(1); st.rerun()
    with next_col:
        if st.button("Rewrite →", use_container_width=True, key="p2_next"):
            go_to(3); st.rerun()


# ─────────────────────────────────────────────
# ══════════════  PAGE 3  ══════════════
# ─────────────────────────────────────────────
elif page == 3:
    st.markdown("""
    <div class="glass-card">
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
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
            time.sleep(1)
            rewritten = rewrite_jd(rewrite_input)
            st.session_state.rewritten_jd = rewritten
            st.session_state.animate_rewrite = True

    if "rewritten_jd" in st.session_state:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin:24px 0 16px;">
            <span class="badge badge-low">✅ INCLUSIVE AI OUTPUT</span>
        </div>""", unsafe_allow_html=True)

        if st.session_state.get("animate_rewrite", False):
            safe_jd = (st.session_state.rewritten_jd
                       .replace('`', '\\`').replace('$', '\\$').replace('\\n', '<br>'))
            st.markdown('<div class="rewrite-box" id="typed-output"></div>', unsafe_allow_html=True)
            components.html(f"""
            <script>
                const text = `{safe_jd}`;
                const target = window.parent.document.getElementById('typed-output');
                if (target) {{
                    let i = 0;
                    function typeWriter() {{
                        if (i < text.length) {{
                            if (text.substr(i, 4) === "<br>") {{
                                target.innerHTML += "<br>"; i += 4;
                            }} else {{
                                target.innerHTML += text.charAt(i); i++;
                            }}
                            setTimeout(typeWriter, 5);
                        }}
                    }}
                    typeWriter();
                }}
            </script>""", height=0)
            st.session_state.animate_rewrite = False
        else:
            st.markdown(f'<div class="rewrite-box">{st.session_state.rewritten_jd}</div>',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_copy, col_down = st.columns(2)
        with col_copy:
            safe_copy = (st.session_state.rewritten_jd
                         .replace('`', '\\`').replace('$', '\\$').replace('\\n', '\\n'))
            components.html(f"""
                <button onclick="navigator.clipboard.writeText(`{safe_copy}`); this.innerText='✅ Copied!';"
                style="width:100%;box-sizing:border-box;padding:12px 24px;background:transparent;
                color:#5bb8c4;border:1px solid #5bb8c4;border-radius:6px;cursor:pointer;
                font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
                font-family:'Inter',sans-serif;transition:all 0.3s ease;">
                📋 Copy Text
                </button>""", height=60)
        with col_down:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(0, 7,
                           text=st.session_state.rewritten_jd
                               .encode('latin-1', 'replace').decode('latin-1'))
            pdf_bytes = bytes(pdf.output())
            st.download_button(
                label="⬇️ Download as PDF",
                data=pdf_bytes,
                file_name=f"inclusive_jd_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Bottom Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    prev_col, next_col = st.columns(2)
    with prev_col:
        if st.button("← Bias Analysis", use_container_width=True, key="p3_prev"):
            go_to(2); st.rerun()
    with next_col:
        if st.button("Dashboard →", use_container_width=True, key="p3_next"):
            go_to(4); st.rerun()


# ─────────────────────────────────────────────
# ══════════════  PAGE 4  ══════════════
# ─────────────────────────────────────────────
elif page == 4:
    st.markdown("""
    <div class="glass-card">
        <div class="section-header">
            <div class="section-icon">
                <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="20" x2="18" y2="10"></line>
                  <line x1="12" y1="20" x2="12" y2="4"></line>
                  <line x1="6"  y1="20" x2="6"  y2="14"></line>
                </svg>
            </div>
            <h2 class="section-title">Diversity &amp; Fairness Dashboard</h2>
        </div>
        <p style="color:var(--text-secondary);margin-bottom:24px;">
        Audit historical hiring data using the
        <strong style="color:var(--text-primary);">EEOC 80% Disparate Impact Rule</strong>.
        Test for systemic bias using intersectional demographic groups.
        </p>
    """, unsafe_allow_html=True)

    col_up, col_sample = st.columns([3, 1])
    with col_up:
        uploaded_file = st.file_uploader("Upload Applicant Data (CSV)", type=["csv"])
    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        use_sample = st.button("🗂️ Use Sample Dataset", use_container_width=True)

    df_raw = None
    demo_label   = "Group"
    target_label = "Favorable Rate"

    if use_sample:
        df_raw = pd.read_csv(io.StringIO(SAMPLE_CSV))
        st.success("✅ Loaded pre-formatted sample dataset covering 12 intersectional groups.")
        demo_label   = "Gender"
        target_label = "Hire Rate"
    elif uploaded_file:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            required = {"gender", "applied", "shortlisted", "hired"}
            if required.issubset(set(df_uploaded.columns)):
                st.success(f"✅ Loaded native format with {len(df_uploaded)} rows.")
                df_raw       = df_uploaded
                demo_label   = "Gender"
                target_label = "Hire Rate"
            else:
                st.info("Raw multi-column dataset detected. Configure mapping below:")
                c1, c2, c3 = st.columns(3)
                file_id = getattr(uploaded_file, 'file_id', uploaded_file.name)
                with c1:
                    demo_cols = st.multiselect("Demographic Matrix", options=df_uploaded.columns,
                                               default=[df_uploaded.columns[0]],
                                               key=f"demo_{file_id}")
                with c2:
                    target_col = st.selectbox("Target Funnel Stage", options=df_uploaded.columns,
                                              index=min(1, len(df_uploaded.columns) - 1),
                                              key=f"target_{file_id}")
                with c3:
                    fav_val = st.selectbox("Favorable Label",
                                           options=list(df_uploaded[target_col].dropna().unique()),
                                           key=f"fav_{file_id}")
                if demo_cols:
                    demo_label = " · ".join(demo_cols)
                    df_raw = df_uploaded.copy()
                    df_raw['merged_group'] = df_raw[demo_cols].astype(str).agg(' · '.join, axis=1)
                    df_raw = (df_raw.groupby('merged_group')
                              .agg(applied=(target_col, "count"),
                                   hired=(target_col, lambda x: (x == fav_val).sum()))
                              .reset_index()
                              .rename(columns={"merged_group": "gender"}))
                    df_raw["shortlisted"] = df_raw["hired"]
                else:
                    st.warning("Please align at least one demographic feature.")
        except Exception as e:
            st.error(f"Integrity check failed: {e}")

    if df_raw is not None:
        df_result           = compute_fairness(df_raw)
        verdict, min_di     = overall_fairness_verdict(df_result)
        overall_hire_rate   = (df_result["hired"].sum() / df_result["applied"].sum() * 100
                               if df_result["applied"].sum() > 0 else 0)
        avg_di              = df_result["disparate_impact"].mean()
        v_html              = ('<span class="badge badge-low">✅ SYSTEM FAIRNESS PASS</span>'
                               if verdict == "fair"
                               else '<span class="badge badge-high">⚠️ SYSTEMIC BIAS DETECTED</span>')

        low_c  = "var(--status-low-color)"
        high_c = "var(--status-high-color)"

        st.markdown(f"""<br>
<div style="background:rgba(0,0,0,0.15);border:1px solid var(--border-color);
     border-radius:16px;padding:32px;margin-bottom:24px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <h3 style="font-family:'Outfit',sans-serif;margin:0;">Analytics Overview</h3>
        {v_html}
    </div>
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-val" style="color:var(--accent-primary);">{overall_hire_rate:.1f}%</div>
            <div class="metric-label">Pipeline Yield</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:{low_c if avg_di>=0.8 else high_c};">{avg_di:.2f}</div>
            <div class="metric-label">Mean Equality Ratio</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color:{low_c if min_di>=0.8 else high_c};">{min_di:.2f}</div>
            <div class="metric-label">Min Disparate Impact</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

        if verdict == "biased":
            worst = df_result.loc[df_result['disparate_impact'].idxmin()]
            st.warning(f"**Human Insight**: Candidates in group **'{worst['gender']}'** face systemic "
                       f"adverse impact — equity score {worst['disparate_impact']:.2f} (Target ≥ 0.80).")
        else:
            st.success("**Human Insight**: Pipeline is operating fairly. All groups pass the 80% baseline.")

        tab1, tab2, tab3 = st.tabs(
            [f"📊 Volume by {demo_label}", "📈 Disparate Impact", "📋 Audit Export"]
        )

        with tab1:
            g = (df_result.groupby("gender")
                 .agg(applied=("applied","sum"), hired=("hired","sum"))
                 .reset_index())
            g["hire_rate_pct"] = (g["hired"] / g["applied"] * 100).round(1)
            colors = ["#5bb8c4","#4caf6e","#c8a84b","#c94f5f","#9a6ecf"] * 10
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=g["gender"], y=g["hire_rate_pct"],
                marker=dict(color=colors[:len(g)], line=dict(color="rgba(255,255,255,0.1)", width=1)),
                text=[f"{v}%" for v in g["hire_rate_pct"]], textposition="outside",
                textfont=dict(color="#f0f4f8", size=13, family="'Inter',sans-serif"),
            ))
            fig1.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="'Inter',sans-serif", color="#f0f4f8", size=12),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=demo_label),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=f"{target_label} (%)"),
                margin=dict(l=10,r=10,t=30,b=10), height=360, hovermode="x",
            )
            st.plotly_chart(fig1, use_container_width=True, theme=None)

        with tab2:
            di_df = df_result.copy()
            di_df["group"] = di_df["gender"]
            di_df = di_df.sort_values("disparate_impact")
            bar_colors = ["#c94f5f" if v < 0.8 else "#4caf6e" for v in di_df["disparate_impact"]]
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                y=di_df["group"], x=di_df["disparate_impact"], orientation="h",
                marker=dict(color=bar_colors, line=dict(color="rgba(255,255,255,0.1)", width=1)),
                text=[f"{v:.2f}" for v in di_df["disparate_impact"]], textposition="outside",
                textfont=dict(color="#f0f4f8", size=12, family="'Inter',sans-serif"),
                hovertemplate="<b>%{y}</b><br>Impact Score: %{x}<extra></extra>",
            ))
            fig2.add_vline(x=0.8, line_dash="dash", line_color="#c8a84b", line_width=2,
                           annotation_text=" 80% Threshold",
                           annotation_font_color="#c8a84b", annotation_font_size=12)
            fig2.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="'Inter',sans-serif", color="#f0f4f8", size=12),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0, 1.15],
                           title="Disparate Impact Ratio"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                margin=dict(l=10,r=40,t=10,b=10), height=max(320, len(di_df)*35),
            )
            st.plotly_chart(fig2, use_container_width=True, theme=None)

        with tab3:
            disp = df_result.copy()
            disp["shortlist_rate"] = (disp["shortlist_rate"]*100).round(1).astype(str) + "%"
            disp["hire_rate"]      = (disp["hire_rate"]*100).round(1).astype(str) + "%"
            disp = disp.rename(columns={"gender": demo_label, "disparate_impact": "Disparate Impact"})

            def highlight_di(val):
                try:
                    return ("background-color:rgba(201,79,95,0.2);color:#c94f5f;font-weight:bold;"
                            if float(val) < 0.8 else "")
                except:
                    return ""

            st.dataframe(disp.style.map(highlight_di, subset=["Disparate Impact"]),
                         use_container_width=True, height=350)
            st.download_button("⬇️ Download Full Report",
                               df_result.to_csv(index=False),
                               f"fairness_report_{datetime.now().strftime('%Y%m%d')}.csv",
                               "text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Bottom Nav ──
    st.markdown("<br>", unsafe_allow_html=True)
    prev_col, _ = st.columns([1, 3])
    with prev_col:
        if st.button("← Rewrite", use_container_width=True, key="p4_prev"):
            go_to(3); st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:40px 0 20px;color:var(--text-secondary);font-size:13px;">
    <strong style="color:var(--accent-primary);">AI Recruitment Bias Auditor</strong> — Enterprise Edition
</div>
""", unsafe_allow_html=True)
