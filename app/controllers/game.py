from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash, jsonify
import app.models.game as game_model

game = Blueprint('game', __name__)


# page d'acceuil des jeux video
@game.route('/', methods=['GET'])
def index():
	return render_template('game/index.html',
	                       top_rated=game_model.get_top_rated_games(6),
	                       most_commented=game_model.get_most_commented_games(6),
	                       most_interested=game_model.get_most_interested_games(6))


# page d'affichage d'un jeu video en fonction de la pagination
@game.route('/<identifiant>', methods=['GET'], defaults={'page': 0})
@game.route('/<identifiant>/<page>', methods=['GET'])
def show(identifiant, page):
	item = game_model.show_game(identifiant)
	if item is None:
		return redirect(request.referrer or '/')
	tab = []
	for i in range(0, round(game_model.get_nb_comments(identifiant) / 20)):
		tab.append(i)
	
	return render_template('game/show.html',
	                       item=item,
	                       page=page,
	                       tab=tab,
	                       countries=game_model.get_countries(identifiant),
	                       user_review=game_model.get_user_review(identifiant,
	                                                              session['id']) if 'id' in session else (),
	                       reviews=game_model.get_reviews(identifiant, 20, page),
	                       genres=game_model.get_genres(identifiant),
	                       wishlist=game_model.get_user_wishlist(identifiant,
	                                                             session['id']) if 'id' in session else ())


# page pour ajouter une note en ajax
@game.route('/<id>/review', methods=['POST'])
def review(id):
	test = game_model.rate_game(id, session['id'], request.form['rate'])
	return jsonify(test)


# page pour ajouter un commentaire
@game.route('/<id>/comment', methods=['POST'])
def comment(id):
	if session['id'] is None or request.form['review'] is None:
		abort(400)
	if game_model.comment_game(id, session['id'], request.form['review']) is True:
		flash('Your comment have been added', 'success')
	else:
		flash('The database is unavailable', 'error')
	return redirect(request.referrer or '/')


# page de suppression d'un commentaire
@game.route('/<id>/delete_comment', methods=['GET'])
def delete_comment(id):
	print(id)
	if session['id'] is None:
		abort(403)
	game_model.delete_comment(id, session['id'])
	return redirect(request.referrer or '/')


# page de suppression d'une note
@game.route('/<id>/delete_rate', methods=['GET'])
def delete_rate(id):
	if session['id'] is None:
		abort(403)
	game_model.delete_rate(id, session['id'])
	return redirect(request.referrer or '/')


# page d'ajout et de suppression a une wishlist
@game.route('/<id>/wishlist', methods=['GET'])
def wishlist(id):
	if session['id'] is None is None:
		abort(400)
	game_model.wishlist_game(id, session['id'])
	return redirect(request.referrer or '/')


# page des jeux video meilleurs notes
@game.route('/top_rate', methods=['GET'], defaults={'page': 0})
@game.route('/top_rate/<int:page>', methods=['GET'])
def best_rate(page):
	tab = []
	for i in range(0, round(game_model.get_total_game_number() / 20)):
		tab.append(i)
	
	return render_template('game/top_rate.html',
	                       top_rated=game_model.get_top_rated_games(20, page),
	                       tab=tab,
	                       page=page)


# page des jeux video plus plus commenté
@game.route('/most_commented', methods=['GET'], defaults={'page': 0})
@game.route('/most_commented/<int:page>', methods=['GET'])
def most_commented(page):
	tab = []
	for i in range(0, round(game_model.get_total_game_number() / 20)):
		tab.append(i)
	return render_template('game/most_commented.html',
	                       top_rated=game_model.get_most_commented_games(20, page),
	                       tab=tab,
	                       page=page)


# page des jeux video les plus ajouter a la liste de souhait
@game.route('/most_wishlisted', methods=['GET'], defaults={'page': 0})
@game.route('/most_wishlisted/<int:page>', methods=['GET'])
def most_wishlisted(page):
	tab = []
	for i in range(0, round(game_model.get_total_game_number() / 20)):
		tab.append(i)
	return render_template('game/most_wishlisted.html',
	                       top_rated=game_model.get_most_interested_games(20, page),
	                       tab=tab,
	                       page=page)
