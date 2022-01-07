import os
import streamlit as st
import pickle
import random
import json
from PIL import Image


def show():
    st.set_page_config(page_title='User trust study', layout='wide')

    @st.cache
    def get_questions():
        question_seed = random.randint(0, 100)
        random.seed(question_seed)
        with open('questions.pkl', 'rb') as f:
            all_questions = pickle.load(f)
        questions = random.sample(all_questions, 3)
        return questions

    def go_to_next_question():
        st.session_state.curr_question_idx += 1
        if (st.session_state.curr_question_idx ==
                st.session_state.total_questions):
            st.session_state.curr_question_idx = 'DONE'

    def store_and_go(result, qno):
        st.session_state.answers[qno] = result
        go_to_next_question()

    def store_final_user_stats(answers):
        a = [answers]
        file_name = 'data_collected.json'
        with open(file_name, 'a', encoding='utf-8') as f:
            json.dump(a, f, ensure_ascii=False)
            f.write(os.linesep)

    def display_question(questions, qno):
        question = questions[qno]
        st.write(question["unique_id"])
        images = question["images"]
        det_image = Image.open(images[0])
        st.image(det_image, caption='Detection')

        if question["type"] == "one":
            st.header("Classification decision explanation")
            col1, col2 = st.columns(2)
            with col1:
                image_one = Image.open(images[1])
                st.image(image_one, caption='Robot A explanation')
            with col2:
                image_two = Image.open(images[1])
                st.image(image_two, caption='Robot B explanation')

        if question["type"] == "two":
            st.header('Robot A bounding box decision explanation')
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                image_one = Image.open(images[1])
                st.image(image_one, caption='xmin')
            with col2:
                image_two = Image.open(images[2])
                st.image(image_two, caption='ymin')
            with col3:
                image_three = Image.open(images[3])
                st.image(image_three, caption='xmax')
            with col4:
                image_four = Image.open(images[4])
                st.image(image_four, caption='ymax')

            st.header('Robot B bounding box decision explanation')
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                image_five = Image.open(images[5])
                st.image(image_five, caption='xmin')
            with col2:
                image_six = Image.open(images[6])
                st.image(image_six, caption='ymin')
            with col3:
                image_seven = Image.open(images[7])
                st.image(image_seven, caption='xmax')
            with col4:
                image_eight = Image.open(images[8])
                st.image(image_eight, caption='ymax')

        result = st.radio(question["question"],  question["options"])
        st.button('Next question', on_click=store_and_go,
                  args=(result, question["unique_id"]))

    questions = get_questions()
    st.session_state.get(questions)

    if "questions" not in st.session_state:
        st.session_state.questions = questions
        st.session_state.answers = {}
        st.session_state.curr_question_idx = 0
        st.session_state.total_questions = len(st.session_state.questions)

    st.sidebar.text('Description about task')
    st.sidebar.text('Contact: depa03@dfki.de')
    st.sidebar.markdown('<h5>Created by Deepan Chakravarthi Padmanabhan</h5>',
                        unsafe_allow_html=True)

    if st.session_state.curr_question_idx != 'DONE':
        display_question(questions, st.session_state.curr_question_idx)
    else:
        st.success('All questions answered. Thank you for your valuable time.')
        print('ALL DONE: ')
        store_final_user_stats(st.session_state.answers)
    st.write('Answers: ')
    st.write(st.session_state.answers)


if __name__ == '__main__':
    show()
