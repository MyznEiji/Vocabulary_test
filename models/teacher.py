"""Defined a teacher model """
from models import ranking
from views import console
import csv


DEFAULT_TEACHER_NAME = 'Smisu'


class Teacher(object):
    """Base model for Teacher."""

    def __init__(self, name=DEFAULT_TEACHER_NAME, user_name='',
                 speak_color='green'):
        self.name = name
        self.user_name = user_name
        self.speak_color = speak_color

    def hello(self):
        """Returns words to the user that the teacher speaks at the beginning."""
        while True:
            template = console.get_template('hello_teacher.txt', self.speak_color)
            user_name = input(template.substitute({
                'teacher_name': self.name}))

            if user_name:
                self.user_name = user_name.title()
                break


class EnglishTeacher(Teacher):
    """Handle data model on English."""

    parts_of_speech_list = ["Noun", "Pronoun", "Adjective", "Verb", "Adverb", "Preposition", "Conjunction", "Interjection", "Phrase"]
    csv_path = "./csv/hoge.csv"
    csv_columns = "english,japanese,parts_of_speech"
    csv_columns_list = ["english" ,"japanese" ,"parts_of_speech"]

    def __init__(self, name=DEFAULT_TEACHER_NAME):
        super().__init__(name=name)
        self.ranking_model = ranking.RankingModel()

    def _hello_decorator(func):
        """Decorator to say a greeting if you are not greeting the user."""
        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper



    def input_new_vocabulary(self):
        new_vocabulary = {}
    
        template = console.get_template(
            'english_vocabulary.txt', self.speak_color)
        new_vocabulary["en"] = input(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
    
        template = console.get_template(
            'japanese_meaning.txt', self.speak_color)
        new_vocabulary["ja"] = input(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
    
        template = console.get_template(
            'which_parts_of_speech.txt', self.speak_color)
        parts_of_speech_num = input(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
        new_vocabulary["parts_of_speech"] = self.parts_of_speech_list[int(parts_of_speech_num)]
    
        return new_vocabulary


    
    def write_new_vocabulary(self, new_vocabulary):
        # if there is not csv
        with open(self.csv_path, "r+") as f:
            line = f.read().split('\n')[0]
            print(line)
            if line != self.csv_columns:
                f.seek(0)
                f.write(self.csv_columns + '\n')
    
    
        with open(self.csv_path, 'a') as c_file:
            writer = csv.DictWriter(c_file, fieldnames=self.csv_columns_list, lineterminator='\n')
            writer.writerow({"english": new_vocabulary['en'], "japanese": new_vocabulary['ja'], "parts_of_speech": new_vocabulary["parts_of_speech"]})
    



    def practice(self):
        with open(self.csv_path, 'r') as f:
            print(f.read())


            while True:
            	# 一行づづ読み込んでいる
                line = f.readline()
                # 読み込み時はデフォルトでend='¥n'というオプションになっているので改行が入る。
                print(line, end="")
                if not line:
                    break










    @_hello_decorator
    def ask_user_todo(self):
        """Collect favorite restaurant information from users."""
        while True:
            template = console.get_template(
                'what_do.txt', self.speak_color)
            todo = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
            }))

            if int(todo) == 0:
                print("Practice")
                self.practice()
            elif int(todo) == 1:
                new_vocabulary = self.input_new_vocabulary()
                self.write_new_vocabulary(new_vocabulary)
            elif int(todo) == 2:
                break
            else:
                print("Error. Please enter again")




    @_hello_decorator
    def thank_you(self):
        """Show words of appreciation to users."""
        template = console.get_template('good_by.txt', self.speak_color)
        print(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
