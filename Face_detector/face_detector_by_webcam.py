import cv2 as cv
import dlib
# 使用 Dlib 的正面人臉檢測器 front_face_detector (取得預設的臉部偵測器)
detector = dlib.get_frontal_face_detector()
# 利用官方提供的模型建構特徵提取器
modelname = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(modelname)
# 選擇第一隻攝影機
cap = cv.VideoCapture(0)
#當攝影機打開時，對每個frame進行偵測
while cap.isOpened():
    #讀出frame資訊
    ret, frame = cap.read()
    #給68特徵點辨識取得一個轉換顏色的frame (BGR必須轉換成RGB)
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # 使用 detector 檢測器來檢測影像中的人臉
    faces = detector(img,0)
    # 使用 enumerate 函數遍歷序列中的元素以及他們的下標
    # k 即為人臉序號
    for k, d in enumerate(faces):
        # 使用 predictor 進行人臉關鍵點辨識, shape 為傳回的結果
        shape = predictor(img, d)
        #繪製68個特徵點 (shape.part(i)是第i個特徵點)
        for index, pt in enumerate(shape.parts()):
            pt_pos = (pt.x, pt.y)
            cv.circle(frame, pt_pos, 1, (0,255,0),2)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(frame, str(index+1),pt_pos,font,0.3,(0,0,255),1,cv.LINE_AA)
    cv.imshow("Frame", frame)
    key = cv.waitKey(10)
    if key == 27:   # 當按下 Esc 鍵時離開
        print(key)
        break
cap.release()
cv.destroyAllWindows()    