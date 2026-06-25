import cv2
import numpy as np

resim = cv2.imread("yol.jpg") #read image

gray= cv2.cvtColor(resim , cv2.COLOR_BGR2GRAY)# convert to gray

blur = cv2.GaussianBlur(gray , (5,5) , 0) #apply gaussian blur for more smooth image

edges = cv2.Canny(blur , 50 , 150)

# cv2.imshow("image",resim)



cv2.imshow("EDGES",edges)

#we have some tree edges sky edges on the image that we just made. we need to remove them
#we will use roi masking

yukseklik , genislik = edges.shape

#opencv de 0,0 noktasında x sağa doğru y aşağı doğru hareket eder.

ucgen_koordinat = np.array([[
    (0, yukseklik),                           # 1. Sol Alt Köşe
    (int(genislik * 0.40), int(yukseklik * 0.40)), # 2. Sol Tepe (Yolu yukarıdan yakalasın)
    (int(genislik * 0.60), int(yukseklik * 0.40)), # 3. Sağ Tepe
    (genislik, yukseklik)                     # 4. Sağ Alt Köşe
]], dtype=np.int32)

mask = np.zeros_like(edges) #simsiyah boş bir maske matrisi

cv2.fillPoly(mask , ucgen_koordinat , 255) # beyaza boyadık

maskeli_yol = cv2.bitwise_and(edges , mask) #sadece maskenin beyaz olduğu yerleri alıyoruz.

cv2.imshow("maskeli yol" , maskeli_yol)

cizgiler= cv2.HoughLinesP(maskeli_yol, 1 ,np.pi/180 , threshold=50 , minLineLength=40, maxLineGap=20)
#1 : piksel cinsinden mesafe
#np.pi/180 radyan cinsinden açı çözünürlüğü
#threshold çizgi sayılması için yan yana gelecek en az piksel miktarı 
#minlinelength çizgi kabul edilecek minimum çizgi boyutu
#maxlinegap kesikli çizgileri birleştirk-mek için max boşluk
cizgi_resmi = np.zeros_like(resim)
#çizgileri çizeceğimiz şeffaf katman

if cizgiler is not None :
    for cizgi in cizgiler :
        x1,y1,x2,y2 = cizgi[0] #başlangıç ve bitiş koordinatları
        cv2.line (cizgi_resmi , (x1,y1), (x2,y2), (255,0 , 0) ,5)

son_goruntu = cv2.addWeighted(resim , 0.8 , cizgi_resmi , 1 , 0)

cv2.imshow("şerit takibi" , son_goruntu)


cv2.waitKey(0)