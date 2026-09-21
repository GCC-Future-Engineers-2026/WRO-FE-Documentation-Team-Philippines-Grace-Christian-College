from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task
from pybricks.robotics import Car
from pupremote_hub import PUPRemoteHub
import gc
import umath as math

# --- Initialization ---
hub = PrimeHub()

rear = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steer = Motor(Port.C, Direction.COUNTERCLOCKWISE)

eyesR = UltrasonicSensor(Port.F)
eyesL = UltrasonicSensor(Port.E)
colorF = ColorSensor(Port.A)

p = PUPRemoteHub(Port.D)
p.add_command("msg", to_hub_fmt="repr", from_hub_fmt="repr")
p.add_channel('cam', to_hub_fmt='bhhb')

print(hub.battery.voltage())

hub.imu.reset_heading(0)
wait(500)
car = Car(steer, rear, 100)
wait(500)

# --- Global Variables ---
targetDist = 100
sum_error, prev_error = 0, 0
sum_Gerror, prev_Gerror = 0, 0
sum_Rerror, prev_Rerror = 0, 0
sumS_error, prevS_error = 0, 0
sumH_error, prevH_error = 0, 0
sump_error, prevp_error = 0, 0

last_error = 0 
last_Cerror = 0
last_Cerror_Cor = 0
l_error = 0

distListR = [0, 0, 0]
distListL = [0, 0, 0]
distListF = [0, 0, 0]

num_turn = 1
max_steer = 45 
direction = 1
distance_wall = 0

drive_power = 0.0
compensation = 0.0
lineColor = 0
p_error = 0
position_target = 0
angle_deg = 0
past_heading = 0

can_sense_corner = False
can_sense_corner_CW = False
can_sense_corner_CCW = False
detect_color = True
is_sequencing = False
turn_left = False
turn_right = False
avoidance = False
finish_turn = False
parking_seq = False
after_curl = False

rob_data = {
    "color": 0,
    "block_x": 0,
    "block_y": 0,
    "corner": 0,
    "heading": 0,
    "ultra_R": 0,
    "ultra_L": 0,
    "line_color": 0
}

steer_center, speed_center = 0, 0
steer_sequence, speed_sequence = 0, 0

# --- Core Sensor Functions ---
# Get samples to stabilize input from ultrasonic sensor
async def getMedianR(samples):
    i = 0
    while i < samples:
        distListR[i] = await eyesR.distance()
        i += 1
    distListR.sort()
    n = len(distListR)
    mid = n // 2
    if n % 2 == 1: return distListR[mid]
    else: return (distListR[mid-1] + distListR[mid]) / 2

async def getMedianL(samples):
    i = 0
    while i < samples:
        distListL[i] = await eyesL.distance()
        i += 1
    distListL.sort()
    n = len(distListL)
    mid = n // 2
    if n % 2 == 1: return distListL[mid]
    else: return (distListL[mid-1] + distListL[mid]) / 2

# Detects orange or blue lines in the corner section
async def getLineColor():
    global detect_color
    lineColor = 0
    hsv = await colorF.hsv()
    if detect_color:
        if (hsv[0] < 45 or (hsv[0] < 370 and hsv[0]> 300)) and hsv[1] > 40: # orange
            lineColor = 1  # orange
        elif (hsv[0] > 200 and hsv[0] < 300) and hsv[1] > 30: # blue
            lineColor = 2  # blue
    else:
        lineColor = 0
    return lineColor

# --- Background Engines ---
# Relays information from the camera
async def remote_engine():
    while True:
        await p.process_async()
        await wait(1)

# update information from sensors and camera
async def update_robot_data():
    global rob_data
    while True:
        rob_data['heading'] = hub.imu.heading()
        rob_data['line_color'] = await getLineColor()
        rob_data['ultra_R'] = await getMedianR(3)
        rob_data['ultra_L'] = await getMedianL(3)

        result = await p.call_multitask("cam")
        if result:
            color, block_x, block_y, corner= result 
            rob_data['color'] = color
            rob_data['block_x'] = block_x
            rob_data['block_y'] = block_y
            rob_data['corner'] = corner
        await wait(20)

# changes motor control according to priority
async def motor_controller():
    global rob_data, is_sequencing
    global steer_center, speed_center
    global steer_sequence, speed_sequence
    
    while True:
        if is_sequencing:
             # PRIORITY 1
            current_steer = steer_sequence
            current_speed = speed_sequence
        else:
            # PRIORITY 2
            current_steer = steer_center
            current_speed = speed_center
                
        car.steer(current_steer)
        car.drive_speed(current_speed)
        
        await wait(10)

# --- Maneuver Functions ---

