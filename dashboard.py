from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)

API_URL = "http://localhost:5000"
app.config['SECRET_KEY'] = 'oreoluwatitans'

@app.route("/")
def dashboard():
    try:
        response = requests.get(f"{API_URL}/data")
        data = response.json() if response.status_code == 200 else []

        if isinstance(data, dict) and 'data' in data:
            data = data['data']
    except Exception as e:
        data = []
        flash('Error loading data from server')
    return render_template("dashboard.html", data=data)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file part in request', 'error')
            return redirect(url_for('dashboard'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('dashboard'))

        file.stream.seek(0)
        temp_path = os.path.join('temp_upload', file.filename)
        os.makedirs('temp_upload', exist_ok=True)
        file.save(temp_path)

        with open(temp_path, 'rb') as f:
            files = {'file': (file.filename, f, file.mimetype)}
            response = requests.post(
                f"{API_URL}/upload",
                files=files,
                timeout=30
            )

        print(f"API Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            flash('Upload successful!', 'success')
        else:
            error = response.json().get('error', 'Unknown error')
            flash(f'Upload failed: {error}', 'error')

    except Exception as e:
        print(f"Upload error: {str(e)}")
        flash(f'Upload error: {str(e)}', 'error')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)