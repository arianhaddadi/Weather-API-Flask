from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuring Database
with open("db_config.json") as file:
    conf = json.load(file)
    print(conf)

username = conf["username"]
password = conf["password"]
db_name = conf["db_name"]

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{db_name}"
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)


@app.route("/user", methods=['POST'])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    country = request.form["country"]
    city = request.form["city"]
    new_user = User(username=username, password=password, country=country, city=city)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(success=True, status_code=200)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)