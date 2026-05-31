import cv2
import numpy as np

# capturar imagem da cãmera
cap = cv2.VideoCapture(0)

# carrega uma imagem de background
path = 'Card-22/assets/straw-hats.png'
img = cv2.imread(path)

# pega as proporções da câmera
h, w, c = cap.read()[1].shape

# redimensiona a imagem para o mesmo tamanho da câmera
bkg = cv2.resize(img, (w, h))

while True:

    # captura os frames da câmera
    _, frame = cap.read()
    # converte o frame da imagem para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # cor que vai ser substituída pela imagem de bkg
    low = np.array([0, 0, 200])
    high = np.array([180, 30, 255])
    # mascara de isolar a cor
    mask = cv2.inRange(hsv_frame, low, high)
    # mascara invertida
    mask_inv = cv2.bitwise_not(mask)
    # recorta a região da cor selecionada na imagem de bkg
    bkg_cut = cv2.bitwise_and(bkg, bkg, mask=mask)
    # recorta o restante da imagem original
    frame_cut = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # junta o background com o frame
    result = cv2.add(bkg_cut, frame_cut)

    # Mostra o frame e o resultado
    cv2.imshow("Chroma Key", result)

    key = cv2.waitKey(1)
    if key == 27:
        break