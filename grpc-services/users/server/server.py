from concurrent import futures
import time
import logging


import grpc

import users_pb2_grpc as users_service
import users_types_pb2 as users_messages

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersService(users_service.UsersServicer):

    def CreateUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        print('CreateUser------------')
        print(metadata)
        user = users_messages.User(username=request.username, user_id=1)
        return users_messages.CreateUserResult(user=user)

    def GetUsers(self, request, context):
        for user in request.user:
            user = users_messages.User(
                username=user.username, user_id=user.user_id
            )
            yield users_messages.GetUsersResult(user=user)


def serve():
    print('Start GRPC server')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_service.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            print('Listening......')
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
        print('STOP GRPC ......')


if __name__ == '__main__':
    serve()