async def get_out_parking():
    global direction
    # Auto detect layout orientation
    if await getMedianR(3) > await getMedianL(3): 
        direction = 1
    else: 
        direction = -1

    # Scale initial steering angle directly based on track direction
    car.steer(100 * direction)
    await wait(100)
    while abs(hub.imu.heading()) < 65:
        car.drive_speed(200)
        await wait(10)
    car.drive_speed(0)
    car.steer(0)
    await wait(100)
    rear.reset_angle()
    while rear.angle() < 990:
        car.drive_speed(700)
        await wait(10)
    car.drive_speed(0)
    car.steer(75 * direction)
    await wait(100)
    
    # Watch gyro orientation bound dynamically 
    while (direction == 1 and hub.imu.heading() > 15) or (direction == -1 and hub.imu.heading() < -15):
        car.drive_speed(-500)
        await wait(10)
    car.drive_speed(0)
    car.steer(0)

# pid in corner turns for smooth execution
async def turn90_PID_L(num_turn, kp=20.0, ki=0.0, kd=55.0, maxP=900, minP=400, forward=False):
    global sumS_error, prevS_error, direction
    global is_sequencing, speed_sequence
    base_target = 90 * num_turn
    target_angle = base_target * direction 
    sumS_error = 0
    prevS_error = 0
    while True:
        current_heading = hub.imu.heading()
        steer_error = target_angle - current_heading
        abs_error = abs(steer_error)
        # cut turn short to avoid turning over 90
        if direction == 1:
            if abs_error <= 2: 
                break
        if direction == -1:
            if abs_error <= 2:
                break
        prop = kp * abs_error
        sumS_error += abs_error
        derivative = kd * (abs_error - prevS_error)
        compensation = prop + (ki * sumS_error) + derivative
        prevS_error = abs_error
        if compensation > maxP:
            compensation = maxP
        elif compensation < minP:
            compensation = minP
        if forward:
            speed_sequence = compensation
        else:
            speed_sequence = -compensation
        await wait(10)
    speed_sequence = 0
    is_sequencing = True

# pid in corner turns for smooth execution
async def last_straight_forward():
    kp = 3.0
    kd = 50.0
    global last_error, steer_center, speed_center

    while rear.angle() < 3080:
        current_angle = hub.imu.heading()
        error = 0 - current_angle
        
        # Calculate derivative (rate of change)
        derivative = error - last_error
        # Calculate PD steering output
        steering = (error * kp) + (derivative * kd)
        # Update last_error for the next iteration
        last_error = error
        steer_center = steering
        speed_center = 550
        # Brief sleep to yield execution to other async tasks
        await wait(10)
    
    await hub.speaker.beep()
    speed_center = 0
    steer_center = 0

    return

async def forward():
    kp = 3.0
    kd = 50.0
    global l_error, steer_sequence, speed_sequence, direction
    
    error = -180*direction - hub.imu.heading()

    # Calculate derivative (rate of change)
    derivative = error - l_error
    # Calculate PD steering output
    steering = (error * kp) + (derivative * kd)
    # Update last_error for the next iteration
    l_error = error
    car.steer(steering)
    car.drive_power(50)
    await wait(10)
    

    

    steer_sequence = steering
    speed_sequence = 850
    # Brief sleep to yield execution to other async tasks
    await wait(10)

async def straight_forward():
    kp = 3.0
    kd = 50.0
    global last_error
    
    current_angle = hub.imu.heading()
    error = 0 - current_angle
    
    # Calculate derivative (rate of change)
    derivative = error - last_error
    
    # Calculate PD steering output
    steering = (error * kp) + (derivative * kd)
    # Update last_error for the next iteration
    last_error = error
    car.steer(steering)
    car.drive_power(50)
    # Brief sleep to yield execution to other async tasks
    await wait(10)

# use gyro to move straight backward
async def straight_backward():
    current_angle = hub.imu.heading()
    error = 0 - current_angle
    if direction == 1:
        car.steer(-(error * 1.5))
    if direction == -1:
        car.steer(-(error * 1.5))   
    car.drive_power(-70) 

# Gyro assist to make the turn as close to 90 degrees as possible
async def last_turn():
    global direction, can_sense_corner, can_sense_corner_CCW, can_sense_corner_CW
    await hub.speaker.beep(600, 100)
    target_angle = 90 * direction
    car.steer(-100 * direction)
    await wait(500)
    car.drive_power(-70) 
    while abs(hub.imu.heading()) < abs(target_angle - 10): 
        await wait(10)
        car.drive_power(-50)
        if (direction == 1 and hub.imu.heading() >= 90) or (direction == -1 and hub.imu.heading() <= -87):
            break
    can_sense_corner = False

