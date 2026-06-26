import cv2
import numpy as np

def process_frame(frame):
    gray_frame= cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    blur= cv2.GaussianBlur(gray_frame , (5,5) , 0)
    edges = cv2.Canny(blur , 5 , 150)

    #ROI (Region of Interest)
    height , width= frame.shape[:2]

    roi_vertices = [(0,height), (width*0.44 , height*0.70), (width , height)]
    mask = np.zeros_like(gray_frame)
    cv2.fillPoly(mask , np.int32([roi_vertices]) , 255 )
    masked_img = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(masked_img ,1, np.pi/180 ,threshold=50 , minLineLength= 50 , maxLineGap= 80 )
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(frame , (x1,y1), (x2,y2) , (255,0,0) ,5)
    return frame , blur ,edges , mask , masked_img

cap = cv2.VideoCapture("yol_videosu.mp4")

while True:
    ret , frame = cap.read()
    if ret == False:
        break

    frame , blur, edges , mask , masked_img =process_frame(frame)
    cv2.imshow("hayirlisi" , frame)
    cv2.imshow("hayirlis" , edges)
    cv2.imshow("hayirlsi" , mask)
    cv2.imshow("hayrlisi" , masked_img)
    cv2.imshow("haylisi" , blur)

    if cv2.waitKey(20) & 0xFF == ord ("p"):
        break

cap.release()
cv2.destroyAllWindows()   

