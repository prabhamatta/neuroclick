__author__ = 'Neuroclick'

import os
import numpy as np
import time
from sklearn import linear_model
import json

def do_offset(tuples_list, filename, format ='%b %d, %Y %H:%M:%S', offset_val=0):
    new_tuples_list = []
    firstval = time.strptime(tuples_list[0][0], format)
    if filename != "slide_timestamps.txt":
        def_time = 'Apr 01, 2000 00:00:00'
    else :
        def_time = 'Apr 01 2000 00:00:00'
    conversion_timer = time.mktime(time.strptime(def_time, format))

    for item in tuples_list:
        t= item[0]
        timer = time.strptime(t, format)  ##3,4,5
        timer = time.mktime(timer) - time.mktime(firstval) + conversion_timer + offset_val
        timer = time.strftime("%H:%M:%S",time.localtime(timer))
        if filename == "spectrum.txt":
            line_list = [timer]
            for i in json.loads(item[1]):
                line_list.append(i)
            print line_list
            new_tuples_list.append(tuple(line_list))
            
        else:
            line_list = [timer]
            for i in item[1:]:
                line_list.append(i)
            print line_list
            new_tuples_list.append(tuple(line_list))       
    return new_tuples_list

    
def getSlideTimeStamps(fr, fw, filename):
    data = []
    text = fr.read()
    text = text.replace(', ',' ')
    text = text.replace('{', '')
    text = text.replace('}', '')

    # text = text.replace(',','\n')
    for t in text.split(','):
        index, ts = t.split('":"')
        ts = ts.replace('"','')
        index = index.replace('"','')
        data.append((ts.strip(),index.strip()))  

    new_data = do_offset(data, filename,'%b %d %Y %H:%M:%S',0)
    ret_val =[]
    for t ,index in new_data:
        fw.write(index+ "\t"+t +"\n")
    return



def getAllData(fr, fw, filename):
    user_data = []
    for line in fr:
        line_list = line.strip().split("\t")
        user_data.append(line_list)    
    
    new_data = do_offset(user_data, filename)
    for line in new_data:
        fw.write("\t".join([str(w) for w in line]))
        fw.write("\n")
    return 



def clean_up_data(raw_path, user_id, filename):
    directory = "../processed_data/"+user_id
    if not os.path.exists(directory):
        os.makedirs(directory)    

    with open("../processed_data/"+user_id+"/"+filename, "w") as fw, open(raw_path+"/"+filename, "r") as fr:
        if "slide"  in filename:
            getSlideTimeStamps(fr,fw, filename)
        else:
            getAllData(fr,fw, filename)


def loadData():
    path = "../../neuroclick-app/data/"
    for dir_name, sub_dir_list, files in os.walk(path):
        #print dir_name, sub_dir_list
        if dir_name[-3:][0].isdigit():
            user_id =  dir_name[-3:]
            for filename in files:
                print filename
                clean_up_data(dir_name, user_id, filename)
                
                
if __name__ == "__main__":
    loadData()
