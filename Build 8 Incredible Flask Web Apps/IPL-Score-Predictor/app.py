import pickle
import joblib
import numpy as np
from flask import Flask,render_template,request

regressor = joblib.load('iplmodel_ridge.sav')
with open('scaler.pkl','rb') as f:
    scaler = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',val='')

@app.route('/predict',methods=['POST'])
def predict():

    a = []

    if request.method == 'POST':

        venue = request.form['venue']
        if venue=='ACA-VDCA Stadium, Visakhapatnam':
            a = a + [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Barabati Stadium, Cuttack':
            a = a + [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Dr DY Patil Sports Academy, Mumbai':
            a = a + [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Dubai International Cricket Stadium, Dubai':
            a = a + [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Eden Gardens, Kolkata':
            a = a + [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Feroz Shah Kotla, Delhi':
            a = a + [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Himachal Pradesh Cricket Association Stadium, Dharamshala':
            a = a + [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='Holkar Cricket Stadium, Indore':
            a = a + [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='JSCA International Stadium Complex, Ranchi':
            a = a + [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]

        elif venue=='M Chinnaswamy Stadium, Bangalore':
            a = a + [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]

        elif venue=='MA Chidambaram Stadium, Chepauk':
            a = a + [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]

        elif venue=='Maharashtra Cricket Association Stadium, Pune':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]

        elif venue=='Punjab Cricket Association Stadium, Mohali':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]

        elif venue=='Raipur International Cricket Stadium, Raipur':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]

        elif venue=='Rajiv Gandhi International Stadium, Uppal':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]

        elif venue=='Sardar Patel Stadium, Motera':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]

        elif venue=='Sawai Mansingh Stadium, Jaipur':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]

        elif venue=='Sharjah Cricket Stadium, Sharjah':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]

        elif venue=='Sheikh Zayed Stadium, Abu-Dhabi':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
            
        elif venue=='Wankhede Stadium, Mumbai':
            a = a + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
            
  
        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            a = a + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Capitals':
            a = a + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            a = a + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            a = a + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            a = a + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            a = a + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            a = a + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            a = a + [0,0,0,0,0,0,0,1]
        

        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            a = a + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Capitals':
            a = a + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            a = a + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            a = a + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            a = a + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            a = a + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            a = a + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            a = a + [0,0,0,0,0,0,0,1]

        if batting_team==bowling_team and batting_team!='none' and bowling_team!='none':
            return render_template('home.html',val='Batting team and Bowling team cant be same and none of the values can\'t be empty.')



        overs = request.form['overs']
        runs = request.form['runs']
        wickets = request.form['wickets']
        runs_in_prev_5 = request.form['runs_in_prev_5']
        wickets_in_prev_5 = request.form['wickets_in_prev_5']

        if overs=='' or runs=='' or wickets=='' or runs_in_prev_5=='' or wickets_in_prev_5=='':
            return render_template('home.html',val='You can\'t leave any field empty!!!')

        overs = float(overs)
        runs = int(runs)
        wickets = int(wickets)
        runs_in_prev_5 = int(runs_in_prev_5)
        wickets_in_prev_5 = int(wickets_in_prev_5)

        a = np.array(a).reshape(1,-1)

        b = [runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]
        b = np.array(b).reshape(1,-1)
        b = scaler.transform(b)

        data = np.concatenate((a,b),axis=1)


        my_prediction = int(regressor.predict(data)[0])
        print(my_prediction)

        return render_template('home.html', val=f'The final score will be around {my_prediction-5} to {my_prediction+10}.')


if __name__ == '__main__':
    app.run(debug=True)