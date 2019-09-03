#!/usr/bin/env python
# -*- coding: utf-8 -*-
class OpenWorkout:

    import json as js
    import sys
    import cv2
    import os
    from sys import platform
    from face.draw_boundary import detect_face
    from body.draw_body import detect_body
    from GUI.mainGUI import MainPage as MP
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('/usr/local/python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "body/models/"

    # impost model face
    faceCascade = cv2.CascadeClassifier('face/model/haarcascade_frontalface_default.xml')

    # impost classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("face/model/classifier.xml")
    img_id = 0
    try:
        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        # imageToProcess = cv2.VideoCapture(0)
        imageToProcess = cv2.VideoCapture(0)
        img_id = 0
        while (True):
            # Read Video
            ret, frame = imageToProcess.read()
            # face
            f1 = detect_face(frame, faceCascade, img_id, clf)

            # datum.openpose input data

            datum.cvInputData = frame
            opWrapper.emplaceAndPop([datum])
            bodyKeypoints = datum.poseKeypoints
            try:
                detect_body(frame, bodyKeypoints,img_id)
            except Exception as e:
                print(e)

            # print("Body keypoints: \n" + str(datum.poseKeypoints))


            cv2.imshow('OpenWorkOut',f1)
            img_id += 1
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
        imageToProcess.release()
        cv2.destroyAllWindows()


    except Exception as e:
        print(e)
        sys.exit(-1)


# import cv2
#
# if __name__ == '__main__':
#
#     video = cv2.VideoCapture("video.mp4");
#
#     # Find OpenCV version
#     (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
#
#     if int(major_ver) < 3:
#         fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
#         print
#         "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
#     else:
#         fps = video.get(cv2.CAP_PROP_FPS)
#         print
#         "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)
#
# video.release();