## Team Introduction

WRO Future Engineers 2026: Team Grace Christian College 🏎️
Welcome to the official engineering repository for Team Grace Christian College from The Philippines.

This repository documents the complete development cycle of our autonomous vehicle, designed from the ground up for the WRO Future Engineers challenge. Our engineering strategy this year focused on lightweight chassis design and high-speed computer vision processing]. By prioritizing [e.g., reliable sensor fusion over complex mechanics], we built a robot capable of navigating dynamic obstacle courses with high precision and consistent lap times.

Below, you will find our complete codebase, electrical schematics, and the engineering documentation that tracks our progress from early prototypes to our final competition-ready vehicle. <br>

<img width="500" alt="image" src="https://github.com/user-attachments/assets/ec08529b-d942-4aec-9292-35f2b0b49923" />

**Team Members:**<br>
   - *Kyron Chen* Grade 8 of Grace Christian College<br>
   contact - chen.kyronemmanuel@grace.gcc.edu.ph

   - *Thomas Yuri* Grade 10 of Grace Christian College<br>
   contact - email

   - *Fritz Lim* Grade 11 of Grace Christian College<br>
   contact - lim.fritz.nathaniel@gmail.com

**Coaches:**<br>
   - *Warren Ong Pe* <br>
   contact - wbongpe@gmail.com

   - *Kim Gamboa* <br>
   contact - kim.kkhg@gmail.com 
 <br> <br>




## Challenge Overview
**Open Challenge**<br>
<img width="1920" height="1080" alt="Your paragraph text" src="https://github.com/user-attachments/assets/b7905e48-aeb5-42b5-8661-68f35fba2c16" />
<br>
- Objective: Autonomously complete 3 consecutive laps either clockwise or counterclockwise<br>
- Environment: Randomized track dimensions and starting direction.<br>
- Obstacles: None. Pure lane-keeping between inner and outer boundary walls.<br>
- End State: Halt vehicle immediately after the 3rd lap is registered.<br><br>

**Obstacle Challenge**<br>
<img width="1920" height="1080" alt="1" src="https://github.com/user-attachments/assets/50f746c1-f3cb-4a79-80a9-d4d00858b0b0" />
<br>
- Objective: Autonomously complete 3 consecutive laps either clockwise or counterclockwise AND execute parallel parking.<br>
- Environment: Randomized track, starting direction, and randomized parking zone.<br>
- Obstacles: Traffic signs (pillars) dynamically placed inside the driving lanes.<br>
   -> RED Pillar: Vehicle must evade and pass to the RIGHT side.<br>
   -> GREEN Pillar: Vehicle must evade and pass to the LEFT side.<br>
- End State: Recognize parking zone post-lap 3 and park within physical limits.<br> <br>


## Vehicle Photos

## Performance Videos

## Robot Specifications
<br>

| **Measurement** | **Unit** |
|---|---|
| Length | 20.0 cm | 
| Width | 11.9 cm | 
| Height | 19.5 cm | 
| Weight | 886 g |

<br>

## Repository Structure
<br>

📁scheme — This directory contains the complete electrical documentation of the vehicle. It includes pictures of each specific component of our robot and their respective functions. Our extensive documentation ensures full hardware reproducibility. It details how the Spike Prime Hub interfaces with the components and how power is distributed across the system. <br>

📁src — This directory contains the entirety of our robot's program in Python (programming language). It includes the obstacle management of each sensor and the core logic behind our robot's decision making and navigation throughout both the open and obstacle challenge, particularly the logic behind the camera code and how it is integrated into the main code. <br>

📁t-photos — This directory contains our team's pictures. <br>

📁v-photos — This directory is where our robot is displayed visually. It includes both 2D and 3D pictures of our robot from all sides. The components seen in images are labelled to further enhance clarity of the images.  <br>

📁video — This directory contains videos of our robot in operation. It includes both open and obstacle challenge videos. <br> <br>
 
# 📚Table of Contents

