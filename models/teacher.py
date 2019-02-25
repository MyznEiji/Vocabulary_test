"""Defined a teacher model """
import csv
import random


from views import console


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
    all_csv_path = "/root/vocabulary_test/csv/all.csv"
    weekly_csv_path = "/root/vocabulary_test/csv/weekly.csv"

    csv_columns = "english,japanese,parts_of_speech"
    csv_columns_list = ["english" ,"japanese" ,"parts_of_speech"]

    def __init__(self, name=DEFAULT_TEACHER_NAME):
        super().__init__(name=name)

    def _hello_decorator(func):
        """Decorator to say a greeting if you are not greeting the user."""
        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper


    # 新しい単語を入力する
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


    # 新しい単語を追加する
    def write_new_vocabulary(self, new_vocabulary, csv_file):
        # if there is not csv
        with open(csv_file, "r+") as f:
            line = f.read().split('\n')[0]
            print(line)
            if line != self.csv_columns:
                f.seek(0)
                f.write(self.csv_columns + '\n')
    
    
        with open(csv_file, 'a') as c_file:
            writer = csv.DictWriter(c_file, fieldnames=self.csv_columns_list, lineterminator='\n')
            writer.writerow({"english": new_vocabulary['en'], "japanese": new_vocabulary['ja'], "parts_of_speech": new_vocabulary["parts_of_speech"]})
    

    # csvからlistへトランスフォーム
    def make_array(self, path):
        """transform from csv to list"""
        array = []
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                array.append([row['english'], row['japanese'], row['parts_of_speech']])
        return array



    def practice(self, csv_file):
        """for practice vocabulary"""

        # Vocabularyの数を取得
        f = open(csv_file)
        num_lines = sum(1 for line in f)
        f.close

        # Vocabularyのcsvデータを配列にトランスフォーム
        vocaburaly_array = self.make_array(csv_file)

        # 乱数を0からnum_lines-2(colomunsの行があるのと、配列は0から始まるから)までで10個生成して、vocabularyを取得する
        for i, question_num in enumerate(random.randint(0, num_lines-2) for n in range(10)):


            # 選択肢の作成
            choices = []
            for j in (random.randint(0, num_lines-2) for n in range(3)):
                choices.append(vocaburaly_array[j][1])
            # 選択肢に正解を追加
            choices.append(vocaburaly_array[question_num][1])
            choices = random.sample(choices, 4)

            # 質問する
            template = console.get_template(
                'question_english_meaning.txt', self.speak_color)
            answer_num = int(input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
                'english': vocaburaly_array[question_num][0],
                'japanese': vocaburaly_array[question_num][1],
                'number': i+1,
                'ch1': choices[0],
                'ch2': choices[1],
                'ch3': choices[2],
                'ch4': choices[3]
            })))

            # 答え合わせ
            if vocaburaly_array[question_num][1] == choices[answer_num]:
                template = console.get_template(
                    'correct.txt', 'blue')
                print(template.substitute())

            else:
                template = console.get_template(
                    'wrong.txt', 'red')
                print(template.substitute({
                        'answer_e': vocaburaly_array[question_num][0],
                        'answer_j': vocaburaly_array[question_num][1],
                        'parts_of_speech': vocaburaly_array[question_num][2]
                        }))









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
                # all.csvかweekly.csvnのどちらに書き込むか選択
                template = console.get_template(
                    'which_all_or_weekly.txt', self.speak_color)
                want_to_do_num = int(input(template.substitute()))

                # 0の場合all_csv、1の場合weekly_csvを読み込みpracticeをする
                if want_to_do_num == 0:
                    self.practice(self.all_csv_path)
                elif want_to_do_num == 1:
                    self.practice(self.weekly_csv_path)


            elif int(todo) == 1:
                new_vocabulary = self.input_new_vocabulary()
                self.write_new_vocabulary(new_vocabulary, self.weekly_csv_path)
                
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
