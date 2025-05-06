import requests
import os
import time
from pathlib import Path
from bs4 import BeautifulSoup
import cohere

# === Configuration ===
SAVE_DIR = "Hackerrank"
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "skrFfXlbJwf9Bi89hiPjUWMTGegJ0TqutFPDBUlb"
co = cohere.Client(COHERE_API_KEY)

# === List of Problem URLs ===
HACKERRANK_PROBLEMS = [
    "https://www.hackerrank.com/challenges/consecutive-subsequences",
    "https://www.hackerrank.com/challenges/find-the-running-median",
    "https://www.hackerrank.com/challenges/sansa-and-xor",
    "https://www.hackerrank.com/challenges/sam-and-substrings",
    "https://www.hackerrank.com/challenges/non-divisible-subset",
    "https://www.hackerrank.com/challenges/special-multiple",
    "https://www.hackerrank.com/challenges/highest-value-palindrome",
    "https://www.hackerrank.com/challenges/acm-icpc-team",
    "https://www.hackerrank.com/challenges/fair-rations",
    "https://www.hackerrank.com/challenges/queens-attack-2",
    "https://www.hackerrank.com/challenges/candies",
    "https://www.hackerrank.com/challenges/truck-tour"
]

# === Helper Functions ===
def get_problem_description_from_url(problem_url):
    """Fetch problem description from a HackerRank URL."""
    response = requests.get(problem_url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch problem data from {problem_url} (Status Code: {response.status_code})")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    description_div = soup.find("div", class_="problem-description__content")
    
    # Debugging output
    if description_div:
        print("✔️ Problem description found!")
        return description_div.get_text(strip=True)
    else:
        print(f"❌ Could not find description for {problem_url}")
        # Optionally print the soup content for more debugging
        print(soup.prettify())
        return None


def generate_cpp_solution_with_cohere(description_text):
    """Generate C++ solution code using Cohere AI."""
    prompt = (
        f"Write only the complete and correct C++ solution for the following HackerRank problem.\n\n"
        f"Problem Description:\n{description_text}\n\n"
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
    """Sanitize problem name to use it as a filename."""
    return "".join(c if c.isalnum() or c in "-_ " else "" for c in name).replace(" ", "")

def save_solution(problem_url, solution_code):
    """Save the solution to a file."""
    problem_name = problem_url.split("/")[-1]  # Use last part of the URL as the problem name
    sanitized_name = sanitize_filename(problem_name)
    file_name = f"{sanitized_name}.cpp"
    file_path = Path(SAVE_DIR) / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(solution_code)
    print(f"✅ Saved solution to {file_path}")

# === Main Flow ===
def main():
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)  # Ensure save directory exists

    for i, problem_url in enumerate(HACKERRANK_PROBLEMS):
        print(f"\n🚀 Processing Problem {i + 1}/{len(HACKERRANK_PROBLEMS)}: {problem_url}")

        description_text = get_problem_description_from_url(problem_url)
        if not description_text:
            print("⚠️ Skipping due to missing description.")
            continue

        ai_solution = generate_cpp_solution_with_cohere(description_text)

        if ai_solution.startswith("// Cohere did not return"):
            print("⚠️ Skipping due to empty AI response.")
            continue

        save_solution(problem_url, ai_solution)

        if i < len(HACKERRANK_PROBLEMS) - 1:
            print("⏳ Waiting 10 seconds before next problem...")
            time.sleep(10)

if __name__ == "__main__":
    main()
