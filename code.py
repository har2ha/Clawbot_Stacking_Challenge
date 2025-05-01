#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT6, False)
right_drive_smart = Motor(Ports.PORT10, True)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 259.34, 320, 40, MM, 1)
arm3 = Motor(Ports.PORT2, False)
claw = Motor(Ports.PORT7, True)
controller = Controller()


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()



# define variables used for controlling motors based on controller inputs
controller_left_shoulder_control_motors_stopped = True
controller_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, controller_left_shoulder_control_motors_stopped, controller_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller.axis3.position() + controller.axis1.position()
            drivetrain_right_side_speed = controller.axis3.position() - controller.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonL1/buttonL2 status
            # to control claw
            if controller.buttonL1.pressing():
                claw.spin(FORWARD)
                controller_left_shoulder_control_motors_stopped = False
            elif controller.buttonL2.pressing():
                claw.spin(REVERSE)
                controller_left_shoulder_control_motors_stopped = False
            elif not controller_left_shoulder_control_motors_stopped:
                claw.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_left_shoulder_control_motors_stopped = True
            # check the buttonR1/buttonR2 status
            # to control arm3
            if controller.buttonR1.pressing():
                arm3.spin(FORWARD)
                controller_right_shoulder_control_motors_stopped = False
            elif controller.buttonR2.pressing():
                arm3.spin(REVERSE)
                controller_right_shoulder_control_motors_stopped = False
            elif not controller_right_shoulder_control_motors_stopped:
                arm3.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

#endregion VEXcode Generated Robot Configuration
myVariable = 0

def when_started1():
    global myVariable
    arm3.spin_for(FORWARD, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 300, MM)
    claw.spin(REVERSE)
    wait(1, SECONDS)
    drivetrain.turn_for(LEFT, 180, DEGREES)
    drivetrain.drive_for(FORWARD, 800, MM)
    drivetrain.stop()
    arm3.spin_for(REVERSE, 90, DEGREES)
    drivetrain.stop()
    claw.spin(FORWARD)
    wait(1, SECONDS)
    drivetrain.drive_for(REVERSE, 200, MM)
    claw.spin(REVERSE)
    wait(1, SECONDS)
    claw.spin(FORWARD)
    drivetrain.stop()
    drivetrain.drive_for(REVERSE, 300, MM)
    drivetrain.turn_for(RIGHT, 195, DEGREES)
    drivetrain.drive_for(FORWARD, 400, MM)
    drivetrain.stop()
    claw.spin(FORWARD)
    wait(1, SECONDS)
    claw.spin(REVERSE)
    wait(1, SECONDS)
    drivetrain.turn_to_rotation(180, DEGREES)
    drivetrain.drive_for(FORWARD, 800, MM)
    arm3.spin_for(FORWARD, 90, DEGREES)
    drivetrain.stop()
    claw.spin(FORWARD)
    wait(1, SECONDS)
    claw.spin(REVERSE)
    wait(1, SECONDS)
    drivetrain.drive_for(REVERSE, 300, MM)
    drivetrain.turn_for(RIGHT, 180, DEGREES)
    drivetrain.stop()

when_started1()
