from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash, jsonify
import app.models.search as search_model

search = Blueprint('search', __name__)


# page ajax pour retourner les 3 meilleurs resultats
@search.route('/', methods=['GET'], defaults={'query': ''})
@search.route('/<query>', methods=['GET'])
def search_query(query):
	result = search_model.search(query)
	return jsonify(result)