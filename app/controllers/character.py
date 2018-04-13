from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash, jsonify
import app.models.character as actor_model

character = Blueprint('character', __name__)


@character.route('/<identifiant>', methods=['GET'])
def show(identifiant):
	return render_template('character/show.html',
	                       character=actor_model.get_character(identifiant),
	                       items=actor_model.get_all_elements(identifiant))