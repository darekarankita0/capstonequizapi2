from flask import Flask, jsonify, redirect, url_for
import json
import os
from flask import Flask, jsonify, redirect, url_for, render_template, send_from_directory


COUNT = 0

q1 = """1. _________ allows us to control electronic components
    a) RETful API
    b) RESTful API
    c) HTTP
    d) MQTT"""
q2 = """
    2. MQTT stands for _____________
    a) MQ Telemetry Things
    b) MQ Transport Telemetry
    c) MQ Transport Things
    d) MQ Telemetry Transport"""
q3 = """3. MQTT is better than HTTP for sending and receiving data.
    a) True
    b) False"""
q4 = """4. MQTT is _________ protocol.
    a) Machine to Machine
    b) Internet of Things
    c) Machine to Machine and Internet of Things
    d) Machine Things"""
q5 = """5. Which protocol is lightweight?
    a) MQTT
    b) HTTP
    c) CoAP
    d) SPI"""


class Questions:
    def __init__(self):
        self.score = 0
        self.ques = [q1, q2, q3, q4, q5]
        self.ans = ["a", "d", "a", "c", "a"]
        # self.ans_dict = {"q1": "a", "q2": "d", "q3": "a", "q4": "c", "q5": "a"}
        quiz_dict = {}
        for i in range(len(self.ques)-1):
            quiz_dict[self.ques[i]] = self.ans[i]
        self.quiz_dict = quiz_dict

    def check_answer(self, qno, ans):
        if ans == self.ans[qno]:
            self.score += 1
        else:
            self.score -= 1

    def return_result(self):
        result_json = json.dumps(self.score)
        result_json = {'1. _________ allows us to control electronic components\\n Correct Answer- RETful API\\n 2. MQTT stands for _____________\\n Correct Answer- MQ Telemetry Transport\\n 3. MQTT is better than HTTP for sending and receiving data.\\n Correct Answer- True\\n 4. MQTT is _________ protocol.\\n Correct Answer- Machine to Machine and Internet of Things\\n 5. Which protocol is lightweight?\\n Correct Answer- MQTT\\n score': result_json}
        return jsonify(result_json)


quiz_app = Questions()
app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'static/favicon.ico')  # , mimetype='image/vnd.microsoft.icon'


@app.route('/')
def home():
    global COUNT
    q = json.dumps(quiz_app.ques[COUNT])
    q = jsonify(q)
    return q


@app.route('/<ans>')
def answer(ans):
    global COUNT
    quiz_app.check_answer(qno=COUNT, ans=ans)
    COUNT += 1
    if COUNT < 5:
        return redirect(url_for('home'))
    else:
        COUNT = 0
        return redirect(url_for('result'))


@app.route('/result')
def result():
    result_json = quiz_app.return_result()
    return result_json


if __name__ == "__main__":
    app.run(debug=True)
