# by Romain Puech

from utils import print_logs
import json
class Assessor():
    def __init__(self,client,model,assessment_history=[]) -> None:
        self.client = client
        self.model = model
        self.history = list(assessment_history)

    def get_purpose(self,pb,sol):
        purpose = \
        f"""A student and their tutor are working on a math problem:
*Problem Statement*:
##
{pb}
##

The *Provided Solution* of this problem is:
##
{sol}
##

The tutor's utterances are preceded by "Tutor:" and the student's utterances are preceded by "Student:".

Analyze the last student's utterance.
select all the feedbacks that apply from "a,b,c,d,e,f,g,h,i,j,k":

a) The student is using or suggesting a wrong method or taking a wrong path to solve the problem
b) The student made an error in the algebraic manipulation
c) The student made a numerical error
d) The student provided an intuitive or incomplete solution
e) The student's answer is not clear or ambiguous
f) The student correctly answered the tutor's previous question
g) The student is explicitly asking about how to solve the problem
h) The student is explicitly asking the tutor to state a specific theorem
i) The student is explicitly asking the tutor to do a numerical calculation
j) The student and tutor arrived at a complete solution for the entirety of the initial *Problem Statement*
k) The student and tutor arrived at a complete solution for the entirety of the initial *Problem Statement* equivalent to the method provided in the *Provided Solution*

Moreover select if relevant some emotional states from "l,m":
l) The student shows a strong lack of motivation
m) The student shows a strong lack of self-confidence

Proceed step by step. First briefly justify your selection, then provide a string containing the selected letters.
Answer in the following JSON format:
##
{{
    "justification": "..",
    "selection": ".."

}}
##
Analyze the last student's utterance.
{{"""
        return purpose

    def create_prompt(self,pb,sol,tutor_messages,student_messages):
        
        purpose = self.get_purpose(pb,sol)
        prompt = [{"role": "system", "content": purpose}] + \
            [
            msg for i in range(len(self.history))
                for msg in (
                    {"role": "user", "content": f"Tutor: \"{tutor_messages[i]}\"\nStudent: \"{student_messages[i]}\"\n"},
                    {"role": "assistant", "content": self.history[i]}
                )
            ]
        prompt.append({"role": "user", "content":f"Tutor: \"{tutor_messages[-1]}\"\nStudent: \"{student_messages[-1]}\"\n" })
        return prompt

    def assess(self,pb,sol,student_messages,tutor_messages):
        prompt = self.create_prompt(pb,sol,tutor_messages,student_messages)
        #print("Assessor called with prompt:")
        #print(print_logs(prompt))
        client = self.client
        completion = client.chat.completions.create(
            model=self.model,
            messages=prompt,
            response_format = { "type": "json_object" },
            max_tokens=300, # should never be reached
            temperature=0.0,
            top_p=0.1
        )

        response = (completion.choices[0].message.content).replace("\\(","$").replace("\\)","$").replace("\\[","$$").replace("\\]","$$").replace("\\","")
        #print("ASSESSMENT IS \n",response)
        # postprocess make sure the format is right
        s = response.find('{')
        e = response.rfind('}')
        response = response[s:e+1]
        json_data = json.loads(response)
        selection = json_data['selection']
        selection = selection.replace(' ','').replace(',','')
        json_data['selection'] = selection
        assessment = json.dumps(json_data)

        self.history.append(assessment)

        total_tokens = completion.usage.total_tokens
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        
        return assessment, prompt_tokens, completion_tokens
    

class NoJustificationAssessor(Assessor):
    def get_purpose(self, pb, sol):
        purpose = \
        f"""A student and their tutor are working on a math problem:
*Problem Statement*:
##
{pb}
##

The *Provided Solution* of this problem is:
##
{sol}
##

The tutor's utterances are preceded by "Tutor:" and the student's utterances are preceded by "Student:".

Analyze the last student's utterance.
select all the feedbacks that apply from "a,b,c,d,e,f,g,h,i,j":

a) The student is using or suggesting a wrong method or taking a wrong path to solve the problem
b) The student made an error in the algebraic manipulation
c) The student made a numerical error
d) The student provided an intuitive or incomplete solution
e) The student's answer is not clear or ambiguous
f) The student correctly answered the tutor's previous question
g) The student is explicitly asking about how to solve the problem
h) The student is explicitly asking the tutor to state a specific theorem
i) The student is explicitly asking the tutor to do a numerical calculation
j) The student and tutor arrived at a complete solution for the entirety of the initial *Problem Statement*
k) The student and tutor arrived at a complete solution for the entirety of the initial *Problem Statement* equivalent to the method provided in the *Provided Solution*

Moreover select if relevant some emotional states from "l,m":
l) The student shows a strong lack of motivation
m) The student shows a strong lack of self-confidence

Answer in the following json format:
##
{{
    "selection": ".."
}}
##
Analyze the last student's utterance.
{{"""
        return purpose
    
class ShortMemoryAssessor(Assessor):
    def assess(self, pb, sol, student_messages, tutor_messages):
        if len(student_messages) > 3:
            student_messages = student_messages[-3:]
        if len(tutor_messages) > 3:
            tutor_messages = tutor_messages[-3:]

        return super().assess(pb, sol, student_messages, tutor_messages)
    
    def create_prompt(self,pb,sol,tutor_messages,student_messages):
        
        purpose = self.get_purpose(pb,sol)
        prompt = [{"role": "system", "content": purpose}]
        extension = \
            [
            msg for i in range(len(tutor_messages)-1)
                for msg in (
                    {"role": "user", "content": f"Tutor: \"{tutor_messages[i]}\"\nStudent: \"{student_messages[i]}\"\n"},
                    {"role": "assistant", "content": self.history[-len(tutor_messages)+1+i]}
                )
            ]
        prompt = prompt + extension
        prompt.append({"role": "user", "content":f"Tutor: \"{tutor_messages[-1]}\"\nStudent: \"{student_messages[-1]}\"\n" })
        #print("Short mem prompt len is:",len(''.join([msg["content"] for msg in prompt])))
        return prompt
    
class EndAssessor(Assessor):
    def get_purpose(self, pb, sol):
        purpose = \
        f"""A student and their tutor are working on a math problem:
*Problem Statement*:
##
{pb}
##

The *Provided Solution* of this problem is:
##
{sol}
##

The tutor's utterances are preceded by "Tutor:" and the student's utterances are preceded by "Student:".

Analyze the last student's utterance.
select all the feedbacks that apply from "j,k":

j) The student and tutor arrived at a complete solution for all questions in the initial *Problem Statement*
k) The student and tutor arrived at a complete solution for all questions in the initial *Problem Statement* equivalent to the method provided in the *Provided Solution*

Proceed step by step. First briefly justify your selection, then provide a string containing the selected letters.
Answer in the following json format:
##
{{
    "justification": "..",
    "selection": ".."

}}
##
Analyze the last student's utterance.
{{"""
        return purpose