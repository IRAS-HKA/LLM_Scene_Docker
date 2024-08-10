cmake_minimum_required(VERSION 3.8)
project(llm_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(object_detector_tensorflow_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(aip_grasp_planning_interfaces REQUIRED)
find_package(aip_packing_planning_interfaces REQUIRED)

set(DEPENDENCIES 
  "sensor_msgs"
  "object_detector_tensorflow_interfaces"
  "geometry_msgs"
  "aip_grasp_planning_interfaces"
  "aip_packing_planning_interfaces"
  "std_srvs"
  
)
#  "object_detector_tensorflow_interfaces"


rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/SceneInterpretation.srv"
  "srv/UserInteraction.srv"
  "srv/PackItems.srv"
  "srv/WebsiteFeedback.srv"
  "srv/SetGetAllTypes.srv"
  DEPENDENCIES ${DEPENDENCIES} # Add packages that above messages depend on, in this case geometry_msgs for Sphere.msg
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime ${DEPENDENCIES})
ament_package()
