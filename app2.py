from flask import Flask,request,redirect
from twilio import twiml
from twilio.rest import TwilioRestClient
import random
import urllib2
import time
from app3 import *

app = Flask(__name__)
account = "AC91ce9b816d9f26f43d2c4b31eb73b311"
token = "4daba747b000a19e968607b08ff7a938"
client = TwilioRestClient(account, token)
#client1 = client(account, token)
initial=1

def spamcheck():
 global initial
 if number in open("spam","rb").read():
  print "spam number detected"
  initial=5

def filewrite(code):
# print "filewrite"
 timee=time.ctime().split()
 text=" ".join([str(number),code,timee[2],timee[1],timee[4],timee[3],"\n"])
 with open("calllogs","ab+") as f:
  f.write(text)

def initialize(type):
# print "type %d"%type
 global initial,authcode
 initial=1
 authcode=random.randint(1000,9999)
 if type==2:
  filewrite("success")
  mainprog()
 if type==3:
  filewrite("spoof")
  mainprog()
 if type==4:
  filewrite("spam")
  mainprog()

def message(a,resp):
 if a==0:
  messbody="your auth code is %s"%authcode
 else:
  messbody="someone is trying to spoof a call using your number"
 resp.sms(messbody)

def numbercheck():
 response = urllib2.urlopen('https://www.searchbug.com/tools/landline-or-cellphone.aspx?FULLPHONE=%d'%int(number))
 html = response.read()
 if "LANDLINE" in html:
  print "landline",number
 else:
  print "celular",number

@app.route("/", methods=["GET","POST"])
def call():
 global number
 resp=twiml.Response()
 print initial
 number=request.values.get("From", None)
 numbercheck()
 spamcheck()
 if initial==1:
  initialize(1)
  message(0,resp)
  resp.say("This is an automatic verification system, a message is beign sent to you use it to authorise........")
  with resp.gather(numDigits=4, action="/IVR", method="POST", timeout="10") as g:
   g.say("enter the four digit auth code after the beep.... eeeeeep")
 elif initial<4 and initial>1:
  print "Authentication failed try again"
  with resp.gather(numDigits=4, action="/IVR", method="POST", timeout="10") as g:
   g.say("invalid entry plese try again....")
 elif initial==4:
  message(1,resp)
  resp.say("exceeded the limit")
  print "Spoof call detected"
  initialize(3)
 else:
  resp.say("detected spam")
  initialize(4)
 return str(resp)

@app.route("/IVR", methods=['GET', 'POST'])
def IVR1():
 global initial
 initial=initial+1
 digit_pressed = request.values.get('Digits', None)
 print digit_pressed
 if digit_pressed==str(authcode):
  print "Code authenticated"
  resp = twiml.Response()
  print "Calling 857-544-8995"
  resp.dial("+18575448995")
  initialize(2)
  return str(resp)
  return redirect("/")
 else:
  return redirect("/")

@app.route("/sms", methods=['GET','POST'])
def sms():
 number=request.values.get("From", None)
 text=request.values.get("Body", None)
 client.messages.create(to="+18575448995",from_=number,body=text)

if __name__=="__main__":
 app.run(debug=True)
