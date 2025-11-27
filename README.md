# Dual-Interface Content Summarizer (AWS Bedrock + Claude)

This project implements an AI-powered content summarizer using Amazon Bedrock and Claude models.

## Features
- Text summarization
- PDF summarization
- CLI tool for automation
- Streamlit-based web UI
- Multiple summary styles (Brief, Detailed, Bullet, Executive)

## AWS Services Used
- Amazon Bedrock
- Claude model
- IAM authentication
- Boto3 SDK

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/CtrlAltDefeattt/content-summarizer-bedrock
cd content-summarizer-bedrock
Install Dependencies
pip install -r requirements.txt

3. Configure AWS Credentials
aws configure

4. Run Setup Test
python setup_summarizer.py

5. Start Web App
streamlit run summarization_app.py

6. Run CLI
python cli_summarizer.py --file document.pdf --style executive

Example CLI Usage
cat notes.txt | python3 cli_summarizer.py --stdin --style bullet_points

License

For educational use only.


Replace `YOUR_USERNAME` later.

---

# ✅ STEP 4: CREATE .gitignore FILE (IMPORTANT)

Create:

```bash
touch .gitignore


Paste:
.env
__pycache__/
*.pyc
venv/
