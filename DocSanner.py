import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *
#import cropImage as ci

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    font = cv2.FONT_HERSHEY_COMPLEX
    width, height = 250, 350
    arr = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if area > 1000:

            if len(approx) == 4:

                #(x, y, w, h) = cv2.boundingRect(approx)
                print(len(approx))
                cv2.drawContours(imgContour, cnt, -1, (0, 0, 255), 3)

                n = approx.ravel()
                print("AR: ", type(approx.ravel()))

                print("Approx R", approx.ravel())
                i = 0
                for j in n:
                    print("NN: ", type(n))

                    if i % 2 == 0:
                        x = n[i]
                        y = n[i + 1]

                        string = str(x) + " " + str(y)
                        arr.append(x)
                        arr.append(y)

                        cv2.putText(imgContour, string, (x, y), font, 0.5, (0, 255, 0))

                    i = i + 1

            for i in range(8):
                print(i, " ", arr[i])

            pts1 = np.float32([[arr[0], arr[1]], [arr[6], arr[7]], [arr[2], arr[3]], [arr[4], arr[5]]])
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            print("points2: ",pts2)
            matrix = cv2.getPerspectiveTransform(pts1, pts2)

            global imgOutput
            imgOutput = cv2.warpPerspective(imgContour, matrix, (width, height))



def get_image(img):
    # global p
    # p = False
    global imgContour

    imgContour = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    #v = np.median(imgBlur)
    # print("V:",type(v))

    # sigma = 0.33
    # lower_thresh = int(max(0, (1.0 - sigma) * v))
    # upper_thresh = int(min(255, (1.0 + sigma) * v))
    imgCanny = cv2.Canny(imgBlur, 100,100)
    #thresh = cv2.threshold(imgCanny, 127, 255, cv2.THRESH_BINARY)

    getContours(imgCanny)

    cv2.imshow("Grey_image", imgGray)
    cv2.imshow("imgBlur", imgBlur)
    cv2.imshow("Countor", imgContour)
    cv2.imshow("Final Output", imgOutput)
    # cv2.imshow("thresh", thresh)
    cv2.imshow("canny img ", imgCanny)

    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()


try:
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    print("File",file)
    img = cv2.imread(file)
    get_image(img)

except Exception as e:
    print("Error: ", e)

win = Tk()
win.geometry("350x400")
win.title("Do you want to save this file?")


def closewindow():
    print(" closewindow Value of p", p)
    # p=False
    exit()


def save_file():
    print(" save_file Value of p", p)
    # p = True
    print("ok ok done")
    try:
        cv2.imwrite('saved_img.jpg', imgOutput)
        print("Image saved!")
    except Exception as e1:
        print("E")
        print("Image not saved!")
    finally:
        print("Processing image...")
        print("Resized...")


b1 = Button(win, text="save", font="bold", command=save_file).pack()
b3 = Button(win, text="Exit", font="bold", command=closewindow).pack()
b4 = Button(win,text="Menual Crop", font="bold" ).pack()

win.mainloop()