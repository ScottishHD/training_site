from gevent.wsgi import WSGIServer
from sha_training_app import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
