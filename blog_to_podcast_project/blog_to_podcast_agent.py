import requests
import urllib3
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Custom CSS ──────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --ink:    #0d0d0d;
    --paper:  #f5f0e8;
    --cream:  #ede8dc;
    --rust:   #c0392b;
    --gold:   #b8860b;
    --muted:  #6b6560;
    --border: #c8c0b0;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--paper) !important;
    font-family: 'DM Mono', monospace !important;
    color: var(--ink) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: 3px solid var(--rust) !important;
}
[data-testid="stSidebar"] * {
    color: var(--paper) !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stSidebar"] input {
    background: #1a1a1a !important;
    border: 1px solid #444 !important;
    color: var(--paper) !important;
    border-radius: 0 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #444 !important;
    border-radius: 0 !important;
    color: var(--paper) !important;
}

/* Hero title */
.hero-block {
    border-top: 4px double var(--ink);
    border-bottom: 4px double var(--ink);
    padding: 2rem 0 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--rust);
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 6vw, 4.2rem);
    font-weight: 900;
    line-height: 1.05;
    color: var(--ink);
    margin: 0;
}
.hero-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    margin-top: 0.75rem;
}
.rule-ornament {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0;
    color: var(--border);
    font-size: 0.8rem;
}
.rule-ornament::before,
.rule-ornament::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* URL input */
[data-testid="stTextInput"] input {
    background: white !important;
    border: 2px solid var(--ink) !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    color: var(--ink) !important;
    padding: 0.75rem 1rem !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
    transition: box-shadow 0.15s ease !important;
}
[data-testid="stTextInput"] input:focus {
    box-shadow: 6px 6px 0 var(--rust) !important;
    border-color: var(--rust) !important;
    outline: none !important;
}

/* Generate button */
[data-testid="stButton"] > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    border: 2px solid var(--ink) !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2.5rem !important;
    box-shadow: 4px 4px 0 var(--rust) !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover:not(:disabled) {
    background: var(--rust) !important;
    border-color: var(--rust) !important;
    box-shadow: 6px 6px 0 var(--ink) !important;
    transform: translate(-2px, -2px) !important;
}
[data-testid="stButton"] > button:disabled {
    opacity: 0.35 !important;
    box-shadow: none !important;
}

/* Step badges */
.step-badge {
    display: inline-block;
    background: var(--ink);
    color: var(--paper);
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    margin-bottom: 0.5rem;
}
.step-badge.active { background: var(--rust); }
.step-badge.done   { background: var(--gold); color: var(--ink); }

/* Audio player */
[data-testid="stAudio"] {
    background: var(--cream) !important;
    border: 2px solid var(--ink) !important;
    border-radius: 0 !important;
    padding: 1rem !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--rust) !important;
    border: 2px solid var(--rust) !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    box-shadow: 3px 3px 0 var(--rust) !important;
    transition: all 0.15s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: var(--rust) !important;
    color: white !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 5px 5px 0 var(--ink) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    background: white !important;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
}

/* Success / warning / error */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-left: 4px solid currentColor !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Spinner */
[data-testid="stSpinner"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
}

/* Code blocks in log */
code, pre {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    background: #1a1a1a !important;
    color: #a8d8a8 !important;
    border-radius: 0 !important;
}

/* Sidebar header */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.1rem !important;
    border-bottom: 1px solid #333 !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 1rem !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
"""


def scrape_blog(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        if len(text.strip()) >= 100:
            return text[:8000], "direct"
    except Exception:
        pass

    jina_url = f"https://r.jina.ai/{url}"
    resp = requests.get(jina_url, headers={"Accept": "text/plain"}, timeout=20)
    resp.raise_for_status()
    return resp.text[:8000], "jina"


# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blog to Podcast",
    page_icon="🎙️",
    layout="centered",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-…")
    base_url = st.text_input(
        "Base URL",
        value="https://api.openai.com/v1",
        help="Change to your proxy endpoint",
    )
    voice = st.selectbox(
        "Voice",
        ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        index=4,
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#555;font-size:0.65rem;letter-spacing:0.08em'>"
        "POWERED BY GPT-4O-MINI · TTS</small>",
        unsafe_allow_html=True,
    )

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-block">
        <div class="hero-eyebrow">AI Agent · Audio Edition</div>
        <h1 class="hero-title">Blog&nbsp;to&nbsp;Podcast</h1>
        <div class="hero-subtitle">Paste a URL · Get a listenable summary · Download &amp; go</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── URL input ────────────────────────────────────────────────────────────────
url = st.text_input("", placeholder="https://example.com/some-great-article", label_visibility="collapsed")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

generate = st.button("▶  Generate Podcast", disabled=not openai_key)

# ── Pipeline ─────────────────────────────────────────────────────────────────
if generate:
    if not url.strip():
        st.warning("Please enter a blog URL.")
        st.stop()

    client = OpenAI(api_key=openai_key, base_url=base_url)

    with st.expander("API log", expanded=True):
        api_log = st.empty()
    log_lines: list[str] = []

    def log(msg: str) -> None:
        log_lines.append(msg)
        api_log.code("\n".join(log_lines), language="text")

    # Step 1 — scrape
    with st.spinner("Fetching article…"):
        try:
            blog_text, method = scrape_blog(url)
            log(f"✓ scraped via {method} — {len(blog_text)} chars")
        except Exception as e:
            st.error(f"Could not fetch URL: {e}")
            st.stop()

    if len(blog_text.strip()) < 100:
        st.error("Not enough text extracted. The site may block scrapers or require JavaScript.")
        st.stop()

    # Step 2 — summarise
    with st.spinner("Summarising with gpt-4o-mini…"):
        try:
            log(f"→ POST {base_url.rstrip('/')}/chat/completions  model=gpt-4o-mini")
            chat_resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Create a concise, engaging podcast summary (max 2000 characters). "
                            "Be conversational and capture the main points. "
                            "Return only the summary text."
                        ),
                    },
                    {"role": "user", "content": f"Summarize this blog for a podcast:\n\n{blog_text}"},
                ],
            )
            summary = chat_resp.choices[0].message.content.strip()
            u = chat_resp.usage
            log(f"✓ summary — {len(summary)} chars  tokens: {u.prompt_tokens}+{u.completion_tokens}={u.total_tokens}")
        except Exception as e:
            log(f"✗ summarisation failed: {e}")
            st.error(f"Summarisation failed: {e}")
            st.stop()

    # Step 3 — TTS
    with st.spinner("Generating audio…"):
        try:
            log(f"→ POST {base_url.rstrip('/')}/audio/speech  model=gpt-4o-mini-tts  voice={voice}")
            tts_resp = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=summary,
            )
            audio_bytes = tts_resp.content
            log(f"✓ audio — {len(audio_bytes):,} bytes  ({len(summary)} TTS chars)")
        except Exception as e:
            log(f"✗ TTS failed: {e}")
            st.error(f"TTS failed: {e}")
            st.stop()

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='rule-ornament'>✦ your podcast is ready ✦</div>",
        unsafe_allow_html=True,
    )
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button("↓  Download podcast.mp3", audio_bytes, "podcast.mp3", "audio/mp3")

    with st.expander("Podcast transcript"):
        st.markdown(
            f"<p style='font-family:DM Mono,monospace;font-size:0.82rem;line-height:1.7;color:#333'>{summary}</p>",
            unsafe_allow_html=True,
        )
