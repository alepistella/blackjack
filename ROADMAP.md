# Roadmap

The integration sequence isolates mechanical fit, electrical load and software behaviour before bringing them together. Each milestone specifies the evidence used to evaluate it.

| Milestone | Evidence |
| --- | --- |
| Chassis and enclosure fit | Compare the deck and board interfaces with the manufacturer CAD. Record fit, fastening, connector access and bend data. Include the BJ-P03 GNSS antenna plate and BJ-P02 LTE opening in the first mechanical build. |
| Power path | Identify the installed battery module and confirm its output rating and the fitted jack and plug. Record voltage and current for board boot, inference and drivetrain transients before selecting the operating envelope. [Bench test plan](studies/BJ-STU-001_power_supply_study.md#7-bench-test-plan). |
| ROS 2 base bring-up | Record velocity commands, encoder and IMU feedback, odometry and the base behaviour when the command stream stops. Capture the software configuration and a short drive trace. |
| Perception and navigation | Confirm the camera stream and its frame, then evaluate localisation and navigation with a documented sensor configuration and route. |
| NPU inference | Run a camera-based object detection workload as a ROS 2 node. Record the model, runtime and input settings. Measure camera-to-detection latency and board input power for the same drive workload with inference disabled and enabled. |
| STM32H5 heading control | Evaluate a local heading loop on the microcontroller. Compare heading error and control timing with the same loop running on Linux during camera inference. [Experiment](#stm32h5-heading-control). |
| RTK and LTE bring-up | After base bring-up, commission GNSS RTK and LTE using the antenna provisions built into the first mechanical configuration. Check the fix and correction stream independently. [Integration checks](#rtk-and-lte-bring-up). |
| Roof accessories | Evaluate the roof mounting provisions for lidar or a turret. |

The bill of materials, wiring details and design decisions accompany the relevant integration milestones.

## STM32H5 heading control

A skid-steer rover can drift away from its intended heading when its two sides encounter different grip. Test whether a fixed-rate heading loop on the STM32H5 improves straight-line tracking while the Dragonwing runs ROS 2 and camera inference.

ROS 2 supplies the requested forward speed and turn rate. The STM32H5 reads yaw rate from a local IMU and applies a bounded left/right speed correction in straight-line mode. The stock UGV02 controller still drives the motors and runs its wheel-speed loops. For this experiment the STM32H5 would be the sole sender of motion commands to the stock controller. Check the serial interface and electrical levels before selecting the connection, and derive the loop period and command timeout from measured controller response and transport timing. [VENTUNO Q hardware reference](https://docs.arduino.cc/hardware/ventuno-q/) · [Waveshare controller firmware](https://files.waveshare.com/wiki/UGV02/UGV02_BASE.zip).

Use the same speed request and marked course with a change in grip under one side. Record a stock baseline, then compare the same heading correction running on Linux and on the STM32H5, with camera inference enabled and disabled. Measure heading error and lateral drift against an external reference. Measure loop jitter and command arrival at the controller on a common time base. In a separate command-loss run, measure the interval from the last valid command to zero demand and to the physical stop. The stock firmware already has a heartbeat timeout, so the experiment must account for that behaviour when attributing the stop.


## RTK and LTE bring-up

The first mechanical build includes the BJ-P03 GNSS plate and the BJ-P02 LTE antenna opening already drawn in CAD. Reserve the module space and cable routes during assembly. Once the drive and camera checks are complete, integrate and commission the MikroE GNSS RTK Click (ZED-F9P) and LTE Cat.1 7 Click (SIM7672E). Verify the added load and modem transients before running both modules from the rover supply. Linux handles the LTE connection and the NTRIP correction stream. The receiver computes the position solution. Confirm the data interfaces and power requirements during bring-up. Record fix state, correction age and reacquisition after an LTE interruption.

The RTK Click exposes a configurable time pulse on its TMP pin. The STM32H5 experiment will capture that pulse with a timer and timestamp local IMU samples and control events on the same clock. Check the pin routing and signal levels before wiring. The time pulse is a timing reference. Check fix state separately in the receiver data. [GNSS RTK Click pinout](https://www.mikroe.com/gnss-rtk-click) · [LTE Click documentation](https://www.mikroe.com/brochure?ref=MIKROE-6434).
