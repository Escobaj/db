from flask import Flask
from flask import render_template

from app.controllers.signup import signup
from app.controllers.movie import movie
from app.controllers.search import search
from app.controllers.game import game
from app.controllers.serie import serie
from app.controllers.character import character

import app.models.search as search_model

app = Flask(__name__)


# page d'accueil
@app.route('/')
def hello_world():
	return render_template("index.html",
	                       random=search_model.getRandomElements(12),
	                       last_review=search_model.getLastReview(6))


app.register_blueprint(signup)
app.register_blueprint(movie, url_prefix='/movie')
app.register_blueprint(game, url_prefix='/game')
app.register_blueprint(serie, url_prefix='/serie')
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(character, url_prefix='/actor')

# permet de chiffrer les sessions
app.secret_key = "92EJDI1JDN2189DYHG890DUJ1902UJDD"

if __name__ == '__main__':
	app.run()
