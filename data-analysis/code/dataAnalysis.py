__author__ = 'Neuroclick'

import os
import numpy as np
import time
from sklearn import linear_model
import datetime

META_DATA = {}
LABEL_DATA = []
PROCESSED_PATH = "../processed_data/"

def generate_user_avg_attn(user_slide_data,user_att_med):
    sum_att = 0
    for stimulus_id in range(1,len(user_slide_data)):
        start_time = user_slide_data[str(stimulus_id)]
        end_time = start_time + META_DATA[str(stimulus_id)][0]
        
        a = time.mktime(time.strptime("2000 "+ start_time, "%Y %H:%M:%S"))
        a = time.mktime(time.strftime("%H:%M:%S",start_time ))
        
        b = a + datetime.timedelta(0,25) # days, seconds, then other fields.
        print a.time()
        print b.time()        


        print "hello"
        
        
        
        
            
    

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


def generateLabels():
    return np.transpose(np.asmatrix(LABEL_DATA))


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


 
def computeCoefficient_scikit():
    X = generateFeatures()
    Y = generateLabels()
    X = X/np.linalg.norm(X)
    clf = linear_model.LinearRegression()
    clf.fit(X,Y)
    print clf.coef_
    
    
def get_user_slidetimestamp(user_id):
    slide_data = {}
    with open(PROCESSED_PATH+user_id+"/slide_timestamps.txt", "r") as fp:
        for line in fp:
            stimulus_idx,ts = line.strip().split("\t")
            slide_data[stimulus_idx] = ts            
    return slide_data
            
def get_user_att_med(user_id):
    att_med_data = {}
    with open(PROCESSED_PATH+user_id+"/att_med.txt", "r") as fp:
        for line in fp:
            line_list=  line.strip().split("\t")
            att_med_data[line_list[0]] = line_list[1:-1]          
    return att_med_data
            


def loadProcessedData():
    all_slide_data = {}
    all_data = {}
    att_med  = {}
    spectrum_data = {}
    for dir_name, sub_dir_list, files in os.walk(PROCESSED_PATH):
        #print dir_name, sub_dir_list
        if dir_name[-3:][0].isdigit():
            user_id =  dir_name[-3:]
            user_slide_data  = get_user_slidetimestamp(user_id)
            user_att_med = get_user_att_med(user_id)
            all_slide_data[user_id] = user_slide_data
            
            generate_user_avg_attn(user_slide_data,user_att_med )
            
            
 
def loadMetaData():
    with open("meta_data.txt", "r") as fp:
        for line in fp:
            stimulus_index, time_dur, label  = line.strip().split("\t")
            META_DATA[stimulus_index] = [time_dur,label]
            LABEL_DATA.append(int(label))
            


if __name__ == "__main__":
    loadMetaData()
    loadProcessedData()
    # computeCoefficient()
    #computeCoefficient_scikit()
    #generateFeatures()
