import os
import logging

from flask import Flask, request
from redis import Redis

logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
#redis = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    logging.info("Request /shutdown")
    logging.info("Server shutting down..")
    return 'Server shutting down...'

@app.route('/')
def hello():
    count = redis.incr('hits')
    logging.info("Request /")
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

