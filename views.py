import base64
from django.conf import settings
from django.shortcuts import render
import os
import cv2
from mtcnn.mtcnn import MTCNN
from django.http import JsonResponse
from django.shortcuts import render, redirect


def login(request):
    return render(request, 'app_biometricos/login.html')

def registro(request):
    if request.method == 'POST':
        usuario_info = request.POST.get('usuario')
        contra_info = request.POST.get('contra')

        with open(usuario_info, "w") as archivo:
            archivo.write(usuario_info + "\n")
            archivo.write(contra_info)

        mensaje = "Registro Convencional Exitoso"

        return render(request, 'app_biometricos/registro_exitoso.html', {'mensaje': mensaje})
    
    return render(request, 'app_biometricos/registro.html')

def guardar_imagen(request):
    if request.method == 'POST' and 'imagen_data' in request.POST:
        imagen_data = request.POST['imagen_data']
        # Aquí puedes guardar la imagen en tu sistema de archivos o en una base de datos

        return JsonResponse({'message': 'Imagen guardada exitosamente.'})
    else:
        return JsonResponse({'error': 'No se proporcionó ninguna imagen.'})

def guardar_imagen_facial(request):
    # Código para guardar la imagen de registro facial aquí
    return JsonResponse({'message': 'Imagen guardada exitosamente.'})

def registro_facial(request):
    if request.method == 'POST':
        usuario_img = request.POST.get('usuario_img')
        image_filename = f"{usuario_img}.jpg"

        images_directory = os.path.join(settings.MEDIA_ROOT, 'user_images')
        os.makedirs(images_directory, exist_ok=True)

        image_path = os.path.join(images_directory, image_filename)

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            cv2.imwrite(image_path, frame)

            detector = MTCNN()
            caras = detector.detect_faces(frame)

            for i, resultado in enumerate(caras):
                x1, y1, ancho, alto = resultado['box']
                x2, y2 = x1 + ancho, y1 + alto
                cara_recortada = frame[y1:y2, x1:x2]
                cara_recortada = cv2.resize(cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)
                
                cara_filename = f"{usuario_img}cara{i}.jpg"
                cara_path = os.path.join(images_directory, cara_filename)
                cv2.imwrite(cara_path, cara_recortada)

            return render(request, 'app_biometricos/registro_exitoso.html')

        else:
            mensaje = "Error al capturar el frame de la cámara"
            return render(request, 'app_biometricos/verificacion_fallida.html', {'mensaje': mensaje})

    return render(request, 'app_biometricos/registro_facial.html')

def capture_photo(request):
    usuario_img = request.POST.get('usuario_img')
    image_filename = f"{usuario_img}_captura.jpg"

    images_directory = os.path.join(settings.MEDIA_ROOT, 'user_images')
    os.makedirs(images_directory, exist_ok=True)

    image_path = os.path.join(images_directory, image_filename)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite(image_path, frame)
        return render(request, 'app_biometricos/registro_facial.html', {'usuario_img': usuario_img})

    mensaje = "Error al capturar el frame de la cámara"
    return render(request, 'app_biometricos/verificacion_fallida.html', {'mensaje': mensaje})


# def iniciar_sesion(request):
#     if request.method == 'POST':
#         # Capturar la foto
#         cap = cv2.VideoCapture(0)
#         ret, frame = cap.read()
#         cap.release()

#         if ret:
#             # Procesar la foto capturada
#             detector = MTCNN()
#             caras = detector.detect_faces(frame)
#             if caras:
#                 x1, y1, ancho, alto = caras[0]['box']
#                 x2, y2 = x1 + ancho, y1 + alto
#                 cara_recortada = frame[y1:y2, x1:x2]
#                 cara_recortada = cv2.resize(cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)

#                 # Comparar con imágenes almacenadas
#                 user_images_directory = os.path.join(settings.MEDIA_ROOT, 'user_images')
#                 similitud_minima = 0.6  # Umbral de similitud para autenticación

