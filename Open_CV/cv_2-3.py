import numpy as np
import cv2
import random
# ---- your code ---------------
gc = np.zeros((512, 512, 3), dtype='uint8') 

unit=72
for i in range(unit):
    b=random.randint(10,256)
    g=random.randint(10,256)
    r=random.randint(10,256)
    cv2.ellipse(gc, (256,256), (200,30),360/unit*i,0,360, (b, g, r), 1)
# ellipse : cv2.ellipse ( 影像, 中心座標, (長軸, 短軸), 旋轉角度, 起始角度, 結束角度, 顏色, 線條寬度 )    

cv2.imshow('circle', gc)


cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)