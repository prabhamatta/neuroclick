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

from flask import Flask, Response, request, render_template, url_for, redirect

from pymindwave import headset
from pymindwave.pyeeg import bin_power


monkey.patch_all()

app = Flask(__name__)
app.debug = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/chat.db'
#db = SQLAlchemy(app)

fname = "dummy1.txt"
FLAG_STATUS = False
fout = None 


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
            global fout
            
            while True:
                t = time.time()
                waves_vector = hs.get('waves_vector')
                meditation = hs.get('meditation')
                attention = hs.get('attention')
                spectrum = raw_to_spectrum(hs.get('rawdata')).tolist()
                #print spectrum
                if FLAG_STATUS:
                    fout.write(str(attention )+ "\t" + str(meditation) +"\t" + str(hs.parser.poor_signal))
                    print str(attention )+ "\t" + str(meditation) +"\t" + str(hs.parser.poor_signal)
                    
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

@app.route('/start')
def expt():
    """
    show index
    """
    return render_template('start.html')

@app.route('/startcall', methods = ["GET"])
def startbutton():
    """
    show index
    """
    global fout
    global FLAG_STATUS
    
    fout = open(fname,"w")
    FLAG_STATUS = True
    return render_template('expt.html')


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/mindwave': MindWaveNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()

 
def onexit():
    global fout 
    print "Exiting..."
    fout.close()
    
if __name__ == '__main__':
    import atexit
    atexit.register(onexit)
    app.run(port=7000)
