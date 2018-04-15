from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash, jsonify
import app.models.serie as serie_model

serie = Blueprint('serie', __name__)


@serie.route('/', methods=['GET'])
def index():
	return render_template('serie/index.html',
	                       top_rated=serie_model.get_top_rated_series(6),
	                       most_commented=serie_model.get_most_commented_series(6),
	                       most_interested=serie_model.get_most_interested_series(6))


@serie.route('/<identifiant>', methods=['GET'])
def show(identifiant):
	item = serie_model.show_serie(identifiant)
	if item is None:
		return redirect(request.referrer or '/')
	return render_template('serie/show.html',
	                       item=item,
	                       countries=serie_model.get_countries(identifiant),
	                       casting=serie_model.get_casting(identifiant),
	                       user_review=serie_model.get_user_review(identifiant,
	                                                               session['id']) if 'id' in session else (),
	                       reviews=serie_model.get_reviews(identifiant),
	                       genres=serie_model.get_genres(identifiant),
	                       wishlist=serie_model.get_user_wishlist(identifiant,
	                                                              session['id']) if 'id' in session else ())


@serie.route('/<id>/review', methods=['POST'])
def review(id):
	test = serie_model.rate_serie(id, session['id'], request.form['rate'])
	return jsonify(test)


@serie.route('/<id>/comment', methods=['POST'])
def comment(id):
	if session['id'] is None or request.form['review'] is None:
		abort(400)
	if serie_model.comment_serie(id, session['id'], request.form['review']) is True:
		flash('Your comment have been added', 'success')
	else:
		flash('The database is unavailable', 'error')
	return redirect(request.referrer or '/')


@serie.route('/<id>/delete_comment', methods=['GET'])
def delete_comment(id):
	print(id)
	if session['id'] is None:
		abort(403)
	serie_model.delete_comment(id, session['id'])
	return redirect(request.referrer or '/')


@serie.route('/<id>/delete_rate', methods=['GET'])
def delete_rate(id):
	if session['id'] is None:
		abort(403)
	serie_model.delete_rate(id, session['id'])
	return redirect(request.referrer or '/')


@serie.route('/<id>/wishlist', methods=['GET'])
def wishlist(id):
	if session['id'] is None is None:
		abort(400)
	serie_model.wishlist_serie(id, session['id'])
	return redirect(request.referrer or '/')


@serie.route('/top_rate', methods=['GET'], defaults={'page': 0})
@serie.route('/top_rate/<int:page>', methods=['GET'])
def best_rate(page):
	tab = []
	for i in range(0, round(serie_model.get_total_serie_number() / 20)):
		tab.append(i)
	
	return render_template('serie/top_rate.html',
	                       top_rated=serie_model.get_top_rated_series(20, page),
	                       tab=tab,
	                       page=page)


@serie.route('/most_commented', methods=['GET'], defaults={'page': 0})
@serie.route('/most_commented/<int:page>', methods=['GET'])
def most_commented(page):
	tab = []
	for i in range(0, round(serie_model.get_total_serie_number() / 20)):
		tab.append(i)
	return render_template('serie/most_commented.html',
	                       top_rated=serie_model.get_most_commented_series(20, page),
	                       tab=tab,
	                       page=page)


@serie.route('/most_wishlisted', methods=['GET'], defaults={'page': 0})
@serie.route('/most_wishlisted/<int:page>', methods=['GET'])
def most_wishlisted(page):
	tab = []
	for i in range(0, round(serie_model.get_total_serie_number() / 20)):
		tab.append(i)
	return render_template('serie/most_wishlisted.html',
	                       top_rated=serie_model.get_most_interested_series(20, page),
	                       tab=tab,
	                       page=page)