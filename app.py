import cv2
from datetime import date, timedelta
import time
import streamlit as st
from utils import *

# Cria objeto streamlit para menu lateral
side = st.sidebar




# Seleciona a banda para aquisição de imagem
bandas = [ 'MODIS_Aqua_CorrectedReflectance_TrueColor', 'MODIS_Terra_CorrectedReflectance_TrueColor', \
	'MODIS_Terra_SurfaceReflectance_Bands121', 'MODIS_Aqua_SurfaceReflectance_Bands121',\
	'MODIS_Terra_CorrectedReflectance_Bands721', 'MODIS_Aqua_CorrectedReflectance_Bands721',\
	'MODIS_Terra_L3_SurfaceReflectance_Bands121_8Day', 'MODIS_Aqua_L3_SurfaceReflectance_Bands121_8Day']

# Cria objeto streamlit vazio
t = st.empty()

# Objeto select box para seleção de banda
banda = side.selectbox("Selecione Uma opção", options = bandas)

# Objeto de entrada de texto para seleção de latitude
latitude = side.text_input("Latitude")

# Objeto de entrada de texto para seleção de longitude
longitude = side.text_input("Longitude")

# Objeto de entrada de texto para seleção de Level (zoom)
level = side.text_input("Zoom level (0-8)")

# Objeto de entrada de texto para seleção de dias passados
dias = side.text_input("Days ago: (min 0)")

# Objeto botão para envio de parâmetros
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
	
	# A função 'get' adquire as imagens da API da Nasa a partir dos parâmetros: data, level(zoom), latitude, longitude e banda.
	img = get(data,level,latitude,longitude,banda)
	
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


