import requests
from detector import analyze_website

def chat_with_ai(message):

    # Website Analysis Mode
    if "http" in message or "www." in message:

        url = message.replace("analyze", "").strip()

        features = analyze_website(url)

        if not features["https"]:
            risk = "High"
        elif features["status_code"] != 200:
            risk = "Medium"
        elif not features["has_contact"] and not features["has_refund"]:
            risk = "Medium"
        else:
            risk = "Low"

        response = f"""
🔍 Website Analysis

URL: {url}

Risk Score: {risk}

Checks Performed:
• HTTPS Enabled: {features['https']}
• Status Code: {features['status_code']}
• Contact Page Found: {features['has_contact']}
• Refund Policy Found: {features['has_refund']}

Summary:
"""

        if risk == "Low":
            response += """
This website passed the basic trust checks. It appears relatively trustworthy, but always verify reviews before purchasing.
"""
        elif risk == "Medium":
            response += """
Some trust indicators are missing. Verify reviews, seller information, and payment methods before purchasing.
"""
        else:
            response += """
Important trust indicators are missing. Avoid entering personal or payment information until the website is verified.
"""

        return response

    # Normal Chat Mode
    else:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": f"""
You are CatBot, a helpful cybersecurity assistant specializing in fake shopping websites.

Answer clearly and simply:

{message}
""",
                "stream": False
            }
        )

        return response.json()["response"]
