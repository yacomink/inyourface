# Cribbed heavily from https://github.com/spmallick/learnopencv/blob/master/FaceSwap/faceSwap.py
import sys, os, io
import numpy as np
import cv2
from google.cloud import vision

import random
from PIL import Image, ImageDraw, ImageFilter
import math

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "swap"
    source_url = ""
    source_faces = []
    frames = [0]

    def manipulate_frame(self, frame_image, faces, index):
        # Read images
        dest = np.array(frame_image.convert('RGB'))
        dest_faces = faces
        mask = np.zeros(dest.shape, dtype = dest.dtype)

        if len(self.source_faces) == 0:
            for source in self.secondary_image:
                output = io.BytesIO()
                source.save(output, format="JPEG")
                secondary_faces = self.get_faces(output.getvalue())
                output.close()
                converted_source = np.array(source.convert('RGB'));
                for face in secondary_faces:
                    self.source_faces.append( (face, converted_source) )


        j = 0
        for dest_face in dest_faces:
            (source_face, source_image) = self.source_faces[j % len(self.source_faces)]
            try:
                (dest, mask) = self.pasteOne(source_image, dest, source_face, dest_face, mask)
            except Exception as e:
                pass
            j = j + 1

        frame_image.paste(Image.fromarray(dest), mask=Image.fromarray(mask).convert('L').filter(ImageFilter.GaussianBlur(4)))
        return frame_image

    def getPoints(self, face):
        points = []
        for feature in ('left_of_left_eyebrow',
                        'right_of_left_eyebrow',
                        'left_of_right_eyebrow',
                        'right_of_right_eyebrow',
                        'midpoint_between_eyes',
                        'nose_tip',
                        'upper_lip',
                        'lower_lip',
                        'mouth_left',
                        'mouth_right',
                        'mouth_center',
                        'nose_bottom_right',
                        'nose_bottom_left',
                        'nose_bottom_center',
                        'left_eye_top_boundary',
                        'left_eye_right_corner',
                        'left_eye_bottom_boundary',
                        'left_eye_left_corner',
                        'right_eye_top_boundary',
                        'right_eye_right_corner',
                        'right_eye_bottom_boundary',
                        'right_eye_left_corner',
                        'left_eyebrow_upper_midpoint',
                        'right_eyebrow_upper_midpoint',
                        'left_ear_tragion',
                        'right_ear_tragion',
                        'left_eye_pupil',
                        'right_eye_pupil',
                        'forehead_glabella',
                        'chin_gnathion',
                        'chin_left_gonion',
                        'chin_right_gonion'):
            points.append( (int(getattr(face.landmarks, feature).position.x_coordinate), int(getattr(face.landmarks, feature).position.y_coordinate)))
        return points

    # Apply affine transform calculated using srcTri and dstTri to src and
    # output an image of size.
    def applyAffineTransform(self, src, srcTri, dstTri, size) :
        
        # Given a pair of triangles, find the affine transform.
        warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
        
        # Apply the Affine Transform just found to the src image
        dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

        return dst


    # Check if a point is inside a rectangle
    def rectContains(self, rect, point) :
        if point[0] < rect[0] :
            return False
        elif point[1] < rect[1] :
            return False
        elif point[0] > rect[0] + rect[2] :
            return False
        elif point[1] > rect[1] + rect[3] :
            return False
        return True


    #calculate delanauy triangle
    def calculateDelaunayTriangles(self, rect, points):
        #create subdiv
        subdiv = cv2.Subdiv2D(rect);
        
        # Insert points into subdiv
        for p in points:
            subdiv.insert(p) 
        
        triangleList = subdiv.getTriangleList();
        
        delaunayTri = []
        
        pt = []    
        
        count= 0    
        
        for t in triangleList:        
            pt.append((t[0], t[1]))
            pt.append((t[2], t[3]))
            pt.append((t[4], t[5]))
            
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])        
            
            if self.rectContains(rect, pt1) and self.rectContains(rect, pt2) and self.rectContains(rect, pt3):
                count = count + 1 
                ind = []
                for j in xrange(0, 3):
                    for k in xrange(0, len(points)):                    
                        if(abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                            ind.append(k)                            
                if len(ind) == 3:                                                
                    delaunayTri.append((ind[0], ind[1], ind[2]))
            
            pt = []        
                
        
        return delaunayTri
            

    # Warps and alpha blends triangular regions from img1 and img2 to img
    def warpTriangle(self, img1, img2, t1, t2) :

        # Find bounding rectangle for each triangle
        r1 = cv2.boundingRect(np.float32([t1]))
        r2 = cv2.boundingRect(np.float32([t2]))

        # Offset points by left top corner of the respective rectangles
        t1Rect = [] 
        t2Rect = []
        t2RectInt = []

        for i in xrange(0, 3):
            t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
            t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
            t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


        # Get mask by filling triangle
        mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
        cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

        # Apply warpImage to small rectangular patches
        img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        #img2Rect = np.zeros((r2[3], r2[2]), dtype = img1Rect.dtype)
        
        size = (r2[2], r2[3])

        img2Rect = self.applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
        
        img2Rect = img2Rect * mask

        # Copy triangular region of the rectangular patch to the output image
        img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )
         
        img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect 

    def pasteOne(self, source, dest, source_face, dest_face, mask):
        img1Warped = np.copy(dest)
        points1 = self.getPoints(source_face)
        points2 = self.getPoints(dest_face)
        
        # Find convex hull
        hull1 = []
        hull2 = []

        hullIndex = cv2.convexHull(np.array(points2), returnPoints = False)
        for i in xrange(0, len(hullIndex)):
            hull1.append(points1[hullIndex[i][0]])
            hull2.append(points2[hullIndex[i][0]])
        
        
        # Find delanauy traingulation for convex hull points
        sizeImg2 = dest.shape    
        rect = (0, 0, sizeImg2[1], sizeImg2[0])
         
        dt = self.calculateDelaunayTriangles(rect, hull2)
        
        if len(dt) == 0:
            quit()
        
        # Apply affine transformation to Delaunay triangles
        for i in xrange(0, len(dt)):
            t1 = []
            t2 = []
            
            #get points for img1, img2 corresponding to the triangles
            for j in xrange(0, 3):
                t1.append(hull1[dt[i][j]])
                t2.append(hull2[dt[i][j]])
            
            self.warpTriangle(source, img1Warped, t1, t2)
        
                
        # Calculate Mask
        hull8U = []
        for i in xrange(0, len(hull2)):
            hull8U.append((hull2[i][0], hull2[i][1]))
        
        cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))
        
        r = cv2.boundingRect(np.float32([hull2]))    
        
        center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))
        
        return (img1Warped, mask)
        
        # Clone seamlessly, looks better but much slower
        # output = cv2.seamlessClone(np.uint8(img1Warped), dest, mask, center, cv2.NORMAL_CLONE)
        # return output

        
            
