from datetime import datetime
import os

def generate_markdown_note(themes_data, output_path="Weekly_Pulse.md"):
    """
    Phase 3: Generate a premium, scannable one-page note.
    Optimized for Groww Product/Growth/Leadership teams.
    """
    print("Phase 3: Crafting Premium Weekly Pulse Report...")
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # Header with premium styling (consistent with Groww branding colors/vibe)
    md_content = f"""# 📈 Groww Weekly User Pulse
**Period:** Last 4 Weeks | **Generated on:** {date_str}

---

## 🎯 Executive Summary
We have synthesized core user feedback into **{len(themes_data['themes'])} key themes**. Use this pulse to prioritize the roadmap and address friction points in the trading/investing journey.

---

"""
    
    for index, theme in enumerate(themes_data["themes"], start=1):
        md_content += f"### {index}. {theme['legend']} {theme['name'].upper()}\n"
        
        md_content += "**🗣️ Real Voice of Customer:**\n"
        for quote in theme["quotes"][:3]:
            md_content += f"> \"*{quote}*\"\n"
            
        md_content += "\n**💡 Tactical Action Ideas:**\n"
        for idea in theme["action_ideas"][:3]:
            md_content += f"- [ ] {idea}\n"
            
        md_content += "\n---\n\n"
    
    md_content += "\n**Note:** This report is scannable and contains no PII. Share with Product, Support, and Growth teams."
         
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Premium Report generated: {os.path.abspath(output_path)}")

def generate_email_draft(themes_data, output_path="Email_Draft.txt"):
    """
    Phase 3: Generate a professional internal email draft.
    """
    print("Phase 3: Drafting Leadership Email...")
    date_str = datetime.now().strftime("%B %d, %Y")
    
    email_content = f"""Subject: 🚀 [Groww Weekly Pulse] Top User Themes | {date_str}

Hi Product & Growth Teams,

Sharing our weekly pulse on App Store/Play Store sentiment. We've analyzed the last 28 days of reviews and identified the following priority areas:

TOP THEMES THIS WEEK:
"""
    for idx, theme in enumerate(themes_data["themes"], start=1):
        email_content += f"{idx}. {theme['legend']} {theme['name']}\n"
        
    email_content += f"""
View the attached "Weekly_Pulse.md" for deep-dive user quotes and 3 specific action ideas for each theme.

Let's discuss these in our next sync.

Best,
The Groww Prototype Agent
-------------------------------------------
(Generated via Groww Review Pulse Pipeline)
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(email_content)
        
    print(f"✅ Email draft ready: {os.path.abspath(output_path)}")

def generate_html_email_draft(themes_data, output_path="Email_Draft.html"):
    """
    Phase 3: Generate a colorful, poster-themed HTML email.
    Matches Groww's color scheme (#00D09C).
    """
    print("Phase 3: Creating Colorful Poster-Theme Email...")
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # Groww Theme Colors
    groww_green = "#00D09C"
    bg_color = "#F7F9FB"
    card_bg = "#FFFFFF"
    text_color = "#44475B"
    header_text = "#FFFFFF"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Inter', Helvetica, Arial, sans-serif; background-color: {bg_color}; margin: 0; padding: 20px; color: {text_color}; }}
            .container {{ max-width: 600px; margin: 0 auto; background: {card_bg}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
            .header {{ background-color: {groww_green}; padding: 40px 20px; text-align: center; color: {header_text}; }}
            .header h1 {{ margin: 0; font-size: 28px; letter-spacing: -0.5px; }}
            .header p {{ margin: 10px 0 0; opacity: 0.9; font-size: 14px; }}
            .content {{ padding: 30px; }}
            .summary {{ background: #effffb; border-left: 4px solid {groww_green}; padding: 15px; margin-bottom: 25px; border-radius: 4px; }}
            .theme-card {{ border: 1px solid #eee; border-radius: 8px; padding: 20px; margin-bottom: 20px; transition: transform 0.2s; }}
            .theme-title {{ color: {groww_green}; font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; }}
            .legend {{ font-size: 12px; background: #f0f0f0; padding: 2px 8px; border-radius: 20px; margin-left: 10px; color: #666; }}
            .quote {{ font-style: italic; color: #555; background: #fafafa; padding: 10px; border-radius: 6px; margin: 10px 0; border-left: 3px solid #ddd; font-size: 13px; }}
            .actions {{ list-style: none; padding: 0; margin-top: 15px; }}
            .actions li {{ margin-bottom: 8px; font-size: 14px; display: flex; align-items: flex-start; }}
            .actions li::before {{ content: '✅'; margin-right: 10px; font-size: 12px; }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #999; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Groww Review Pulse</h1>
                <p>Weekly Insights & Actionable Feedback • {date_str}</p>
            </div>
            <div class="content">
                <div class="summary">
                    <strong>Hi Team,</strong><br>
                    We've identified <strong>{len(themes_data['themes'])} critical themes</strong> from the last 28 days of user reviews. Here's your weekly health pulse.
                </div>
    """
    
    for theme in themes_data["themes"]:
        html_content += f"""
                <div class="theme-card">
                    <div class="theme-title">
                        {theme['name']} <span class="legend">{theme['legend']}</span>
                    </div>
                    <strong>🗣️ Voice of Customer:</strong>
        """
        for quote in theme["quotes"][:2]:
            html_content += f'<div class="quote">"{quote}"</div>'
            
        html_content += '<ul class="actions">'
        for idea in theme["action_ideas"][:3]:
            html_content += f'<li>{idea}</li>'
        html_content += '</ul></div>'
        
    html_content += f"""
                <div class="footer">
                    Sent via Groww Pulse Automated Pipeline<br>
                    No PII data included • Confidential Internal Report
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"✅ Colorful HTML Email generated: {os.path.abspath(output_path)}")
    return output_path
