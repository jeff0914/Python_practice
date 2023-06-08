import os
import face_recognition
# 已知人臉照片的檔案路徑
path = "c:\\FaceImage"   
files = os.listdir(path)
# 從目錄讀取所有的檔案至 files 中
know_names = []
know_faces = []
for file in files:
    filename = str(file)
    print(filename)
    know_names.append(filename)
    image = face_recognition.load_image_file(path+"\\"+filename)
    encoding = face_recognition.face_encodings(image)[0]
    know_faces.append(encoding)

unknown_Image = face_recognition.load_image_file("c:\\TestFace\\test.jpg")
unknown_face = face_recognition.face_encodings(unknown_Image)[0]
results = face_recognition.compare_faces(know_faces,unknown_face, tolerance=0.45)   #tolerance 可以調整判斷
print("辨識結果如下 :")
for i in range(len(know_names)):
    print(know_names[i]+":",end="")
    if results[i]:
        print("相同")
    else:
        print("不相同")