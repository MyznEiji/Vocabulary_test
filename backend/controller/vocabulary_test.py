"""Controller for speaking with teacher"""
from models import teacher


def talk_about_english():
    """Function to speak with teacher"""
    english_teacher = teacher.EnglishTeacher()
    english_teacher.hello()
    english_teacher.ask_user_todo()
    english_teacher.thank_you()
