from random import choices

class MirroredQuestion():

    def __init__(self,p=0.1,questions=[1,0]):
        ''' Probability p that the respondend will answer the original question,
            thus 1-p is hte probability that will answer the opposite
        '''

        self.p = float(p)
        self.questions=questions
        if self.p == 0.5:
            raise Exception('Not allowed')
        elif self.p < 0.0 or self.p > 1.0:
            raise Exception('Probability must be [0,1]')

    def respond(self,question):
        if question in self.questions:
            decision = choices(['P','N'], [self.p,1- self.p],k=1)[0]

            if decision == 'P':
                # respond the positive form
                return question
            elif decision == 'N':

                if question == self.questions[0]:
                    return self.questions[1]
                elif question == self.questions[1]:
                    return self.questions[0]
        else:
            raise Exception('This question is not in the list')

    @staticmethod
    def estimate(p,questions,p_y,y):
        i = questions.index(y)
        if i == 0:
            p_z_1 = (p_y + p - 1.0)/(2.0 * p - 1.0)

            if p_z_1 <= 0:
                return 0.0
            else:
                return p_z_1
        elif i == 1:
            p_z_1 = (p_y + p - 1.0) / (2.0 * p - 1.0)
            p_z_0 = 1.0 - p_z_1
            return p_z_0
        else:
            raise Exception('Only binary responses allowed')
