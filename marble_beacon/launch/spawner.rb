def spawner(_name, _modelURI, _worldName, _x, _y, _z, _roll, _pitch, _yaw)
  <<-HEREDOC
  <plugin name="ignition::launch::GazeboFactory"
          filename="libignition-launch-gazebo-factory.so">
    <name>#{_name}</name>
    <allow_renaming>false</allow_renaming>
    <pose>#{_x} #{_y} #{_z + 0.2} #{_roll} #{_pitch} #{_yaw}</pose>
    <world>#{_worldName}</world>
    <is_performer>true</is_performer>
    <sdf version='1.6'>
    <include>
      <name>#{_name}</name>
      <uri>#{_modelURI}</uri>
      <!-- Publish robot state information -->
      <plugin filename="libignition-gazebo-pose-publisher-system.so"
        name="ignition::gazebo::systems::PosePublisher">
        <publish_link_pose>true</publish_link_pose>
        <publish_sensor_pose>true</publish_sensor_pose>
        <publish_collision_pose>false</publish_collision_pose>
        <publish_visual_pose>false</publish_visual_pose>
        <publish_nested_model_pose>#{$enableGroundTruth}</publish_nested_model_pose>
      </plugin>
    </include>
    </sdf>
  </plugin>
  HEREDOC
end

def rosExecutables(_name, _worldName)
  <<-HEREDOC
  <executable name='robot_description'>
    <command>roslaunch --wait marble_beacon description.launch world_name:=#{_worldName} name:=#{_name}</command>
  </executable>
  <executable name='topics'>
    <command>roslaunch --wait marble_beacon vehicle_topics.launch world_name:=#{_worldName} name:=#{_name}</command>
  </executable>
  HEREDOC
end
