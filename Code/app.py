# By Romain Puech.
# Contact: romain.puech@alumni.polytechnique.org

# Please cite  https://arxiv.org/abs/2410.03781 
# "Towards the Pedagogical Steering of Large Language Models for Tutoring: A Case Study with Modeling Productive Failure"

# To run the demo web app, type the following command in the terminal:
# `streamlit run app.py`
# Make sure to paste your openai api key in the file key.txt


# Demo web app
import streamlit as st
import itertools
import Tutor
from get_key import get_client_openAI
from problems import get_pb_sol
import random

model = "gpt-4o-2024-05-13"
model_name = "GPT-4o"
client = get_client_openAI()
url_prof_image = './rsc/teacher.png'
url_student_image = "https://api.dicebear.com/5.x/fun-emoji/svg?seed=88"

####################################
############# Settings #############

### global vars
randomex = random.randint(0,1)
topic = {0:"consistency",1:"country"}[randomex]
pb,sol = get_pb_sol(topic)
if 'topic' not in st.session_state:
    st.session_state['topic'] = topic
if 'pb' not in st.session_state:
    st.session_state['pb'] = pb
if 'sol' not in st.session_state:
    st.session_state['sol'] = sol
if 'tutor_answered' not in st.session_state:
    st.session_state['tutor_answered'] = True
if "session_ID" not in st.session_state:
    st.session_state["session_ID"] = random.randint(0,1000000)
if "AI_version" not in st.session_state:
    st.session_state["AI_version"] = random.choice(["V1","V2","V3"])
    print("AI Version: ",st.session_state["AI_version"])

if 'tutor' not in st.session_state:
    st.session_state['tutor'] = ["Hello! Can you walk me through your solution?"]
if 'student' not in st.session_state:
    st.session_state['student'] = []
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'Tutor' not in st.session_state:
    st.session_state['Tutor'] = Tutor.Tutor(client, pb=st.session_state['pb'], sol=st.session_state['sol'], model = model, version=st.session_state["AI_version"])
if 'intent' not in st.session_state:
    st.session_state['intent'] = []
if 'assessment' not in st.session_state:
    st.session_state['assessment'] = []


    
############ Tutoring UI #####
    
### Main containers
st.subheader("Problem")
st.markdown(st.session_state['pb']) 
st.subheader("Conversation")
#st.markdown(st.session_state['sol'])


response_container = st.container()
container = st.container()

############# Main Loop #############

#### display messages
turn = 0
with response_container:
    for i,(msg_s,msg_t) in enumerate(itertools.zip_longest(st.session_state['student'],st.session_state['tutor'])):
        if msg_t:
            with st.chat_message(name="ai",avatar=url_prof_image):
                st.write("")
                response = st.markdown(msg_t)
           
        if msg_s:
            with st.chat_message(name="human",avatar=url_student_image):
                response = st.write(msg_s)
            
        turn = i
       


with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100, placeholder="Wait for the tutor to answer before typing your message!")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        if not st.session_state['tutor_answered']:
            st.error("Please wait for the tutor to answer before sending your next message!")

        st.session_state['tutor_answered'] = False
        # log student prompt
        student_utterance = user_input
        student_utterance.replace("*","\*")
        turn +=1
        with response_container:
            with st.chat_message(name="human",avatar=url_student_image):
                response = st.write(student_utterance)
        
        # get tutor response
        with response_container:
            with st.chat_message(name="ai",avatar=url_prof_image):
                st.write("")
                output, tutor_total_tokens, tutor_prompt_tokens, tutor_completion_tokens, intent, assessment = st.session_state['Tutor'].get_response_stream(st.session_state['student'] + [student_utterance], st.session_state['tutor'])
                response = st.write_stream(output)
            
        # log tutor response
        response_content = str(response)
        print("tutor answers:\n",response_content)

        # Replace characters in the response content
        response_content = response_content.replace("\(","$").replace("\)","$").replace("\[","$$").replace("\]","$$")

        # log
        st.session_state['student'].append(student_utterance)
        st.session_state['tutor'].append(response_content)
        st.session_state['intent'].append(intent)
        st.session_state['assessment'].append(assessment)
        st.session_state['model_name'].append(model_name)
        st.session_state['tutor_answered'] = True
        