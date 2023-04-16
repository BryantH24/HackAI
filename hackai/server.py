from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
import json
import random
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


data = [
        {"msg": "Jump Ball Powell vs Zeller (Bullock gains possession)", "score":6, "time": "4:01:12"}, 
        {"msg": "[DAL 2-0] Powell Alley Oop Layup shot: Made (2 PTS) Assist: Doncic (1 AST)", "score":5, "time": "4:01:57"}, 
        {"msg": "[DAL] Dinwiddie Driving Floating Jump Shot: Missed", "score":2, "time": "4:02:01"}, 
        # {"msg": "[DAL] Irving Alley Oop to Doncic Dunk", "score":9, "time": "4:02:15"}, 
        ]


sponsors = ["Chime", "Dr Pepper", "Kroger", "American Airlines", "UT SouthWestern"]
@app.route('/')
@cross_origin()
def hello():
    
    # for i in data:
    #     i["generated"] = spell something 
    for i in range(len(data)): 
        response = requests.post(
        "https://api.respell.ai/v1/run",
        headers={
            # This is your API key
            'Authorization': 'Bearer 40ff75bc-45f5-4865-9da1-0727e2e1d5db',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            "spellId": "liRHBStHlmLcSuwC9hExX",
            # This field can be omitted to run the latest published version
            "spellVersionId": 'jIjPL_4_fHZ4KjIC1ZOWK',
            # Fill in dynamic values for each of your 2 input blocks
            "inputs": {
            "text_input_2": "Create a tweet based off of this recent play data:" + data[i]['msg'] + ". Include the sponsor company: " + random.choice(sponsors),
            "prompt": "Instruction: You are an AI tasked with writing a tweet for a basketball team's twitter account based on text describing a recent play. You will receive instructions to create a tweet based off a string containing play data, and a sponsor company which you should add into the message. The team you are writing tweets for is the Dallas Mavericks, and so the tweets should have positive sentiment towards the Dallas Mavericks",
            }
        }),
        )

        # print(response.json())
        data[i]["generated"] = response.json()['outputs']['text_output']
    print("responded")
    return data

if __name__ == '__main__':
    app.run(debug=True)
    







