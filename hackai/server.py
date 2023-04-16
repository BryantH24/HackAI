from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)


data = [
        {"msg": "Lebron James dunks", "generated": "Lebron james with the slam!", "score":7, "time": 123}, 
        {"msg": "Kevin Durmant", "generated": "KD Balling out!", "score":-2, "time": 123}, 
        {"msg": "Michael Jordan with the game winner", "generated": "really great shot!", "score":5, "time": 123}, 
        {"msg": "Michael Jordan with the game winner", "generated": "really awesome shot!", "score":5, "time": 123},
        {"msg": "Elvis Presley with the game winner", "generated": "really awesome shot!", "score":5, "time": 123} 
        ]
@app.route('/')
@cross_origin()
def hello():
    # for i in data:
    #     i["generated"] = spell something 


    return data

if __name__ == '__main__':
    app.run()