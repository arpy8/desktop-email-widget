# Email Desktop Widget

A desktop widget to monitor my Gmail inbox and display recent emails with AI-enhanced summaries and priority indicators. The widget appears/disappears based on desktop visibility and provides hover previews of email content.

## Project Structure

```
├── main.py          # Main GUI application with PyQt5
├── mailer.py        # Gmail IMAP integration
├── llm.py           # AI processing with Google Gemini
├── utils.py         # Windows API utilities for desktop detection
├── config.py        # Configuration and constants
├── monitor.py       # Development hot-reload script
├── logs.json        # Email cache (auto-generated)
└── .env             # Environment variables (see .env.example)
```

## Prerequisites

- Python 3.12
- Gmail account with App Password enabled
- Google Gemini API key

## Installation

1. **Clone/Download the project**
   ```bash
   cd c:\Users\arpy8\Desktop\temp
   ```

2. **Install required packages**
   ```bash
   pip install PyQt5 watchdog google-generativeai python-dotenv
   ```

3. **Set up Gmail App Password**
   - Go to Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for "Mail"

4. **Get Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

5. **Create `.env` file**
   ```env
   USER_EMAIL=your-email@gmail.com
   USER_PASSWORD=your-app-password
   GEMINI_API_KEY=your-gemini-api-key
   ```

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

### Widget Behavior

- **Auto Show/Hide**: Widget appears when desktop is visible, hides when applications are in focus
- **Email Updates**: Automatically checks for new emails every 15 minutes
- **Manual Refresh**: Press `Ctrl+R` to force refresh
- **Hover Preview**: Hover over any email to see full content in a popup

### Color Coding

- 🔴 **Red**: High priority (urgent, deadlines, interviews, offers)
- 🟡 **Yellow**: Medium priority (meetings, reminders, applications)
- 🟢 **Green**: Low priority (general emails)
- 🟠 **Orange**: Emails from 'zs' domain (special category)

## Configuration

### Email Priority Keywords

Modify `mailer.py` to customize priority detection:

```python
high_keywords = ['urgent', 'deadline', 'asap', 'important', 'critical']
medium_keywords = ['meeting', 'reminder', 'update', 'registration']
```

### Widget Appearance

Customize colors and styling in `config.py`:

```python
COLOR_MAP = {
    'high': 'red',
    'medium': 'yellow',
    'low': 'green',
    'zs': '#ed7b08'
}
```

### AI Prompt Customization

Modify the LLM instructions in `config.py` to change how emails are summarized and prioritized.

## Components Overview

### main.py
- **MainWindow**: Main widget with email display
- **Log**: Individual email display components
- **HoverCanvas**: Popup for email content preview
- **WindowsAPIBS**: Desktop visibility detection

### mailer.py
- Gmail IMAP connection and email fetching
- Email parsing and basic priority detection
- Content extraction from HTML/plain text emails

### llm.py
- Google Gemini AI integration
- Email summarization and priority enhancement
- JSON response processing and error handling

### utils.py
- Windows API integration for desktop state detection
- Window management utilities

### monitor.py
- Development utility for hot reloading
- Automatically restarts the application when files change

## Troubleshooting

### Common Issues

1. **Gmail Connection Failed**
   - Verify App Password is correct
   - Check if 2FA is enabled
   - Ensure "Less secure app access" is not blocking

2. **Widget Not Showing**
   - Check if desktop is actually visible
   - Verify Windows API calls are working
   - Try running as administrator

3. **AI Summaries Not Working**
   - Verify Gemini API key is valid
   - Check API quota limits
   - Review error logs in console

4. **Import Errors**
   - Install all required packages: `pip install PyQt5 watchdog google-generativeai python-dotenv`
   - Check Python version compatibility

### Logs and Debugging

- Console output shows fetch status and errors
- `logs.json` contains cached email data
- Enable debug mode by modifying logging levels in `llm.py`

## Development

### Adding New Features

1. **Email Filters**: Modify `mailer.py` to add custom email filtering
2. **New Priorities**: Update `COLOR_MAP` and priority detection logic
3. **UI Customization**: Modify PyQt5 styling in `main.py`

### Hot Reload Development

Use `monitor.py` for development - it automatically restarts the application when you save changes to `main.py`.

## Security Notes

- Store credentials securely in `.env` file
- Use Gmail App Passwords instead of main password
- Keep API keys private and don't commit to version control

## License

This project is for personal use. Ensure compliance with Gmail API terms and Google Gemini API usage policies.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review console output for error messages
- Ensure all dependencies are correctly installed
