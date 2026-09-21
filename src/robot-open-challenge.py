from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.robotics import Car
from pupremote_hub import PUPRemoteHub
from pybricks.tools import multitask, run_task, wait

import gc

hub = PrimeHub()

# Set up motors
rear = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steer = Motor(Port.C, Direction.COUNTERCLOCKWISE)

# Initialize the sensor
eyesR = UltrasonicSensor(Port.F)
eyesL = UltrasonicSensor(Port.E)
colorF = ColorSensor(Port.A)

# OpenMV camera
p = PUPRemoteHub(Port.D)
p.add_command("msg", to_hub_fmt="repr", from_hub_fmt="repr")
p.add_channel('cam', to_hub_fmt='bhhb')

hub.imu.reset_heading(0)
wait(500)

car = Car(steer, rear, 100)
wait(500)

targetDist = 100
sum_error = 0
prev_error = 0
prev_error_h = 0 # for gyro PID
prev_error_C = 0
error = 0

sum_Gerror = 0
prev_Gerror = 0
sum_Rerror = 0 
prev_Rerror = 0

sumS_error = 0
prevS_error = 0

sumH_error = 0
prevH_error = 0

last_Cerror_Cor = 0

distListR = [0, 0, 0]
distListL = [0, 0, 0]
distListF = [0, 0, 0]

num_turn = 1
max_steer = 20
direction = 0

drive_power = 0.0
compensation = 0.0
lineColor = 0

can_sense_corner = False

rob_data = {"color": 0, 
            "block_x": 0, 
            "block_y": 0, 
            "corner": 0, 
            "heading": 0, 
            "ultra_R": 0,
            "ultra_L": 0,
            "line_color": 0 }

steer = 0
speed = 0
steer_center = 0
speed_center = 0
steer_wall = 0
speed_wall = 0

steer_sequence = 0 
speed_sequence = 0

is_sequencing = False

# retrieve samples to stabilize the inputs from the ultrasonic sensors
async def getMedianR(samples):
    i = 0
    while i < samples:
        distListR[i] = await eyesR.distance()
        i += 1
    
    distListR.sort()
    n = len(distListR)
    mid = n // 2 # median of the 3 samples

    if n % 2 == 1: # if odd number of samples, return information 
        return distListR[mid]
    else: # if even number, find average then return information 
        return (distListR[mid-1] + distListR[mid]) / 2

async def getMedianL(samples):
    i = 0
    while i < samples:
        distListL[i] = await eyesL.distance()
        i += 1
    
    distListL.sort()
    n = len(distListL)
    mid = n // 2

    if n % 2 == 1:
        return distListL[mid]
    else:
        return (distListL[mid-1] + distListL[mid]) / 2

# detecting blue and orange lines
async def getLineColor():
    lineColor = 0
    hsv = await colorF.hsv()
    if (hsv[0] < 45 or (hsv[0] < 370 and hsv[0]> 300)) and hsv[1] > 40: # orange
        lineColor = 1  # orange
    elif (hsv[0] > 200 and hsv[0] < 300) and hsv[1] > 30: # blue
        lineColor = 2  # blue
    else:
        lineColor = 0  # white
    return lineColor

async def remote_engine():
    while True:
        # connects hub to the camera and relay information
        await p.process_async()
        # A tiny wait is necessary to let other tasks in
        await wait(1)

# updates information from camera and sensors
async def update_robot_data():
    global rob_data
    
    while True:
        # This is specifically designed for Pybricks multitasking.
        result = await p.call_multitask("cam")
        
        if result:
            # Unpack the tuple directly from the result
            color, block_x, block_y, corner = result 
            
            heading = hub.imu.heading()
            lineColor = await getLineColor()
            us_R = await getMedianR(3)
            us_L = await getMedianL(3)

            rob_data['color'] = color
            rob_data['block_x'] = block_x
            rob_data['block_y'] = block_y
            rob_data['corner'] = corner
            rob_data['heading'] = heading
            rob_data['ultra_R'] = us_R
            rob_data['ultra_L'] = us_L
            rob_data['line_color'] = lineColor
            
        await wait(20) # Increased to 20ms to give the connection 'breathing room'

