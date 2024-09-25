from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

app = Flask(__name__, template_folder="templates")
CORS(app)
app.secret_key = "h19aundecided"  # Secret Key APP


# Configure the SQLAlchemy database URI
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:password@localhost:3306/uni"

# # Initialize the SQLAlchemy database
# db.init_app(app)

# Initialize JWTManager
app.config["JWT_SECRET_KEY"] = "h19aundecided_jwt"  # Secret Key JW
jwt = JWTManager(app)

# Email
app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "PROJECT15UNSW@outlook.com"
app.config["MAIL_PASSWORD"] = "$undecided123"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

app.app_context().push()
