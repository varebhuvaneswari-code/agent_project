# 🤖 Student Assistant Agent

An intelligent AI-powered student assistant built using **Google ADK (Agent Development Kit)** and **Google Gemini**. The agent is designed to assist students with academic tasks, productivity, content generation, and basic project automation.

## ✨ Features

* 📚 **Study Assistance**
  Provides guidance, explanations, and support for student-related queries.

* 🧮 **Grade Average Calculator**
  Calculates average marks and scores quickly and accurately.

* 📝 **File & Note Creation**
  Automatically creates and saves notes and documents to disk.

* 💼 **LinkedIn Post Generator**
  Generates professional and engaging LinkedIn post drafts.

* 🚀 **GitHub Integration**
  Supports GitHub-related project synchronization and automation.

## 🛠️ Tech Stack

* **Python**
* **Google ADK (Agent Development Kit)**
* **Google Gemini**
* **python-dotenv**
* **Git & GitHub**

## 📁 Project Structure

```text
agent_project/
│
├── .env                  # Environment variables (not committed)
├── .gitignore            # Files ignored by Git
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
└── my_agent/
    ├── __init__.py       # Package initialization
    ├── agent.py          # Main agent definition
    ├── tools.py          # Custom agent tools
    ├── prompts.py        # Prompt templates
    └── config.py         # Agent configuration
```

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.10 or later
* Git
* A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/varebhuvaneswari-code/agent_project.git
cd agent_project
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

> **Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the Agent

```bash
python -m my_agent.agent
```

## 🔐 Environment Variables

| Variable         | Description                          |
| ---------------- | ------------------------------------ |
| `GOOGLE_API_KEY` | API key used to access Google Gemini |

## 💡 Use Cases

The Student Assistant Agent can be used to:

* Get help with academic questions
* Calculate grades and averages
* Generate study notes
* Create files and documents
* Generate professional LinkedIn content
* Automate basic GitHub-related tasks

## 🔮 Future Improvements

* 🌐 Add a web-based user interface
* 💬 Add conversational memory
* 📊 Add student performance tracking
* 📅 Add personalized study-plan generation
* 🔔 Add reminders and notifications
* 🔗 Expand GitHub automation capabilities
* 🎙️ Add voice-based interaction

## 👩‍💻 Author

**Vare Bhuvaneswari**

B.Tech Computer Science Engineering Student

Interested in **AI, Python, Full-Stack Development, and Software Engineering**.

## 📄 License

This project is developed for educational and learning purposes.
