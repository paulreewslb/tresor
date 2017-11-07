import pandas as pd
import flask
import flask_swagger as swagger
import functools
import json
import os

app = flask.Flask(__name__)
static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
print(static_folder_root)

specA = """
aaa

---
tags:
    - test
parameters:
    - in: query
      name: number
      type: int

response:
    200:
        description: successful operation
    400:
        description: failed to get info needed

"""

specB = """
aaa

---
tags:
    - test


response:
    200:
        description: successful operation
    400:
        description: failed to get info needed

"""


def set_docstring(value):

    def __doc(fn):
        fn.__doc__ = value
        return fn
    return __doc


@app.route('/spec')
def spec():

    swagger_spec = swagger.swagger(app)
    swagger_spec['info']['title'] = 'ZP & TAOS SWAGGER'
    swagger_spec['info']['author'] = 'ZHAOPENG'
    return flask.jsonify(swagger_spec)


@app.route('/', methods=['GET'])
def index():
    return flask.send_from_directory(static_folder_root, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def static_file(path):
    return flask.send_from_directory(static_folder_root, path)


@set_docstring(specA)
@app.route('/test/testA', methods=['GET'])
def testA():

    num = flask.request.args.get('number')

    return json.dumps({'x': [1, 2, int(num)]})


@set_docstring(specB)
@app.route('/test/testB', methods=['GET'])
def testB():

    return json.dumps({'x': [2, 2]})


def main():

    app.run(debug=False, host='0.0.0.0', port=5001)

if __name__ == '__main__':

    main()


