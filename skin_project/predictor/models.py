from django.db import models

class SkinPrediction(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_disease = models.CharField(max_length=100)
    precautions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.predicted_disease
