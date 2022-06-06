import math

class Calculate:

    def length(self,vector):
        sq_length = 0
        for index in range(0, len(vector)):
            sq_length += math.pow(vector[index], 2)
        return math.sqrt(sq_length)


    def dot_product(self,vector1, vector2):
        if len(vector1) == len(vector2):
            dot_prod = 0
            for index in range(0, len(vector1)):
                if not vector1[index] == 0 and not vector2[index] == 0:
                    dot_prod += vector1[index] * vector2[index]
            return dot_prod
        else:
            return "Unmatching dimensionality"