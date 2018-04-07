from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash
import app.models.movie as movie_model

movie = Blueprint('movie', __name__, )


@movie.route('/', methods=['GET'])
def index():
	return render_template('movie/index.html',
	                       top_rated=movie_model.get_top_rated_movies(6),
	                       most_commented=movie_model.get_most_commented_movies(6),
	                       most_interested=movie_model.get_most_interested_movies(6))


@movie.route('/<id>', methods=['GET'])
def show(id):
	return render_template('movie/show.html',
	                       item = movie_model.show_movie(id))
