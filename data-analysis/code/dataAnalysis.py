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
 
def compute_correlation_coeff(feature_list):
    X = feature_list
    Y = LABEL_DATA
    
    #print scipy.corrcoef(X,Y)
    print pearsonr(X,Y)
    
    plt.scatter(X,Y)
    
    plt.show()
    print "*****************************"
    
def compute_correlation_coeff(feature_list,LABEL_DATA ):
    X = feature_list
    Y = LABEL_DATA
    
    #print scipy.corrcoef(X,Y)
    print pearsonr(X,Y)
    
    #plt.scatter(X,Y)
    #plt.show()
    print "*****************************"
    
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
            user_alpha_beta_data = get_user_alpha_beta(user_id)
            all_users_alpha_beta[user_id] = user_alpha_beta_data
            user_alpha_beta_avg = generate_user_avg_alpha_beta(user_slide_data, user_alpha_beta_data)
            with open(PROCESSED_PATH+user_id+"/avg_alpha_beta.json", "w") as fp:
                fp.write(json.dumps(user_alpha_beta_avg))
            all_users_alpha_beta[user_id] = user_alpha_beta_avg
 
    with open(ALL_USER_PROCESSED_PATH+"/avg_att_med.json", "w") as fp: 
        fp.write(json.dumps(all_users_att_med))                     
            
    with open(ALL_USER_PROCESSED_PATH+"/avg_alpha_beta.json", "w") as fp: 
        fp.write(json.dumps(all_users_alpha_beta))    


def load_meta_data():
    with open("meta_data.txt", "r") as fp:
        for line in fp:
            stimulus_index, time_dur, label  = line.strip().split("\t")
            META_DATA[stimulus_index] = [time_dur,label]
            LABEL_DATA.append(int(label))
            
def load_all_attn_med_data():
    with open(ALL_USER_PROCESSED_PATH+"/avg_att_med.json", "r") as fp:
        all_users_att_med  = json.loads(fp.read())
        return all_users_att_med
 
def load_all_alpha_beta_data():
    with open(ALL_USER_PROCESSED_PATH+"/avg_alpha_beta.json", "r") as fp:
        all_users_alpha_beta  = json.loads(fp.read())
        return all_users_alpha_beta       
        
def generate_all_user_attn_med_features(attn_med_flag):
    if attn_med_flag == "attn":
        val = 0
    elif attn_med_flag == "med":
        val =1
        
    all_users_att_med = load_all_attn_med_data()
    num_users = len(all_users_att_med)
    num_stimulus = len(all_users_att_med['101'])
    attn_feature_list = []
    attn_dict = {}
    
    for user, attn_med in all_users_att_med.items():
        for i in range(1,len(attn_med)+1): 
            if i in attn_dict:
                attn_dict[i].append(attn_med[str(i)][val])
            else:
                attn_dict[i] = [attn_med[str(i)][val]]

    for i in range(1, num_stimulus+1):
        attn_feature_list.append(round(sum(attn_dict[i])/len(attn_dict[i]),3))

    print len(attn_feature_list)
    if attn_med_flag == "attn":
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_att.json", "w") as fp:
            fp.write(json.dumps(attn_feature_list))
    elif attn_med_flag == "med": 
        with open(ALL_USER_PROCESSED_PATH+"/all_slides_avg_med.json", "w") as fp:
            fp.write(json.dumps(attn_feature_list))        
        
    return attn_feature_list

        
def generate_all_user_alpha_beta_features(alpha_beta_flag):
    
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
    

    all_users_alpha_beta = load_all_alpha_beta_data()
    num_users = len(all_users_alpha_beta)
    num_stimulus = len(all_users_alpha_beta['101'])
    alpha_beta_feature_list = []
    alpha_beta_dict = {}

    for user, alpha_beta in all_users_alpha_beta.items():
        for i in range(1,len(alpha_beta)+1): 
            if i in alpha_beta_dict:
                alpha_beta_dict[i].append(alpha_beta[str(i)][val])
            else:
                alpha_beta_dict[i] = [alpha_beta[str(i)][val]]

    for i in range(1, num_stimulus+1):
        alpha_beta_feature_list.append(round(sum(alpha_beta_dict[i])/len(alpha_beta_dict[i]),3))

    print len(alpha_beta_feature_list)
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



def get_user_alpha_beta(user_id):
    alpha_beta_data = []
    with open(PROCESSED_PATH+user_id+"/all_data.txt", "r") as fp:
        for line in fp:
            line_list=  line.strip().split("\t")
            alpha_beta_data.append(line_list)          
    return alpha_beta_data
               
    

if __name__ == "__main__":
    load_meta_data()
    #load_processed_data()
    
    """ Calculating Correlation coeff for Attention and Meditation"""
    attn_feature_list = generate_all_user_attn_med_features('attn')
    med_feature_list = generate_all_user_attn_med_features('med')
    compute_correlation_coeff(attn_feature_list)
    compute_correlation_coeff(med_feature_list)
    
    """ Calculating Correlation coeff for Alpha, Beta, Gamma,... """    
    delta_feature_list = generate_all_user_alpha_beta_features('delta')
    theta_feature_list = generate_all_user_alpha_beta_features('theta')
    low_alpha_feature_list = generate_all_user_alpha_beta_features('low_alpha')
    high_alpha_feature_list = generate_all_user_alpha_beta_features('high_alpha')
    low_beta_feature_list = generate_all_user_alpha_beta_features('low_beta')
    high_beta_feature_list = generate_all_user_alpha_beta_features('high_beta')
    low_gamma_feature_list = generate_all_user_alpha_beta_features('low_gamma')
    mid_gamma_feature_list = generate_all_user_alpha_beta_features('mid_gamma')
    
    compute_correlation_coeff(delta_feature_list)
    compute_correlation_coeff(theta_feature_list)    
    compute_correlation_coeff(low_alpha_feature_list)
    compute_correlation_coeff(high_alpha_feature_list)    
    compute_correlation_coeff(low_beta_feature_list)
    compute_correlation_coeff(high_beta_feature_list)    
    compute_correlation_coeff(low_gamma_feature_list)
    compute_correlation_coeff(mid_gamma_feature_list)    

   
   
    #load_processed_expt_data()
    
    #computeCoefficient_scikit()
    #generate_user_attn_features()
