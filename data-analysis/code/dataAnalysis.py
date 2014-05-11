__author__ = 'Neuroclick'

import os
import numpy as np
from datetime import datetime, timedelta 
from sklearn import linear_model
import json
import matplotlib.pyplot as plt
import pylab
import scipy
from scipy.stats.stats import pearsonr

META_DATA = {}
LABEL_DATA = []
PROCESSED_PATH = "../processed_data/"
ALL_USER_PROCESSED_PATH = "../all_user_processed_data/"

#BLINK_TIME = {
    #'BLINK_START_TEX_SHORT': 1,
    #'BLINK_END_TEX_SHORT' : 5,
    #'BLINK_START_TEX_LONG' : 3,
    #'BLINK_END_TEX_LONG' : 12,
    #'BLINK_START_PIC_PIC' : 2,
    #'BLINK_END_PIC_PIC' : 4,
    #'BLINK_START_VID_SHORT' :2,
    #'BLINK_END_VID_SHORT' : 5,
    #'BLINK_START_VID_LONG' : 15,
    #'BLINK_END_VID_LONG' : 35,
    #'BLINK_START_BAS_BASELINE':2,
    #'BLINK_END_BAS_BASELINE' : 6,
#}


#BLINK_TIME = {
    #'BLINK_START_TEX_SHORT': 1,
    #'BLINK_END_TEX_SHORT' : 5,
    #'BLINK_START_TEX_LONG' : 1,
    #'BLINK_END_TEX_LONG' : 5,
    #'BLINK_START_PIC_PIC' : 1,
    #'BLINK_END_PIC_PIC' : 5,
    #'BLINK_START_VID_SHORT' :1,
    #'BLINK_END_VID_SHORT' : 5,
    #'BLINK_START_VID_LONG' : 1,
    #'BLINK_END_VID_LONG' : 5,
    #'BLINK_START_BAS_BASELINE':1,
    #'BLINK_END_BAS_BASELINE' : 5,
#}


BLINK_TIME = {
    'BLINK_START_TEX_SHORT': 1,
    'BLINK_END_TEX_SHORT' : 3,
    'BLINK_START_TEX_LONG' : 1,
    'BLINK_END_TEX_LONG' : 3,
    'BLINK_START_PIC_PIC' : 1,
    'BLINK_END_PIC_PIC' : 3,
    'BLINK_START_VID_SHORT' :1,
    'BLINK_END_VID_SHORT' : 3,
    'BLINK_START_VID_LONG' : 1,
    'BLINK_END_VID_LONG' : 3,
    'BLINK_START_BAS_BASELINE':1,
    'BLINK_END_BAS_BASELINE' : 3,
}





def generate_user_avg_attn(user_slide_data,user_att_med):
    sum_att = 0
    user_attn_med_avg = {}
    for stimulus_id in range(1,len(user_slide_data)):         
        start_time = user_slide_data[str(stimulus_id)]
        delta_time = META_DATA[str(stimulus_id)][0]
        
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time =start_time + timedelta(seconds=int(delta_time))
        #print end_time.strftime("%H:%M:%S")
        sum_att = 0
        sum_med = 0
        #cnt = 1
        for time_attn_med in user_att_med:
            t = datetime.strptime(time_attn_med[0], "%H:%M:%S")
            if t>=start_time and t<=end_time:
                #cnt +=1
                
                sum_att += int(time_attn_med[1])
                sum_med += int(time_attn_med[2])
            elif t>end_time:
                #print t
                break
        
        user_avg_attn =float(sum_att)/(int(delta_time)+1)
        user_avg_med =float(sum_med)/(int(delta_time)+1)
        user_attn_med_avg[stimulus_id] = [round(user_avg_attn,3), round(user_avg_med,3)]
        
    return user_attn_med_avg
                
        
    
