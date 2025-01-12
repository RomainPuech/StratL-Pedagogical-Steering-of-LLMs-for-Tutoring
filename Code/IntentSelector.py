# By Romain Puech
from taxonomy import Intent
import json


class IntentSelector():
    def __init__(self,intent_history=[]) -> None:
        self.previous_intent = intent_history[-1] if intent_history != [] else [Intent.S_STRATEGY]

    def get_intent(self,assessment,open=True):
        #print("selecting intent... ")
        previous_intent = self.previous_intent
        assessment_codes = self.extract_assessment_codes(assessment)
        intents = self.get_intent_aux(previous_intent,assessment_codes,open=open)
        #print(f"selected intent: {intents}")
        return intents
    
    def extract_assessment_codes(self,assessment):
        json_data = json.loads(assessment)
        selection = json_data['selection']
        codes = list(selection)
        return codes
        
    def get_intent_aux(self,previous_intent,assessment_codes,open=True):
        if not open and 'j' in assessment_codes:
            assessment_codes.append('k')
        #print(f"codes are {assessment_codes} and previous intent is {previous_intent}")
        intents = []
        # non previous intent-dependent selections:
        if Intent.G_GREETINGS in previous_intent:
            intents.append(Intent.G_GREETINGS)
        if Intent.P_REFLECTION in previous_intent:
            intents.append(Intent.G_GREETINGS)
        if 'k' in assessment_codes:
            intents.append(Intent.P_REFLECTION)
        if 'i' in assessment_codes:
            intents.append(Intent.S_OFFLOAD)
        if 'h' in assessment_codes:
            intents.append(Intent.S_STATE)
        if 'e' in assessment_codes and 'g' not in assessment_codes:
            intents.append(Intent.P_ARTICULATION)
        if any(code in assessment_codes for code in ('a','b','c')):
            intents.append(Intent.S_SELFCORRECTION)
        elif 'd' in assessment_codes:
            intents.append(Intent.S_STRATEGY)
        if 'j' in assessment_codes and 'k' not in assessment_codes and Intent.G_GREETINGS not in previous_intent:
            intents.append(Intent.P_LIMITS)
        
            

        # previous intent-dependent selections:
        
        if Intent.S_SELFCORRECTION in previous_intent:
            if 'f' in assessment_codes:
                intents.append(Intent.S_STRATEGY)
            elif 'a' in assessment_codes or 'b' in assessment_codes:
                intents.append(Intent.S_CORRECTION)
            if 'c' in assessment_codes:
                intents.append(Intent.S_OFFLOAD)

        if Intent.S_STRATEGY in previous_intent:
            if 'g' in assessment_codes and 'd' not in assessment_codes and 'f' not in assessment_codes:
                intents.append(Intent.P_HYPOTHESIS)
            elif ('l' in assessment_codes or 'k' in assessment_codes) and 'g' in assessment_codes:
                intents.append(Intent.S_HINT)
        if Intent.P_HYPOTHESIS in previous_intent:
            if 'f'in assessment_codes:
                intents.append(Intent.P_ARTICULATION)
        if len(intents)==0 and ('f' in assessment_codes or 'g' in assessment_codes):
            intents.append(Intent.S_STRATEGY)
        
        #dirty fixes
        if Intent.S_CORRECTION in intents and Intent.S_SELFCORRECTION in intents:
            intents.remove(Intent.S_SELFCORRECTION)

        if Intent.S_SELFCORRECTION in intents and Intent.S_OFFLOAD in intents:
            intents.remove(Intent.S_SELFCORRECTION)
        
        self.previous_intent = intents
        return intents

        
        

class StrategyIntentSelector(IntentSelector):

    def get_intent_aux(self, previous_intent,assessment_codes, open=True):

        if Intent.G_GREETINGS in previous_intent:
            intent = [Intent.G_GREETINGS]
        elif 'k' in assessment_codes:
            intent = [Intent.G_GREETINGS]
        elif 'j' in assessment_codes and not open:
            intent = [Intent.G_GREETINGS]
        else:
            intent = [Intent.S_STRATEGY]

        self.previous_intent = intent
        return intent


class LLMIntentSelector(IntentSelector):
    def __init__(self,client,intent_history=[]) -> None:
        self.client = client
        self.previous_intent = intent_history[-1] if intent_history != [] else [Intent.S_STRATEGY]

    def get_intent(self,assessment,open=True):
        #print("selecting intent... ")
        previous_intent = self.previous_intent
        assessment_codes = self.extract_assessment_codes(assessment)
        intents = self.get_intent_aux(self.client,previous_intent,assessment_codes,open=open)
        #print(f"selected intent: {intents}")
        return intents
    
    def get_prompt(self,previous_intent,assessment_codes):
        prompt = \
        f"""A student and a tutor are working on a math problem. The tutor responds to the student's messages following some intents. Before responding, the tutor first selects the most appropriate intents from a *Taxonomy*.
The tutor selects the intents based on the Productive Failure teaching method. The goal is to let the student explore the space of solution by themself to generate as many representation and solution methods as possible, even if they are only partially correct.
Select the best set of intents for the tutor's next message based on the following *Taxonomy*:

*Taxonomy*:
##
    P_LIMITS : Ask the student to identify some limits of their reasoning or answer.
    P_HYPOTHESIS : Ask the student to start by providing a guess, hypothesis or explain their intuition of the problem.
    P_ARTICULATION : Ask the student how they can write their intuition mathematically or detail their answer.
    P_REFLECTION : Reflect on the solution, recapitulate, and underline more general implications.
    S_SELFCORRECTION : Ask a question to hint the student to identify errors in their answer.
    S_CORRECTION : Correct a student's mistake
    S_STRATEGY : Make the student find and perform the next step to solve the problem without giving a hint.
    S_STATE : State a theorem or definition asked by the student.
    S_OFFLOAD : Perform a computation for the student
    S_HINT : Give a hint to the student
    G_GREETINGS : Say goodbye to the student
##

The tutor's previous intents for their last message to the student were: {previous_intent}.
The student answered the last tutor's message. An assessment of their answer has been conducted using the following codes:

assessment codes:
##
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
l) The student shows a strong lack of motivation
m) The student shows a strong lack of self-confidence
##

The assessment for the last student's message is: {assessment_codes}.

Based on the assessment and the last tutor's intents, select the most appropriate set of intents for the next tutor's message.
Proceed step by step. First, briefly justify your selection, then provide a list containing the selected intents from the *Taxonomy*.

Answer in the following json format:
##
{{
    "justification": "...",
    "intents": []

}}
##
{{"""
        return prompt
    
    def get_intent_aux(self,client, previous_intent,assessment_codes, open=True):
        #print("LLM Intent Selector called")
        client = self.client
        prompt = self.get_prompt(previous_intent,assessment_codes)
        intents=[]

        completion = client.chat.completions.create(
            model="myGPT4",
            messages = [{"role":"system", "content":prompt}],
            max_tokens=300, # should never be reached
            temperature=0,
            top_p=0.1
        )

        response = (completion.choices[0].message.content).replace("\\(","$").replace("\\)","$").replace("\\[","$$").replace("\\]","$$").replace("\\","")
        #print("The LLM intent selector thinks:")
        #print(response)
        # postprocess make sure the format is right
        s = response.find('{')
        e = response.rfind('}')
        response = response[s:e+1]
        json_data = json.loads(response)
        strintents_list = json_data['intents']
        for strintent in strintents_list:
            try:
                intent = Intent[strintent]
                intents.append(intent)
            except:
                pass


        self.previous_intent = intents
        return intents
