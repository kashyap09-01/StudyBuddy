from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from pypdf import PdfReader
import google.generativeai as palm
palm.configure(api_key='YOUR_API_KEY')
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
# import io
import time
from PyPDF2 import PdfReader
import re
import random
from genetictabler import GenerateTimeTable
import datetime
import math

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password!', category='error')
        else:
            flash('Email does not exist! Please Sign Up!', category='error')

    return render_template('StudyBuddy.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',  methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('useremail')
        name = request.form.get('username')
        pass1 = request.form.get('userpassword1')
        pass2 = request.form.get('userpassword2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exists! Please Login!', category='success')
        if len(name) < 2:
            flash('Signup Unsuccesful. Name must be atleast 2 Characters.', category='error')
        if pass1 != pass2:
            flash('Signup Unsuccesful. Passwords do not match.', category='error')
        if len(pass1) < 7:
            flash('Signup Unsuccesful. Password must be atleast 7 characters.', category='error')
        else:
            new_user = User(email=email, username=name, password = generate_password_hash(pass1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Signup Successful. Account Created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        return render_template('StudyBuddy.html')
    
@auth.route('/answergen',  methods=['GET', 'POST'])
def answergen():
    if request.method == 'POST':
        # Get the PDF file from the user
        pdf_file = request.files['pdf_file']

        # Read the PDF file as text
        # creating a pdf file object
        reader = PdfReader(pdf_file)
        # creating a pdf reader object
        # pdfReader = PdfReader(pdfFileObject)
        text=[]
        summary=' '
        #Storing the pages in a list
        for i in range(0,len(reader.pages)):
        # creating a page object
            pageObj = reader.pages[i].extract_text()
            pageObj= pageObj.replace('\t\r','')
            pageObj= pageObj.replace('\xa0','')
            # extracting text from page
            text.append(pageObj)
        # Merge multiple page - to reduce API Calls
        def join_elements(lst, chars_per_element):
            new_lst = []
            for i in range(0, len(lst), chars_per_element):
                new_lst.append(''.join(lst[i:i+chars_per_element]))
            return new_lst

        # Option to keep x elements per list element
        new_text = join_elements(text, 3)


        for i in range(len(new_text)):
            prompt =f"""
            Your task is to act as a Question answer Generator.
            I'll give you text from  pages of a book from beginning to end.
            And your job is to give 10 long questions and their answers regarding the text from these pages.
            The answers should atleast be 5 sentences long.
            Don't be conversational.
            Text is shared below, delimited with triple backticks:
            ```{text[i]}```
            """
            try:
                response = get_completion(prompt)
            except:
                response = get_completion(prompt)
            summary= summary+' ' +response.result +'\n\n'
            
            # result.append(response)
            time.sleep(19) 

        # Return the questions and answers to the user
        return render_template('Answer.html', questions_and_answers=summary)
    else:
        return render_template('Answer.html')



# def convert_file_storage_to_string(file_storage, encoding='utf-8'):
#     """Converts a FileStorage object to a string object."""

#     data = file_storage.read()
#     data= str(data)
#     # try:
#     #     return data.decode(encoding)
#     # except UnicodeDecodeError:
#     #     return data.decode('latin-1')

# def convert_file_storage_to_bytes(file_storage):
#     """Converts a FileStorage object to a bytes object."""

#     data = file_storage.read()
#     return data


def get_completion(prompt):
    response = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=800,)
    return response

@auth.route('/assessment',  methods=['GET', 'POST'])
@login_required
def assessment():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']

        reader = PdfReader(pdf_file)
        text=[]
        summary=' '
        for i in range(0,len(reader.pages)):
            pageObj = reader.pages[i].extract_text()
            pageObj= pageObj.replace('\t\r','')
            pageObj= pageObj.replace('\xa0','')
            text.append(pageObj)
        def join_elements(lst, chars_per_element):
            new_lst = []
            for i in range(0, len(lst), chars_per_element):
                new_lst.append(''.join(lst[i:i+chars_per_element]))
            return new_lst

        new_text = join_elements(text, 3)

        for i in range(len(new_text)):
            prompt =f"""
            Your task is to act as a Multiple Choice Question Generator.
            I'll give you text from  pages of a book from beginning to end.
            And your job is to give 10 multiple choice questions with options, and also answers regarding the text from these pages.
            I want the question, answer and the options to be returned in the form of a python dictionary.
            The format of the returned text should be in the following format:
            "question": question,
            "answer": answer,
            "options": options.
            The above mentioned format is to be followed everytime.
            The exact answer should be one of the options.
            Don't be conversational.
            Text is shared below, delimited with triple backticks:
            ```{text[i]}```
            """
            try:
                response = get_completion(prompt)
            except:
                response = get_completion(prompt)
            summary= summary+' ' +response.result +'\n\n'
            time.sleep(19) 

        print(summary)

        pattern = r'"question": "(.*?)",\s+"answer": "(.*?)",\s+"options": \["(.*?)", "(.*?)", "(.*?)", "(.*?)"\]'

        # Find all matches using the regular expression pattern
        matches = re.findall(pattern, summary)


        # Assuming 'matches' is a list of tuples containing (question, answer, option1, option2, option3, option4)
        # Initialize the list to hold the shuffled questions
        questions_list = []

        for match in matches:
            question, answer, option1, option2, option3, option4 = match

            # Shuffle the options
            options = [option1, option2, option3, option4]
            random.shuffle(options)

            # Find the index of the correct answer
            correct_index = options.index(answer) + 1  # Adding 1 to convert to 1-based indexing

            question_dict = {
                "question": question,
                "answer": (chr(ord('A') + correct_index - 1)).lower(),  # Convert index to corresponding ASCII character
                "options": options
            }

            questions_list.append(question_dict)
        
        
        # Print the list of dictionaries
        for question_dict in questions_list:
            print("Question:", question_dict["question"])
            print("Answer:", question_dict["answer"])
            print("Options:", question_dict["options"])
            print("\n")
        return render_template('assessment.html', questions_list=questions_list)
    else:
        return render_template('file_upload.html')

@auth.route('/mcq_generator',  methods=['GET', 'POST'])
@login_required
def generate_mcq():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']

        reader = PdfReader(pdf_file)
        text=[]
        summary=' '
        for i in range(0,len(reader.pages)):
            pageObj = reader.pages[i].extract_text()
            pageObj= pageObj.replace('\t\r','')
            pageObj= pageObj.replace('\xa0','')
            text.append(pageObj)
        def join_elements(lst, chars_per_element):
            new_lst = []
            for i in range(0, len(lst), chars_per_element):
                new_lst.append(''.join(lst[i:i+chars_per_element]))
            return new_lst

        new_text = join_elements(text, 3)

        for i in range(len(new_text)):
            prompt =f"""
            Your task is to act as a Multiple Choice Question Generator.
            I'll give you text from  pages of a book from beginning to end.
            And your job is to give 10 multiple choice questions with options, and also answers regarding the text from these pages.
            I want the question, answer and the options to be returned in the form of a python dictionary.
            The format of the returned text should be in the following format:
            "question": question,
            "answer": answer,
            "options": options.
            The above mentioned format is to be followed everytime.
            The exact answer should be one of the options.
            Don't be conversational.
            Text is shared below, delimited with triple backticks:
            ```{text[i]}```
            """
            try:
                response = get_completion(prompt)
            except:
                response = get_completion(prompt)
            summary= summary+' ' +response.result +'\n\n'
            time.sleep(19) 

        print(summary)
        
        pattern = r'"question": "(.*?)",\s+"answer": "(.*?)",\s+"options": \["(.*?)", "(.*?)", "(.*?)", "(.*?)"\]'

        matches = re.findall(pattern, summary)

        questions_list = []

        for match in matches:
            question, answer, option1, option2, option3, option4 = match

            question_dict = {
                "question": question,
                "answer": answer,
                "options": [option1, option2, option3, option4]
            }

            questions_list.append(question_dict)

        # Print the list of dictionaries
        for question_dict in questions_list:
            print("Question:", question_dict["question"])
            print("Answer:", question_dict["answer"])
            print("Options:", question_dict["options"])
            print("\n")
        return render_template('mcq_generator.html', questions_list=questions_list)
    else:
        return render_template('mcq_file.html')
    

@auth.route('/timetable')
def timetable():
    return render_template("/TTM.html")
8
@auth.route('/generate_timetable',methods =['POST'])
def gentimetable():

    preferredStartTiming = request.form.get('pfst')
    preferredEndTiming = request.form.get('pfet')

    numSubjects = request.form.getlist('subjectName[]')

    # Get the form data
    information = {
    "classes" : 1,
    "pfst": preferredStartTiming,
    "pfet": preferredEndTiming,
    "numSubjects" : request.form.get('numSubjects'),
    "slots" : math.floor(calculate_time_difference(preferredStartTiming,preferredEndTiming)),
    "dayz" : request.form.get('days'),
    "subjectNames" : request.form.getlist('subjectName[]'),
    "reps" : request.form.get('reps'),
    }


    '''print(information["classes"])
    print(information["numSubjects"])
    print(information['slots'])
    print(information['dayz'])
    print(information['reps'])'''


    table = GenerateTimeTable(int(information["classes"]),int(information["numSubjects"]),int(information['slots']),int(information['dayz']),int(information['reps']))

    duplicate_list = []

    for single_table in table.run():
        for days in single_table:
            print(days)
            duplicate_list.append(days)
        print("-----------------------------------")



    # Pass the HTML table string to the template
    return render_template("/AIGTT.html",info = information, duplicate_list=duplicate_list,d =len(duplicate_list),e = len(numSubjects))


#FUNCTION TO CALCULATE TIME DIFFERENCE TO GET SLOTS

def calculate_time_difference(pfst, pfet):
  """Calculates the difference in hours between two times.

  Args:
    pfst: The preferred start time, as a string in the format "HH:MM".
    pfet: The preferred end time, as a string in the format "HH:MM".

  Returns:
    The difference in hours between the two times, as a float.
  """

  # Convert the times to datetime objects.
  start_time = datetime.datetime.strptime(pfst, "%H:%M")
  end_time = datetime.datetime.strptime(pfet, "%H:%M")

  # Calculate the difference in seconds between the two datetime objects.
  time_difference = (end_time - start_time).total_seconds()

  # Divide the difference in seconds by 3600 to get the difference in hours.
  time_difference_in_hours = time_difference / 3600

  return time_difference_in_hours


    
