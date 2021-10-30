from flask import Flask, render_template, request
from out_prediction import Prediction_class
import datetime

app = Flask(__name__)

print("Hello")

@app.route("/")
def home():
    return render_template("home2.html")

@app.route("/inputs")
def inputs():
    return render_template("form.html")


@app.route("/predict" , methods=["POST"])
def predict():
    if request.method == "POST":
        
        if request.form['submit'] == 'PREDICT':
        
            season = (int(request.form.get("season")))
            holiday = (int(request.form.get("holiday")))
            weathersit = (int(request.form.get("weathersit")))
            temp = (float(request.form.get("temp"))-(-8))/(39-(-8))
            atemp = (float(request.form.get("atemp"))-(-16))/(50-(-16))
            hum = (float(request.form.get("hum"))/100)
            windspeed = (float(request.form.get("windspeed"))/67)
            dteday = request.form.get("dteday")
        weekday = datetime.datetime.strptime(dteday,'%Y-%m-%d').weekday() 
        mnth = datetime.datetime.strptime(dteday,'%Y-%m-%d').month

    
        if(holiday==0 and (weekday in [0,1,2,3,4]) ):
            workingday=1
        elif(holiday==0 and (weekday in [5,6])):
            workingday=0
        elif(holiday==1 and (weekday in [0,1,2,3,4])):
            workingday=0
        else:
            holiday=0
            workingday=0
        if(datetime.datetime.strptime(dteday,'%Y-%m-%d').year == 2020):
            yr=0
        elif(datetime.datetime.strptime(dteday,'%Y-%m-%d').year == 2021):
            yr=1
    
    user_inputs = [{'dteday':dteday,'season':season ,'yr':yr,'mnth':mnth,'holiday':holiday,'weekday':weekday,'workingday':workingday,
 'weathersit':weathersit,'temp':temp,'atemp':atemp,'hum':hum,'windspeed':windspeed,}] 

#cols = ["dteday","season","yr","mnth","holiday","weekday","workingday","weathersit","temp","atemp","hum","windspeed","casual","registered","cnt"]

#    file_obj = open("Prediction_logs","a")
#    logger_obj = App_Logger()
    pred_class = Prediction_class()      
    cnt,casual,registered = pred_class.predict(user_inputs)
    result = [cnt,casual,registered]
 #   user_inputs[0].update({"casual":casual,"registered":registered,"cnt":cnt})
    print(result)

    return render_template("output.html", content = cnt)

if __name__ == '__main__':
    app.run(debug=False)