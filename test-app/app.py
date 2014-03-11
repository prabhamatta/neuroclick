#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ
import atexit
import random as rn
import string

MISSING_PAGE = 'NOTFOUND'
app = flask.Flask(__name__)
app.debug = True
dbclicks = shelve.open("clicks.db")
db = shelve.open("shorten.db")


@app.route('/')
def index():
    """Builds a template based on a GET request, with some default
    arguements"""
    index_title = request.args.get("title", "Web Architecture")
    hello_name = request.args.get("name", "Prabhavathi Matta")
    #app.add_url_rule('/', 'index', index)

    return flask.render_template(
                'index.html',
                title=index_title,
                name=hello_name)



@app.route("/create", methods=['PUT', 'POST'])
def create():
    """Create an association of =short= with the POST argument =url="""
    try:
        print("Entered PUT/POST")
        print("request.form==", request.form)
        print("request.args==", request.args)
        longurl = request.form.get('long', "")
        print("Long provided....",longurl)
        shorturl = request.form.get('short', "")
        print("Short provided....",shorturl)



        """ check if shortpath already exists in db"""
        for k, v in db.items():
            if v == str(longurl):
                print("FOUND")
                shorturl = k

                """ update clicks in dbclicks database """
                clicks = dbclicks.get(str(shorturl),0)
                print("dbclicks....",clicks)
                dbclicks[str(shorturl)] = int(clicks)+1

                mesg = "Short path for "+str(longurl)+" already exits as "+str(shorturl)+"... No. of clicks(attempts to shorten this url): "+ str(clicks+1)
                return flask.render_template(
                                        'output.html',
                                        message = mesg,
                                        header = '"Hurray!!"',
                                        imglink = 'static/img/hurray.gif')


        if shorturl=="":
            shorturl = ''.join(rn.choice(string.ascii_letters) for x in range(6))
        mesg = "Short path created for "+str(longurl)+" : "+str(shorturl)
        print("Short assigned....",shorturl)
        """ create short path for url """
        db[str(shorturl)] = str(longurl)
        dbclicks[str(shorturl)] = 1

        print("sending info to output.html")

        return flask.render_template(
                        'output.html',
                        message = mesg,
                        header = '"Hurray!!"',
                        imglink = 'static/img/hurray.gif')
    except:
        import traceback
        traceback.print_exc()
        raise Exception('Short URL not properly created')



@app.route("/<short>", methods=['GET'])
def redirect(short):
    """Redirect the request to the URL associated =short=, otherwise return 404
    NOT FOUND"""
    print("SHORT is....",short)
    destination = db.get(str(short), MISSING_PAGE)

    print("DESTINATION is....",destination)
    print("Redirecting to " + destination)
    if destination == MISSING_PAGE:
        mesg = "URL for "+short +" is not set"
        return flask.render_template(
                                'output.html',
                                message = mesg,
                                header = '"OOPS...404"',
                              imglink = 'static/img/404.gif')
       #return flask.render_template('404.html',
                                     #shorturl=short)
    else:
        return flask.redirect(destination)


@app.route("/delete", methods=['POST'])
def destroy():
    """Remove the association between =short= and its URL"""
    try:
        print("Entered DELETE")
        print("request.form==", request.form)
        print("request.args==", request.args)
        shorturl = request.form.get('short', "")
        print("Short provided....",shorturl)
        longurl = db.get(str(shorturl),None)
        print("Long from db....",longurl)

        """ check if shortpath already exists in db"""
        if longurl is None:
            mesg = "You are trying to delete the short url "+shorturl +" which is not in the database"
            return flask.render_template(
                            'output.html',
                            message = mesg,
                            header = '"Whhhaaat??"',
                          imglink = 'static/img/whhaat.gif')
        else:
            mesg = "Short path "+shorturl+" is deleted successfully!"

            """ updating clicks in dbclicks database """
            clicks = dbclicks.get(str(shorturl),None)
            print("++++++++++++",clicks)
            if clicks is not None:
                dbclicks.pop(str(shorturl))
                print("deleted dbclicks")

            db.pop(str(shorturl))
            return flask.render_template(
                        'output.html',
                        message = mesg,
                        header = '"Yuppie!!"',
                       imglink = 'static/img/yuppie.gif')
    except:
        import traceback
        traceback.print_exc()
        raise Exception('ERROR in deleting Short URL')

def onexit():
    db.close()


if __name__ == "__main__":
    atexit.register(onexit)
    app.run(port=int(environ['FLASK_PORT']))

