import requests

def analyze_website(url):

    if not url.startswith("http"):
        url = "https://" + url

    result = {}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        result["https"] = url.startswith("https")
        result["status_code"] = response.status_code

        html = response.text.lower()

        result["has_contact"] = "contact" in html
        result["has_refund"] = "refund" in html

    except Exception as e:

        print("Error:", e)

        result["https"] = url.startswith("https")
        result["status_code"] = "Error"
        result["has_contact"] = False
        result["has_refund"] = False

    return result