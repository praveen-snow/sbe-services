#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import MySQLdb
app = Flask(__name__)
CORS(app)
success =   {
                'status': "Success",
                'errorDesc': "User details has been succesfully inserted"
            }

error = {
            'status': "Failure",
            'errorDesc': "User already have an account"
        }

db = MySQLdb.connect(host="localhost", user="root", passwd="Baba321gow.",db="sbw_db")
cursor = db.cursor()
@app.route('/user/signin', methods=['POST'])
def user_sigin():
    reqJson = request.get_json(force=True)
    #print 'data from client:', reqJson
    cursor.execute("SELECT email, passcode FROM sbw_db.sbw_users")
    result_set = cursor.fetchall()
    #print '====>', result_set
    user_exist = False
    for row in result_set:
        if reqJson['email'] == row[0] and reqJson['passcode'] == row[1]:
            dictToReturn = success
            dictToReturn['errorDesc'] = "User details found"
            break
        else:
            dictToReturn = error
            dictToReturn['errorDesc'] = "User details not found" 
    db.commit()
    return jsonify(dictToReturn)

@app.route('/user/signup', methods=['POST'])
def user_signup():
    reqJson = request.get_json(force=True)
    #print 'data from client:', reqJson
    cursor.execute("SELECT email FROM sbw_db.sbw_users")
    result_set = cursor.fetchall()
    # print '====>', result_set
    user_exist = False
    for row in result_set:
        if reqJson['email'] == row[0]:
            dictToReturn = error
            user_exist = True
            break
        else:
            user_exist = False
    if user_exist == False:
        cursor.execute("""INSERT INTO sbw_db.sbw_users (email, firstname, lastname, passcode)VALUES (%s, %s, %s, %s)""", (reqJson['email'], reqJson['firstName'], reqJson['lastName'], reqJson['passcode']))
        dictToReturn = success
    db.commit()
    return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(debug=True)



