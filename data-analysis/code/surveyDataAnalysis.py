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


def get_survey_correlation_basic_stimulus_type(attn_med_flag ):
    print "AVERAGES STIMULUS DATA for ==============================================", attn_med_flag  
    all_29_29_feature_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
    all_29_29_label_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"avg_att_med.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    #print "user_id \t stimulus_type \t corr_val \t p_val \n"
    for user_id, data in all_users_slide_popularity.items(): 

        label_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        feature_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            #stimulus_tag = META_DATA[slide_no][2][:3]
            stimulus_tag =  META_DATA[slide_no][2][:3].upper() + "_" + META_DATA[slide_no][3].strip().upper()
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
            #print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+attn_med_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 
 

def get_survey_correlation_blink(attn_med_flag ):
    print " BLINK EFFECT DATA for ==============================================", attn_med_flag  
    all_29_29_feature_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
    all_29_29_label_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}       
        
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"blink_att_med.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    #print "user_id \t stimulus_type \t corr_val \t p_val \n"
    for user_id, data in all_users_slide_popularity.items(): 
        label_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        feature_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}        
     
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            #stimulus_tag = META_DATA[slide_no][2][:3]   
            stimulus_tag =  META_DATA[slide_no][2][:3].upper() + "_" + META_DATA[slide_no][3].strip().upper()
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
            #print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+attn_med_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 



def get_survey_correlation_basic_alpha_beta(alpha_beta_flag ):
    print " AVERAGES STIMULUS DATA for ==============================================", alpha_beta_flag   
    
    if alpha_beta_flag == "delta":
        val = 0
    elif alpha_beta_flag == "theta":
        val =1
    elif alpha_beta_flag == "low_alpha":
        val =2   
    elif alpha_beta_flag == "high_alpha":
        val =3       
    elif alpha_beta_flag == "low_beta":
        val =4    
    elif alpha_beta_flag == "high_beta":
        val =5    
    elif alpha_beta_flag == "low_gamma":
        val =6    
    elif alpha_beta_flag == "mid_gamma":
        val =7     


    all_29_29_feature_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
    all_29_29_label_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}       
        
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"avg_alpha_beta.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    #print "user_id \t stimulus_type \t corr_val \t p_val \n"
    for user_id, data in all_users_slide_popularity.items(): 
        label_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        feature_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}        
     
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            #stimulus_tag = META_DATA[slide_no][2][:3]   
            stimulus_tag =  META_DATA[slide_no][2][:3].upper() + "_" + META_DATA[slide_no][3].strip().upper()
            label_list[stimulus_tag].append(popularity)
            feature_val = all_users_avg_att_med[user_id][slide_no][val]                
            feature_list[stimulus_tag].append(feature_val)      
              
            all_29_29_feature_list[stimulus_tag].append(feature_val)                
            all_29_29_label_list[stimulus_tag].append(popularity)                          
        
        for sti_tag, feat_list in feature_list.items():
            corr = compute_correlation_coeff(feat_list,label_list[sti_tag])
            #print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+alpha_beta_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 

 


def get_survey_correlation_blink_alpha_beta(alpha_beta_flag ):
    print " BLINK EFFECT DATA for ==============================================", alpha_beta_flag   
    
    if alpha_beta_flag == "delta":
        val = 0
    elif alpha_beta_flag == "theta":
        val =1
    elif alpha_beta_flag == "low_alpha":
        val =2   
    elif alpha_beta_flag == "high_alpha":
        val =3       
    elif alpha_beta_flag == "low_beta":
        val =4    
    elif alpha_beta_flag == "high_beta":
        val =5    
    elif alpha_beta_flag == "low_gamma":
        val =6    
    elif alpha_beta_flag == "mid_gamma":
        val =7     


    all_29_29_feature_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
    all_29_29_label_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}       
        
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"blink_alpha_beta.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    #print "user_id \t stimulus_type \t corr_val \t p_val \n"
    for user_id, data in all_users_slide_popularity.items(): 
        label_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        feature_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}        
     
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            #stimulus_tag = META_DATA[slide_no][2][:3]   
            stimulus_tag =  META_DATA[slide_no][2][:3].upper() + "_" + META_DATA[slide_no][3].strip().upper()
            label_list[stimulus_tag].append(popularity)
            feature_val = all_users_avg_att_med[user_id][slide_no][val]                
            feature_list[stimulus_tag].append(feature_val)      
              
            all_29_29_feature_list[stimulus_tag].append(feature_val)                
            all_29_29_label_list[stimulus_tag].append(popularity)                          
        
        for sti_tag, feat_list in feature_list.items():
            corr = compute_correlation_coeff(feat_list,label_list[sti_tag])
            #print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+alpha_beta_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 

 

