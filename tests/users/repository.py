# -*- coding: utf-8 -*-
from json import dumps, loads
from flask import url_for
import ipdb

def test_insert_user(user_repo, fake_user):
   
    payload = loads(fake_user)
    response = user_repo.create(payload)
    ipdb.set_trace()

def test_delete_user_by_id(user_repo, user_db):
    _id = user_db.query.first().id
    
    ipdb.set_trace()
    response = user_repo.remove_by_id(_id)
    assert response is True  
    ipdb.set_trace()


    
def test_response_422_when_empty_payload( client, unauthenticated_headers):            
    resp = client.post(url_for('user_bp.create', _external=True), headers=unauthenticated_headers)

    # resp = client.post(ENDPOINT, content_type='application/json')
    # ipdb.set_trace()
    assert resp.status_code == 422
# 
#     def test_message_when_empty_payload(self, test_client):
#         resp = client.post(ENDPOINT)
#         assert resp.json.get('message') == MSG_NO_DATA
# 
#     def test_response_422_when_data_is_not_valid(self, test_client):
#         resp = client.post(
#             ENDPOINT,
#             data=dumps(dict(foo='bar')),
#             content_type='application/json'
#         )
#         assert resp.status_code == 422
# 
#     def test_message_when_password_is_not_valid(self, test_client):
#         resp = client.post(
#             ENDPOINT,
#             data=dumps(dict(foo='bar')),
#             content_type='application/json'
#         )
#         assert resp.json.get('message') == MSG_INVALID_DATA
#         assert resp.json.get('errors').get('password') == MSG_PASSWORD_DIDNT_MATCH
# 
#     def test_message_required_when_fullname_not_in_payload(self, test_client):
#         resp = client.post(
#             ENDPOINT,
#             data=dumps(dict(email='teste@teste.com', password='123456', confirm_password='123456')),
#             content_type='application/json'
#         )
#         assert resp.json.get('message') == MSG_INVALID_DATA
#         assert resp.json.get('errors').get('full_name')[0] == MSG_FIELD_REQUIRED
# 
#     def test_message_required_when_email_not_in_payload(self, test_client):
#         resp = client.post(
#             ENDPOINT,
#             data=dumps(dict(full_name='teste', password='123456', confirm_password='123456')),
#             content_type='application/json'
#         )
#         assert resp.json.get('message') == MSG_INVALID_DATA
#         assert resp.json.get('errors').get('email')[0] == MSG_FIELD_REQUIRED
# 
#     def test_responses_already_exists(self, client, mongo):
#         client.post(
#             ENDPOINT,
#             data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
#             content_type='application/json'
#         )
# 
#         resp_2 = client.post(
#             ENDPOINT,
#             data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
#             content_type='application/json'
#         )
# 
#         assert resp_2.status_code == 400
#         assert resp_2.json.get('message') == MSG_ALREADY_EXISTS.format('usuário')
# 
# 
#     def test_responses_ok(self, client, mongo):
#         resp = client.post(
#             ENDPOINT,
#             data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
#             content_type='application/json'
#         )
# 
#         assert resp.status_code == 200
#         assert resp.json.get('message') == MSG_RESOURCE_CREATED.format('Usuário')
