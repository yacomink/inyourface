import google.cloud.vision.face

class Face(google.cloud.vision.face.Face):
    @classmethod
    def from_google_face(cls, google_face):
        face_data = {
            'angles': google_face._angles,
            'bounds': google_face._bounds,
            'detection_confidence': google_face._detection_confidence,
            'emotions': google_face._emotions,
            'fd_bounds': google_face._fd_bounds,
            'headwear_likelihood': google_face._headwear_likelihood,
            'image_properties': google_face._image_properties,
            'landmarks': google_face._landmarks,
            'landmarking_confidence': google_face._landmarking_confidence,
        }
        return cls(**face_data)

    def get_landmark_coords(self, landmark_name):

        return (getattr(self.landmarks, landmark_name).position.x_coordinate,
                getattr(self.landmarks, landmark_name).position.y_coordinate)

    def get_eye_coords(self, side):
        (ex, ey) = self.get_landmark_coords(side + '_eye')
        ((lcx, lcy), (rcx, rcy)) = self.get_paired_landmark_coords(side + '_eye_%s_corner')
        return ((lcx, lcy), (ex, ey), (rcx, rcy))

    def get_paired_landmark_coords(self, landmark_name):
        return map(lambda side: self.get_landmark_coords( landmark_name % side ), ['left', 'right'])
