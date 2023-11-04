import asyncio

from cvzone.ClassificationModule import Classifier
import cv2
import iothub

choice = input("Chose your exercise: ")

cap = cv2.VideoCapture(1)

if choice == "1":
    classifier = Classifier('Resources/Model/Shoulders.h5', 'Resources/Model/Shoulders.txt')
elif choice == "2":
    classifier = Classifier('Resources/Model/Biceps.h5', 'Resources/Model/Biceps.txt')

while True:
    _, img = cap.read()
    imgResize = cv2.resize(img, (454, 340))

    prediction = classifier.getPrediction(img)
    print(prediction[1])
    classId = prediction[1]

    nr = str(prediction[1])

    with open('shoulders.txt', 'a') as file:
        file.write(nr)

    iothub.loop = asyncio.get_event_loop()
    iothub.loop.run_until_complete(iothub.send_message())

    cv2.imshow("Image", img)
    cv2.waitKey(1)
