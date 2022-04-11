import numpy
import socket
import threading
import time
import cv2
from datetime import datetime
import sys
import base64
import cvlib as cv
face_in_img = numpy.array([1,2,3])
class ClientSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_POR$
            self.connectCount = 0
            self.sendnumber()

        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            self.connectServer()

    def sendImages(self):
        global face_in_img
        global state
        state = False
        try:
            capture = cv2.VideoCapture(-1)
            while capture.isOpened():
                ret, frame = capture.read()
                face, confidence = cv.detect_face(frame)
                if confidence:
                    print(confidence)
                    if confidence[0] > 0.7:
                        for idx, f in enumerate(face):
                            f[1] = f[1]+(f[3]-f[1])//5
                            face_in_img = frame[f[1]:f[3], f[0]:f[2], :]

                        now = time.localtime()
                        stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

                        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                        result, imgencode = cv2.imencode('.jpg', face_in_img, encode_param)
                        data = numpy.array(imgencode)
                        stringData = base64.b64encode(data)
                        length = str(len(stringData))
                        self.sock.sendall(length.encode('utf-8').ljust(64))
                        self.sock.send(stringData)
                        self.sock.send(stime.encode('utf-8').ljust(64))
                        time.sleep(0.095)
                        break
            capture.release()
            cv2.destroyAllWindows()
            self.sendnumber()

        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()

    def sendnumber(self):
        try:
            Input = input('say temperature: ')
            self.sock.sendall(Input.encode('utf-8').ljust(64))
            self.sendImages()
        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendnumber()

def main():
    TCP_IP ='192.168.0.23'
    TCP_PORT = 8080
    client = ClientSocket(TCP_IP, TCP_PORT)

if __name__ == "__main__":
    main()

