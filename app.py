from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import sqlite3

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cropcycle.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
from models import Farmer, Crop, Field, FieldCrop, SoilTestResult, PlantingSchedule, CropRotationHistory

# Initialize the database
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database with schema and sample data."""
    # Create tables
    db.create_all()
    
    # Import sample data if needed
    with app.open_resource('schema.sql') as f:
        connection = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        connection.executescript(f.read().decode('utf8'))
        connection.close()
    
    print("Database initialized!")

# Routes
@app.route('/')
def index():
    if 'farmer_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        farmer = Farmer.query.filter_by(username=username).first()
        
        if farmer and check_password_hash(farmer.password_hash, password):
            session['farmer_id'] = farmer.farmer_id
            session['farmer_name'] = farmer.name
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        # Check if username or email already exists
        if Farmer.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
            
        if Farmer.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return render_template('register.html')
        
        # Create new farmer
        new_farmer = Farmer(
            username=username,
            password_hash=generate_password_hash(password),
            name=name,
            email=email,
            phone=phone
        )
        
        db.session.add(new_farmer)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Field management routes
@app.route('/fields')
def fields():
    if 'farmer_id' not in session:
        return redirect(url_for('login'))
    
    farmer_fields = Field.query.filter_by(farmer_id=session['farmer_id']).all()
    return render_template('fields.html', fields=farmer_fields)

@app.route('/fields/add', methods=['GET', 'POST'])
def add_field():
    if 'farmer_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        area = float(request.form['area'])
        location = request.form['location']
        soil_type = request.form['soil_type']
        
        new_field = Field(
            farmer_id=session['farmer_id'],
            name=name,
            area_acres=area,
            location=location,
            soil_type=soil_type
        )
        
        db.session.add(new_field)
        db.session.commit()
        
        flash('Field added successfully!', 'success')
        return redirect(url_for('fields'))
    
    return render_template('add_field.html')

# Crop rotation routes
@app.route('/rotation/plan/<int:field_id>')
def plan_rotation(field_id):
    if 'farmer_id' not in session:
        return redirect(url_for('login'))
    
    field = Field.query.get_or_404(field_id)
    
    # Check if field belongs to the logged-in farmer
    if field.farmer_id != session['farmer_id']:
        flash('You do not have permission to view this field', 'danger')
        return redirect(url_for('fields'))
    
    crops = Crop.query.all()
    current_crops = FieldCrop.query.filter_by(field_id=field_id).all()
    soil_tests = SoilTestResult.query.filter_by(field_id=field_id).order_by(SoilTestResult.test_date.desc()).first()
    rotation_history = CropRotationHistory.query.filter_by(field_id=field_id).order_by(CropRotationHistory.planting_date.desc()).all()
    
    return render_template('plan_rotation.html', 
                          field=field,
                          crops=crops, 
                          current_crops=current_crops, 
                          soil_tests=soil_tests,
                          rotation_history=rotation_history)

@app.route('/api/crops')
def get_crops():
    crops = Crop.query.all()
    return jsonify([{
        'id': crop.crop_id,
        'name': crop.name,
        'family': crop.family,
        'growing_season': crop.growing_season,
        'days_to_maturity': crop.days_to_maturity,
        'nitrogen_fixation': crop.nitrogen_fixation,
        'nitrogen_consumption': crop.nitrogen_consumption,
        'water_needs': crop.water_needs
    } for crop in crops])

@app.route('/api/recommend-rotation', methods=['POST'])
def recommend_rotation():
    if 'farmer_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    field_id = data.get('field_id')
    
    # Get field history
    history = CropRotationHistory.query.filter_by(field_id=field_id).order_by(CropRotationHistory.planting_date.desc()).all()
    field = Field.query.get_or_404(field_id)
    last_soil_test = SoilTestResult.query.filter_by(field_id=field_id).order_by(SoilTestResult.test_date.desc()).first()
    
    # Get all crops
    all_crops = Crop.query.all()
    
    # Basic rotation logic (this would be more sophisticated in a real app)
    recommended_crops = []
    
    # Check if we have history
    if history:
        last_crop = Crop.query.get(history[0].crop_id)
        
        if last_crop.family == 'Poaceae':  # If last crop was a grass (like corn)
            # Recommend legumes next
            recommended_crops = [crop for crop in all_crops if crop.family == 'Fabaceae']
        elif last_crop.family == 'Fabaceae':  # If last crop was a legume
            # Recommend root vegetables or leafy greens
            recommended_crops = [crop for crop in all_crops if crop.family in ['Solanaceae', 'Brassicaceae']]
        else:
            # Recommend grasses or cereals
            recommended_crops = [crop for crop in all_crops if crop.family == 'Poaceae']
    else:
        # No history, recommend starting with legumes to build soil nitrogen
        recommended_crops = [crop for crop in all_crops if crop.family == 'Fabaceae']
    
    # Return recommendations
    return jsonify([{
        'id': crop.crop_id,
        'name': crop.name,
        'family': crop.family,
        'reason': f"Good rotation after previous crops in field {field.name}"
    } for crop in recommended_crops[:3]])

if __name__ == '__main__':
    app.run(debug=True) 