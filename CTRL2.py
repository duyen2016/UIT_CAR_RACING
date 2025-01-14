
from controller import Robot
from controller import Motor
from controller import DistanceSensor
from controller import Camera
from controller import LED
from controller import Supervisor
import math
robot = Robot()

# get the time step of the current world
timestep = 8
robot.step(timestep)

#camera     
cam = robot.getDevice("camera")
cam.enable(64)
# Leff motor, Right motor   
lm = robot.getDevice("left wheel motor")
lm.setPosition(float("inf"))
lm.setVelocity(0)

rm = robot.getDevice("right wheel motor")
rm.setPosition(float("inf"))
rm.setVelocity(0)

# Sensors
NB_GROUND_SENS = 8
gs = []
gsNames = [
    'gs0', 'gs1', 'gs2', 'gs3',
    'gs4', 'gs5', 'gs6', 'gs7'
]
for i in range(NB_GROUND_SENS):
    gs.append(robot.getDevice(gsNames[i]))
    gs[i].enable(timestep)

# Waiting for completing initialization
### thí sinh không được bỏ phần này
initTime = robot.getTime()
while robot.step(timestep) != -1:
    if (robot.getTime() - initTime) * 1000.0 > 200:
        break

### Phần code cần chỉnh sửa cho phù hợp ##
# Định nghĩa các tín hiệu của xe
NOP = -3
MID = 0
LEFT = 1
RIGHT = -1
LEFT_VUONG = 4
RIGHT_VUONG = -4
LEFT_MID = 5
RIGHT_MID = -5
FULL_SIGNAL  = 2
BLANK_SIGNAL = -2

# MAX_SPEED <= 1000
MAX_SPEED = 40
threshold = [330, 330, 330, 330, 330, 330, 330, 330]
preFilted = 0b00000000

# Biến lưu giá trị tỉ lệ tốc độ của động cơ
left_ratio = 0.0
right_ratio = 0.0

# Hàm đọc giá trị của sensors
def ReadSensors():
    gsValues = []
    filted = 0x00
    for i in range(NB_GROUND_SENS):
        gsValues.append(gs[i].getValue())
        if gsValues[i] > threshold[i]:
            filted |= (0x01 << (NB_GROUND_SENS - i - 1))
    #print(gs[7].getValue(), sep = '\t')
    return filted

# Phần code điều khiển xe
def DeterminePosition(filted):
    if filted == 0b11100111:
        return MID
    elif (str_filted[0] == '0' and str_filted[5:8] == '111'): #or filted == 0b10000111 or str_filted[:4] == '0':
        return LEFT_VUONG
    elif (str_filted[4:8] == '1111' and str_filted[:4] != '1111') or filted == 0b10000111:
        return LEFT
    elif ((str_filted[7] == '0') and (str_filted[:3] == '111')):# or filted == 0b11100001 or str_filted[3:8] == '0':
        return RIGHT_VUONG
    elif ((str_filted[:4] == '1111') and (str_filted[4:8] != '1111')) or filted == 0b11100001:
        return RIGHT
    elif filted == 0b11111111 or filted == 0b11101111 or filted == 0b11110111:
        return FULL_SIGNAL
    elif filted == 0b00000000:
        return BLANK_SIGNAL
    return NOP

#các hàm điều khiển xe di chuyển
def GoStraight(filted):
    lm.setVelocity(1 * MAX_SPEED)
    rm.setVelocity(1 * MAX_SPEED)

def TurnLeft(filted):
    if filted == 0b11101111:
        lm.setVelocity(0.866 * MAX_SPEED)
        rm.setVelocity(1.0 * MAX_SPEED)
        print('left lil')
    elif filted == 0b11001111:
        lm.setVelocity(0.707 * MAX_SPEED)
        rm.setVelocity(1.0 * MAX_SPEED)
        print('left med')
    elif filted == 0b10011111:
        lm.setVelocity(0.5 * MAX_SPEED)
        rm.setVelocity(1.0 * MAX_SPEED)
        print('left big')
    lm.setVelocity(0.5 * MAX_SPEED)
    rm.setVelocity(1.0 * MAX_SPEED)

def TurnRight(filted):
    if filted == 0b11110111:
        lm.setVelocity(1.0 * MAX_SPEED)
        rm.setVelocity(0.866 * MAX_SPEED)
        print('right lil')
    elif filted == 0b11110011:
        lm.setVelocity(1.0 * MAX_SPEED)
        rm.setVelocity(0.707 * MAX_SPEED)
        print('right med')
    elif filted == 0b11111001:
        lm.setVelocity(1.0 * MAX_SPEED)
        rm.setVelocity(0.5 * MAX_SPEED)
        print('right big')
    lm.setVelocity(1.0 * MAX_SPEED)
    rm.setVelocity(0.5 * MAX_SPEED)
    return 1.0, 0.5

def TurnRightVuong():
    lm.setVelocity(1 * MAX_SPEED)
    rm.setVelocity(0.15 * MAX_SPEED)
    while robot.step(timestep) != -1:
        filted = ReadSensors()
        pos = DeterminePosition(filted)
        if pos == MID:
            NgaTuRight_Signal = False
            return
def TurnLeftVuong():
     lm.setVelocity(0.15 * MAX_SPEED)
     rm.setVelocity(1 * MAX_SPEED)
     while robot.step(timestep) != -1:
        filted = ReadSensors()
        pos = DeterminePosition(filted)
        if pos == MID:
            NgaTuLeft_Signal = False
            return
