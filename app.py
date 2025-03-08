from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Post
from forms import LoginForm, RegistrationForm, PostForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=10)  # Hiển thị tất cả bài viết
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.is_active and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin.html', title='Admin', users=User.query.all())

@app.route('/block_user/<int:user_id>')
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user:
        user.is_active = False
        db.session.commit()
        flash(f'User {user.username} has been blocked.')
    return redirect(url_for('admin'))

@app.route('/unblock_user/<int:user_id>')
@login_required
def unblock_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user:
        user.is_active = True
        db.session.commit()
        flash(f'User {user.username} has been unblocked.')
    return redirect(url_for('admin'))

@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.')
    return redirect(url_for('admin'))

@app.route('/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user:
        new_password = generate_password_hash("default123")
        user.password = new_password
        db.session.commit()
        flash(f'Password for {user.username} has been reset.')
    return redirect(url_for('admin'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='Create Post', form=form)

@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('index'))

    if current_user.is_admin or post.user_id == current_user.id:  # Admin hoặc chủ bài viết mới có quyền xóa
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.')
    else:
        flash('You do not have permission to delete this post.')

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
