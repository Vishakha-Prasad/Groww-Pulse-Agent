import sys
import os
import time
from datetime import datetime, timedelta

from Phase_1_Ingestion.ingestion import fetch_recent_reviews, save_raw_data
from Phase_2_Analysis.analysis import extract_themes
from Phase_3_Outputs.reporting import generate_markdown_note, generate_html_email_draft
from Phase_4_Email.mailing import send_email

def run_pipeline():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Periodic Review Pulse...")
    
    # Phase 1: Ingestion
    reviews = fetch_recent_reviews(app_id="com.nextbillion.groww", weeks=4)
    save_raw_data(reviews)
    
    if not reviews:
        print("No data to process.")
        return

    # Phase 2: Analysis
    themes_data = extract_themes(reviews)
    
    # Phase 3: Reporting
    generate_markdown_note(themes_data)
    email_draft_path = generate_html_email_draft(themes_data)
    
    # Phase 4: Email Automation
    print("\n=== Phase 4: Email Automation ===")
    with open(email_draft_path, "r", encoding='utf-8') as f:
        email_body = f.read()
    
    # Extracting subject
    subject = f"Groww Weekly Pulse | {themes_data['themes'][0]['name'][:30]}..."
    success = send_email(subject, email_body)
    
    if success:
        print("✅ Pipeline executed and email sent.")
    else:
        print("⚠️ Pipeline executed but email failed to send. Check your .env SMTP settings.")

def main():
    print("=== Modularized Review Pulse Pipeline (Scheduled every 5 mins) ===")
    print("Press Ctrl+C to stop the scheduler.")
    
    while True:
        try:
            run_pipeline()
            next_run_time = datetime.now() + timedelta(weeks=1)
            print(f"\nSleeping for 1 week... Zzz (Next run scheduled for {next_run_time.strftime('%Y-%m-%d %H:%M:%S')})")
            time.sleep(60 * 60 * 24 * 7) # 60 * 60 * 24 * 7 seconds = 1 week
        except IndexError:
             # Basic handling for empty themes if LLM fails
             print("Error: Could not extract themes. Retrying in 5 minutes...")
             time.sleep(300)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Retrying in 5 minutes...")
            time.sleep(300)

if __name__ == "__main__":
    main()
