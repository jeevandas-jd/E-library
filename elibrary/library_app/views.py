from django.shortcuts import render,get_object_or_404
from google.cloud import storage
import datetime
from django.http import HttpResponse
from .models import StudyMaterial
from elibrary import settings
import logging
from .forms import FileUploadForm
from .utils import upload_data_to_gcs
from .utils import upload_data_to_gcs, update_file_in_gcs, download_data_from_gcs

import os

def study_materials(request):
    materials = StudyMaterial.objects.all().order_by('semester', 'subject')
    return render(request, 'materials.html', {'materials': materials})

from django.shortcuts import render
from .models import StudyMaterial

def home(request):
    subjects = StudyMaterial.SUBJECTS  # Get list of subjects from choices
    semesters = StudyMaterial.SEMESTERS  # Get list of semesters from choices

    # Get selected filters from the GET parameters (defaults to None)
    selected_subject = request.GET.get('subject')
    selected_semester = request.GET.get('semester')

    # Filter materials based on selected options
    materials = StudyMaterial.objects.all()
    if selected_subject:
        materials = materials.filter(subject=selected_subject)
    if selected_semester:
        materials = materials.filter(semester=selected_semester)

    context = {
        'materials': materials,
        'subjects': subjects,
        'semesters': semesters,
        'selected_subject': selected_subject,
        'selected_semester': selected_semester,
    }
    return render(request, 'home.html', context)


def study_materials(request):
    # Logging setup for debugging Google Cloud Storage integration
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging.debug(f"Default file storage: {settings.DEFAULT_FILE_STORAGE}")
        logging.debug(f"Bucket name: {settings.GS_BUCKET_NAME}")

        # Additional debug statement to confirm files are accessible
        materials = StudyMaterial.objects.all()
        logging.debug(f"Total materials retrieved: {materials.count()}")

    except Exception as e:
        logging.error("Error accessing study materials", exc_info=True)

    # Render the view with materials, logging as necessary
    return render(request, 'materials.html', {'materials': materials})

def download_file(request, material_id):
    material = get_object_or_404(StudyMaterial, pk=material_id)
    bucket_name = 'jdkjdk123'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(material.file.name)

    print(f"blob name is :{blob}")

    print(f"download action for {material.title} is invoked")

    # Generate a signed URL for temporary access
    url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))

    print(f"the url is {url}")

    return HttpResponse(f"<a href='{url}'>Download {material.title}</a>")



def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            destination_name = form.cleaned_data['destination_name']
            file_path = f"/tmp/{file.name}"

            # Save file temporarily to upload it to GCS
            with open(file_path, 'wb+') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            # Upload to GCS
            bucket_name = "jdkjdk123"  # Your bucket name
            if upload_data_to_gcs(bucket_name, file_path, destination_name):
                message = "File uploaded successfully!"
            else:
                message = "Failed to upload the file."

            # Clean up the temp file
            os.remove(file_path)

            return render(request, 'upload_result.html', {'message': message})
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})

def update_file(request):
    """Update file in Google Cloud Storage."""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            destination_name = form.cleaned_data['destination_name']
            file_path = f"/tmp/{file.name}"

            with open(file_path, 'wb+') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            if update_file_in_gcs("jdkjdk123", file_path, destination_name):
                message = "File updated successfully!"
            else:
                message = "Failed to update the file."

            os.remove(file_path)
            return render(request, 'upload_result.html', {'message': message})
    else:
        form = FileUploadForm()

    return render(request, 'update_file.html', {'form': form})



def download_file(request, file_name):
    """Download file from Google Cloud Storage."""
    download_path = f"/tmp/{file_name}"
    source_name = f"materials/{file_name}"  # Adjust path as needed in GCS

    if download_data_from_gcs("jdkjdk123", source_name, download_path):
        with open(download_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            os.remove(download_path)
            return response
    else:
        return HttpResponse("File not found.", status=404)