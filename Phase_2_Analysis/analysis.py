import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (GEMINI_API_KEY)
load_dotenv()

def extract_themes(reviews_data, max_themes=5):
    """
    Phase 2: Extract themes, quotes, and action ideas using Gemini LLM.
    Falls back to mock data if API key is missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found. Using Mock Data for Phase 2.")
        return get_mock_data(max_themes)

    print(f"Phase 2: Analyzing {len(reviews_data)} reviews via Gemini...")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prepare review text for the prompt
    # Limiting to a reasonable sample if the dataset is massive, though Gemini has high context
    review_sample = ""
    for r in reviews_data[:500]: # Processing top 500 for safety and speed
        review_sample += f"- Rating: {r['rating']}, Text: {r['text']}\n"

    prompt = f"""
    You are a Product Manager at Groww. Analyze the following user reviews from the App Store and Play Store.
    
    Task:
    1. Identify the top {max_themes} themes/issues users are reporting.
    2. For each theme, provide:
       - A descriptive name.
       - A 'legend' (e.g., 🔴 High Severity, 🟠 Medium Severity, 🟡 Needs Clarity, 🟢 Positive).
       - 3 representative real user quotes from the provided list (do not modify them).
       - 3 specific, professional action ideas to address the theme.
    3. Ensure no Personal Identifiable Information (PII) like names or IDs are included.
    4. Format the output as a valid JSON object with a 'themes' key.

    Constraint: Max {max_themes} themes. Keep it scannable.

    Reviews:
    {review_sample}
    """

    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        analysis_result = json.loads(response.text)
        
        # Enforce constraints just in case
        analysis_result["themes"] = analysis_result["themes"][:max_themes]
        print("Phase 2 Complete: Themes extracted via Gemini.")
        return analysis_result
        
    except Exception as e:
        print(f"Error during LLM processing: {e}")
        print("Falling back to Mock Data.")
        return get_mock_data(max_themes)

def get_mock_data(max_themes):
    """Fallback mock data."""
    mock_response = {
        "themes": [
            {
                "name": "App Crashes on Login",
                "legend": "🔴 High Severity",
                "quotes": [
                    "App crashes every time I try to log in.",
                    "Since the last update, I can't even open the app.",
                    "Login screen is broken."
                ],
                "action_ideas": [
                    "Investigate crash logs for the latest release.",
                    "Consider temporary rollback.",
                    "Fix authentication module."
                ]
            },
            {
                "name": "Slow Withdrawal Processing",
                "legend": "🟠 Medium Severity",
                "quotes": [
                    "My withdrawal has been pending for 3 days.",
                    "Takes too long to get my money out.",
                    "Support says 24 hours but it's been 48 hours."
                ],
                "action_ideas": [
                    "Review payment gateway queues.",
                    "Improve in-app status communication.",
                    "Automate status notifications."
                ]
            },
            {
                "name": "Great UI and Easy to Use",
                "legend": "🟢 Positive",
                "quotes": [
                    "Love the new layout, very intuitive.",
                    "Best app for mutual funds, super easy.",
                    "Clean interface."
                ],
                "action_ideas": [
                    "Leverage UI praise in marketing.",
                    "Maintain design language for new features.",
                    "Acknowledge positive sentiment."
                ]
            },
            {
                "name": "Confusing F&O Charges",
                "legend": "🟡 Needs Clarity",
                "quotes": [
                    "The charges for F&O are not clear.",
                    "Hidden fees everywhere.",
                    "Explain the exact breakdown of taxes."
                ],
                "action_ideas": [
                    "Redesign order preview for transparency.",
                    "Create charge explainer tooltips.",
                    "Update FAQ documentation."
                ]
            },
            {
                "name": "Customer Support Response Time",
                "legend": "🔴 High Severity",
                "quotes": [
                    "Raised a ticket 5 days ago, no reply.",
                    "Chatbot is slow to connect to human.",
                    "Support takes too long to resolve issues."
                ],
                "action_ideas": [
                    "Optimize chatbot escalation paths.",
                    "Increase support headcounts for peaks.",
                    "Implement auto-reply with expected ETA."
                ]
            }
        ]
    }
    mock_response["themes"] = mock_response["themes"][:max_themes]
    return mock_response
