import requests
import cv2
import numpy as np

def convert(lat,lon,level):
	row = ((90 - lat) * (2 ** level)) // 288
	col = ((180 + lon) * (2 ** level)) // 288
	return int(row),int(col)

def get(data,level,lat,lon,banda):
	row, col = convert(float(lat),float(lon),int(level))
	url = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{}/default/{}/250m/{}/{}/{}.jpg".format(banda,data,int(level),row,col)
	print(url)
	# Conversão do quadrante adquirido para o formato opencv
	req =requests.get(url).content
	arr = np.asarray(bytearray(req), dtype=np.uint8)
	img = cv2.imdecode(arr, -1)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	return img