def generate_user_avg_alpha_beta(user_slide_data,user_alpha_beta):
    sum_att = 0
    user_alpha_beta_avg = {}
    for stimulus_id in range(1,len(user_slide_data)):         
        start_time = user_slide_data[str(stimulus_id)]
        delta_time = META_DATA[str(stimulus_id)][0]
        
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time =start_time + timedelta(seconds=int(delta_time))
        #print end_time.strftime("%H:%M:%S")
        sum_delta = 0
        sum_theta = 0
        sum_low_alpha = 0
        sum_high_alpha = 0
        sum_low_beta = 0
        sum_high_beta = 0
        sum_low_gamma = 0
        sum_mid_gamma = 0
        
        #cnt = 1
        for time_alpha_beta in user_alpha_beta:
            t = datetime.strptime(time_alpha_beta[0], "%H:%M:%S")
            if t>=start_time and t<=end_time:
                #cnt +=1
                
                sum_delta += int(time_alpha_beta[1])
                sum_theta += int(time_alpha_beta[2])
                sum_low_alpha += int(time_alpha_beta[3])
                sum_high_alpha += int(time_alpha_beta[4])
                sum_low_beta += int(time_alpha_beta[5])
                sum_high_beta += int(time_alpha_beta[6])
                sum_low_gamma += int(time_alpha_beta[7])
                sum_mid_gamma += int(time_alpha_beta[8])
                
            elif t>end_time:
                #print t
                break
        
        user_avg_delta =float(sum_delta)/(int(delta_time)+1)
        user_avg_theta =float(sum_theta)/(int(delta_time)+1)  
        user_avg_low_alpha =float(sum_low_alpha)/(int(delta_time)+1)
        user_avg_high_alpha =float(sum_high_alpha)/(int(delta_time)+1)
        user_avg_low_beta =float(sum_low_beta)/(int(delta_time)+1)
        user_avg_high_beta =float(sum_high_beta)/(int(delta_time)+1)        
        user_avg_low_gamma =float(sum_low_gamma)/(int(delta_time)+1)
        user_avg_mid_gamma =float(sum_mid_gamma)/(int(delta_time)+1)                        
        
        user_alpha_beta_avg[stimulus_id] = [round(user_avg_delta,3), round(user_avg_theta,3), round(user_avg_low_alpha,3), round(user_avg_high_alpha,3), round(user_avg_low_beta,3), round(user_avg_high_beta,3), round(user_avg_low_gamma,3), round(user_avg_mid_gamma,3)]
        
    return user_alpha_beta_avg

    
def generate_user_norm_alpha_beta(user_slide_data,user_alpha_beta):
    sum_att = 0
    user_alpha_beta_avg = {}
    for stimulus_id in range(1,len(user_slide_data)):         
        start_time = user_slide_data[str(stimulus_id)]
        delta_time = META_DATA[str(stimulus_id)][0]
        
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time =start_time + timedelta(seconds=int(delta_time))
        #print end_time.strftime("%H:%M:%S")
        sum_delta = 0
        sum_theta = 0
        sum_low_alpha = 0
        sum_high_alpha = 0
        sum_low_beta = 0
        sum_high_beta = 0
        sum_low_gamma = 0
        sum_mid_gamma = 0
        
        #cnt = 1
        for time_alpha_beta in user_alpha_beta:
            t = datetime.strptime(time_alpha_beta[0], "%H:%M:%S")
            if t>=start_time and t<=end_time:
                #cnt +=1
                
                sum_delta += float(time_alpha_beta[1])
                sum_theta += float(time_alpha_beta[2])
                sum_low_alpha += float(time_alpha_beta[3])
                sum_high_alpha += float(time_alpha_beta[4])
                sum_low_beta += float(time_alpha_beta[5])
                sum_high_beta += float(time_alpha_beta[6])
                sum_low_gamma += float(time_alpha_beta[7])
                sum_mid_gamma += float(time_alpha_beta[8])
                
            elif t>end_time:
                #print t
                break
        
        user_avg_delta =float(sum_delta)/(int(delta_time)+1)
        user_avg_theta =float(sum_theta)/(int(delta_time)+1)  
        user_avg_low_alpha =float(sum_low_alpha)/(int(delta_time)+1)
        user_avg_high_alpha =float(sum_high_alpha)/(int(delta_time)+1)
        user_avg_low_beta =float(sum_low_beta)/(int(delta_time)+1)
        user_avg_high_beta =float(sum_high_beta)/(int(delta_time)+1)        
        user_avg_low_gamma =float(sum_low_gamma)/(int(delta_time)+1)
        user_avg_mid_gamma =float(sum_mid_gamma)/(int(delta_time)+1)                        
        
        user_alpha_beta_avg[stimulus_id] = [round(user_avg_delta,3), round(user_avg_theta,3), round(user_avg_low_alpha,3), round(user_avg_high_alpha,3), round(user_avg_low_beta,3), round(user_avg_high_beta,3), round(user_avg_low_gamma,3), round(user_avg_mid_gamma,3)]
        
    return user_alpha_beta_avg

 
def compute_correlation_coeff(feature_list):
    X = feature_list
    Y = LABEL_DATA
    
    #print scipy.corrcoef(X,Y)
    print "No. of feature values===", len(feature_list)
    print pearsonr(X,Y)
    
    plt.scatter(X,Y)
    plt.ylabel("Popular/Non Popular")
    plt.xlabel("Frequency")
    
    plt.show()
    print "*****************************"
    
def compute_correlation_coeff_feat_label(feature_list,label_data ):
    X = feature_list
    Y = label_data
    
    #print scipy.corrcoef(X,Y)
    corr = pearsonr(X,Y)
    
    #plt.scatter(X,Y)
    #plt.show()
    return corr

    
def get_user_slidetimestamp(user_id):
    slide_data = {}
    with open(PROCESSED_PATH+user_id+"/slide_timestamps.txt", "r") as fp:
        for line in fp:
            stimulus_idx,ts = line.strip().split("\t")
            slide_data[stimulus_idx] = ts            
    return slide_data


