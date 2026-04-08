# github_issue_analyzer.py
"""
AI GitHub Issue Analyzer
- Fetches open issues from a GitHub repo
- Categorizes them using OpenAI GPT
- Generates an Excel report
"""

from github import Github, Auth, GithubException
import openai
import pandas as pd
import os
from config import (
    GITHUB_TOKEN,
    REPO_NAME,
    OPENAI_API_KEY,
    REPORT_FOLDER,
    REPORT_FILENAME,
)

# ==========================
# Setup OpenAI
# ==========================
openai.api_key = OPENAI_API_KEY


# ==========================
# FUNCTION: Fetch Open Issues
# ==========================
def fetch_issues(repo_name):
    g = Github(auth=Auth.Token(GITHUB_TOKEN))
    try:
        repo = g.get_repo(repo_name)
    except GithubException.UnknownObjectException:
        raise RuntimeError(
            f"GitHub repository not found or inaccessible: '{repo_name}'. "
            "Check REPO_NAME in config.py and ensure your token has repo access."
        )
    issues = repo.get_issues(state="open")
    issue_list = []
    for issue in issues:
        issue_list.append(
            {
                "title": issue.title,
                "body": issue.body or "",
                "labels": [label.name for label in issue.labels],
                "created_at": issue.created_at,
                "updated_at": issue.updated_at,
                "author": issue.user.login,
            }
        )
    return issue_list


# ==========================
# FUNCTION: AI Categorization
# ==========================
def categorize_issue(title, body):
    prompt = f"""
    Categorize the following GitHub issue into one of these categories:
    Bug, Feature Request, Documentation, Enhancement, Question.

    Title: {title}
    Body: {body}

    Category:
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003", prompt=prompt, max_tokens=10
        )
        category = response.choices[0].text.strip()
    except Exception as e:
        print(f"Error categorizing issue '{title}': {e}")
        category = "Unknown"
    return category


# ==========================
# FUNCTION: Generate Excel Report
# ==========================
def generate_report(issue_list):
    # Ensure report folder exists
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    df = pd.DataFrame(issue_list)
    report_path = os.path.join(REPORT_FOLDER, REPORT_FILENAME)
    df.to_excel(report_path, index=False)

    category_summary = df["category"].value_counts()
    print("\n===== GitHub Issue Category Summary =====")
    print(category_summary)
    print(f"\nReport saved as {report_path}")


# ==========================
# MAIN FUNCTION
# ==========================
def main():
    print("Fetching open issues...")
    try:
        issues = fetch_issues(REPO_NAME)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return

    if not issues:
        print("No open issues found.")
        return

    print(f"Total open issues fetched: {len(issues)}")
    print("Categorizing issues using AI...")
    for issue in issues:
        issue["category"] = categorize_issue(issue["title"], issue["body"])
        print(f"{issue['title']} --> {issue['category']}")

    print("Generating Excel report...")
    generate_report(issues)


# ==========================
# RUN SCRIPT
# ==========================
if __name__ == "__main__":
    main()
