import re
import io
import sys
import os

regexp_lines = {
    "NOMBRE_SUJETO_ASISTENCIA" : [r'Nombre:[\s]*[Dña\.|D\.|Sra.|Sr.]?(([\s]*[A-Z][a-z\.-]+)+)',
                                  r'Apellidos:[\s]*[Dña\.|D\.|Sra.|Sr.]?(([\s]*[A-Z][a-z\.-]+)+)' ],
    "EDAD_SUJETO_ASISTENCIA": [r'Edad:[\s]*(\d{2}(\s+[años|dias])?)'],
    "SEXO_SUJETO_ASISTENCIA": [r'Sexo:[\s]*([[H|h]ombre|[M|m]ujer|[V|v]aron|M|m|H|h|V|v])'],
    "FAMILIARES_SUJETO_ASISTENCIA": [],
    "NOMBRE_PERSONAL_SANITARIO": [r'Médico:[\s]*[Dra\.|Dr\.]?(([\s]*[A-Z][a-z\.-]+)+)' ],
    "FECHAS": [r'(\d{1,2}/\d{1,2}/\d{2,4})', 
                r'((([L|l]unes|[M|m]artes|[M|m]iercoles|[J|j]ueves|[V|v]iernes|[S|s]abado|[D|d]omingo)\s+)?(\d{1,2}\s*(de)?\s+)?([E|e]nero|[F|f]ebrero|[M|m]arzo|[A|a]bril|[M|m]ayo|[J|j]unio|[J|j]ulio|[A|a]gosto|[S|s]eptiembre|[O|o]ctubre|[N|n]oviembre|[D|d]iciembre)\s+(de|del)?\s*\d{2,4})' ],
    "PROFESIÓN": [],
    "HOSPITAL": [r'(Hospital(\s+[[A-Z][a-z]+|de|del|la|las|el|los])+)'],

    "CORREO_ELECTRÓNICO": [r'([a-zA-Z0-9_+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+)']
}

def leer_por_lineas(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return [x[:-2] for x in fichero.readlines()]
    
def leer_completo(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return fichero.read()
		
def match_to_brat(lista, ruta_salida):
    T = 1
    with open(ruta_salida,'w') as fichero:
        for el in lista:
            fichero.write("T%s\t%s\t%s\t%s\t%s\n"%(T,el['tag'],el['match'].start(),el['match'].end()-1,el['match'].group(1)))
            T+=1
			

def analiza_fichero(ruta, completo = False):
	if completo:
		texto = leer_completo(ruta)
	else:
		texto = leer_por_lineas(ruta)
	resultados = []
	for tag in regexp_lines:
		for exp in range(len(regexp_lines[tag])):
			if completo:
				find = re.search(regexp_lines[tag][exp],texto)
				if find is not None:
					resultados.append({'tag':tag,'match':find})
			else:
				for line in texto:
					find = re.search(regexp_lines[tag][exp],line)
					if find is not None:
						resultados.append({'tag':tag,'match':find})
	return resultados

def main():					
	if len(sys.argv)!=3:
		print("USO: %s ruta/fichero/o/directorio/a/analizar ruta/salida/brat")
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
		resultados = analiza_fichero(file, completo=True)
		match_to_brat(resultados,os.path.join(sys.argv[2], os.path.basename(file).split('.')[0]+'.ann'))

main()