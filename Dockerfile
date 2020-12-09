FROM ubuntu:20.04
COPY . /app
WORKDIR /app
RUN apt-get clean
RUN apt-get update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y poppler-utils
RUN DEBIAN_FRONTEND='noninteractive' apt-get install -y tesseract-ocr
RUN pip3 install flask
RUN pip3 install PyPDF2
RUN pip3 install textract
RUN pip3 install nltk
EXPOSE 5000
ENTRYPOINT [ "python3" ] 
CMD [ "app.py" ]