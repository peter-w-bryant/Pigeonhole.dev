# # Path: backend\api\routes\auth.py
# from flask import request, jsonify, Blueprint
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# from sqlalchemy.exc import IntegrityError  

# from utils.db import db
# from utils.models import Users
# from utils.auth import bcrypt, login_manager
# from utils.admin import requires_admin, verify_admin_secret_key

# accounts = Blueprint('accounts', __name__)  # blueprint for auth routes

# @accounts.route('/accounts/register', methods=['POST'])
# def register():
#     """
#     Registers a new user to the database and returns a JWT (access token).
#     ---
#     tags:
#     - Accounts
#     parameters:
#     - name: User JSON object
#       in: body
#       required: true
#       description: A JSON object containing a username, password, and email. The optional *admin_secret* field is required to register a new admin user, allowing access to protected routes.
#       schema:
#         type: object
#         required:
#             - username
#             - password
#             - email
#         optional:
#             - admin_secret
#         properties:
#           username:
#             required: true
#             type: string
#             description: The username of the new user.
#             example: testuser
#           password:
#             required: true
#             type: string
#             description: The password of the new user.
#             example: testpassword
#           email:
#             required: true
#             type: string
#             description: The email address of the new user.
#             example: test@email.com
#           admin_secret:
#             required: false
#             type: string
#             description: The admin secret to register a new admin user.
#             example: optional_adminsecret
#     responses:
#       200:
#           description: User registered successfully, returns access token
#       400:
#           description: Invalid payload, username, password, and email required in request body
#       409:
#           description: Username already exists
#       500:
#           description: Internal server error
#     """

#     if request.method == 'POST':
#         data = request.get_json()
#         if not all(key in data.keys() for key in ['username', 'password', 'email']):
#              return {'error': 'Invalid payload, username, password, and email required in request body.'}, 400
#         try:
#             # ensure username and password are not empty
#             if data['username'] == '' or data['username'] == None or data['password'] == '' or data['password'] == None or data['email'] == '' or data['email'] == None:
#                 return {'error': 'Username, password, and email cannot be empty!'}, 400

#             # check if is_test_account is provided in request body
#             if 'is_test_account' not in data.keys(): is_test_account = False
#             else: is_test_account = data['is_test_account']

#             # check if username already exists
#             user = Users.query.filter_by(username=data['username']).first()

#             if user != None:
#                 return {'error': 'Username already exists!'}, 409
            
#             hashed_password = bcrypt.generate_password_hash(data['password']) # hash password
#             new_user = None

#             # if admin_secret is provided and correct, create admin user
#             if 'admin_secret' in data.keys():
#                 # check if the admin secret key is correct
#                 if verify_admin_secret_key(data['admin_secret']):
#                     new_user = Users(username=data['username'], password=hashed_password, # create new user
#                                      email=data['email'], is_admin=True, is_test_account=is_test_account)
#             # otherwise, create a normal user
#             if new_user == None:
#                 new_user = Users(username=data['username'], password=hashed_password, # create new user
#                              email=data['email'], is_test_account=is_test_account)
            
#             db.session.add(new_user)  # add new user to database
#             db.session.commit()       # commit changes to database
#             access_token = create_access_token(identity=new_user.UID)

#             return jsonify({'access_token': access_token, "admin_status": new_user.is_admin}), 200

#         except IntegrityError as ie:
#             return {'error': 'IntegrityError: Username already exists!'}, 409

#         except Exception as e:
#             return {'error': f"Exception {e}"}, 500
        
# @accounts.route('/accounts/delete_account', methods=['POST'])
# @jwt_required()
# def delete_account():
#     """
#     Deletes a user account from the database, requires a JWT for the user to be deleted.
#     ---
#     tags:
#     - Accounts
#     parameters:
#     - name: Authorization
#       in: header
#       required: true
#       description: "The JWT of the current user. The required header format is: **{'Authorization: Bearer {JWT}'}**"
#       example: Bearer <JWT_token>
#       schema:
#         type: object
#         properties:
#           access_token:
#             type: string
#             description: The access token of the user.
#             example: access_token
#     responses:
#       200:
#           description: User deleted successfully
#       404:
#           description: Unable to verify current user
#       500:
#           description: Internal server error
#     """
#     if request.method == 'POST':
#         try:
#             current_user_id = get_jwt_identity()
#             current_user = Users.query.filter_by(UID=current_user_id).first()  
#             if current_user == None:
#                 return {'error': 'Unable to verify current user!'}, 404
#             db.session.delete(current_user)
#             db.session.commit()
#             return {'message': 'Account deleted!'}, 200
        
#         except Exception as e:
#             print(e)
#             return {'error': str(e)}, 500

# @accounts.route('/accounts/protected/delete_all_accounts', methods=['POST'])
# @jwt_required()
# @requires_admin
# def delete_all_accounts():
#     """
#     Protected route to delete all accounts from the database. By default, this route will delete all non-admin accounts. If the query parameter **filter** is set to **test_accounts**, only test accounts will be deleted.
#     ---
#     tags:
#     - Accounts
#     parameters:
#     - name: Authorization
#       in: header
#       required: true
#       description: "The JWT of the current admin user. The required header format is: **{'Authorization: Bearer {JWT}'}**"
#       example: Bearer <JWT_token>
#       schema:
#         type: object
#         properties:
#           access_token:
#             type: string
#             description: The access token of the user.
#             example: access_token
#     responses:
#       200:
#           description: All non-admin accounts deleted
#       401:
#             description: Invalid request method
#       500:
#           description: Internal server error
#     """
#     if request.method == 'POST':
#         try:
#             # check to see if query parameter is provided
#             if request.get_json() != None:
#                 filter_by = request.get_json()['filter']
#                 if filter_by == 'test_accounts':
#                     # delete all test accounts
#                     db.session.query(Users).filter(Users.is_test_account == True).delete()
#                     db.session.commit()
#                     return {'status': 'success', 'message': 'All test accounts deleted!'}, 200
#                 elif filter_by == 'all':
#                     # delete all accounts that are not admin accounts
#                     db.session.query(Users).filter(Users.is_admin == False).delete()
#                     db.session.commit()
#                     return {'status': 'success', 'message': 'All non-admin accounts deleted!'}, 200
#                 else:
#                     return {'status': 'error', 'message': 'Invalid query parameter!'}, 400
#         except Exception as e:
#             print(e)
#             return {'status': 'error', 'message': str(e)}, 500
        
#     return {'status':'error', 'message': 'Invalid request method!'}, 401