def get_user_att_med(user_id):
    att_med_data = []
    with open(PROCESSED_PATH+user_id+"/att_med.txt", "r") as fp:
        for line in fp:
            line_list=  line.strip().split("\t")
            att_med_data.append(line_list)          
    return att_med_data
            


def load_processed_data():
    all_slide_data = {}
    all_users_att_med  = {}  
    all_users_alpha_beta  = {}   
    norm_all_users_alpha_beta = {}
    
    for dir_name, sub_dir_list, files in os.walk(PROCESSED_PATH):
        print dir_name, sub_dir_list
        if dir_name[-3:][0].isdigit():
            user_id =  dir_name[-3:]
            user_slide_data  = get_user_slidetimestamp(user_id)
            all_slide_data[user_id] = user_slide_data
           
            #loading attn and med data  
            user_att_med = get_user_att_med(user_id)
            all_users_att_med[user_id] = user_att_med
            user_attn_med_avg = generate_user_avg_attn(user_slide_data, user_att_med)
            with open(PROCESSED_PATH+user_id+"/avg_att_med.json", "w") as fp:
                fp.write(json.dumps(user_attn_med_avg))
            all_users_att_med[user_id] = user_attn_med_avg
            
            #loading alpha, beta,...
            user_alpha_beta_data,normalized_alpha_beta_data  = get_user_alpha_beta(user_id)
            
            all_users_alpha_beta[user_id] = user_alpha_beta_data
            user_alpha_beta_avg = generate_user_avg_alpha_beta(user_slide_data, user_alpha_beta_data)
            with open(PROCESSED_PATH+user_id+"/avg_alpha_beta.json", "w") as fp:
                fp.write(json.dumps(user_alpha_beta_avg))
            all_users_alpha_beta[user_id] = user_alpha_beta_avg
            
            norm_all_users_alpha_beta[user_id] = normalized_alpha_beta_data
            norm_user_alpha_beta_avg = generate_user_norm_alpha_beta(user_slide_data, normalized_alpha_beta_data)
            with open(PROCESSED_PATH+user_id+"/norm_avg_alpha_beta.json", "w") as fp:
                fp.write(json.dumps(norm_user_alpha_beta_avg))
            norm_all_users_alpha_beta[user_id] = norm_user_alpha_beta_avg            
                        
 
    with open(ALL_USER_PROCESSED_PATH+"/avg_att_med.json", "w") as fp: 
        fp.write(json.dumps(all_users_att_med))                     
            
    with open(ALL_USER_PROCESSED_PATH+"/avg_alpha_beta.json", "w") as fp: 
        fp.write(json.dumps(all_users_alpha_beta))    

    with open(ALL_USER_PROCESSED_PATH+"/norm_avg_alpha_beta.json", "w") as fp: 
        fp.write(json.dumps(norm_all_users_alpha_beta))


def generate_user_blink_attn(user_slide_data,user_att_med):
    sum_att = 0
    user_attn_med_blink = {}
    for stimulus_id in range(1,len(user_slide_data)): 
        stimulus_id = str(stimulus_id)        
        stimulus_type =  META_DATA[stimulus_id][2][:3].upper() + "_" + META_DATA[stimulus_id][3].strip().upper()
        
       
        start_time = datetime.strptime(user_slide_data[stimulus_id], "%H:%M:%S")  + timedelta(seconds=int(BLINK_TIME["BLINK_START_"+stimulus_type] -1))
                    
        delta_time =  BLINK_TIME["BLINK_END_"+stimulus_type] - BLINK_TIME["BLINK_START_"+stimulus_type] + 1
    
        #start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time =start_time + timedelta(seconds=int(delta_time))
        #print end_time.strftime("%H:%M:%S")
        sum_att = 0
        sum_med = 0
        #cnt = 1
        #print stimulus_id, start_time, end_time
        for time_attn_med in user_att_med:
            t = datetime.strptime(time_attn_med[0], "%H:%M:%S")
            if t>=start_time and t<=end_time:
                #cnt +=1
                
                sum_att += int(time_attn_med[1])
                sum_med += int(time_attn_med[2])
            elif t>end_time:
                #print t
                break
        
        user_blink_attn =float(sum_att)/(int(delta_time)+1)
        user_blink_med =float(sum_med)/(int(delta_time)+1)
        user_attn_med_blink[stimulus_id] = [round(user_blink_attn,3), round(user_blink_med,3)]
        
    return user_attn_med_blink
                
    
