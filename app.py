from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle

open_df = pickle.load(open('openBook.pkl','rb'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///details.db"
with app.app_context():
    db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        return f"{self.email} - {self.password}"

@app.route("/")
def login():
    return render_template('login.html',)

@app.route("/signup", methods=["GET", "POST"])
def signup():
        if request.method == "POST":
            # Get form data
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            if not password:
                return render_template("signup.html", error="Password cannot be empty")

            # Create new user object
            user = User(name=name, email=email, password=password)

            # Add new user to database
            db.session.add(user)
            db.session.commit()

            # Redirect to home page
            return redirect("/")

        # Render signup template for GET request
        return render_template("signup.html")

@app.route("/home")
def home():
    return render_template('home.html',
                           book_name = list(open_df['Book-Title'].values),
                           author = list(open_df['Book-Author'].values),
                           image = list(open_df['Image-URL-M'].values),
                           publisher = list(open_df['publisher'].values))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)