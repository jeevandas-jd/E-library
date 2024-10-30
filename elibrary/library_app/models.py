from django.db import models
class StudyMaterial(models.Model):
    SEMESTERS = [(i, f'Semester {i}') for i in range(1, 11)]
    SUBJECTS = [
        ('Physics', 'Physics'),
        ('Maths', 'Maths'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=50, choices=SUBJECTS)
    semester = models.IntegerField(choices=SEMESTERS)
    #file = models.FileField(upload_to='study_materials2/')
    file = models.FileField(upload_to='materials2/')
    

    def __str__(self):
        return f"{self.title} - {self.subject} (Semester {self.semester})"
"""jeevandas@precise-antenna-439718-f3.iam.gserviceaccount.com"""