def generate_user_blink_alpha_beta(user_slide_data,user_alpha_beta):
    sum_att = 0
    user_alpha_beta_avg = {}
    for stimulus_id in range(1,len(user_slide_data)):  
        stimulus_id = str(stimulus_id)        
        stimulus_type =  META_DATA[stimulus_id][2][:3].upper() + "_" + META_DATA[stimulus_id][3].strip().upper()
        
       
        start_time = datetime.strptime(user_slide_data[stimulus_id], "%H:%M:%S")  + timedelta(seconds=int(BLINK_TIME["BLINK_START_"+stimulus_type] -1))
                    
        delta_time =  BLINK_TIME["BLINK_END_"+stimulus_type] - BLINK_TIME["BLINK_START_"+stimulus_type] + 1
    
        #start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time =start_time + timedelta(seconds=int(delta_time))        

        
        #print end_time.strftime("%H:%M:%S")
        sum_delta = 0
        sum_theta = 0
        sum_low_alpha = 0
        sum_high_alpha = 0
        sum_low_beta = 0
        sum_high_beta = 0
        sum_low_gamma = 0
        sum_mid_gamma = 0
        
        #cnt = 1
        for time_alpha_beta in user_alpha_beta:
            t = datetime.strptime(time_alpha_beta[0], "%H:%M:%S")
            if t>=start_time and t<=end_time:
                #cnt +=1
                
                sum_delta += int(time_alpha_beta[1])
                sum_theta += int(time_alpha_beta[2])
                sum_low_alpha += int(time_alpha_beta[3])
                sum_high_alpha += int(time_alpha_beta[4])
                sum_low_beta += int(time_alpha_beta[5])
                sum_high_beta += int(time_alpha_beta[6])
                sum_low_gamma += int(time_alpha_beta[7])
                sum_mid_gamma += int(time_alpha_beta[8])
                
            elif t>end_time:
                #print t
                break
        
        user_avg_delta =float(sum_delta)/(int(delta_time)+1)
        user_avg_theta =float(sum_theta)/(int(delta_time)+1)  
        user_avg_low_alpha =float(sum_low_alpha)/(int(delta_time)+1)
        user_avg_high_alpha =float(sum_high_alpha)/(int(delta_time)+1)
        user_avg_low_beta =float(sum_low_beta)/(int(delta_time)+1)
        user_avg_high_beta =float(sum_high_beta)/(int(delta_time)+1)        
        user_avg_low_gamma =float(sum_low_gamma)/(int(delta_time)+1)
        user_avg_mid_gamma =float(sum_mid_gamma)/(int(delta_time)+1)                        
        
        user_alpha_beta_avg[stimulus_id] = [round(user_avg_delta,3), round(user_avg_theta,3), round(user_avg_low_alpha,3), round(user_avg_high_alpha,3), round(user_avg_low_beta,3), round(user_avg_high_beta,3), round(user_avg_low_gamma,3), round(user_avg_mid_gamma,3)]
        
    return user_alpha_beta_avg

def generate_blink_data():
    all_slide_data = {}
    all_users_att_med  = {}  
    all_users_alpha_beta  = {}    
    
    for dir_name, sub_dir_list, files in os.walk(PROCESSED_PATH):
        print dir_name, sub_dir_list
        if dir_name[-3:][0].isdigit():
            user_id =  dir_name[-3:]
            user_slide_data  = get_user_slidetimestamp(user_id)
            all_slide_data[user_id] = user_slide_data
           
            #loading attn and med data  
            user_att_med = get_user_att_med(user_id)
            all_users_att_med[user_id] = user_att_med
            user_attn_med_blink = generate_user_blink_attn(user_slide_data, user_att_med)
            with open(PROCESSED_PATH+user_id+"/blink_att_med.json", "w") as fp:
                fp.write(json.dumps(user_attn_med_blink))
            all_users_att_med[user_id] = user_attn_med_blink
            
            #loading alpha, beta,...
            user_alpha_beta_data,normalized_alpha_beta_data = get_user_alpha_beta(user_id)
            all_users_alpha_beta[user_id] = user_alpha_beta_data
            user_alpha_beta_blink = generate_user_blink_alpha_beta(user_slide_data, user_alpha_beta_data)
            with open(PROCESSED_PATH+user_id+"/blink_alpha_beta.json", "w") as fp:
                fp.write(json.dumps(user_alpha_beta_blink))
            all_users_alpha_beta[user_id] = user_alpha_beta_blink
                        
 
    with open(ALL_USER_PROCESSED_PATH+"/blink_att_med.json", "w") as fp: 
        fp.write(json.dumps(all_users_att_med))                     
            
    with open(ALL_USER_PROCESSED_PATH+"/blink_alpha_beta.json", "w") as fp: 
        fp.write(json.dumps(all_users_alpha_beta))    
            
            
def load_meta_data():
    with open("meta_data.txt", "r") as fp:
        for line in fp:
            stimulus_index, time_dur, label, stimulus_type, long_short  = line.strip().split("\t")
            META_DATA[stimulus_index] = [time_dur, label, stimulus_type, long_short]
            LABEL_DATA.append(int(label))
            
def load_all_attn_med_data():
    with open(ALL_USER_PROCESSED_PATH+"/avg_att_med.json", "r") as fp:
        all_users_att_med  = json.loads(fp.read())
        return all_users_att_med
 
