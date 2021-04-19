from flask import Flask
from flask import request
from flask import jsonify
import string
import random
# for linking frontend-backend
from flask_cors import CORS

# for mongo db
from model_mongodb import User

users = { 
   'users_list' :
   [
      # { 
      #    'id' : 'xyz789',
      #    'name' : 'Charlie',
      #    'job': 'Janitor',
      # },
      # {
      #    'id' : 'abc123', 
      #    'name': 'Mac',
      #    'job': 'Bouncer',
      # },
      # {
      #    'id' : 'ppp222', 
      #    'name': 'Mac',
      #    'job': 'Professor',
      # }, 
      # {
      #    'id' : 'yat999', 
      #    'name': 'Dee',
      #    'job': 'Aspring actress',
      # },
      # {
      #    'id' : 'zap555', 
      #    'name': 'Dennis',
      #    'job': 'Bartender',
      # }
   ]
}
def id_gen():
    return "".join(random.choice(string.ascii_lowercase) for x in range(3)) + "".join(random.choice(string.digits) for x in range(3))


app = Flask(__name__)
CORS(app)

@app.route('/users')
def get_users():
   search_username = request.args.get('name') #accessing the value of parameter 'name'
   if search_username :
      subdict = {'users_list' : []}
      for user in users['users_list']:
         if user['name'] == search_username:
            subdict['users_list'].append(user)
      return subdict
   return users



# @app.route('/users/<id>')
# def get_user_id(id):
#    if id :
#       for user in users['users_list']:
#         if user['id'] == id:
#            return user
#       return ({})
#    return users

@app.route('/users/<name>')
def get_user_name(name):
   list_users = users
   if name :
      match_name = lambda user: user['name'] == name
      list_users = {'users_list': list(filter(match_name, list_users['users_list']))}
   return list_users 

@app.route('/users', methods=['GET', 'POST','DELETE'])
def get_users_methods():
   # find_users = users
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_userjob = request.args.get('job')
      if search_userjob and search_username:
          return User().find_users_by_name_job(search_username, search_userjob)
      elif search_username :
         # match_name = lambda user: user['users_list'] == search_username
         # find_users = {'users_list': list(filter(match_name,find_users['users_list']))}
         users = User().find_by_name(search_username)
      elif search_userjob:
         # match_job = lambda user: user['job'] == search_userjob
         # find_users = {'users_list': list(filter(match_job,find_users['users_list']))}
         return User().find_by_job(search_userjob)
      return User().find_all()
      
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd['id']=id_gen()
      users['users_list'].append(userToAdd)
      resp = jsonify(userToAdd)
      resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp
   elif request.method == 'DELETE':
      # need to send whole user to the request
      userToDelete = request.get_json()
      users['users_list'].remove(userToDelete)
      resp = jsonify(success=True)
      #resp.status_code = 200 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if id:
        if request.method == 'GET':
            for user in users['users_list']:
                if user['id'] == id:
                    return user
            return ({})
        elif request.method == 'DELETE':
            for user in users['users_list']:
                if user['id'] == id:
                    users['users_list'].remove(user)
                    resp = jsonify(success=True)
                    resp.status_code = 204
                    return resp
            resp = jsonify(success=False)
            resp.status_code = 404
            resp.message = "Id Not Found"
            return resp
    return users

# if(__name__ == '__main__'):
#    app.debug = True
#    app.run()