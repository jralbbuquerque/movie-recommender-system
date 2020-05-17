# Libraries usadas
from tqdm import tqdm
import time
import datetime as dt
import os.path
import requests
import sys
import zipfile

# Inicializa o timer de execução
print("Iniciado em: {}\n".format(dt.datetime.now()))
start_time = time.time()

# Diretórios
PATH_DATASRC = './datasrc/'
PATH_DATASET = './datasets/'

# Para o nome do arquivo e a url foram criados dois vetores, dessa forma, 
# é possível baixar ambos os arquivos com a lógica implementada
FILE_NAME = ['ml-latest-small.zip', 
						'ml-25mb.zip']

url = ['http://files.grouplens.org/datasets/movielens/ml-25m.zip',
			'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip']

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

def unzip_datasets(PATH_DATASRC, FILE_NAME):
	with zipfile.ZipFile(PATH_DATASRC + FILE_NAME, 'r') as zip_ref:
		zip_ref.extractall(PATH_DATASET)

######################################################################################################
### Main
print('Baixando os datasets...')

for i in range(0, len(url)):
	if os.path.isfile(PATH_DATASRC + FILE_NAME[i]):
		print('  + O arquivo {} encontrado. Download ignorado.'.format(FILE_NAME))
	else:
		get_dataset(url[i], PATH_DATASRC, FILE_NAME[i])

	unzip_datasets(PATH_DATASRC, FILE_NAME[i])
	print('  + O arquivo {} descompatado e movido para o diretório {}.\n'.format(FILE_NAME[i], PATH_DATASET))

# Print out elapsed time
elapsed_time = (time.time() - start_time) / 60
print("Finalizado em: {}. ".format(dt.datetime.now()), end="")
print("Tempo de execução: {0:0.4f} minutes.".format(elapsed_time))
