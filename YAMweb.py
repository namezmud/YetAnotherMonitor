from flask import Flask,render_template, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE

import datetime

import YAMdisplay
import YAMextract
import pickle

application = Flask(__name__)

application.vars={}

@application.route('/', methods=['GET', 'POST'])
def index():

    yam = YAMdisplay.YAMdisplay()
    
    #    data = {'milii': {1493517926.254: 23.00, 1493517937.666: 23.00}, 'Bob': {1493517926.254: 27.0, 1493517937.666: 27.9}}
    
    e = YAMextract.YAMextract()
    data = e.getData()

#    with open('data.pic', 'rb') as infile:
#        data = pickle.load(infile)
    
    [script, div] = yam.getTemperature(data)
#    [script, div] = ["", ""]
        
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    #return render_template('graph.html',
    return render_template('index.html',
                           script=script,
                           js_resources=js_resources,
                           css_resources=css_resources,
                           div=div)

if __name__ == "__main__":

    application.debug = True
    application.run()
