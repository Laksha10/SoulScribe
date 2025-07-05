from flask import Flask
from flask_cors import CORS
from db.connection import init_db
from dotenv import load_dotenv
load_dotenv()
import os
print("LOADED DB URL:", os.getenv("DATABASE_URL"))


app = Flask(__name__)
CORS(app)

# Initialize the database
init_db(app)

# Register your routes
from routes.predict import predict_bp
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    app.run(debug=True)
