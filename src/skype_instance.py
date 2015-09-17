from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

from logger import Connection




"""
Example of json-rpc usage with Wergzeug and requests.

NOTE: there are no Werkzeug and requests in dependencies of json-rpc.
NOTE: server handles all url paths the same way (there are no different urls).
"""


def auth(skypename, password):
    """

    :param str skypename:
    :param str password:
    :return:
    """
    print '\n\nGot request on auth'
    print 'provided skypename is:', skypename
    print 'provided password is:', password
    print '\n\n'

    connection.connect()

    return True


def shutdown():
    """

    :return:
    """
    print '\n\nGot request on shutdown\n\n'

    connection.shutdown()

    return True


# @dispatcher.add_method
def send_message(skypename, message):
    """

    :param str skypename:
    :param str message:
    :return:
    """
    print skypename, '::', message

    connection.wrapped_send(skypename, message)

    return True


def on_message_callback(message):
    """

    :param str message:
    :return:
    """
    print '*' * 30
    print 'Received message:'
    print message
    print '^' * 30


connection = Connection(on_message_callback)



@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher['auth'] = auth
    dispatcher['shutdown'] = shutdown
    dispatcher['send_message'] = send_message

    response = JSONRPCResponseManager.handle(
        request.get_data(cache=False, as_text=True),
        dispatcher
    )

    return Response(response.json, mimetype='application/json')


def init():
    run_simple('localhost', 4000, application)


if __name__ == '__main__':
    init()