def load_all_alpha_beta_data(norm_flag=False):
    if norm_flag:
        with open(ALL_USER_PROCESSED_PATH+"/norm_avg_alpha_beta.json", "r") as fp:
            all_users_alpha_beta  = json.loads(fp.read())
            return all_users_alpha_beta               
    else:
        with open(ALL_USER_PROCESSED_PATH+"/avg_alpha_beta.json", "r") as fp:
            all_users_alpha_beta  = json.loads(fp.read())
            return all_users_alpha_beta       
        
def generate_all_user_attn_med_features(attn_med_flag):
    print "AVERAGES DATA for ==============================================", attn_med_flag 
    
    if attn_med_flag == "attn":
        val = 0
    elif attn_med_flag == "med":
        val =1
        
    all_users_att_med = load_all_attn_med_data()
    num_users = len(all_users_att_med)
    num_stimulus = len(all_users_att_med['101'])
    attn_feature_list = []
    attn_dict = {}
    all_103_29_feature_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
    all_103_29_label_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
    
    for user, attn_med in all_users_att_med.items():
        for i in range(1,len(attn_med)+1):         
            feature_val = attn_med[str(i)][val]

            stimulus_tag =  META_DATA[str(i)][2][:3].upper() + "_" + META_DATA[str(i)][3].strip().upper()
            all_103_29_feature_list[stimulus_tag].append(feature_val)
            
            popularity = int(META_DATA[str(i)][1])
            all_103_29_label_list[stimulus_tag].append(popularity)
            
            if i in attn_dict:
                attn_dict[i].append(feature_val)
            else:
                attn_dict[i] = [feature_val]
    temp_feat = []
    temp_labels = []
    for sti_tag, feat in all_103_29_feature_list.items():
        corr = compute_correlation_coeff_feat_label(feat,all_103_29_label_list[sti_tag])
        print "Stimulus type: "+sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 
        temp_feat += feat
        temp_labels += all_103_29_label_list[sti_tag]
    #print "********Number of Values=",len(temp_feat)
    #print "********",compute_correlation_coeff_feat_label(temp_feat,temp_labels )        
            
    for i in range(1, num_stimulus+1):
        attn_feature_list.append(round(sum(attn_dict[i])/len(attn_dict[i]),3))
    #print len(attn_feature_list)
    
    if attn_med_flag == "attn":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_att.json", "w") as fp:
            fp.write(json.dumps(attn_feature_list))
    elif attn_med_flag == "med": 
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_med.json", "w") as fp:
            fp.write(json.dumps(attn_feature_list))                
    return attn_feature_list

def load_all_blink_attn_med_data():
    with open(ALL_USER_PROCESSED_PATH+"/blink_att_med.json", "r") as fp:
        all_users_att_med  = json.loads(fp.read())
        return all_users_att_med
         
def generate_all_user_blink_attn_med_features(attn_med_flag):
    print "BLINK DATA for ==============================================", attn_med_flag 
    if attn_med_flag == "attn":
        val = 0
    elif attn_med_flag == "med":
        val =1
        
    all_users_att_med = load_all_blink_attn_med_data()
    num_users = len(all_users_att_med)
    num_stimulus = len(all_users_att_med['101'])
    attn_feature_list = []
    attn_dict = {}
    all_103_29_feature_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
    all_103_29_label_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
    
    for user, attn_med in all_users_att_med.items():
        for i in range(1,len(attn_med)+1):         
            feature_val = attn_med[str(i)][val]
            stimulus_tag =  META_DATA[str(i)][2][:3].upper() + "_" + META_DATA[str(i)][3].strip().upper()
            all_103_29_feature_list[stimulus_tag].append(feature_val)
            
            popularity = int(META_DATA[str(i)][1])
            all_103_29_label_list[stimulus_tag].append(popularity)
            
            if i in attn_dict:
                attn_dict[i].append(feature_val)
            else:
                attn_dict[i] = [feature_val]
    temp_feat=[]
    temp_labels = []
    for sti_tag, feat in all_103_29_feature_list.items():
        corr = compute_correlation_coeff_feat_label(feat,all_103_29_label_list[sti_tag])
        print "Number of Values=",len(feat)
        print "Stimulus type: "+sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 
        temp_feat += feat
        temp_labels += all_103_29_label_list[sti_tag]
    #print "********Number of Values=",len(temp_feat)
    #print "********",compute_correlation_coeff_feat_label(temp_feat,temp_labels )
            
    for i in range(1, num_stimulus+1):
        attn_feature_list.append(round(sum(attn_dict[i])/len(attn_dict[i]),3))
    #print len(attn_feature_list)
    
    if attn_med_flag == "attn":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_att.json", "w") as fp:
            fp.write(json.dumps(attn_feature_list))
    elif attn_med_flag == "med": 
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_med.json", "w") as fp:
            fp.write(json.dumps(attn_feature_list))        
        
    return attn_feature_list


             