async def curl():
    global direction, distance_wall
    current_rot = rear.angle()
    while rear.angle() < current_rot + 330:
        car.steer(0)
        car.drive_speed(800)
        await wait(10)

    if direction==1:
        while hub.imu.heading() > -175:
            car.steer(-60)
            car.drive_speed(750)
            await wait (10)
    elif direction == -1:
        while hub.imu.heading() < 175:
            car.steer(60)
            car.drive_speed(750)
            await wait (10)
    
    car.steer(0)
    car.drive_speed(0)

    await wait(100)

    current_rot = rear.angle()
    
    l_error = 0
    while rear.angle() < current_rot + 900:
        await forward()
        await wait(10)
    
    car.drive_speed(0)
    car.steer(85*direction)
    await wait(300)

    if direction == 1:
        while hub.imu.heading() < -120:
            car.drive_speed(800)
            await wait(10)

    if direction == -1:
        while hub.imu.heading() > 120:
            car.drive_speed(800)
            await wait(10)
    
    car.drive_speed(0)
    car.steer(0)
    await wait(300)
    
    current_rot = rear.angle()
    car.steer(0)
    while rear.angle() < current_rot + 500:
        car.drive_speed(800)
        await wait(10)

    if direction == 1:
        distance_wall = await getMedianL(3)
        print(distance_wall)
    if direction == -1:
        distance_wall = await getMedianR(3)
    rear.reset_angle(0)
    hub.imu.reset_heading(0)
    car.drive_power(0)
    await wait(300)

    if direction == 1:
        while rear.angle() > -172:
            await straight_backward()
            await wait(10)

    if direction == -1:
        while rear.angle() > -158:
            await straight_backward()
            await wait(10)
    car.drive_power(0)
    car.steer(0)
    await wait(700)
    if direction == 1:
        await last_turn()
    if direction == -1:
        await last_turn()
    car.steer(0)
    car.drive_power(0)
    await wait(100)

    rear.reset_angle(0)
    car.steer(0)
    hub.imu.reset_heading(0)
    await wait(300)
    if direction == 1:
        while rear.angle() > int(-(distance_wall * 2.5)):
            await straight_backward() 
            await wait(10)
        rear.reset_angle(0)
        car.drive_power(0)
        
    if direction == -1:
        while rear.angle() > int(-(distance_wall * 2.5)):
            await straight_backward() 
            await wait(10)
        rear.reset_angle(0)
        car.drive_power(0)
    if direction == 1:
        hub.imu.reset_heading(0)
        car.steer(0)
        await wait(500)
        rear.reset_angle(0)
        while rear.angle() < 3080:
            await straight_forward()
            await wait(10)
    if direction == -1:
        hub.imu.reset_heading(0)
        car.steer(0)
        await wait(500)
        rear.reset_angle(0)
        while rear.angle() < 3088:
            await straight_forward()
            await wait(10)


# this function uses car.steer and car.drive_power because it is outside of the multitask
async def parallel_parking():

    global is_sequencing, after_curl

    global num_turn, speed_sequence, steer_sequence
    global distance_wall, direction, parking_seq
    hub.imu.reset_heading(0)
    rear.reset_angle(0)
    car.drive_power(0)
    car.steer(0)
    await wait(300)
    if direction == 1:
        while rear.angle() > -172:
            await straight_backward()
            await wait(10)
    if direction == -1:
        while rear.angle() > -158:
            await straight_backward()
            await wait(10)
    car.drive_power(0)
    car.steer(0)
    await wait(700)
    if direction == 1:
        await last_turn()
    if direction == -1:
        await last_turn()
    car.steer(0)
    car.drive_power(0)
    await wait(100)

    rear.reset_angle(0)
    car.steer(0)
    hub.imu.reset_heading(0)
    await wait(300)

    if direction == 1:
        while rear.angle() > int(-(distance_wall * 2.5)):
            await straight_backward() 
            await wait(10)
        rear.reset_angle(0)
        car.drive_power(0)
        
    if direction == -1:
        while rear.angle() > int(-(distance_wall * 2.5)):
            await straight_backward() 
            await wait(10)
    car.drive_power(0)
    await wait(100)

    is_sequencing = False
        
    hub.imu.reset_heading(0)
    car.steer(0)
    await wait(500)
    rear.reset_angle(0)
    await multitask(
        remote_engine(),  
        update_robot_data(),
        last_avoid_blocks_and_return_center(),
        last_straight_forward(),
        motor_controller(),
        race = True
    )
    await wait (50)
    if after_curl == True:
        await curl()
    
    # difference in value from the location of the differentialww
    if direction == 1:
        car.drive_power(0)
        await wait(500)
        rear.reset_angle(0)
        car.steer(-89)
        await wait(100)
        while hub.imu.heading() < 75:
            car.drive_power(-40)
            await wait(10)
        car.drive_power(0)
        await wait (100)
        await wait(200)
        car.steer(93)
        
        await wait(200)
        while hub.imu.heading() >= 20:
            car.drive_power(-40)
            await wait(10)
        car.drive_power(0)
        await wait(300)
        rear.reset_angle(0)
        car.steer(-90)
        await wait(100)
        while hub.imu.heading() > 5:
            car.drive_power(10)
    # difference in value from the location of the differentialww
    if direction == -1:
        car.drive_power(0)
        await wait(500)
        rear.reset_angle(0)
        car.steer(89)
        await wait(100)
        while hub.imu.heading() > -75:
            car.drive_power(-40)
            await wait(10)
        car.drive_power(0)
        await wait (100)
        await wait(200)
        car.steer(-93)
        
        await wait(200)
        while hub.imu.heading() <= -20:
            car.drive_power(-40)
            print(hub.imu.heading())
            await wait(10)
        car.drive_power(0)
        await wait(300)
        rear.reset_angle(0)
        car.steer(90)
        await wait(100)
        while hub.imu.heading() < -5:
            car.drive_power(10)
            
    car.drive_power(0)
    await wait(500)
    car.steer(0)
    await wait(500)

