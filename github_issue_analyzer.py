# github_issue_analyzer.py
"""
AI GitHub Issue Analyzer
- Fetches open issues from a GitHub repo
- Categorizes them using OpenAI GPT
- Generates an Excel report
"""

from github import Github, Auth, GithubException  # Import GitHub library for API access
import openai  # Import OpenAI library for AI categorization
import pandas as pd  # Import pandas for data manipulation
import os  # Import os for file system operations
from config import (  # Import configuration constants
    GITHUB_TOKEN,  # GitHub personal access token
    REPO_NAME,  # Name of the GitHub repository
    OPENAI_API_KEY,  # OpenAI API key
    REPORT_FOLDER,  # Folder to save reports
    REPORT_FILENAME,  # Name of the report file
)

# ==========================
# Setup OpenAI
# ==========================
openai.api_key = OPENAI_API_KEY  # Set the OpenAI API key for authentication


# ==========================
# FUNCTION: Fetch Open Issues
# ==========================
def fetch_issues(repo_name):  # Define function to fetch issues from GitHub
    g = Github(auth=Auth.Token(GITHUB_TOKEN))  # Authenticate with GitHub using token
    try:  # Try to get the repository
        repo = g.get_repo(repo_name)  # Get the repository object
    except GithubException.UnknownObjectException:  # Handle case where repo not found
        raise RuntimeError(  # Raise runtime error with message
            f"GitHub repository not found or inaccessible: '{repo_name}'. "  # Error message part 1
            "Check REPO_NAME in config.py and ensure your token has repo access."  # Error message part 2
        )
    issues = repo.get_issues(state="open")  # Get all open issues
    issue_list = []  # Initialize empty list for issues
    for issue in issues:  # Loop through each issue
        issue_list.append(  # Append issue data to list
            {  # Create dictionary for issue
                "title": issue.title,  # Issue title
                "body": issue.body or "",  # Issue body, default to empty string
                "labels": [label.name for label in issue.labels],  # List of label names
                "created_at": issue.created_at,  # Creation date
                "updated_at": issue.updated_at,  # Last update date
                "author": issue.user.login,  # Author's login name
            }
        )
    return issue_list  # Return the list of issues


# ==========================
# FUNCTION: AI Categorization
# ==========================
def categorize_issue(title, body):  # Define function to categorize issue using AI
    prompt = f"""  # Create prompt for OpenAI
    Categorize the following GitHub issue into one of these categories:  # Prompt instruction
    Bug, Feature Request, Documentation, Enhancement, Question.  # Categories list

    Title: {title}  # Include issue title
    Body: {body}  # Include issue body

    Category:  # Ask for category
    """
    try:  # Try to get AI response
        response = openai.chat.completions.create(  # Call OpenAI chat completion API
            model="gpt-3.5-turbo",  # Use GPT-3.5-turbo model
            messages=[{"role": "user", "content": prompt}],  # Provide messages
            max_tokens=10,  # Limit response length
        )
        category = response.choices[
            0
        ].message.content.strip()  # Extract and clean category
    except Exception as e:  # Handle any exceptions
        print(f"Error categorizing issue '{title}': {e}")  # Print error message
        category = "Unknown"  # Default category
    return category  # Return the category


# ==========================
# FUNCTION: Generate Excel Report
# ==========================
def generate_report(issue_list):  # Define function to generate Excel report
    # Ensure report folder exists
    if not os.path.exists(REPORT_FOLDER):  # Check if folder exists
        os.makedirs(REPORT_FOLDER)  # Create folder if not

    df = pd.DataFrame(issue_list)  # Create DataFrame from issue list
    report_path = os.path.join(REPORT_FOLDER, REPORT_FILENAME)  # Construct report path
    df.to_excel(report_path, index=False)  # Save DataFrame to Excel

    category_summary = df["category"].value_counts()  # Count categories
    print("\n===== GitHub Issue Category Summary =====")  # Print summary header
    print(category_summary)  # Print summary
    print(f"\nReport saved as {report_path}")  # Print save message


# ==========================
# MAIN FUNCTION
# ==========================
def main():  # Define main function
    print("Fetching open issues...")  # Print status message
    try:  # Try to fetch issues
        issues = fetch_issues(REPO_NAME)  # Call fetch function
    except RuntimeError as exc:  # Handle runtime error
        print(f"ERROR: {exc}")  # Print error
        return  # Exit function

    if not issues:  # Check if no issues
        print("No open issues found.")  # Print message
        return  # Exit function

    print(f"Total open issues fetched: {len(issues)}")  # Print count
    print("Categorizing issues using AI...")  # Print status
    for issue in issues:  # Loop through issues
        issue["category"] = categorize_issue(
            issue["title"], issue["body"]
        )  # Categorize each
        print(f"{issue['title']} --> {issue['category']}")  # Print result

    print("Generating Excel report...")  # Print status
    generate_report(issues)  # Call generate function


# ==========================
# RUN SCRIPT
# ==========================
if __name__ == "__main__":  # Check if script is run directly
    main()  # Call main function
