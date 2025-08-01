# Empathos - Mental Health Support Platform

A compassionate Flask-based web application designed to provide mental health support through AI chatbot assistance, confidential help requests, and educational resources.

## 🌟 Features

### 🔐 Dual Login System
- **Individual Users**: Access chatbot support, submit help requests, view awareness content
- **Authority Members**: Manage complaints, monitor chat interactions, update request status
- Secure authentication with role-based access control

### 💬 AI Chatbot Interface
- 24/7 AI assistant for immediate emotional support
- Real-time messaging with typing indicators
- Chat history stored securely in SQLite database
- Conversation starters and helpful tips

### 🆘 Help & Complaint System
- Confidential submission of personal complaints and help requests
- Multiple categories: mental health, stress, abuse, financial, etc.
- Status tracking: Pending → In Progress → Resolved
- Emergency mode for urgent situations

### 📢 Mental Health Awareness
- Educational content and resources
- Self-care tips and coping strategies
- Mental health statistics and facts
- Crisis support information

### 📊 Authority Dashboard
- Comprehensive complaint management
- Real-time status updates
- Chat interaction monitoring
- Filtering and search capabilities

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
- **Authentication**: Flask-SQLAlchemy with password hashing
- **Templating**: Jinja2

## 📁 Project Structure

```
empathos/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/               # Static assets
│   ├── CSS/
│   │   └── style.css     # Custom styles
│   ├── JAVASCRIPT/
│   │   └── main.js       # Main JavaScript file
│   └── Images/           # Image assets
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Individual user dashboard
│   ├── admin_dashboard.html # Authority dashboard
│   ├── chatbot.html      # AI chatbot interface
│   ├── help_form.html    # Help request form
│   └── awareness.html    # Mental health awareness
└── empathos.db          # SQLite database (created automatically)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd empathos
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 👥 User Roles

### Individual Users
- Register and login with personal credentials
- Access AI chatbot for immediate support
- Submit confidential help requests and complaints
- View mental health awareness content
- Track request status and history

### Authority Members
- Special access to administrative dashboard
- View and manage all user complaints
- Update complaint status (Pending/In Progress/Resolved)
- Monitor chatbot interactions
- Access analytics and statistics

## 🔧 Configuration

### Environment Variables
The application uses default configuration, but you can customize:

```python
# In app.py
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empathos.db'
```

### Database
The SQLite database is created automatically on first run. Tables include:
- `user`: User accounts and authentication
- `complaint`: Help requests and complaints
- `chat_message`: Chatbot conversation history

## 🎨 Customization

### Styling
- Modify `static/CSS/style.css` for custom styling
- Update color variables in CSS root for theme changes
- Add custom animations and effects

### Content
- Edit awareness content in `templates/awareness.html`
- Modify chatbot responses in `app.py` send_message route
- Update emergency contact information

### Features
- Add new complaint categories in help form
- Implement email notifications
- Integrate with external mental health APIs

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- SQL injection prevention with SQLAlchemy
- CSRF protection with Flask-SQLAlchemy

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🚨 Emergency Information

**Important**: This platform is for support and guidance only. For emergencies:

- **Emergency Services**: 911
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Local Crisis Centers**: Contact nearest mental health facility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bootstrap for responsive UI components
- Font Awesome for icons
- Flask community for the excellent framework
- Mental health organizations for inspiration

## 📞 Support

For technical support or questions about the application:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Remember**: Mental health matters. You're not alone. ❤️ 