# --- Block Avoidance & Recovery Functions ---

def avoid_blocks(color=0, kp=1.5, ki=0.000001, kd=10.0, bl_x=0.0, bl_y=0.0, minPower=500, maxPower=900, max_steer_obs=80):

    global sum_Rerror, prev_Rerror, sum_Gerror, prev_Gerror
    global steer_sequence, speed_sequence, turn_right, turn_left
    global direction, finish_turn, angle_deg, num_turn, parking_seq
        
   
    current_error = 0 
    
    if color == 2:  # Red block
        
        # bl_x is the distance from the center 
        x = bl_x + 95
        # bl_y is the distance from the top
        y = bl_y

        angle_deg = abs(math.atan2(x, y) * 180.0 / math.pi)
        
        if x > 0:
            angle_deg = angle_deg
        else:
            angle_deg = 0

        if direction == 1:
            # Target heading increases by +90 per turn: 0 -> 90 -> 180
            target_heading = (num_turn - 1) * 90 + angle_deg
            Rerror = target_heading - hub.imu.heading()

        elif direction == -1:
            # Target heading decreases by -90 per turn: 0 -> -90 -> -180
            # The camera angle offset is inverted (* direction) to properly mirror the avoidance swing
            target_heading = ((num_turn - 1) * 90 * direction) + angle_deg
            Rerror = target_heading - hub.imu.heading()

        current_error = Rerror
        prop = kp * Rerror 
        sum_Rerror += Rerror
        integral = ki * sum_Rerror

        if integral > 10.0: 
            integral = 10.0
        
        derivative = kd * (Rerror - prev_Rerror) 
        compensation = prop + integral + derivative
        prev_Rerror = Rerror
        
        if compensation > max_steer_obs: 
            compensation = max_steer_obs
        elif compensation < -max_steer_obs: 
            compensation = -max_steer_obs
        
        steer_sequence = compensation

        
        temp_speed = -(45 / 28) * (abs(Rerror) - 1120 / 3)
        
        if temp_speed < minPower:
            speed_sequence = minPower
        else:
            speed_sequence = temp_speed

        turn_left = True
        turn_right = False
        
    elif color == 1:  # Green block

        # bl_x is the distance from the center 
        x = bl_x - 90
        # bl_y is the distance from the top
        y = bl_y

        angle_deg = abs(math.atan2(x, y) * 180.0 / math.pi)        
        
        if x < 0:
            angle_deg = -angle_deg
        else:
            angle_deg = 0

        if direction == 1:
            # Target heading increases by +90 per turn: 0 -> 90 -> 180
            target_heading = (num_turn - 1) * 90 + angle_deg
            Gerror = target_heading - hub.imu.heading()

        elif direction == -1:
            # Target heading decreases by -90 per turn: 0 -> -90 -> -180
            # The camera angle offset is inverted (* direction) to properly mirror the avoidance swing
            target_heading = ((num_turn - 1) * 90 * direction) + angle_deg
            Gerror = target_heading - hub.imu.heading()
            
        current_error = Gerror
        prop = kp * Gerror 
        sum_Gerror += Gerror
        integral = ki * sum_Gerror 
        if integral > 10.0: integral = 10.0
        derivative = kd * (Gerror - prev_Gerror)
        compensation = prop + integral + derivative


        prev_Gerror = Gerror
        if compensation > max_steer_obs: 
            compensation = max_steer_obs
        elif compensation < -max_steer_obs: 
            compensation = -max_steer_obs
        
        steer_sequence = compensation 
        
        temp_speed = -(45 / 28) * (abs(Gerror) - 1120 / 3)
        
        if temp_speed < minPower:
            speed_sequence = minPower
        else:
            speed_sequence = temp_speed 
        
        turn_right = True
        turn_left = False

    return current_error

