from app import db
from datetime import datetime

class Farmer(db.Model):
    """Model representing a farm owner or manager"""
    farmer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    fields = db.relationship('Field', backref='farmer', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Farmer {self.username}>'

class Crop(db.Model):
    """Model representing a crop type"""
    crop_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    family = db.Column(db.String(100), nullable=False)
    growing_season = db.Column(db.String(50), nullable=False)
    days_to_maturity = db.Column(db.Integer, nullable=False)
    nitrogen_fixation = db.Column(db.Boolean, default=False)
    nitrogen_consumption = db.Column(db.Integer, nullable=False)  # 1-5 scale
    water_needs = db.Column(db.Integer, nullable=False)  # 1-5 scale
    companion_crops = db.Column(db.Text)
    antagonistic_crops = db.Column(db.Text)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Crop {self.name}>'

class Field(db.Model):
    """Model representing a farm field"""
    field_id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    area_acres = db.Column(db.Float, nullable=False)
    location = db.Column(db.Text)
    soil_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    current_crops = db.relationship('FieldCrop', backref='field', lazy=True, cascade="all, delete-orphan")
    soil_tests = db.relationship('SoilTestResult', backref='field', lazy=True, cascade="all, delete-orphan")
    planting_schedules = db.relationship('PlantingSchedule', backref='field', lazy=True, cascade="all, delete-orphan")
    rotation_history = db.relationship('CropRotationHistory', backref='field', lazy=True, cascade="all, delete-orphan")
    
    __table_args__ = (db.UniqueConstraint('farmer_id', 'name'),)
    
    def __repr__(self):
        return f'<Field {self.name}>'

class FieldCrop(db.Model):
    """Model representing current crop assignments to fields"""
    field_crop_id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.field_id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    planting_date = db.Column(db.Date)
    expected_harvest_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='planned')  # planned, planted, harvested
    notes = db.Column(db.Text)
    
    # Relationship
    crop = db.relationship('Crop')
    
    def __repr__(self):
        return f'<FieldCrop {self.field_id}:{self.crop_id}>'

class SoilTestResult(db.Model):
    """Model representing soil test results for a field"""
    test_id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.field_id'), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    ph_level = db.Column(db.Float)
    nitrogen_level = db.Column(db.Float)
    phosphorus_level = db.Column(db.Float)
    potassium_level = db.Column(db.Float)
    organic_matter_percentage = db.Column(db.Float)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SoilTest {self.field_id} on {self.test_date}>'

class PlantingSchedule(db.Model):
    """Model representing planned crop rotations"""
    schedule_id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.field_id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    planned_planting_date = db.Column(db.Date, nullable=False)
    planned_harvest_date = db.Column(db.Date)
    season = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rotation_sequence = db.Column(db.Integer)  # Position in rotation cycle
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, skipped
    notes = db.Column(db.Text)
    
    # Relationship
    crop = db.relationship('Crop')
    
    def __repr__(self):
        return f'<PlantingSchedule {self.field_id}:{self.crop_id} for {self.season} {self.year}>'

class CropRotationHistory(db.Model):
    """Model representing historical crop rotations"""
    history_id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.field_id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    planting_date = db.Column(db.Date, nullable=False)
    harvest_date = db.Column(db.Date)
    yield_amount = db.Column(db.Float)
    yield_unit = db.Column(db.String(20))
    notes = db.Column(db.Text)
    
    # Relationship
    crop = db.relationship('Crop')
    
    def __repr__(self):
        return f'<CropHistory {self.field_id}:{self.crop_id} planted on {self.planting_date}>' 