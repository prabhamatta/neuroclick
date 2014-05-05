from flask import Flask, Response, request, render_template, url_for, redirect, jsonify
import json
import math

app = Flask(__name__)
ALL_USER_PROCESSED_PATH = "../data-analysis/all_user_processed_data/"

@app.route("/", methods = ["GET", "POST"])
def login():
    return render_template('login.html')

@app.route("/start", methods=["GET", "POST"])
def start():
    return render_template('landing.html')


@app.route("/dash", methods=["GET","POST"])
def dashboard():
    return render_template('dash.html')

@app.route("/getAverageAttention", methods=['GET'])
def get_average_attention():
    metric1_data, metric2_data, stats = GetDataFromFiles("all_slides_avg_att", "all_slides_avg_med")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats)


@app.route("/getAverageAlpha", methods=['GET'])
def get_average_alpha():
    metric1_data, metric2_data, stats = GetDataFromFiles("all_slides_avg_low_alpha", "all_slides_avg_high_alpha")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats)

@app.route('/getStatsForUser', methods=['POST'])
def get_user_stats():
    user_id = request.form['userid']


@app.route('/wiki', methods=['POST','GET'])
def wik():
    return render_template('wikirecruitment.html')

def GetDataFromFiles(metric1,metric2):
    fp_metric1 = open(ALL_USER_PROCESSED_PATH + metric1 + ".json", "r")
    fp_metric2 = open(ALL_USER_PROCESSED_PATH + metric2 + ".json", "r")
    ret_json_metric1 = json.loads(fp_metric1.read())
    ret_json_metric2 = json.loads(fp_metric2.read())

    stats = {}
    stats['metric1'] = {'min':min(ret_json_metric1), 'max': max(ret_json_metric1), 'mean': round(sum(ret_json_metric1) / float(len(ret_json_metric1)),2)}
    stats['metric2'] = {'min':min(ret_json_metric2), 'max': max(ret_json_metric2), 'mean': round(sum(ret_json_metric2) / float(len(ret_json_metric2)),2)}

    return (ret_json_metric1, ret_json_metric2, stats)


if __name__ == "__main__":
    app.run()
