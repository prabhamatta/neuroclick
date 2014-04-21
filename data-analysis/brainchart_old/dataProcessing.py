__author__ = 'rahmanaicc'

import os
import numpy as np
import time
from sklearn import linear_model

fp= open("108_stata_data.txt", "w")


def getSlideTimeStamps():
    data = []
    with open("../../neuroclick-app/data/108/slide_timestamps.txt") as f:
        text = f.read()
        text = text.replace(', ',' ')
        text = text.replace('{', '')
        text = text.replace('}', '')

        # text = text.replace(',','\n')
        for t in text.split(','):
            index, ts = t.split('":"')
            ts = ts.replace('"','')
            index = index.replace('"','')
            data.append((ts.strip(),index.strip()))
    new_data = do_offset(data, '%b %d %Y %H:%M:%S',0,True)
    ret_val =[]
    for t ,index in new_data:
        ret_val.append(t)
    #print ret_val
    return ret_val

def generateFeatures():
    timed_user_data = getUserData()
    slide_times = getSlideTimeStamps()
    feature_set= []

    sum_delta = 0
    sum_alpha = 0
    sum_beta = 0
    sum_gamma = 0
    sum_theta = 0

    avg = 0

    for i in range(1, len(slide_times)-1):
        # duration_of_slide = slide_times[i+1] - slide_times[i]

        start_index_of_slide = 29

        s = start_index_of_slide
        for j in range(s,len(timed_user_data) - s):
            if(timed_user_data[j][0] > slide_times[i+1]):
                flag = False
                break
            else:
                start_index_of_slide +=1
                sum_delta += int(timed_user_data[j][1])
                sum_theta += int(timed_user_data[j][2])
                sum_alpha += ((int(timed_user_data[j][3]) + int(timed_user_data[j][4]))/2)
                sum_beta +=  ((int(timed_user_data[j][5]) + int(timed_user_data[j][6]))/2)
                sum_gamma += ((int(timed_user_data[j][7]) + int(timed_user_data[j][8]))/2)
        n_data = start_index_of_slide - s
        feature_set.append([sum_delta/n_data, sum_theta/n_data, sum_alpha/n_data, sum_beta/n_data, sum_gamma/n_data])
        fp.write("\t".join(str(s) for s in [sum_delta/n_data, sum_theta/n_data, sum_alpha/n_data, sum_beta/n_data, sum_gamma/n_data]))
        fp.write("\n")
        
    fp.close()
    return np.asmatrix(feature_set)
    # return np.array(feature_set)

def getUserData():
    user_data = []
    with open("../../neuroclick-app/data/108/all_data.txt") as f:
        for line in f:
            line_list = line.strip().split("\t")
            user_data.append(line_list)

    new_data = do_offset(user_data)
    #print new_data
    return new_data


def do_offset(tuples_list, format ='%b %d, %Y %H:%M:%S', offset_val=0,slides = False):
    new_tuples_list = []
    firstval = time.strptime(tuples_list[0][0], format)
    if not slides:
        def_time = 'Apr 01, 2000 00:00:00'
    else:
        def_time = 'Apr 01 2000 00:00:00'

    conversion_timer = time.mktime(time.strptime(def_time, format))

    for item in tuples_list:
        t= item[0]
        timer = time.strptime(t, format)  ##3,4,5
        timer = time.mktime(timer) - time.mktime(firstval) + conversion_timer + offset_val
        timer = time.strftime("%H:%M:%S",time.localtime(timer))
        if not slides:
            new_tuples_list.append((timer,item[1],item[2], item[3],item[4],item[5], item[6],item[7],item[8]))
        else:
            new_tuples_list.append((timer,item[1]))
    return new_tuples_list





def generateLabels():
    a =  [1,1,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,0,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,1]
    return np.transpose(np.asmatrix(a))


def computeCoefficient():
    #beta = inverse(X_t * X) * X_t * Y;
    X = generateFeatures()
    Y = generateLabels()
    X = X/np.linalg.norm(X)

    X_transpose = np.transpose(X)
    # beta = np.linalg.inv(X_transpose * X) * X_transpose * Y
    # print beta
    # print X_transpose
    t = X_transpose * Y
    # print t
    t1 = np.asmatrix(X_transpose) * np.asmatrix(X)
    beta = t1 * t
    print beta

def computeAverageMetrics():
    path = "../../neuroclick-app/data/"
    for dir_name, sub_dir_list, files in os.walk(path):
        print dir_name
        print "\n"
        for f in files:
            print f


def computeCoefficient_scikit():
    X = generateFeatures()
    Y = generateLabels()
    X = X/np.linalg.norm(X)
    clf = linear_model.LinearRegression()
    clf.fit(X,Y)
    print clf.coef_


if __name__ == "__main__":
    computeAverageMetrics()
    # computeCoefficient()
    #computeCoefficient_scikit()
    #generateFeatures()
