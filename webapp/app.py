from flask import Flask, Response
import sys
import os
from google.protobuf.json_format import MessageToJson
from client_wrapper import ServiceClient
GRPC_HOST = os.environ.get('GRPC_HOST', "users")
GRPC_PORT=int(os.environ.get('GRPC_PORT', 50051))
import users_pb2_grpc as users_service
import users_types_pb2 as users_messages
import logging
LOG = logging.getLogger('app')

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
@app.route("/healthz")
def ping():
    LOG.info('--------------aaa-----------')
    res = users_get()
    LOG.info('--------------bbb-----------')
    LOG.info(f'ping res={res}')
    return "ok", 200

@app.route('/users/')
def users_get():
    LOG.info(f'start connect to GRPC server GRPC_HOST={GRPC_HOST} GRPC_PORT={GRPC_PORT}')
    try:
        app.config['users'] = ServiceClient(users_service, 'UsersStub', GRPC_HOST, GRPC_PORT)
        request = users_messages.GetUsersRequest(
            user=[users_messages.User(username="alexa", user_id=1),
                users_messages.User(username="christie", user_id=1)]
        )
        def get_user():
            response = app.config['users'].GetUsers(request)
            for resp in response:
                yield MessageToJson(resp)
        return Response(get_user(), content_type='application/json')
    except Exception as e:
        LOG.error(f'Exception ex={e}')
        return {'code':200, 'mess':'fake'}
