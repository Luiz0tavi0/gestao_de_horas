# -*- coding: utf-8 -*-
from src.utils import user as user_utils
import random
from sqlalchemy import update, select
from sqlalchemy.orm import load_only, defer, Load, undefer
from flask_jwt_extended import decode_token

from json import dumps, loads
from flask import url_for
import ipdb


def test_response_201_when_new_user_created(client, unauthenticated_headers, fake_user):
    payload = loads(fake_user)

    payload.pop('active', None)
    payload.pop('projects', None)

    payload['confirm_password'] = "sEnHa_Forte_e_igual:_-123!@#4$¨%.89"
    payload['password'] = "sEnHa_Forte_e_igual:_-123!@#4$¨%.89"

    payload = dumps(payload)
#    tests/users/entrypoints.py::test_response_422_when_data_is_not_valid
    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)

    assert resp.status_code == 201


def test_response_422_when_empty_payload(client, unauthenticated_headers):

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers)
    assert resp.status_code == 422


def test_response_422_when_data_is_not_valid(client, unauthenticated_headers, fake_user):

    payload = loads(fake_user)
    payload.pop('active', None)
    payload.pop('projects', None)
    payload.pop("email")
    payload.pop('password')
    # payload['confirm_password']= payload['password']

    payload = dumps(payload)

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)

    assert resp.status_code == 422


def test_message_required_when_email_not_in_payload(client, unauthenticated_headers, fake_user):
    payload = loads(fake_user)
    payload.pop('active', None)
    payload.pop('projects', None)
    payload.pop('email')
    payload['confirm_password'] = payload['password']

    payload = dumps(payload)

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)
    #
    assert resp.status_code == 422
    assert loads(resp.data)['errors'][0]['msg'] == 'field required' and loads(
        resp.data)['errors'][0]['field'] == 'email'


def test_message_response_when_confirm_password_not_in_payload(client, unauthenticated_headers, fake_user):
    payload = loads(fake_user)
    import ipdb
#
    payload.pop('active', None)
    payload.pop('projects', None)
    payload.pop('email')
    payload.pop('confirm_password', None)

    payload = dumps(payload)

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)
    import ipdb
#
    assert resp.status_code == 422
    assert loads(resp.data)['errors'][0]['msg'] == 'field required' and loads(
        resp.data)['errors'][0]['field'] == 'confirm_password'


def test_message_required_when_password_not_in_payload(client, unauthenticated_headers, fake_user):
    payload = loads(fake_user)
    payload.pop('active', None)
    payload.pop('projects', None)
    payload.pop('password')

    payload = dumps(payload)

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)
    # import ipdb;
    assert resp.status_code == 422
    assert loads(resp.data)['errors'][0]['msg'] == 'field required' and loads(
        resp.data)['errors'][0]['field'] == 'password'


def test_response_422_when_password_is_not_strongest(client, unauthenticated_headers, fake_user):

    payload = loads(fake_user)
    payload.pop('active', None)
    payload.pop('projects', None)

    #
    # senha fraca
    payload['password'] = '15498sa4d9a'
    payload['confirm_password'] = '15498sa4d9a'

    payload = dumps(payload)

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)

    assert resp.status_code == 422


def test_response_401_when_password_is_incorrect(client, unauthenticated_headers, fake_user, random_user_already_registered):
    payload = loads(fake_user)

    payload = dumps({
        "email": random_user_already_registered.email,
        # user_already_registered.password
        "password":  "sEnHa_Errada_Forte_e_igual:_-123!@#4$¨%.89"[23:]
    }
    )

    resp = client.post(url_for('user_bp.login', _external=True),
                       headers=unauthenticated_headers, data=payload)

    assert resp.status_code == 401


def test_response_message_when_password_and_password_confirmation_are_different(client, unauthenticated_headers, fake_user):
    payload = loads(fake_user)
    payload.pop('active', None)
    payload.pop('projects', None)

    payload['confirm_password'] = payload['password'][::-1]

    payload = dumps(payload)
    import ipdb
