"""
AgroSpectra AI - design system (replaces your old styles.py).
Light "field notes" theme: deep forest ink on pale sage, golden-hour amber accent.
Every text colour is set explicitly so nothing can turn invisible.
"""


def apply_custom_styles() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Public+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg: #F6F8F3;
    --surface: #FFFFFF;
    --sage: #EAF0E5;
    --ink: #16301F;
    --muted: #4F6256;
    --line: #DCE5D8;
    --green: #2F6B3F;
    --green-dark: #1D4A2B;
    --amber: #C98A1B;
}

/* ---------- Base: force readable text everywhere ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--ink) !important;
    font-family: 'Public Sans', system-ui, sans-serif;
}
.stApp p, .stApp li, .stApp span, .stApp label, .stApp div { color: inherit; }
.stMarkdown p, .stCaption, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
h1, h2, h3, h4 {
    font-family: 'Fraunces', Georgia, serif !important;
    color: var(--ink) !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em;
}
hr { border-color: var(--line) !important; }

/* CHANGED: was 2.2rem. Streamlit's top header bar is about 3.75rem tall,
   so 2.2rem hid the top edge of the first banner behind it.
   4.5rem keeps the whole banner (and its top border) visible. */
.block-container { padding-top: 4.5rem !important; max-width: 1180px; }

/* ---------- Top header bar (was black) ---------- */
[data-testid="stHeader"] {
    background: rgba(246, 248, 243, 0.92) !important;
    backdrop-filter: blur(6px);
}
[data-testid="stHeader"] *, [data-testid="stToolbar"] * { color: var(--ink) !important; }
[data-testid="stDecoration"] { display: none; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--sage) !important;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * { color: var(--ink); }
[data-testid="stSidebar"] h2 { font-size: 1.3rem !important; }

/* Navigation radio -> clean nav list */
[data-testid="stSidebar"] div[role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 9px 12px;
    width: 100%;
    cursor: pointer;
    transition: background .15s ease;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: rgba(47,107,63,.08); }
/* hide the dot */
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none !important; }
[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    color: var(--ink) !important;
    font-size: 0.94rem;
    font-weight: 500;
}
/* active page */
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: var(--green);
    border-color: var(--green);
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 600;
}

.nature-divider { height: 1px; background: var(--line); margin: 4px 0 16px 0; }

/* ---------- Hero banner with aerial photo ---------- */
.hero-container {
    position: relative;
    width: 100%;
    height: 350px;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(22, 48, 31, .18);
    border: 1px solid var(--line);
    background: linear-gradient(135deg, #16301F 0%, #254D38 50%, #2F6B3F 100%);
}
.hero-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    object-fit: cover !important;
    object-position: center 42% !important;
    display: block !important;
    margin: 0 !important;
    padding: 0 !important;
}
.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, rgba(16, 40, 25, 0.84) 0%, rgba(16, 40, 25, 0.50) 50%, rgba(16, 40, 25, 0.15) 100%);
    pointer-events: none;
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 38px 44px;
}
.hero-banner {
    position: relative;
    min-height: 350px;
    border-radius: 14px;
    overflow: hidden;
    padding: 48px 44px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background-size: cover, cover !important;
    background-position: center 48%, center 48% !important;
    background-repeat: no-repeat, no-repeat !important;
    background-color: var(--green-dark);
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(22, 48, 31, .18);
    border: 1px solid var(--line);
}
.hero-eyebrow {
    color: #F7D58B !important;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 8px;
    text-shadow: 0 1px 4px rgba(0,0,0,.45);
}
.hero-title {
    font-family: 'Fraunces', Georgia, serif;
    color: #FFFFFF !important;
    font-size: 3.2rem;
    font-weight: 600;
    line-height: 1.05;
    margin-bottom: 10px;
    text-shadow: 0 2px 14px rgba(0,0,0,.45);
}
.hero-description {
    color: #F1F5EE !important;
    font-size: 1.05rem;
    line-height: 1.55;
    max-width: 580px;
    text-shadow: 0 1px 8px rgba(0,0,0,.45);
}
.hero-header { margin: 4px 0 18px 0; }
.hero-subtitle { color: var(--muted) !important; font-size: 1rem; max-width: 720px; line-height: 1.55; }

/* ---------- Cards ---------- */
.nature-card, .nature-card-sm, .feature-card, .metric-box {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px 22px;
    height: 100%;
}
.nature-card { margin-bottom: 12px; }
.nature-card-sm { padding: 18px 20px; }
.nature-card h3, .nature-card p { margin-bottom: 4px; }
.nature-card p, .feature-description, .metric-sub, .nature-card-sm p, .feature-card p {
    color: var(--muted) !important;
    font-size: .92rem;
    line-height: 1.55;
}
.metric-box { border-left: 4px solid var(--green); }
.metric-label { color: var(--muted) !important; font-size: .74rem; font-weight: 700; letter-spacing: .07em; }
.metric-value {
    font-family: 'Fraunces', Georgia, serif;
    color: var(--ink) !important;
    font-size: 2.1rem;
    font-weight: 600;
    margin: 6px 0 4px 0;
}
.feature-icon { font-size: 1.6rem; margin-bottom: 8px; }
.feature-title { color: var(--ink) !important; font-weight: 600; font-size: 1.05rem; margin-bottom: 6px; }

/* ---------- Disclosure banner ---------- */
.disclosure-banner {
    background: #FBF4E4;
    border: 1px solid #EBD9AE;
    border-left: 4px solid var(--amber);
    border-radius: 10px;
    padding: 18px 22px;
    margin: 8px 0 24px 0;
    color: var(--ink) !important;
    font-size: .93rem;
    line-height: 1.6;
}
.disclosure-banner * { color: var(--ink) !important; }
.disclosure-title { font-weight: 700; margin-bottom: 6px; }

/* ---------- Pills ---------- */
.pill-badge {
    display: inline-block;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: .75rem;
    font-weight: 600;
    border: 1px solid var(--line);
    background: var(--sage);
    color: var(--ink) !important;
}
.pill-success { background: #E3F2E5; border-color: #B9DDBE; color: #1D5E2B !important; }

/* ---------- Widgets (uploaders, inputs, buttons, tabs) ---------- */
[data-testid="stFileUploader"] section { background: var(--surface); border: 1px dashed #B9C9B4; }
[data-testid="stFileUploader"] * { color: var(--ink) !important; }
.stButton > button, .stDownloadButton > button {
    background: var(--green); color: #fff !important; border: none; border-radius: 8px; font-weight: 600;
}
.stButton > button:hover { background: var(--green-dark); }
.stTabs [data-baseweb="tab"] { color: var(--muted); }
.stTabs [aria-selected="true"] { color: var(--green-dark) !important; }
[data-testid="stAlert"] * { color: inherit !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: var(--ink) !important; }

@media (max-width: 720px) {
    .hero-banner { padding: 32px 22px; min-height: 300px; }
    .hero-title { font-size: 2.3rem; }
}
</style>
"""
