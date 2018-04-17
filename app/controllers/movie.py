from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash, jsonify
import app.models.movie as movie_model

movie = Blueprint('movie', __name__)


# page d'accueil des films
@movie.route('/', methods=['GET'])
def index():
	return render_template('movie/index.html',
	                       top_rated=movie_model.get_top_rated_movies(6),
	                       most_commented=movie_model.get_most_commented_movies(6),
	                       most_interested=movie_model.get_most_interested_movies(6))


# page d'affichage d'un film avec la pagination
@movie.route('/<identifiant>', methods=['GET'], defaults={'page': 0})
@movie.route('/<identifiant>/<page>', methods=['GET'])
def show(identifiant, page):
	item = movie_model.show_movie(identifiant)
	if item is None:
		return redirect(request.referrer or '/')
	tab = []
	for i in range(0, round(movie_model.get_nb_comments(identifiant) / 20)):
		tab.append(i)
	return render_template('movie/show.html',
	                       item=item,
	                       page=page,
	                       tab=tab,
	                       countries=movie_model.get_countries(identifiant),
	                       casting=movie_model.get_casting(identifiant),
	                       user_review=movie_model.get_user_review(identifiant,
	                                                               session['id']) if 'id' in session else (),
	                       reviews=movie_model.get_reviews(identifiant, 20, page),
	                       genres=movie_model.get_genres(identifiant),
	                       wishlist=movie_model.get_user_wishlist(identifiant,
	                                                              session['id']) if 'id' in session else ())


# ajax pour ajouter une note
@movie.route('/<id>/review', methods=['POST'])
def review(id):
	test = movie_model.rate_movie(id, session['id'], request.form['rate'])
	return jsonify(test)


# page d'ajout d'un commentaire
@movie.route('/<id>/comment', methods=['POST'])
def comment(id):
	if session['id'] is None or request.form['review'] is None:
		abort(400)
	if movie_model.comment_movie(id, session['id'], request.form['review']) is True:
		flash('Your comment have been added', 'success')
	else:
		flash('The database is unavailable', 'error')
	return redirect(request.referrer or '/')


# page de suppression d'un commenataire
@movie.route('/<id>/delete_comment', methods=['GET'])
def delete_comment(id):
	print(id)
	if session['id'] is None:
		abort(403)
	movie_model.delete_comment(id, session['id'])
	return redirect(request.referrer or '/')


# page de suppression d'une note
@movie.route('/<id>/delete_rate', methods=['GET'])
def delete_rate(id):
	if session['id'] is None:
		abort(403)
	movie_model.delete_rate(id, session['id'])
	return redirect(request.referrer or '/')


# page pour changer le status d'un element dans la wishlist
@movie.route('/<id>/wishlist', methods=['GET'])
def wishlist(id):
	if session['id'] is None is None:
		abort(400)
	movie_model.wishlist_movie(id, session['id'])
	return redirect(request.referrer or '/')


# page des films les mieux notés
@movie.route('/top_rate', methods=['GET'], defaults={'page': 0})
@movie.route('/top_rate/<int:page>', methods=['GET'])
def best_rate(page):
	tab = []
	for i in range(0, round(movie_model.get_total_movie_number() / 20)):
		tab.append(i)
	
	return render_template('movie/top_rate.html',
	                       top_rated=movie_model.get_top_rated_movies(20, page),
	                       tab=tab,
	                       page=page)


# page des films les plus commentés
@movie.route('/most_commented', methods=['GET'], defaults={'page': 0})
@movie.route('/most_commented/<int:page>', methods=['GET'])
def most_commented(page):
	tab = []
	for i in range(0, round(movie_model.get_total_movie_number() / 20)):
		tab.append(i)
	return render_template('movie/most_commented.html',
	                       top_rated=movie_model.get_most_commented_movies(20, page),
	                       tab=tab,
	                       page=page)


# page des films les plus ajouter a la wishlist
@movie.route('/most_wishlisted', methods=['GET'], defaults={'page': 0})
@movie.route('/most_wishlisted/<int:page>', methods=['GET'])
def most_wishlisted(page):
	tab = []
	for i in range(0, round(movie_model.get_total_movie_number() / 20)):
		tab.append(i)
	return render_template('movie/most_wishlisted.html',
	                       top_rated=movie_model.get_most_interested_movies(20, page),
	                       tab=tab,
	                       page=page)