#

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)

#    assert resp.status_code == 401
    assert 'Password and confirm password must be equal.' in loads(resp.data)['errors'][0]['msg'] and\
           loads(resp.data)['errors'][0]['field'] == 'confirm_password'


def test_response_202_when_login_is_sucesfull(client, unauthenticated_headers, fake_user, random_user_already_registered):
    payload = loads(fake_user)

    payload = dumps({
        "email": random_user_already_registered.email,
        "password":  random_user_already_registered.password
    }
    )
    # ipdb.set_trace()

    resp = client.post(
        url_for('user_bp.login', _external=True), headers=unauthenticated_headers, data=payload
    )
    ipdb.set_trace()
    assert loads(resp.data).get("token", None) is not None
    assert resp.status_code == 201


def test_response_404_when_user_not_registered(client, unauthenticated_headers, fake_user):
    payload = loads(fake_user)

    payload = {
        "email": payload['email'],
        "password": payload['password']
    }

    payload = dumps(payload)

    resp = client.post(url_for('user_bp.login', _external=True),
                       headers=unauthenticated_headers, data=payload)

    assert resp.status_code == 404


def test_responses_already_exists(client, unauthenticated_headers, fake_user, random_user_already_registered):
    payload = loads(fake_user)

    payload = dumps(
        {
            "email": random_user_already_registered.email,
            "cpf": random_user_already_registered.cpf,
            "name": random_user_already_registered.name,
            "password": "sEnHa_Forte_e_igual:_-123!@#4$¨%.89",
            "confirm_password": "sEnHa_Forte_e_igual:_-123!@#4$¨%.89",
            "occupation": random_user_already_registered.occupation,

        }
    )

    resp = client.post(url_for('user_bp.create', _external=True),
                       headers=unauthenticated_headers, data=payload)

    assert resp.status_code == 422


def test_message_response_when_update_user_password(client, header_with_access_token, fake_user, random_user_already_registered):

    payload = loads(fake_user)

    payload = loads(fake_user)
    # import ipdb;
    payload['email'] = "carvalhoana-julia@example.com"
    payload['password'] = "Nova_SENHA*Forte123456789"
    payload['confirm_password'] = "Nova_SENHA*Forte123456789"

    payload = dumps(payload)

    resp = client.patch(url_for('user_bp.change_password', _external=True),
                        headers=header_with_access_token, data=payload)
    import ipdb

    assert resp.status_code == 302
    # 'field required' and loads(resp.data)['errors'][0]['field'] == 'confirm_password'
    assert loads(resp.data)['status'] == 'Ok'
    assert loads(resp.data)['msg'] == 'success'


def test_response_204_when_update_user(client, header_with_access_token, fake_user, random_user_already_registered):
    # payload = loads(fake_user)
    import ipdb

    login_response = user_utils.make_login_response(
        random_user_already_registered)
    header_with_access_token = {
        'Authorization': f'Bearer {login_response["token"]}',
        'Content-Type': 'application/json'
    }

    payload = loads(fake_user)

    fields_to_update = random.sample(payload.keys(), 3)

    for key in fields_to_update:
        # print(f"{key} in payload -> {payload[key]} -------------- {key} in user -> {getattr(user,key)}")

        payload[key] = getattr(random_user_already_registered, key)

#

    payload = dumps(payload)

    resp = client.patch(url_for('user_bp.update', _external=True),
                        headers=header_with_access_token, data=payload)

    assert resp.status_code == 204


def test_message_response_when_logout_user(client, header_with_access_token):

    resp = client.delete(
        url_for('user_bp.logout', _external=True), headers=header_with_access_token)
    assert resp.status_code == 200


def test_response_200_when_password_reset_is_requested(client, random_user_already_registered):
    user_email = random_user_already_registered.email

    resp = client.get(url_for('user_bp.reset_password',
                              user_email=user_email, _external=True))

    assert resp.status_code == 204
