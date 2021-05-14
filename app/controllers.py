import random
import json
from flask          import render_template, flash, redirect, url_for, request, jsonify
from flask_login    import current_user, login_user, logout_user, login_required
from datetime       import time
from datetime       import datetime
from app            import db, login
from app.forms      import LoginForm, RegistrationForm, EditProfileForm
from app.models     import load_user
from app.models     import User, CurrentQuestion, Option, Score
from werkzeug.urls  import url_parse

 
# Helper class for user control
class UserController():
    # Login function
    def login():
        form = LoginForm()
        if form.validate_on_submit():            # validate login form
            user = User.query.filter_by(username = form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            next_page = request.args.get('next') # save requested (protected) URL
            if not next_page or url_parse(next_page).netloc !='':
                next_page = 'home'               # redirect to home if requested URL doesn't exist
            return redirect(url_for(next_page))  # 
        return render_template('login.html', title="Log In", form=form)
    
    # Register function
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            # add new user to user table
            user = User(username=form.username.data, user_type='regular',
                        email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=False)    # login immediately
            return redirect(url_for('home'))    # redirect to home
        return render_template('register.html', title='Register', form=form)

    # Quiz submission resultss
    def submit_results():
        resultDict = request.get_json(force=True)
        userID = int(resultDict['userID'])
        questionsetID = resultDict['questionsetID']
        score = resultDict['score']
        seconds = resultDict['timeTaken']
        time_obj = seconds.split(':')
        timeTaken = time(minute = int(time_obj[0]), second = int(time_obj[1]))
        res = Score(user_id = userID,
                    questionset_id = questionsetID,
                    score = score,
                    time_taken = timeTaken)
        db.session.add(res)
        db.session.commit()
        return redirect(url_for('result'))



# Helper class for generating quiz
class QuizController():
    def generate_quiz():
        # Get a list of questions belongs to the selected set.  
        questionsetID = request.args.get('questionsetID')
        questionList = CurrentQuestion.query.filter(CurrentQuestion.questionset_id == questionsetID).all()
        quiz_dict = []      # initialise question set
        totalTime = 0       # initialise time available
        for i in range(0, len(questionList)):           # for each question
            if questionList[i].question_id != '':       # validate whether the id is empty
                answerOptions = Option.query.filter_by(question_id = questionList[i].parent.id).all()
                answerOptions.append(questionList[i].parent.answer)
                random.shuffle(answerOptions)           # shuffle options
                quiz_dict.append({'question':questionList[i].parent.question,
                                'qType':'multiple',
                                'answerOptions': answerOptions,
                                'answer':questionList[i].parent.answer})
                totalTime += 20                         # 20 sec / question
        return render_template('quiz.html', questions = quiz_dict, timer = totalTime, questionsetID = questionsetID)

