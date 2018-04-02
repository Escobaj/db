from flask import Flask
from flask import render_template

from app.controllers.signup import signup
from app.controllers.movie import movie

app = Flask(__name__)


@app.route('/')
def hello_world():
	return render_template("index.html")


app.register_blueprint(signup)
app.register_blueprint(movie, url_prefix='/movie')

app.secret_key = "92EJDI1JDN2189DYHG890DUJ1902UJDD"

if __name__ == '__main__':
	app.run()
