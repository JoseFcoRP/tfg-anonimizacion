import re
import io
import sys
import os

regexp_lines = {
    "NOMBRE_SUJETO_ASISTENCIA" : [r'Nombre:[\s]*[Dña\.|D\.|Sra.|Sr.]?[\s]*(([\s]*[A-Z][a-z]+|[\s]*[A-Z]\.)+)',
                                  r'Apellidos:[\s]*[Dña\.|D\.|Sra.|Sr.]?[\s]*(([\s]*[A-Z][a-z]+|[\s]*[A-Z]\.)+)' ],
    "EDAD_SUJETO_ASISTENCIA": [r'Edad:[\s]*(\d{2}(\s+[años|dias])?)'],
    "SEXO_SUJETO_ASISTENCIA": [r'Sexo:[\s]*([[H|h]ombre|[M|m]ujer|[V|v]aron|M|m|H|h|V|v])'],
    "FAMILIARES_SUJETO_ASISTENCIA": [],
    "NOMBRE_PERSONAL_SANITARIO": [r'Médico:[\s]*[Dra\.|Dr\.]?(([\s]*[A-Z][a-z\.-]+)+)' ],
    "FECHAS": [r'(\d{1,2}/\d{1,2}/\d{2,4})', 
                r'((([L|l]unes|[M|m]artes|[M|m]iercoles|[J|j]ueves|[V|v]iernes|[S|s]abado|[D|d]omingo)\s+)?(\d{1,2}\s*(de)?\s+)?([E|e]nero|[F|f]ebrero|[M|m]arzo|[A|a]bril|[M|m]ayo|[J|j]unio|[J|j]ulio|[A|a]gosto|[S|s]eptiembre|[O|o]ctubre|[N|n]oviembre|[D|d]iciembre)\s+(de|del)?\s*\d{2,4})' ],
    "PROFESIÓN": [],
    "HOSPITAL": [r'(Hospital(\s+[[A-Z][a-z]+|de|del|la|las|el|los])+)'],
	"ID_CENTRO_DE_SALUD": [],
	"INSTITUCION": [],
	"CALE": [],
	"TERRITORIO": [],
	"PAÍS": [],
	"NÚMERO_TELÉFONO": [],
	"NÚMERO_FAX": [],
    "CORREO_ELECTRÓNICO": [r'([a-zA-Z0-9_+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+)'],
	"ID_SUJETO_ASISTENCIA": [],
	"ID_CONTACTO_ASISTENCIAL": [],
	"ID_ASEGURAMIENTO": [],
	"ID_TITULACIÓN_PERSONAL_SANITARIO": [],
	"ID_EMPLEO_PERSONAL_SANITARIO": [],
	"IDENTIF_VEHÍCULOS_NRSERIE_PLACAS": [],
	"IDENTIF_DISPOSITIVOS_NRSERIE": [],
	"DIREC_PROT_INTERNET": [],
	"URL_WEB": [],
	"IDENTIF_BIOMÉTRICOS": [],
	"NUMERO_IDENTIF": [],
	"OTROS_SUJETO_ASISTENCIA":[]
}

def leer_por_lineas(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return [x.replace('\n','') for x in fichero.readlines()]
    
def leer_completo(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return fichero.read()
		
def match_to_brat(lista, ruta_salida):
    T = 1
    with open(ruta_salida,'w') as fichero:
        for el in lista:
            fichero.write("T%s\t%s\t%s\t%s\t%s\n"%(T,el['tag'],el['start'],el['end'],el['token']))
            T+=1
			

def analiza_fichero(ruta, completo = False):
	if completo:
		texto = leer_completo(ruta)
	else:
		texto = leer_por_lineas(ruta)
	resultados = []
	total_index = 0
	for tag in regexp_lines:
		for exp in range(len(regexp_lines[tag])):
			total_index = 0
			if completo:
				find = re.search(regexp_lines[tag][exp],texto)
				if find is not None:
					resultados.append({'tag':tag,'match':find})
			else:
				for line in texto:
					find = re.search(regexp_lines[tag][exp],line)
					if find is not None:
						resultados.append({'tag':tag, 'start':find.start(1)+total_index, 'end':find.end(1)+total_index, 'token':find.group(1)})
					total_index += len(line)+1
	print(resultados)
	return resultados

def main():					
	if len(sys.argv)!=3:
		print("USO: %s ruta/fichero/o/directorio/a/analizar ruta/salida/brat"%sys.argv[0])
		return 1
		
	if not os.path.isfile(sys.argv[1]):
		ficheros = []
		for root, dirs, files in os.walk(sys.argv[1]):
			for filename in files:
				ficheros.append(os.path.join(sys.argv[1], filename))
	else:
		ficheros = [sys.argv[1]]
	
	for file in ficheros:
		if '.txt' not in file:
			continue
		resultados = analiza_fichero(file, completo=False)
		match_to_brat(resultados,os.path.join(sys.argv[2], os.path.basename(file).split('.')[0]+'.ann'))

main()