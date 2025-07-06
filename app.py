from datetime import datetime
from flask import Flask, flash, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sql import SignupForm, LoginForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "515798c503f83b1f4846bdfc15ab5d40"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Srimanta2005@localhost:3306/FURNITURE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# Create tables
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return redirect(url_for('signup'))
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('signup.html', form=form)

        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('signup.html', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            gender=form.gender.data if form.gender.data else None,
            dob=form.dob.data
        )
        user.set_password(form.password.data)

        
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Welcome to our platform.', 'success')
        return redirect(url_for('home'))
        

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.title()}: {error}', 'error')

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html', form=form)

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


@app.route("/home")
def home():
    return render_template("home.html", title="HOME")

@app.route("/about")
def about():
    return render_template("about.html", title="ABOUT")

@app.route("/category")
def category():
    return render_template("category.html", title="CATEGORY")

@app.route("/bedroom")
def bedroom():
    return render_template("bedroom.html", title="bedroom")

@app.route("/living")
def living():
    return render_template("living_room.html", title="living_room")

@app.route("/diningroom")
def diningroom():
    return render_template("dining_room.html", title="dining_room")

@app.route("/office")
def office():
    return render_template("office.html", title="office_room")

@app.route("/outdoor")
def outdoor():
    return render_template("outdoor.html", title="OUTDOOR")

@app.route("/accent")
def accent():
    return render_template("accent.html", title="ACCENT")

@app.route("/sofa_section")
def sofa_section():
    return render_template("sofa_section.html", title="SOFA")

@app.route("/mattresses")
def mattresses():
    return render_template("mattresses.html", title="MATTRESSES")

@app.route("/kitchen")
def kitchen():
    return render_template("kitchen.html", title="KITCHEN")

@app.route("/luxury")
def luxury():
    return render_template("luxury.html", title="LUXURY")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html", title="Thanks")

@app.route("/cart")
def cart():
    return render_template("cart.html", title="CART")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        print(f"Message from {name} ({email}): {message}")
        flash("Thank you for contacting us! We'll get back to you shortly.")
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/buy')
def buy():
    return render_template("buy.html")

@app.route('/3')
def preview():
    return render_template("3d.html")

if __name__ == '__main__':
    app.run(debug=True)
