from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from config import Config

app = Flask(__name__)
# Apply the configuration from the Config class
app.config.from_object(Config)

# Elements
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connection = False


# Team Images Model (this will be moved into its own component)
class TeamImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_owner = db.Column(db.String(80), unique=False, nullable=False)
    image_name = db.Column(db.String(80), unique=True, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)


# Add Image Info to DB (this will also be moved into its own component)
def add_team_images():
    print("Checking Images")

    team_images = [
        {'image_owner': 'austen', 'image_name': 'austen-profile-pic', 'image_path': 'static/images/team-profile-images/austen-profile-pic.png'},
        {'image_owner': 'omar', 'image_name': 'omar-profile-pic', 'image_path': 'static/images/team-profile-images/omar-profile-pic.png'},
        {'image_owner': 'leo', 'image_name': 'leo-profile-pic', 'image_path': 'static/images/team-profile-images/leo-profile-pic.png'},
        {'image_owner': 'analee', 'image_name': 'analee-profile-pic', 'image_path': 'static/images/team-profile-images/analee-profile-pic.png'},
        {'image_owner': 'austen', 'image_name': '1999-nissan-gtr', 'image_path': 'static/images/team-images/austen/1999-nissan-gtr.jpg'},
        {'image_owner': 'omar', 'image_name': 'dune', 'image_path': 'static/images/team-images/omar/dune.jpg'},
        {'image_owner': 'leo', 'image_name': 'interest-one', 'image_path': 'static/images/team-images/leo/interest-one.jpg'},
        {'image_owner': 'analee', 'image_name': 'women-health', 'image_path': 'static/images/team-images/analee/women-health.png'},
        {'image_owner': 'alex', 'image_name': 'alex-profile-pic', 'image_path': 'static/images/team-profile-images/alex-profile-pic.png'},
        {'image_owner': 'alex', 'image_name': 'sim-racing', 'image_path': 'static/images/team-images/alex/sim-racing.jpg'},
        {'image_owner': 'alex', 'image_name': 'gym', 'image_path': 'static/images/team-images/alex/gym.jpg'}
    ]

    for image_data in team_images:
        # Checks for Existing Image
        existing_image = TeamImages.query.filter_by(
            image_owner=image_data['image_owner'], 
            image_name=image_data['image_name']
        ).first()

        if existing_image is None:
            new_team_image = TeamImages(
                image_owner = image_data['image_owner'],
                image_name = image_data['image_name'],
                image_path = image_data['image_path']
            )
            db.session.add(new_team_image)
        
        else:
            print(f"Image {image_data['image_name']} already exists for {image_data['image_owner']}")

    db.session.commit()
    return jsonify({'message': 'Database Updated'}), 200


if __name__ == '__main__':

    with app.app_context():

        # Test database connection inside app context
        try:
            db.session.execute(text('SELECT 1'))
            print("Database connection successful!")
            connection = True
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            connection = False

        if connection:
            add_team_images()

    app.run(debug=True)