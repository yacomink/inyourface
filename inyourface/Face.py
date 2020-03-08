from google.cloud.vision import types, enums
import pprint

class Face(object):
    
    face_types = vars(enums.FaceAnnotation.Landmark.Type);

    def __init__(self, google_face):
        self.fd_bounding_poly = google_face.fd_bounding_poly
        self.bounding_poly = google_face.bounding_poly
        self.landmarks = google_face.landmarks
        self.roll_angle = google_face.roll_angle
        self.tilt_angle = google_face.tilt_angle
        self.pan_angle = google_face.pan_angle
        self.detection_confidence = google_face.detection_confidence
        self.landmarking_confidence = google_face.landmarking_confidence
        self.joy_likelihood = google_face.joy_likelihood
        self.sorrow_likelihood = google_face.sorrow_likelihood
        self.anger_likelihood = google_face.anger_likelihood
        self.surprise_likelihood = google_face.surprise_likelihood
        self.under_exposed_likelihood = google_face.under_exposed_likelihood
        self.blurred_likelihood = google_face.blurred_likelihood
        self.headwear_likelihood = google_face.headwear_likelihood

    def get_landmark(self, landmark_name):
        return self.landmarks[ self.face_types.get(landmark_name.upper()) - 1 ]

    def get_landmark_coords(self, landmark_name):

        return (self.get_landmark(landmark_name).position.x,
                self.get_landmark(landmark_name).position.y)

    def get_eye_coords(self, side):
        (ex, ey) = self.get_landmark_coords(side + '_eye')
        ((lcx, lcy), (rcx, rcy)) = self.get_paired_landmark_coords(side + '_eye_%s_corner')
        return ((lcx, lcy), (ex, ey), (rcx, rcy))

    def get_paired_landmark_coords(self, landmark_name):
        return [self.get_landmark_coords( landmark_name % side ) for side in ['left', 'right']]
