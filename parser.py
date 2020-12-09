import PyPDF2
import textract
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
from itertools import islice
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def get_pdf_title(pdf_file_path):
    pdf_reader = PyPDF2.PdfFileReader(open(pdf_file_path, "rb")) 
    return pdf_reader.getDocumentInfo().title

def get_tags(filename):
   """Reads Most frequent tags appearing in the PDF or Image"""
   extension = filename.split('.')[-1];
   text = ""
   title = ""
   if extension == 'pdf':
      pdfFileObj = open(filename,'rb')
      pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
      num_pages = pdfReader.numPages
      count = 0

      #The while loop will read each page.
      while count < num_pages:
         pageObj = pdfReader.getPage(count)
         count +=1
         text += pageObj.extractText()

      title = get_pdf_title(filename)

      if title:
         text += " " + title

   if text == "":
      text = textract.process(os.path.join(os.getcwd(), filename), method='tesseract', language='eng')

   if not isinstance(text, str):
      text = text.decode("utf-8")

   tokens = word_tokenize(text)
   if title:
      tokens += word_tokenize(title) 

   stop_words = string.punctuation #set(stopwords.words('english') + list(string.punctuation))
   # stop_words = set(stopwords.words('english') + list(string.punctuation))

   keywords = [word for word in tokens if not word in stop_words]

   #removing everything except nouns
   tags = nltk.pos_tag(keywords)
   nouns = [word for word,pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
   # print(keywords)

   keyword_freqency = dict()

   for word in nouns:
      keyword_freqency[word] = keyword_freqency.get(word, 0) + 1

   sorted_keywords = {
      k: v for k, 
      v in sorted(keyword_freqency.items(), key=lambda item: item[1], reverse=True)
   }
   frequent_keywords = list(islice(sorted_keywords, 10))
   return frequent_keywords


filename = 'UPSC FORM  FURKAN.pdf'
# filename = 'NPR_NRIC.PNG' 
# filename = 'RCA-XOVER-JIRA.pdf' 

# print("Tags", get_tags(filename))

