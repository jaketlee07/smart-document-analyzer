from flask import Blueprint, render_template
import logging

logging.basicConfig(level=logging.DEBUG)

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    logging.debug("Rendering the uploader_form.html template")
    return render_template('uploader_form.html')
