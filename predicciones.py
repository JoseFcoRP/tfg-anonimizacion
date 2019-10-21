import spacy
import io
import os

def leer_completo(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return fichero.read()
		
def load_model(ruta):
    return spacy.load(ruta)
	
def predice(prdnlp, text):
    doc = prdnlp(text)
    tags = []
    for ent in doc.ents:
        tags.append({"text":ent.text, "start":ent.start_char, "end": ent.end_char, "tag":ent.label_ })
    return tags
	
def prediccion_a_brat(pred):
    token = 1
    lineas = []
    for tag in pred:
        texto = "T%d\t%s\t%d\t%d\t%s\n"%(token,tag['tag'],tag['start'],tag['end'],tag['text'])
        lineas.append(texto)
        token+=1
    return lineas
	
iteraciones = [5,10,15,20,25,30,35,40]
drops = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
ruta = ""
ruta_out = "salidas"

for it in iteraciones:
    for drop in drops:
        model = load_model('modelos/iteraciones=%s_drop=%s'%(it,drop))
        folder = ruta_out+'/iteraciones=%s_drop=%s'%(it,drop)
        try:
            os.mkdir(folder)
        except:
            pass
        for file in os.listdir(ruta):
            if '.txt' in file:
                texto = leer_completo(ruta+'/'+file).replace('\n',' ')
                prediccion = predice(model,texto)
                lines = prediccion_a_brat(prediccion)
            with io.open(folder+'/'+file.replace('.txt','.ann'),'w', encoding='utf-8') as file:
                for line in lines:
                    print(line)
                    file.write(line) 