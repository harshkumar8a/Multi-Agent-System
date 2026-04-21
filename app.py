import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MULTI AGENT SYSTEM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Full CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist+Mono:wght@300;400;500&family=Geist:wght@300;400;500;600&display=swap');

/* ── CSS Variables ── */
:root {
    --bg:          #06080d;
    --bg-2:        #0c0f17;
    --bg-3:        #111520;
    --surface:     rgba(255,255,255,0.04);
    --border:      rgba(255,255,255,0.07);
    --border-warm: rgba(99,179,255,0.2);
    --text:        #dde3ee;
    --text-dim:    #7a8499;
    --text-faint:  #3d4455;
    --accent:      #4f9eff;
    --accent-2:    #7b5fff;
    --accent-glow: rgba(79,158,255,0.15);
    --green:       #3ecf8e;
    --green-glow:  rgba(62,207,142,0.12);
    --amber:       #f5a623;
    --red:         #ff5f5f;
    --radius:      14px;
    --radius-sm:   8px;
}

/* ── Reset ── */
html, body, [class*="css"] {
    font-family: 'Geist', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 90% 60% at 10% -5%,  rgba(79,158,255,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 90% 100%, rgba(123,95,255,0.06) 0%, transparent 50%),
        radial-gradient(ellipse 50% 40% at 50%  50%, rgba(6,8,13,0)        0%, transparent 100%);
}

/* Animated grid overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2.5rem 5rem;
    max-width: 1280px;
    position: relative;
    z-index: 1;
}

/* ─────────────────────────────────────────
   HERO
───────────────────────────────────────── */
.hero {
    padding: 4rem 0 2rem;
    position: relative;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(79,158,255,0.08);
    border: 1px solid rgba(79,158,255,0.2);
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.5rem;
}

.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

.hero h1 {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 400;
    line-height: 1.0;
    letter-spacing: -0.02em;
    color: #eef1f8;
    margin: 0 0 0.2rem;
}

.hero h1 em {
    font-style: italic;
    background: linear-gradient(135deg, #4f9eff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: var(--text-dim);
    max-width: 460px;
    line-height: 1.7;
    margin-top: 0.8rem;
}

.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.8rem;
}
.stat {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}
.stat-num {
    font-family: 'Instrument Serif', serif;
    font-size: 1.6rem;
    color: #eef1f8;
    line-height: 1;
}
.stat-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-faint);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.stat-divider {
    width: 1px;
    background: var(--border);
    align-self: stretch;
    margin: 0.2rem 0;
}

/* ── Horizontal rule ── */
.hr {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.8rem 0;
}

/* ─────────────────────────────────────────
   INPUT AREA
───────────────────────────────────────── */
.input-section {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

.input-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4f9eff, #7b5fff);
    opacity: 0.6;
}

/* Streamlit input overrides */
.stTextInput > div > div > input {
    background: var(--bg-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: #eef1f8 !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: var(--accent) !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(79,158,255,0.5) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--text-faint) !important;
}
.stTextInput > label {
    font-family: 'Geist Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--accent) !important;
    font-weight: 500 !important;
    margin-bottom: 0.4rem !important;
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #4f9eff 0%, #7b5fff 100%) !important;
    color: #fff !important;
    font-family: 'Geist', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.75rem 1.5rem !important;
    cursor: pointer !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(79,158,255,0.25) !important;
    position: relative !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(79,158,255,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.99) !important;
}

/* ── Chip row ── */
.chips-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.chip-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-faint);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-right: 0.2rem;
}
.chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.25rem 0.85rem;
    font-size: 0.75rem;
    color: var(--text-dim);
    font-family: 'Geist', sans-serif;
    cursor: pointer;
    transition: all 0.15s;
    user-select: none;
    white-space: nowrap;
}
.chip:hover {
    background: rgba(79,158,255,0.08);
    border-color: rgba(79,158,255,0.3);
    color: var(--accent);
    transform: translateY(-1px);
}

/* ─────────────────────────────────────────
   PIPELINE PANEL
───────────────────────────────────────── */
.pipeline-panel {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.6rem;
    position: sticky;
    top: 1.5rem;
}

.pipeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.pipeline-title {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-faint);
}
.pipeline-count {
    font-family: 'Instrument Serif', serif;
    font-size: 1.2rem;
    color: var(--accent);
}

/* Step card */
.step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    border: 1px solid transparent;
    transition: all 0.3s ease;
    position: relative;
}
.step.waiting {
    background: transparent;
    border-color: transparent;
}
.step.running {
    background: rgba(79,158,255,0.06);
    border-color: rgba(79,158,255,0.2);
    animation: step-pulse 2s ease-in-out infinite;
}
.step.done {
    background: var(--green-glow);
    border-color: rgba(62,207,142,0.2);
}

@keyframes step-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(79,158,255,0); }
    50%       { box-shadow: 0 0 0 4px rgba(79,158,255,0.08); }
}

/* Step connector line */
.step-connector {
    width: 1px;
    height: 18px;
    background: var(--border);
    margin: 0 0 0 1.35rem;
    transition: background 0.3s;
}
.step-connector.lit { background: var(--green); opacity: 0.4; }

/* Icon circle */
.step-icon {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    transition: all 0.3s;
}
.step.waiting .step-icon {
    background: var(--bg-3);
    border: 1px solid var(--border);
    color: var(--text-faint);
}
.step.running .step-icon {
    background: rgba(79,158,255,0.15);
    border: 1px solid rgba(79,158,255,0.4);
    color: var(--accent);
}
.step.done .step-icon {
    background: rgba(62,207,142,0.15);
    border: 1px solid rgba(62,207,142,0.4);
    color: var(--green);
}

.step-body { flex: 1; min-width: 0; }
.step-name {
    font-weight: 500;
    font-size: 0.88rem;
    color: var(--text);
    line-height: 1;
    margin-bottom: 0.25rem;
}
.step.waiting .step-name { color: var(--text-faint); }

.step-desc {
    font-size: 0.74rem;
    color: var(--text-faint);
    font-family: 'Geist Mono', monospace;
}
.step.running .step-desc { color: var(--accent); opacity: 0.8; }
.step.done   .step-desc { color: var(--green); opacity: 0.7; }

.step-badge {
    font-family: 'Geist Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.55rem;
    border-radius: 100px;
    flex-shrink: 0;
    align-self: flex-start;
    margin-top: 0.15rem;
}
.badge-waiting { background: var(--bg-3); color: var(--text-faint); }
.badge-running {
    background: rgba(79,158,255,0.12);
    color: var(--accent);
    animation: badge-blink 1.5s ease-in-out infinite;
}
@keyframes badge-blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}
.badge-done { background: rgba(62,207,142,0.12); color: var(--green); }

/* Progress bar */
.progress-bar-wrap {
    margin-top: 1.2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
.progress-bar-label {
    display: flex;
    justify-content: space-between;
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-faint);
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.progress-bar-track {
    height: 3px;
    background: var(--bg-3);
    border-radius: 100px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #4f9eff, #7b5fff);
    border-radius: 100px;
    transition: width 0.6s ease;
}

/* ─────────────────────────────────────────
   RESULTS
───────────────────────────────────────── */
.results-section { margin-top: 1rem; }

.section-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.6rem;
    color: #eef1f8;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Report card */
.report-card {
    background: var(--bg-2);
    border: 1px solid var(--border-warm);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.report-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(79,158,255,0.5), transparent);
}
.report-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.report-card-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
}
.word-count {
    font-family: 'Geist Mono', monospace;
    font-size: 0.63rem;
    color: var(--text-faint);
    letter-spacing: 0.08em;
}

/* Feedback card */
.feedback-card {
    background: var(--bg-2);
    border: 1px solid rgba(62,207,142,0.18);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.feedback-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(62,207,142,0.4), transparent);
}
.feedback-card-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(62,207,142,0.1);
}

/* Raw output cards */
.raw-card {
    background: var(--bg-3);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.raw-card-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-faint);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.raw-card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}
