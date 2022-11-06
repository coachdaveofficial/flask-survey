from crypt import methods
from urllib import response
from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension


import surveys


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "super secret key"

debug = DebugToolbarExtension(app)





# @app.route('/', methods=["GET", "POST"])
# def start():
#     # set response count to zero and start survey upon button submit
#     session["responses"] = []
   
    
#     return """
#     <form action="/home" method="POST">
#         <button>Start Survey</button>
#     </form>
#     """

@app.route('/', methods=["GET", "POST"])
def home():
    session["responses"] = []
    return render_template('survey_home.html', survey=surveys.satisfaction_survey)

@app.route('/questions/<int:num>')
def show_question(num):
    # check if URL is within range for the number of questions in survey
    try:
        survey = surveys.satisfaction_survey.questions[num]
    except IndexError:
        # if all questions completed, thank the user
        if len(session['responses']) == len(surveys.satisfaction_survey.questions):
            return redirect('/thank-you')

        
        
    if len(session['responses']) != num:
        flash('Please answer questions in numerical order')
        return redirect(f'/questions/{len(session["responses"])}')

    

    return render_template('survey_question.html', survey=survey, num=num)

@app.route('/answer/', methods=["POST"])
def answer():
    # update session with appropriate responses
    answer = request.form["choice"]
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    # send user to next question if applicable
    return redirect(f'/questions/{len(session["responses"])}')

   

@app.route('/thank-you/')
def thank_you():
    
    return """
            <h1>Thank you!</h1>
            """