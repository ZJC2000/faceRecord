# FILE: /faceRecord/faceRecord/main.py
from flask import Flask, render_template_string, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Time Recorder</title>
            <style>
              button {
                font-size: 20px;
                padding: 10px 20px;
                margin: 5px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>Record Time</h1>
              <button onclick="recordTime('clock-in')">上班</button>
              <button onclick="recordTime('clock-out')">下班</button>
              <button onclick="fetchTimes()">历史记录</button>
              <div id="output"></div>
              <div id="times"></div>
            </div>
            <script>
              function recordTime(action) {
                fetch('/record_time', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({action: action})
                })
                .then(response => response.json())
                .then(data => {
                  document.getElementById('output').innerText = data.time;
                });
              }

              function fetchTimes() {
                fetch('/fetch_times')
                .then(response => response.json())
                .then(data => {
                  let timesDiv = document.getElementById('times');
                  timesDiv.innerHTML = '<h2>Recorded Times</h2>';
                  data.times.forEach(row => {
                    timesDiv.innerHTML += `<p>${row[0]}: ${row[1]}</p>`;
                  });
                });
              }
            </script>
          </body>
        </html>
    ''')


@app.route('/record_time', methods=['POST'])
def record_time():
    data = request.get_json()
    action = data['action']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('times.csv', 'r') as csvfile:
        reader = list(csv.reader(csvfile))
    with open('times.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([action, current_time])
        writer.writerows(reader)
    return {'time': f'{action.capitalize()} time recorded at {current_time}'}



@app.route('/fetch_times', methods=['GET'])
def fetch_times():
    times = []
    with open('times.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        times = list(reader)
    return jsonify({'times': times})

if __name__ == '__main__':
    app.run(debug=True, port=5001)