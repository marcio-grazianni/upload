import os
import pandas as pd

from io import StringIO
from django.shortcuts import render
from app.forms import UploadFileForm
from templates.src import funcoes as fn


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
    csv_lines = []
    info = {}
    if request.method == 'POST':
        formulario = UploadFileForm(data=request.POST, files=request.FILES)
        arquivo = request.FILES['arquivo']

        # Variáveis para colocar no dicionário "info"
        nome_completo_arquivo = arquivo.name
        nome_arquivo, extensao_arquivo = os.path.splitext(p=nome_completo_arquivo)
        info['nome_completo_arquivo'] = nome_completo_arquivo
        info['nome_arquivo'] = nome_arquivo
        info['extensao_arquivo'] = extensao_arquivo.replace(".", "")
        # print("-" * 90)
        # for key, value in info.items():
        #     print(f'{key}: {value}')
        # if info['extensao_arquivo'] == "csv":
        #     print("Extensão csv detectada.")
        # print("-" * 90)
        if formulario.is_valid():
            start_csv_data = False
            for line in arquivo:
                line = line.decode('utf-8').strip()
                if line:
                    if info['extensao_arquivo'] == "csv":
                        if not start_csv_data and "Data" in line:
                            start_csv_data = True
                        if start_csv_data:
                            csv_lines.append(line)
                            # print(line)
                    else:
                        csv_lines.append(line)
                        # print(line)
            if info['extensao_arquivo'] == "csv":
                df_dict, csv_type = create_data_frame(request=request, csv_lines=csv_lines, file_name=info['nome_arquivo'])
                info['df_dict'] = df_dict
                info['csv_type'] = csv_type
            return render(request=request, template_name='upload_csv_complete.html', context={'lines': csv_lines, 'info': info})
    else:
        formulario = UploadFileForm()
    return render(request=request, template_name='upload_csv.html', context={'form': formulario, 'titulo':'Upload CSV'})


def create_data_frame(request, csv_lines, file_name):
    csv_type = fn.detect_csv_type(csv_lines=csv_lines)
    csv_delimiter = fn.detect_csv_delimiter(csv_type=csv_type)

    data_string = "\n".join(csv_lines)
    data_io = StringIO(initial_value=data_string)

    df = pd.read_csv(filepath_or_buffer=data_io, delimiter=csv_delimiter)
    if csv_type == fn.CSVType.INTER:
        df['Valor'] = df['Valor'].str.replace(pat=',', repl='.').astype(dtype=float)
    df_filtered = df[df['Valor'] < 0]
    df_filtered = df_filtered[~df['Descrição'].str.contains(pat="MARCIO GRAZIANNI")]
    df_dict = df_filtered.to_dict(orient="records")

    print("-" * 90)
    print(f"file_name: [{file_name}]")
    print(f"csv_type: [{csv_type}]")
    print(f"delimiter: [{csv_delimiter}]")

    print("-" * 90)
    print("colunas:")
    for coluna in df.columns:
        print(coluna)

    print("-" * 90)
    print("linhas:")
    for line in df_dict:
        print(line)

    print("-" * 90)
    print("total df_filtered:")
    print(len(df_filtered))

    print("-" * 90)
    print("total df_dict:")
    print(len(df_dict))
    print("-" * 90)

    return df_dict, csv_type