# pid for smooth, controlled turns
def turn90_pid(num_turn, kp=35, ki=0.000001, kd=1.0, forward=False, maxP=1100, minP=400):
    global sumS_error, prevS_error
    global speed_sequence

    maxS = maxP
    minS = minP
    steer_error = abs((90 * (num_turn)) - abs(rob_data['heading']))
    prop = kp * steer_error # proportional
    
    sumS_error += steer_error
    integral = ki * sumS_error # integral

    if integral > 10.0:
        integral = 10.0

    derivative = kd * (steer_error - prevS_error) # derivative

    compensation = prop + integral + derivative

    prevS_error = steer_error
    
    if compensation > maxS:
        compensation = maxS
    elif compensation < minS:
        compensation = minS
    
    if forward:
        speed_sequence = compensation
    else:
        speed_sequence = -compensation

# signal to turn after detecting corner wall
async def detect_corner():
    global num_turn, direction
    global rob_data, steer_sequence, speed_sequence, is_sequencing
    global can_sense_corner
    global sum_error, prev_error

    while True:
        error = rob_data['ultra_R'] - rob_data['ultra_L']
        
        if can_sense_corner == True and abs(error) > 800 and not is_sequencing:
            is_sequencing = True
        
            rear.reset_angle(0)
            while rear.angle() < 50:
                await heading_pid_corner(speed=400)
                await wait(10)
            else:
                await hub.speaker.beep(900, 100)
    
            if direction == -1:
                steer_sequence = -80 # left turn
            elif direction == 1:
                steer_sequence = 80 # right turn

            # reduce the turn amount to stop momentum from increasing the turn
            while abs(rob_data['heading']) < (90 * num_turn - 14):
                turn90_pid(num_turn, forward=True, maxP=900, minP=300)                
                await wait(10)
            num_turn += 1
            
            rear.reset_angle(0)
            while rear.angle() < 600:
                await heading_pid_corner()
                await wait(10)
            else:
                await hub.speaker.beep(900, 100)
            
            # crucial for knowing how many laps the robot did
            steer_sequence = 0
            speed_sequence = 0

            sum_error = 0 
            prev_error = 0

            is_sequencing = False
            can_sense_corner = False

        await wait(50)
    
async def heading_pid_corner(speed=1000):
    kp = 1.5
    kd = 20.0
    global last_Cerror_Cor, num_turn, direction
    global steer_sequence, speed_sequence, is_sequencing

    is_sequencing = True

    current_angle = hub.imu.heading()
    target_heading = (90 * (num_turn - 1)) * direction
    error =  target_heading - current_angle

    # Calculate derivative (rate of change)
    derivative = error - last_Cerror_Cor
    
    # Calculate PD steering output
    steering = (error * kp) + (derivative * kd)
    # Update last_error for the next iteration
    last_Cerror_Cor = error
    steer_sequence = steering
    speed_sequence = speed
    # Brief sleep to yield execution to other async tasks
    await wait(10)

async def heading_pid_corner_c(speed=1000):
    kp = 2.5
    kd = 20.0
    global last_Cerror_Cor, num_turn, direction
    global steer_sequence, speed_sequence, is_sequencing

    is_sequencing = True

    current_angle = hub.imu.heading()
    target_heading = (90 * (num_turn - 1)) * direction
    error =  target_heading - current_angle

    # Calculate derivative (rate of change)
    derivative = error - last_Cerror_Cor
    
    # Calculate PD steering output
    steering = (error * kp) + (derivative * kd)
    # Update last_error for the next iteration
    last_Cerror_Cor = error
    car.steer(steering)
    car.drive_speed(speed)
    # Brief sleep to yield execution to other async tasks
    await wait(10)

# pid to have a straight movement
async def ultrasonic_PID(kp=0.075, ki=0.000001, kd=100.0, minPower=1100, maxPower=1500):
    
    global sum_error, prev_error, max_steer, direction, num_turn
    global rob_data, steer_center, speed_center, error

    drive_power = 0.0
    compensation = 0.0
    
    while num_turn <= 12:  
        # after 3 laps, pid stops   
        error = rob_data['ultra_R'] - rob_data['ultra_L']    
            
        prop = kp * error # proportional
        
        sum_error += error
        integral = ki * sum_error # integral

        if integral > 10.0:
            integral = 10.0

        derivative = kd * (error - prev_error) # derivative

        compensation = prop + integral + derivative

        prev_error = error

        # negative steer = steer to the left
        # positive steer = steer to the right
        
        if compensation > max_steer:
            compensation = max_steer
        elif compensation < -max_steer:
            compensation = -max_steer
        
        maxP = maxPower
        minP = minPower
        max_error = 2000
        
        # cap the steering of the robot 
        if error > max_error:
            error = max_error
        elif error < 0:
            error = 0

        # adjust speed depending on the error - bigger the error, slower the movement and vice versa
        drive_power = -(maxP - minP) * (error - max_error) / max_error + minP   
        
        steer_center = compensation
        speed_center = drive_power               
        
        await wait(50)
    
    # set speed to 0 to stop robot from moving
    speed_center = 0

