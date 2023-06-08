import cv2
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread('../image/contour.png')
cv2.imshow('original', img)
# -------- 垂直 rotate 90 度 ------------------------
img2 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imshow('rotate 90', img2)

# ----- 3*3 高斯濾波器 -----------------------------
img3 = cv2.GaussianBlur(img2, (3, 3), sigmaX=0.8, sigmaY=0.8)
cv2.imshow('3*3GaussianBlur', img3)

# ------- 將前一處理後圖片取 SobelX, SobelY and addWeight(0.5, 0.5)----------

sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1)
sobelx = cv2.convertScaleAbs(sobelx)
sobely = cv2.convertScaleAbs(sobely)
sobelxy = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
cv2.imshow('sobelX, sobelY', sobelxy)

# ------- 輪廓偵測 (contours) 將找到的輪廓畫在原圖上 ----------

sobelxy_g = cv2.cvtColor(sobelxy, cv2.COLOR_BGR2GRAY)
cnts, hierarchy = cv2.findContours(sobelxy_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mask = cv2.drawContours(sobelxy, cnts, -1, (0,0,255),-1)
cv2.imshow('contour', mask)
cv2.waitKey(0)

# ------- 將上圖中的物件中心用圓圈標示出來, 並將面積標示於圓心旁邊 ---------
for i in range(len(cnts)):
    M = cv2.moments(cnts[i])
    cx = int(M['m10']/M['m00'])   # 中心點 x 座標
    cy = int(M['m01']/M['m00'])   # 中心點 y 座標
    
    area = cv2.contourArea(cnts[i])
    round_len = cv2.arcLength(cnts[i], True)  # 面積
    cv2.circle(mask, (cx,cy), 3, (0,255,0), -2)  # 週長
    cv2.putText(mask, f'area = {area}', (cx+10,cy), cv2.FONT_HERSHEY_SIMPLEX, .6, (0,255,0), 2, cv2.LINE_AA)
    print(f'輪廓 {i} 的中心點 ({cx}, {cy}),\t面積 : {area:10,.2f},\t週長 : {round_len:9,.2f}')
    # temp=np.zeros(im.shape, np.uint     
      

cv2.imshow('mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)