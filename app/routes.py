from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return 'The project page'

@main.route('/about') 
def about():
    return 'The about page'