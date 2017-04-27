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


users = [
            {
                "userId": "RahulDev",
                "passCode": "123456789"
            },
            {
                "userId": "praveenDev",
                "passCode": "987654321"
            },
            {
                "userId": "praveenDev",
                "passCode": "987654321"
            }
        ]
success =   {
                'status': "Success",
                'errorDesc': "User verified",
                'statusCode': 200
            }

error = {
            'status': "errored",
            'errorDesc': "User not verified",
            'statusCode': 200
        }

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/setuser', methods=['POST'])
def set_user():
    db = MySQLdb.connect(host="localhost", user="root", passwd="Baba321gow.",db="sbw_db")
    cursor = db.cursor()
    cursor.execute("SELECT passCode, userId FROM sbw_db.sbw_users")
    db.commit()
    result_set = cursor.fetchall()
    reqJson = request.get_json(force=True)
    print 'data from client:', reqJson
    for row in result_set:
        print row[0] ,'---->', row[1]
        if reqJson['userId'] == row[1] and reqJson['passCode'] == row[0]:
            dictToReturn = success
            break
        else:
            dictToReturn = error
    return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(debug=True)



