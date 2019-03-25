from flask import request, render_template, jsonify, url_for, redirect, g, render_template_string
from .models import User
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token
from .libs.mailgun import mailgun as mg
import json

REACT_COMPONENT_TEMPLATE = "<div data-react-props='{{props}}' data-react-class={{ name }}></div>"


@app.template_global()
def react_component(name, props={}):
    return render_template_string(REACT_COMPONENT_TEMPLATE, name=name, props=json.dumps(props))


@app.route('/', methods=['GET'])
def index():
    return render_template('templates/index.html')


@app.route("/reactdemo", methods=['GET'])
def reactdemo():
    return render_template("templates/reactdemo.html")


@app.route('/user/new', methods=['GET'])
def user_new():
    return render_template('templates/user/new.html')


@app.route('/user/create', methods=['POST'])
def user_create():

    # Get values that were entered into the form
    email = request.form.get('email')
    password = request.form.get('password')

    # Instantiate a new user object
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect('/')


@app.route('/user/invite', methods=['GET'])
def user_invite():
    return render_template('templates/user/invite.html')


@app.route('/user/invite-sent', methods=['POST'])
def user_invites_sent():
    # Get email address from invitation form
    email = request.form.get('email')
    try:
        mg.send(email)
    except:
        pass
    print("invite sent!!")
    return redirect('/')


@app.route("/login", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


'''
@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )
'''


@app.route("/user/create", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403