def last_avoid_blocks(color=0, kp=1.5, ki=0.000001, kd=10.0, bl_x=0.0, bl_y=0.0, minPower=500, maxPower=900, max_steer_obs=80):

    global sum_Rerror, prev_Rerror, sum_Gerror, prev_Gerror
    global steer_sequence, speed_sequence, turn_right, turn_left
    global direction, finish_turn, angle_deg, num_turn, parking_seq
       
   
    current_error = 0 
    if color == 2 and direction == 1:  # Red block
        
        # bl_x is the distance from the center 
        x = bl_x + 95
        # bl_y is the distance from the top
        y = bl_y

        angle_deg = abs(math.atan2(x, y) * 180.0 / math.pi)

        
        if x > 0:
            angle_deg = angle_deg
        else:
            angle_deg = 0

            # Target heading increases by +90 per turn: 0 -> 90 -> 180
        target_heading = direction * angle_deg
        Rerror = target_heading - hub.imu.heading()
        
        current_error = Rerror
        prop = kp * Rerror 
        sum_Rerror += Rerror
        integral = ki * sum_Rerror

        if integral > 10.0: 
            integral = 10.0
        
        derivative = kd * (Rerror - prev_Rerror) 
        compensation = prop + integral + derivative
        prev_Rerror = Rerror
        
        if compensation > max_steer_obs: 
            compensation = max_steer_obs
        elif compensation < -max_steer_obs: 
            compensation = -max_steer_obs
        

        steer_sequence = compensation
        
        temp_speed = -(45 / 28) * (abs(Rerror) - 1120 / 3)
        
        if temp_speed < minPower:
            speed_sequence = minPower
        else:
            speed_sequence = temp_speed

        
    elif color == 1 and direction == -1:  # Green block

        # bl_x is the distance from the center 
        x = bl_x - 95
        # bl_y is the distance from the top
        y = bl_y

        angle_deg = abs(math.atan2(x, y) * 180.0 / math.pi)        
        
        if x < 0:
            angle_deg = -angle_deg
        else:
            angle_deg = 0


            # Target heading decreases by -90 per turn: 0 -> -90 -> -180
            # The camera angle offset is inverted (* direction) to properly mirror the avoidance swing
        target_heading = angle_deg
        Gerror = target_heading - hub.imu.heading()
            
        current_error = Gerror
        prop = kp * Gerror 
        sum_Gerror += Gerror
        integral = ki * sum_Gerror 
        if integral > 10.0: integral = 10.0
        derivative = kd * (Gerror - prev_Gerror)
        compensation = prop + integral + derivative


        prev_Gerror = Gerror
        if compensation > max_steer_obs: 
            compensation = max_steer_obs
        elif compensation < -max_steer_obs: 
            compensation = -max_steer_obs
        
        steer_sequence = compensation
        
        temp_speed = -(45 / 28) * (abs(Gerror) - 1120 / 3)
        
        if temp_speed < minPower:
            speed_sequence = minPower
        else:
            speed_sequence = temp_speed 
                    
    return current_error

# Calculates steering PID correction to head back toward center target
def position_to_center(position_target, p_error, kp=7.5, ki=0.000001, kd=15.0, max_steer=80):
    
    global sump_error, prevp_error, num_turn
    global steer_sequence, speed_sequence
    
    p_error = position_target - hub.imu.heading()
    prop = kp * p_error 
    sump_error += p_error
    integral = ki * sump_error 
    if integral > 10.0: 
        integral = 10.0
    elif integral < -10.0: 
        integral = -10.0
    
    derivative = kd * (p_error - prevp_error) 
    compensation = prop + integral + derivative
    prevp_error = p_error
    
    if compensation > max_steer: 
        compensation = max_steer
    elif compensation < -max_steer: 
        compensation = -max_steer
    
    steer_sequence = compensation

# return to the middle on the track
async def return_to_center_position(num_turn, direction, gyro_angle_correct=20, max_steer=80, color = 0):
    
    global prevp_error, sump_error, p_error
    global steer_sequence, speed_sequence, turn_right, turn_left
    global position_target, angle_deg, target_distance, past_heading
    
    if direction == 1:
        if turn_left == True: #centering from red block
            position_target = 90 * (num_turn-1) * direction - (angle_deg) + abs(past_heading)
        elif turn_right == True: #centering from green block
            position_target = 90 * (num_turn-1) * direction + (-angle_deg) + abs(past_heading)
    
    elif direction == -1:
        if turn_right == True: 
            position_target = 90 * (num_turn-1) * direction + (-angle_deg) + abs(past_heading)
        elif turn_left == True: 
            position_target = 90 * (num_turn-1) * direction - (angle_deg) + abs(past_heading)

    p_error = position_target - hub.imu.heading()
    rear.reset_angle(0)
    while rear.angle() < int(target_distance * 1.5):
        p_error = position_target - hub.imu.heading()
                
        position_to_center(position_target, p_error, max_steer=max_steer)
        speed_sequence = 1100
        await wait(10)


