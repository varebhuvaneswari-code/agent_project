# Student Assistant Agent 🤖

An intelligent student assistant agent built with **Google ADK** (Agent Development Kit) and **Gemini**.

## 🌟 Features

- 📚 **Study Guidance**: Answers student queries and provides study assistance.
- 🧮 **Grade Average Calculation**: Calculates averages from marks and scores.
- 📁 **File & Note Creation**: Automatically writes notes and documents to disk.
- ✍️ **LinkedIn Post Generator**: Crafts professional, engaging post drafts.
- 🚀 **GitHub Synchronization**: Pushes and keeps project code synchronized with GitHub.

## 📁 Project Structure

`
Agent/
├── .env                  # API keys and environment variables (ignored in Git)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── my_agent/             # Core Agent Package
    ├── __init__.py       # Package entry
    ├── agent.py          # Student assistant agent definition & instructions
    ├── tools.py          # Custom agent tools
    ├── prompts.py        # Prompt templates
    └── config.py         # Agent configuration
`

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or later
- A Google Gemini API Key

### 2. Setup
`ash
# Clone the repository
git clone https://github.com/varebhuvaneswari-code/agent_project.git
cd agent_project

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
`

### 3. Environment Configuration
Create a .env file in the root directory:
`env
GOOGLE_API_KEY=your_gemini_api_key_here
`

### 4. Running the Agent
`ash
python -m my_agent.agent
`
