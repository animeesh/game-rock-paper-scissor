import cv2
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
    prevtime = 0
    curtime = 0
    cap = cv2.VideoCapture(0)
    '''
    #cap.set(cv2.CAP_PROP_POS_MSEC,96000)
    cnt=0
    success=True
    fps=int(cap.get(cv2.CAP_PROP_FPS))
    '''
    detector = handdetector()
    tipids = [4, 8, 12, 16, 20]

    maxges=[]



    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        # findpositions(img)
        lmlist = detector.findpositions(img)
        gesture = []
        #cap.set(cv2.CAP_PROP_POS_FRAMES,500)
        #a,b=cap.read()
        '''
        if cnt%(5*fps)==0:
            cv2.imwrite("frame%d.jpg"%cnt,img)
        '''

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

            totalfingers=fingers.count(1)
            #print(totalfingers)



            if totalfingers ==5:
                gesture.append("paper")
            elif totalfingers==0:
                gesture.append("rock")
            elif totalfingers==2:
                gesture.append("scissor")
            else:
                gesture.append("try again")


            #maxges=(max(list(gesture),key=gesture.count))
            print(gesture)
            #gesture=("paper" if totalfingers==5,"stone" if totalfingers==0,"scisor" if totalfingers==2)

            # hears the game code begine

            '''
            possible_action = ["rock", "paper", "scissor"]
            computer_action = random.choice(possible_action)

            print(f"\nyou chose :{gesture},computer chose :{computer_action}.\n")

                # hear starts the real technique
            if gesture == computer_action:
                print(f"both player selected {gesture}.hence its a tie!")
            elif gesture == "rock":
                if computer_action == "scissor":
                    print("rock smashes scissor! you win")
                else:
                    print("paper covers the rock! you lose")

            elif gesture == "paper":
                if computer_action == "rock":
                        print("paper covers the rock! you win")
                else:
                        print("scissor cuts the paper! you lose")

            elif gesture == "scissor":
                if computer_action == "rock":
                    print("rock smashes scissor! you win")
                else:
                        print("rock smashes the scissor! you lose")

            play_again = input("play again enter y/n  :")
            if play_again.lower() != "y":
                break
            '''



        cv2.putText(img, str(gesture), (50, 70), cv2.FONT_HERSHEY_COMPLEX,1, (0, 0, 255),2)
        cv2.imshow("image", img)
        cv2.waitKey(1)
    #game begin
        '''
        boo=[]
        for i in range(len(gesture)):
            boo=(gesture[i])
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
        if play_again.lower() != "y":
            break
        break
        '''


if __name__ == '__main__':
    main()