# pid for return to center from block
def steer_to_center(target, kp=2.0, ki=0.000001, kd=10.0, max_steer=80):
    global sumH_error, prevH_error, steer_sequence
    h_error = target - hub.imu.heading()
    prop = kp * h_error 
    sumH_error += h_error
    integral = ki * sumH_error 
    if integral > 10.0: integral = 10.0
    elif integral < -10.0: integral = -10.0
    derivative = kd * (h_error - prevH_error) 
    compensation = prop + integral + derivative
    prevH_error = h_error
    if compensation > max_steer: compensation = max_steer
    elif compensation < -max_steer: compensation = -max_steer
    steer_sequence = compensation

# straighten out the robot after returning to center position
async def return_center_fr_block(num_turn, direction, max_steer=50):
    
    global steer_sequence, speed_sequence, turn_left, turn_right
    global sumH_error, prevH_error
    sumH_error = 0
    prevH_error = 0
    target = 0

    if direction == 0: 
        target = 0
    if turn_left == False or turn_right == False:
        target = (90 * (num_turn - 1)) * direction
    else:
        if turn_left == True:
            target = (90 * (num_turn - 1)) * direction
            # target = (90 * (num_turn - 1)) * direction
        if turn_right == True:
            target = (90 * (num_turn - 1)) * direction
            # target = (90 * (num_turn - 1)) * direction
    
    while True:
        h_error = target - hub.imu.heading()
        if turn_left or turn_right:
            if abs(h_error) <= 15: 
                steer_sequence = 0
                break
        else:
            if abs(h_error) <= 15: 
                steer_sequence = 0
                break 
                
        steer_to_center(target, max_steer=max_steer)
        speed_sequence = 700
        await wait(10)

# --- Navigation and Detection logic ---

# detecting corner, resetting gyro after each lap and initiating parking sequence
async def detect_corner():
    
    global num_turn, direction
    global rob_data, steer_sequence, speed_sequence, is_sequencing
    global can_sense_corner, can_sense_corner_CW, can_sense_corner_CCW
    global detect_color, distance_wall
    
    if num_turn < 12:
        is_sequencing = True
        await hub.speaker.beep()
        if direction == 0:
            if rob_data['ultra_L'] > rob_data['ultra_R']: direction = -1
            elif rob_data['ultra_L'] < rob_data['ultra_R']: direction = 1
        if num_turn in [4, 8]:
            rear.reset_angle(0)
            steer_sequence = 0
            if direction == 1:
                watch = StopWatch()
                while watch.time() < 1500: 
                    current_angle = hub.imu.heading()
                    error = (90 * (num_turn - 1) * direction) - current_angle
                    steer_sequence = error * 1.65
                    speed_sequence = 800
                    await wait(10)

            if direction == -1:

                watch = StopWatch()
                while watch.time() < 1500: 
                    current_angle = hub.imu.heading()
                    error = (90 * (num_turn - 1) * direction) - current_angle
                    steer_sequence = error * 1.65
                    speed_sequence = 800
                    await wait(10)

            hub.imu.reset_heading(90 * (num_turn-1) * direction)
            rear.reset_angle(0)
            steer_sequence = 0
            await wait(10)
            while rear.angle() > -370:
                speed_sequence = -800
                await wait(10)
        else:
            rear.reset_angle(0)
            while rear.angle() > -310:
                speed_sequence = -800
                await wait(10)
            
            speed_sequence = 0
            
        
        steer_sequence = -80 * direction
        await wait(100)
        await turn90_PID_L(num_turn, forward=False, maxP=1100, minP=400)
        num_turn += 1

        
        await wait(10)
        steer_sequence = 0
        await wait(200)
        rear.reset_angle(0)
        
        while rear.angle() < 1000 and (rob_data['block_x'] == 0.0 or rob_data['block_x'] > 275 or rob_data['block_x'] < 45):
            await heading_pid_corner(speed=800)
            await wait(10)
        
        await hub.speaker.beep(1100)
        is_sequencing = False
        if direction == 1: can_sense_corner_CW = False
        elif direction == -1: can_sense_corner_CCW = False


    elif num_turn == 12:
        # initiating parking sequence
        if direction == 1:
            can_sense_corner = can_sense_corner_CW
        elif direction == -1:
            can_sense_corner = can_sense_corner_CCW
        
        is_sequencing = True
        await hub.speaker.beep(100)
        watch = StopWatch()
        watch.reset()
        rear.reset_angle(0)
        while rear.angle() < 500 and watch.time() < 2000: 
            current_angle = hub.imu.heading()
            error = (90 * (num_turn-1) * direction) - current_angle
            steer_sequence = error * 2.5
            speed_sequence = 700
            await wait(10)
        rear.reset_angle(0)
        await wait (100)
        speed_sequence = 0
        steer_sequence = 0
        await wait(100)
        speed_sequence = 0
        steer_sequence = 60
        await wait(100)
        rear.reset_angle(0)
        while rear.angle() < 50 and watch.time() < 3000:
            speed_sequence = 200
            await wait(10)
        speed_sequence = 0
        await wait(100)
        steer_sequence = -60
        await wait (200)
        while rear.angle() < 50 and watch.time() < 3800:
            speed_sequence = 200
            await wait(10)
        steer_sequence = 0
        await wait(100)
        while rear.angle() < 50 and watch.time() < 4600:
            speed_sequence = 200
            await wait(10)
        if direction == 1:
            distance_wall = await getMedianL(3)
        if direction == -1:
            distance_wall = await getMedianR(3)
        speed_sequence = 0
        steer_sequence = 0
        await wait(250)
        parking_seq = True
        num_turn += 1

        is_sequencing = False


