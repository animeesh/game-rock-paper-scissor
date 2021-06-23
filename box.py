import cv2
import time
import mediapipe as mp
import random


class handdetector():
    def __init__(self, mode=False, maxhands=1, det_confi=0.5, track_confi=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.det_confi = det_confi
        self.track_confi = track_confi

        self.mphands = mp.solutions.hands

        self.mpdraw = mp.solutions.drawing_utils
        self.hands = self.mphands.Hands(self.mode, self.maxhands, self.det_confi, self.track_confi)

    #
    def findhands(self, img, draw=True):
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handsmp in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handsmp, self.mphands.HAND_CONNECTIONS)

        return img

    def findpositions(self, img, handno=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]

            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        return lmlist  #




def main():
# SET THE COUNTDOWN TIMER
# for simplicity we set it to 3
# We can also take this as input
    TIMER = int(3)
    gesture=[]
    detector = handdetector()
    tipids = [4, 8, 12, 16, 20]

    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:

        # Read and display each frame
        ret, img = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str("press Q to start & esc to end"), (50, 50), font, 1, (0, 255, 255), 4, cv2.LINE_AA)
        cv2.imshow("game",img)
        k = cv2.waitKey(125)

        # set the key for the countdown
        # to begin. Here we set q
        # if key pressed is q
        if k == ord('q'):
            prev = time.time()

            while TIMER >= 0:
                ret, img = cap.read()
                img = detector.findhands(img)
                lmlist = detector.findpositions(img)
                #gesture = []

                if len(lmlist) != 0:
                    fingers = []

                    # thumb
                    if lmlist[tipids[0]][1] > lmlist[tipids[0] - 1][1]:
                        fingers.append(1)

                    else:
                        fingers.append(0)
                    for id in range(1, 5):
                        if lmlist[tipids[id]][2] < lmlist[tipids[id] - 2][2]:
                            fingers.append(1)

                    else:
                        fingers.append(0)

                    totalfingers = fingers.count(1)
                    # print(totalfingers)

                    if totalfingers == 5:
                        gesture.append("paper")
                    elif totalfingers == 0:
                        gesture.append("rock")
                    elif totalfingers == 2:
                        gesture.append("scissor")
                    else:
                        gesture.append("try again")
                    # break
                    # maxges=(max(list(gesture),key=gesture.count))
                    print(gesture[-1])
                # Display countdown on each frame
                # specify the font and draw the
                # countdown using puttext
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(TIMER),(200, 250), font,4, (0, 255, 255),4, cv2.LINE_AA)
                cv2.imshow('a', img)
                #cv2.putText(img, str("press escape"), (200, 250), font, 4, (0, 255, 255), 4, cv2.LINE_AA)
                cv2.waitKey(125)

                # current time
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrease the counter
                if cur - prev >= 1:
                    prev = cur
                    TIMER = TIMER - 1

            else:
                ret, img = cap.read()

                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                #cv2.putText(img, str(gesture), (50, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('a', img)

                # time for which image displayed
                cv2.waitKey(2)
            cv2.putText(img, str(gesture[-1]), (50, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('a', img)

        elif k == 27:
            break
        '''success, img = cap.read()
        img = detector.findhands(img)
        # findpositions(img)
        lmlist = detector.findpositions(img)
        gesture = []'''


    # Press Esc to exit


    # close the camera
    cap.release()

    # close all the opened windows
    cv2.destroyAllWindows()

    #game code begins here


    boo=[]

    for i in range(len(gesture)):
        boo=(gesture[-1])
        print(boo)

    possible_action = ["rock", "paper", "scissor"]
    computer_action = random.choice(possible_action)

    print(f"\nyou chose :{boo},computer chose :{computer_action}.\n")

    # hear starts the real technique
    if boo == computer_action:
        print(f"both player selected {boo}.hence its a tie!")
    elif boo == "rock":
        if computer_action == "scissor":
            print("rock smashes scissor! you win")
        else:
            print("paper covers the rock! you lose")

    elif boo == "paper":
        if computer_action == "rock":
            print("paper covers the rock! you win")
        else:
            print("scissor cuts the paper! you lose")

    elif boo == "scissor":
        if computer_action == "rock":
            print("rock smashes scissor! you win")
        else:
            print("rock smashes the scissor! you lose")

    play_again = input("play again enter y/n  :")

if __name__ == '__main__':
    main()