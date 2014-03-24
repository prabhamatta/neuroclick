import re
import time
import json
import unicodedata
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from werkzeug.exceptions import NotFound
import gevent
from gevent import monkey
import atexit
import os
from os import path

from flask import Flask, Response, request, render_template, url_for, redirect

from pymindwave import headset
from pymindwave.pyeeg import bin_power

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
print CUR_DIR

DATA_DIR = None

monkey.patch_all()

app = Flask(__name__)
app.debug = True

FLAG_STATUS = False
F_ATT_MED = None 
F_ALL_DATA = None 
F_SPECTRUM = None


# connect to the headset
hs = None
hs = headset.Headset('/dev/tty.MindWaveMobile-DevA')
hs.disconnect()
time.sleep(1)
print 'connecting to headset...'
hs.connect()
time.sleep(1)
while hs.get('state') != 'connected':
    print hs.get('state')
    time.sleep(0.5)
    if hs.get('state') == 'standby':
        hs.connect()
        print 'retrying connecting to headset'


def raw_to_spectrum(rawdata):
    #print rawdata
    #print len(rawdata)
    flen = 50
    spectrum, relative_spectrum = bin_power(rawdata, range(flen), 512)
    #print spectrum
    #print relative_spectrum
    return spectrum


class MindWaveNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    #def __init__(self, *a, **k):
        #super(MindWaveNamespace, self).__init__(*a, **k)
        ##atexit.register(self.recv_disconnect)
        
        
    def initialize(self, flag_status = True):
        self.logger = app.logger
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def set_flag(self, status):
        self.flag = status
        
    def recv_connect(self):
        #with open("test.txt","w") as ftest:
        #ftest.write("Helloworld\n")
        #ftest.close()
        
    
        def send_metrics():
            global hs
            global FLAG_STATUS
            global F_ATT_MED
            
            while True:
                t = time.time()
                waves_vector = hs.get('waves_vector')
                meditation = hs.get('meditation')
                attention = hs.get('attention')
                spectrum = raw_to_spectrum(hs.get('rawdata')).tolist()
                #print spectrum
                if FLAG_STATUS:
                    #print F_ATT_MED
                    F_ATT_MED.write(str(t) + "\t" + str(attention )+ "\t" + str(meditation) +"\t" + str(hs.parser.poor_signal)+ "\n")
                    print str(t) + "\t" + str(attention )+ "\t" + str(meditation) +"\t" + str(hs.parser.poor_signal)
                    F_SPECTRUM.write(str(t) + "\t" + str(spectrum)+"\n")
                    F_ALL_DATA.write(str(t) + "\t" + str(waves_vector[0] )+ "\t" + str(waves_vector[1]) +"\t" + str(waves_vector[2] )+ "\t" + str(waves_vector[3]) +"\t" + str(waves_vector[4] )+ "\t" + str(waves_vector[5])+ "\t" + str(waves_vector[6])+ "\t" + str(waves_vector[7]) +"\n")
                
                self.emit('second_metric', {
                    'timestamp': t,
                    'meditation': {
                        'value': meditation,
                    },
                    'attention': {
                        'value': attention,
                    },
                    'raw_spectrum': {
                        'value': json.dumps(spectrum),
                    },
                    'delta_waves': {
                        'value': waves_vector[0],
                    },
                    'theta_waves': {
                        'value': waves_vector[1],
                    },
                    'alpha_waves': {
                        'value': (waves_vector[2]+waves_vector[3])/2,
                    },
                    'low_alpha_waves': {
                        'value': waves_vector[2],
                    },
                    'high_alpha_waves': {
                        'value': waves_vector[3],
                    },
                    'beta_waves': {
                        'value': (waves_vector[4]+waves_vector[5])/2,
                    },
                    'low_beta_waves': {
                        'value': waves_vector[4],
                    },
                    'high_beta_waves': {
                        'value': waves_vector[5],
                    },
                    'gamma_waves': {
                        'value': (waves_vector[6]+waves_vector[7])/2,
                    },
                    'low_gamma_waves': {
                        'value': waves_vector[6],
                    },
                    'mid_gamma_waves': {
                        'value': waves_vector[7],
                    },
                })
                gevent.sleep(1)
        self.spawn(send_metrics)
        return True

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        self.disconnect(silent=True)
        return True


def init_db():
    #db.create_all(app=app)
    global hs
    pass


# views
@app.route('/')
def index():
    """
    show index
    """
    return render_template('index.html')

@app.route('/expt')
def expt():
    """
    show index
    """
    return render_template('start.html')



@app.route('/basic')
def basic():
    """
    show index
    """
    return render_template('basic.htm')

@app.route('/startcall', methods = ["GET","POST"])
def startbutton():
    """
    show index
    """
    global CUR_DIR
    global FLAG_STATUS
    global DATA_DIR
    global F_ATT_MED
    global F_SPECTRUM
    global F_ALL_DATA

    
    
    with open("userids.txt", "a+") as fp:
        fp.seek(0)
        last_id = fp.readlines()[-1].strip()
        print "LAST ID===",last_id
        next_id = str(int(last_id)+1)
        fp.write(next_id + "\n") 
    new_dir = "data/"+str(next_id)
    print new_dir
    DATA_DIR = os.path.join(CUR_DIR,new_dir)
    print DATA_DIR
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)    
    
    F_ATT_MED = open(DATA_DIR + "/att_med.txt","w")
    F_SPECTRUM = open(DATA_DIR + "/spectrum.txt","w")
    F_ALL_DATA = open(DATA_DIR + "/all_data.txt","w")
    
    print "AFTER creating...",F_ATT_MED
    FLAG_STATUS = True
    return render_template('basic.htm')


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/mindwave': MindWaveNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()

 
def onexit():
    global F_ATT_MED 
    print "Exiting..."
    F_ATT_MED.close()
    F_SPECTRUM.close()
    F_ALL_DATA.close()
    
if __name__ == '__main__':
    import atexit
    atexit.register(onexit)
    app.run(port=7000)
