import cv2
from matplotlib import pyplot
import numpy as np
import sys

sys.path.insert(0, "../")
from utiltools import plot_img

# pega o caminho da imagem por meio de um parâmetro do terminal
img_path = sys.argv[1]
# verifica se não existe um parâmetro especificando o tamanho do kernel
if len(sys.argv) == 2:
    sys.argv.append(5)

# imagem BGR sem nenhum processamento
src_img = cv2.imread(img_path)

# converte a imagem para tons de cinza
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# # aplica o blur gaussiano (redução de ruído)
# suavized_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
# # cv2.threshold(src, X, Y, flag) --> se o valor de um pixel for maior que X, ele será mudado para Y
# r, mask = cv2.threshold(suavized_img, 150, 255, cv2.THRESH_BINARY)

# binarização adaptativa
mask = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY, 115, 1)

# relacionado à convolução
kernel = np.ones((int(sys.argv[2]), int(sys.argv[2])), np.uint8)

# realiza a erosão da imagem
eroded_img = cv2.erode(mask, kernel, iterations=1)

# realiza a dilatação da imagem
dilated_img = cv2.dilate(mask, kernel, iterations=1)

# erosão seguida de uma dilatação
er_di_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# dilatação seguida de uma erosão
di_er_img = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Solução Alternativa -->

# # aplica a erosão e depois a dilatação
# er_di_img = cv2.dilate(cv2.erode(mask, kernel, iterations=1),
#                        kernel, iterations=1)
#
# # aplica a dilatação e depois a erosão
# di_er_img = cv2.erode(cv2.dilate(mask, kernel, iterations=1),
#                        kernel, iterations=1)

# organiza as imagens e os textos para serem exibidos
imgs = [src_img, mask, eroded_img, dilated_img, er_di_img, di_er_img]
txts = ["Original", "Binarizada", "Erosão", "Dilatação",
        "Erosão e depois Dilatação", "Dilatação e depois Erosão"]

plot_img(*zip(imgs, txts))

pyplot.show()
