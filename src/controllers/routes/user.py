from src.utils.email_holder import send_template_email
import os
from src.utils.email_holder import send_email
# from src.utils.user import send_email
import ipdb
from flask import Blueprint, request, jsonify, redirect, url_for, make_response, current_app, render_template
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from src.service_layer import UserService
import src.utils.messages as msg

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/', methods=['GET'])
def get():
    # ipdb.set_trace()
    return {'ok': 200}


@user_bp.route('/', methods=['POST'])
def create():
    if not request.data:
        return jsonify({'error': msg.MSG_NO_DATA}), 422

    service = UserService()
    data = request.get_json()
    result = service.signin(data)
    # ipdb.set_trace()

    response = make_response(result, result.pop('status_code', 201))
    return response


@user_bp.route('/login', methods=['POST'])
def login():

    if not request.data:
        return jsonify({'error': msg.MSG_NO_DATA}), 422

    service = UserService()
    data = request.get_json()

    result = service.login(data)

    response = jsonify(result)

    response.status_code = result.pop('status_code', 201)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


@user_bp.route('/logout', methods=('DELETE',))
@jwt_required()
def logout():
    service = UserService()
    jwt = get_jwt()
    result = service.logout(jwt)
    return redirect(url_for('login'))  # jsonify(msg="Access token revoked")


@user_bp.route('/', methods=['PATCH'])
@jwt_required()
def update():
    if not request.data:
        return jsonify({'error': msg.MSG_NO_DATA}), 422
    current_user = get_jwt_identity()
#    ipdb.set_trace()
    data = request.get_json()
    service = UserService()
    result = service.update(current_user, data)
    # ipdb.set_trace()

    response = make_response(result, result.pop('status_code', 201))
    return response


@user_bp.route('/pwd', methods=['PATCH'])
@jwt_required()
def change_password():
    if not request.data:
        return jsonify({'error': msg.MSG_NO_DATA}), 422
    current_user = get_jwt_identity()

    service = UserService()
    data = request.get_json()
    result = service.change_password(current_user, data, get_jwt())

    response = make_response(result, result.pop('status_code', 201))
    return response


@user_bp.route('/pwd/reset/<string:token>', methods=['POST', 'GET'])
def reset_password(token=None):

    service = UserService()
    ipdb.set_trace()
    if request.method == 'GET' and user_email is not None:
        result = service.get_reset_token(user_email=user_email)

        token = result['reset_token']
        ipdb.set_trace()

        send_template_email(
            template='template_reset_password.html',
            to=user_email,
            subj='You added a site!',
            name='user.first_name',
            url='www.contoso.com.br'
        )

        return make_response(result, result.pop('status_code', 200))

    data = request.get_json()
    ipdb.set_trace()
    result = service.change_password(current_user, data, get_jwt())

    response = make_response(result, result.pop('status_code', 201))
    return response


@user_bp.route('/pwd/reset', methods=['POST', 'GET'])
def reset_password_request():
    service = UserService()
    user_email = request.args.get('email')
    ipdb.set_trace()
    if request.method == 'GET' and user_email is not None:
        result = service.get_reset_token(user_email=user_email)

        token = result['reset_token']
        ipdb.set_trace()

        send_template_email(
            template='template_reset_password.html',
            to=user_email,
            subj='You added a site!',
            name='user.first_name',
            url='www.contoso.com.br'
        )

        return make_response(result, result.pop('status_code', 200))

    data = request.get_json()
    ipdb.set_trace()
    result = service.change_password(current_user, data, get_jwt())

    response = make_response(result, result.pop('status_code', 201))
    return response


def send_password_reset_request_email(user_name, reset_link):

    tmpl_context = {
        'reset_link': reset_link,
        'name': user_name
    }
    ipdb.set_trace()
    email_msg = EmailHolder(
        subject='{} password reset request'.format(
            os.getenv('GLOBAL_SITE_NAME')),
        recipient=user_name,
        text=render_template(
            '/home/loon/projects/gestao_de_horas/src/utils/templates/reset-request.html', **tmpl_context),
        html=render_template(
            'src/utils/templates/reset-request.html', **tmpl_context),
    )

    send_email(email_msg)
