import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def debug_smtp():
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", 587))
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS").strip().replace(" ", "") if os.getenv("SMTP_PASS") else None
    
    print(f"Connecting to {host}:465 (SSL) as {user}...")
    try:
        server = smtplib.SMTP_SSL(host, 465)
        server.set_debuglevel(1)
        print("Logging in...")
        server.login(user, pwd)
        print("✅ Login Success!")
        server.quit()
    except Exception as e:
        print(f"❌ Login Failed: {e}")

if __name__ == "__main__":
    debug_smtp()
