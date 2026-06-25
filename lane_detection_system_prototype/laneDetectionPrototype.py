import cv2
import numpy as np

video = cv2.VideoCapture("yol_videosu.mp4")

fps = video.get(cv2.CAP_PROP_FPS)

delay = int (1000/fps)

while True:
    
    check , catch = video.read()
    if not check:
        
        break
    
    catch = cv2.resize(catch ,(720,480) )
    # cv2.imshow("yol" , catch)
    gray = cv2.cvtColor(catch , cv2.COLOR_BGR2GRAY)
    blur= cv2.GaussianBlur(gray, (5,5) , 0)
    kenarlar = cv2.Canny(blur ,50 , 150 )

    yukseklik , genislik = kenarlar.shape

    ucgen_koordinat = np.array ([[
        (int(genislik * 0.01), yukseklik),          # Sol alt (Biraz daha dışa açtık)
        (int(genislik * 0.48), int(yukseklik * 0.53)), # Sol tepe (Ufuk çizgisine yaklaştırdık)
        (int(genislik * 0.56), int(yukseklik * 0.58)), # Sağ tepe
        (int(genislik * 0.65), yukseklik)#sağ alt
    ]],dtype=np.int32)

    maske = np.zeros_like(kenarlar)
    cv2.fillPoly(maske , ucgen_koordinat ,255 )
    maskelenmis= cv2.bitwise_and(kenarlar , maske)

    cizgiler = cv2.HoughLinesP(maskelenmis , 1 , np.pi/180 , threshold=90 , minLineLength=110 , maxLineGap=25 )

    
    sol_cizgiler=[]
    sag_cizgiler=[]


    if cizgiler is not None:
        for cizgi in cizgiler:
            x1,y1,x2,y2 = cizgi[0]
            
            parametreler=np.polyfit((x1,x2) , (y1,y2) , 1)
            egim= parametreler[0]
            y_kesim= parametreler[1]
            if egim < -0.3: # Çok yatay gürültüleri eliyoruz
                sol_cizgiler.append((egim, y_kesim))
            elif egim > 0.3:
                sag_cizgiler.append((egim, y_kesim))
    cizgi_resmi = np.zeros_like(catch)
    ekran_merkezi = genislik // 2
    
    
    if len(sol_cizgiler) > 0:
        sol_ortalama = np.average(sol_cizgiler, axis=0)
        sol_egim, sol_y_kesim = sol_ortalama
        
        y1 = yukseklik
        y2 = int(yukseklik * 0.55)
        x1 = int((y1 - sol_y_kesim) / sol_egim)
        x2 = int((y2 - sol_y_kesim) / sol_egim)
        
        cv2.line(cizgi_resmi, (x1, y1), (x2, y2), (255, 0, 0), 10)
        
    
    if len(sag_cizgiler) > 0:
        sag_ortalama = np.average(sag_cizgiler, axis=0)
        sag_egim, sag_y_kesim = sag_ortalama
        y1 = yukseklik
        y2 = int(yukseklik * 0.55)
        x1 = int((y1 - sag_y_kesim) / sag_egim)
        x2 = int((y2 - sag_y_kesim) / sag_egim)
        
        cv2.line(cizgi_resmi, (x1, y1), (x2, y2), (255, 0, 0), 10)

    
    

    son_cikti= cv2.addWeighted(catch , 0.8 , cizgi_resmi , 1 , 0)
    cv2.imshow("Canli Otonom Serit Takibi", son_cikti)

    if cv2.waitKey(delay) & 0xFF == ord("p"):
        break


cv2.destroyAllWindows()


        





