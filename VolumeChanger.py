import cv2 as cv
import numpy as np
import time
import mediapipe as mp
import queue
import math
import threading
from HandDetector import HandDetector
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from comtypes import CLSCTX_ALL



class VolumeChanger:
    url = 'http://192.168.1.9:4747/video'

    def __init__(self,min_detection_confidence=0.5
                 ,min_tracking_confidence=0.5):

        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.hand_detector = HandDetector(min_detection=self.min_detection_confidence
                                          ,min_tracking=self.min_tracking_confidence)

        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.q = queue.Queue(maxsize=1)
        self.prev_vol = 0

    def get_frame(self):
        cap = cv.VideoCapture(self.url)
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                pass

            if self.q.empty():
                frame = cv.resize(frame,(1280,720))
                self.q.put(frame)
        time.sleep(0.01)
        cap.release()

    def process_frame(self):
        min_vol, max_vol, _ = self.volume.GetVolumeRange()
        rec_vol = 0
        vol_percentage = 0
        while True:
            if self.q.empty():
                time.sleep(0.01)
                continue

            frame = self.q.get()
            frame = self.hand_detector.find_hands(frame)
            lms = self.hand_detector.find_position(frame)

            if 4 in lms and 8 in lms:
                x1,y1 = lms[4]
                x2,y2 = lms[8]

                length = math.hypot(x2-x1,y2-y1)
                center_x = (x1+x2)//2
                center_y = (y1+y2)//2
                cv.line(frame,(x1,y1),(x2,y2),(255,0,255),2)

                if length < 50:
                    cv.circle(frame,(center_x,center_y),15,(0,255,55),cv.FILLED)
                vol = np.interp(length,[50,350],[min_vol,max_vol])

                smooth = 0.7 * self.prev_vol + 0.3 * vol
                self.prev_vol = vol
                vol_percentage = np.interp(smooth,[min_vol,max_vol],[0,100])
                rec_vol = np.interp(vol_percentage,[0,100],[650,290])


                self.volume.SetMasterVolumeLevelScalar(vol_percentage / 100,None)
                print(length)

            frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
            frame = cv.flip(frame, 1)
            cv.rectangle(frame, (10, 290), (80, 650), (0, 255, 0), 2)
            cv.rectangle(frame, (10, int(rec_vol)), (80, 650), (0, 255, 0), cv.FILLED)
            cv.putText(frame, f"{int(vol_percentage)} %",(10,250),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv

            cv.imshow('test',frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)

def main():
    vc = VolumeChanger()

    t1 = threading.Thread(target=vc.get_frame, daemon=True)
    t2 = threading.Thread(target=vc.process_frame, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    cv.destroyAllWindows()




if __name__ == '__main__':
    main()