def generate_all_user_alpha_beta_features(alpha_beta_flag, norm_flag=False):
    print "BLINK DATA for ==============================================", alpha_beta_flag 
       
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
    
    all_users_alpha_beta = load_all_alpha_beta_data(norm_flag)
    num_users = len(all_users_alpha_beta)
    num_stimulus = len(all_users_alpha_beta['101'])
    alpha_beta_feature_list = []
    alpha_beta_dict = {}
    all_103_29_feature_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
    all_103_29_label_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
        
    for user, alpha_beta in all_users_alpha_beta.items():
        for i in range(1,len(alpha_beta)+1): 
            feature_val = alpha_beta[str(i)][val]
            stimulus_tag =  META_DATA[str(i)][2][:3].upper() + "_" + META_DATA[str(i)][3].strip().upper()
            all_103_29_feature_list[stimulus_tag].append(feature_val)
            
            popularity = int(META_DATA[str(i)][1])
            all_103_29_label_list[stimulus_tag].append(popularity)            

            if i in alpha_beta_dict:
                alpha_beta_dict[i].append(feature_val)
            else:
                alpha_beta_dict[i] = [feature_val]

    temp_feat = []
    temp_labels = []
    for sti_tag, feat in all_103_29_feature_list.items():
        corr = compute_correlation_coeff_feat_label(feat,all_103_29_label_list[sti_tag])
        print "Stimulus type: "+sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 
        temp_feat += feat
        temp_labels += all_103_29_label_list[sti_tag]
    #print "********Number of Values=",len(temp_feat)
    #print "********",compute_correlation_coeff_feat_label(temp_feat,temp_labels ) 
    
    for i in range(1, num_stimulus+1):
        alpha_beta_feature_list.append(round(sum(alpha_beta_dict[i])/len(alpha_beta_dict[i]),3))

    #print len(alpha_beta_feature_list)
    if alpha_beta_flag == "delta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_delta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))        
        
    elif alpha_beta_flag == "theta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_theta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))                
    elif alpha_beta_flag == "low_alpha":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_low_alpha.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))          
    elif alpha_beta_flag == "high_alpha":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_high_alpha.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))            
    elif alpha_beta_flag == "low_beta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_low_beta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))         
    elif alpha_beta_flag == "high_beta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_high_beta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))          
    elif alpha_beta_flag == "low_gamma":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_low_gamma.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))            
    elif alpha_beta_flag == "mid_gamma":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_blink_mid_gamma.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))          
    
    return alpha_beta_feature_list



def load_all_blink_alpha_beta_data(norm_flag=False):
    with open(ALL_USER_PROCESSED_PATH+"/blink_alpha_beta.json", "r") as fp:
        all_users_att_med  = json.loads(fp.read())
        return all_users_att_med
    
def generate_all_user_blink_alpha_beta_features(alpha_beta_flag, norm_flag=False):
    print "AVERAGES DATA for ==============================================", alpha_beta_flag 
       
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
    
    all_users_alpha_beta = load_all_blink_alpha_beta_data(norm_flag)
    num_users = len(all_users_alpha_beta)
    num_stimulus = len(all_users_alpha_beta['101'])
    alpha_beta_feature_list = []
    alpha_beta_dict = {}
    all_103_29_feature_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
    all_103_29_label_list =  {'TEX_SHORT':[], 'TEX_LONG':[], 'PIC_PIC':[], 'VID_SHORT':[],'VID_LONG':[], 'BAS_BASELINE':[]}  
        
    for user, alpha_beta in all_users_alpha_beta.items():
        for i in range(1,len(alpha_beta)+1): 
            feature_val = alpha_beta[str(i)][val]
            stimulus_tag =  META_DATA[str(i)][2][:3].upper() + "_" + META_DATA[str(i)][3].strip().upper()
            all_103_29_feature_list[stimulus_tag].append(feature_val)
            
            popularity = int(META_DATA[str(i)][1])
            all_103_29_label_list[stimulus_tag].append(popularity)            

            if i in alpha_beta_dict:
                alpha_beta_dict[i].append(feature_val)
            else:
                alpha_beta_dict[i] = [feature_val]

    temp_feat = []
    temp_labels = []
    for sti_tag, feat in all_103_29_feature_list.items():
        corr = compute_correlation_coeff_feat_label(feat,all_103_29_label_list[sti_tag])
        print "Stimulus type: "+sti_tag +"\t"+"Corr: " + str(corr[0]) + "\t" + "p_val: " +str(corr[1]) + "\n" 
        temp_feat += feat
        temp_labels += all_103_29_label_list[sti_tag]
    #print "********Number of Values=",len(temp_feat)
    #print "********",compute_correlation_coeff_feat_label(temp_feat,temp_labels ) 
    
    for i in range(1, num_stimulus+1):
        alpha_beta_feature_list.append(round(sum(alpha_beta_dict[i])/len(alpha_beta_dict[i]),3))

    #print len(alpha_beta_feature_list)
    if alpha_beta_flag == "delta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_delta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))        
        
    elif alpha_beta_flag == "theta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_theta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))                
    elif alpha_beta_flag == "low_alpha":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_low_alpha.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))          
    elif alpha_beta_flag == "high_alpha":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_high_alpha.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))            
    elif alpha_beta_flag == "low_beta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_low_beta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))         
    elif alpha_beta_flag == "high_beta":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_high_beta.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))          
    elif alpha_beta_flag == "low_gamma":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_low_gamma.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))            
    elif alpha_beta_flag == "mid_gamma":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_mid_gamma.json", "w") as fp:
            fp.write(json.dumps(alpha_beta_feature_list))          
    
    return alpha_beta_feature_list



