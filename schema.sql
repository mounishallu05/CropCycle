-- Drop tables if they exist
DROP TABLE IF EXISTS crop_rotation_history;
DROP TABLE IF EXISTS planting_schedule;
DROP TABLE IF EXISTS soil_test_results;
DROP TABLE IF EXISTS field_crops;
DROP TABLE IF EXISTS fields;
DROP TABLE IF EXISTS crops;
DROP TABLE IF EXISTS farmers;

-- Create farmers table
CREATE TABLE farmers (
    farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create crops table
CREATE TABLE crops (
    crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    family VARCHAR(100) NOT NULL,
    growing_season VARCHAR(50) NOT NULL,
    days_to_maturity INTEGER NOT NULL,
    nitrogen_fixation BOOLEAN DEFAULT FALSE,
    nitrogen_consumption INTEGER NOT NULL, -- 1-5 scale
    water_needs INTEGER NOT NULL, -- 1-5 scale
    companion_crops TEXT,
    antagonistic_crops TEXT,
    description TEXT
);

-- Create fields table
CREATE TABLE fields (
    field_id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    area_acres FLOAT NOT NULL,
    location TEXT,
    soil_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id) ON DELETE CASCADE,
    UNIQUE(farmer_id, name)
);

-- Create field_crops table for current crop assignments
CREATE TABLE field_crops (
    field_crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    planting_date DATE,
    expected_harvest_date DATE,
    status VARCHAR(20) DEFAULT 'planned', -- planned, planted, harvested
    notes TEXT,
    FOREIGN KEY (field_id) REFERENCES fields(field_id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);

-- Create soil_test_results table
CREATE TABLE soil_test_results (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL,
    test_date DATE NOT NULL,
    ph_level FLOAT,
    nitrogen_level FLOAT,
    phosphorus_level FLOAT,
    potassium_level FLOAT,
    organic_matter_percentage FLOAT,
    notes TEXT,
    FOREIGN KEY (field_id) REFERENCES fields(field_id) ON DELETE CASCADE
);

-- Create planting_schedule table
CREATE TABLE planting_schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    planned_planting_date DATE NOT NULL,
    planned_harvest_date DATE,
    season VARCHAR(20) NOT NULL,
    year INTEGER NOT NULL,
    rotation_sequence INTEGER, -- Position in rotation cycle
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, completed, skipped
    notes TEXT,
    FOREIGN KEY (field_id) REFERENCES fields(field_id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);

-- Create crop_rotation_history table
CREATE TABLE crop_rotation_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    planting_date DATE NOT NULL,
    harvest_date DATE,
    yield_amount FLOAT,
    yield_unit VARCHAR(20),
    notes TEXT,
    FOREIGN KEY (field_id) REFERENCES fields(field_id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);

-- Insert some sample crop data
INSERT INTO crops (name, family, growing_season, days_to_maturity, nitrogen_fixation, nitrogen_consumption, water_needs, companion_crops, antagonistic_crops, description)
VALUES 
('Corn', 'Poaceae', 'Summer', 80, 0, 5, 4, 'Beans, Squash, Cucumber', 'Tomato', 'High nitrogen feeder, part of the Three Sisters planting technique.'),
('Soybeans', 'Fabaceae', 'Summer', 100, 1, 1, 3, 'Corn, Sunflower', 'Garlic, Onion', 'Nitrogen-fixing legume, good rotation crop after corn.'),
('Winter Wheat', 'Poaceae', 'Winter', 240, 0, 3, 2, 'Clover', 'None', 'Cover crop that suppresses weeds and prevents soil erosion.'),
('Alfalfa', 'Fabaceae', 'Spring/Summer', 365, 1, 1, 3, 'None', 'None', 'Perennial nitrogen-fixing legume with deep roots that improve soil structure.'),
('Potato', 'Solanaceae', 'Spring', 110, 0, 3, 3, 'Beans, Corn', 'Tomato, Cucumber', 'Root vegetable, avoid planting after tomatoes or other nightshades.'); 