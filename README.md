# tfg-anonimizacion
En este repositorio se encuentra una herramienta para entrenar el NER de spacy a partir de anotaciones en formato [brat](https://brat.nlplab.org/standoff.html).
Los datos de entrada para entrenar el modelo deben encontrarse en una carpeta donde cada texto debe tener extensión ".txt" y una anotación con el mismo nombre de fichero con extensión ".ann".
Ejemplo:

    data/S0004-06142006000500012-1.txt
    data/S0004-06142006000500012-1.ann

Los datos de entrada para realizar predicciones de las anotaciones a partir de un modelo entrenado debe contener únicamente los ficheros ".txt".

Los parámetros que se le pueden indicar a esta herramienta son los siguientes:

 - Para el modo **entrenamiento** debe indicarse el parámetro `-t`, con cualquiera de los siguientes parámetros **opcionales**:
 -- `-in <path>`: Ruta del directorio donde se encuentran los textos.
 -- `-out <path>`: Ruta del directorio donde se desea escribir el modelo.
 -- `-i <n_iteraciones>`: Cantidad de iteraciones que se van a realizar durante el entrenamiento.
 -- `-d <drop>`: Coeficiente de drop para el entrenamiento del modelo (entre 0 y 1).
 - Para el modo de **predicción** debe indicarse el parámetro `-p`, con cualquiera de los siguientes parámetros **opcionales**:
 -- `-m <path>`: Ruta del directorio donde se encuentra el modelo que realiza las predicciones.
 -- `-in <path>`: Ruta donde se encuentran los ficheros para anotar.
 -- `-out <path>`: Ruta donde se desea escribir las anotaciones del modelo.
 
 Por defecto la ruta de entrada es *data*, la ruta de salida es *model*, la ruta del modelo es *model*, el número de iteraciones es *20* y el coeficiente de drop es *0.2*.
 
Existen dos formas de ejecutar esta herramienta, o bien se dispone de las dependencias localmente y se ejecuta llamando al script correspondiente, o se ejecuta en un contenedor con las dependencias instaladas.
## Ejecución local
Para ejecutar localmente la herramienta es necesario disponer de las dependencias del fichero *requirements.txt*, esto se puede hacer disponiendo de python 3 y ejecutando `pip install -r requirements.txt`, no obstante es una mejor práctica hacer uso de [entornos de conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
Para ejecutar el modo entrenamiento se debe ejecutar `python main.py -t [PARAMETROS OPCIONALES]` mientras que para ejecutar el modo de predicción sería `python main.py -p [PARAMETROS OPCIONALES]` .
## Ejecución con docker
Para ejecutar la herramienta dentro de un contenedor es necesario tener instalado [docker](https://docs.docker.com/get-docker/).
Se debe construir la imagen de la herramienta ejecutando en el directorio del repositorio `docker build . -t <NOMBRE DE LA IMAGEN>`.
Para ejecutar la herramienta se deben crear los volúmenes necesarios para leer y escribir en los directorios de entrada y salida, por tanto la herramienta se ejecuta de la siguiente forma:
 - Entrenamiento: `docker run -v <DIRECTORIO DATOS LOCAL>:<DIRECTORIO DATOS CONTENEDOR> -u $(id -u $USER) <NOMBRE DE LA IMAGEN> -t [PARAMETROS OPCIONALES]`
 - Predicción: `docker run -v <DIRECTORIO DATOS LOCAL>:<DIRECTORIO DATOS CONTENEDOR> -u $(id -u $USER) <NOMBRE DE LA IMAGEN> -p [PARAMETROS OPCIONALES]`

Se hace uso del argumento `-u $(id -u $USER)` para que los datos escritos queden con los permisos correspondiente al usuario que ejecuta la herramienta.
En este caso es recomendable tener los directorios con los datos y donde se guarde las salidas dentro de otro directorio de datos, o montar tantos volúmenes como sean necesarios para que la herramienta pueda leerlos dentro del contenedor.
En el ejemplo del repositorio sería `docker run -v $(pwd)/data:/data -v $(pwd)/models:/models -u $(id -u $USER) <NOMBRE DE LA IMAGEN> -t`.
