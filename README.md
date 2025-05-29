# CropCycle: Smart Crop Rotation Solutions for Farmers

CropCycle is a web application designed to help farmers manage and optimize their crop rotation practices for improved soil health, higher yields, and sustainable farming.

## Features

- **Field Management**: Track and manage all your fields in one place
- **Crop Database**: Access information about various crops, their growing requirements, and rotation compatibility
- **Smart Rotation Recommendations**: Get AI-powered recommendations for crop rotation based on field history and soil conditions
- **Soil Health Tracking**: Monitor soil health metrics over time to make data-driven decisions
- **Rotation Planning**: Plan your crop rotations with an intuitive interface
- **Historical Data**: Keep records of past crops to analyze performance and improve future planning

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mounishallu05/cropcycle.git
   cd cropcycle
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   flask init-db
   ```

5. Run the application:
   ```
   flask run
   ```

6. Access the application in your browser at `http://127.0.0.1:5000`

## Project Structure

- `app.py`: Main application file with Flask routes
- `models.py`: SQLAlchemy models for database tables
- `schema.sql`: SQL schema and sample data
- `templates/`: HTML templates for the web interface
- `static/`: CSS, JavaScript, and image files
- `requirements.txt`: Python dependencies

## Usage

1. Create an account or login
2. Add your fields with relevant information
3. View and manage your fields
4. Plan crop rotations for each field
5. Get smart recommendations based on your field's history and soil conditions
6. Track your implementation and results over time

## Future Enhancements

- Weather integration for planting recommendations
- Mobile app for field data collection
- Integration with soil testing services
- Yield prediction based on historical data
- Community features for sharing insights with other farmers

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Icons provided by Font Awesome
- UI components from Bootstrap 5
- Crop data sourced from agricultural research databases 
