from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash
# import app.models.signup as user_model

movie = Blueprint('movie', __name__, )


@movie.route('/', methods=['GET'])
def index():
	return render_template('movie/index.html')


@movie.route('/<id>', methods=['GET'])
def show(id):
	return render_template('movie/show.html')
