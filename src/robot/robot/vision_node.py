#!/usr/bin/env python3
"""
Vision Node for Robot Camera and Face Detection

This node interfaces with the Raspberry Pi camera using picamera2 (libcamera),
performs face detection using OpenCV, and publishes both raw camera frames
and face detection results to ROS topics.

Topics Published:
  - /camera/image_raw (sensor_msgs/Image): Raw camera frames
  - /vision/faces (robot/FaceDetectionArray): Detected face bounding boxes

Parameters:
  - camera_width (int): Camera resolution width (default: 640)
  - camera_height (int): Camera resolution height (default: 480)
  - camera_framerate (int): Target framerate (default: 15)
  - detector_type (str): Face detector type - 'haar' or 'dnn' (default: 'haar')
  - debug_draw_boxes (bool): Draw bounding boxes on published images (default: false)
"""

import rclpy
from rclpy.node import Node
from robot.face_detector.haar_cascade_detector import HaarCascadeDetector
from robot.msg import FaceDetection, FaceDetectionArray
from sensor_msgs.msg import Image
from std_msgs.msg import Header
from cv_bridge import CvBridge
from picamera2 import Picamera2
from time import perf_counter
import cv2

import numpy as np



class VisionNode(Node):
    """ROS2 node for camera capture and face detection"""
    
    def __init__(self):
        super().__init__('vision_node')
        
        # Declare parameters
        self.declare_parameter('camera_width', 640)
        self.declare_parameter('camera_height', 480)
        self.declare_parameter('camera_framerate', 15)
        self.declare_parameter('detector_type', 'haar')
        self.declare_parameter('debug_draw_boxes', False)
        
        # Get parameters
        self.camera_width = self.get_parameter('camera_width').value
        self.camera_height = self.get_parameter('camera_height').value
        self.camera_framerate = self.get_parameter('camera_framerate').value
        self.detector_type = self.get_parameter('detector_type').value
        self.debug_draw_boxes = self.get_parameter('debug_draw_boxes').value
        
        self.get_logger().info(f"Initializing vision node...")
        self.get_logger().info(f"  Camera: {self.camera_width}x{self.camera_height} @ {self.camera_framerate}fps")
        self.get_logger().info(f"  Detector: {self.detector_type}")
        self.get_logger().info(f"  Debug draw: {self.debug_draw_boxes}")
        
        # Initialize CV Bridge for ROS-OpenCV conversion
        self.bridge = CvBridge()
        
        # Initialize publishers
        self.image_pub = self.create_publisher(
            Image,
            '/camera/image_raw',
            10
        )

        self.faces_pub = self.create_publisher(
            FaceDetectionArray,
            '/vision/faces',
            10
        )
        
        # Initialize face detector
        self.detector = self._create_detector()

        self.camera = self._initialize_camera()
        
        # Create timer for main processing loop
        timer_period = 1.0 / self.camera_framerate
        self.timer = self.create_timer(timer_period, self.process_frame)
        
        self.get_logger().info("Vision node initialized successfully")
    
    def _create_detector(self):
        """Create face detector based on parameter"""
        if self.detector_type == 'haar':
            try:
                detector = HaarCascadeDetector()
                self.get_logger().info("Haar cascade detector loaded")
                return detector
            except Exception as e:
                self.get_logger().error(f"Failed to load Haar detector: {e}")
                raise
        elif self.detector_type == 'dnn':
            # TODO: Implement DNN detector in future
            self.get_logger().error("DNN detector not yet implemented")
            raise NotImplementedError("DNN detector not yet implemented")
        else:
            self.get_logger().error(f"Unknown detector type: {self.detector_type}")
            raise ValueError(f"Unknown detector type: {self.detector_type}")
    
    def _initialize_camera(self):
        camera = Picamera2()
        config = camera.create_preview_configuration(
            main={"size": (self.camera_width, self.camera_height), "format": "RGB888"}
        )
        camera.configure(config)
        camera.start()
        return camera

    def construct_face_detection_array(self, detections):
        detection_msgs = []
        for detection in detections:
            msg = FaceDetection()
            msg.x, msg.y, msg.width, msg.height, msg.confidence = detection
            detection_msgs.append(msg)
        result = FaceDetectionArray()
        result.header = Header()
        result.header.stamp = self.get_clock().now().to_msg()
        result.header.frame_id = 'camera'
        result.detections = detection_msgs
        return result
    
    def process_frame(self):
        """
        Main processing loop: capture frame, detect faces, publish results.
        
        This is called by the timer at the configured framerate.
        """
        try:

            def convert_and_publish_image(image_array):
                image_msg = self.bridge.cv2_to_imgmsg(image_array, encoding="rgb8")
                self.image_pub.publish(image_msg)
            t1 = perf_counter()
            array = self.camera.capture_array("main")
            t2 = perf_counter
            self.get_logger().info(f"time to capture: {t2-t1}")
            if not self.debug_draw_boxes:
                convert_and_publish_image(array)

            t3 = perf_counter()
            detections = self.detector.detect(array)
            t4 = perf_counter()

            self.get_logger().info(f"time to detect: {t4-t3}")

            detections_msg = self.construct_face_detection_array(detections)

            self.faces_pub.publish(detections_msg)

            if self.debug_draw_boxes:
                for detection in detections:
                    pt1 = detection[:2]
                    pt2 = (detection[0] + detection[2], detection[1]+detection[3])
                    cv2.rectangle(array, pt1, pt2, color=(0,255,0))
                convert_and_publish_image(array)
            
        except Exception as e:
            self.get_logger().error(f"Error processing frame: {e}")
    
    def destroy_node(self):
        """Clean up resources when node is shutdown"""
        if hasattr(self, 'camera'):
            self.camera.stop()
            self.camera.close()
        
        super().destroy_node()


def main(args=None):
    """Main entry point for the vision node"""
    rclpy.init(args=args)
    
    try:
        node = VisionNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
