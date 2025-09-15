*** Skin Disease Detection Web App ***
A Django-based web application that allows users to upload skin images and get predictions of skin diseases using a pre-trained deep learning model. The app also provides precautions and advice for each detected disease.

*** Features ***
▶ Image Upload: Easily upload skin images for analysis.
▶ Disease Prediction: Predicts a variety of skin conditions, including:
▶ Actinic keratosis
▶ Atopic Dermatitis
▶ Benign keratosis
▶ Dermatofibroma
▶ Melanocytic nevus
▶ Melanoma
▶ Squamous cell carcinoma
▶ Tinea Ringworm Candidiasis
▶ Vascular lesion
▶ Preventative Advice: Displays precautionary advice for each predicted disease.
▶ Prediction Storage: Stores all predictions in a database for easy retrieval.

*** 💻 Requirements ***
▶ Python 3.10
▶ Django 5.2+
▶ TensorFlow / Keras
▶ Other Python packages: numpy, pillow

*** ⚙️ Installation & Setup ***
Follow these steps to get the application running on your local machine.

*** 1. Clone the repository ***
Bash

git clone <REPO_URL>
cd skin_project
*** 2. Create and activate a virtual environment ***
Bash

python -m venv venv310
# Windows:

Bash

venv310\Scripts\activate
# macOS/Linux:

Bash

source venv310/bin/activate
*** 3. Install dependencies ***
Install the required Python packages.

Bash

# Recommended: Install from requirements file
pip install -r requirements.txt

# Alternatively, install manually
pip install django tensorflow numpy pillow
Note: If you encounter TensorFlow errors with Python 3.10, try installing a compatible version like pip install tensorflow==2.13.0.

*** 4. Place the model file ***
Copy the pre-trained deep learning model file (skin_disease_model.h5) to the project's root folder, in the same directory as manage.py.

*** 5. Apply database migrations ***
Bash

python manage.py makemigrations
python manage.py migrate
*** 6. Run the development server ***
Bash

python manage.py runserver
*** 🚀 Usage ***
Open a web browser and navigate to http://127.0.0.1:8000/. On the homepage, use the form to upload a skin image and click "Predict". The app will display the predicted skin disease and relevant precautionary advice.

*** 📁 Project Structure ***
skin_project/
├── manage.py
├── skin_disease_model.h5    # Pre-trained deep learning model
├── db.sqlite3
├── media/                   # Uploaded images are stored here
├── static/                  # CSS, JS, and other static files
├── skin_project/            # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── predictor/               # Django application
    ├── models.py            # Database models
    ├── views.py             # Logic for handling requests
    ├── forms.py             # Web forms
    ├── urls.py              # App-specific URL configurations
    └── templates/
        └── predictor/
            └── predict.html # HTML template for the prediction form

*** ⚠️ Important Notes ***
▶ Ensure the model file (skin_disease_model.h5) is in the correct directory as specified in settings.py.
▶ Verify that MEDIA_URL = '/media/' and MEDIA_ROOT = os.path.join(BASE_DIR, 'media') are correctly configured in settings.py.
▶ The media/ folder must exist to store uploaded images.
▶ The prediction form in predict.html must include enctype="multipart/form-data" to handle file uploads: <form method="POST" enctype="multipart/form-data">.
▶ To clear past predictions, you can delete records directly from the SkinPrediction table in db.sqlite3.