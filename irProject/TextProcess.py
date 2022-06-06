import datefinder
from textblob import TextBlob

class TextProcess:


    def get_date(self,string_with_dates):
        match=[]
        matches = datefinder.find_dates(string_with_dates)
        match.append(matches)
        # for match in matches:
        #     print(match)
        return match

    def check(self,string):
        result=[]
        k=1
        while (k==1):
            k=0
            if (string.find("U.S") != -1):
                string=string.replace("U.S","")
                result.append('UNITED STATES')
                k=1
            if (string.find("U.K") != -1):
                string = string.replace("U.K", "")
                result.append('UNITED KINGDOM')
                k = 1
            if (string.find("U_S") != -1):
                string=string.replace("U_S","")
                result.append('UNITED STATES')
                k=1
            if (string.find("U_K") != -1):
                string=string.replace("U_K","")
                result.append('UNITED KINGDOM')
                k=1
            if (string.find("U-S") != -1):
                string=string.replace("U-S","")
                result.append('UNITED STATES')
                k=1
            if (string.find("U-K") != -1):
                string=string.replace("U-K","")
                result.append('UNITED KINGDOM')
                k=1
            if (string.find("US") != -1):
                string=string.replace("US","")
                result.append('UNITED STATES')
                k=1
            if (string.find("UK") != -1):
                string=string.replace("UK","")
                result.append('UNITED KINGDOM')
                k=1
            if (string.find("U.N") != -1):
                string=string.replace("U.N","")
                result.append('UNITED NATIONS')
                k=1
            if (string.find("U_N") != -1):
                string = string.replace("U_N", "")
                result.append('UNITED NATIONS')
                k = 1
            if (string.find("U-N") != -1):
                string=string.replace("U-N","")
                result.append('UNITED NATIONS')
                k=1
            if (string.find("VIET NAM") != -1):
                string=string.replace("VIET NAM","")
                result.append('VIET NAM')
                k=1
            if (string.find("VIETNAM") != -1):
                string = string.replace("VIETNAM", "")
                result.append('VIET NAM')
                k=1
        return result


    def auto_correct(self,text):
        query = TextBlob(text)
        query = query.correct()
        return query




