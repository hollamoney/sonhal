import cv2
import numpy as np
import imutils
import datetime
import sqlite3
from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lb = np.array([0, 0, 248])
    ub = np.array([93, 20, 255])

    mask = cv2.inRange(hsv, lb, ub)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    thresh = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)[1]
    imgBlur = cv2.GaussianBlur(thresh, (5, 5), 1)

    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgBlur, kernel, iterations=3)
    imgThre = cv2.erode(imgDial, kernel, iterations=2)

    cnts = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)


    def find_contours(cnts):
        areas = []
        for cnt in cnts:
            cont_area = cv2.contourArea(cnt)
            if cont_area > 500:
                areas.append(cont_area)

        return areas


    from time import sleep

    sorted_contours = sorted(cnts, key=cv2.contourArea, reverse=True)
    bosch = 1
    jq = 2


    def hello(name):
        try:
            if len(sorted_contours) >= 2 and int(
                    find_contours(sorted_contours)[0] + find_contours(sorted_contours)[1]) >= 10000:
                dt_now = datetime.datetime.now()
                print(int(find_contours(sorted_contours)[0] + find_contours(sorted_contours)[1]))
                print(dt_now)
                con = sqlite3.connect("vpvp.db", check_same_thread=False)
                cursor = con.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS Data (alan INT,tarih TIMESTAMP,id INT)")
                cursor.execute("INSERT INTO Data VALUES(?,?,?)",
                               ((int(find_contours(sorted_contours)[0] + find_contours(sorted_contours)[1]),
                                 dt_now, jq)))
                con.commit()
            else:
                dt_now = datetime.datetime.now()
                print(int("0"))
                print(dt_now)
                con = sqlite3.connect("vpvp.db", check_same_thread=False)
                cursor = con.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS Data (alan INT,tarih TIMESTAMP,id INT)")
                cursor.execute("INSERT INTO Data VALUES(?,?,?)",
                               ((0,
                                 dt_now, bosch)))
                con.commit()
        except IndexError:
            dt_now = datetime.datetime.now()
            print(int("0"))
            print(dt_now)
            con = sqlite3.connect("vpvp.db", check_same_thread=False)
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Data (alan INT,tarih TIMESTAMP,id INT)")
            cursor.execute("INSERT INTO Data VALUES(?,?,?)",
                           ((0,
                             dt_now, bosch)))
            con.commit()


    rt = RepeatedTimer(1, hello, "World")
    for sc in sorted_contours[0:2]:
        cv2.drawContours(frame, [sc], -1, (0, 0, 255), 3)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1000)
    try:
        sleep(1),
    finally:
        rt.stop()

cap.release()
cv2.desteroyAllWindows()