#                 # Recorre las imágenes almacenadas y compara
#                 for image_filename in os.listdir(user_images_directory):
#                     image_path = os.path.join(user_images_directory, image_filename)
#                     stored_image = cv2.imread(image_path)

#                     # Procesar la imagen almacenada para comparar
#                     stored_cara = detector.detect_faces(stored_image)
#                     if stored_cara:
#                         x1, y1, ancho, alto = stored_cara[0]['box']
#                         x2, y2 = x1 + ancho, y1 + alto
#                         stored_cara_recortada = stored_image[y1:y2, x1:x2]
#                         stored_cara_recortada = cv2.resize(stored_cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)

#                         # Comparar las características de las caras
#                         similarity_score = compare_faces(cara_recortada, stored_cara_recortada)
#                         if similarity_score >= similitud_minima:
#                             # Autenticación exitosa
#                             return render(request, 'app_biometricos/inicio_sesion_exitoso.html')

#             # Autenticación fallida
#             return render(request, 'app_biometricos/inicio_sesion_fallido.html')

#     return render(request, 'app_biometricos/iniciar_sesion.html')

# def compare_faces(face1, face2):
#     # Implementa la comparación de características faciales
#     # Puedes usar algoritmos como el reconocimiento facial basado en distancia euclidiana o similares
#     # Devuelve una puntuación de similitud entre 0 y 1
#     return 0.75  # Ejemplo: 0.75 significa un 75% de similitud

#aqui esta para poder hacer el login facial 

from django.shortcuts import render
import os

def verificacion_login(request):
    if request.method == 'POST':
        log_usuario = request.POST.get('verificacion_usuario')
        log_contra = request.POST.get('verificacion_contra')

        lista_archivos = os.listdir()   # Lista de archivos en el directorio actual

        if log_usuario in lista_archivos:
            with open(log_usuario, "r") as archivo2:
                verificacion = archivo2.read().splitlines()
                if log_contra in verificacion:
                    mensaje = "Inicio de sesión exitoso"
                    return render(request, 'app_biometricos/inicio_sesion_exitoso.html', {'mensaje': mensaje})
                else:
                    mensaje = "Contraseña incorrecta, ingrese de nuevo"
                    return render(request, 'app_biometricos/verificacion_fallida.html', {'mensaje': mensaje})
        else:
            mensaje = "Usuario no encontrado"
            return render(request, 'app_biometricos/verificacion_fallida.html', {'mensaje': mensaje})

    return render(request, 'app_biometricos/verificacion_login.html')



import os
import cv2
from django.shortcuts import render, redirect
from django.conf import settings
from mtcnn.mtcnn import MTCNN

def iniciar_sesion(request):
    if request.method == 'POST':
        usuario_img = request.POST.get('usuario_img')
        imagen_data = request.POST.get('imagen_data')
        
        # Tomar la foto y procesarla
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            detector = MTCNN()
            caras = detector.detect_faces(frame)
            if caras:
                x1, y1, ancho, alto = caras[0]['box']
                x2, y2 = x1 + ancho, y1 + alto
                cara_recortada = frame[y1:y2, x1:x2]
                cara_recortada = cv2.resize(cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)

                # Comparar con imágenes almacenadas
                user_images_directory = os.path.join(settings.MEDIA_ROOT, 'user_images')
                similarity_score_threshold = 0.99  # Umbral de similitud para autenticación

                for image_filename in os.listdir(user_images_directory):
                    image_path = os.path.join(user_images_directory, image_filename)
                    stored_image = cv2.imread(image_path)

                    stored_caras = detector.detect_faces(stored_image)
                    if stored_caras:
                        x1, y1, ancho, alto = stored_caras[0]['box']
                        x2, y2 = x1 + ancho, y1 + alto
                        stored_cara_recortada = stored_image[y1:y2, x1:x2]
                        stored_cara_recortada = cv2.resize(stored_cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)

                        similarity_score = compare_faces(cara_recortada, stored_cara_recortada)
                        if similarity_score >= similarity_score_threshold:
                            request.session['authenticated_user'] = usuario_img
                            return redirect('perfil')  # Redirigir al perfil

    return render(request, 'app_biometricos/iniciar_sesion.html')

