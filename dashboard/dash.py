import flask
from flask import Flask, Response, request, render_template, url_for, redirect, jsonify
import json
import math
import os




app = Flask(__name__)
ALL_USER_PROCESSED_PATH = "../data-analysis/all_user_processed_data/"
PROCESSED_PATH = "../data-analysis/processed_data/"


@app.route("/", methods = ["GET", "POST"])
def dash():
    return render_template('landing.html')

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template('login.html')

@app.route("/start", methods=["GET", "POST"])
def start():
    return render_template('landing.html')


@app.route("/neuroclick_analytics", methods=["GET","POST"])
def dashboard():
    return render_template('neuroclick_analytics.html')

@app.route("/getAverageAttention", methods=['GET'])
def get_average_attention():
    metric1_data, metric2_data, stats, average = GetDataFromFiles("all_slides_avg_att", "all_slides_avg_med")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average = average)




def GetMetaData_video():
    meta_data = {}
    with open('/Users/rahmanaicc/Workspace/Dropbox/BrainDrain/Codebase/neuroclick/data-analysis/code/meta_data.txt') as meta:
        for line in meta:
            tokens = line.strip().split('\t')
            if int(tokens[0]) > 68:
                meta_data[int(tokens[0])] = tokens[4]
            else:
                continue
    return meta_data

def GetMetaData_text():
    meta_data = {}
    with open('/Users/rahmanaicc/Workspace/Dropbox/BrainDrain/Codebase/neuroclick/data-analysis/code/meta_data.txt') as meta:
        for line in meta:
            tokens = line.strip().split('\t')
            if int(tokens[0]) < 44:
                meta_data[int(tokens[0])] = tokens[4]
            else:
                continue
    return meta_data

@app.route("/getTextStats", methods=['GET'])
def get_test_stats():
    meta_data = GetMetaData_text()
    metric1_data, metric2_data, stats,average = GetDataFromFiles_text("all_slides_avg_low_alpha", "all_slides_avg_high_alpha", meta_data)

    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)

#
# @app.route("/getTextVidStats", methods=['GET'])
# def get_text_video_stats():
#     meta_data_text = GetMetaData_text()
#     meta_data_video = GetMetaData_video()
#     metric1_text_data, metric2_text_data, stats_text,average_text = GetDataFromFiles_text("all_slides_avg_low_alpha", "all_slides_avg_high_alpha", meta_data)
#     metric1_video_data, metric2_video_data, stats_video,average_video = GetDataFromFiles_video("all_slides_avg_low_alpha", "all_slides_avg_high_alpha", meta_data)
#     [stats_text['short']['mean'],stats_video['short']['mean']]
#     return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)


@app.route("/getVideoStats", methods=['GET'])
def get_video_stats():
    meta_data = GetMetaData_video()
    metric1_data, metric2_data, stats,average = GetDataFromFiles_video("all_slides_avg_low_beta", "all_slides_avg_high_beta", meta_data)
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)


def GetDataFromFiles_text(metric1,metric2,meta_data, gender=False):
    fp_metric1 = open(ALL_USER_PROCESSED_PATH + metric1 + ".json", "r")
    fp_metric2 = open(ALL_USER_PROCESSED_PATH + metric2 + ".json", "r")
    ret_json_metric1 = json.loads(fp_metric1.read())
    ret_json_metric2 = json.loads(fp_metric2.read())

    avg_metric = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1,ret_json_metric2)]
    long_sum = 0
    short_sum = 0
    i = 1
    for metric in avg_metric:
        if i < 44:
            if meta_data[i] == 'Long':
                long_sum += metric
                i +=1
            else:
                short_sum += metric
                i +=1

    long_count =  meta_data.values().count('Long')
    short_count = meta_data.values().count('Short')

    stats = {}
    if not gender:
        stats['short'] = {'mean': round((short_sum/short_count),2)}
        stats['long'] = {'mean': round((long_sum/long_count),2)}
    return (ret_json_metric1, ret_json_metric2, stats,avg_metric)



def GetDataFromFiles_video(metric1,metric2,meta_data, gender=False):
    fp_metric1 = open(ALL_USER_PROCESSED_PATH + metric1 + ".json", "r")
    fp_metric2 = open(ALL_USER_PROCESSED_PATH + metric2 + ".json", "r")
    ret_json_metric1 = json.loads(fp_metric1.read())
    ret_json_metric2 = json.loads(fp_metric2.read())

    avg_metric = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1,ret_json_metric2)]
    long_sum = 0
    short_sum = 0
    i = 1
    for metric in avg_metric:
        if i > 68:
            if meta_data[i] == 'Long':
                long_sum += metric
                i +=1
            else:
                short_sum += metric
                i +=1
        else:
            i+=1

    long_count =  meta_data.values().count('Long')
    short_count = meta_data.values().count('Short')

    stats = {}
    if not gender:
        stats['short'] = {'mean': round((short_sum/short_count),2)}
        stats['long'] = {'mean': round((long_sum/long_count),2)}
    return (ret_json_metric1, ret_json_metric2, stats,avg_metric)



@app.route("/getAverageAlpha1", methods=['GET'])
def get_average_alpha():
    metric1_data, metric2_data, stats,average = GetDataFromFiles("all_slides_avg_low_alpha", "all_slides_avg_high_alpha")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average =average )


@app.route("/getAverageBeta1", methods=['GET'])
def get_average_beta():
    # meta_data = GetMetaData()
    metric1_data, metric2_data, stats,average = GetDataFromFiles("all_slides_avg_low_beta", "all_slides_avg_high_beta")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)



