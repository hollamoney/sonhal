import cv2
from flask import Flask, render_template, Response, request
import sqlite3
import json
import os.path
import sqlite3

app = Flask(__name__)
"""
camera = cv2.VideoCapture(0)
"""
"""
def generate_frames():
    while True:

        # read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame'
                   b'Content-Type: image/jpeg' + frame + b'')"""


"""@app.route('/')
def index():
    return render_template("dashboards_aside.html")"""


"""@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')"""


@app.route("/data.json")
def data():
    con = sqlite3.connect(r"C:\Users\U44295\vpvp.db")
    cursor = con.cursor()
    cursor.execute(" select * from data ")
    results = cursor.fetchall()
    con.commit()
    cursor.close()
    return json.dumps(results)


@app.route("/graph")
def graph():
    return render_template('graph.html')

@app.route("/dbvp")
def dbvp():
    return render_template('dbvp.html')


cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(
        debug=True,
        threaded=True,
        host='0.0.0.0'
    )