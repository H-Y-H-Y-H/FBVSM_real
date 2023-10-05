from controller import *


def spiral_move():
    action_list = np.loadtxt('trajectory/spiral_cmds.csv')
    action_list = np.clip(action_list,-1,1)
    cmd0 = np.copy(action_list[0])
    act_cmds(cmd0 ,150)
    time.sleep(1)

    for i in range(0,len(action_list),2):
        if i <250:
            if i%5!=0:
                continue
        print(i)
        print(action_list[i])
        act_cmds(action_list[i],1000)
        time.sleep(0.3)


def cfp():
    action_list = np.loadtxt('trajectory/fcl_169_smooth.csv')
    action_list = np.clip(action_list,-1,1)


    # act_cmds([0,0,0,0] ,150)
    # time.sleep(1)   

    cmd0 = np.copy(action_list[0])
    act_cmds(cmd0 ,150)
    time.sleep(3)


    for i in range(len(action_list)):

        print(i)
        print(action_list[i])

        act_cmds(action_list[i],1000)

        time.sleep(1)
if __name__ == '__main__':

 
    cfp()

