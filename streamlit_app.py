import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from Phase_1_Ingestion.ingestion import fetch_recent_reviews, save_raw_data
from Phase_2_Analysis.analysis import extract_themes
from Phase_3_Outputs.reporting import generate_markdown_note, generate_html_email_draft
from Phase_4_Email.mailing import send_email

# Page configuration
st.set_page_config(
    page_title="Groww Pulse 3.0",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for Groww Branding
st.markdown("""
    <style>
    .main { background-color: #F7F9FB; }
    .stButton>button { background-color: #00D09C; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }
    .stButton>button:hover { background-color: #00b085; color: white; }
    .groww-header { color: #00D09C; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

def run_pulse_logic():
    with st.status("🚀 Initializing Groww Pulse Pipeline...", expanded=True) as status:
        try:
            # Phase 1
            st.write("📁 Phase 1: Ingesting App Store & Play Store Reviews...")
            reviews = fetch_recent_reviews()
            save_raw_data(reviews)
            
            # Phase 2
            st.write("🧠 Phase 2: Analyzing sentiment with Gemini AI...")
            themes_data = extract_themes(reviews)
            
            # Phase 3
            st.write("📊 Phase 3: Generating reports and posters...")
            generate_markdown_note(themes_data)
            html_path = generate_html_email_draft(themes_data)
            
            # Phase 4
            st.write("📧 Phase 4: Dispatching Email Pulse...")
            with open(html_path, "r", encoding='utf-8') as f:
                html_body = f.read()
            
            success = send_email(f"🚀 Groww Pulse | {datetime.now().strftime('%B %d')}", html_body)
            
            if success:
                status.update(label="✅ Pulse Completed Successfully!", state="complete", expanded=False)
                st.success("Email sent successfully to the configured recipient!")
            else:
                status.update(label="⚠️ Pulse Completed with Email Issue", state="error", expanded=False)
                st.warning("The report was generated, but the email failed to send. Please check your **Streamlit Secrets** (SMTP_USER, SMTP_PASS, etc.).")
                st.info("💡 Tip: Ensure you are using an **App Password** for Gmail, not your regular password.")
            
            return themes_data, html_path
        except Exception as e:
            status.update(label="❌ Pipeline Error", state="error", expanded=True)
            st.error(f"An unexpected error occurred: {e}")
            return None, None

# Sidebar / Config
st.sidebar.image("https://groww.in/logo-groww-dark.611409.svg", width=120)
st.sidebar.title("Configuration")

# Secrets Diagnostic
st.sidebar.subheader("Environment Check")
keys_to_check = ["GEMINI_API_KEY", "SMTP_USER", "SMTP_PASS", "RECIPIENT_EMAIL"]
env_status = {}
for key in keys_to_check:
    # Check os.environ (for local) and st.secrets (for Cloud)
    val = os.getenv(key) or st.secrets.get(key)
    env_status[key] = "✅ Found" if val else "❌ Missing"

for key, stat in env_status.items():
    st.sidebar.write(f"**{key}:** {stat}")

if any(v == "❌ Missing" for v in env_status.values()):
    st.sidebar.warning("Some configuration values are missing. The app might not function correctly.")

if st.sidebar.button("Refresh Config & Reset"):
    st.rerun()

# Main UI
st.markdown("<h1 class='groww-header'>Groww Review Pulse</h1>", unsafe_allow_html=True)
st.markdown("### Executive Intelligence from App Reviews")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("Welcome to the **Groww Pulse Dashboard**. This tool automatically fetches, analyzes, and dispatches weekly insights directly from your users.")
    if st.button("▶️ Trigger Weekly Pulse Now"):
        themes, html_file = run_pulse_logic()
        
        if themes:
            st.divider()
            st.subheader("Latest Themes Extracted")
            for theme in themes['themes']:
                with st.expander(f"{theme['legend']} {theme['name']}"):
                    st.write("**Quotes:**")
                    for q in theme['quotes']:
                        st.info(f"\"{q}\"")
                    st.write("**Actions:**")
                    for a in theme['action_ideas']:
                        st.write(f"- {a}")

with col2:
    st.subheader("System Overview")
    st.info("""
    - **Injesting**: 1000+ Recent Reviews
    - **AI Engine**: Gemini 1.5 Flash
    - **Frequency**: On-Demand (Manual) or Weekly Automation
    """)
    
    if os.path.exists("Weekly_Pulse.md"):
        with open("Weekly_Pulse.md", "r") as f:
            st.download_button("📥 Download Latest Markdown Report", f.read(), "Weekly_Pulse.md")

st.markdown("---")
st.caption("Version: Groww Pulse 3.0 (Streamlit Edition)")