@app.route("/getAverageGamma1", methods=['GET'])
def get_average_gamma():
    metric1_data, metric2_data, stats,average = GetDataFromFiles("all_slides_avg_low_gamma", "all_slides_avg_mid_gamma")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)



@app.route("/getAverageAlpha", methods=['GET'])
def get_average_alpha_blink():
    metric1_data, metric2_data, stats,average = GetDataFromFiles("all_slides_blink_low_alpha", "all_slides_blink_high_alpha")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average =average )


@app.route("/getAverageBeta", methods=['GET'])
def get_average_beta_blink():
    # meta_data = GetMetaData()
    metric1_data, metric2_data, stats,average = GetDataFromFiles("all_slides_blink_low_beta", "all_slides_blink_high_beta")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)



@app.route("/getAverageGamma", methods=['GET'])
def get_average_gamma_blink():
    metric1_data, metric2_data, stats,average = GetDataFromFiles("all_slides_blink_low_gamma", "all_slides_blink_mid_gamma")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats,average=average)







@app.route('/getStatsForUser', methods=['POST'])
def get_user_stats():
    user_id = request.form['userid']


@app.route('/survey_results', methods=['POST','GET'])
def surveyResults():
    return render_template('survey_results.html')

def GetDataFromFiles_attn_med(metric1,metric2,gender=False):
    fp_metric1 = open(ALL_USER_PROCESSED_PATH + metric1 + ".json", "r")
    fp_metric2 = open(ALL_USER_PROCESSED_PATH + metric2 + ".json", "r")
    ret_json_metric1 = json.loads(fp_metric1.read())
    ret_json_metric2 = json.loads(fp_metric2.read())

    # avg_metric = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1,ret_json_metric2)]


    stats = {}
    if not gender:
        stats['metric1'] = {'min':min(ret_json_metric1), 'max': max(ret_json_metric1), 'mean': round(sum(ret_json_metric1) / float(len(ret_json_metric1)),2)}
        stats['metric2'] = {'min':min(ret_json_metric2), 'max': max(ret_json_metric2), 'mean': round(sum(ret_json_metric2) / float(len(ret_json_metric2)),2)}

    return (ret_json_metric1, ret_json_metric2, stats)


def GetDataFromFiles(metric1,metric2,gender=False):
    fp_metric1 = open(ALL_USER_PROCESSED_PATH + metric1 + ".json", "r")
    fp_metric2 = open(ALL_USER_PROCESSED_PATH + metric2 + ".json", "r")
    ret_json_metric1 = json.loads(fp_metric1.read())
    ret_json_metric2 = json.loads(fp_metric2.read())

    avg_metric = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1,ret_json_metric2)]


    stats = {}
    if not gender:
        stats['metric1'] = {'min':min(ret_json_metric1), 'max': max(ret_json_metric1), 'mean': round(sum(ret_json_metric1) / float(len(ret_json_metric1)),2)}
        stats['metric2'] = {'min':min(ret_json_metric2), 'max': max(ret_json_metric2), 'mean': round(sum(ret_json_metric2) / float(len(ret_json_metric2)),2)}

    return (ret_json_metric1, ret_json_metric2, stats,avg_metric)



@app.route('/getBlinkData')
def get_blink_data():
    metric1_data, metric2_data, stats = GetDataFromFiles("all_slides_blink_att", "all_slides_blink_med")
    return jsonify(metric1= metric1_data, metric2 = metric2_data, stats = stats)


@app.route('/home')
def home():
    return render_template('landing.html')


@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/getGenderBeta')
def get_gender_beta():
    avg_male, avg_female = GetDataFromFiles_gender("gender_all_slides_avg_high_beta", "gender_all_slides_avg_low_beta", "beta")
    return jsonify(metric1= avg_male, metric2 = avg_female)


@app.route('/getGenderAlpha')
def get_gender_alpha():
    avg_male, avg_female = GetDataFromFiles_gender("gender_all_slides_avg_high_alpha", "gender_all_slides_avg_low_alpha", "alpha")
    return jsonify(metric1= avg_male, metric2 = avg_female)


@app.route('/getGenderGamma')
def get_gender_gamma():
    avg_male, avg_female = GetDataFromFiles_gender("gender_all_slides_mid_gamma", "gender_all_slides_low_gamma", "gamma")
    return jsonify(metric1= avg_male, metric2 = avg_female)



def GetDataFromFiles_gender(metric1,metric2,met):
    fp_metric1 = open(ALL_USER_PROCESSED_PATH + metric1 + ".json", "r")
    fp_metric2 = open(ALL_USER_PROCESSED_PATH + metric2 + ".json", "r")
    ret_json_metric1 = json.loads(fp_metric1.read())
    ret_json_metric2 = json.loads(fp_metric2.read())

    avg_male = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1['M'],ret_json_metric2['M'])]
    avg_female = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1['F'],ret_json_metric2['F'])]

    # avg_metric = [(float(x)+float(y))/2 for x,y in zip(ret_json_metric1,ret_json_metric2)]

    print met
    print "male " + str(float(sum(avg_male))/ len(avg_male))
    print "female " + str(float(sum(avg_female))/ len(avg_female))
    print "====================================================="
    return (avg_male,avg_female)

#
#
# @app.route('/experimentdata')
# def experiment_data_users():
#     count = 0
#     []
#     for dir_name, sub_dir_list, files in os.walk(PROCESSED_PATH):


if __name__ == "__main__":
    app.run(debug=True)

