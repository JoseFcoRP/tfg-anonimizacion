FROM continuumio/miniconda3:4.8.2

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD main.py /src/main.py
ADD spacy_ner.py /src/spacy_ner.py

ENTRYPOINT ["python", "/src/main.py"]