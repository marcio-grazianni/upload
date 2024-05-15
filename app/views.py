import os

from django.http import HttpResponse
from django.shortcuts import render
from app.forms import UploadFileForm


def principal(request) -> HttpResponse:
    return render(request=request, template_name='principal.html')


def upload(request) -> HttpResponse:
    lines = []
    if request.method == 'POST':
        formulario = UploadFileForm(data=request.POST, files=request.FILES)
        arquivo = request.FILES['arquivo']

        if formulario.is_valid():
            for line in arquivo:
                line = line.decode('utf-8').strip()
                if line:
                    lines.append(line)
                    print(line)
            print("-" * 100)

            return render(request=request, template_name='upload_complete.html', context={'lines': lines})
    else:
        formulario = UploadFileForm()
    return render(request=request, template_name='upload.html', context={'form': formulario})


def upload_csv(request) -> HttpResponse:
    lines: list = []
    info: dict = {}
    if request.method == 'POST':
        formulario = UploadFileForm(data=request.POST, files=request.FILES)
        arquivo = request.FILES['arquivo']

        # Variáveis para colocar no dicionário "info"
        nome_completo_arquivo = arquivo.name
        nome_arquivo, extensao_arquivo = os.path.splitext(nome_completo_arquivo)
        info['nome_completo_arquivo'] = nome_completo_arquivo
        info['nome_arquivo'] = nome_arquivo
        info['extensao_arquivo'] = extensao_arquivo.replace(".", "")
        print("-" * 100)
        for key, value in info.items():
            print(f'{key}: {value}')
        if info['extensao_arquivo'] == "csv":
            print("Extensão csv detectada.")
        print("-" * 100)
        if formulario.is_valid():
            start_csv_data = False
            for line in arquivo:
                line = line.decode('utf-8').strip()
                if line:
                    if info['extensao_arquivo'] == "csv":
                        if not start_csv_data and "Data" in line:
                            start_csv_data = True
                        if start_csv_data:
                            lines.append(line)
                            print(line)
                    else:
                        lines.append(line)
                        print(line)
            print("-" * 100)

            return render(request=request, template_name='upload_csv_complete.html', context={'lines': lines, 'info': info})
    else:
        formulario = UploadFileForm()
    return render(request=request, template_name='upload_csv.html', context={'form': formulario})
