# Função para converter a posição de Latitude e Longitude para a escala
def convert(lat,lon,level):
	row = ((90 - lat) * (2 ** level)) // 288
	col = ((180 + lon) * (2 ** level)) // 288
	return int(row),int(col)

