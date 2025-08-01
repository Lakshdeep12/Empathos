from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'empathos-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empathos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'individual' or 'authority'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    complaints = db.relationship('Complaint', backref='user', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # mental_health, finance, abuse, etc.
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for both individual users and authorities"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            if role == 'authority':
                flash('Welcome back, Authority Member!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Welcome back!', 'success')
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page for new users"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'error')
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash, role=role)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Individual user dashboard"""
    if 'user_id' not in session or session['role'] != 'individual':
        flash('Please login as an individual user.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    complaints = Complaint.query.filter_by(user_id=user.id).order_by(Complaint.created_at.desc()).all()
    
    return render_template('dashboard.html', user=user, complaints=complaints)

@app.route('/admin_dashboard')
def admin_dashboard():
    """Authority member dashboard"""
    if 'user_id' not in session or session['role'] != 'authority':
        flash('Please login as an authority member.', 'error')
        return redirect(url_for('login'))
    
    # Get all complaints with user information
    complaints = db.session.query(Complaint, User.username).join(User).order_by(Complaint.created_at.desc()).all()
    
    # Get recent chat messages
    chat_messages = db.session.query(ChatMessage, User.username).join(User).order_by(ChatMessage.timestamp.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html', complaints=complaints, chat_messages=chat_messages)

@app.route('/chatbot')
def chatbot():
    """Chatbot interface"""
    if 'user_id' not in session:
        flash('Please login to access the chatbot.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    chat_messages = ChatMessage.query.filter_by(user_id=user.id).order_by(ChatMessage.timestamp.desc()).limit(20).all()
    
    return render_template('chatbot.html', user=user, chat_messages=chat_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    """Handle chatbot message sending"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    message = request.form.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Generate dummy response (in a real app, this would connect to an AI service)
    responses = [
        "I understand your concern. Let me help you with that.",
        "That's a valid question. Here's what I can tell you...",
        "I'm here to support you. Can you tell me more about this?",
        "Thank you for reaching out. Let me provide some guidance...",
        "I appreciate you sharing this with me. Here's my advice..."
    ]
    import random
    response = random.choice(responses)
    
    # Save message to database
    chat_message = ChatMessage(
        user_id=session['user_id'],
        message=message,
        response=response
    )
    
    db.session.add(chat_message)
    db.session.commit()
    
    return jsonify({
        'message': message,
        'response': response,
        'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/help_form')
def help_form():
    """Help and complaint form"""
    if 'user_id' not in session or session['role'] != 'individual':
        flash('Please login as an individual user.', 'error')
        return redirect(url_for('login'))
    
    return render_template('help_form.html')

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    """Submit a new complaint or help request"""
    if 'user_id' not in session or session['role'] != 'individual':
        flash('Please login as an individual user.', 'error')
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    
    if not all([title, description, category]):
        flash('All fields are required.', 'error')
        return redirect(url_for('help_form'))
    
    complaint = Complaint(
        user_id=session['user_id'],
        title=title,
        description=description,
        category=category
    )
    
    try:
        db.session.add(complaint)
        db.session.commit()
        flash('Your complaint has been submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash('Failed to submit complaint. Please try again.', 'error')
        return redirect(url_for('help_form'))

@app.route('/update_complaint_status', methods=['POST'])
def update_complaint_status():
    """Update complaint status (authority only)"""
    if 'user_id' not in session or session['role'] != 'authority':
        return jsonify({'error': 'Unauthorized'}), 403
    
    complaint_id = request.form.get('complaint_id')
    new_status = request.form.get('status')
    
    complaint = Complaint.query.get(complaint_id)
    if complaint:
        complaint.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})
    
    return jsonify({'error': 'Complaint not found'}), 404

@app.route('/awareness')
def awareness():
    """Awareness section with blog-style content"""
    return render_template('awareness.html')

if __name__ == '__main__':
    app.run(debug=True) 