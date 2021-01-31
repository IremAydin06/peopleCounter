import imutils
import cv2

avg = None
video = cv2.VideoCapture("C:\\Users\\Lenovo\\Desktop\\Bitirme_projesi\\counter2.mp4")
xDegerleri = list()
hareket = list()
sayac1 = 0
sayac2 = 0

#Bir python listesindeki çoğunluğu bulmaya yarar.
def find_majority(k):    #https://stackoverflow.com/questions/20038011/trying-to-find-majority-element-in-a-list
   myMap = {}
   maksimum = ('', 0)  # (meydana gelen öge, oluşumlar)

   for n in k:
       if n in myMap:
           myMap[n] += 1
       else:
           myMap[n] = 1

       # Hareket halindeyken maksimum değeri takip eder
       if myMap[n] > maksimum[1]: maksimum = (n, myMap[n])

   return maksimum


while 1:
   ret, frame = video.read()
   flag = True
   text = ""

   frame = imutils.resize(frame, width=500)            #video boyutu
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      #griye çevirme
   gray = cv2.GaussianBlur(gray, (21, 21), 0)          #netlik-bulanıklık ayarı

   if avg is None:
       print ("[INFO] starting background model...")
       avg = gray.copy().astype("float")
       continue

   # delta görüntüsünü eşleyin ve bir dizi genişleme uygulayın
   # delikleri doldurmaya yardımcı olmak için
   cv2.accumulateWeighted(gray, avg, 0.5)
   frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
   thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
   thresh = cv2.dilate(thresh, None, iterations=2)
   cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   for c in cnts:
       if cv2.contourArea(c) < 5000:                  #kontur çıkarma
           continue
       (x, y, w, h) = cv2.boundingRect(c)             #çerçeve oluşturma
       xDegerleri.append(x)
       cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)    #çerçeve boyut ve renk ayarı
       flag = False

   no_x = len(xDegerleri)

   if (no_x > 2):
       fark = xDegerleri[no_x - 1] - xDegerleri[no_x - 2]
       if (fark > 0):
           hareket.append(1)
       else:
           hareket.append(0)

   if flag is True:
       if (no_x > 5):
           val, zaman = find_majority(hareket)
           if val == 1 and zaman >= 15:
               sayac1 += 1
           else:
               sayac2 += 1

       xDegerleri = list()
       hareket = list()

   cv2.line(frame, (260, 0), (260, 480), (0, 255, 0), 2) #videodaki line (x, y, renk, kalınlık)
   #cv2.line(frame, (420, 0), (420, 480), (0, 255, 0), 2)

   # cv2.FONT_HERSHEY_SIMPLEX = Yazı tipini belirtir.
   cv2.putText(frame, "Cikan Sayisi: {}".format(sayac1), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
   cv2.putText(frame, "Giren Sayisi: {}".format(sayac2), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
   cv2.imshow("Frame", frame)
   cv2.imshow("Gray", gray)
   cv2.imshow("FrameDelta", frameDelta)

   key = cv2.waitKey(1) & 0xFF
   if key == ord('q'):            #q tuşuna basıldığında kapatır.
       break

video.release()                   #videoyu serbest bırakır.
cv2.destroyAllWindows()           #pencereleri kapatır.
