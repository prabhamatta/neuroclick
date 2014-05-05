__author__ = 'Neuroclick'

import os
import numpy as np
from datetime import datetime, timedelta 
from sklearn import linear_model
import json
#import dataAnalysis
import matplotlib.pyplot as plt
import pylab
import scipy
from scipy.stats.stats import pearsonr

META_DATA = {}
ALL_USER_PROCESSED_PATH = "../all_user_processed_data/"
SURVEY_PROCESSED_PATH = "../expt_survey_data/"
NUM_SLIDES = 103



def load_meta_data():
    with open("meta_data.txt", "r") as fp:
        for line in fp:
            stimulus_index, time_dur, label, stimulus_type, long_short  = line.strip().split("\t")
            META_DATA[stimulus_index] = [time_dur, label, stimulus_type, long_short]
            #LABEL_DATA.append(int(label))


def compute_correlation_coeff(feature_list,LABEL_DATA ):
    X = feature_list
    Y = LABEL_DATA
    
    #print scipy.corrcoef(X,Y)
    corr = pearsonr(X,Y)
    
    #plt.scatter(X,Y)
    #plt.show()
    return corr



def get_correlation_basic(attn_med_flag ):
    print "DATA for ==============================================", attn_med_flag  
    all_29_29_feature_list =  {'pic':[], 'vid':[]}  
    all_29_29_label_list =  {'pic':[], 'vid':[]}  
    
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"avg_att_med.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    print "user_id \t stimulus_type \t corr_val \t p_val \n"
    
    for user_id, data in all_users_slide_popularity.items(): 
        label_list = {'pic':[], 'vid':[]}    
        feature_list = {'pic':[], 'vid':[]}      
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            stimulus_tag = META_DATA[slide_no][2][:3]            
            label_list[stimulus_tag].append(popularity)
            if attn_med_flag == "attn":
                feature_val = all_users_avg_att_med[user_id][slide_no][0]                
                feature_list[stimulus_tag].append(feature_val)      
            elif attn_med_flag == "med":
                feature_val = all_users_avg_att_med[user_id][slide_no][1]                
                feature_list[stimulus_tag].append(feature_val) 
                
            all_29_29_feature_list[stimulus_tag].append(feature_val)
            all_29_29_label_list[stimulus_tag].append(popularity)
            
        for sti_tag, feat_list in feature_list.items():
            corr = compute_correlation_coeff(feat_list,label_list[sti_tag])
            print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+attn_med_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n"        

               
def get_correlation_normalized(attn_med_flag ):
    print "DATA for ==============================================", attn_med_flag  
    all_29_29_feature_list =  {'pic':[], 'vid':[]}  
    all_29_29_label_list =  {'pic':[], 'vid':[]}  
    
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"avg_att_med.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    print "user_id \t stimulus_type \t corr_val \t p_val \n"
    
    for user_id, data in all_users_slide_popularity.items(): 
        label_list = {'pic':[], 'vid':[]}    
        feature_list = {'pic':[], 'vid':[]}      
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            stimulus_tag = META_DATA[slide_no][2][:3]            
            label_list[stimulus_tag].append(popularity)
            if attn_med_flag == "attn":
                feature_val = all_users_avg_att_med[user_id][slide_no][0]                
                feature_list[stimulus_tag].append(feature_val)      
            elif attn_med_flag == "med":
                feature_val = all_users_avg_att_med[user_id][slide_no][1]                
                feature_list[stimulus_tag].append(feature_val) 
                
            all_29_29_feature_list[stimulus_tag].append(feature_val)
            all_29_29_label_list[stimulus_tag].append(popularity)
            
        for sti_tag, feat_list in feature_list.items():
            corr = compute_correlation_coeff(feat_list,label_list[sti_tag])
            print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+attn_med_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n"        
               
               
if __name__ == "__main__":
    load_meta_data()
    get_correlation_basic("attn")
    get_correlation_basic("med")
    
    get_correlation_normalized("attn")
    
    #load_processed_data()
    
    #get_feature_list_attn("alpha")
    