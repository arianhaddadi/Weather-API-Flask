from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import exceptions
import json
import hashlib
import jwt
import datetime

app = Flask(__name__)

# Configuring Database
with open("db_config.json") as file:
    conf = json.load(file)

username = conf["username"]
password = conf["password"]
db_name = conf["db_name"]

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{db_name}"

db = SQLAlchemy(app)


def authorize(f):
    def decorator():
        try:
            username = request.args.get("username")
            token = request.headers.environ.get("HTTP_AUTHORIZATION")
            if username is None or token is None:
                raise exceptions.BadRequest

            token = token.split()[1]
            token_decoded = jwt.decode(token, "weath", algorithms=["HS256"])
            if username != token_decoded["username"]:
                raise jwt.exceptions.InvalidTokenError

            user = User.query.filter_by(username=username).first()
            if user is None or token_decoded["password"] != user.password:
                raise jwt.exceptions.InvalidTokenError

            return f(user)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify(success=False, status_code=401, message="Token Expired! Please Login Again!")
        except jwt.exceptions.InvalidTokenError:
            return jsonify(success=False, status_code=401, message="Token Invalid!")
        except exceptions.BadRequest:
            return jsonify(success=False, status_code=400, message="Bad Request! Check The Request Data!")

    return decorator

class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)


@app.route("/user", methods=['POST'])
def add_user():
    username = request.form["username"]
    password = hashlib.sha256(request.form["password"].encode()).hexdigest()
    country = request.form["country"]
    city = request.form["city"]
    new_user = User(username=username, password=password, country=country, city=city)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify(success=True, status_code=200, message="Successfully Signed Up!")
    except Exception as e:
        if e.orig.pgcode == "23505":
            return jsonify(success=False, status_code=400, message="Username already exists!")
        else:
            return jsonify(success=False, status_code=400, message="An Error Happened!")


# Login
@app.route("/login", methods=['POST'])
def login():
    username = request.form["username"]
    password = hashlib.sha256(request.form["password"].encode()).hexdigest()
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        return jsonify(success=False, status_code=400, message="User doesn't exist! Try Again!")
    else:
        payload = {
            "username": username,
            "password": password,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=20)
        }
        key = "weath"
        token = jwt.encode(payload, key)
        return jsonify(success=True, status_code=200, message="Successfully Logged In!", jwt_token=token)


# Update Location
@app.route("/user", methods=['PUT'])
@authorize
def update_location(user):
    new_city = request.form.get("city")
    new_country = request.form.get("country")
    if new_country is not None:
        user.country = new_country
    if new_city is not None:
        user.city = new_city
    db.session.commit()
    return jsonify(success=True, status_code=200, message="Update Was Successful!")

# Delete User


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)