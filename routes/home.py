from flask import Blueprint, render_template

home_bp = Blueprint('Home', __name__)

@home_bp.route('/home')
def home_page():
    return render_template('home.html')