__author__ = 'Neuroclick'

import os
import numpy as np
from datetime import datetime, timedelta 
from sklearn import linear_model
import json
import dataAnalysis

META_DATA = {}
#LABEL_DATA = []
PROCESSED_PATH = "../processed_data/"
ALL_USER_PROCESSED_PATH = "../all_user_processed_data/"
SURVEY_PROCESSED_PATH = "../expt_survey_data/"
NUM_SLIDES = 103


def load_meta_data():
    with open("meta_data.txt", "r") as fp:
        for line in fp:
            stimulus_index, time_dur, label  = line.strip().split("\t")
            META_DATA[stimulus_index] = [time_dur,label]
            #LABEL_DATA.append(int(label))

def get_feature_list_attn(attn_med_flag):
    print "DATA for ==============================================", attn_med_flag
    label_list = []
    feature_list = []
    with open(SURVEY_PROCESSED_PATH+"all_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"avg_att_med.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
        
    for user_id, data in all_users_slide_popularity.items():   
        print "USER ID: ", user_id
        for slide_no,popularity in sorted(data.items()):
            label_list.append(popularity)
            if attn_med_flag == "attn":
                feature_list.append(all_users_avg_att_med[user_id][slide_no][0])      
            elif attn_med_flag == "med":
                feature_list.append(all_users_avg_att_med[user_id][slide_no][1])      
        dataAnalysis.compute_correlation_coeff(feature_list,label_list)
        
               

if __name__ == "__main__":
    #load_meta_data()
    
    get_feature_list_attn("attn")
    
    get_feature_list_attn("med")
    #load_processed_data()