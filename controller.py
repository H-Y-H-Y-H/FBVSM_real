from LX16A import *
import numpy as np

lx16_control = LX16A()

def norm_act(cmds_):
    cmds = np.asarray(cmds_)
    assert ( cmds <= 1. ).all() and ( cmds >= -1. ).all(),\
        'ERROR: cmds wrong, should between -1 and 1'
    cmds[1:] *= -1
    cmds = cmds*((870-130)/3) + 500 # +-60

    return cmds.astype(int)

def act_cmds(cmds_):
    cmds = norm_act(cmds_)
    for i in range(10,14):
        lx16_control.moveServo(i,cmds[i-10],rate=100)

def read_pos():
    pos = []
    for i in range(12):
        pos.append(lx16_control.readPosition(i+10))
    return pos

if __name__ == '__main__':

    reset_pos = [0.]*4

    act_cmds(reset_pos)
