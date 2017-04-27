#!flask/bin/python
from flask import Flask, jsonify, request

from flask_cors import CORS, cross_origin

import MySQLdb

app = Flask(__name__)

CORS(app)



# numrows = int(cursor.rowcount)

# for x in range(0,numrows):
#     row = cursor.fetchone()
#     print row[1], "-->", row[2]


# users = [
#             {
#                 "userId": "RahulDev",
#                 "passCode": "123456789"
#             },
#             {
#                 "userId": "praveenDev",
#                 "passCode": "987654321"
#             },
#             {
#                 "userId": "praveenDev",
#                 "passCode": "987654321"
#             }
#         ]
success =   {
                'status': "Success",
                'errorDesc': "User details has been succesfully inserted",
                'statusCode': 200
            }

error = {
            'status': "Failure",
            'errorDesc': "User already have an account",
            'statusCode': 200
        }

# @app.route('/users', methods=['GET'])
# def get_users():
#     return jsonify({'users': users})

@app.route('/setuser', methods=['POST'])
def set_user():
    reqJson = request.get_json(force=True)
    print 'data from client:', reqJson
    db = MySQLdb.connect(host="localhost", user="root", passwd="Baba321gow.",db="sbw_db")
    cursor = db.cursor()
    cursor.execute("SELECT email FROM sbw_db.sbw_users")
    result_set = cursor.fetchall()
    print '====>', result_set
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



