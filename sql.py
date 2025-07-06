from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# Forms
class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(4, 15)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    gender = SelectField(
        "Gender",
        choices=[
            ('', 'Select Gender'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer-not-to-say', 'Prefer not to say')
        ],
        validators=[Optional()]
    )
    dob = DateField(
        "Date of Birth",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(5, 15)]
    )
    conform_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(5, 15), EqualTo("password", message="Passwords must match")]
    )
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(4, 150)]
    )
    remember = BooleanField(
        "Remember me"
    )
    submit = SubmitField("Login")

class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(),Length(2,20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    message = TextAreaField(
        'Message',
        validators=[DataRequired(), Length(min=10)]
    )
    submit = SubmitField('Send Message')