from LX16A import *
import numpy as np
import time
import cv2
import threading
import os
lx16_control = LX16A()

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(3)  # 0 for default camera
        self.frame = None
        self.lock = threading.Lock()
        self.is_running = True

        # Start the capture thread
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.start()

    def _capture_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            with self.lock:
                self.frame = frame

    def get_latest_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.cap.release()



def norm2act(cmds_):
    cmds = np.asarray(cmds_)
    assert ( cmds <= 1. ).all() and ( cmds >= -1. ).all(),\
        'ERROR: cmds wrong, should between -1 and 1'
    cmds[1:] *= -1
    cmds = cmds*(380) + 500 # +-60

    return cmds.astype(int)

def act_cmds(cmds_,speed=300):
    cmds = norm2act(cmds_)
    for i in range(10,14):
        lx16_control.moveServo(i,cmds[i-10],rate=speed)
    return cmds

def read_pos():
    pos = []
    for i in range(10,14):
        actual_pos = lx16_control.readPosition(i)
        norm_pos =(actual_pos-500)/380
        pos.append(norm_pos)
    
    return pos


if __name__ == '__main__':
    camera = Camera()

    save_path = '../data0923/'
    os.makedirs(save_path,exist_ok = True)

    #reset_pos = [-1.,-1.,0.,- 0.7]
    #act_cmds(reset_pos,speed =500)
    #time.sleep(5)

    print('start')
    action_list = np.loadtxt('cleaned_con_action_robo0_dof4_size20.csv')
    num_data = len(action_list)
    pos_list = []
    for a in range(50000,num_data):
        pos = [0.] * 4
        cmd = action_list[a]
        act_cmds(cmd)
        time.sleep(0.1)
        for i in range(50):
            pos = read_pos()
            time.sleep(0.2)
            
            error = abs(pos - cmd).sum()
            print(cmd, pos, error)

            if error<0.8:
                break
            else:
                print('moved %d setps'%i,'error:',error)

            if i == 49:
                quit()

        img = camera.get_latest_frame()
        if img is not None:
            img = img[:, 420:1500]
            img = cv2.resize(img, (540, 540))
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite(save_path +'/%06d.png'%a,img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        pos_list.append(pos)
        if a%10000 == 0:
            np.savetxt('log_pos0923.csv',pos_list)
            
    np.savetxt('log_pos0923.csv',pos_list)
            
    camera.stop()
    cv2.destroyAllWindows()

