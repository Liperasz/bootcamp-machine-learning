import cv2
import numpy as np

# importando a classe para capturar imagem da camera
cap = cv2.VideoCapture(0)

while True:

    # captura os frames da câmera
    _, frame = cap.read()
    # converte o frame da imagem para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Vermelho
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])

    # Máscara que isola as cores entre o low e o high red
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    # Calcula as imagens que devem ser processadas (nesse caso, tudo que é vermelho)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)

    # O processo se repete para as outras cores

    # Azul
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Verde
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Tudo menos branco
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostra o frame e o resultado
    cv2.imshow("Frame", frame)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break