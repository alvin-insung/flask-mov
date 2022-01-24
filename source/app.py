from flask import Flask, request, Response
from flask_restx import Resource, Api, fields
from flask import abort, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

ns_movie = api.namespace('ns_movie', description='Movie APIs')

movie_data = api.model(
    'Movie Data',
    {
      "name": fields.String(description="name", required=True),
      "actor": fields.String(description="actor", required=True),
    }
)

movie_info = {}
number_of_movie = 0

@ns_movie.route('/movie')
class movie(Resource):
  def get(self):
    return {
        'number_of_movie': number_of_movie,
        'movie_info': movie_info
    }

  @api.expect(movie_data) # body
  def post(self):
    global number_of_movie
    id = number_of_movie
    number_of_movie += 1

    params = request.get_json() # get body json
    params['model_id'] = id
    movie_info[id] = params
   
  
    return Response(status=200)


      
@ns_movie.route('/movie/<int:model_id>')
class movie_model(Resource):
  def get(self, model_id):
    if not model_id in movie_info.keys():
      abort(404, description=f"Model_id {model_id} doesn't exists")

    return {
        'model_id': model_id,
        'data': movie_info[model_id]
    }

  

  def delete(self, model_id):
    if not model_id in movie_info.keys():
      abort(404, description=f"Model_id {model_id} doesn't exists")

    del movie_info[model_id]
    global number_of_movie
    number_of_movie -= 1

    return Response(status=200)


  @api.expect(movie_data)
  def put(self, model_id):
    global movie_info
    if not model_id in movie_info.keys():
      abort(404, description=f"Model_id {model_id} doesn't exists")
    
    params = request.get_json()
    movie_info[model_id] = params
    
    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=31212)