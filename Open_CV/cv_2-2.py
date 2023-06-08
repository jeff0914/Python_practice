import numpy as np
import random
import cv2
# ---- your code -----------------
gc = np.zeros((512, 512, 3), dtype='uint8') 

# count = 12
for i in range(13):
    b=random.randint(0,256)
    g=random.randint(0,256)
    r=random.randint(0,256)
    cv2.circle(gc, (256,256), i*20, (b, g, r), 5)
# circle : cv2.circle ( 影像, 圓心座標, 半徑, 顏色, 線條寬度 )
    
cv2.imshow('circle', gc)
    
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)