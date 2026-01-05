# Medica - AI-Powered Food Analysis System

A Django-based web application that uses Google's Gemini AI to analyze food products and provide personalized health recommendations based on user personas.

## 🚀 Features

- **Image Analysis**: Upload images of food products for instant analysis
- **Multi-Agent AI System**: Utilizes specialized AI agents for comprehensive analysis
- **Personalized Recommendations**: Tailors advice based on user personas (Athlete, Parent, etc.)
- **Health Assessment**: Provides detailed ingredient analysis with risk/benefit evaluation
- **User-Friendly Interface**: Clean, modern web interface for easy interaction

## 🧠 AI Architecture

The system employs a multi-agent architecture with the following components:

1. **Extractor Agent**: Processes and extracts text from uploaded product images
2. **Scientist Agent**: Analyzes ingredients for health implications and risks
3. **Coach Agent**: Provides personalized recommendations based on user persona
4. **Synthesizer Agent**: Combines all analyses into a comprehensive final verdict

## 🛠️ Tech Stack

- **Backend**: Django 5.2.9
- **AI/ML**: Google Gemini (gemini-2.5-flash)
- **Agent Framework**: LangChain & LangGraph
- **Frontend**: HTML, CSS, JavaScript (Django Templates)
- **Database**: SQLite (default)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API Key
- Git (for cloning)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd medica
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create  `agents/config.py` and add your API key:
```python
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 5. Set Up Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 📁 Project Structure

```
medica/
├── agents/                 # AI agent implementations
│   ├── multiagent.py      # Main multi-agent system
│   ├── config.py          # API configuration
│   └── test.py            # Testing utilities
├── core/                   # Django app core
│   ├── views.py           # Main application views
│   ├── urls.py            # URL routing
│   └── models.py          # Database models
├── data/                   # Static data files
│   └── user_data.json     # User configuration data
├── medica/                 # Django project settings
│   ├── settings.py        # Project configuration
│   └── urls.py            # Main URL configuration
├── templates/              # HTML templates
├── media/                  # User-uploaded files
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── manage.py              # Django management script
```

## 🎯 How to Use

1. **Open the Application**: Navigate to `http://127.0.0.1:8000/`
2. **Upload Product Image**: Click the upload area and select a food product image
3. **View Analysis**: The system will automatically:
   - Extract ingredients from the image
   - Analyze health implications
   - Provide personalized recommendations
4. **Review Results**: See the comprehensive analysis with risk assessments and advice

## 🔧 Configuration

### User Personas
The system supports different user personas that affect recommendations:
- **Athlete**: Focus on performance and recovery
- **Parent**: Emphasis on family health and safety
- **Health-Conscious**: Priority on nutritional benefits
- **Custom**: Tailored to specific dietary needs

Edit `data/user_data.json` to modify user preferences:
```json
{
    "user_name": "Your Name",
    "user_initials": "YN",
    "persona": "Athlete"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: No module named 'agents.config'**
   - Create `agents/config.py` with your API key
   - Ensure `agents/__init__.py` exists (can be empty)

2. **API Key Not Working**
   - Verify your Gemini API key is valid
   - Check that the `.env` file is in the project root
   - Ensure the API key has proper permissions

3. **Server Not Starting**
   - Make sure virtual environment is activated
   - Check all dependencies are installed
   - Verify database migrations are complete

4. **Image Upload Not Working**
   - Ensure `media/` directory exists
   - Check file permissions
   - Verify image format is supported

### Getting Help
- Check the Django development server logs for detailed error messages
- Ensure all files are properly created and configured
- Verify your API key has sufficient credits





## 📞 Support

For questions or issues, please:
- Check the troubleshooting section above
- Review the error logs in the Django development server
- Ensure all setup steps have been completed correctly

---

**Built with ❤️ by Medica Team**
