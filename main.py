import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone



model=YOLO('best.pt')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        print(point)
  
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
            
        



cap=cv2.VideoCapture(0)


my_file = open("coco1.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)



count=0

while True:    
    ret,frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
   

    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
   

#    print(px)
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'person' in c:
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
            cvzone.putTextRect(frame,f'{c}',(x1,y1),2,2)
        else:
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cvzone.putTextRect(frame,f'{c}',(x1,y1),2,2)
            
    
    cv2.imshow("Hand Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF==27:
        break
cap.release()  
cv2.destroyAllWindows()




