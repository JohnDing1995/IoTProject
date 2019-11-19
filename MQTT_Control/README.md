# MQTT Control
We compile C API code to shared library and using `ctype` library to call the C functions. The reason of doing this is to easier extend our application by levering the rich external libraries of Python.
* `control_api/` : Python API interface for controlling the car
* `helper.py`: Helper functions, include the definition of the thread for getting the reading from sensors. 
* `test.py`: Test the platoon control with API call.
* `leader-ps4.py`:Define leader's behaviour, with control signal from PS4 controller
* `follower.py`:Define follower's behaviour.
* `config.py`: Configure.
