import spacy
import random
import io
import os

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

ruta = ""

txt = [ruta+'\\'+x for x in os.listdir(ruta) if '.txt' in x]
ann = [x.replace('.txt','.ann') for x in txt]

TRAIN_DATA = [(leer_completo(ruta).replace('\n',' '),train_data_from_ann(ruta_ann)) for (ruta,ruta_ann) in zip(txt,ann)]

def train_spacy(data,iterations):
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
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp
	
prdnlp = train_spacy(TRAIN_DATA, 10)

def predice(prdnlp, text):
    doc = prdnlp(text)
    for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
			
def save_model(ruta):
	prdnlp.to_disk(ruta)