import cv2
import requests
import numpy as np
from datetime import date, timedelta
import time
import streamlit as st


side = st.sidebar



# Função para converter a posição de Latitude e Longitude para a escala
def convert(lat,lon,level):
	row = ((90 - lat) * (2 ** level)) // 288
	col = ((180 + lon) * (2 ** level)) // 288
	return int(row),int(col)


# Seleciona a banda para aquisição de imagem
bandas = [ 'MODIS_Aqua_CorrectedReflectance_TrueColor', 'MODIS_Terra_CorrectedReflectance_TrueColor', \
	'MODIS_Terra_SurfaceReflectance_Bands121', 'MODIS_Aqua_SurfaceReflectance_Bands121',\
	'MODIS_Terra_CorrectedReflectance_Bands721', 'MODIS_Aqua_CorrectedReflectance_Bands721',\
	'MODIS_Terra_L3_SurfaceReflectance_Bands121_8Day', 'MODIS_Aqua_L3_SurfaceReflectance_Bands121_8Day']

t = st.empty()
banda = side.selectbox("Selecione Uma opção", options = bandas)


latitude = side.text_input("Latitude")
longitude = side.text_input("Longitude")
level = side.text_input("Zoom level (0-8)")
dias = side.text_input("Days ago: (min 0)")
enviar = side.button("Send")

if latitude == "":
	latitude = 0
if longitude == "":
	longitude = 0
if level == "":
	level =0 
if dias == "":
	dias = 0
if enviar and int(level) >=0 and int(level) <=8:
	# Configuração dos parâmetros para requisição da API
	data = date.today()  - timedelta(days=int(dias))
	

	row, col = convert(float(latitude),float(longitude),int(level))
	url = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{}/default/{}/250m/{}/{}/{}.jpg".format(banda,data,int(level),row,col)
	print(url)
	# Conversão do quadrante adquirido para o formato opencv
	req =requests.get(url).content
	arr = np.asarray(bytearray(req), dtype=np.uint8)
	img = cv2.imdecode(arr, -1)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	st.image(img)
	# Divide imagem em canais de cor e utiliza apenas o canal VERMELHO para detecção de nuvem
	# Essa decisão deriva da baixa presença de vermelho , para reduzir falsos positivos.
	blue,green, red = cv2.split(img)

	# Segmenta pixels com intensidade entre 190 e 255 e cria a máscara
	_, mask = cv2.threshold(red, 160, 255, cv2.THRESH_BINARY)

	# Normaliza máscara para cálculo de área coberta pela máscara
	mask_norm = mask / 255.

	# calcula o total de pixels brancos na máscara (onde foi detectada nuvem)
	total = np.sum(mask_norm)

	# Calcula o percentual da máscara em relação ao total possível

	# Multiplicação da altura x largura da imagem é a maior dimensão de cobertura possível
	total_possivel = img.shape[0] * img.shape[1]

	# calcula o percentual do total de cobertura detectado com o total posśivel
	percentual =  (total / total_possivel) * 100.


	t.title("Cloud Detected: {}%".format(round(percentual,2)))

	# Converte máscara de 1 canal para 3 canais de cor para poder concatenar com o frame
	mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
	#img_final = cv2.hconcat([img,mask_rgb])
	st.image(mask_rgb)



