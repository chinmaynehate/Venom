<a href="https://www.youtube.com/watch?v=NFO0sFC34yE&t=108s"><img src="https://i.imgur.com/0I80tvl.jpg" title="Venom" alt="Venom"></a>


# Venom : Sprawling-type Quadruped robot

> Venom is  a 12-DOF unmanned Quadruped(four legged robot) equipped with 12 Servo Actuators an ARM Processor for onboard computations.

> The Quadruped is based on Sprawling type motion with creep and trot gait successfully implemented on it.


[![Venom2](https://i.imgur.com/ZmYRAiz.jpg)]()

> This is a part of research project in Legged Mobility at Society of Robotics and Automation, VJTI.

- Most of the robots available in the industry make use of wheels for navigation. The goal is to build legged vehicle with multiple-terrain mobility  superior to existing wheeled and tracked vehicles.
- The system would be able to travel anywhere a person or animal  could  go using their legs while carrying its own fuel and payload. It would be smart enough to negotiate terrain with a minimum of human guidance and intervention



**Demo Video**

<a href ="https://www.youtube.com/watch?v=NFO0sFC34yE&t=108s"> VENOM- All terrain Quadruped</a>

---

## Table of Contents (Optional)

> If your `README` has a lot of info, section headers might be nice.

- [Installation](#Software-Installation)
- [Installation](#Hardware-Stack)
- [Team](#team)
- [FAQ](#faq)
- [License](#license)


---

## Creep GAIT Example

```python
venom = Quadruped(servoId) # Servo ID Array
venom.setParams(dirVector,FixedPoints)# Servo Direction and Set Points
venom.go2CreepStartPosition()
input("Press Enter") # Wait for user Input
# For CREEP GAIT
venom.walk(CREEP)
# For TROT GAIT
venom.walk(TROT)
```
---

## Software-Installation

- Requires Python 3.4+ installed on RaspberryPi (or Similar Development Board).

## Hardware-Stack

-  [Jetson Nano](https://www.nvidia.com/en-in/autonomous-machines/embedded-systems/jetson-nano/) (RasberryPi will work as well)
-  Servo Motors: [ 12 Dynamixel AX-12A](https://www.trossenrobotics.com/dynamixel-ax-12-robot-actuator.aspx) or better / any Normal PWM Servo Motor (Torque > 20kgcm )
-  [PCA9685 16 Channel PWM Servo Driver](https://www.amazon.com/SunFounder-PCA9685-Channel-Arduino-Raspberry/dp/B014KTSMLA) for PWM Servo , [CM-530 Robotis Servo Controller
](https://www.trossenrobotics.com/p/cm-530-robotis-servo-controller.aspx) for Dyanmixel Servos.
- Acrylic Chasis (CAD Files Available)


### Clone

- Clone this repo to your local machine using `https://github.com/chinmaynehate/Venom.git`

### Setup

> Install dependencies

```shell
$ python3 -m pip install numpy adafruit_servokit busio sympy 
```


## Team

| <a href="http://fvcproductions.com" target="_blank">**Chinmay Nehate**</a> | <a href="http://fvcproductions.com" target="_blank">**Suyash More**</a> | <a href="http://fvcproductions.com" target="_blank">**Shashank Deshmukh**</a> |
| :---: |:---:| :---:|
| [![Chinmay Nehate](https://avatars0.githubusercontent.com/u/42030910?s=460&u=8f503c88db898081aaf11c7fd9ca2a36bcc56716&v=4)](https://github.com/chinmaynehate)    | [![Suyash More](https://avatars1.githubusercontent.com/u/29707660?s=460&u=c73a6d9697a744762277dde68183010426a2818d&v=4)](https://github.com/SuyashMore) | [![Shashank Deshmukh](https://avatars0.githubusercontent.com/u/33441200?s=460&v=4)](https://github.com/shanks-d)  |
| <a href="http://github.com/chinmaynehate" target="_blank">`github.com/chinmaynehate`</a> | <a href="http://github.com/SuyashMore" target="_blank">`github.com/SuyashMore`</a> | <a href="http://github.com/shanks-d" target="_blank">`github.com/shanks-d`</a> |


---

## FAQ

- **How do I do *specifically* so and so?**
    - Create an Issue to this repo , we wil respond to the query

---



## License


- **[MIT license](http://opensource.org/licenses/mit-license.php)**
