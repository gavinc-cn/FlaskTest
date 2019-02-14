from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


def values2dict(content):
    _dict = {}
    for i in content:
        _dict[i] = content[i]
    return _dict


@app.route("/mirror", method=['GET', "POST"])
def mirror():
    content = values2dict(request.values)
    return jsonify(content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6699)