async def ultrasonic_PID(kp=0.001, ki=0.000001, kd=10.0, minPower=900, maxPower=1000, gyro_angle_correct=20):
    
    global sum_error, prev_error, max_steer, direction, num_turn
    global rob_data, steer_center, speed_center, is_sequencing

    while num_turn <= 12:        
        if is_sequencing == True:
            sum_error = 0
            prev_error = 0
            await wait(20)
            continue
            
        error = rob_data['ultra_R'] - rob_data['ultra_L']
        prop = kp * error 
        sum_error += error
        integral = ki * sum_error 
        if integral > 10.0: 
            integral = 10.0
        derivative = kd * (error - prev_error) 
        compensation = prop + integral + derivative
        prev_error = error
        
        if compensation > max_steer: 
            compensation = max_steer
        elif compensation < -max_steer: 
            compensation = -max_steer
        
        maxP, minP = maxPower, minPower
        
        max_error = 1000
        if abs(error) > max_error: 
            error = max_error
        elif error < 0: 
            error = 0
        
        drive_power = -(maxP - minP) * (error - max_error) / max_error + minP   
        steer_center = compensation
        speed_center = drive_power                    
        await wait(50) 
    
    speed_center = 0

async def heading_pid(speed=1000, kp=4.0, kd=20.0):
    
    global last_Cerror, num_turn, direction
    global steer_center, speed_center, is_sequencing
    
    while num_turn <= 12:
        if is_sequencing == True:
            prev_error = 0
            last_Cerror = 0
            await wait(20)
        else:
            current_angle = hub.imu.heading()
            target_heading = (90 * (num_turn - 1)) * direction
            error =  target_heading - current_angle
            
            # Calculate derivative (rate of change)
            derivative = error - last_Cerror
            
            # Calculate PD steering output
            steering = (error * kp) + (derivative * kd)
            
            # Update last_error for the next iteration
            last_Cerror = error
            steer_center = steering
            speed_center = speed
            
            # Brief sleep to yield execution to other async tasks
            await wait(20)
    
    return

async def heading_pid_corner(speed=1000):
    kp = 3.0
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

# Allows the robot to turn at corners
async def sense_line_color():
    global can_sense_corner_CW, can_sense_corner_CCW, detect_color, finish_turn, num_turn

    while True:
        if rob_data['line_color'] == 1 and (direction == 0 or direction == 1) and detect_color == True: 
            can_sense_corner_CW = True
            await hub.speaker.beep(100)
            await wait(100)
            detect_color = False
            is_sequencing = True
            watch = StopWatch()
            while True:
                await heading_pid_corner()
                if rob_data["corner"] == 1:
                    await detect_corner()
                    finish_turn = True
                    break
                elif watch.time() > 2500 and finish_turn == False:
                    await detect_corner()
                    finish_turn = True
                    break
                await wait (10)
        
        elif rob_data['line_color'] == 2 and (direction == 0 or direction == -1) and detect_color == True: 
            can_sense_corner_CCW = True
            await hub.speaker.beep(100)
            detect_color = False
            watch = StopWatch()
            while True:
                await heading_pid_corner()
                if rob_data["corner"] == 1:
                    await detect_corner()
                    finish_turn = True
                    break
                elif watch.time() > 2500 and finish_turn == False:
                    await detect_corner()
                    finish_turn = True
                    break
                await wait (10)
        
        await wait(20)

