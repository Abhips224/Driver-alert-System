import cv2
import dlib
from scipy.spatial import distance
from playsound import playsound
import time

def calculate_EAR(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear_aspect_ratio = (A+B)/(2.0*C)
	return ear_aspect_ratio

def mouth_aspect_ratio(mouth):
	A = dist.euclidean(mouth[13], mouth[19])
	B = dist.euclidean(mouth[14], mouth[18])
	C = dist.euclidean(mouth[15], mouth[17])

	MAR = (A + B + C) / 3.0
	return MAR

cap = cv2.VideoCapture(0)
face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
	_, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_detector(gray)

	for face in faces:
		face_landmarks = dlib_facelandmark(gray, face)
		leftEye = []
		rightEye = []
		count_frame=0
		for n in range(36, 42):
			x = face_landmarks.part(n).x
			y = face_landmarks.part(n).y
			leftEye.append((x, y))
			next_point = n + 1
			if n == 41:
				next_point = 36
			x2 = face_landmarks.part(next_point).x
			y2 = face_landmarks.part(next_point).y
			cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

		for n in range(42, 48):
			x = face_landmarks.part(n).x
			y = face_landmarks.part(n).y
			rightEye.append((x, y))
			next_point = n + 1
			if n == 47:
				next_point = 42
			x2 = face_landmarks.part(next_point).x
			y2 = face_landmarks.part(next_point).y
			cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

		left_ear = calculate_EAR(leftEye)
		right_ear = calculate_EAR(rightEye)

		EAR = (left_ear + right_ear) / 2
		EAR = round(EAR, 2)
		if EAR<0.26:

				cv2.putText(frame,"Drowsiness Alert!!",(20,400),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),4)
				print("Drowsy!")
				playsound("Annoying Alarm Tone1.mp3")
		print(EAR)




	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)
	if key == 27:
		break
cap.release()
cv2.destroyAllWindows()