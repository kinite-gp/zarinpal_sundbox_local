from flask import Flask, request, jsonify, render_template
import string
import random
import json

app = Flask(__name__, template_folder='templates')

pays = {}



@app.route('/pg/services/WebGate/wsdl', methods=['POST'])
def post_data():
    global pays
    req_data = request.get_json()
    authority = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(36))
    if 'MerchantID' in req_data and 'Amount' in req_data and 'Description' in req_data and "CallbackURL" in req_data:
        pays[authority] = {
                "MerchantID": req_data["MerchantID"],
                "Amount": req_data["Amount"],
                "Description": req_data["Description"],
                "CallbackURL": req_data["CallbackURL"]
            }
        req_data = {
            "Status": 100,
            "Authority": f"{authority}",
        }
        return jsonify(req_data)
    else:
        req_data = {
            "Status": -200,
            "Authority": "",
        }
        return jsonify(req_data)

@app.route('/pg/StartPay/<string:authority>', methods=['POST'])
def custom_url(authority):
    global pays

    return render_template("template.html", data=pays[authority])




if __name__ == '__main__':
    app.run(debug=True, port=8888)
