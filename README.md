# StudyBuddy: The Ultimate Study Companion

StudyBuddy is a website developed to help students prepare for their exams and for teachers to prepare study materials. Users can upload a PDF and get important questions, answers, and MCQs extracted from the document. They can also attempt quizzes based on these MCQs, evaluate themselves, and generate study timetables by specifying the number of subjects and hours dedicated to each subject. Users need to log in to access the features of the website.

## Features
- Upload PDFs to extract important questions and answers
- Generate MCQs from the provided study material
- Attempt quizzes based on the generated MCQs
- Generate study timetables using AI (Genetic Algorithms) or manually
- User authentication and login system

## Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Flask
- Database: SQLite3
- AI API: PALM AI API for generating questions and MCQs

## Folder Structure
```
website
|-- static
|-- templates
|-- __init__.py
|-- auth.py
|-- views.py
main.py
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kashyap09-01/StudyBuddy.git
   cd StudyBuddy
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
   
3. **Set up the database**:
   Initialize the SQLite3 database by running the following command in the Python shell:
   ```python
   from website import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()
   ```

4. **Run the website**:
   ```bash
   python main.py
   ```

5. **Open the website**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
- Log in to the website using your credentials.
- Upload a PDF document to extract important questions and answers.
- Generate MCQs from the uploaded document.
- Attempt quizzes and evaluate your performance.
- Generate a study timetable by specifying the number of subjects and hours dedicated to each subject. You can choose to generate the timetable using AI (Genetic Algorithms) or build it manually.

## AI Integration
The PALM AI API is used to generate important questions and MCQs from the uploaded PDFs. Ensure you have the necessary API keys and configurations set up to use the PALM AI API.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements
- [PALM AI]([https://palm.ai/](https://ai.google.dev/gemini-api)) for the API used in generating questions and MCQs.
- [Flask](https://flask.palletsprojects.com/) for the web framework.