.raw-text {
    font-family: 'Geist Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
    color: var(--text-dim);
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
}
.raw-text::-webkit-scrollbar { width: 4px; }
.raw-text::-webkit-scrollbar-track { background: transparent; }
.raw-text::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Spinner override ── */
.stSpinner > div { color: var(--accent) !important; }

/* ── Expander ── */
details summary {
    font-family: 'Geist Mono', monospace !important;
    font-size: 0.7rem !important;
    color: var(--text-faint) !important;
    letter-spacing: 0.1em !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-dim) !important;
    font-family: 'Geist Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: var(--radius-sm) !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: var(--surface) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.2rem;
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Geist Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-faint) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.6rem 1rem !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    transition: color 0.15s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    background: var(--surface) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 3rem 0 1rem;
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-faint);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Warning ── */
.stAlert { background: rgba(245,166,35,0.06) !important; border-color: rgba(245,166,35,0.25) !important; }

/* ── Success banner ── */
.success-banner {
    background: var(--green-glow);
    border: 1px solid rgba(62,207,142,0.25);
    border-radius: var(--radius);
    padding: 0.9rem 1.4rem;
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: var(--green);
    letter-spacing: 0.06em;
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1.5rem;
    animation: fade-in 0.4s ease;
}
@keyframes fade-in {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Markdown inside result panels */
.report-body h1, .report-body h2, .report-body h3 {
    font-family: 'Instrument Serif', serif;
    color: #eef1f8;
}
.report-body h1 { font-size: 1.8rem; margin-top: 0; }
.report-body h2 { font-size: 1.35rem; }
.report-body h3 { font-size: 1.1rem; }
.report-body p  { color: var(--text-dim); line-height: 1.75; font-size: 0.95rem; }
.report-body a  { color: var(--accent); }
.report-body code {
    background: var(--bg-3);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.1em 0.4em;
    font-family: 'Geist Mono', monospace;
    font-size: 0.85em;
    color: #c5d8ff;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("results", {}), ("running", False), ("done", False), ("last_topic", "")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Helpers ───────────────────────────────────────────────────────────────────
STEPS = [
    ("search", "🔍", "Search Agent",  "Scans web for recent data"),
    ("reader", "📄", "Reader Agent",  "Deep-scrapes top resources"),
    ("writer", "✍️", "Writer Chain",  "Drafts the full report"),
    ("critic", "🧐", "Critic Chain",  "Reviews & scores quality"),
]

def get_step_state(step_key: str) -> str:
    r = st.session_state.results
    if step_key in r:
        return "done"
    if st.session_state.running:
        for k, *_ in STEPS:
            if k not in r:
                return "running" if k == step_key else "waiting"
    return "waiting"

def steps_done() -> int:
    return len(st.session_state.results)

def progress_pct() -> int:
    return (steps_done() * 100) // len(STEPS)

def word_count(text: str) -> str:
    wc = len(text.split())
    mins = max(1, wc // 200)
    return f"{wc:,} words · ~{mins} min read"

def render_pipeline(placeholder):
    r = st.session_state.results
    n_done = steps_done()
    pct = progress_pct()

    html = '<div class="pipeline-panel">'
    html += f'''
    <div class="pipeline-header">
        <span class="pipeline-title">Agent Pipeline</span>
        <span class="pipeline-count">{n_done}/{len(STEPS)}</span>
    </div>'''

    for i, (key, icon, name, desc) in enumerate(STEPS):
        state = get_step_state(key)
        if   state == "running": badge = '<span class="step-badge badge-running">● Running</span>'
        elif state == "done":    badge = '<span class="step-badge badge-done">✓ Done</span>'
        else:                    badge = '<span class="step-badge badge-waiting">Waiting</span>'

        html += f'''
        <div class="step {state}">
            <div class="step-icon">{icon}</div>
            <div class="step-body">
                <div class="step-name">{name}</div>
                <div class="step-desc">{desc}</div>
            </div>
            {badge}
        </div>'''
        if i < len(STEPS) - 1:
            lit = "lit" if state == "done" else ""
            html += f'<div class="step-connector {lit}"></div>'

    html += f'''
    <div class="progress-bar-wrap">
        <div class="progress-bar-label">
            <span>PROGRESS</span>
            <span>{pct}%</span>
        </div>
        <div class="progress-bar-track">
            <div class="progress-bar-fill" style="width:{pct}%"></div>
        </div>
    </div>
    </div>'''

    placeholder.markdown(html, unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_main, col_gap, col_side = st.columns([6, 0.4, 3.4])

with col_main:
    # ── Hero ──
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Multi-Agent AI System</div>
        <h1>Research<em>Mind</em></h1>
        

    </div>
    <div class="hr"></div>
    """, unsafe_allow_html=True)

    # ── Input ──
    # st.markdown('<div class="input-section">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2026",
        key="topic_input",
    )

    col_btn, col_dl = st.columns([3, 1])
    with col_btn:
        run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)



    st.markdown('</div>', unsafe_allow_html=True)

    # ── Results area ──
    results_ph = st.empty()

with col_side:
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    pipeline_ph = st.empty()
    render_pipeline(pipeline_ph)


# ── Trigger run ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️  Please enter a research topic first.")
    else:
        st.session_state.results  = {}
        st.session_state.running  = True
        st.session_state.done     = False
        st.session_state.last_topic = topic.strip()
        st.rerun()


# ── Execute pipeline ──────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.last_topic

    render_pipeline(pipeline_ph)

    # Step 1 — Search
    with st.spinner("🔍  Search Agent is gathering information…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    render_pipeline(pipeline_ph)

    # Step 2 — Reader
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)
    render_pipeline(pipeline_ph)

    # Step 3 — Writer
    with st.spinner("✍️  Writer is drafting the full report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)
    render_pipeline(pipeline_ph)

    # Step 4 — Critic
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()


# ── Display results ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    render_pipeline(pipeline_ph)   # ensure final state shown

    with results_ph.container():
        st.markdown('<div class="results-section">', unsafe_allow_html=True)

        if st.session_state.done:
            topic_label = st.session_state.get("last_topic", "your topic")
            st.markdown(
                f'<div class="success-banner">✓ &nbsp;Research complete — '
                f'<strong>{topic_label}</strong></div>',
                unsafe_allow_html=True,
            )

        # ── Tabs for clean navigation ──
        tab_report, tab_raw, tab_feedback = st.tabs([
            "Final Report",
            "Raw Outputs",
            "Critic Feedback",
        ])

        with tab_report:
            if "writer" in r:
                wc = word_count(r["writer"])
                st.markdown(f"""
                <div class="report-card">
                    <div class="report-card-header">
                        <span class="report-card-label">📝 Research Report</span>
                        <span class="word-count">{wc}</span>
                    </div>
                    <div class="report-body">
                """, unsafe_allow_html=True)
                st.markdown(r["writer"])
                st.markdown("</div></div>", unsafe_allow_html=True)

                col_dl1, col_dl2, _ = st.columns([2, 2, 4])
                with col_dl1:
                    st.download_button(
                        "⬇  Download .md",
                        data=r["writer"],
                        file_name=f"research_{int(time.time())}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )
                with col_dl2:
                    st.download_button(
                        "⬇  Download .txt",
                        data=r["writer"],
                        file_name=f"research_{int(time.time())}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
            else:
                st.info("Report not yet generated — run the pipeline first.")

        with tab_raw:
            has_raw_output = False

            if "search" in r:
                has_raw_output = True
                st.markdown("""
                <div class="raw-card">
                    <div class="raw-card-label">Search Agent Output</div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div class="raw-text">{r["search"]}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if "reader" in r:
                has_raw_output = True
                st.markdown("""
                <div class="raw-card">
                    <div class="raw-card-label">Reader Agent Output</div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div class="raw-text">{r["reader"]}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if not has_raw_output:
                st.info("No raw outputs available yet.")

        with tab_feedback:
            if "critic" in r:
                st.markdown("""
                <div class="feedback-card">
                    <div class="feedback-card-label">🧐 Critic Feedback & Score</div>
                """, unsafe_allow_html=True)
                st.markdown(r["critic"])
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Critic feedback not yet available — run the pipeline first.")

        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    createdby: Harsh Kumar &nbsp;·&nbsp; Multi-agent pipeline powered by LangChain &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
