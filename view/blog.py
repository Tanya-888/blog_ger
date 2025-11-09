from flask import Blueprint, render_template, request, redirect, url_for
import random
from controller.blog import BlogController as controller
import werkzeug.exceptions as exceptions


blog_bp = Blueprint('blog', __name__, template_folder='templates/blog', url_prefix='/blog')


@blog_bp.before_request
def add_request_id():
    request.request_id = random.randint(1000, 9999)


@blog_bp.route("/post/<post_id>", methods=['GET'])
def blog_post(post_id):
    try:
        blog_item = controller.blog_post(post_id)
    except ValueError:
        raise exceptions.BadRequest("Post not found")

    return render_template('blog/post.html', post=blog_item, username=request.request_user)


@blog_bp.route("/add_post", methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        try:
            post_id = controller.add_post(title, content)
        except ValueError as e:
            return render_template(
                'blog/add_post.html', 
                form_error=str(e),
                old_title=title,
                old_content=content,
                username=request.request_user)

        return redirect(url_for('blog.blog_post', post_id=post_id))

    return render_template('blog/add_post.html', username=request.request_user)

@blog_bp.route("/update_post/<post_id>", methods=['GET', 'POST'])
def update_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        post_id = controller.update_post(post_id, title, content)

        return redirect(url_for('blog.blog_post', post_id=post_id))

    post = controller.blog_post(post_id)

    return render_template('blog/update_post.html', post=post, username=request.request_user)


@blog_bp.route("/delete/<post_id>", methods=['GET'])
def delete_post(post_id):
    is_deleted = controller.delete_post(post_id)

    if is_deleted:
        return redirect("/")
    
    raise exceptions.BadRequest("Post not found")
