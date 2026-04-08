# GitHub AI Issue Analyzer

A professional tool for analyzing and categorizing GitHub issues using artificial intelligence. This application fetches open issues from a specified GitHub repository, categorizes them using OpenAI's GPT model, and generates a comprehensive Excel report with summary statistics.

## Features

- **Automated Issue Fetching**: Retrieves all open issues from a GitHub repository using the GitHub API.
- **AI-Powered Categorization**: Utilizes OpenAI's GPT model to intelligently categorize issues into predefined categories (Bug, Feature Request, Documentation, Enhancement, Question).
- **Excel Report Generation**: Creates a detailed Excel spreadsheet with issue details and category summaries.
- **Error Handling**: Robust error handling for API failures and missing repositories.
- **Configurable**: Easy configuration through a dedicated config file.

## Prerequisites

- Python 3.8 or higher
- GitHub Personal Access Token with repository read access
- OpenAI API Key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/github-ai-issue-analyzer.git
   cd github-ai-issue-analyzer
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the application:
   - Set environment variables for your GitHub token, repository name, and OpenAI API key:
     ```bash
     export GITHUB_TOKEN="your_github_token"
     export REPO_NAME="owner/repo"
     export OPENAI_API_KEY="your_openai_key"
     ```
   - Or create a `.env` file in the project root with these variables.

## Usage

Run the analyzer:

```bash
python github_issue_analyzer.py
```

The script will:

1. Fetch all open issues from the specified repository.
2. Categorize each issue using AI.
3. Generate an Excel report in the `reports/` folder.
4. Display a category summary in the console.

## Configuration

Edit `config.py` to set:

- `GITHUB_TOKEN`: Your GitHub personal access token.
- `REPO_NAME`: The GitHub repository in the format `owner/repo`.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `REPORT_FOLDER`: Directory for saving reports (default: "reports").
- `REPORT_FILENAME`: Name of the output Excel file (default: "GitHub_Issue_Report.xlsx").

## Output

The generated Excel report includes:

- Issue title
- Issue body
- Labels
- Creation date
- Last update date
- Author
- AI-assigned category

A category summary is also printed to the console.

## Docker

To run the application in a Docker container:

1. Build the image:

   ```bash
   docker build -t github-ai-analyzer .
   ```

2. Create a `.env` file with your configuration:

   ```
   GITHUB_TOKEN=your_github_token
   REPO_NAME=owner/repo
   OPENAI_API_KEY=your_openai_key
   ```

3. Run the container:
   ```bash
   docker run --env-file .env github-ai-analyzer
   ```

## Dependencies

- PyGithub: For GitHub API interaction
- OpenAI: For AI categorization
- Pandas: For data manipulation and Excel export
- NumPy: Numerical computing support

## Security Note

Never commit API keys or tokens to version control. Use environment variables or a secure configuration method in production.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
