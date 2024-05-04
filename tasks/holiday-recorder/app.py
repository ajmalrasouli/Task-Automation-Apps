from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime
import holidays

TOTAL_ALLOWED_HOLIDAYS = 28

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///holiday_recorder.db'  # SQLite database file
db = SQLAlchemy(app)

# Define custom filter for formatting dates
@app.template_filter('strftime')
def format_datetime(value, format='%m/%d/%Y'):
    if value is None:
        return ""
    return value.strftime(format)

# Your routes and other app configurations...

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    holidays = db.relationship('Holiday', backref='user', lazy=True)

# Define Holiday model
class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'email' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if request.form['submit_button'] == 'login':
            return redirect(url_for('login'))
        elif request.form['submit_button'] == 'register':
            return redirect(url_for('register'))

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = User.query.filter_by(email=request.form['email']).first()
        if existing_user:
            flash('Email already exists, please choose another one.', 'error')
            return redirect(url_for('register'))
        else:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            new_user = User(email=request.form['email'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password):
            session['email'] = request.form['email']
            session['user_id'] = user.id  # Store the user ID in the session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# Fetch bank holidays for the current year
def get_bank_holidays():
    current_year = datetime.now().year
    uk_holidays = holidays.UnitedKingdom(years=current_year)
    bank_holidays = [{'Date': date.strftime('%Y-%m-%d'), 'Day of the week': date.strftime('%A'), 'Bank holiday': name} for date, name in uk_holidays.items()]
    return bank_holidays

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    current_user = session.get('email')
    current_year = datetime.now().year  # Get the current year

    current_user_id = session.get('user_id')
    current_holidays = Holiday.query.filter_by(user_id=current_user_id).all()
    remaining_holidays = get_remaining_holidays()
    total_allowed_holidays = TOTAL_ALLOWED_HOLIDAYS

    # Fetch bank holidays for the current year
    bank_holidays = get_bank_holidays()

    # Convert date objects to strings with desired format
    for holiday in current_holidays:
        holiday.date_from_str = holiday.date_from.strftime('%m/%d/%Y')
        holiday.date_to_str = holiday.date_to.strftime('%m/%d/%Y')

    return render_template('dashboard.html', current_user=current_user, holidays=current_holidays, remaining=remaining_holidays, total_allowed_holidays=total_allowed_holidays, bank_holidays=bank_holidays, current_year=current_year)

def get_remaining_holidays():
    user_id = session.get('user_id')
    if user_id is None:
        return 0  # No user logged in, so no remaining holidays

    # Calculate the total days taken for holidays by the user
    holidays = Holiday.query.filter_by(user_id=user_id).all()
    total_days_taken = sum((holiday.date_to - holiday.date_from).days + 1 for holiday in holidays)

    # Calculate remaining holidays based on total allowed holidays and total days taken
    remaining_holidays = TOTAL_ALLOWED_HOLIDAYS - total_days_taken

    return max(0, remaining_holidays)  # Ensure remaining holidays is non-negative

@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    if 'email' not in session:
        return redirect(url_for('login'))

    title = request.form.get('title')
    date_from_str = request.form.get('date_from')
    date_to_str = request.form.get('date_to')
    reason = request.form.get('reason')

    # Check if any of the required fields are empty
    if not (title and date_from_str and date_to_str and reason):
        return jsonify({'error': 'Please fill out all fields.'}), 400

    # Convert date strings to datetime objects
    try:
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    # Ensure date_to is after date_from
    if date_to < date_from:
        return jsonify({'error': 'End date must be after start date.'}), 400

    # Fetch user ID from session
    user_id = session.get('user_id')

    # Create and save holiday record
    new_holiday = Holiday(title=title, date_from=date_from, date_to=date_to, reason=reason, user_id=user_id)
    db.session.add(new_holiday)
    db.session.commit()

    return redirect(url_for('dashboard'))

# Your existing code...

@app.route('/edit_holiday/<int:holiday_id>', methods=['GET', 'POST'])
def edit_holiday(holiday_id):
    if request.method == 'POST':
        holiday = Holiday.query.get(holiday_id)
        holiday.title = request.form['title']
        holiday.date_from = datetime.strptime(request.form['date_from'], '%Y-%m-%d').date()
        holiday.date_to = datetime.strptime(request.form['date_to'], '%Y-%m-%d').date()
        holiday.reason = request.form['reason']
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        holiday = Holiday.query.get(holiday_id)
        return render_template('edit_holiday.html', holiday=holiday)


@app.route('/delete_holiday/<int:holiday_id>', methods=['POST'])
def delete_holiday(holiday_id):
    if 'email' not in session:
        return redirect(url_for('login'))

    # Fetch the holiday by its ID
    holiday = Holiday.query.get_or_404(holiday_id)

    # Ensure that the current user owns the holiday
    if holiday.user_id != session.get('user_id'):
        flash('You are not authorized to delete this holiday.', 'error')
        return redirect(url_for('dashboard'))

    # Delete the holiday from the database
    db.session.delete(holiday)
    db.session.commit()

    flash('Holiday deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    return render_template('about.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)