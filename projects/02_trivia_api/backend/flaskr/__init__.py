import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  
  #----------------------------------------------------------------------------#
  # Custom Methods:
  #----------------------------------------------------------------------------#

  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

#----------------------------------------------------------------------------#
# /categories Endpoints (GET):
#----------------------------------------------------------------------------#

  '''
  Create an endpoint to handle GET requests for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()
    format_categories = [category.format() for category in categories]
    category_names = []
    for category in format_categories:
      category_names.append(category['type'])

    return jsonify({
      'success': True,
      'categories': category_names
    })

  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'current_category': category_id
    })

  #----------------------------------------------------------------------------#
  # /questions Endpoints (GET, POST, DELETE):
  #----------------------------------------------------------------------------#

  '''
  Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def retreive_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.all()
    format_categories = [category.format() for category in categories]
    category_names = []
    for category in format_categories:
      category_names.append(category['type'])

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': category_names,
      'current_category': category_names
    })

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      
      question.delete()

      return jsonify({
        'success': True,
        'question': question_id,
      })
    except:
      abort(422)

  '''
  Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  ADDITIONALLY:
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def add_or_search_questions():
    body = request.get_json()

    if not body:
      abort(400)

    search = body.get('searchTerm', None)
    
    if search:
      try:
        selection = Question.query.filter(Question.question.ilike('%{}%'.format(search)))
        if not selection:
          abort(404)
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        categories_all = [category.format() for category in categories]

        return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(current_questions),
        'current_category': categories_all
        })

      except:
        abort(422)

    else:
      question_text = body.get('question', None)
      answer_text = body.get('answer', None)
      category = body.get('category', None)
      difficulty = body.get('difficulty', None)

      if not question_text or not answer_text or not category or not difficulty:
        abort(400)

      try:
        question = Question(question_text, answer_text, category, difficulty)
        question.insert()
        
        return jsonify({
          'success': True,
          'created': question.id,
          'num_questions': len(Question.query.all())
        })

      except:
        abort(422)

#----------------------------------------------------------------------------#
# /quizzes Endpoint (POST):
#----------------------------------------------------------------------------#

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category, one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    if not body:
      abort(400)

    category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions', None)

    if not previous_questions:
      if not category:
        question_options = Question.query.all()
      else:
        question_options = Question.query.filter(Question.category == str(category['id'])).all()
    else:
      if not category:
        question_options = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        question_options = Question.query.filter(Question.category == str(category['id']), Question.id.notin_(previous_questions)).all()
    
    
    formatted_question = random.choice(question_options).format()
    # questions_formatted = [question.format() for question in question_options]
    # random_question = random.choice(questions_formatted)

    return jsonify({
      'success': True,
      'question': formatted_question
    })
  
  #----------------------------------------------------------------------------#
  # Error Handlers:
  #----------------------------------------------------------------------------#
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500
  
  return app

    