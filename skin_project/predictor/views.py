from django.shortcuts import render
from django.views import View
from .forms import SkinPredictionForm
from .models import SkinPrediction
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO

import os

# Load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'skin_disease_model.h5')

try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Model not loaded. Check the model path. Error: {e}")
    model = None

# Disease precautions and class labels
disease_precautions = {
    'Actinic keratosis': "Avoid sun exposure, use sunscreen, keep the area clean, consult a dermatologist promptly.",
    'Atopic Dermatitis': "Moisturize regularly, avoid scratching, use mild soap, keep nails short, see dermatologist.",
    'Benign keratosis': "Keep the area clean, avoid irritation, monitor for changes, consult dermatologist if needed.",
    'Dermatofibroma': "Do not scratch or pick at the lesion, keep it clean, consult dermatologist if it grows or changes.",
    'Melanocytic nevus': "Monitor for color/size changes, protect from sun, consult dermatologist if any change occurs.",
    'Melanoma': "Seek immediate dermatology consultation, avoid sun exposure, do not scratch or self-treat.",
    'Squamous cell carcinoma': "Avoid sun exposure, keep area clean, seek dermatology advice promptly.",
    'Tinea Ringworm Candidiasis': "Keep affected area dry, avoid scratching, use antifungal powder/cream if available, see dermatologist.",
    'Vascular lesion': "Avoid trauma to the area, monitor for bleeding or growth, consult dermatologist if changes occur."
}

class_labels = list(disease_precautions.keys())

# View
class SkinDiseasePredictionView(View):
    template_name = 'predictor/predict.html'

    def get(self, request):
        form = SkinPredictionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SkinPredictionForm(request.POST, request.FILES)
        result = None
        suggestion = None
        error_msg = None

        if form.is_valid() and model:
            try:
                # Get uploaded file
                uploaded_file = request.FILES['image']

                # Convert to BytesIO
                img_bytes = BytesIO(uploaded_file.read())

                # Load image from BytesIO
                img = image.load_img(img_bytes, target_size=(224, 224))
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Predict
                pred = model.predict(img_array)
                pred_class_index = np.argmax(pred, axis=1)[0]
                pred_label = class_labels[pred_class_index]

                # Save to database
                pred_obj = form.save(commit=False)
                pred_obj.prediction = pred_label
                pred_obj.save()

                result = pred_label
                suggestion = disease_precautions.get(pred_label)

            except Exception as e:
                error_msg = f"Error during prediction: {str(e)}"
                print(error_msg)

        else:
            error_msg = "Form is not valid or model not loaded. Please select an image."

        return render(request, self.template_name, {
            'form': form,
            'result': result,
            'suggestion': suggestion,
            'error_msg': error_msg
        })