async def ultrasonic_PID_gyro(kp=0.075, ki=0.000001, kd=100.0, minPower=900, maxPower=1100, kp_ang=0.75, kd_ang=1.0):
    
    global sum_error, prev_error, max_steer, direction, num_turn
    global rob_data, steer_center, speed_center, error

    global prev_error_h

    drive_power = 0.0
    compensation = 0.0
    
    while num_turn <= 12:  
        # after 3 laps, pid stops   
        error = rob_data['ultra_R'] - rob_data['ultra_L'] 
        error_h = ((num_turn-1) * 90 * direction) - hub.imu.heading() 

            
        prop = kp * error # proportional
        
        sum_error += error
        integral = ki * sum_error # integral

        if integral > 10.0:
            integral = 10.0

        derivative = kd * (error - prev_error) # derivative

        
        compensation = prop + integral + derivative
        prev_error = error

        if abs(compensation) < 15.0: # if steering is relatively centered, switch to gyro PID
            compensation = kp_ang*error_h + kd_ang*(error_h - prev_error_h)
            prev_error_h = error_h

        # negative steer = steer to the left
        # positive steer = steer to the right
        
        if compensation > max_steer:
            compensation = max_steer
        elif compensation < -max_steer:
            compensation = -max_steer
        
        maxP = maxPower
        minP = minPower
        max_error = 2000
        
        # cap the steering of the robot 
        if error > max_error:
            error = max_error
        elif error < 0:
            error = 0

        # adjust speed depending on the error - bigger the error, slower the movement and vice versa
        drive_power = (-(maxP - minP) * (error - max_error) / max_error + minP)

        if abs(compensation) > 15.0: # if steering is relatively centered, switch to gyro PID
            drive_power *= 0.5

        print("compensation:", compensation)
        
        steer_center = compensation
        speed_center = drive_power              
        
        await wait(50)
    
    # set speed to 0 to stop robot from moving
    speed_center = 0

async def ultrasonic_PID_C(kp=6.0, ki=0.000001, kd=100.0, minPower=900, maxPower=1100):
    
    global sum_error, prev_error_C, max_steer, direction, num_turn
    global rob_data, steer_center, speed_center, error

    drive_power = 0.0
    compensation = 0.0
    
    error = rob_data['ultra_R'] - rob_data['ultra_L']    
        
    prop = kp * error # proportional
    
    sum_error += error
    integral = ki * sum_error # integral

    if integral > 10.0:
        integral = 10.0

    derivative = kd * (error - prev_error) # derivative

    compensation = prop + integral + derivative

    prev_error_C = error

    # negative steer = steer to the left
    # positive steer = steer to the right
    
    if compensation > max_steer:
        compensation = max_steer
    elif compensation < -max_steer:
        compensation = -max_steer
    
    maxP = maxPower
    minP = minPower
    max_error = 2000
    
    # cap the steering of the robot 
    if error > max_error:
        error = max_error
    elif error < 0:
        error = 0

    # adjust speed depending on the error - bigger the error, slower the movement and vice versa
    drive_power = -(maxP - minP) * (error - max_error) / max_error + minP   
    
    steer_center = compensation
    speed_center = drive_power  


            
    
    await wait(50)

async def sense_line_color():
    global can_sense_corner, direction

    while True:
        # can_sense_corner allows the robot to turn at the corner
        if rob_data['line_color'] == 1 and (direction == 0 or direction == 1): # orange clockwise
            can_sense_corner = True
            direction = 1
            await hub.speaker.beep(100)
        elif rob_data['line_color'] == 2 and (direction == 0 or direction == -1): # blue counter-clockwise
            can_sense_corner = True
            direction = -1
            await hub.speaker.beep(100)
        
        await wait(20)

