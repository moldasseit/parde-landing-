from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с любого домена

# Настройка доступа к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ecstatic-moon-461104-h1-771c431d304b.json", scope)
client = gspread.authorize(creds)
sheet = client.open("parde_waitlist").sheet1  # имя Google Sheets файла

@app.route('/submit', methods=['POST'])
def submit_phone():
    data = request.get_json()
    phone = data.get('phone')
    if not phone:
        return jsonify({"status": "error", "message": "No phone number provided"}), 400

    sheet.append_row([phone])
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)