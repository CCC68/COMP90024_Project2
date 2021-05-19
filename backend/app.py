from flask import Flask, json, url_for, redirect, render_template, request, jsonify

app = Flask(__name__)


@app.route("/map/<city>", methods=['GET'])
def map(city):
    filename = city + '.json'
    directory = "backend"
    try:
        with open(directory + '/' + filename) as f:
            jsonStr = json.load(f)
            return json.dumps(jsonStr)
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


@app.route('/analysis/<city>', methods=['GET'])
def analysis():
    return 1


if __name__ == '__main__':
    app.run(debug=True)