def TurnLeftMid():
    lm.setVelocity(0.5 * MAX_SPEED)
    rm.setVelocity(1 * MAX_SPEED)
    while robot.step(timestep) != -1:
        filted = ReadSensors()
        pos = DeterminePosition(filted)
        if pos == MID:
            return

def TurnRightMid():
    lm.setVelocity(1 * MAX_SPEED)
    rm.setVelocity(0.5 * MAX_SPEED)
    while robot.step(timestep) != -1:
        filted = ReadSensors()
        pos = DeterminePosition(filted)
        if pos == MID:
            return
def NgaTuLeft():
    for i in range(51):
        robot.step(timestep)
        lm.setVelocity(0.15 * MAX_SPEED)
        rm.setVelocity(1 * MAX_SPEED)
def NgaTuRight():
    for i in range(51):
        robot.step(timestep)
        lm.setVelocity(1 * MAX_SPEED)
        rm.setVelocity(0.15 * MAX_SPEED)
def VongXuyen():
    for i in range(48):
        robot.step(timestep)
        lm.setVelocity(1 * MAX_SPEED)
        rm.setVelocity(0.15 * MAX_SPEED)

lastPos = 0  
NgaTuLeft_Signal = False
NgaTuRight_Signal = False
VongXuyen_Signal = False
BLANK_SIGNAL_COUNTER = 0
# Main loop:
# Chương trình sẽ được lặp lại vô tận 
while robot.step(timestep) != -1:
    filted = ReadSensors()
    #pos: position - vị trí của xe
    str_filted = (str(bin(filted))[2:]).zfill(8)
    pos = DeterminePosition(filted)
    # In ra màn hình giá trị của filted ở dạng nhị phân
    print('Position: ' + str(format(filted, '08b')), sep = '\t')
    if pos == MID and lastPos == MID:
        GoStraight(filted)
        print('straight')
    elif preFilted == 0b00000000 and filted != 0b00000000:
        if NgaTuRight_Signal:
            for i in range(10):
                robot.step(timestep)
                lm.setVelocity(1 * MAX_SPEED)
                rm.setVelocity(0.15 * MAX_SPEED)
            TurnRightVuong()
            print('RE NGA TU R')
            NgaTuRight_Signal = False 
            VongXuyen_Signal = False
            BLANK_SIGNAL_COUNTER = 0
            print('right 4')
        elif NgaTuLeft_Signal:
            for i in range(10):
                robot.step(timestep)
                lm.setVelocity(0.15 * MAX_SPEED)
                rm.setVelocity(1 * MAX_SPEED)
            TurnLeftVuong()
            print('RE NGA TU L')
            NgaTuLeft_Signal = False
            VongXuyen_Signal = False 
            BLANK_SIGNAL_COUNTER = 0
            print('left 4')
        else:
            VongXuyen_Signal = True 
    elif (filted == 0b00111100 or filted == 0b00011000 or filted == 0b01111110 or filted == 0b11000011) and VongXuyen_Signal:
        for i in range(10):
            robot.step(timestep)
            lm.setVelocity(0.15 * MAX_SPEED)
            rm.setVelocity(1 * MAX_SPEED)
        TurnRightVuong()
        print('vong xoay')
    elif (filted == 0b11100001 or filted == 0b11000001) and VongXuyen_Signal:
        for i in range(10):
            robot.step(timestep)
            lm.setVelocity(1 * MAX_SPEED)
            rm.setVelocity(0.15 * MAX_SPEED)
        TurnRightVuong()
        VongXuyen_Signal = False 
        BLANK_SIGNAL_COUNTER = 0 
        NgaTuLeft_Signal = False
        NgaTuRight_Signal = False
    elif lastPos == LEFT_VUONG and filted == 0b11111111:# or filted == 0b01111111 or filted == 0b11111110):
        print('left vuong')
        TurnLeftVuong()
    elif lastPos == RIGHT_VUONG and filted == 0b11111111:# or filted == 0b01111111 or filted == 0b11111110):
        print('right vuong')
        TurnRightVuong() 
    elif lastPos == MID and filted == 0b11110011:
        print('right mid')
        TurnRightMid()
    elif lastPos == MID and filted == 0b11001111:
        print('left mid')
        TurnLeftMid() 
    elif pos == RIGHT:
        TurnRight(filted)
    elif pos == LEFT:
        TurnLeft(filted)  
    elif BLANK_SIGNAL_COUNTER >= 30:
        lm.setVelocity(0 * MAX_SPEED)
        rm.setVelocity(0 * MAX_SPEED)     
    else:  
        lm.setVelocity(1 * MAX_SPEED)
        rm.setVelocity(1 * MAX_SPEED) 
    if (lastPos == LEFT_VUONG or preFilted == 0b00000111) and pos != FULL_SIGNAL and pos != LEFT_VUONG and (pos == MID or filted == 0b11110111 or filted == 0b11101111):
        NgaTuLeft_Signal = True
    elif (lastPos == RIGHT_VUONG or preFilted == 0b11100000) and pos != FULL_SIGNAL and pos != RIGHT_VUONG and (pos == MID or filted == 0b11101111 or filted == 0b11110111):
        NgaTuRight_Signal = True
    if pos == BLANK_SIGNAL:
        BLANK_SIGNAL_COUNTER += 1
    print('right NT', NgaTuRight_Signal)
    print('left NT', NgaTuLeft_Signal)
    print('Vong xuyen: ', VongXuyen_Signal)
    print('Signal BL: ', str(BLANK_SIGNAL_COUNTER))
    preFilted = filted
    lastPos = pos
    print('-----------------------------')
    pass