* 👥 [Team Introduction](#team-introduction)
  <br><br>
* [Challenge Overview](#challenge-overview)
  <br><br>
* [Vehicle Photos](#vehicle-photos)
  <br><br>
* [Performance Videos](#performance-videos)
  <br><br>
* [Repository Structure](#repository-structure)
  <br><br>
* [1.0 Mechanical Design and Mobility Management](#10-mechanical-design-and-mobility-management)
   * [1.1 Chassis Architecture](#11-chassis-architecture)
      * [1.1.1 Tire Selection](#111-tire-selection)
      * [1.1.2 Motor Configuration](#112-motor-configuration)
   * [1.2 Drivetrain and Kinematics](#12-drivetrain-and-kinematics)
      * [1.2.1 Differential Gear Integration](#121-differential-gear-integration)
      * [1.2.2 Ackermann Steering Geometry](#122-ackermann-steering-geometry)
   * [1.3 Powertrain Analysis](#13-powertrain-analysis)
      * [1.3.1 Torque and Speed Analysis](#131-torque-and-speed-analysis)
   * [1.4 Mechanical Tradeoffs and Iterations](#14-mechanical-tradeoffs-and-iterations)
      * [1.4.1 Cantilever vs. Braced Rear Wheel Stability](#141-cantilever-vs-braced-rear-wheel-stability)
   * [1.5 Assembly and Bill of Materials (BOM)](#15-assembly-and-bill-of-materials-bom)
      * [1.5.1 Building Instructions](#151-building-instructions)
      * [1.5.2 Complete Component List](#152-complete-component-list)
* [2.0 Power and Sense Management](#20-power-and-sense-management)
   * [2.1 Power Distribution](#21-power-distribution)
      * [2.1.1 LEGO SPIKE Hub Battery](#211-lego-spike-hub-battery)
      * [2.1.2 External Power](#212-external-power)
   * [2.2 Wiring & Schematics](#22-wiring--schematics)
      * [2.2.1 LEGO SPIKE Hub](#221-lego-spike-hub)
      * [2.2.2 External Wiring](#222-external-wiring)
   * [2.3 Sensor Integration](#23-sensor-integration)
      * [2.3.1 OpenMV H7 Plus](#231-openmv-h7-plus)
      * [2.3.2 Ultrasonic Sensors](#232-ultrasonic-sensors)
      * [2.3.3 Spike IMU/Gyro](#233-spike-imugyro)
      * [2.3.4 Color Sensor](#234-color-sensor)
* [3.0 Obstacle Management and Software Documentation](#30-obstacle-management-and-software-documentation)
   * [3.1 Open Challenge](#31-open-challenge)
   * [3.2 Obstacle Challenge](#32-obstacle-challenge)
   * [3.3 Camera Usage and Software](#33-camera-usage-and-software)
   * [3.4 Problems Encountered](#34-problems-encountered) 
<br><br><br>

## 1.0 Mechanical Design and Mobility Management

## 1.1 Chassis Architecture
   
## 1.1.1 Tire Selection
&emsp; &emsp; **Rear Wheels:** LEGO Technic Tire 62.4 x 20	

&emsp; <img width="474" height="474" alt="OIP" src="https://github.com/user-attachments/assets/70aab19b-2eb9-4e7c-9320-6dd2b9ac9914" />
<br><br>
   
The rear wheels are responsible for propelling the mass of the robot and resolving the torque distributed by the differential gear. The 62.4 mm x 20 mm tire was selected to optimize linear velocity and traction. <br>

   * **Kinematic Velocity:** Linear speed is directly proportional to wheel radius. At a fixed maximum motor RPM, the larger 62.4 mm diameter significantly increases the vehicle's top straight-line speed compared to standard 43 mm tires.

   * **Differential Synergy & Contact Patch:** A differential prevents wheel scrub by allowing the outer wheel to spin faster during a turn. However, if a tire lacks grip, the differential will dump all torque into the slipping wheel (path of least resistance), stranding the vehicle. The 20 mm width provides a wide, flat contact patch that guarantees sufficient static friction to keep both wheels anchored, ensuring smooth, continuous torque delivery through corners.
<br><br><br><br>

&emsp; &emsp; **Front Wheels:** Integrated Wheel 43 x 14 (Part 65834)

&emsp; <img width="474" height="423" alt="Kolo-Robota-Mindstorms-43x14-1szt-LEGO-65834" src="https://github.com/user-attachments/assets/275e1658-528d-4a80-9907-178f90be9e17" />
<br><br>

The front wheels actuate the Ackermann steering geometry. The priority here is minimizing servo load, eliminating steering hysteresis, and maintaining geometric clearance. The 43 mm x 14 mm integrated wheel is structurally and geometrically superior for this role.

* **Scrub Radius & Servo Torque:** In an Ackermann setup, wheels pivot around a kingpin axis. A wide tire forces the contact patch further away from this pivot point, creating a large "scrub radius." The narrow 14 mm profile keeps the contact patch almost perfectly aligned with the pivot axis. This dramatically reduces the friction force fighting the steering servo, allowing for lightning-fast, micro-adjustments driven by the PID algorithm.

* **Elimination of Sidewall Flex:** Part 65834 is an integrated wheel: the hard rubber tire is permanently molded into the plastic rim. During high-speed cornering, lateral shear forces cause standard 2-piece Lego rubber tires to flex sideways or peel off the rim. This deformation introduces hysteresis (a delay between the servo turning and the car actually changing direction). The solid integration of the 65834 wheel ensures zero sidewall flex, translating servo commands into immediate, mathematically predictable drifts.

* **Spatial Clearance:** The smaller 43 mm diameter allows the wheel to pivot to extreme lock angles without colliding with the chassis walls, tie rods, or ultrasonic sensors mounted at the front of the vehicle.
<br><br><br><br>

## 1.1.2 Motor Configuration
The vehicle's propulsion and directional control are governed by a dual-motor powertrain utilizing a combination of LEGO Technic Large and Medium Angular Motors. These specific models were engineered into the design primarily because they feature internal absolute encoders. This closed-loop hardware feedback allows for high-resolution odometry, ensuring the robot can maintain perfectly straight linear trajectories and execute precise positional tasks with minimal drift. Additionally, their box-like form factor and low-profile wiring harnesses greatly facilitated a clean, tightly integrated chassis build. 
<br><br>

&emsp; &emsp; **LEGO Technic Medium Angular Motor (Vertical)**

&emsp; <img width="474" height="474" alt="R" src="https://github.com/user-attachments/assets/2c7899da-9349-43c7-88ed-be22a46470b5" />
<br>

This motor is oriented vertically and serves as the primary steering actuator for the vehicle. To optimize the chassis footprint, the motor is strategically mounted facing inward toward the center of the chassis rather than protruding outward. This internal orientation was chosen because it ensures the adjacent mounting connections remain static and do not interfere with the dynamic movement of the steering axle. By packing the steering assembly inward, the design significantly reduces the overall longitudinal length of the robot. This compacted wheelbase directly translates to a reduced turning radius, enabling the sharper, high-precision cornering required to navigate around tight obstacles. 
<br><br><br><br>

&emsp; &emsp; **LEGO Technic Large Angular Motor (Horizontal)**

&emsp; <img width="474" height="474" alt="image" src="https://github.com/user-attachments/assets/53c26369-691a-4214-b203-34ed6d8556fa" />
<br>

Mounted horizontally, this unit functions as the primary drive motor for the vehicle's propulsion. By utilizing the larger variant for the drivetrain, the system benefits from higher torque output, which is necessary to overcome the static friction of the vehicle's mass and maintain consistent velocities during the Open and Obstacle Challenges. Its horizontal integration seamlessly couples with the drive axle and differential gear to deliver stable, continuous power to the rear wheels. 
<br><br><br><br>

## 1.2 Drivetrain and Kinematics
   
## 1.2.1 Differential Gear Integration
&emsp; <img width="474" height="301" alt="607458375-cebe4825-b5ef-4ca0-b05a-08d2a869794f" src="https://github.com/user-attachments/assets/b22d56bf-24f5-4cef-884e-422a2e634d44" />
<br>

The vehicle's rear-wheel-drive powertrain incorporates a mechanical differential gear to manage torque distribution from the primary horizontal drive motor to the rear wheels. In autonomous track navigation, fixing both drive wheels to a solid axle results in severe wheel scrubbing during cornering, as the outer wheel is forced to travel a greater distance than the inner wheel in the same amount of time. By integrating a differential, the rear wheels are mechanically decoupled. This allows them to rotate at independent angular velocities while maintaining continuous and balanced power delivery. This design minimizes tire wear, prevents traction loss, and is critical for maintaining highly precise odometry. It ensures that the rotational data from the motor's internal encoder strictly reflects true rolling distance rather than artificial slipping

### **Advantages**
   * **Elimination of Rear Wheel Scrubbing:** Prevents friction-induced torque loss and mechanical drag during sharp cornering.
   * **Reduced Powertrain Strain:** Minimizes shock loading on motor gears by allowing proportional speed distribution across both drive wheels.
   * **Odometry Preservation:** Ensures smooth linear velocity transfer, preventing wheel slip that could otherwise corrupt encoder readings and gyro-assisted path tracking. 
<br><br><br><br>

## 1.2.2 Ackermann Steering Geometry
&emsp; <img width="474" height="252" alt="image" src="https://github.com/user-attachments/assets/5ef04509-f272-4c32-9b1e-0d5f397b7922" />
<br>

To complement the rear differential, the vehicle's front steering assembly employs Ackermann steering geometry. Traditional parallel steering systems force both front tires to maintain identical turning angles, which inevitably causes the inner wheel to drag laterally through tight corners. The Ackermann linkage geometrically corrects this error by ensuring the inner wheel steers at a slightly sharper angle than the outer wheel. This allows all four wheels to trace concentric circles that share a common center point aligned with the rear drive axle.This kinematic alignment completely eliminates lateral tire scrubbing and maximizes the contact patch of the 62.4 x 20 tires. When paired with the differential gear, the Ackermann setup provides exceptionally smooth, high-precision cornering. Furthermore, it drastically reduces the dynamic load and torsional strain on the vertical steering motor, allowing the software's PID control loops to execute instantaneous directional corrections with negligible mechanical resistance.

### **Advantages**
   * **Kinematic Alignment:** During a turn, the inside wheel traces a tighter circle than the outside wheel. The linkage geometry causes the inner wheel to turn at a steeper angle, aligning all four wheel axes toward a single, common point known as the Instantaneous Center of Rotation (ICR).
   * **Friction & Load Reduction:** By ensuring each tire rolls pure-statically along its precise turning arc without lateral dragging, steering resistance is drastically minimized. This reduces the required actuation torque from the steering motor.
   * **High-Precision Cornering:** The combination of an Ackermann front linkage and a differential rear axle enables clean, predictable 90-degree cornering routines, preventing trajectory drift during autonomous obstacle-avoidance maneuvers. 
<br><br><br><br>

## 1.3 Powertrain Analysis

## 1.3.1 Torque and Speed Reasoning
The powertrain is engineered to balance the torque required to accelerate the vehicle's 886 g mass with the maximum linear velocity needed to achieve competitive lap times.

* **Drive Motor (Large Angular):** The LEGO Large Angular Motor outputs significantly higher torque (approx. 15 Ncm running) compared to the medium variant. This torque is critical to overcome both the internal mechanical friction of the differential gear assembly and the static inertia of the 886 g chassis from a standstill.
* **Velocity Translation:** Linear speed is dictated by the motor's RPM and the tire circumference. Coupled with the 62.4 mm rear tires, the large motor (running at a nominal ~175 RPM) yields a theoretical top speed of roughly 0.57 m/s. This configuration prioritizes high top speed on open straightaways while maintaining just enough low-end torque to prevent stalling during tight obstacle maneuvering.
* **Steering Actuation (Medium Angular):** Because the front Ackermann linkage utilizes narrow 14 mm tires to eliminate scrub radius, the steering assembly encounters very little mechanical resistance. Therefore, high torque is unnecessary. The Medium Angular Motor was selected instead for its higher rotational velocity (~250 RPM). This allows the software's PID controller to execute micro-adjustments instantly, drastically reducing steering latency during wall-centering and obstacle avoidance.
<br><br><br>

## 1.4 Mechanical Tradeoffs and Iterations
   
## 1.4.1 Cantilever vs. Braced Rear Wheel Stability

&emsp; &emsp; **Example of Cantilever Wheels**

&emsp; <img width="474" height="267" alt="fde622be1b35c086e08aad69b99be743225c7290Lego-Mindstorms-Ev3-Car-With-Two-Wheel-Drive-Robot-Fllcasts" src="https://github.com/user-attachments/assets/c5eef589-a431-48b8-908f-79f853ae2238" />

&emsp; &emsp; **Example of Braced Wheels**

&emsp; <img width="474" height="267" alt="OIP" src="https://github.com/user-attachments/assets/efd465d3-5719-49b4-8075-3ce7eae6fa8e" />

Initial rear-drive prototypes utilized a cantilever wheel configuration to minimize track width and simplify direct-drive motor coupling. However, testing revealed that the unsupported axles suffered from deflection under the weight of the rear chassis components. This resultant axle wobble compromised the tire contact patches and introduced unpredictable micro-drifts into straight-line odometry
<br><br>
To resolve this kinematic instability, the rear drivetrain was redesigned to have braced wheels. This transition required a deliberate engineering tradeoff: adopting a braced framework inherently increases the vehicle's overall footprint and introduces outer hardware edges that risk catching on track borders. However, the team determined that these spatial penalties were necessary to secure mechanical reliability. By supporting both ends of the axle within a rigid fork, the new configuration maintained strict vertical wheel alignment under load, providing the absolute rigidity required for consistent rear traction and accurate sensor-driven navigation.
<br><br><br><br>

## 1.5 Assembly and Bill of Materials (BOM)
   
## 1.5.1 Building Instructions
<img width="450" alt="1_1x" src="https://github.com/user-attachments/assets/9cf4a0f4-46bc-46fc-b5e6-03cf4d21febb" />
<img width="450" alt="2_1x - Copy" src="https://github.com/user-attachments/assets/1b88cf9b-ab1b-4231-9170-d0695a8744ca" />
<img width="450" alt="3_1x - Copy" src="https://github.com/user-attachments/assets/fbacf456-a4e4-4898-bfb3-af05dad62f3e" />
<img width="450" alt="4_1x - Copy" src="https://github.com/user-attachments/assets/3439bc68-b10e-4611-aae0-bcc06a4bc240" />
<img width="450" alt="5_1x - Copy" src="https://github.com/user-attachments/assets/fe21f8a7-5ee6-4b7e-ab1f-bf75235006ff" />
<img width="450" alt="6_1x - Copy" src="https://github.com/user-attachments/assets/69e20950-959b-47c8-b76e-73dc221e558e" />
<img width="450" alt="7_1x - Copy" src="https://github.com/user-attachments/assets/2cc913ab-5ea4-435e-b8c3-f4f157a9e2de" />
<img width="450" alt="8_1x - Copy" src="https://github.com/user-attachments/assets/d69d6479-92c8-4032-aebc-294ff38e2ce1" />
<img width="450" alt="9_1x - Copy" src="https://github.com/user-attachments/assets/cf716722-908b-4516-b5e9-7fd505156cb2" />
<img width="450" alt="10_1x - Copy" src="https://github.com/user-attachments/assets/31b8c794-0506-4937-9ce6-b45e5fd7ec2d" />
<img width="450" alt="11_1x - Copy" src="https://github.com/user-attachments/assets/ed2b9215-ad41-44c3-b43b-2645a573cfec" />
<img width="450" alt="12_1x - Copy" src="https://github.com/user-attachments/assets/f6c6202e-0aa2-4f0d-b6de-b69dcfe456c2" />
<img width="450" alt="13_1x - Copy" src="https://github.com/user-attachments/assets/1f1d334b-042e-4fa3-8eac-0c594fe75948" />
<img width="450" alt="14_1x - Copy" src="https://github.com/user-attachments/assets/51b05397-3399-44b7-ad52-660146a20b7a" />
<img width="450" alt="15_1x - Copy" src="https://github.com/user-attachments/assets/9ba8b765-2bfc-425e-9dcb-a5457190b4b0" />
<img width="450" alt="16_1x - Copy" src="https://github.com/user-attachments/assets/123d8042-9665-45b9-ae24-491ea6ae84db" />
<img width="450" alt="16_1x - Copy" src="https://github.com/user-attachments/assets/bac4650b-0aa5-4701-82ab-ae680200b46d" />
<img width="450" alt="17_1x - Copy" src="https://github.com/user-attachments/assets/9f1d35f3-4ae2-4915-808f-760593a2c2e9" />
<img width="450" alt="18_1x - Copy" src="https://github.com/user-attachments/assets/bdc4631e-b03d-4399-891e-eb88e46d1653" />
<img width="450" alt="19_1x - Copy" src="https://github.com/user-attachments/assets/1ac44692-5d84-494e-93d1-697cac1fb8c8" />
<img width="450" alt="20_1x - Copy" src="https://github.com/user-attachments/assets/f3a6b966-f5cf-4460-8974-1fed89345853" />
<img width="450" alt="21_1x - Copy" src="https://github.com/user-attachments/assets/e8ce2c4b-350a-4b5d-8a37-e93d7e93ad56" />
<img width="450" alt="22_1x - Copy" src="https://github.com/user-attachments/assets/f6a54867-f0b4-4a6f-a0f7-ff62d0e08ca5" />
<img width="450" alt="23_1x - Copy" src="https://github.com/user-attachments/assets/8d729189-8f28-4078-819b-d57457c13771" />
<img width="450" alt="24_1x - Copy" src="https://github.com/user-attachments/assets/ad436e90-71d7-43cf-9866-584f2bd54402" />
<img width="450" alt="25_1x - Copy" src="https://github.com/user-attachments/assets/948f33ee-07c2-43fe-8d63-1683eb2b762e" />
<img width="450" alt="26_1x - Copy" src="https://github.com/user-attachments/assets/5c924007-c50d-40a8-a71d-70aae03895cd" />
<img width="450" alt="27_1x - Copy" src="https://github.com/user-attachments/assets/52e337f2-502a-4edd-8d12-ed86d1e4342c" />
<img width="450" alt="28_1x - Copy" src="https://github.com/user-attachments/assets/e5c0aed0-417e-4801-b71c-9a7aa8faea76" />
<img width="450" alt="29_1x - Copy" src="https://github.com/user-attachments/assets/b77ef906-46e1-47f3-9cdc-04f9cfeab98f" />
<img width="450" alt="30_1x - Copy" src="https://github.com/user-attachments/assets/f5724db1-63fa-49c5-a4a4-41c5abbea34d" />
<img width="450" alt="31_1x - Copy" src="https://github.com/user-attachments/assets/56fbc6ba-fe3f-45bf-b786-07644059d9d7" />
<img width="450" alt="32_1x - Copy" src="https://github.com/user-attachments/assets/94d8713a-d8d4-49df-a788-ef994b18a90b" />
<img width="450" alt="33_1x - Copy" src="https://github.com/user-attachments/assets/1ed6705b-fb51-4fd1-a356-319c5b2e1830" />
<img width="450" alt="34_1x - Copy" src="https://github.com/user-attachments/assets/67f3ff31-6687-4884-a08a-24cfdedde857" />
<img width="450" alt="35_1x - Copy" src="https://github.com/user-attachments/assets/3e3cca88-010a-4455-95e6-340d709c9834" />
<img width="450" alt="36_1x - Copy" src="https://github.com/user-attachments/assets/b09163fa-9a3c-4227-941b-d6a8c6303a0f" />
<img width="450" alt="37_1x - Copy" src="https://github.com/user-attachments/assets/93327e76-60e2-4fde-8780-825b40d6ecd9" />
<img width="450" alt="38_1x - Copy" src="https://github.com/user-attachments/assets/5e947560-29c1-4025-907f-603dfeb1d8ef" />
<img width="450" alt="39_1x" src="https://github.com/user-attachments/assets/2fbabe39-a8a7-4efa-b7dc-e291b2f337fb" />
<img width="450" alt="40_1x" src="https://github.com/user-attachments/assets/3b248551-4b5e-4fc4-89dd-8bbf53cf99d7" />
<img width="450" alt="41_1x" src="https://github.com/user-attachments/assets/e1f83237-6904-4d7c-a908-2ed97643c2d1" />
<img width="450" alt="42_1x" src="https://github.com/user-attachments/assets/369534e9-176d-4f8b-800b-301811675b3b" />
<img width="450" alt="43_1x" src="https://github.com/user-attachments/assets/a7e8a90b-b025-4803-b6ad-de1109d20916" />
<img width="450" alt="44_1x" src="https://github.com/user-attachments/assets/b0ab6af2-880b-4c81-935d-c2eb1c4980d6" />
<img width="450" alt="45_1x" src="https://github.com/user-attachments/assets/f06a9e80-644c-4943-ba21-c2f274eddb76" />
<img width="450" alt="46_1x" src="https://github.com/user-attachments/assets/c4ce4af1-2aaa-43c1-9ed2-3b6ee3016703" />
<img width="450" alt="47_1x" src="https://github.com/user-attachments/assets/634cc96c-3d4b-4597-b112-e98f1447aa62" />
<img width="450" alt="48_1x" src="https://github.com/user-attachments/assets/016dc344-3833-4ca1-9b3b-9cf25a3b3448" />
<img width="450" alt="49_1x" src="https://github.com/user-attachments/assets/abf91385-4cc0-42c3-8f14-1ed97f9f427a" />
<img width="450" alt="50_1x" src="https://github.com/user-attachments/assets/d1354895-958b-4416-9518-f17616e7f5b4" />
<img width="450" alt="51_1x" src="https://github.com/user-attachments/assets/6f1bdfd3-a5a3-4046-87f3-20ea6924acf4" />
<img width="450" alt="52_1x" src="https://github.com/user-attachments/assets/6210cb4b-6d32-4b32-b318-cee51fee3669" />
<img width="450" alt="53_1x" src="https://github.com/user-attachments/assets/ab682197-8ebd-450f-9faa-75dd08e7c616" />
<img width="450" alt="54_1x" src="https://github.com/user-attachments/assets/dc7c17d5-91ec-49f8-88a9-9aabec9b1641" />
<img width="450" alt="55_1x" src="https://github.com/user-attachments/assets/efb4776f-e2a1-46f9-8ed5-113fcaeb9d3c" />
<img width="450" alt="56_1x" src="https://github.com/user-attachments/assets/ed14838d-02ba-47f3-8b26-02bb0ed4b1dd" />
<img width="450" alt="57_1x" src="https://github.com/user-attachments/assets/bf8f6dd3-efbf-43aa-b0e2-eddf2633772f" />
<img width="450" alt="58_1x" src="https://github.com/user-attachments/assets/6adcfd65-28f7-4cd2-a459-708f775eedf3" />
<img width="450" alt="59_1x" src="https://github.com/user-attachments/assets/2ea14d57-3946-4b39-bfc7-6fc1b38c8651" />
<img width="450" alt="60_1x" src="https://github.com/user-attachments/assets/34674dad-d7f7-4e4e-860d-45f92d660719" />
<img width="450" alt="61_1x" src="https://github.com/user-attachments/assets/c2df2fb3-26d3-42d5-9f78-bd45035a490c" />
<img width="450" alt="62_1x" src="https://github.com/user-attachments/assets/1b5dff2a-ca40-4cee-99a6-220c63074417" />
<img width="450" alt="62_1x" src="https://github.com/user-attachments/assets/f478baee-47ec-4205-9273-10e860be9431" />
<img width="450" alt="63_1x" src="https://github.com/user-attachments/assets/bb05a73f-2473-4051-ae63-a9681995db8f" />
<img width="450" alt="64_1x" src="https://github.com/user-attachments/assets/fb22f0ed-f202-4d80-9583-bd9a88fac883" />
<img width="450" alt="65_1x" src="https://github.com/user-attachments/assets/ff719aeb-e852-44f7-9892-28649a2781ee" />
<img width="450" alt="66_1x" src="https://github.com/user-attachments/assets/0b0784d1-cfa9-4831-9b8e-7a7fa3a90657" />
<img width="450" alt="67_1x" src="https://github.com/user-attachments/assets/34fe2b71-80b3-408c-945f-13e4f0ee1afd" />
<img width="450" alt="68_1x" src="https://github.com/user-attachments/assets/019ff5fd-6c5c-4ea5-b3c0-691c61697e55" />
<img width="450" alt="69_1x" src="https://github.com/user-attachments/assets/feccb713-e8c8-4cdd-a114-e07bd40d0fc5" />
<img width="450" alt="70_1x" src="https://github.com/user-attachments/assets/6da16154-808f-4da5-8b9c-28b8011c233b" />
<img width="450" alt="71_1x" src="https://github.com/user-attachments/assets/e7072da9-e707-4e1f-9c60-63f0eb829247" />
<img width="450" alt="72_1x" src="https://github.com/user-attachments/assets/7c5f6e8f-594d-462c-a3f7-ed0ae50de57c" />
<img width="450" alt="73_1x" src="https://github.com/user-attachments/assets/83dc1f64-c2e7-448a-806a-fe4829db8f97" />
<img width="450" alt="74_1x" src="https://github.com/user-attachments/assets/0a0a28d3-9062-457d-892d-ebe69b95cb76" />
<img width="450" alt="75_1x" src="https://github.com/user-attachments/assets/cdbd6d95-8013-4114-bb5a-e23b94ca078a" />
<img width="450" alt="76_1x" src="https://github.com/user-attachments/assets/27add380-357b-4a66-9270-c85a163070b8" />
<img width="450" alt="77_1x" src="https://github.com/user-attachments/assets/1f4ce2c3-d6b7-4512-8104-bb9cd7ad05de" />
<br><br>

## 1.5.2 Complete Component List

### Lego Components
<img width="249" height="177" alt="Picture7" src="https://github.com/user-attachments/assets/6e5b7dd4-6cb7-47a7-8916-acbbf04c8bb7" />
<img width="220" height="156" alt="Picture6" src="https://github.com/user-attachments/assets/15a6240f-c532-45d9-8d8c-6f6a3b5269b0" />
<img width="244" height="173" alt="Picture5" src="https://github.com/user-attachments/assets/556f400a-c753-41cd-90a4-45a5cdf0bc10" />
<img width="259" height="183" alt="Picture4" src="https://github.com/user-attachments/assets/3a29a269-a642-411c-980e-7a809dcd8b1f" />
<img width="230" height="161" alt="Picture3" src="https://github.com/user-attachments/assets/74b8dfe5-9efa-4b74-9200-f134809c2eb6" />
<img width="220" height="156" alt="Picture2" src="https://github.com/user-attachments/assets/cd208dd6-7398-4e76-8084-0b48bfbd3bd7" />
<img width="238" height="169" alt="Picture1" src="https://github.com/user-attachments/assets/9de5f27b-ffba-4bc2-b70f-1837f9cea481" />
<br>

### Other Components
<br>
#### Voltage Regulator <br>
<img width="205" height="136" alt="Picture10" src="https://github.com/user-attachments/assets/f4aed760-356f-4cb2-9912-dee6fbebd2a8" />
<br>

#### Wide Angle Lens <br>
<img width="156" height="145" alt="Picture9" src="https://github.com/user-attachments/assets/28db39ec-c644-4b91-9389-bbdaed96294a" />
<br>

#### DSLONG LED Fill Light <br>
<img width="159" height="212" alt="Picture8" src="https://github.com/user-attachments/assets/1df6cec3-565e-4f8b-8302-e6c1c7018a47" />
<br>
#### 3D printed Camera case<br>
<img width="30%" alt="798414015_1753964069870121_956414356854542009_n" src="https://github.com/user-attachments/assets/9abb7506-9384-43ff-b550-2dec25369634" />



## 2.0 Power and Sense Management

## 2.1 Power Distribution

## 2.1.1 LEGO SPIKE Hub Battery
&emsp; <img width="474" height="474" alt="leg45612_lego-education-spike-small-hub-battery" src="https://github.com/user-attachments/assets/e56980f2-9fc3-41e5-9584-37145c15c929" />

The LEGO SPIKE hub battery is a rechargeable lithium-ion battery designed for use with Technic Large Hub and SPIKE Prime Set.

### **Specifications:**
* **Capacity:** 2100 mAh
* **Normal Voltage:** 7.3 V 
* **Standard Discharge:** 0.2C (~420 mA)
* **Standard Charge Current:** 500 mA (~3 hour charging time)
* **Weight:** 110 g (~6.7 oz)

### **Reason For Selection**
* **Regulated and Stable Voltage Output -** The SPIKE Prime battery features integrated power management circuitry that keeps a steady nominal voltage (7.3 V).
* **Lightweight Footprint:** The battery itself is 110 g, which helps minimize the overall mass of the robot (886 g). Lower weight reduces the inertial load on the powertrain, allowing for sharper cornering and faster acceleration without causing wheel slip.
* **Seamless Integration:** It slots directly into the Hub, avoiding the need for heavy, messy external wiring for the primary processing and motor controls. This keeps the chassis compact and the center of gravity predictable.
<br><br><br>

## 2.1.2 External Power
&emsp; <img width="474" height="703" alt="download" src="https://github.com/user-attachments/assets/260204ea-6f0d-4b89-9f3c-6e23670fbb9b" />
<br>
Three 1.5 V Lithium Ion Batteries in series.
<br>
### **Specifications:**
* **Capacity:** 2700 mAh
* **Normal Voltage:** 4.5 V 
* **Weight:** 110 g (~6.7 oz)

### **Reason For Selection**
* **Isolated High-Draw Circuit:** The OpenMV H7 Plus (up to 250 mA) and the DSLONG LED Fill Light (~1556 mA) draw a massive combined current. Routing this load through the SPIKE Hub would exceed its standard discharge limits, risking sudden voltage sags, hub resets, or severe disruption to the motor encoders.
* **Consistent Vision Lighting:** Supplying an isolated 4.5 V to the LED fill light ensures constant, flicker-free illumination. Because the OpenMV camera is configured with locked auto-exposure and fixed white balance, any dimming caused by the drive motors drawing shared power would instantly corrupt the camera's color thresholding.
* **Additional Capacity & Hub Preservation:** Offloading the vision and lighting systems entirely from the SPIKE battery ensures the Hub's capacity is strictly reserved for locomotion and calculation, guaranteeing consistent speed and lap times across multiple consecutive runs.
<br><br><br>

## 2.2 Wiring & Schematics

## 2.2.1 LEGO SPIKE Hub
&emsp; <img width="474" height="267" alt="image" src="https://github.com/user-attachments/assets/7cd1c827-653c-43bc-8e90-e0c15cc2a3eb" />
<br><br>
### **Power Consumption**

| **Component** | **Voltage** | **Current** | **Standard Discharge** |
|---|---|---|---|
| Color Sensor | 3.3 V | ~20 mA - 50 mA | ~35 mA |
| Large Angular Motor | ~6.0 V - 8.4 V <br> (nominally ~7.3) | 135 mA - 1400 mA <br> (depends on load) | ~300 mA - 500 mA |
| Medium Angular Motor | ~6.0 V - 8.4 V <br> (nominally ~7.3) | 110 mA - 800 mA <br> (depends on load) | ~150 mA - 250 mA |
| OpenMV H7 Plus | 3.3 V | 0 mA (not drawing power) | 0 mA |
| Ultrasonic Sensor | 3.3 V | ~30 mA - 50 mA | ~40 mA |

<br>

The total continuous discharge of the components on the SPIKE PRIME Hub Battery is approximately 675 mA to 1000 mA (including SPIKE Hub processor and bluetooth consumption). The expected runtime is 2.4 hours (2100 mAh / 850 mA (average draw) = 2.4 hrs).

<br><br><br>

## 2.2.2 External Wiring
&emsp; <img width="474" height="321" alt="image" src="https://github.com/user-attachments/assets/adc3bb63-2212-42c7-aab8-461524ca5062" />
<br><br>
### **Power Consumption**

| **Component** | **Voltage** | **Current** | **Standard Discharge** |
|---|---|---|---|
| OpenMV H7 Plus | 4.5 V | 100 mA - 250 mA | ~150 mA - 180 mA |
| Fill Light | 4.5 V | ~1556 mA | ~1556 mA |

<br><br><br>

## 2.3 Sensor Integration
The autonomous navigation system uses deterministic sensor fusion. Processing loads are distributed across specialized sensors utilizing hardware-level calibration and software noise filtering to ensure highly predictable performance without single points of failure.

## 2.3.1 OpenMV H7 Plus
&emsp; <img width="474" height="255" alt="image" src="https://github.com/user-attachments/assets/c91ce047-27c4-4791-b2c8-deac86066037" />

The primary optical processor identifies traffic signs (Red/Green blocks) and boundary markers (black walls) at 320x240 resolution.

* **Environmental Calibration:** Auto-gain, auto-exposure, and auto-white-balance are explicitly disabled at initialization. Locking these hardware parameters ensures LAB color space thresholds remain absolute, preventing vision failures from ambient lighting shifts.

* **Dynamic Regions of Interest (ROI):** To maximize inference speed, the field of view is cropped into task-specific ROIs: a narrow central strip for corner detection and a wide lower strip for obstacle tracking.
  
* **Perspective-Based Depth Estimation:** Due to the camera's downward mounting angle, Y-coordinates act as physical depth proxies. Objects lower on the image plane are physically closer to the chassis, allowing the software to consistently prioritize the nearest obstacle..
<br><br><br>

## 2.3.2 Ultrasonic Sensors
&emsp; <img width="474" height="355" alt="image" src="https://github.com/user-attachments/assets/859bd0fe-219a-4946-9edc-b9a1ddabc210" />

Two lateral SPIKE Ultrasonic sensors continuously map the track's inner and outer boundary walls to drive the open-lane navigation logic.

* **Noise Filtering:** Ultrasonic sensors occasionally register false distance readings due to stray echoes. To prevent these random spikes from disrupting the steering, the system rapidly takes three distance samples, sorts them, and uses the middle (median) value. This guarantees the robot ignores sudden, inaccurate data before it affects navigation.

* **Error Vector Calculation:** Filtered distance arrays feed directly into the steering PID controller. The steering error is calculated as distance from the right wall minus the distance from the left wall. A zero error indicates perfect centering, enabling oscillation-free lane keeping.
<br><br><br>

## 2.3.3 Spike IMU/Gyro
&emsp; <img width="474" height="267" alt="image" src="https://github.com/user-attachments/assets/7434012e-9a58-4b25-8303-06e1ccf652ef" />

The Hub's built-in 6-axis IMU provides absolute heading and turning odometry, independent of wheel slip.

* **Closed-Loop Cornering:** Upon corner detection, ultrasonic tracking is temporarily suspended. A dedicated PID loop takes over, reading real-time yaw data to execute a precise 90-degree Ackermann turn while dynamically decelerating the drive motor to maintain traction.

* **Momentum Compensation:** To account for chassis inertia, the turning sequence is programmed to terminate early. The target angle is offset by 14 degrees. This allows the vehicle's physical momentum to carry it smoothly through the remaining rotation into perfect orthogonal alignment.
<br><br><br>

## 2.3.4 Color Sensor
&emsp; <img width="474" height="316" alt="image" src="https://github.com/user-attachments/assets/f6c55940-951c-42bc-9640-bf7ebd2f09f8" />

Mounted vertically facing the track floor, this sensor acts strictly as a hardware-level safety trigger to eliminate false positives from the vision system.

* **Corner Detection Authorization:** Shadows or track scuffs can occasionally trick the OpenMV camera into flagging a false corner. To prevent catastrophic early turns, the vehicle is mathematically locked out of cornering until the color sensor detects a colored lane boundary (Orange for Clockwise routing, Blue for Counter-Clockwise). Crossing this line acts as a hardware interlock, successfully arming the vision system to accept the next corner flag.
<br><br><br>

## 3.0 Obstacle Management and Software Documentation

## 3.1 Open Challenge
To navigate the Open Challenge track, the vehicle integrates 2 ultrasonic sensors, an OpenMV camera module, and the SPIKE Hub’s internal IMU (gyroscope).

* **Track Navigation & Wall-Centering:** The robot utilizes a proportional-integral-derivative (PID) controller fed by the left and right ultrasonic sensors to calculate real-time error, dynamically adjusting steering to keep the vehicle centered between walls.

* **Corner Detection:** A central Region of Interest (ROI) configured on the OpenMV camera monitors the track ahead. When the camera detects a black corner boundary—and confirms a color line crossing—it triggers the turn sequence.

* **Directional Decision & Turning:** The turn direction (clockwise vs. counter-clockwise) is determined by comparing the differential distance read by the left and right ultrasonic sensors. The vehicle executes a controlled, reverse-steering maneuver, using gyro-based heading feedback to complete a precise 90-degree turn.

* **Lap Tracking & Finish:** Each completed turn increments the global variable num_turn. The PID loop maintains heading stability using absolute IMU values throughout the run. Once num_turn reaches 12 (completing 3 full laps across 4 corners), the turning routine disengages and the vehicle drives forward under PID control back across the finish line.

&emsp; <img width="70%" alt="Untitled Diagram drawio_page-0001" src="https://github.com/user-attachments/assets/4eb3d02e-a88e-4a4b-9331-e58ade7158f8" />


```python
p = PUPRemoteHub(Port.D)
p.add_command("msg", to_hub_fmt="repr", from_hub_fmt="repr")
p.add_channel('cam', to_hub_fmt='bhhb')
```
PUPRemoteHub connects the hub to an external OpenMV camera via Port D. It sets up a command channel called 'cam' to receive 4 variables packaged as binary data.
```python
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
```
To avoid reading random spikes from the ultrasonic sensors, this function takes 3 quick distance samples, sorts them in ascending order, and extracts the middle value (median). This completely discards outlier anomalies.
```python
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
```
* remote_engine: Keeps communication alive with the OpenMV camera.

* update_robot_data: Constantly populates a global dictionary (rob_data) every 20 milliseconds with refreshed telemetry: camera tracking data (color, block_x, corner), IMU gyro heading, color sensor color, and filtered ultrasonic distances.
```python
async def ultrasonic_PID(kp=0.075, ki=0.000001, kd=10000.0, minPower=900, maxPower=1100):
    global sum_error, prev_error, max_steer, direction, num_turn
    global rob_data, steer_center, speed_center

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
                    
        await wait(100)
    
    # set speed to 0 to stop robot from moving
    speed_center = 0
```
The Error for the PID is calculated by subtracting the left wall distance from the right wall distance. If the robot is perfectly centered, the error is 0.

This function also gives the robot **dynamic speed**. The function slows the robot down dynamically if the error is large (approaching a wall) and speeds up to maximum power when the error is low (driving perfectly straight).
```python
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

    while True:
        if rob_data["corner"] == 1 and not is_sequencing and can_sense_corner:  # corner wall
            is_sequencing = True
            speed_sequence = 0
            await hub.speaker.beep()
            
            if direction == 0:
                if rob_data['ultra_L'] > rob_data['ultra_R']: # left corner turn
                    direction = -1
                elif rob_data['ultra_L'] < rob_data['ultra_R']: # right corner turn
                    direction = 1
                
            if direction == -1:
                steer_sequence = -75 # left turn
            elif direction == 1:
                steer_sequence = 75 # right turn

            # reduce the turn amount to stop momentum from increasing the turn
            while abs(rob_data['heading']) < (90 * num_turn - 14):
                turn90_pid(num_turn, forward=True, maxP=1000, minP=300)                
                await wait(1)

            num_turn += 1
            # crucial for knowing how many laps the robot did
            
            steer_sequence = 0
            speed_sequence = 0
            is_sequencing = False
            can_sense_corner = False
            
        await wait(50)
```
* detect_corner: Waits until the OpenMV camera sets corner == 1 and a color lane line has been crossed (can_sense_corner).

Once triggered, it locks out normal wall-following (is_sequencing = True) and forces a hard turn (75 or -75 steering angle) while dynamically calculating speed using turn90_pid based on the internal Gyro heading.

Momentum Compensation: It cuts the turn sequence short by 14 degrees (90 * num_turn - 14) because the physical weight and speed of the robot will cause it to drift smoothly through the remaining 14 degrees.
```python
async def sense_line_color():
    global can_sense_corner

    while True:
        # can_sense_corner allows the robot to turn at the corner
        if rob_data['line_color'] == 1 and (direction == 0 or direction == 1): # orange clockwise
            can_sense_corner = True
            await hub.speaker.beep(100)
        elif rob_data['line_color'] == 2 and (direction == 0 or direction == -1): # blue counter-clockwise
            can_sense_corner = True
            await hub.speaker.beep(100)
        
        await wait(20)
```
To ensure the camera doesn't accidentally trigger a corner turn sequence in the middle of a straightaway due to a visual glitch, This function forces the robot to physically cross a colored line (Orange for clockwise tracks, Blue for counter-clockwise tracks) before it is permitted to execute a corner turn.
```python
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
```
This function acts as the multiplexer. It checks if the robot is currently executing a corner turn (is_sequencing). If it is, it feeds the corner variables to the motors. If not, it feeds the wall-following PID values (steer_center, speed_center) to the motors.
```python
async def main():
    # Run tasks concurrently
    await multitask(
        remote_engine(), 
        update_robot_data(), 
        detect_corner(),
        sense_line_color(),
        ultrasonic_PID(kp=0.0005, ki=0.0000001, kd=1.0),
        motor_controller(),
        race=True
        # if even one function stops, all function stops
    )

    car.drive_speed(0)
    car.steer(0)
    gc.collect() # <--- Force a full memory clear here!
    await wait(10) # Give the hub a moment to breathe

    rear.reset_angle(0)
    while rear.angle() < 1850:
        await UltrasonicPID_2Sensor_C(num_turn=13, kp=0.075, ki=0.000001, kd=1.0, max_steer=20, gyro_angle_correct=25, with_gyro=True)
        gc.collect()
        
    car.drive_speed(0)
```
* race=True: This Pybricks feature means that if any single task ends, all tasks are stopped. The ultrasonic_PID loop ends when num_turn > 12 (meaning the robot has finished 3 full laps of a 4-corner track).

Once the multitasking race finishes, the car drops out of the concurrent loop, stops, fires gc.collect() to free memory, and runs a standalone function (UltrasonicPID_2Sensor_C) utilizing gyro correction angles to smoothly drive forward exactly 1850 motor degrees back across the starting finish line to complete the run.
<br><br><br>

## 3.2 Obstacle Challenge
For the obstacle challenge, the robot uses a code similar to the open challenge. The camera has another roi that takes up half of the camera to detect an approaching obstacle and its color. The robot uses the ultrasonic sensors to determine which direction it needs to face after leaving the parking lot. The robot uses pid to face straight forward. When a block enters the roi, the camera also detects its color. By using the x coordinate and the color of the obstacle, the robot is able to maneuver away from the obstacle. To avoid detecting corner blocks that cause the robot to face the wrong direction, we utilized the orange and blue lines of the track. When the robot passes the orange or blue line, the robot will ignore the obstacle until it makes a turn. The robot will repeat this until num_turn is equal to 12. When num_turn reaches 12, the robot will align itself using the walls and execute a parallel parking.

&emsp; <img width="100%"  alt="Untitled Diagram oc drawio_page-0001" src="https://github.com/user-attachments/assets/216c2a1c-e014-44f7-8426-ec3c51461759" />


**Logic and Behavoir**
```python
p = PUPRemoteHub(Port.D) # Connection to an external openMV/SPIKE camera hub
p.add_command("msg", to_hub_fmt="repr", from_hub_fmt="repr")
p.add_channel('cam', to_hub_fmt='bhhb')
```
PUPRemoteHub handles data streaming from an external smart camera over a serial port. This camera passes information regarding obstacle colors, coordinates, and corner signs.
```python
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
```
Ultrasonic sensors are prone to occasional noise or random spikes. Both getMedianR and getMedianL take 3 rapid readings, sort them, and pick the middle value (median filter). This ensures smooth, reliable data for the steering logic.

```python
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
```
These asynchronous loops run constantly in the backround using Python uasyncio:

* remote_engine(): Keeps the communication channel with the camera active.

* update_robot_data(): Constantly refreshes the robot’s telemetry—its IMU (gyro) heading, line colors, ultrasonic distances, and camera tracking metrics—saving them into a global dictionary called rob_data.

* motor_controller(): Acts as a safety/priority switchboard. If the robot is executing a strict maneuver (like avoiding a block or taking a corner), is_sequencing is true, and it takes commands from steer_sequence. Otherwise, it defaults to steer_center (basic wall-centering).

```python
async def get_out_parking():
    global direction
    # Auto detect layout orientation
    if await getMedianR(3) > await getMedianL(3): 
        direction = 1
    else: 
        direction = -1

    # Scale initial steering angle directly based on track direction
    car.steer(75 * direction)
    await wait(100)
    while abs(hub.imu.heading()) < 65:
        car.drive_speed(500)
        await wait(10)
    car.drive_speed(0)
    car.steer(0)
    await wait(100)
    rear.reset_angle()
    while rear.angle() < 1000:
        car.drive_speed(800)
        await wait(10)
    car.drive_speed(0)
    car.steer(75 * direction)
    await wait(100)
    
    # Watch gyro orientation bound dynamically 
    while (direction == 1 and hub.imu.heading() > 10) or (direction == -1 and hub.imu.heading() < -10):
        car.drive_speed(-500)
        await wait(10)
    car.drive_speed(0)
    car.steer(0)
```
This function runs immediately at launch. It reads the left and right sensors to see which wall is further away, automatically determining if the track runs clockwise (direction = 1) or counter-clockwise (direction = -1). It then performs a hard-coded swing maneuver to clear the starting stall and align with the track.
```python
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
            if abs_error <= 5: 
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
```
This function uses a PID controller tied to the internal gyro (hub.imu.heading()) to seamlessly execute a precise 90-degree corner turn. It slows down dynamically as it reaches its target heading to avoid overshooting.
```python
async def parallel_parking():
    await hub.speaker.beep(100,500)
    await wait(500)
    await hub.speaker.beep(100,500)

    global num_turn, speed_sequence, steer_sequence
    global distance_wall, direction

    hub.imu.reset_heading(0)
    rear.reset_angle(0)
    if direction == 1:
        while rear.angle() > -100:
            await straight_backward()
            await wait(10)
    if direction == -1:
        while rear.angle() > -100:
            await straight_backward()
            await wait(10)
    car.drive_power(0)
    car.steer(0)
    await wait(500)
    hub.speaker.beep(600,100)
    await last_turn()
    car.steer(0)
    car.drive_power(0)
    await wait(100)

    rear.reset_angle(0)
    car.steer(0)
    hub.imu.reset_heading(0)
    if direction == 1:
        while rear.angle() > int(-(distance_wall * 2.5)):
            await straight_backward() 
            await wait(10) 
    if direction == -1:
        while rear.angle() > int(-(distance_wall * 3.5)):
            await straight_backward() 
            await wait(10)
    car.drive_power(0)
    await wait(100)
    
    hub.imu.reset_heading(0)
    car.steer(0)
    await wait(100)
    rear.reset_angle(0)
    if direction == 1:
        while rear.angle() < 3330:
            await straight_forward()
            await wait(10)
    if direction == -1:
        while rear.angle() < 3325:
            await straight_forward()
            await wait(10)
    car.drive_power(0)
    rear.reset_angle(0)
    await wait(100)
    
    # difference in value from the location of the differential
    if direction == 1:
        car.steer(-75 * direction)
        while rear.angle() > -460:
            car.drive_power(-200)
            await wait(10)
        car.drive_power(0)
        await wait(200)
        car.steer(75 * direction)
        
        await wait(200)
        while rear.angle() > -1070:
            car.drive_power(-200)
            await wait(10)
            if (direction == 1 and hub.imu.heading() <= 7):
                break
    if direction == -1:
        car.steer(-75 * direction)
        while rear.angle() > -460:
            car.drive_power(-200)
            await wait(10)
        car.drive_power(0)
        await wait(200)
        car.steer(75 * direction)
        
        await wait(200)
        while rear.angle() > -1200:
            car.drive_power(-200)
            await wait(10)
            if (direction == -1 and hub.imu.heading() >= -2):
                break
            
    car.drive_power(0)
    await wait(500)
    car.steer(0)
    await wait(500)
```
parallel_parking is a long, sequential function triggered at the very end of the race (after 12 turns/3 laps). It uses a sequence of timed straight reverses, a 90-degree pivot (last_turn()), and calculated back-and-forth S-turns to cleanly park the vehicle inside the designated finish zone.
```python
def avoid_blocks(color=0, kp=0.5, ki=0.000001, kd=0.1, bl_x=0.0, bl_y=0.0, max_steer_obs=55):
    global sum_Rerror, prev_Rerror, sum_Gerror, prev_Gerror
    global steer_sequence, speed_sequence, turn_right, turn_left
    
    Rerror = 65 - bl_x
    Gerror = 290 - bl_x     
    current_error = 0 
    
    if color == 2:  # Red block
        current_error = Rerror
        prop = kp * Rerror 
        sum_Rerror += Rerror
        integral = ki * sum_Rerror 
        if integral > 10.0: integral = 10.0
        derivative = kd * (Rerror - prev_Rerror) 
        compensation = prop + integral + derivative
        prev_Rerror = Rerror
        if compensation > max_steer_obs: compensation = max_steer_obs
        elif compensation < -max_steer_obs: compensation = -max_steer_obs
        
        steer_sequence = -compensation
        speed_sequence = -(45 / 28) * (abs(Rerror) - 1120 / 3) 
        turn_left = True
        turn_right = False
        
    elif color == 1:  # Green block
        current_error = Gerror
        prop = kp * Gerror 
        sum_Gerror += Gerror
        integral = ki * sum_Gerror 
        if integral > 10.0: integral = 10.0
        derivative = kd * (Gerror - prev_Gerror)
        compensation = prop + integral + derivative
        prev_Gerror = Gerror
        if compensation > max_steer_obs: compensation = max_steer_obs
        elif compensation < -max_steer_obs: compensation = -max_steer_obs
        
        steer_sequence = -compensation
        speed_sequence = -(45 / 28) * (abs(Gerror) - 1120 / 3)  
        turn_right = True
        turn_left = False
```
This function is used when it detects a block near it (color == 2 for Red, color == 1 for Green). This function calculates a PID error based on where the block is horizontally (bl_x) relative to safe zones (65 for Red, 290 for Green). It swerves the car away from the block.
```python
def position_to_center(position_target, p_error, kp=6, ki=0.000001, kd=1.0, max_steer=40):
    global sump_error, prevp_error, num_turn
    global steer_sequence, speed_sequence
    p_error = position_target - hub.imu.heading()
    prop = kp * p_error 
    sump_error += p_error
    integral = ki * sump_error 
    if integral > 10.0: integral = 10.0
    elif integral < -10.0: integral = -10.0
    derivative = kd * (p_error - prevp_error) 
    compensation = prop + integral + derivative
    prevp_error = p_error
    if compensation > max_steer: compensation = max_steer
    elif compensation < -max_steer: compensation = -max_steer
    steer_sequence = compensation

# return to the middle on the track
async def return_to_center_position( num_turn, direction, gyro_angle_correct=20, max_steer = 45, color = 0):
    global prevp_error, sump_error, p_error
    global steer_sequence, speed_sequence, turn_right, turn_left
    
    if direction == 1:
        if turn_left == True: position_target = 90 * (num_turn-1) - 30
        elif turn_right == True: position_target = 90 * (num_turn-1) + 30
    elif direction == -1:
        if turn_right == True: position_target = 90 * (num_turn-1) * direction + 35
        elif turn_left == True: position_target = 90 * (num_turn-1) * direction - 35
    
    while True:
        p_error = position_target - hub.imu.heading()
        await wait(10)
        if abs(p_error) <= 5:
            steer_sequence = 0
            await wait(10)
            current_rot = rear.angle()
            while rear.angle() < current_rot + 140:
                steer_sequence = 0
                speed_sequence = 900
                await wait(10)
                if rob_data['line_color'] in [1, 2]:
                    break
            break 
        position_to_center(position_target, p_error, max_steer=max_steer)
        speed_sequence = 1100
        await wait(10)

# pid for return to center from block
def steer_to_center(target, kp=12, ki=0.000001, kd=1.0, max_steer=45):
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
async def return_center_fr_block(num_turn, direction, max_steer=40):
    global steer_sequence, speed_sequence, turn_left, turn_right
    global sumH_error, prevH_error
    sumH_error = 0
    prevH_error = 0
    if direction == 0: target = 0
    else:
        if turn_left == True:
            target = (90 * (num_turn - 1)) * direction -5
        if turn_right == True:
            target = (90 * (num_turn - 1)) * direction +5
    while True:
        h_error = target - hub.imu.heading()
        if turn_left or turn_right:
            if abs(h_error) <= 10: 
                steer_sequence = 0
                break
                
        steer_to_center(target, max_steer=max_steer)
        speed_sequence = 1100
        await wait(10)
```
return_to_center_position() and return_center_fr_block() calculate a counter-heading using the Gyro sensor to steer the car diagonally back toward the middle of the track lane, straightening out once it gets there and preparing for the next block.
```python
async def detect_corner():
    global num_turn, direction
    global rob_data, steer_sequence, speed_sequence, is_sequencing
    global can_sense_corner, can_sense_corner_CW, can_sense_corner_CCW
    global detect_color, distance_wall
    while True:
        if num_turn < 12:
            if direction == 1: can_sense_corner = can_sense_corner_CW
            elif direction == -1: can_sense_corner = can_sense_corner_CCW
            
            if rob_data["corner"] == 1 and not is_sequencing and can_sense_corner: 
                is_sequencing = True
                await hub.speaker.beep()
                if direction == 0:
                    if rob_data['ultra_L'] > rob_data['ultra_R']: direction = -1
                    elif rob_data['ultra_L'] < rob_data['ultra_R']: direction = 1
                if num_turn in [4, 8]:
                    rear.reset_angle(0)
                    steer_sequence = 0
                    while rear.angle() < 700: 
                        current_angle = hub.imu.heading()
                        error = (90 * (num_turn-1) * direction) - current_angle
                        if direction == 1:
                            steer_sequence = error * 1.35
                        if direction == -1:
                            steer_sequence = error * 1.65
                        speed_sequence = 750
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
                    while rear.angle() > -150:
                        speed_sequence = -800
                        await wait(10)
                
                steer_sequence = -75 * direction
                await turn90_PID_L(num_turn, forward=False, maxP=1100, minP=400)
                num_turn += 1
                await wait(10)
                steer_sequence = 0
                await wait(200)
                rear.reset_angle(0)
                is_sequencing = False
                if direction == 1: can_sense_corner_CW = False
                elif direction == -1: can_sense_corner_CCW = False
        elif num_turn == 12:
            # initiating parking sequence
            if direction == 1: can_sense_corner = can_sense_corner_CW
            elif direction == -1: can_sense_corner = can_sense_corner_CCW
            if rob_data["corner"] == 1 and not is_sequencing and can_sense_corner:
                rear.reset_angle(0)
                while rear.angle() < 500: 
                    current_angle = hub.imu.heading()
                    error = (90 * (num_turn-1) * direction) - current_angle
                    steer_sequence = error * 5
                    speed_sequence = 800
                    await wait(10) 
                if direction == 1:
                    distance_wall = await getMedianL(3)
                if direction == -1:
                    distance_wall = await getMedianR(3)
                speed_sequence = 0
                steer_sequence = 0
                return 
        await wait(20)
```
This function monitors rob_data["corner"]. When the color sensor spots a corner line tape, it freezes normal driving (is_sequencing = True), tracks what lap/turn it is on (num_turn), adjusts its alignment, and kicks off the 90-degree PID turn. Once complete, it bumps num_turn by 1. When num_turn hits 12, it breaks out of the loop to trigger parking.
```python
async def ultrasonic_PID(kp=0.001, ki=0.000001, kd=1000.0, minPower=900, maxPower=1100):
    global sum_error, prev_error, max_steer, direction, num_turn
    global rob_data, steer_center, speed_center, is_sequencing
    while num_turn <= 12:        
        if is_sequencing:
            sum_error = 0
            prev_error = 0
            await wait(20)
            continue
            
        error = rob_data['ultra_R'] - rob_data['ultra_L']    
        prop = kp * error 
        sum_error += error
        integral = ki * sum_error 
        if integral > 10.0: integral = 10.0
        derivative = kd * (error - prev_error) 
        compensation = prop + integral + derivative
        prev_error = error
        if compensation > max_steer: compensation = max_steer
        elif compensation < -max_steer: compensation = -max_steer
        maxP, minP = maxPower, minPower
        max_error = 1000
        if error > max_error: error = max_error
        elif error < 0: error = 0
        drive_power = -(maxP - minP) * (error - max_error) / max_error + minP   
        steer_center = compensation
        speed_center = drive_power                    
        await wait(20) 
    speed_center = 0
```
The error for the PID is calculated by using the two ultrasonic sensors and finding the difference between them. If the difference is zero the robot is in the center of the track. If it drifts, the PID loop outputs a correction to steer_center to bring the robot back to the middle of the lane.
```python
async def sense_line_color():
    global can_sense_corner_CW, can_sense_corner_CCW, detect_color
    while True:
        if rob_data['line_color'] == 1 and (direction == 0 or direction == 1) and detect_color == True: 
            can_sense_corner_CW = True
            await hub.speaker.beep(100)
            await wait(100)
            detect_color = False
        elif rob_data['line_color'] == 2 and (direction == 0 or direction == -1): 
            can_sense_corner_CCW = True
            await hub.speaker.beep(100)
        await wait(20)
```
This function converts raw sensor values to colors. Spotting orange(1) tells the system it needs to prepare for a Clockwise corner turn; spotting blue(2) prepares it for a Counter-Clockwise turn.
```python
async def main():
    await get_out_parking()
    # asynchronously controls functions
    await multitask(
        remote_engine(),  
        update_robot_data(),
        avoid_blocks_and_return_center(),
        sense_line_color(),
        detect_corner(),
        ultrasonic_PID(kp=0.003, ki=0.000001, kd=10000.0), 
        motor_controller(),
        race=True        
    )
    await parallel_parking()
    car.drive_speed(0)
    car.steer(0)
    gc.collect() 
    await wait(500) 
```
This function orchestrates everything. The multitask() function allows the robot to do PID, obstacle avoidance, and line checking at the same time. The moment detect_corner() finishes lap 3 (turn 12), the multitasking race ends, and the script moves directly to the final parallel_parking() function.
<br><br><br>

## 3.3 Camera Usage and Software
### **OPEN CHALLENGE CAMERA**

Our Camera Code for the open challenge searches for objects and sends the data to a Lego Hub using the PUPRemote library. It sets the camera resolution to QVGA (320x240 pixels). When it starts, it sets up a Region of Interest (ROI) to limit where the camera looks. set_auto_gain(), set_auto_whitebal(), and set_auto_exposure() are set to False to keep the image and thresholds consistent when in different lighting conditions.

In the main loop, the camera takes a picture and makes a copy of it. This lets the script read the data on one copy while drawing helpful lines on the screen with the other. 
```python
img_debug = sensor.snapshot()
    img = img_debug.copy()
    img_debug.draw_cross(160, 120, color=(0, 0, 0))
```
A special function tweaks the picture's contrast to make objects stand out clearly from the background. The script checks a small ROI at the top-center of the picture for dark objects. This ROI is used to detect the black corner and tells the robot to turn once it reaches near the corner
```python
img_center = (160, 120)
img_roi = (5, 110, 310, 125)
roi_rect = (img_roi[0], img_roi[1], img_roi[2], img_roi[3])
roi_left_bottom = (5, 201, 70, 35)
roi_right_bottom = (245, 201, 70, 35)
img_roi_corner = (155, 80, 10,40)
```
If it finds a dark object there, it changes a status number from 0 to 1. Finally, the script puts the object data and the status number into a small group of 4 pieces of information. It sends this packet to the Lego Hub right away before starting over.
```python
def check_corner_roi(img, img_debug):
    img_contrast = img.copy()
    img_contrast.gamma_corr(gamma=1.9, contrast=1.1, brightness=-0.1)
    threshold_black = (0, 37, -128, 15, -54, 37)
    img_debug.draw_rectangle(img_roi, color=(0, 0, 255))
    img_debug.draw_rectangle(img_roi_corner, color=(255, 255, 0))
    black = img_contrast.find_blobs([threshold_black], area_threshold=150, roi=img_roi_corner, merge=True)
    if black:
        black_val = 1
    else:
        black_val = 0
    corner = {"black": black_val}
    return corner

while True:
    img_debug = sensor.snapshot()
    img = img_debug.copy()
    img_debug.draw_cross(160, 120, color=(0, 0, 0))
    block = find_block(img, img_debug, 30)
    corner = check_corner_roi(img, img_debug)
    data = (block["color"], block["center_x"], block["center_y"], corner["black"])
    p.update_channel('cam', *data)
    p.process()
```

### **OBSTACLE CHALLENGE CAMERA**

The camera first turns on its front LED lights to full brightness. This keeps the lighting on the track perfectly steady and stops outside shadows from messing up the camera’s view. The camera then locks its settings for exposure and color balance. By turning off the camera's automatic adjustments, the code ensures colors look exactly the same whether the room is bright or dim. The camera also fixes lens distortion so shapes look accurate.

To save computing power, the camera doesn’t search the whole screen. Instead, it looks only inside two specific boxes called Regions of Interest:

* The Wide Middle Strip: A wide box across the lower half of the screen. This is where the camera watches out for red, green, or pink obstacle blocks on the floor.

* The Central Thin Strip: A narrow vertical box right in the center. This is whre the camera searches for oncoming walls or black lines.

Every time the camera takes a picture, it makes an exact copy of it. It uses the clean original to draw colorful boxes and crosshairs on your computer screen for testing. It takes the copy and alters its brightness and contrast to make the background go black while making the block colors stand out sharply. It uses a special color system that measures the actual tint of an object rather than how bright it is. Since red can look bright or dark depending on shadows, the camera uses two separate red filters and combines them so reduces the chance to miss a red obstacle.

<img width="463" height="348" alt="Screenshot_3" src="https://github.com/user-attachments/assets/93d56997-3c43-4584-b25c-3fd17b836d37" />


If the camera sees more than one block at the same time, it uses perspective to figure out which one is the closest. Because the camera points downward at the floor, objects that are lower down on the screen are physically closer to the robot.

The camera checks the bottom edge of the blocks and picks the one closest to the bottom of the screen. If a red and green block are both visible, the lower one wins priority. The camera then calculates the exact center of that winning block and labels it with a simple color ID number.

<img width="467" height="348" alt="Screenshot_2" src="https://github.com/user-attachments/assets/dcc030b7-af08-4d0c-a4ef-4b39abbef44e" />

At the same time, the camera looks inside the narrow central box to see if the path ahead is clear. If it spots a dark object or a black line inside the strip, it instantly changes an internal status number from zero to one. This acts as an early warning, letting the robot know it is about to hit a wall or cross a boundary line.

<img width="457" height="349" alt="Screenshot_1" src="https://github.com/user-attachments/assets/3390f3bb-e073-4d89-85b6-71e0c7dd9589" />

All of this gathered information is packed into a compact 4-part data packet containing the closest color ID, its coordinates, and the black line status. Finally, the script continuously transmits this data stream over a PUPRemote channel so the connected LEGO robot can steer toward the blocks or react to the corner.
 ```
 data = (block["color"], block["center_x"], block["center_y"], corner["black"])
    p.update_channel('cam', *data)
    p.process()
```

<br><br><br>
## 3.4 Problems Encountered 
We encountered many problems in our old code and we made many improvements since then. We managed to complete the parking and made the AvoidBlocks command more consistent. We have also managed to make it go both clockwise and counterclockwise.
<table class="failure-table">
    <thead>
      <tr>
        <th>Issue Encountered</th>
        <th>Root Cause Analysis</th>
        <th>Implemented Solution</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Corner Detection</td>
        <td>Camera hadn't seen the black or Black is too different from the Range</td>
        <td>Timer after detecting Orange or Blue</td>
      </tr>
      <tr>
        <td>Wrong algorithm for Parking</td>
        <td>only possible with a specific case</td>
        <td>make it possible to park with multiple cases</td>
      </tr>
      <tr>
        <td>Centering</td>
        <td>Ultrasonic beinging off resulting in of centering</td>
        <td>calibrate the difference of the 2 ultrasonic</td>
      </tr>
       <tr>
        <td>Block Avoidance </td>
        <td>Camera sometimes miss seeing the block resulting late or early avoidance</td>
        <td>Find coordinate of block and use the coordinates to find Tangent Angle and hypotenuse </td>
      </tr>
       <tr>
        <td>Gyro drift</td>
        <td></td>
        <td>resetting the gyro every lap</td>
      </tr>
       <tr>
        <td>Corner block detection</td>
        <td>when entering a corner the camera acidentaly detects the corner block before the robot turns a corner</td>
        <td>to avoid detecting corner block wehn entering corner section, the robot ignores all blocks after detecting a blue or orange line depending on direction.</td>
      </tr>
       <td>Corner fail safe </td>
       <td>when the ROI fails the detect the wall it will bump to the wall and get stuck</td>
       <td> if the robot does not detect the wall 3 seconds afrer detecting the blue or orange line, the robot will automatically turn.</td>
    </tbody>
  </table>
https://drive.google.com/file/d/1IwvF9whDRN1dr9YeoEUpp2IKtazWew4s/view (old code)

[https://drive.google.com/file/d/1YzoAbaAszqIbo_PungKgBqTQ1u02eVbx/view?usp=sharing
](https://drive.google.com/file/d/1YzoAbaAszqIbo_PungKgBqTQ1u02eVbx/view?usp=sharing) (current code)

### Disclaimer
Gemini and Claude were used to enchance the formulated code and as an inspiration for the github by providing examples. Claude was used to improve the threshold of the colors and Gemini was used to help build the code in specific parts by providing an example and was modified by us to complete the challenge, and it also helped in making the github in some parts.
