from datetime import datetime

class QuestionHandler():

    def __init__(self,questions):
        '''
        Filter the valid questions first
        :param questions:
        '''
        self.today = datetime.now()
        self._questions = []

        for q in questions:
            if q['completed']== False:
                q_start = datetime.strptime(q['begin_datetime'], "%Y-%m-%dT%H:%M:%SZ")
                q_end = datetime.strptime(q['end_datetime'], "%Y-%m-%dT%H:%M:%SZ")

                if self.today >= q_start and self.today <= q_end:
                    self._questions.append(q)
            else:
                continue

    def get_valid_questions(self):

        return self._questions
