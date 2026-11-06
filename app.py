from flask import Flask, request, render_template, send_file, jsonify
import os
import uuid
from crypto_engine import EyzAES

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # يدعم ملفات لحد 5 جيجا

UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    action = request.form.get('action')
    password = request.form.get('password', 'eyzzey') # الباسورد الافتراضي
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    file_id = str(uuid.uuid4())
    input_path = os.path.join(TEMP_FOLDER, f"{file_id}_in")
    output_path = os.path.join(TEMP_FOLDER, f"{file_id}_out")
    file.save(input_path)

    crypt = EyzAES(password)

    try:
        if action == 'encrypt':
            crypt.encrypt_file(input_path, output_path)
            out_name = file.filename + ".eyz"
        elif action == 'decrypt':
            crypt.decrypt_file(input_path, output_path)
            out_name = file.filename.replace(".eyz", "")
            if out_name == file.filename: out_name += ".decrypted"
        else:
            return jsonify({"status": "error", "message": "Invalid action"}), 400

        os.remove(input_path)
        return send_file(output_path, as_attachment=True, download_name=out_name)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("[*] EyzCrypt Enterprise Server running on http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)
