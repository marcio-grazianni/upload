import os
import pandas as pd

from io import StringIO
from django.shortcuts import render
from app.forms import UploadFileForm


def principal(request):
    return render(request=request, template_name='principal.html')


def upload(request):
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
            print("-" * 90)

            return render(request=request, template_name='upload_complete.html', context={'lines': lines})
    else:
        formulario = UploadFileForm()
    return render(request=request, template_name='upload.html', context={'form': formulario})


def upload_csv(request):
    lines = []
    info = {}
    if request.method == 'POST':
        formulario = UploadFileForm(data=request.POST, files=request.FILES)
        arquivo = request.FILES['arquivo']

        # Variáveis para colocar no dicionário "info"
        nome_completo_arquivo = arquivo.name
        nome_arquivo, extensao_arquivo = os.path.splitext(nome_completo_arquivo)
        info['nome_completo_arquivo'] = nome_completo_arquivo
        info['nome_arquivo'] = nome_arquivo
        info['extensao_arquivo'] = extensao_arquivo.replace(".", "")
        print("-" * 90)
        for key, value in info.items():
            print(f'{key}: {value}')
        if info['extensao_arquivo'] == "csv":
            print("Extensão csv detectada.")
        print("-" * 90)
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
                            # print(line)
                    else:
                        lines.append(line)
                        # print(line)
            if info['extensao_arquivo'] == "csv":
                data_frame = processa_data_frame(request, lines, info['nome_arquivo'])
            return render(request=request, template_name='upload_csv_complete.html', context={'lines': lines, 'info': info, 'data_frame': data_frame})
    else:
        formulario = UploadFileForm()
    return render(request=request, template_name='upload_csv.html', context={'form': formulario, 'titulo':'Upload CSV'})


def processa_data_frame(request, linhas, nome_arquivo):
    data_string = "\n".join(linhas)
    data_io = StringIO(data_string)
    delimiter = "," if "nome_arquivo" == "nubank" else ";"
    df = pd.read_csv(data_io, delimiter=delimiter).to_dict(orient="records")
    print(f"nome_arquivo: [{nome_arquivo}]")
    print(f"delimiter: [{delimiter}]")
    for line in df:
        print(line)
    print("-" * 90)
    return df
