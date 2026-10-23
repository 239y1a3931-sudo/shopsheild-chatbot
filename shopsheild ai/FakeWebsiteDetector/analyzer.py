from detector import analyze_website
from ollama_chat import explain_result

def analyze_with_ai(url):

    features = analyze_website(url)

    return explain_result(features)