def perfil(request):
    authenticated_user = request.session.get('authenticated_user')
    if authenticated_user:
        return render(request, 'app_biometricos/perfil.html', {'usuario': authenticated_user})
    else:
        return redirect('iniciar_sesion')

def compare_faces(face1, face2):
    # Implementa la comparación de características faciales
    # Devuelve una puntuación de similitud entre 0 y 1
    return 0.99  # Ejemplo: 0.75 significa un 75% de similitu

#aqui empieza otro codigo 

import os
import cv2
import base64
from django.shortcuts import render, redirect
from django.conf import settings
from mtcnn.mtcnn import MTCNN

def registrar_usuario(request):
    if request.method == 'POST':
        usuario_img = request.POST.get('usuario_img')
        imagen_data = request.POST.get('imagen_data')

        image_data = imagen_data.replace("data:image/jpeg;base64,", "")
        image_data = image_data.encode()
        image_filename = f'{usuario_img}.jpg'
        user_images_directory = os.path.join(settings.MEDIA_ROOT, 'user_images')
        image_path = os.path.join(user_images_directory, image_filename)
        
        with open(image_path, "wb") as f:
            f.write(base64.decodebytes(image_data))

        return redirect('iniciar_sesion')  # Redirigir al inicio de sesión

    return render(request, 'app_biometricos/registrar_usuario.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        usuario_img = request.POST.get('usuario_img')
        imagen_data = request.POST.get('imagen_data')
        
        # Tomar la foto y procesarla
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            detector = MTCNN()
            caras = detector.detect_faces(frame)
            if caras:
                x1, y1, ancho, alto = caras[0]['box']
                x2, y2 = x1 + ancho, y1 + alto
                cara_recortada = frame[y1:y2, x1:x2]
                cara_recortada = cv2.resize(cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)

                # Comparar con la imagen almacenada del usuario
                user_images_directory = os.path.join(settings.MEDIA_ROOT, 'user_images')
                similarity_score_threshold = 0.99  # Umbral de similitud para autenticación
                image_filename = f'{usuario_img}.jpg'
                image_path = os.path.join(user_images_directory, image_filename)
                
                stored_image = cv2.imread(image_path)
                stored_caras = detector.detect_faces(stored_image)
                
                if stored_caras:
                    x1, y1, ancho, alto = stored_caras[0]['box']
                    x2, y2 = x1 + ancho, y1 + alto
                    stored_cara_recortada = stored_image[y1:y2, x1:x2]
                    stored_cara_recortada = cv2.resize(stored_cara_recortada, (150, 200), interpolation=cv2.INTER_CUBIC)

                    similarity_score = compare_faces(cara_recortada, stored_cara_recortada)
                    if similarity_score >= similarity_score_threshold and image_filename.split('.')[0] == usuario_img:
                        request.session['authenticated_user'] = usuario_img
                        return redirect('perfil')  # Redirigir al perfil
                    else:
                        return render(request, 'app_biometricos/iniciar_sesion.html', {'error': 'Inicio de sesión fallido'})

    return render(request, 'app_biometricos/iniciar_sesion.html')

def perfil(request):
    authenticated_user = request.session.get('authenticated_user')
    if authenticated_user:
        return render(request, 'app_biometricos/perfil.html', {'usuario': authenticated_user})
    else:
        return redirect('iniciar_sesion')

def compare_faces(face1, face2):
    # Implementar la comparación de características faciales
    # Devolver una puntuación de similitud entre 0 y 1
    return 0.99  # Ejemplo: 0.99 significa un 99% de similitud