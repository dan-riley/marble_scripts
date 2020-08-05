There are two options for displaying a robot model in RVIZ, depending on whether you have a base_link to world tf.  In addition there are two options for robot models.

First, pick a robot model.

1.  I have robot model and I don't mind if there are RVIZ errors:

A typical robot model (such as marble_husky_sensor_config_1) has multiple links, but we really only care about base_link.  So if you don't have the other links, RVIZ will complain, but the main model will still follow base_link.  For this case, just use replace the customized model in the later steps.

2.  I hate errors!  Get rid of the errors!

To get rid of RVIZ errors, our robot model needs to ONLY use base_link.  The models under marble_base_station/marble_base_models have already been simplified.  Essentially all links and joints have been removed, and the applicable visual models moved under base_link.  See robot_from_sdf.xacro.  These models publish under $(robot)_base/base_link, instead of $(robot)/base_link, but can be changed by editing line 4.  You may also want to change description.launch, line 4 to change the namespace of the robot_description.


Now, setup our tf.

1.  I have a base_link tf, or at least a tf that can act like base_link:

If you already have a base_link tf, just launch the robot model!  If you don't have base_link, but you have another tf that you'd like to use, edit the robot_from_sdf.xacro of the model, and find the line similar to <link name='${robot_namespace}/base_link'> and change the base_link as desired.

roslaunch ROBOT_MODEL_PACKAGE description.launch name:=ROBOT

This will run briefly, then close.  Don't be alarmed!  Now go to RVIZ, add a Robot Model, and in the settings change Description to ROBOT/robot_description.  If using one of my custom models, use ROBOT_base/robot_description.  The model should appear, and it will follow the base_link tf.  As noted above, if you're using a regular model, you will likely get errors, but the model should work.

2.  I don't have a tf, because my bag file doesn't have it!  But I have odometry!

I have you covered!

roslaunch marble_scripts/rviz_robot_model.launch robot:=ROBOT model:=ROBOT_MODEL

By default this will launch my custom model description.launch, and odom_to_tf to create a base_link from the topic /ROBOT/odometry.

You can pass odomTopic:=new_topic if odometry is on a different topic.

If you're using a stock robot model, you probably want to edit the launch file, and change newFrame to "$(arg robot)/base_link" (it's commented out for you), and change the description.launch include to find your package instead of 'marble_' + model + '_base'.

In RVIZ, add the robot model as described above!  Enjoy your model!
