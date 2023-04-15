from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
import numpy as np
from PIL import Image

# Загрузка модели
model = tf.keras.models.load_model('./my_model.h5')

# Создание классов дорожных знаков
classes = {1: 'Ограничение скорости (20км/ч)',
           2: 'Ограничение скорости (30км/ч)',
           3: 'Ограничение скорости (50км/ч)',
           4: 'Ограничение скорости (60км/ч)',
           5: 'Ограничение скорости (70км/ч)',
           6: 'Ограничение скорости (80км/ч)',
           7: 'Ограничение скорости (80км/ч)',
           8: 'Ограничение скорости (100км/ч)',
           9: 'Ограничение скорости (120км/ч)',
           }

# Функция для обработки POST-запроса на загрузку изображения
def upload_and_classify(request):
    if request.method == 'POST' and request.FILES['image']:
        # Сохранение изображения на сервере
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)

        # Классификация изображения
        img = Image.open(str(settings.BASE_DIR) + uploaded_file_url)
        img = img.resize((30, 30))
        img = np.expand_dims(img, axis=0)
        img = np.array(img)
        predict_classes = model.predict([img])[0]
        pred = np.argmax(predict_classes)
        sign = classes[pred + 1]

        # Вывод результатов на страницу
        return render(request, 'upload.html', {'uploaded_file_url': uploaded_file_url, 'sign': sign})

    # Вывод страницы загрузки изображения
    return render(request, 'upload.html')

