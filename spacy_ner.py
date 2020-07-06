import spacy
import random
import io
import os
import logging
import shutil

logger = logging.getLogger(__name__)

def leer_por_lineas(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return [x.replace('\n','') for x in fichero.readlines()]
        
def leer_completo(ruta):
    with io.open(ruta,'r', encoding='utf-8') as fichero:
        return fichero.read()
        
def train_data_from_ann(ruta):
    tags = {'entities':[]}
    for line in leer_por_lineas(ruta):
        tags['entities'].append((int(line.split()[2]),int(line.split()[3]),line.split()[1]))
    return tags
    
def train_spacy(data,iterations, drop):
    TRAIN_DATA = data
    nlp = spacy.blank('es')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            logger.info("Iteración " + str(itn+1))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=drop,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            logger.debug(f"losses: {losses}")
    return nlp

def save_model(modelo, ruta):
    logger.info(f"Guardando modelo en el directorio: {ruta}")
    os.makedirs(ruta, exist_ok=True)
    modelo.to_disk(ruta)
    
def load_model(ruta):
    logger.info(f"Cargando modelo del directorio: {ruta}")
    return spacy.load(ruta)
    
def model_from_brat(path_in,path_out, it, drop):
    # Papare data for training
    ruta = os.path.abspath(path_in)
    logger.info(f"Leyendo ficheros del directorio: {ruta}")
    txt = [os.path.join(ruta,x) for x in os.listdir(ruta) if '.txt' in x]
    ann = [x.replace('.txt','.ann') for x in txt]
    TRAIN_DATA = [(leer_completo(ruta).replace('\n',' '),train_data_from_ann(ruta_ann)) for (ruta,ruta_ann) in zip(txt,ann)]
    # Train and save model
    ner = train_spacy(TRAIN_DATA, it, drop)
    save_model(ner,os.path.abspath(path_out))
    
      
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
        texto = "T%d\t%s %d %d\t%s\n"%(token,tag['tag'],tag['start'],tag['end'],tag['text'])
        lineas.append(texto)
        token+=1
    return lineas
    
def predict_from_model(path_model,path_in, path_out):
    model = load_model(os.path.abspath(path_model))
    ruta_in = os.path.abspath(path_in)
    ruta_out = os.path.abspath(path_out)
    os.makedirs(ruta_out, exist_ok=True)
    for file in os.listdir(ruta_in):
        if '.txt' in file:
            texto = leer_completo(os.path.join(ruta_in,file)).replace('\n',' ')
            prediccion = predice(model,texto)
            lines = prediccion_a_brat(prediccion)
            shutil.copy2(os.path.join(ruta_in,file), os.path.join(ruta_out,file))
            with io.open(os.path.join(ruta_out,file.replace('.txt','.ann')),'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line) 
    