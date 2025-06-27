from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)

# Google Sheets credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ecstatic-moon-461104-h1-771c431d304b.json", scope)
client = gspread.authorize(creds)
sheet = client.open("parde_waitlist").sheet1

# Serve index.html from templates
@app.route('/')
def home():
    return render_template("index.html")

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    number = data.get("phone")
    if number:
        sheet.append_row([number])
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Missing phone"}), 400

if __name__ == '__main__':
    app.run(debug=True)
