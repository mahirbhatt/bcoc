import os
import sys
import time
import urllib, requests
from flask import Flask, g,render_template, session, request, redirect, url_for, jsonify, json, flash, make_response, send_file
from forms import SignUpForm
from web3 import Web3, HTTPProvider
import ipfshttpclient, ipfsapi
import json
import base58
from flask_bootstrap import Bootstrap
#for login
from wtforms.validators import InputRequired, Email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import json

api = ipfsapi.connect('127.0.0.1',5001)
from werkzeug.utils import secure_filename
import pdfkit
import tempfile
import os, re, os.path

UPLOAD_FOLDER = '/home/mahir/Desktop/ZOOM/'

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'tcet'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
bootstrap = Bootstrap(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf','jpg', 'jpeg','py','odt', 'docx', 'doc'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




f=open('Bcoc.json', 'r')
if f.mode == 'r':
   BcocABI = f.read()
   BcocABI = json.loads(BcocABI)
   f.close()

print(datetime.now())
web3=Web3(HTTPProvider('http://localhost:8100'))
bcoc = web3.eth.contract(address=BcocABI['networks']['1110']['address'], abi=BcocABI['abi'])


accounts = {'1120':[web3.eth.accounts[0], 'redhat'],
'1121':[web3.eth.accounts[1], 'redhat'],
'1122':[web3.eth.accounts[2], 'redhat'],
'1123':[web3.eth.accounts[3], 'redhat']}

web3.eth.defaultAccount = accounts['1120'][0]

balance = web3.eth.getBalance(web3.eth.accounts[0])

print(balance)

@app.route('/')
def home1():
    return render_template('registrationform.html')


@app.route('/home1.html', methods=['GET','POST'])
def createevi():
    if g.user:
        message=None
        if request.method == 'POST':
            if 'files[]' not in request.files:
                flash('No file part')
                return redirect(request.url)
            files = request.files.getlist('files[]') #uploading all the uploaded files into a local folder ZOOM
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
    				#destination = "/".join([target, filename])url
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
    		# Uploading the files folder and storing list of hashes in the variable res
            res = api.add(UPLOAD_FOLDER,pin= True)
            # Removing all the files from local folder ZOOM
            for root,dirs,files in os.walk(UPLOAD_FOLDER):
                for file in files:
                    os.remove(os.path.join(root, file))
            for i in res:
                if i['Name'] == 'ZOOM':
                    evihash = i['Hash']
            print(evihash)
            session['res']= res
            c = request.form['eid']
            evidenceID = c
            evidenceIpfsHash = evihash         
            accountAddress = session['accountAddress']
            chainpas = session['chainpas']
            #print(chainpas)#testing
            print(accountAddress)
            
            web3.geth.personal.unlockAccount(accountAddress, chainpas,0)

            bcoc.functions.createEvidence(evidenceID, evidenceIpfsHash).transact({'from': accountAddress})
            #print(evidenceIpfsHash)#testingz
            message="File(s) Successfully Uploaded"
            flash('File(s) successfully uploaded')
        return render_template('home1.html',message=message)
    return redirect(url_for('login'))


 
@app.route('/getevi.html', methods=['GET', 'POST'])
def getevi():
    if g.user:
        form = SignUpForm()
        error = None
        if form.is_submitted():
            
            try:
                accountAddress = session['accountAddress']
                evidenceID = request.form['eid']
                print(evidenceID)
                file_info = bcoc.functions.getEvidence(evidenceID).call({'from': accountAddress})
                print(file_info)
                url = 'http://127.0.0.1:8080/ipfs/' + file_info
                return redirect(url)
            except Exception as e:
                flash("Error")
                print('error')
                error = 'Invalid Evidence ID!'
                return render_template("getevi.html", error = error)

        return render_template('getevi.html',form=form)
    return redirect(url_for('login')) 

@app.route('/ucoc.html')
def ucoc():
    res = session['res']
    # Receiving files using hash variable res, this method is for us to check whether all files are uploaded on ipfs. 
    for i in res:
        if i['Name'] == 'ZOOM':
            url = 'http://127.0.0.1:8080/ipfs/' + i['Hash']
            print(url)
                   
    return render_template('ucoc.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error=None
    session.pop('user', None)#for logging out user if any
    if request.method == 'POST':
        session.pop('user', None)
        userID = request.form['emp_id']
        ipfshash = bcoc.functions.login(userID).call()
        session['chainpas'] = ipfshash[0]
        session['accountAddress'] = ipfshash[1]
        if session['chainpas'] != request.form['psw']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['user'] = request.form['emp_id']
            session['chainpas'] = ipfshash[0]
            session ['accountAddress'] = ipfshash[1]
            acads = session['accountAddress']
            web3.geth.personal.unlockAccount(web3.eth.accounts[0],"redhat")
            web3.eth.sendTransaction({'to': acads, 'from': web3.eth.coinbase, 'value': 1000000000000000000})
            web3.geth.personal.lockAccount(web3.eth.accounts[0])
            return redirect(url_for('createevi'))

    return render_template('login.html', error=error)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:

        return session['user']

    return 'Not logged in!'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template(url_for('login'))   

@app.route('/transferevi.html', methods=['GET', 'POST'])
def transferevi():
    if g.user:
        form = SignUpForm()
        message=None
        error=None
        if form.is_submitted():
            try:
                accountAddress = session['accountAddress']
                chainpas = session['chainpas']
                evidenceID = request.form['eid']
                newOwnerID = request.form['empid']
                print(evidenceID)
                web3.geth.personal.unlockAccount(accountAddress, chainpas,0)
                bcoc.functions.transferEvidence(evidenceID, newOwnerID).transact({'from':accountAddress})
                message= 'Successfully Transfered Evidence!'
                return render_template('transferevi.html',message=message)
            except Exception as e:
                error='Invalid Evidence ID || you are not authorized'
                return render_template('transferevi.html',error=error)
        return render_template('transferevi.html',message=message)
    return redirect(url_for('login'))    

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    form = SignUpForm()
    if form.is_submitted():

        web3.eth.defaultAccount = web3.eth.accounts[0];
        userid = []
        regList = []
        pswlist = []

        # making dict mutable
        result2 = request.form.to_dict()
        a = result2['user_id']
        b = result2['name']
        c = result2['designation']
        d = result2['psw']
        # for i in userid:
        #     print (i) 
        #     if i is a:
        #         flash('User already exists')                  

        # userid.append(a)

        userID = a
        userIpfsHash = d
        walletAddress = web3.geth.personal.newAccount(d)
        print(walletAddress)
        web3.geth.personal.unlockAccount(web3.eth.accounts[0],"redhat")
        bcoc.functions.registration(userID, walletAddress, userIpfsHash).transact()
        with open("ipfshashreg.txt", "a+") as myfile:
        # making file empty
            myfile.write(a+"\n"+b+"\n"+c+"\n"+d)
        
        with open("ipfshashpssw.txt","a+") as passfile:
            passfile.truncate(0)
            passfile.write(d)
    
        with ipfshttpclient.connect() as client:
          #  entire registration hash 
          hash = client.add('ipfshashreg.txt')
          regHash = hash['Hash']
          regList.append(regHash)
          print (regList)

        #   password hash 
          hash = client.add('ipfshashpssw.txt')
          pswHash = hash['Hash']
          pswlist.append(pswHash)
          print(pswlist)

        os.remove('ipfshashreg.txt')
        os.remove('ipfshashpssw.txt')
        
        return render_template('registrationform.html')
    return render_template('registrationform.html', form=form)    


if __name__ == '__main__':
    app.run(debug=True)
