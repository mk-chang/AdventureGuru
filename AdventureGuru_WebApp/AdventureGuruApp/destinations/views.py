from flask import render_template, request, Blueprint

destinations = Blueprint('destinations',__name__)

@destinations.route('/')
def input():
    return render_template('input.html')