def normalize(data_list):
    minimum = min(data_list)
    maximum = max(data_list)
    return [round((float(elem)-minimum)/(maximum-minimum),5) for elem in data_list]
    
def get_user_alpha_beta(user_id):
    alpha_beta_data = []
    unnormalized_alpha_beta_data = {'delta':[], 'theta': [], 'low_alpha': [], 'high_alpha': [], 'low_beta':[], 'high_beta':[], 'low_gamma':[], 'mid_gamma':[]}
    
    map_dict = {1:'delta', 2:'theta', 3: 'low_alpha', 4: 'high_alpha', 5:'low_beta',  6:'high_beta', 7:'low_gamma', 8:'mid_gamma'}
    
    normalized = {'delta':[], 'theta': [], 'low_alpha': [], 'high_alpha': [], 'low_beta':[], 'high_beta':[], 'low_gamma':[], 'mid_gamma':[]}
    
    timestamps = []
    normalized_alpha_beta_data = []
    with open(PROCESSED_PATH+user_id+"/all_data.txt", "r") as fp:
        for line in fp:
            line_list=  line.strip().split("\t")
            for i, val in enumerate(line_list):
                if i != 0:
                    unnormalized_alpha_beta_data[map_dict[i]].append(int(val))
                else:
                    timestamps.append(val)
            alpha_beta_data.append(line_list)  
            
        for alpha_beta, sub_list in unnormalized_alpha_beta_data.items():       
            normalized[alpha_beta] = normalize(sub_list)
    with open(PROCESSED_PATH+user_id+"/all_normalized_data.txt", "w") as fw:
        for i in range(len(timestamps)):
            fw.write(timestamps[i] + "\t" + str(normalized['delta'][i])  + "\t" + str(normalized['theta'][i])  + "\t" + str(normalized['low_alpha'][i])  + "\t" + str(normalized['high_alpha'][i])  + "\t" + str(normalized['low_beta'][i])  + "\t" + str(normalized['high_beta'][i])  + "\t" + str(normalized['low_gamma'][i]) + "\t" + str(normalized['mid_gamma'][i]) + "\n")

            normalized_alpha_beta_data.append((timestamps[i], str(normalized['delta'][i])  , str(normalized['theta'][i])  , str(normalized['low_alpha'][i]) ,str(normalized['high_alpha'][i]) ,str(normalized['low_beta'][i])  , str(normalized['high_beta'][i]), str(normalized['low_gamma'][i]), str(normalized['mid_gamma'][i])))  
    return alpha_beta_data,normalized_alpha_beta_data
               
def compute_correlations_normalized():
    """ Calculating Correlation coeff for Attention and Meditation"""
    #attn_feature_list = generate_all_user_attn_med_features('attn')
    #med_feature_list = generate_all_user_attn_med_features('med')
    #compute_correlation_coeff(attn_feature_list)
    #compute_correlation_coeff(med_feature_list)
    
    #""" Calculating Correlation coeff for Alpha, Beta, Gamma,... """    
    delta_feature_list = generate_all_user_alpha_beta_features('delta', True)
    compute_correlation_coeff(delta_feature_list)
    
    theta_feature_list = generate_all_user_alpha_beta_features('theta', True)
    compute_correlation_coeff(theta_feature_list)    
    
    low_alpha_feature_list = generate_all_user_alpha_beta_features('low_alpha', True)
    compute_correlation_coeff(low_alpha_feature_list)
    
    high_alpha_feature_list = generate_all_user_alpha_beta_features('high_alpha', True)
    compute_correlation_coeff(high_alpha_feature_list)    
    
    low_beta_feature_list = generate_all_user_alpha_beta_features('low_beta', True)
    compute_correlation_coeff(low_beta_feature_list)
    
    high_beta_feature_list = generate_all_user_alpha_beta_features('high_beta', True)
    compute_correlation_coeff(high_beta_feature_list)    
    
    low_gamma_feature_list = generate_all_user_alpha_beta_features('low_gamma', True)
    compute_correlation_coeff(low_gamma_feature_list)
    
    mid_gamma_feature_list = generate_all_user_alpha_beta_features('mid_gamma', True)    
    compute_correlation_coeff(mid_gamma_feature_list)    