# combined function for the whole avoiding block and recovery process
async def avoid_blocks_and_return_center():

    global is_sequencing, steer_sequence, speed_sequence, detect_color, turn_left, turn_right
    global sum_Gerror, prev_Gerror, sum_Rerror, prev_Rerror, sump_error, prevp_error, avoidance, finish_turn
    global num_turn, target_distance, past_heading, parking_seq
    
    while True:
        if direction == 1: 
            current_corner_active = can_sense_corner_CW
        elif direction == -1: 
            current_corner_active = can_sense_corner_CCW
        else: 
            current_corner_active = False

        colorBlock = rob_data['color']
        target_x = rob_data['block_x']
        target_y = rob_data['block_y']        

        if current_corner_active or (is_sequencing and target_x == 0 and speed_sequence != 800):
            await wait(20)
            continue 

        if target_x != 0.0 and target_y > 100 and not is_sequencing and colorBlock in (1,2):            
            is_sequencing = True
            avoidance = True
            sum_Gerror, prev_Gerror = 0, 0
            sum_Rerror, prev_Rerror = 0, 0
            sump_error, prevp_error = 0, 0
            
            await hub.speaker.beep(900,10)
            
            # --- STEP 1: CAM LOOP ---

            x = target_x - 160
            y = 240 - target_y

            if x == -160 and y == 240: # wrong reading, ignore
                continue        

            # --- HYPOTENUSE MULTIPLIER (Swapped 1.5x buffer out for your 1.25x) ---
            target_distance = int(math.sqrt(x * x + y * y) * (y / 21.0))

            if target_distance > 900: # failsafe for when x and y readings are crazy
                target_distance = 700

            past_heading = hub.imu.heading() - (num_turn-1)*90*direction
                        
            rear.reset_angle(0)            
            print('error?')         
            while abs(rear.angle()) < target_distance:
                avoid_blocks(color = colorBlock, bl_x = x, bl_y = y, max_steer_obs = 80)
                
                await wait(10)

            # --- STEP 2: CLEARANCE BUFFER ---
            current_rot = rear.angle()
            
            while rear.angle() < current_rot + 75:
                steer_sequence = 0
                speed_sequence = 800
                await wait(10)
            detect_color = True

            # --- STEP 3: DIAGONAL RECOVERY ---
            await return_to_center_position(num_turn, direction, max_steer=45)
            await wait(10)
            
            # --- STEP 4: FLATTEN ALIGNMENT ---
            await return_center_fr_block(num_turn, direction, max_steer=45)
            await wait(10)
            
            turn_left = False
            turn_right = False
            is_sequencing = False 
            avoidance = False
            finish_turn = False
        else:
            pass

        await wait(20)

async def last_avoid_blocks_and_return_center():

    global is_sequencing, steer_sequence, speed_sequence, detect_color, turn_left, turn_right
    global sum_Gerror, prev_Gerror, sum_Rerror, prev_Rerror, sump_error, prevp_error, avoidance, finish_turn
    global num_turn, target_distance, past_heading, parking_seq
    global last_error, distance_wall, after_curl
    
    while True:
        if direction == 1: 
            current_corner_active = can_sense_corner_CW
        elif direction == -1: 
            current_corner_active = can_sense_corner_CCW
        else: 
            current_corner_active = False

        colorBlock = rob_data['color']
        target_x = rob_data['block_x']
        target_y = rob_data['block_y']

        if ((colorBlock == 1 and direction == -1) or (colorBlock == 2 and direction == 1)) \
        and target_x != 0.0 and target_y > 100 and not is_sequencing and rear.angle() < 3080*0.7:   

            is_sequencing = True
            avoidance = True
            sum_Gerror, prev_Gerror = 0, 0
            sum_Rerror, prev_Rerror = 0, 0
            sump_error, prevp_error = 0, 0
            
            await hub.speaker.beep(900,10)
            
            # --- STEP 1: CAM LOOP ---
            x = target_x - 160
            y = 240 - target_y
            if x == -160 and y == 240:
                continue        

            # --- HYPOTENUSE MULTIPLIER (Swapped 1.5x buffer out for your 1.25x) ---
            target_distance = int(math.sqrt(x * x + y * y) * (y / 20.0))

            if target_distance > 900: # failsafe for when x and y readings are crazy
                target_distance = 700

            past_heading = hub.imu.heading()-90*direction

            current_rot = rear.angle() 
            speed_sequence = 0
            await wait(300)  
            
            while abs(rear.angle()) < current_rot + target_distance:
                last_avoid_blocks(color = colorBlock, bl_x = x, bl_y = y, max_steer_obs = 80)
                
                await wait(10)
            after_curl = True
            break
        
            turn_left = False
            turn_right = False
            is_sequencing = False 
            avoidance = False
            finish_turn = False

            return
        else:
            pass

        await wait(20)

# --- Execution ---

async def main():
    await get_out_parking()
    # asynchronously controls functions
    await multitask(
        remote_engine(),  
        update_robot_data(),
        avoid_blocks_and_return_center(),
        sense_line_color(),
        heading_pid(speed=1000, kp=3.0, kd=20.0),
        motor_controller(),
        race=True        
    )
    await parallel_parking()
    car.drive_speed(0)
    car.steer(0)
    gc.collect() 
    await wait(500) 

run_task(main())
