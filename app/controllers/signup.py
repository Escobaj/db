from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash
import app.models.signup as user_model
from pymysql import MySQLError


signup = Blueprint('signup', __name__, )


@signup.route('/login', methods=['GET'])
def login():
	if 'username' in session:
		flash(u'you are already logged in', 'info')
		return redirect(request.referrer or '/')
	
	return render_template('signup/login.html')


@signup.route('/login', methods=['POST'])
def connect():
	user_exist = 0
	if 'username' in session:
		flash(u'you are already logged in', 'info')
		return redirect(request.referrer or '/')
	
	if request.form['username'] is None or request.form['password'] is None:
		return redirect(url_for('signup.login'))
	else:
		
		try:
			user_exist = user_model.user_exist(request.form['username'], request.form['password'])
		
		except:
			abort(500)
		
		if user_exist == 1:
			session['username'] = request.form['username']
			flash(u'Connected with success', 'success')
			return redirect('/')
		else:
			flash(u'Invalid username or password', 'error')
			return render_template('signup/login.html')


@signup.route('/logout', methods=['GET'])
def logout():
	session.pop('username')
	flash(u'You are now disconnected.', 'info')
	return redirect(request.referrer or '/')


@signup.route('/register', methods=['GET'])
def register_form():
	return render_template('signup/register.html')


@signup.route('/register', methods=['POST'])
def register():
	if (request.form['username'].strip() != '' or request.form['password'].strip() != '' or request.form[
		'first_name'].strip() != '' or request.form['last_name'].strip() != '' or request.form['email'].strip() != ''):
		
		try:
			user_model.create_user(request.form['username'], request.form['password'],
			                       request.form['first_name'], request.form['last_name'], request.form['email'])
			flash(u'User have been created', 'error')
			return redirect(url_for('signup.login'))
		except MySQLError:
			flash(u'Username or Email is already used', 'error')
			return render_template('signup/register.html')
	else:
		return render_template('signup/register.html')
