from flask import Blueprint, render_template, request, make_response, redirect
from controller.user import UserController as controller

user_bp = Blueprint('user', __name__, template_folder='../templates/user', url_prefix='/user')


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.request_user is not None:
        return "You are already logged in", 400
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            user = controller.login(username, password)
        except ValueError as e:
            return render_template(
                'login.html', 
                form_error=str(e),
                old_username=username,
                username=request.request_user
            )

        resp = make_response(redirect("/"))
        resp.set_cookie('user_name', user.name)
        resp.set_cookie('token', user.password)

        return resp

    return render_template('login.html', username=request.request_user)

@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.request_user is not None:
        return "You are already logged in", 400
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        
        try:
            user = controller.register(username, password, repeat_password)
        except ValueError as e:
            return render_template(
                'register.html', 
                form_error=str(e),
                old_username=username,
            )

        resp = make_response(redirect("/"))
        resp.set_cookie('user_name', user.name)
        resp.set_cookie('token', user.password)

        return resp

    return render_template(
        'register.html',
    )


@user_bp.route("/logout", methods=['GET'])
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('user_name', '', expires=0)
    resp.set_cookie('token', '', expires=0)

    return resp

@user_bp.route("/", methods=['GET'])
def get_users():
    if request.request_user is None:
        return "Unauthorized", 401


    users = controller.get_users()
    

    return render_template('user_list.html', users=users, username=request.request_user)