def get_survey_correlation_normalized_attn_med(attn_med_flag ):
    print "NORMALIZED STIMULUS DATA for ==============================================", attn_med_flag  
    all_29_29_feature_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
    all_29_29_label_list =  { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        
    with open(SURVEY_PROCESSED_PATH+"all_survey_users_slide_popularity.json", "r") as fp:
        all_users_slide_popularity= json.loads(fp.read())
    with open(ALL_USER_PROCESSED_PATH+"avg_att_med.json", "r") as fr:
        all_users_avg_att_med= json.loads(fr.read())    
    
    print "user_id \t stimulus_type \t corr_val \t p_val \n"
    count = 1
    for user_id, data in all_users_slide_popularity.items(): 

        print count
        count += 1
        label_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        feature_list = { 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[]}  
        for slide_no,popularity in sorted(data.items()):
            feature_val = ''
            #stimulus_tag = META_DATA[slide_no][2][:3]
            stimulus_tag =  META_DATA[slide_no][2][:3].upper() + "_" + META_DATA[slide_no][3].strip().upper()
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
            #print user_id +"\t" + sti_tag +"\t" + str(corr[0]) + "\t" + str(corr[1]) + "\n"
    print "Combined correlation of all 29 users and all 29 survey stimuli========"+attn_med_flag +" \n"    
    for all_sti_tag, all_feat_list in all_29_29_feature_list.items():         
        corr = compute_correlation_coeff(all_feat_list,all_29_29_label_list[all_sti_tag])
        print "Stimulus type: "+all_sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 


def compute_correlations_basic():

    get_survey_correlation_basic_stimulus_type("attn")
    get_survey_correlation_basic_stimulus_type("med")    
    get_survey_correlation_basic_alpha_beta('delta')
    get_survey_correlation_basic_alpha_beta('theta')
    get_survey_correlation_basic_alpha_beta('low_alpha')
    get_survey_correlation_basic_alpha_beta('high_alpha')
    get_survey_correlation_basic_alpha_beta('low_beta')
    get_survey_correlation_basic_alpha_beta('high_beta')
    get_survey_correlation_basic_alpha_beta('low_gamma')
    get_survey_correlation_basic_alpha_beta('mid_gamma') 


def compute_correlations_blink():
    get_survey_correlation_blink("attn")
    get_survey_correlation_blink("med") 
    
    get_survey_correlation_blink_alpha_beta("delta")
    get_survey_correlation_blink_alpha_beta("theta")
    get_survey_correlation_blink_alpha_beta("low_alpha")
    get_survey_correlation_blink_alpha_beta("high_alpha")
    get_survey_correlation_blink_alpha_beta("low_beta")
    get_survey_correlation_blink_alpha_beta("high_beta")
    get_survey_correlation_blink_alpha_beta("low_gamma")
    get_survey_correlation_blink_alpha_beta("mid_gamma")
                
if __name__ == "__main__":
    load_meta_data()
    compute_correlations_basic()
    #compute_correlations_blink()
    


    #load_processed_data()
    
    #get_feature_list_attn("alpha")
    