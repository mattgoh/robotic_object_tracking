# robotic_object_tracking
EECE 5644

# Summary
This was a group project for a graduate-level course in machine learning. We aimed to investigate object detection capabilities by designing an autonomous robotic system that executed maneuvers based on visual input from a Raspberry Pi camera and object recognition algorithms. The trained algorithms were stored on a Raspberry Pi, which, along with the Pi camera, were mounted a Roomba which served as a chasis for the robotic car. For this project, we focused on k-means classification and Canny edge detection.

# Motivation
Object detection and tracking has a variety of applications in security and surveillance, human computer interaction, biometrics, and vehicle navigation. In the specific case of autonomous vehicle navigation, object detection capabilities remain a core problem. Generally speaking, detection approaches need to run in near realtime so that evasive actions can be successfully performed. At the same time, the implementation of any such solutions are often constrained by external factors, such as economic cost or consumer affordability.

For this project, we aimed to 

# Objectives

1. Use machine learning to detect a set of objects based on visual input (Raspberry Pi camera)

2. Create an autonomous system controlled by the Raspberry Pi (Raspberry Pi, Pi camera, Roomba)

3. Use object detection to set a target object for the car to identify and drive towards (k-means, Canny edge)

4. Use object detection to detect and avoid objects in the path of the goal (k-means, Canny edge)
