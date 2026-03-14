import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, body_text):
    """
    Phase 4: Sends an email using SMTP with dual-port fallback (SSL/TLS).
    """
    try:
        import streamlit as st
        # Try to get from Streamlit Secrets first on Cloud
        s = st.secrets
    except:
        s = {}

    smtp_host = os.getenv("SMTP_HOST") or s.get("SMTP_HOST")
    smtp_user_raw = os.getenv("SMTP_USER") or s.get("SMTP_USER")
    smtp_pass_raw = os.getenv("SMTP_PASS") or s.get("SMTP_PASS")
    recipient_raw = os.getenv("RECIPIENT_EMAIL") or s.get("RECIPIENT_EMAIL")

    smtp_user = smtp_user_raw.strip() if smtp_user_raw else None
    smtp_pass = smtp_pass_raw.strip().replace(" ", "") if smtp_pass_raw else None
    recipient = recipient_raw.strip() if recipient_raw else None

    if not all([smtp_host, smtp_user, smtp_pass, recipient]):
        print(f"WARNING: Phase 4 skipped. Incomplete SMTP configuration. Host: {smtp_host}, User: {smtp_user}, Pass: {'****' if smtp_pass else None}, Recipient: {recipient}")
        return False

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'html'))

    # Configuration sets to try
    configs = [
        {"port": 465, "use_ssl": True},
        {"port": 587, "use_ssl": False}
    ]

    for config in configs:
        port = config["port"]
        use_ssl = config["use_ssl"]
        print(f"Phase 4: Attempting Port {port} ({'SSL' if use_ssl else 'TLS'})...")
        
        try:
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_host, port, timeout=10)
            else:
                server = smtplib.SMTP(smtp_host, port, timeout=10)
                server.starttls()
            
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent successfully via Port {port}!")
            return True
        except Exception as e:
            print(f"❌ Port {port} failed: {e}")
            continue # Try next port

    print("⚠️ All email delivery attempts failed.")
    return False

if __name__ == "__main__":
    # Test send
    send_email("Test Pulse", "This is a test of the Groww Review Pulse email system.")
