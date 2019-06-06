This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

### Reflection

Unfortunately this is a single submission by me, Volker Brichzin. Joining a team didn't work out due to some reasons.

The general code structure was described in the project introduction, here is a graphical summary:
![code-structure](/imgs/code-structure.png)

The code has three main parts: perception, planning and control.

Perception: for classifying traffic lights in the simulator (and possible in the vehicle Carla on the Udacity test site) pre-trained detection models are used by loading the model graphs and reading out the scores of the trained classes. The class with the highest score is determined to be the detected light state. For the training of the models I took the liberty of using the [training data set](https://drive.google.com/file/d/0B-Eiyn-CUQtxdUZWMkFfQzdObUE/view) from [Anthony Sarkis](https://medium.com/@anthony_sarkis). This contains already labeled image sets for the simulator and Carla. The alternative would have been to record images (only possible in the simulator) and assign the correct labels with tool [LabelImg](https://github.com/tzutalin/labelImg).
For the actual training a pipeline was used outside of this project that was making use of code from the [Udacity Object Detection Lab](https://github.com/udacity/CarND-Object-Detection-Lab) as well as the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection). The training concluded in `frozen_inference_graph.pb` files that were loaded during the initialization of the `tl_detector` node and later used in the traffic light state classification.

Planning: for the planning the main component is the `waypoint_updater.py` node that is responsible for selecting a predetermined number of waypoints ahead of the vehicle (`LOOKAHEAD_WPS`) that describe the desired route with the desired velocities. This information is then published to the `/final_waypoints` topic.
The walkthroughs by Stephen and Aaron were very helpful in the implementation.

Control: for controlling of the car in the simulator (or in the Carla vehicle) the `dbw_node.py` is responsible. Once receiving `/final_waypoints` messages, the vehicle's waypoint follower will publish twist commands to the `/twist_cmd` topic. The drive-by-wire node is the using these in controllers for throttle, brake and steering.
Again, the walkthrough of Stephen and Aaron on this topic was very helpful for completing this.

### Installation

I had many issues in getting this installed and running locally as working in the workspace I didn't find so productive. And also running the VM was quite slow. I finally settled on a native linux installation, unfortunately on a fairly week PC so that testing in the simulator still showed quite some lagging.

Below is the original instruction from Udacity for installation and getting things running.

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

### Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|        | Simulator | Carla  |
| :-----------: |:-------------:| :-----:|
| Nvidia driver | 384.130 | 384.130 |
| CUDA | 8.0.61 | 8.0.61 |
| cuDNN | 6.0.21 | 6.0.21 |
| TensorRT | N/A | N/A |
| OpenCV | 3.2.0-dev | 2.4.8 |
| OpenMP | N/A | N/A |

We are working on a fix to line up the OpenCV versions between the two.
