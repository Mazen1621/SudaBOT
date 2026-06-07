from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Scholarship Bot: GitHub Setup and Automation Guide', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def add_section(pdf, title, body):
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, title, 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, body)
    pdf.ln(5)

pdf = PDF()
pdf.add_page()

# Introduction
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, 'This guide walks you through pushing the Scholarship Bot source code to GitHub and configuring GitHub Actions for automated execution every 6 hours.')
pdf.ln(10)

# Prerequisites
add_section(pdf, 'Prerequisites',
            '1. A GitHub account (create at https://github.com if needed)\n'
            '2. Git installed on your machine (https://git-scm.com)\n'
            '3. The scholarship bot source code (this package)')

# Step 1: Create GitHub Repository
add_section(pdf, 'Step 1: Create a New GitHub Repository',
            '1. Log in to https://github.com\n'
            '2. Click the "+" icon in the top-right -> "New repository"\n'
            '3. Repository name: e.g., scholarship-bot\n'
            '4. Description: Automated scholarship alert system for Sudanese students seeking Renewable Energy Master\'s/PhD\n'
            '5. Visibility: Public or Private (your choice)\n'
            '6. Do NOT initialize with README, .gitignore, or license (we will push existing code)\n'
            '7. Click "Create repository"')

# Step 2: Prepare Local Repository
add_section(pdf, 'Step 2: Prepare Local Repository',
            '1. Open a terminal/command prompt and navigate to the extracted scholarship bot folder\n'
            '2. Initialize Git: git init\n'
            '3. Set your Git identity (replace with your GitHub username/email):\n'
            '   git config --global user.name "Your GitHub Username"\n'
            '   git config --global user.email "you@example.com"\n'
            '4. Add all files (respects .gitignore): git add .\n'
            '5. Commit: git commit -m "Initial commit: Scholarship Bot with enhanced scrapers, filtering, storage, Telegram notifier, and GitHub Actions workflow"\n')

# Step 3: Connect to GitHub and Push
add_section(pdf, 'Step 3: Connect to GitHub and Push',
            'Option A: Using HTTPS with Personal Access Token (Recommended for simplicity)\n'
            '1. Change remote URL to HTTPS:\n'
            '   git remote set-url origin https://github.com/your-username/scholarship-bot.git\n'
            '2. Generate a Personal Access Token (PAT):\n'
            '   - Go to GitHub Settings -> Developer settings -> Personal access tokens -> Tokens (classic)\n'
            '   - Click "Generate new token" -> "Generate new token (classic)"\n'
            '   - Give it a note (e.g., "scholarship-bot-push"), set expiration, select "repo" scope\n'
            '   - Copy the token (looks like ghp_...)\n'
            '3. Push: git push origin main\n'
            '   - When prompted for username, enter your GitHub username\n'
            '   - When prompted for password, paste your Personal Access Token\n\n'
            'Alternative: Using SSH (if you prefer)\n'
            '1. Ensure you have an SSH key pair and the public key is added to your GitHub account\n'
            '2. Keep remote as git@github.com:your-username/scholarship-bot.git\n'
            '3. Push: git push origin main')

# Step 4: Set Up GitHub Secrets (for Telegram)
add_section(pdf, 'Step 4: Configure GitHub Secrets (Required for Telegram Notifications)',
            '1. On your GitHub repo page, click "Settings" tab\n'
            '2. In left sidebar: "Secrets and variables" -> "Actions"\n'
            '3. Click "New repository secret" twice to add:\n'
            '   - Name: BOT_TOKEN\n'
            '     Value: 8754585969:AAGvfkLV4ChvqjXTobsDCWaQ9hWaAjAQsso (your actual token)\n'
            '   - Name: CHAT_ID\n'
            '     Value: 383236986 (your actual chat ID)\n'
            '4. Click "Add secret" for each')

# Step 5: Verify GitHub Actions Workflow
add_section(pdf, 'Step 5: Verify GitHub Actions Workflow',
            'The repository already includes: .github/workflows/scholarship-bot.yml\n'
            'This workflow is configured to:\n'
            '   - Run every 6 hours (cron: \'0 */6 * * *\')\n'
            '   - Allow manual triggers (workflow_dispatch)\n'
            '   - Check out your code\n'
            '   - Set up Python\n'
            '   - Install dependencies from requirements.txt\n'
            '   - Run: python scholarship_bot.py with BOT_TOKEN and CHAT_ID injected as environment variables\n'
            'To test: Go to the "Actions" tab in your repo, click "Scholarship Bot" workflow, then "Run workflow".')

# Step 6: Ongoing Usage
add_section(pdf, 'Step 6: Ongoing Usage',
            '- To update code: make changes locally, then:\n'
            '   git add .\n'
            '   git commit -m "Your descriptive message"\n'
            '   git push origin main\n'
            '- GitHub Actions will automatically run on each push to main\n'
            '- You can also manually trigger runs via the "Actions" tab\n'
            '- View logs in each workflow run to monitor execution')

# Notes
add_section(pdf, 'Important Notes',
            '• Never commit your .env file containing real credentials (it is already ignored by .gitignore)\n'
            '• The .gitignore excludes: .env, scholarships_seen.db, scholarship_bot.log, __pycache__/, *.pyc\n'
            '• Your Telegram credentials are stored encrypted in GitHub Secrets and never exposed in logs\n'
            '• If you accidentally commit sensitive data, immediately revoke the token and remove the commit\n'
            '• The bot includes a SQLite database (scholarships_seen.db) to prevent duplicate notifications between runs within the same execution; note that GitHub Actions runs are ephemeral, so the database does not persist between scheduled runs (this is acceptable; you may see duplicate notifications if the same scholarship appears in consecutive runs)')

pdf.output('Scholarship_Bot_GitHub_Guide.pdf')
print('PDF created: Scholarship_Bot_GitHub_Guide.pdf')
