from django.shortcuts import render

# Create your views here.
import pandas as pd
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
import os
from django.http import HttpResponse

def handle_uploaded_file(f):
    file_path = 'uploaded_file'
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def generate_summary_report(uploaded_file):
    file_name = uploaded_file.name  # Get the uploaded file name
    extension = os.path.splitext(file_name)[1]  
 
    if extension == '.csv':
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    elif extension == '.xlsx':
        df = pd.read_excel(uploaded_file)  
    else:
        raise ValueError('Unsupported file format')

    summary = df.describe().to_string() 
    return summary



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']  
            summary_report = generate_summary_report(uploaded_file) 

            subject = f'Python Assignment - {request.user.username}' 
            message = f'Summary Report:\n\n{summary_report}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['tech@themedius.ai'])

            return render(request, 'success.html', {'summary': summary_report})
    else:
        form = UploadFileForm()
    
    return render(request, 'upload.html', {'form': form})

