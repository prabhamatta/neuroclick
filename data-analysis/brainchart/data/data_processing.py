import time

def do_offset(tuples_list, offset_val=0):
    new_tuples_list = []    
    firstval = time.strptime("2000:"+tuples_list[0][0], "%Y:%H:%M:%S")
    conversion_timer = time.mktime(time.strptime("2000:00:00:00", "%Y:%H:%M:%S"))
    
    for item in tuples_list:
        t= item[0]
        timer = time.strptime("2000:"+t, "%Y:%H:%M:%S")  ##3,4,5
        timer = time.mktime(timer) - time.mktime(firstval) + conversion_timer + offset_val
        timer = time.strftime("%H:%M:%S",time.localtime(timer))
        new_tuples_list.append((timer,item[1],item[2], item[3]))
    return new_tuples_list
    
def combine_all():
    names = ["john", "thomas","vaidy"]
    my_files = ["john.combined.csv","thomas.combined.csv","vaidy.combined.csv"]
    f_offset = {
        "john":0,
         "thomas":0,
          "vaidy":0,
        } #offset by 0 sec
    
    data = {}
    for fin in my_files:
        name = fin.split(".")[0]
        data[name] = []
        f = open(fin,"r")
        heading = f.readline()

        for line in f:
            line_list = line.strip().split(",")
            #data[name].append(line_list[0],line_list[1],line_list[2],line_list[3])
            data[name].append(tuple(line_list))
            
  
        data[name]  = do_offset(data[name],f_offset[name])
        
    before_zip = []
    for n in names:
        before_zip.append(data[n])
        
    f_attn = open("attention.csv","w") 
    f_med = open("meditation.csv","w") 
    header = "Time"+"," + ",".join([n for n in names]) + "\n"
    f_attn.write(header)
    f_med.write(header)
    for tt in zip(*before_zip):
        f_attn.write(tt[0][0] + "," + ",".join([attn for tim, ps, attn, med in tt]) + "\n")
        f_med.write(tt[0][0] + "," + ",".join([med for tim, ps, attn, med in tt]) + "\n")

    f_attn.close() 
    f_med.close()
        
    
        

if __name__ == "__main__":
    combine_all()