def compute_correlations_basic():
    """ Calculating Correlation coeff for Attention and Meditation"""
    attn_feature_list = generate_all_user_attn_med_features('attn')
    compute_correlation_coeff(attn_feature_list)
    
    med_feature_list = generate_all_user_attn_med_features('med')
    compute_correlation_coeff(med_feature_list)
    
    #""" Calculating Correlation coeff for Alpha, Beta, Gamma,... """    
    delta_feature_list = generate_all_user_alpha_beta_features('delta')
    compute_correlation_coeff(delta_feature_list)
    
    theta_feature_list = generate_all_user_alpha_beta_features('theta')
    compute_correlation_coeff(theta_feature_list)    
    
    low_alpha_feature_list = generate_all_user_alpha_beta_features('low_alpha')
    compute_correlation_coeff(low_alpha_feature_list)
    
    high_alpha_feature_list = generate_all_user_alpha_beta_features('high_alpha')
    compute_correlation_coeff(high_alpha_feature_list)    
    
    low_beta_feature_list = generate_all_user_alpha_beta_features('low_beta')
    compute_correlation_coeff(low_beta_feature_list)
    
    high_beta_feature_list = generate_all_user_alpha_beta_features('high_beta')
    compute_correlation_coeff(high_beta_feature_list)    
    
    low_gamma_feature_list = generate_all_user_alpha_beta_features('low_gamma')
    compute_correlation_coeff(low_gamma_feature_list)
    
    mid_gamma_feature_list = generate_all_user_alpha_beta_features('mid_gamma')    
    compute_correlation_coeff(mid_gamma_feature_list)    

def compute_correlations_blink():
    """ Calculating Correlation coeff for Attention and Meditation"""
    attn_feature_list = generate_all_user_blink_attn_med_features('attn')
    compute_correlation_coeff(attn_feature_list)

    
    med_feature_list = generate_all_user_blink_attn_med_features('med')
    compute_correlation_coeff(med_feature_list)
    
    #""" Calculating Correlation coeff for Alpha, Beta, Gamma,... """    
    delta_feature_list = generate_all_user_blink_alpha_beta_features('delta')
    compute_correlation_coeff(delta_feature_list)
    
    theta_feature_list = generate_all_user_blink_alpha_beta_features('theta')
    compute_correlation_coeff(theta_feature_list)    
    
    low_alpha_feature_list = generate_all_user_blink_alpha_beta_features('low_alpha')
    compute_correlation_coeff(low_alpha_feature_list)
    
    high_alpha_feature_list = generate_all_user_blink_alpha_beta_features('high_alpha')
    compute_correlation_coeff(high_alpha_feature_list)    
    
    low_beta_feature_list = generate_all_user_blink_alpha_beta_features('low_beta')
    compute_correlation_coeff(low_beta_feature_list)
    
    high_beta_feature_list = generate_all_user_blink_alpha_beta_features('high_beta')
    compute_correlation_coeff(high_beta_feature_list)    
    
    low_gamma_feature_list = generate_all_user_blink_alpha_beta_features('low_gamma')
    compute_correlation_coeff(low_gamma_feature_list)
    
    mid_gamma_feature_list = generate_all_user_blink_alpha_beta_features('mid_gamma')
    compute_correlation_coeff(mid_gamma_feature_list) 
    
    


def compute_correlations_gender():
    with open(ALL_USER_PROCESSED_PATH+"/gender_all_slides_avg_att.json", "r") as fattn:
        mf_attention = json.loads(fattn.read())
    compute_correlation_coeff(mf_attention['M'])
    compute_correlation_coeff(mf_attention['F'])
    
    with open(ALL_USER_PROCESSED_PATH+"/gender_all_slides_avg_med.json", "r") as fmed:
        mf_med = json.loads(fmed.read())
    compute_correlation_coeff(mf_med['M'])
    compute_correlation_coeff(mf_med['F'])

    with open(ALL_USER_PROCESSED_PATH+"/gender_all_slides_blink_att.json", "r") as fattn_blink:
        mf_attention_blink = json.loads(fattn_blink.read())
    compute_correlation_coeff(mf_attention_blink['M'])
    compute_correlation_coeff(mf_attention_blink['F'])
        

    with open(ALL_USER_PROCESSED_PATH+"/gender_all_slides_blink_med.json", "r") as fmed_blink:
        mf_med_blink = json.loads(fmed_blink.read())
    compute_correlation_coeff(mf_med_blink['M'])
    compute_correlation_coeff(mf_med_blink['F'])
                    

if __name__ == "__main__":
    load_meta_data()
    generate_blink_data()

    #load_processed_data() # creates processed data for basic correlations and normalized correlations
    
    #compute_correlations_normalized()
    #compute_correlations_basic()
    #compute_correlations_blink()
    
    #compute_correlations_gender()
    
   