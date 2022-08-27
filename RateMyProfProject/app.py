#!C:\Python27\python.exe
import ratemyprofessor
from flask import Flask, request, render_template, session, redirect 
from flask_session import Session
from datetime import timedelta

# Flask constructor  
app = Flask(__name__)
app.secret_key="zarak"

SECRET_KEY = "zarak"
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.permanent_session_lifetime = timedelta(minutes=10)
Session(app)

@app.route('/',methods=["GET","POST"]) # serving an html form to run the api
def serve_form(): #declaring a serve_form function
    
    return render_template("index.html") 

@app.route('/process',methods =["GET","POST"])# saving data from html form to python flask
def get_Uni():
    
    if request.method == "POST":
        uni= request.form.get("university")
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")

        session["uni"]=uni #placing data in session variables to allow use through different routes
        session["firstname"]=firstname
        session["lastname"]=lastname
        
        return redirect("/results") #routing app to the results
    else:
        return redirect("/") #routing app back to serve form

@app.route("/results", methods=["GET","POST"]) #sending data to html file to display
def result():
    
    uni=session.get("uni") #retrieving session variables
    firstname=session.get("firstname")
    lastname=session.get("lastname")
    name=firstname+" "+lastname
    professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name(uni), lastname) #RateMyProf api to find various scores
    
    if professor is not None: #if else statement to find if a professor is found in api
        
        department=professor.department
        profrating=professor.rating
        profdif=professor.difficulty
        profnum=professor.num_ratings
        
        if professor.would_take_again is not None: #if else statement to find if the prof would take again is available or not
           profwouldtake=professor.would_take_again
        else:
            profwouldtake= "N/A"
    return render_template("results.html",uni=uni,name=name,department=department,profrating=profrating,profdif=profdif,profwouldtake=profwouldtake,profnum=profnum) #return various variables to results.html

       
if __name__=='__main__':
   app.run(debug=True)
    
