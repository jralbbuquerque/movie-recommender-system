# Libraries usadas
from tqdm import tqdm
import os.path
import requests
import sys
import zipfile

# Diretórios
PATH_DATASRC = './datasrc/'
PATH_DATASET = './datasets/'
FILE_NAME = 'ml-latest-small.zip'
url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

def get_dataset(url, PATH_DATASRC, FILE_NAME):
	# Realiza uma requisição HTTP
	r = requests.get(url, stream=True)

	# Testa se a requisição HTTP retorna o status 200 (OK). 
	# Caso contrário, o script para de rodar retornando uma mensagem de erro para o usuário.
	if r.status_code != 200:
		sys.exit("""Erro! HTTP Status Code {}.\nProblemas para encontrar a base de dados no endereço solicitado"""
		.format(r.status_code))

	# Tamanho do arquivo em Bytes
	total_size = int(r.headers.get('content-length', 0))

	# 1 Kibibyte
	block_size = 1024

	# Cria um objeto t para chamar os métodos da lib tqdm
	t = tqdm(total=total_size, unit='iB', unit_scale=True)

	with open(PATH_DATASRC + FILE_NAME, 'wb') as f:
		for data in r.iter_content(block_size):
			t.update(len(data))
			f.write(data)
	t.close()

def unzip_datasets():
	with zipfile.ZipFile(PATH_DATASRC + FILE_NAME, 'r') as zip_ref:
		zip_ref.extractall(PATH_DATASET)

if os.path.isfile(PATH_DATASRC + FILE_NAME):
	print('Arquivo {} encontrado. Download ignorado. \n'.format(FILE_NAME))
else:
	get_dataset(url, PATH_DATASRC, FILE_NAME)

unzip_datasets()