import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .forms import PostForm
from game import db
from .models import Post, User
from uuid import uuid4


# Setting main blueprint
main = Blueprint('main', __name__)


# Index page view
@main.route('/')
@main.route('/home')
def index_page():
	posts = Post.query.all()
	for datas in posts:
		with open(f'game/static/image_{datas.id}.jpg', 'wb') as f:
			images = f.write(datas.image)
	return render_template('index.html', posts=posts)


# Add post page view
@main.route('/add-post', methods=['GET', 'POST'])
def add_post_page():
	form = PostForm()

	if request.method == 'POST':
		title = form.title.data
		description = form.description.data
		author = current_user.username

		if 'file' not in request.files:
			flash(['No file part'], category='danger')
			return redirect(request.url)
		file = request.files['file']

		if file.filename == '':
			new_post = Post(title=title, description=description, author=author)
			db.session.add(new_post)
			db.session.commit()

			return redirect(url_for('main.index_page'))

		if file:
			filename = f'{uuid4()}.jpg'
			file.save(os.path.join('game/static/', filename))
			with open(f'game/static/{filename}', 'rb') as f:
				file_data = f.read()
			os.remove(f'game/static/{filename}')
			new_post = Post(title=title, description=description, image=file_data, author=author)
			db.session.add(new_post)
			db.session.commit()
			return redirect(url_for('main.index_page'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(err_msg, category='danger')

	if current_user.is_authenticated:
		return render_template('add_post.html', form=form)

	else:
		return redirect(url_for('main.index_page'))


# User profile page view
@main.route('/user/<username>')
def user_page(username):
	user = User.query.filter_by(username=username).first()
	if user:
		username = user.username
		email = user.email
		return render_template('user.html', username=username, email=email)

	else:
		return '<h2 style="text-align: center;">User not found!</h2>'

 
# Article page view
@main.route('/posts/<id>-post')
def post_page(id):
	post = Post.query.filter_by(id=id).first()

	if post:
		with open(f'game/static/image_{post.id}.jpg', 'wb') as f:
			images = f.write(post.image)
		return render_template('post.html', post=post)

	else:
		return render_template('404-error.html')


