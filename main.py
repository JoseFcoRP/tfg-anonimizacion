import spacy_ner
import argparse
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Aplicación para creación de modelos de NER basado en anotaciones en formato brat y predicciones a partir de esos modelos')

    parser.add_argument('-t', action="store_true", dest='t', default=False)
    parser.add_argument('-p', action="store_true", dest='p',default=False)
    
    parser.add_argument('-m', action="store", dest='path_model', default="model")
    parser.add_argument('-in', action="store", dest='path_in', default="data")
    parser.add_argument('-out', action="store", dest='path_out', default="model")
    parser.add_argument('-i', action="store", dest='iteraciones', type=int, default=20)
    parser.add_argument('-d', action="store", dest='drop', type=float, default=0.2)
    
    argumentos = parser.parse_args()
    if argumentos.t:
        logger.info(f'Iniciando entrenamiento')
        logger.info(f'Parámetros: path_in={argumentos.path_in}, path_out={argumentos.path_out}, iteraciones={argumentos.iteraciones},  drop={argumentos.drop}')
        spacy_ner.model_from_brat(argumentos.path_in,
                                    argumentos.path_out,
                                    argumentos.iteraciones,
                                    argumentos.drop)
    elif argumentos.p:
        logger.info(f'Iniciando predicción')
        logger.info(f'Parámetros: path_model={argumentos.path_model}, path_in={argumentos.path_in}, path_out={argumentos.path_out}, iteraciones={argumentos.iteraciones},  drop={argumentos.drop}')
        spacy_ner.predict_from_model(argumentos.path_model,
                                    argumentos.path_in,
                                    argumentos.path_out)

if __name__ == "__main__":
    main()

