import cv2
import numpy as np
# ------- your code ----------------------
img = cv2.imread('')
b, g, r = cv2.split(img)

b[100:400, 150:415] = 255
g[100:400, 150:415] = 128
r[100:400, 150:415] = 0

cv2.imshow('BGR', cv2.merge([b, g, r]))

cv2.imshow('GRB', cv2.merge([g, r, b]))

cv2.imshow('BBB', cv2.merge([b, b, b]))

cv2.waitKey(0)
cv2.destroyAllWindows()