import requests

def explain_result(features):

    prompt = f"""
You are a cybersecurity assistant.

Analyze this shopping website:

HTTPS Enabled: {features['https']}
Status Code: {features['status_code']}
Contact Page Found: {features['has_contact']}
Refund Policy Found: {features['has_refund']}

Provide:
1. Risk Score (Low/Medium/High)
2. Short Explanation
3. Recommendation
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]