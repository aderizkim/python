#library#
import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*
import cvzone
import time
import sqlite3

#yolo model#
model=YOLO('config_nano.pt')

def VIDEO(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        print(point)
  
        
#tampilan#
cv2.namedWindow('VIDEO')
cv2.setMouseCallback('VIDEO', VIDEO)
cap=cv2.VideoCapture("video/1208.mp4")


#file coco#
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0
masuk={}
counter1=[]
counter3=[]
counter5=[]
counter7=[]

#garis vertical
cy1=300
cy2=350
offset=6

#tracking#
tracker1=Tracker()
tracker2=Tracker()
tracker3=Tracker()
tracker4=Tracker()

keluar={}
counter2=[]
counter4=[]
counter6=[]
counter8=[]


#database#
conn = sqlite3.connect("db.db")
cursor = conn.cursor()


# Seting waktu
start_time = time.time()
program_duration = 250

while (time.time() - start_time) < program_duration:
    ret, frame = cap.read()
    if not ret:
        break


    count += 1
    if count % 3 != 0:
        continue
    #ukuran layar
    frame=cv2.resize(frame,(1080,540))
   

    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list1=[]
    motorcycle=[]
    list2=[]
    car=[]
    list3=[]
    truck=[]
    list4=[]
    bus=[]
    for index,row in px.iterrows():
#        print(row)
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        #cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
        if 'motorcycle' in c:
            list1.append([x1,y1,x2,y2])
            motorcycle.append(c)
        elif 'car' in  c:
            list2.append([x1,y1,x2,y2])
            car.append(c)
        elif 'truck' in  c:
            list3.append([x1,y1,x2,y2])
            truck.append(c)
        elif 'bus' in  c:
            list3.append([x1,y1,x2,y2])
            bus.append(c)


    bbox1_id1=tracker1.update(list1)
    bbox2_id2=tracker2.update(list2)
    bbox3_id3=tracker3.update(list3)
    bbox4_id4=tracker4.update(list4)

            #Motor----------------#
    for bbox1 in bbox1_id1:
        for i in motorcycle:
            x3,y3,x4,y4,id1=bbox1
            cxm=int(x3+x4)//2
            cym=int(y3+y4)//2
            cv2.circle(frame, (cxm, cym), 4, (0, 255, 0), -1)
            #masuk
            if cy1<(cym+offset) and cy1>(cym-offset):
               cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),1)
               cvzone.putTextRect(frame,f'{id1}',(x3,y3),1,1)
               masuk[id1] = (cxm, cym)
            if id1 in masuk:
                if cy2 < (cym + offset) and cy2 > (cym - offset):
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id1}', (x3, y3), 1, 1)
                    if counter1.count(id1)==0:
                        counter1.append(id1)
            #keluar
            if cy2<(cym+offset) and cy2>(cym-offset):
               cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),1)
               cvzone.putTextRect(frame,f'{id1}',(x3,y3),1,1)
               keluar[id1] = (cxm, cym)
            if id1 in keluar:
                if cy1 < (cym + offset) and cy1 > (cym - offset):
                    cv2.circle(frame, (cxm, cym), 4, (0, 255, 0), -1)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id1}', (x3, y3), 1, 1)
                    if counter2.count(id1)==0:
                        counter2.append(id1)
            #Mobil----------------#
    for bbox2 in bbox2_id2:
        for h in car:
            x5,y5,x6,y6,id2=bbox2
            cxc=int(x5+x6)//2
            cyc=int(y5+y6)//2
            cv2.circle(frame, (cxc, cyc), 4, (0, 255, 0), -1)
            #masuk
            if cy1 < (cyc + offset) and cy1 > (cyc - offset):
                cv2.rectangle(frame,(x5,y5),(x6,y6),(0,0,255),1)
                cvzone.putTextRect(frame,f'{id2}',(x5,y5),1,1)
                masuk[id2] = (cxc, cyc)
            if id2 in masuk:
                if cy2 < (cyc + offset) and cy2 > (cyc - offset):
                    cv2.rectangle(frame, (x5, y5), (x6, y6), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id2}', (x5, y5), 1, 1)
                    if counter3.count(id2) == 0:
                        counter3.append(id2)
            # keluar
            if cy2 < (cyc + offset) and cy2 > (cyc - offset):
                cv2.rectangle(frame, (x5, y5), (x6, y6), (0, 0, 255), 1)
                cvzone.putTextRect(frame, f'{id2}', (x5, y5), 1, 1)
                keluar[id2] = (cxc, cyc)
            if id2 in keluar:
                if cy1 < (cyc + offset) and cy1 > (cyc - offset):
                    cv2.rectangle(frame, (x5, y5), (x6, y6), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id2}', (x5, y5), 1, 1)
                    if counter4.count(id2) == 0:
                        counter4.append(id2)
            # Truck----------------#
    for bbox3 in bbox3_id3:
        for t in truck:
            x7, y7, x8, y8, id3 = bbox3
            cxt = int(x7 + x8) // 2
            cyt = int(y7 + y8) // 2
            cv2.circle(frame, (cxt, cyt), 4, (0, 255, 0), -1)
            #masuk
            if cy1 < (cyt + offset) and cy1 > (cyt - offset):
                cv2.rectangle(frame, (x7, y7), (x8, y8), (0, 0, 255), 1)
                cvzone.putTextRect(frame, f'{id3}', (x7, y7), 1, 1)
                masuk[id3] = (cxt, cyt)
            if id3 in masuk:
                if cy2 < (cyt + offset) and cy2 > (cyt - offset):
                    cv2.rectangle(frame, (x7, y7), (x8, y8), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id3}', (x7, y7), 1, 1)
                    if counter5.count(id3) == 0:
                        counter5.append(id3)
            # keluar
            if cy2 < (cyt + offset) and cy2 > (cyt - offset):
                cv2.rectangle(frame, (x7, y7), (x8, y8), (0, 0, 255), 1)
                cvzone.putTextRect(frame, f'{id3}', (x7, y7), 1, 1)
                keluar[id3] = (cxt, cyt)
            if id3 in keluar:
                if cy1 < (cyt + offset) and cy1 > (cyt - offset):
                    cv2.rectangle(frame, (x7, y7), (x8, y8), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id3}', (x7, y7), 1, 1)
                    if counter6.count(id3) == 0:
                        counter6.append(id3)
            # Bus----------------#
        for bbox4 in bbox4_id4:
            for b in bus:
                x9, y9, x10, y10, id4 = bbox4
                cxb = int(x9 + x10) // 2
                cyb = int(y9 + y10) // 2
                cv2.circle(frame, (cxb, cyb), 4, (0, 255, 0), -1)
                #masuk
                if cy1 < (cyb + offset) and cy1 > (cyb - offset):
                    cv2.rectangle(frame, (x9, y9), (x10, y10), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id4}', (x9, y9), 1, 1)
                    masuk[id4] = (cxb, cyb)
                if id4 in masuk:
                    if cy2 < (cyb + offset) and cy2 > (cyb - offset):
                        cv2.rectangle(frame, (x9, y9), (x10, y10), (0, 0, 255), 1)
                        cvzone.putTextRect(frame, f'{id4}', (x9, y9), 1, 1)
                        if counter7.count(id4) == 0:
                            counter7.append(id4)
                # Keluar
                if cy2 < (cyb + offset) and cy2 > (cyb - offset):
                    cv2.rectangle(frame, (x9, y9), (x10, y10), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{id4}', (x9, y9), 1, 1)
                    keluar[id4] = (cxb, cyb)
                if id4 in keluar:
                    if cy1 < (cyb + offset) and cy1 > (cyb - offset):
                        cv2.rectangle(frame, (x9, y9), (x10, y10), (0, 0, 255), 1)
                        cvzone.putTextRect(frame, f'{id4}', (x9, y9), 1, 1)
                        if counter8.count(id4) == 0:
                            counter8.append(id4)

   

    cv2.line(frame,(2,cy1),(1018,cy1),(0,0,255),2)
    cv2.line(frame,(5, cy2),(1019, cy2),(0,255,255),2)


    motor_masuk=(len(counter1))
    motor_keluar = (len(counter2))
    mobil_masuk = (len(counter3))
    mobil_keluar = (len(counter4))
    truck_masuk = (len(counter5))
    truck_keluar = (len(counter6))
    bus_masuk = (len(counter7))
    bus_keluar = (len(counter8))

    # Masukan ke database
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO deteksi (timestamp, motor_masuk, motor_keluar, mobil_masuk, mobil_keluar, truck_masuk, truck_keluar, bus_masuk, bus_keluar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (timestamp, motor_masuk, motor_keluar, mobil_masuk, mobil_keluar, truck_masuk, truck_keluar, bus_masuk, bus_keluar))
    conn.commit()

    # Warna teks
    text_color = (255, 255, 255)  # Putih
    bg_color = (0, 0, 0)  # Hitam

    #cvzone.putTextRect(frame, f'motor_kanan:{motor_masuk}',(920, 30), 1, 1)
    #cvzone.putTextRect(frame, f'mobil_kanan:{mobil_masuk}', (920, 71), 1, 1)
    #cvzone.putTextRect(frame, f'truck_kanan:{truck_masuk}', (920, 112), 1, 1)
    #cvzone.putTextRect(frame, f'bus_kanan:{bus_masuk}', (920, 153), 1, 1)

    #cvzone.putTextRect(frame, f'motor_kiri:{motor_keluar}', (19,30),1,1)
    #cvzone.putTextRect(frame, f'mobil_kiri:{mobil_keluar}', (19, 71), 1, 1)
    #cvzone.putTextRect(frame, f'truck_kiri:{truck_keluar}', (19, 112), 1, 1)
    #cvzone.putTextRect(frame, f'bus_kiri:{bus_keluar}', (19, 153), 1, 1)

    # Kanan
    cv2.rectangle(frame, (820, 10), (1120, 50), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'motor_kanan:{motor_masuk}', (820, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.rectangle(frame, (820, 60), (1120, 100), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'mobil_kanan:{mobil_masuk}', (820, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.rectangle(frame, (820, 110), (1120, 150), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'truck_kanan:{truck_masuk}', (820, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.rectangle(frame, (820, 160), (1120, 200), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'bus_kanan:{bus_masuk}', (820, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    #kiri
    cv2.rectangle(frame, (100, 10), (230, 50), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'motor_kiri:{motor_keluar}', (19, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.rectangle(frame, (19, 60), (230, 100), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'mobil_kiri:{mobil_keluar}', (19, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.rectangle(frame, (19, 110), (230, 150), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'truck_kiri:{truck_keluar}', (19, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.rectangle(frame, (19, 160), (230, 200), bg_color, -1)  # Latar belakang teks (hitam)
    cv2.putText(frame, f'bus_kiri:{bus_keluar}', (19, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    cv2.imshow("VIDEO", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
# Tutup koneksi
conn.close()
cap.release()
cv2.destroyAllWindows()




