from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

app = Flask(__name__)
CORS(app)

# Abstract API Key
ABSTRACT_API_KEY = "3c50fae39ddc47c0b4a1a39cc209c877"

# Google Sheets credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ecstatic-moon-461104-h1-771c431d304b.json", scope)
client = gspread.authorize(creds)
sheet = client.open("parde_waitlist").sheet1

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"status": "error", "message": "Missing email"}), 400

    # Проверка email через Abstract API
    response = requests.get(
        "https://emailvalidation.abstractapi.com/v1/",
        params={"api_key": ABSTRACT_API_KEY, "email": email}
    )
    result = response.json()

    is_valid = result.get("is_valid_format", {}).get("value") and result.get("is_smtp_valid", {}).get("value")

    if is_valid:
        sheet.append_row([email])
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email"}), 400

if __name__ == '__main__':
    app.run(debug=True)
