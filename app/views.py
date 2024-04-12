from django.http import HttpResponse
from django.shortcuts import render
from app.forms import UploadFileForm


def file_upload(request) -> HttpResponse:
    lines: list = []
    if request.method == 'POST':
        form = UploadFileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            for line in request.FILES['arquivo']:
                lines.append(line.decode('utf-8').strip())
                print(line.decode('utf-8').strip())

            return render(request=request, template_name='upload_complete.html', context={'lines': lines})
    else:
        form = UploadFileForm()
    return render(request=request, template_name='upload.html', context={'form': form})
