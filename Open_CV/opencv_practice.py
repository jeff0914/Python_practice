import cv2
import time
import dlib
import numpy as np

# 讀取影片
cap = cv2.VideoCapture('Your video file path')

detector = dlib.get_frontal_face_detector() 

# 設置計時器和特效索引
start_time = time.time()
effect_index = 0
# 初始化幀數計數器
frame_count = 0
font = 2;    lt = 16
# 取得影片幀率
fps = int(cap.get(cv2.CAP_PROP_FPS))

while True:
    # 讀取當前幀
    ret, frame = cap.read()
    
    if ret:
         # 累加幀數
        frame_count += 1
        # 計算當前的FPS
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        # 將當前幀轉換為灰度影像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 在畫面上顯示當前偵數/FPS
        cv2.putText(frame, "Frame: {}".format(frame_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "FPS: {:.2f}".format(fps), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 執行人臉檢測
        face_rects, scores, idx = detector.run(frame, 0, -.5)
        # 在畫面上標出檢測到的人臉位置 # 標示分數
        for i, d in enumerate(face_rects):               # 取出所有偵測的結果
            x1, y1, x2, y2 = d.left(), d.top(), d.right(), d.bottom()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA) # 以方框標示偵測的人臉
            cv2.putText(frame, f'{scores[i]:.2f}, ({idx[i]:0.0f})', (x1, y1), font,          # 標示分數
                    0.7, (255, 255, 255), 1, lt)
        
        # 根據特效索引添加特效
        if effect_index == 0:
            #退色效果
            b, g, r = cv2.split(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.merge((b, r, g))
        elif effect_index == 1:
            # 邊緣檢測
            frame = cv2.Canny(frame, 50, 150)
        elif effect_index == 2:
            # 人臉馬賽克
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            for face in faces:
                x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
                w, h = x2 - x1, y2 - y1
                ksize = 15
                face_roi = frame[y1:y2, x1:x2]
                face_roi = cv2.resize(face_roi, (w // ksize, h // ksize), interpolation=cv2.INTER_NEAREST)
                face_roi = cv2.resize(face_roi, (w, h), interpolation=cv2.INTER_NEAREST)
                frame[y1:y2, x1:x2] = face_roi
        elif effect_index == 3:
            # 高斯模糊
            frame = cv2.GaussianBlur(frame, (15, 15), 0)
        elif effect_index == 4:
            # 膨脹效果
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            frame = cv2.dilate(frame, kernel)
        elif effect_index == 5:
            # 二值化
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        elif effect_index == 6:
            # 拉普拉斯濾波
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.Laplacian(gray, cv2.CV_64F)
        elif effect_index == 7:
            #  反轉顏色
            frame = cv2.bitwise_not(frame)
        elif effect_index == 8:
            # 縮放視窗
            height, width = frame.shape[:2]
            w = width // 2
            h = height // 2
            frame_resized = cv2.resize(frame, (w, h))

            # 建立四格視窗
            frame_origin = frame_resized.copy()
            frame_flip1 = cv2.flip(frame_resized, 0)
            frame_flip2 = cv2.flip(frame_resized, 1)
            frame_flip3 = cv2.flip(frame_resized, -1)
            
            # 添加不同的色彩
            frame_origin_gray = cv2.cvtColor(frame_origin, cv2.COLOR_BGR2GRAY)
            frame_flip1_gray = cv2.cvtColor(frame_flip1, cv2.COLOR_BGR2GRAY)
            frame_flip2_gray = cv2.cvtColor(frame_flip2, cv2.COLOR_BGR2GRAY)
            frame_flip3_gray = cv2.cvtColor(frame_flip3, cv2.COLOR_BGR2GRAY)

            frame_origin_color = cv2.applyColorMap(frame_origin_gray, cv2.COLORMAP_JET)
            frame_flip1_color = cv2.applyColorMap(frame_flip1_gray, cv2.COLORMAP_HOT)
            frame_flip2_color = cv2.applyColorMap(frame_flip2_gray, cv2.COLORMAP_COOL)
            frame_flip3_color = cv2.applyColorMap(frame_flip3_gray, cv2.COLORMAP_WINTER)

            # 在畫面中呈現四格視窗
            frame[0:h, 0:w] = frame_origin_color
            frame[0:h, w:2*w] = cv2.resize(frame_flip1_color, (w, h), interpolation=cv2.INTER_LINEAR)
            frame[h:2*h, 0:w] = cv2.resize(frame_flip2_color, (w, h), interpolation=cv2.INTER_LINEAR)
            frame[h:2*h, w:2*w] = cv2.resize(frame_flip3_color, (w, h), interpolation=cv2.INTER_LINEAR)

  

        # 顯示當前幀
        cv2.imshow('frame',  frame)
        
        # 每30個偵更換一次特效 (1秒) %9 9個特效
        if frame_count % 30 == 0:
            effect_index = (effect_index + 1) % 9
        
        # 按下'esc'鍵退出迴圈
        if cv2.waitKey(1) == 27:
            break
    else:
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)