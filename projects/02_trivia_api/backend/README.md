# Full Stack Trivia API Backend
## Install Project Locally
### Installing Dependencies
#### Python 3.7
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
#### Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.
##### Key Dependencies

  

-  [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

  

-  [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

  

-  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

  

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
### Running the server
From within the `backend` directory first ensure you are working using your created virtual environment.
To run the server, execute:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Documentation
### Getting Started
- Base URL: This app can only be run locally and is not hosted at a base URL. The backend app is hosted on a flask server at the default address,  `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
-   Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return these error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

### Endpoints
### Categories Endpoints
#### GET /categories
Retrieve all available categories
`curl -X GET http://127.0.0.1:5000/categories`
- Returns: a list of categories with each category's type as a value and a success value
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```
#### GET /categories/<category_id>/questions
Retrieves all questions from a given category
`curl -X GET http://127.0.0.1:5000/categories/2/questions`
- Returns: a list of question objects (with all the data associated with each question), the requested category, the number of questions within that category, and the success value
```
{
	"current_category": 2,
	"questions": [
	{
		"answer": "Lake Victoria",
		"category": 2,
		"difficulty": 2,
		"id": 13,
		"question": "What is the largest lake in Africa?"
	},
	{
		"answer": "The Palace of Versailles",
		"category": 2,
		"difficulty": 3,
		"id": 14,
		"question": "In which royal palace would you find the Hall of Mirrors?"
	},
	{
		"answer": "Agra",
		"category": 2,
		"difficulty": 2,
		"id": 15,
		"question": "The Taj Mahal is located in which Indian city?"
	}
	],
	"success": true,
	"total_questions": 3
}
```
### Questions Endpoints
#### GET /questions
Retrieve all questions
`curl -X GET http://127.0.0.1:5000/questions?page=1`
- Returns: a list of question objects (with all the data associated with each question), all available categories, the current categories, the total number of questions, and the success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
```
{
	"categories": [
		"Science",
		"Art",
		"Geography",
		"History",
		"Entertainment",
		"Sports"
	],
	"current_category": [
		"Science",
		"Art",
		"Geography",
		"History",
		"Entertainment",
		"Sports"
	],
	"questions": [
		{
			"answer": "Maya Angelou",
			"category": 3,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 4,
			"difficulty": 3,
			"id": 6,
			"question": "What was the titleof the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 3,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
		},
		{
			"answer": "Brazil",
			"category": 5,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		},
		{
			"answer": "Uruguay",
			"category": 5,
			"difficulty": 4,
			"id": 11,
			"question": "Which country won the first ever soccer World Cup in 1930?"
		},
		{
			"answer": "George Washington Carver",
			"category": 3,
			"difficulty": 2,
			"id": 12,
			"question": "Who invented Peanut Butter?"
		},
		{
			"answer": "Lake Victoria",
			"category": 2,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "The Palace of Versailles",
			"category": 2,
			"difficulty": 3,
			"id": 14,
			"question": "In which royal palace would you find the Hall of Mirrors?"
		},
		{
			"answer": "Agra",
			"category": 2,
			"difficulty": 2,
			"id": 15,
			"question": "The Taj Mahal is located in which Indian city?"
		},
		{
			"answer": "Escher",
			"category": 1,
			"difficulty": 1,
			"id": 16,
			"question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
		}
	],
	"success": true,
	"total_questions": 19
}
```
#### POST /questions
Searches database for questions containing a given search term, if one is provided. Otherwise, inserts a new question into the database.

Search Questions:
`curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "what"}' -H 'Content-Type: application/json'`
Create Question:
`curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "What color is the sky?", "category" : "0" , "answer" : "blue", "difficulty" : 1 }' -H 'Content-Type: application/json'`
- Returns:
	- For search: the current categories available, a list of question objects (and all their associated information) whose question attributes contain the search term (case-insensitive), and a success value
	- For insertion: the id of the new question, the total number of questions, and a success value

Example Search Response:
```
{
	"current_category": [
		{
			"id": 0,
			"type": "Science"
		},
		{
			"id": 1,
			"type": "Art"
		},
		
		[...] // all current categories
		
	],
	"questions": [
		{
			"answer": "The Liver",
			"category": 0,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Blood",
			"category": 0,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},

			[...] // + all other questions containing search term
			
	],
	"success": true,
	"total_questions": 6
}
```
Example Insertion Response:
```
{
	"created": 43,
	"num_questions": 20,
	"success": true
}
```
#### DELETE /questions/<question_id>
Deletes question with given id
`curl -X DELETE http://127.0.0.1:5000/questions/10`
- Returns: the id of the deleted question and a success value
```
{
	"question": 43,
	"success": true
}
```
### Quizzes Endpoint
#### POST /quizzes
Play the trivia game
`curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [20, 21, 27], "quiz_category" : {"type" : "Science", "id" : "0"}} ' -H 'Content-Type: application/json'`
- Returns: a random question that is in the given category (if one is provided) that hasn't been seen in the list of previous questions (if one is provided) as well as a success value
```
{
	"question": {
		"answer": "Blood",
		"category": 0,
		"difficulty": 4,
		"id": 27,
		"question": "Hematology is a branch of medicine involving the study of what?"
	},
	"success": true
}
```