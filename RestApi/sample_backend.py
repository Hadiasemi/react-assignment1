from flask import Flask
from flask import request
from flask import jsonify

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

app = Flask(__name__)

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

@app.route('/users', methods=['GET', 'POST'])
def get_users_methods():
   if request.method == 'GET':
      search_username = request.args.get('name')
      if search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      users['users_list'].append(userToAdd)
      resp = jsonify(success=True)
      #resp.status_code = 200 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp

@app.route('/users/<name>', methods=['GET', 'DELETE'])
def get_user(name):
    if name:
        if request.method == 'GET':
            for user in users['users_list']:
                if user['name'] == name:
                    return user
            return ({})
        elif request.method == 'DELETE':
            for user in users['users_list']:
                if user['name'] == name:
                    users['users_list'].remove(user)
                    resp = jsonify(success=True)
                    resp.status_code = 204
                    return resp
            resp = jsonify(success=False)
            resp.status_code = 404
            resp.message = "Id Not Found"
            return resp
    return users

if(__name__ == '__main__'):
   app.debug = True
   app.run()