# changes the speed and steer controller depending on situation
async def motor_controller():
    global rob_data, steer, speed, is_sequencing
    global steer_center, speed_center
    global steer_sequence, speed_sequence

    while True:
        if is_sequencing:
            steer = steer_sequence 
            speed = speed_sequence          
        elif rob_data['block_x'] == 0:
            steer = steer_center
            speed = speed_center 
            
        car.steer(steer)
        car.drive_speed(speed)
        
        await wait(50)

def steer_to_center2(target, error, kp=2.0, ki=0.000001, kd=10.0, max_steer=80):
    
    global sumH_error, prevH_error, steer_sequence, speed_sequence

    h_error = error
    prop = kp * h_error 
    sumH_error += h_error
    integral = ki * sumH_error 
    if integral > 10.0: 
        integral = 10.0
    elif integral < -10.0: 
        integral = -10.0
    derivative = kd * (h_error - prevH_error) 
    compensation = prop + integral + derivative
    prevH_error = h_error
    
    if compensation > max_steer: 
        compensation = max_steer
    elif compensation < -max_steer: 
        compensation = -max_steer
    
    steer_sequence = compensation
    speed_sequence = 700

async def straighten_heading(gyro_angle_correct=20):

    global num_turn, direction
    global rob_data, steer_sequence, speed_sequence, is_sequencing, can_sense_corner
    global sumH_error, prevH_error
    
    while True:
        if direction == 0: # when there is no defined direction yet (first section)
            temp_direction = 1
        else:
            temp_direction = direction

        target = (90 * (num_turn - 1)) * temp_direction
        error = target - hub.imu.heading()

        if abs(error) > gyro_angle_correct and not is_sequencing:
            is_sequencing = True
            sumH_error = 0 
            prevH_error = 0
            while abs(error) > 2.0 and not can_sense_corner:
                steer_to_center2(target, error, kp=2.0, ki=0.000001, kd=1.0, max_steer=40)
                error = target - hub.imu.heading()
                await wait(50)

            await hub.speaker.beep()
            is_sequencing = False
            
        await wait(50)



# back to starting position after last turn
async def UltrasonicPID_2Sensor_C(num_turn, kp=0.075, ki=0.000001, kd=10000, max_steer=20, gyro_angle_correct=25, with_gyro=False):
    global sum_error, prev_error, direction, drive_power, compensation 

    error = await getMedianR(3) - await getMedianL(3)
    
    if with_gyro:
        if hub.imu.heading() > gyro_angle_correct + (90 * (num_turn-1)):
            while hub.imu.heading() > gyro_angle_correct//2 + (90 * (num_turn-1)):
                steer_to_center(num_turn, kp=kp, ki=ki, kd=kd, turn=1)
                car.drive_speed(1100)
                await wait(1)
            
        if hub.imu.heading() < -gyro_angle_correct - (90 * (num_turn-1)):
            while hub.imu.heading() < -gyro_angle_correct//2 -(90 * (num_turn-1)):
                steer_to_center(num_turn, kp=kp, ki=ki, kd=kd, turn=2)
                car.drive_speed(1100)
                await wait(1)
        
    prop = kp * error # proportional
    
    sum_error += error
    integral = ki * sum_error # integral

    if integral > 10.0:
        integral = 10.0

    derivative = kd * (error - prev_error) # derivative

    compensation = prop + integral + derivative

    prev_error = error

    if compensation > max_steer:
        compensation = max_steer
    elif compensation < -max_steer:
        compensation = -max_steer
        
    car.steer(compensation)

    maxP = 1100
    minP = 900
    max_error = 2000
    
    if error > max_error:
        error = max_error
    elif error < 0:
        error = 0

    drive_power = -(maxP - minP) * (error - max_error) / max_error + minP   
    car.drive_speed(drive_power)
    await wait(10)

async def main():
    print(hub.battery.voltage())
    # Run tasks concurrently
    await multitask(
        remote_engine(), 
        update_robot_data(), 
        detect_corner(),
        sense_line_color(),
        straighten_heading(),
        ultrasonic_PID(kp=2.5, ki=0.001, kd=250.0),
        motor_controller(),
        race=True
        # if even one function stops, all function stops
    )

    car.drive_speed(0)
    car.steer(0)
    gc.collect() # <--- Force a full memory clear here!
    await wait(10) # Give the hub a moment to breathe

    rear.reset_angle(0)
    while rear.angle() < 2000:
        await heading_pid_corner_c()
    else:
        await hub.speaker.beep(900, 10)
    
        
    car.drive_speed(0)

run_task(main())
