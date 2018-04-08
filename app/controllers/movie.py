from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash, jsonify
import app.models.movie as movie_model

movie = Blueprint('movie', __name__, )


@movie.route('/', methods=['GET'])
def index():
	return render_template('movie/index.html',
	                       top_rated=movie_model.get_top_rated_movies(6),
	                       most_commented=movie_model.get_most_commented_movies(6),
	                       most_interested=movie_model.get_most_interested_movies(6), )


@movie.route('/<id>', methods=['GET'])
def show(id):
	item = movie_model.show_movie(id)
	if item is None:
		return redirect(request.referrer or '/')
	return render_template('movie/show.html',
	                       item=item,
	                       countries=movie_model.get_countries(id),
	                       casting=movie_model.get_casting(id),
	                       user_review=movie_model.get_user_review(id, session['id']),
	                       reviews=movie_model.get_reviews(id),
	                       genres=movie_model.get_genres(id))


@movie.route('/<id>/review', methods=['POST'])
def review(id):
	test = movie_model.rate_movie(id, session['id'], request.form['rate'])
	return jsonify(test)
