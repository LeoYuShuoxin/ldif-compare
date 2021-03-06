#!env/bin/python

from flask import Flask, render_template , url_for , request , make_response
from werkzeug.utils import secure_filename
from handler import ldifCompareHandler
import sys

ifWebviewGUI = True

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

import webview
import sys
import threading
import time
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index-drag-drop.html')

@app.route('/compare', methods = ['POST'])
def compare():
    aFile = request.files['aFile']
    bFile = request.files['bFile']
    csvFile, tableDate = ldifCompareHandler(aFile,bFile)["guiData"]
    if len(request.form.getlist('ifCSV_Format')) == 1 :
        #response = make_response(ldifCompareHandler(aFile,bFile)["csv"])
        #response.headers['Content-type'] = 'text/csv'
        #response.mimetype = 'text/csv'
        #response.headers['Content-Disposition'] = "attachment;filename=LDIF_compare_result.csv"
        # macOS filePath = webview.create_file_dialog(webview.SAVE_DIALOG, directory="/", save_filename='LDIF_compare_result.csv')[0]
        filePath = webview.create_file_dialog(webview.SAVE_DIALOG, directory="/", save_filename='LDIF_compare_result.csv')
        print filePath
        outputFile = open(filePath,"w")
        outputFile.write(csvFile)
        outputFile.close()
    response = render_template("result.html",data = tableDate )
    return response
def start_server():
    app.run()

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    time.sleep(3)
    webview.create_window("LDIF Compare Tool","http://127.0.0.1:5000/", width=900, height=800, resizable=True)
    sys.exit()

