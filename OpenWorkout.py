import pickle
import cv2
import os
from sys import platform
from face.draw_boundary import detect_face
from body.draw_body import detect_body as dBody
from body.predict_drowBody import detect_body as pdBody
from tkinter import *
import gui

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
        sys.path.append('/usr/local/python')
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


class OpenWorkpout:
    print('OpenWorkout Ok...')

    def __init__(self, filename, nameEx, nameEx2,typeWork):
        self.filename = filename
        self.nameEx = nameEx
        self.nameEx2 = nameEx2
        self.typeWork  = typeWork
        print('filename = ',self.filename)
        print('nameEx = ',self.nameEx)
        print('nameEx2 = ',self.nameEx2)
    def _OpenCVpose(self):
        print(type(self.filename), self.filename)
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "body/models/"

        # impost model face
        faceCascade = cv2.CascadeClassifier('face/model/haarcascade_frontalface_default.xml')

        # impost classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("face/model/classifier.xml")
        try:
            if self.nameEx == 'predictVdo':
                file_model = open('model/'+self.nameEx2+'/MLPClassifier.pkl', 'rb')
                # file_model = open('model/'+self.nameEx2+'/Knn.pkl', 'rb')
                # file_model = open('model/MLPClassifier.pkl', 'rb')
                self.model = pickle.load(file_model)
                file_model.close()
        except IOError as e:
            print(e)

        try:
            # Starting OpenPose
            opWrapper = op.WrapperPython()
            opWrapper.configure(params)
            opWrapper.start()

            # Process Image
            datum = op.Datum()
            # imageToProcess = cv2.VideoCapture(0)

            imageToProcess = cv2.VideoCapture(self.filename)
            img_id = 1
            if self.nameEx != 'predictVdo':
                path = [os.path.join('dataSet/' + self.nameEx, f) for f in os.listdir('dataSet/' + self.nameEx)]
                if len(path) >= 1:
                    if self.nameEx != 'cam':
                        img_id = len(path)
            while (imageToProcess.isOpened()):
                # Read Video
                ret, frame = imageToProcess.read()


                # face
                # f1 = detect_face(ret, frame, faceCascade, img_id, clf)

                # datum.openpose input data

                datum.cvInputData = frame
                opWrapper.emplaceAndPop([datum])
                bodyKeypoints = datum.poseKeypoints
                try:
                    if self.nameEx == 'predictVdo':
                        f1 = pdBody(frame, bodyKeypoints, img_id, self.nameEx, self.nameEx2,self.model)
                    if self.nameEx != 'predictVdo':
                        f1 = dBody(frame, bodyKeypoints, img_id, self.nameEx)
                except Exception as e:
                    print(e)

                # print("Body keypoints: \n" + str(datum.poseKeypoints))
                f = cv2.flip(f1, 1)

                cv2.putText(f, str('close  =  "Q"'), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1)
                cv2.putText(f, str(self.typeWork), (10, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
                if self.nameEx == 'predictVdo':
                    cv2.putText(f, str(self.nameEx2), (10, 125), cv2.FONT_HERSHEY_DUPLEX, 1, (65, 166, 42), 1)

                cv2.imshow('OpenWorkOut', f)
                # cv2.imshow('OpenWorkOut')
                img_id += 1
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    break


        except Exception as e:
            print(e)
            imageToProcess.release()
            cv2.destroyAllWindows()
            # sys.exit(-1)

        imageToProcess.release()
        cv2.destroyAllWindows()

# if __name__ == '__main__':
#
#     opw = OpenWorkpout(0, 'cam', 'Dumbbell Shoulder Press')
#     opw._OpenCVpose()
# #
