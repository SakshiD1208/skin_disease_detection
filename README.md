# 🩺 Skin Disease Detection Web App  

A **Django-based web application** that allows users to upload skin images and get predictions of skin diseases using a **pre-trained deep learning model**. The app also provides **precautions and advice** for each detected disease.  

---

## ✨ Features  
- 📤 **Image Upload**: Upload skin images for analysis.  
- 🔍 **Disease Prediction**: Supports multiple conditions, including:  
  - Actinic keratosis  
  - Atopic Dermatitis  
  - Benign keratosis  
  - Dermatofibroma  
  - Melanocytic nevus  
  - Melanoma  
  - Squamous cell carcinoma  
  - Tinea / Ringworm / Candidiasis  
  - Vascular lesion  
- 🛡 **Preventative Advice**: Displays precautionary advice for each predicted disease.  
- 💾 **Prediction Storage**: All predictions are saved in a database for later retrieval.  

---

## 💻 Requirements  
- Python **3.10**  
- Django **5.2+**  
- TensorFlow / Keras  
- Other Python packages: `numpy`, `pillow`  

---

## ⚙️ Installation & Setup  

Follow these steps to get the application running locally:  

### 1️⃣ Clone the repository  
```bash
git clone <REPO_URL>
cd skin_disease_detection

2️⃣ Create and activate a virtual environment
python -m venv venv310

Windows:

venv310\Scripts\activate


macOS/Linux:

source venv310/bin/activate

3️⃣ Install dependencies

From requirements.txt (recommended):

pip install -r requirements.txt


Or manually:

pip install django tensorflow numpy pillow


⚠️ Note: If you face TensorFlow issues with Python 3.10, install a compatible version:

pip install tensorflow==2.13.0

4️⃣ Place the model file

Copy the pre-trained model file skin_disease_model.h5 into the project’s root directory (same location as manage.py).

5️⃣ Apply database migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Run the development server
python manage.py runserver

🚀 Usage

Open your browser and go to: http://127.0.0.1:8000/

Upload a skin image using the form.

Click Predict to view:

The predicted skin disease

Relevant precautionary advice

📁 Project Structure

skin_disease_detection/
├── manage.py
├── skin_disease_model.h5      # Pre-trained model
├── db.sqlite3
├── media/                     # Uploaded images
├── static/                    # CSS, JS, assets
├── skin_project/              # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── predictor/                 # Django app
    ├── models.py              # Database models
    ├── views.py               # Request handling
    ├── forms.py               # Forms
    ├── urls.py                # App URLs
    └── templates/
        └── predictor/
            └── predict.html   # Upload & prediction page
⚠️ Important Notes

✅ Ensure skin_disease_model.h5 is in the correct directory.

✅ In settings.py, check:

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


✅ Ensure media/ folder exists (for uploaded files).

✅ Prediction form (predict.html) must use:

<form method="POST" enctype="multipart/form-data">


🗑 To clear old predictions, delete records from the SkinPrediction table in db.sqlite3.


ScreenShot

<img width="1798" height="960" alt="Screenshot 2025-09-19 003206" src="https://github.com/user-attachments/assets/19cb8b0b-a6c9-4232-abd9-d9a86ca25ef5" />

