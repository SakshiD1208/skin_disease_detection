from django.shortcuts import render
from django.views import View
from .forms import SkinPredictionForm
from .models import SkinPrediction
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from django.core.files.storage import FileSystemStorage

# Load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'skin_disease_model.h5')

try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Model not loaded. Error: {e}")
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

class_labels = list(disease_precautions.keys())  # must match model training order!

class SkinDiseasePredictionView(View):
    template_name = 'predictor/predict.html'

    def get(self, request):
        form = SkinPredictionForm()
        return render(request, self.template_name, {'form': form, 'chat': []})

    def post(self, request):
        form = SkinPredictionForm(request.POST, request.FILES)
        user_message = request.POST.get("user_message", "").strip()
        chat = []  # keep chat history for rendering
        uploaded_file_url = None
        result = None
        suggestion = None
        error_msg = None

        # If user typed something
        if user_message:
            chat.append({"sender": "user", "text": user_message})

            if user_message.lower() == "hi" or user_message.lower()=="hello" or user_message.lower()=="hey" or user_message.lower()=="hii" :
                bot_response = "👩‍⚕️ Hi! Please upload your skin image for analysis."
            else:
                bot_response = "👩‍⚕️ Sorry, I only understand 'HI'. Please upload an image."

            chat.append({"sender": "bot", "text": bot_response})

        # If image uploaded
        if form.is_valid() and model and 'image' in request.FILES:
            try:
                uploaded_file = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                uploaded_file_url = fs.url(filename)

                # Prediction
                img = image.load_img(fs.path(filename), target_size=(224, 224))
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                pred = model.predict(img_array)
                pred_class_index = np.argmax(pred, axis=1)[0]
                pred_label = class_labels[pred_class_index]

                # Save to DB
                pred_obj = form.save(commit=False)
                pred_obj.prediction = pred_label
                pred_obj.save()

                result = pred_label
                suggestion = disease_precautions.get(pred_label)

                # Add chat messages
                chat.append({"sender": "user", "text": "Uploaded Image", "image": uploaded_file_url})
                chat.append({"sender": "bot", "text": f"Prediction: {result}. Precautions: {suggestion}"})

            except Exception as e:
                error_msg = f"Error during prediction: {str(e)}"
                chat.append({"sender": "bot", "text": error_msg})

        return render(request, self.template_name, {
            'form': form,
            'chat': chat,
            'uploaded_file_url': uploaded_file_url
        })
