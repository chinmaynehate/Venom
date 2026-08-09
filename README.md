[![PR](https://camo.githubusercontent.com/f96261621753dacf526590825b84f87ccb1db0e6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5052732d77656c636f6d652d627269676874677265656e2e7376673f7374796c653d666c6174)](https://github.com/chinmaynehate/Venom/pulls)
[![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/chinmaynehate)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

<a href="https://www.youtube.com/watch?v=NFO0sFC34yE&t=108s"><img src="https://i.imgur.com/M67nE8U.jpg" title="Venom" alt="Venom"></a>

# Venom: Sprawling-Type Quadruped Robot

> Venom is a 12-DOF unmanned quadruped (four-legged robot) equipped with 12 servo actuators and an ARM processor for onboard computation.

> The quadruped uses sprawling-type motion, with creep and trot gaits implemented and tested.

[![Venom2](https://i.imgur.com/ZmYRAiz.jpg)]()

> Built as part of a research project in Legged Mobility at the Society of Robotics and Automation, VJTI.

- Most robots in industry rely on wheels for navigation. Venom's goal is legged mobility with multi-terrain capability beyond what wheeled or tracked vehicles can achieve.
- The aim is a system that can travel anywhere a person or animal could go on foot, carrying its own power and payload, and negotiating terrain with minimal human guidance.

**Demo Video**: [VENOM — All-terrain Quadruped](https://www.youtube.com/watch?v=NFO0sFC34yE&t=108s)

---

## Table of Contents

- [How It Works](#how-it-works)
- [Software Installation](#software-installation)
- [Hardware Stack](#hardware-stack)
- [Team](#team)
- [FAQ](#faq)
- [License](#license)

---

## How It Works

The robot control code lives under [`src/Quadruped/`](src/Quadruped):

| Module | Responsibility |
|---|---|
| `Quadruped.py` | Top-level `Quadruped` and `Leg` classes — configures servo IDs and leg geometry, and implements the gait state machines (`Creep`, `Creep_w_bump`, `Trot`, `stanceBackward`) driven through `walk()` / `walkOnce()` |
| `constants.py` | Per-gait tuning parameters (`Creep`, `Trot` classes: step height, stance limits, timing), gait-mode IDs (`CREEP`, `TROT`, `TROT_BACK`, `CREEP_DYN`), and link lengths used for kinematics |
| `Core/kinematics.py` | Inverse kinematics (`getInverse`) that converts a target foot position `(x, y, z)` into joint angles for each leg |
| `Core/pwmServo.py` | PWM servo driver interface (via the `adafruit_servokit`/PCA9685 stack) |
| `Core/IMU.py`, `Core/GPS.py` | Sensor interfaces for orientation and position — used by the `CREEP_DYN` gait to actively stabilize the base against terrain unevenness (feedback loop in `Leg.StepInY_feedback`) |
| `Core/kalman_filter.py` | Kalman filtering for sensor fusion |
| `Core/trajectory_fourier.py` | Fourier-based trajectory generation experiments |
| `Core/imu/` | IMU calibration scripts and reference material (RTIMULib config, ellipsoid-fit MATLAB scripts for magnetometer calibration) |
| `Components/Gamepad.py` | Linux joystick (`/dev/input/js*`) input handling for manual teleoperation |
| `JGpio.py` | GPIO helper for bump-switch / digital I/O pins used in dynamic leg placement |
| `unit_Tests/` | Standalone scripts for exercising individual servo angles (`writeAngles.py`, `writeAllAngles0.py`) |

### Gait Modes

Four gait modes are defined in `constants.py` and dispatched via `Quadruped.walk(Mode)`:

- `CREEP` — static creep gait, one leg moves at a time
- `TROT` — diagonal-pair trot gait
- `TROT_BACK` — reverse trot
- `CREEP_DYN` — creep gait with dynamic, IMU-feedback-driven leg placement for stability on uneven terrain (this is the mode used in `Quadruped.py`'s own `__main__`)

### Example

```python
from Quadruped import Quadruped
from constants import CREEP, TROT, CREEP_DYN

venom = Quadruped(servoId)              # Servo ID array
venom.setParams(dirVector, FixedPoints) # Servo direction and fixed set points
venom.go2CreepStartPosition()
input("Press Enter")                    # Wait for user input

venom.walk(CREEP)      # Static creep gait
venom.walk(TROT)       # Trot gait
venom.walk(CREEP_DYN)  # IMU-stabilized dynamic creep gait
```

## Software Installation

- Python 3.4+ on a Raspberry Pi (or similar single-board computer / ARM dev board).

### Clone

```shell
git clone https://github.com/chinmaynehate/Venom.git
```

### Setup

Install dependencies:

```shell
python3 -m pip install numpy adafruit_servokit busio sympy
```

## Hardware Stack

- [Jetson Nano](https://www.nvidia.com/en-in/autonomous-machines/embedded-systems/jetson-nano/) (a Raspberry Pi will also work)
- Servo motors: [12x Dynamixel AX-12A](https://www.trossenrobotics.com/dynamixel-ax-12-robot-actuator.aspx) or better, or any standard PWM servo (torque > 20 kg·cm)
- Alternate servos: [coreless servo, 35 kg·cm](https://robokits.co.in/motors/rc-servo-motors/ultra-torque-dual-shaft-metal-gear-35kgcm-coreless-servo-w-t-acc)
- [PCA9685 16-channel PWM servo driver](https://www.amazon.com/SunFounder-PCA9685-Channel-Arduino-Raspberry/dp/B014KTSMLA) for PWM servos, or [CM-530 Robotis servo controller](https://www.trossenrobotics.com/p/cm-530-robotis-servo-controller.aspx) for Dynamixel servos
- Acrylic chassis — CAD files available in [`CAD Files/`](CAD%20Files) (Fusion 360 `.f3d`: frame base/top, additional floor, Tibia side plate, end-effector)

## Team

| <a href="http://fvcproductions.com" target="_blank">**Chinmay Nehate**</a> | <a href="http://fvcproductions.com" target="_blank">**Suyash More**</a> | <a href="http://fvcproductions.com" target="_blank">**Shashank Deshmukh**</a> |
| :---: |:---:| :---:|
| [![Chinmay Nehate](https://avatars0.githubusercontent.com/u/42030910?s=460&u=8f503c88db898081aaf11c7fd9ca2a36bcc56716&v=4)](https://github.com/chinmaynehate)    | [![Suyash More](https://avatars1.githubusercontent.com/u/29707660?s=460&u=c73a6d9697a744762277dde68183010426a2818d&v=4)](https://github.com/SuyashMore) | [![Shashank Deshmukh](https://avatars0.githubusercontent.com/u/33441200?s=460&v=4)](https://github.com/shanks-d)  |
| <a href="http://github.com/chinmaynehate" target="_blank">`github.com/chinmaynehate`</a> | <a href="http://github.com/SuyashMore" target="_blank">`github.com/SuyashMore`</a> | <a href="http://github.com/shanks-d" target="_blank">`github.com/shanks-d`</a> |

---

## FAQ

- **How do I do *specifically* so and so?**
    - Create an issue on this repo — we'll respond to the query.

---

## License

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
