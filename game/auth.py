from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user
from .models import User
from . import db


auth = Blueprint('auth', __name__)

# Register page
@auth.route('/user/register', methods=['GET', 'POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			flash(['This username already exists! Try with another username.'], category='danger')
			return redirect(url_for('auth.register_page'))
		
		else:
			user = User.query.filter_by(email=form.email_address.data).first()

			if user:
				flash(['This email already exists! Try with another email.'], category='danger')
				print('YESSSSSSSSSSSSSS')
				return redirect(url_for('auth.register_page'))		

			else:
				new_user = User(
					username=form.username.data, 
					email=form.email_address.data, 
					password=form.password1.data
				)
				db.session.add(new_user)
				db.session.commit()
				login_user(new_user)

				flash(['You are logged successfully!'], category='success')
				return redirect(url_for('main.index_page'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(err_msg, category='danger')

	return render_template('register.html', form=form)


# Login page
@auth.route('/user/login', methods=['GET', 'POST'])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.query.filter_by(username=username, password=password).first()

		if user:
			login_user(user)
			flash(['You are logged successfully!'], category='success')
			return redirect(url_for('main.index_page'))

		else:
			flash(['Username or password invalid! Try again.'], category='danger')
			return redirect(url_for('auth.login_page'))

	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(err_msg, category='danger')

	return render_template('login.html', form=form)


# Logout
@auth.route('/user/logout')
def logout_page():
	logout_user()
	flash(["You have been logged out!"], category='info')
	return redirect(url_for("main.index_page"))
