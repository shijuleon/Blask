"""


"""


from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, g
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import TextField, validators, PasswordField, TextAreaField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


#Mapped classes
class Posts(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	content = db.Column(db.Text)
	pub_dtime = db.Column(db.Integer, default=datetime.now().strftime("%A, %B %d, %Y, %H:%M"))

	def __repr__(self):
		return '<id %r>' % self.id
#Forms
class CreatePostForm(Form):
	title = TextField('Title', [validators.required("Please enter a title")])
	content = TextAreaField('Content', [validators.required("Please enter a body.")])

#Define pages functionality
@app.route('/')
def index():
		instance = db.session.query(Posts).order_by(Posts.id.desc())
		return render_template('index.html', instance=instance, app=app)

@app.route('/<int:id>/<string:title>')
def show(id, title):
	instance = db.session.query(Posts).filter(id==id).first()
	return render_template('show.html', instance=instance, app=app)


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'	
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('admin'))
	return render_template('login.html', error=error, app=app)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out!')
	return redirect(url_for('index'))

@app.route('/admin')
def admin():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	instance = db.session.query(Posts).order_by(Posts.id.desc())
	return render_template('admin.html', instance=instance, app=app)

@app.route('/admin/add', methods=['GET', 'POST'])
def addpost():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	post = Posts()
	form = CreatePostForm()
	if form.validate_on_submit():
		form.populate_obj(post)
		db.session.add(post)
		db.session.commit()
		flash("New post added!")
		return redirect(url_for('index'))
	return render_template('add.html', form=form, post=post, app=app)

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def editpost(id):
	if not session.get('logged_in'):
		return redirect(url_for('login'))		
	post = Posts.query.filter(Posts.id == id).first()
	form = CreatePostForm(request.form, post)
	if form.validate_on_submit():
		form.populate_obj(post)
		db.session.add(post)
		db.session.commit()
		flash("Post edited!")
		return redirect(url_for('admin'))
	return render_template('edit.html', form=form, post=post, app=app)

@app.route('/admin/delete/<int:id>')
def deletepost(id):
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	delete = db.session.query(Posts).filter(id==id).first()
	db.session.delete(delete)
	db.session.commit()
	flash("Post deleted!")
	return redirect(url_for('admin'))

#Rock and roll
if __name__ == '__main__':
	app.run(debug=True)