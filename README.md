# Email Desktop Widget

A desktop widget to monitor your Gmail inbox and display recent emails with AI-enhanced summaries and priority indicators. The widget appears/disappears based on desktop visibility and provides hover previews of email content.

## Project Structure

```text
├── main.py            # Main GUI application with PyQt5
├── mailer.py          # Gmail IMAP integration and email processing
├── llm.py             # AI processing with Google Gemini
├── utils.py           # Windows API utilities and toast notifications
├── config.py          # Configuration management
├── config_dialog.py   # GUI configuration dialog
├── monitor.py         # Development hot-reload script
├── logs.json          # Email cache (auto-generated)
├── user_config.json   # User configuration (auto-generated)
├── .env.example       # Environment variables template
└── assets/
    └── logo.ico       # Application icon
```

## Prerequisites

- Python 3.12+
- Windows OS (for desktop detection and toast notifications)
- Gmail account with App Password enabled
- Google Gemini API key

## Installation

1. **Clone/Download the project**

   ```bash
   git clone https://github.com/arpy8/desktop-email-widget
   cd desktop-email-widget
   ```

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail App Password**
   - Go to Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for "Mail"

4. **Get Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

5. **Configure the application**
   - Run the application for the first time
   - A configuration dialog will appear
   - Enter your Gmail credentials and Gemini API key

## Usage

### Running the Application

**Production Mode:**

```bash
python main.py
```

**Development Mode (with hot reload):**

```bash
python monitor.py
```

### How It Works

1. **Desktop Detection**: The widget monitors when the desktop is visible
2. **Email Fetching**: Retrieves latest emails from Gmail using IMAP
3. **AI Processing**: Uses Google Gemini to generate summaries and classify priority
4. **Widget Display**: Shows emails as colored labels on the desktop
5. **Hover Preview**: Displays email content when hovering over email labels
6. **Smart Caching**: Stores processed emails locally to reduce API calls

### Configuration

The application supports two configuration methods:

1. **GUI Configuration** (Recommended): Run the app and use the configuration dialog

### Priority Classification

Emails are automatically classified into three priority levels:

- 🔴 **High Priority**: Contains urgent keywords (urgent, deadline, ASAP, critical, etc.)
- 🟡 **Medium Priority**: Contains meeting, reminder, or update keywords
- 🟢 **Low Priority**: General emails

### Dependencies

- **PyQt5**: GUI framework for the desktop widget
- **google-generativeai**: Google Gemini API integration
- **python-dotenv**: Environment variable management
- **windows-toasts**: Native Windows toast notifications (auto-installed)

### Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile -w 'main.py' --icon "assets/logo.ico"
```

The executable will be created in the `dist/` directory.