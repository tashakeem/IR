import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
import re

class QueryProcess:

    # def process(self,text):
    #     stoplist = set(stopwords.words('english'))
    #
    #     my_file = open("cacm/common_words", "r")
    #     data = my_file.read()
    #     data_into_list = data.split("\n")
    #     my_file.close()
    #
    #     word_list = [word for word in word_tokenize(text.lower())  if not word in stoplist
    #                  and not word in string.punctuation and not word in data_into_list]
    #     return word_list

    def process(self,string):
        stop_words = set(stopwords.words('english'))
        my_file = open("cacm/common_words", "r")
        data = my_file.read()
        data_into_list = data.split("\n")
        my_file.close()

        lower_string = string.lower()
        no_number_string = re.sub(r'\d+', '', lower_string)
        no_punc_string = re.sub(r'[^\w\s]', '', no_number_string)

        no_wspace_string = no_punc_string.strip()

        lst_string = [no_wspace_string][0].split()

        no_stpwords_string = ""

        for i in lst_string:
            if not i in stop_words and not i in data_into_list:
                no_stpwords_string += i + ' '

        no_stpwords_string = no_stpwords_string[:-1]

        word_list = [word for word in word_tokenize(no_stpwords_string)]
        return word_list


    def stemming(self,text):
        stemmer = PorterStemmer()
        query_stem = [stemmer.stem(word) for word in text]
        return (query_stem)

    def lemming(self,text):
        lemmer = WordNetLemmatizer()
        query_lem = [lemmer.lemmatize(word) for word in text]
        return (query_lem)
