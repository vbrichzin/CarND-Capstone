from styx_msgs.msg import TrafficLight
import os
import numpy as np
import tensorflow as tf
import cv2

#SSD_MOBILENET_MODEL_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#        '../../../../models/ssd_mobilenet_v1_sim_2019_04_06/frozen_inference_graph.pb')
SIM_SSD_MODEL_FILE = '../../../../models/ssd_mobilenet_v1_sim_2019_04_06/frozen_inference_graph.pb'
SITE_SSD_MODEL_FILE = '../../../../models/faster_rcnn_inception_v2_udacity_2019_04_11/frozen_inference_graph.pb')

class TLClassifier(object):
    def __init__(self, is_site):

        #TODO load classifier

        # Loading differently pre-trained traffic light detection models
        # for simulator and for test site
        self.is_site = is_site
        if is_site:
            self.detection_graph = self.load_graph(SITE_SSD_MODEL_FILE)
        else:
            self.detection_graph = self.load_graph(SIM_SSD_MODEL_FILE)

        # Extracting relevant tensors according to Udacity Object Classification Lab
        # `get_tensor_by_name` returns the Tensor with the associated name in the Graph.
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')

        # The classification of the object (integer id).
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction

        # Following closely the Udacity Object Detection Lab

        image_np = np.expand_dims(np.asarray(image, dtype=np.uint8), 0)

        with tf.Session(graph=self.detection_graph) as sess:
            # Actual detection.
            (boxes, scores, classes) = self.sess.run([self.detection_boxes,
                            self.detection_scores, self.detection_classes],
                            feed_dict={self.image_tensor: image_np})

            # Remove unnecessary dimensions
            boxes = np.squeeze(boxes)
            scores = np.squeeze(scores)
            classes = np.squeeze(classes)

            confidence_cutoff = 0.5
            # Filter boxes with a confidence score less than `confidence_cutoff`
            boxes, scores, classes = self.filter_boxes(confidence_cutoff, boxes, scores, classes)

            # The current box coordinates are normalized to a range between 0 and 1.
            # This converts the coordinates actual location on the image.
            height, width = image.size
            box_coords = self.to_image_coords(boxes, height, width)

            if len(scores) == 0:
                return TrafficLight.UNKNOWN
            else:
                scoreboard = {}
                for idx in range(scores.size):
                    if classes[idx] not in scoreboard:
                        scoreboard[classes[idx]] = scores[idx]
                    else:
                        scoreboard[classes[idx]] += scores[idx]
                label = max(scoreboard.iterkeys(), key=(lambda key: scoreboard[key]))
                if label == 1:
                    return TrafficLight.GREEN
                elif label == 2:
                    return TrafficLight.RED
                elif label == 3:
                    return TrafficLight.YELLOW
                else:
                    return TrafficLight.UNKNOWN

    #
    # Utility funcs from Udacity Object Detection Lab
    #

    def filter_boxes(self, min_score, boxes, scores, classes):
        """Return boxes with a confidence >= `min_score`"""
        n = len(classes)
        idxs = []
        for i in range(n):
            if scores[i] >= min_score:
                idxs.append(i)

        filtered_boxes = boxes[idxs, ...]
        filtered_scores = scores[idxs, ...]
        filtered_classes = classes[idxs, ...]
        return filtered_boxes, filtered_scores, filtered_classes

    def to_image_coords(self, boxes, height, width):
        """
        The original box coordinate output is normalized, i.e [0, 1].

        This converts it back to the original coordinate based on the image
        size.
        """
        box_coords = np.zeros_like(boxes)
        box_coords[:, 0] = boxes[:, 0] * height
        box_coords[:, 1] = boxes[:, 1] * width
        box_coords[:, 2] = boxes[:, 2] * height
        box_coords[:, 3] = boxes[:, 3] * width

        return box_coords

    def load_graph(self, graph_file):
        """Loads a frozen inference graph"""
        graph = tf.Graph()
        with graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(graph_file, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return graph
