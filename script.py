import requests
import os
import time
from pathlib import Path
from bs4 import BeautifulSoup
import cohere

# === Configuration ===
SAVE_DIR = "Leetcode"
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "skrFfXlbJwf9Bi89hiPjUWMTGegJ0TqutFPDBUlb"
co = cohere.Client(COHERE_API_KEY)

# === Problem Numbers to Process ===
PROBLEM_NUMBERS = [
    23, 215, 239, 253, 347, 373, 621, 862,
    814, 543, 257, 236, 979, 331, 701, 98,
    938, 199
]

# === Helper Functions ===
def get_slug_and_title_from_number(problem_number):
    metadata = requests.get("https://leetcode.com/api/problems/all/").json()
    for question in metadata['stat_status_pairs']:
        if question['stat']['frontend_question_id'] == problem_number:
            slug = question['stat']['question__title_slug']
            title = question['stat']['question__title']
            return slug, title
    return None, None

def get_cpp_snippet(slug):
    graphql_url = "https://leetcode.com/graphql"
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            content
            codeSnippets {
                lang
                code
            }
        }
    }
    """
    response = requests.post(graphql_url, json={
        "query": query,
        "variables": {"titleSlug": slug}
    })

    data = response.json()
    question_data = data.get("data", {}).get("question", None)
    if not question_data:
        print("❌ Could not fetch question data (possibly premium):", slug)
        return None, None

    snippets = question_data.get("codeSnippets", [])
    if not snippets:
        print("❌ No code snippets found for:", slug)
        return None, None

    cpp_snippet = next((s['code'] for s in snippets if s['lang'] == 'C++'), None)
    if not cpp_snippet:
        print(f"❌ No C++ snippet found for problem: {slug}")
        return None, None

    content = question_data.get("content", "")
    return cpp_snippet, content

def generate_cpp_solution_with_cohere(description_text, snippet):
    prompt = (
        f"Write only the complete and correct C++ solution for the following LeetCode problem.\n\n"
        f"Problem Description:\n{description_text}\n\n"
        f"Start from this C++ code snippet:\n{snippet}\n\n"
        f"Respond ONLY with the complete C++ code. No explanations, no comments, no markdown formatting."
    )

    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=1000,
        temperature=0.3,
        stop_sequences=["```", "<end>"]
    )

    if response.generations and response.generations[0].text.strip():
        return response.generations[0].text.strip()
    else:
        return "// Cohere did not return a valid solution."

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in "-_ " else "" for c in name).replace(" ", "")

def save_solution(problem_number, problem_title, solution_code):
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
    sanitized_title = sanitize_filename(problem_title)
    file_name = f"{problem_number}-{sanitized_title}.cpp"
    file_path = Path(SAVE_DIR) / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(solution_code)
    print(f"✅ Saved solution to {file_path}")

# === Main Flow ===
def main():
    for i, problem_number in enumerate(PROBLEM_NUMBERS):
        print(f"\n🚀 Processing Problem #{problem_number} ({i + 1}/{len(PROBLEM_NUMBERS)})")

        title_slug, problem_title = get_slug_and_title_from_number(problem_number)
        if not title_slug:
            print("❌ Problem number not found.")
            continue

        snippet, description_html = get_cpp_snippet(title_slug)
        if not snippet or not description_html:
            print("⚠️ Skipping due to missing snippet or content (possibly premium).")
            continue

        description_text = BeautifulSoup(description_html, "html.parser").get_text()
        ai_solution = generate_cpp_solution_with_cohere(description_text, snippet)

        if ai_solution.startswith("// Cohere did not return"):
            print("⚠️ Skipping due to empty AI response.")
            continue

        save_solution(problem_number, problem_title, ai_solution)

        if i < len(PROBLEM_NUMBERS) - 1:
            print("⏳ Waiting 10 seconds before next problem...")
            time.sleep(10)

if __name__ == "__main__":
    main()
