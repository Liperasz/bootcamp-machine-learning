import cv2
import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

# capturar imagem da camera
cap = cv2.VideoCapture(0)

# carregando modelo para identificar os rostos (tirei o caminho pois tive que usar o caminho absoluto para funcionar)
cascade_path = ''
face_cascade = cv2.CascadeClassifier(cascade_path)

# carregando modelo para prever a expressao (tirei o caminho pois tive que usar o caminho absoluto para funcionar)
model_path = ''
model = load_model(model_path)

# expressoes faciais
expressions = ["Raiva", "Nojo", "Medo", "Feliz", "Triste", "Surpreso", "Neutro"]

font,font_size = cv2.FONT_HERSHEY_SIMPLEX, 0.7 

while True:
    
    # captura os frames da câmera
    conected, frame = cap.read()

    # se não conectou já encerra
    if not conected:
        break

    # convertendo o frame para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detectar faces
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=5,minSize=(30,30))

    # se detectou faces
    if len(faces) > 0:
        for (x, y, w, h) in faces:

            # desenha retângulo ao redor da face
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h+10),(255,50,50),2)
     
            # extrai apenas a região de interesse
            roi = gray[y:y + h, x:x + w]      
            # redimensiona
            roi = cv2.resize(roi, (48, 48))
            # converte pra float
            roi = roi.astype("float")
            # converção para array
            roi = img_to_array(roi)
            # muda o formato para incluir a dimensão das cores (1 dimensão, grayscale)
            roi = np.expand_dims(roi, axis=0)

            # faz a predição
            result = model.predict(roi)[0]
            print(result)
            if result is not None:
                # encontra a emoção com maior probabilidade
                result_predict = np.argmax(result)

                # escreve a emoção acima do rosto
                cv2.putText(frame,expressions[result_predict],(x,y-10), font, font_size,(255,255,255),1,cv2.LINE_AA)

            # mostra a imagem
            cv2.imshow('Emotion Detector', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break