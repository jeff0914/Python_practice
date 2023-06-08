import dlib
from skimage import io
# 使用 Dlib 的正面人臉檢測器 front_face_detector (取得預設的臉部偵測器)
detector = dlib.get_frontal_face_detector()
# 根據shape_predictor方法載入68個特徵點模型，此方法為人臉表情識別的偵測器 (Dlib 的68點模型)
modelname = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(modelname)
img = io.imread("Faceimage.jpg")
# 生成 Dlib 的影像視窗
win = dlib.image_window()
# 顯示要檢測的影像
win.set_image(img)
# 使用 detector 檢測器來檢測影像中的人臉
faces = detector(img,1)
print("人臉數:",len(faces))

# 繪製矩形輪廓
win.add_overlay(faces)
# 繪製兩個 overlay, 人臉外接矩形框與面部特徵框

for i, d in enumerate(faces):
    print("第", i+1, "個人臉的矩形框座標 :", "left:",d.left(),
         "right:",d.right(), "top:",d.top(),"bottom:",d.bottom())
    # 使用 predictor 來計算面部輪廓
    shape = predictor(img, faces[i])
    # 繪製面部輪廓
    win.add_overlay(shape)

# 保持影像
dlib.hit_enter_to_continue()