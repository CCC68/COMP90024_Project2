from flask import Flask, json, url_for, redirect, render_template, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/map/vic", methods=["GET"])
def map_vic():
    filename = "vic_plus.json"
    directory = "aurin"
    try:
        with open(directory + '/' + filename) as f:
            jsonStr = json.load(f)
            return json.dumps(jsonStr)
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


@app.route("/map/nsw", methods=["GET"])

def map_nsw():
    filename = "nsw_plus.json"
    directory = "aurin"
    try:
        with open(directory + '/' + filename) as f:
            jsonStr = json.load(f)
            return json.dumps(jsonStr)
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})

if __name__ == '__main__':
    app.run(debug=True)
