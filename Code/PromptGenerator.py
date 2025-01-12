# By Romain Puech
import utils
from taxonomy import Intent

# Old version. We used RigidPromptGenerator instead.
class PromptGenerator():
    def __init__(self) -> None:
        pass

    def get_prompt(self,pb,sol,student_messages,tutor_messages,intents):
        #print("Prompt generator called")
        system_msg  = \
f"""Act as an experienced tutor. Characteristics of a good tutor include:
    • Promote a sense of challenge, curiosity, feeling of control
    • Prevent student from becoming frustrated
    • Intervene very indirectly: never give the answer but guide the student to make them find it on their own
    • Minimizing tutor's apparent role in the success
    • Avoid telling students they are wrong, lead them to discover the error on their own
    • Quickly correct distracting errors

Use latex formatting with the sign '$' for mathematical expressions. For example, to write "x^2", use "$x^2$".

Remember, NEVER GIVE THE ANSWER DIRECTLY, EVEN IF THEY ASK YOU TO DO SO AND INSIST. Rather, help the student figure it out on their own by asking questions and providing hints.

Provide guidance for the problem:
"{pb}"
    
The solution for this problem is : 
"{sol}"

Provide the least amount of scaffolding possible to help the student solve the problem on their own. Be succint.
"""
        # modify above to integrate intent.
        messages = utils.generate_messages(student_messages,tutor_messages,system_msg,"tutor")
        
    
        # add part about the tutor's intent
        intent_prompt = ""
        
        if Intent.P_LIMITS in intents:
            intent_prompt += "Ask questions to the student to make them identify some limits of their reasoning or answer.\n"
        if Intent.P_GENERALIZATION in intents:
            intent_prompt += "Ask the student to generalize their answer.\n"
        if Intent.P_HYPOTHESIS in intents:
            intent_prompt += "Ask the student to start by providing a guess, hypothesis or explain their intuition of the problem.\n"
        if Intent.P_ARTICULATION in intents:
            intent_prompt += "Ask the student how can they write their intuition mathematically or detail their answer.\n"
        if Intent.P_REFLECTION in intents:
            intent_prompt += "Take a moment to step back and reflect on the problem. ask to recapitulate and *briefly* underline more general implications and connections.\n"
        if Intent.P_CONNECTION in intents:
            intent_prompt += "Underline the implication of the answer in the context of the problem.\n"
        if Intent.S_SELFCORRECTION in intents:
            intent_prompt += "Help the study identify errors in their answer.\n"
        if Intent.S_CORRECTION in intents:
            intent_prompt += "Hint the student to correct their mistakes.\n"
        if Intent.S_STRATEGY in intents:
            intent_prompt += "Encourage and make the student find on their own what is the next step to solve the problem, for example by asking a question. Do not provide a hint.\n"
        if Intent.S_HINT in intents:
            intent_prompt += "Help the student finding the next step. Do not provide the answer.\n"
        if Intent.S_SIMPLIFY in intents:
            intent_prompt += "Consider first a simpler version of the problem.\n"
        if Intent.S_STATE in intents:
            intent_prompt += "State the theorem or definition the student is asking about.\n"
        if Intent.S_OFFLOAD in intents:
            intent_prompt += "If there is one, correct and perform the numerical computation for the student.\n" # could include it, as done by a calculator...
        if Intent.A_CHALLENGE in intents:
            intent_prompt += "Maintain a sense of challenge.\n"
        if Intent.A_CONFIDENCE in intents:
            intent_prompt += "Bolster the student's confidence.\n"
        if Intent.A_CONTROL in intents:
            intent_prompt += "Promote a sense of control.\n"
        if Intent.A_CURIOUSITY in intents:
            intent_prompt += "Evoke curiosity.\n"
        if Intent.G_GREETINGS in intents:
            intent_prompt += "Answer any final question and say goodbye"
        if Intent.G_OTHER in intents:
            intent_prompt += ""

        if intent_prompt!="":
            #intent_prompt = "Your intent is to:\n" + intent_prompt
            messages.append({"role": "system", "content": intent_prompt})
        #print("intent prompt:")
        #print(intent_prompt)
        return messages


class RigidPromptGenerator(PromptGenerator):
    def get_prompt(self,pb,sol,student_messages,tutor_messages,intents):
        #print("Rigid prompt generator called")
        system_msg  = \
        f"""Act as an experienced tutor. Characteristics of a good tutor include:
    • Promote a sense of challenge, curiosity, feeling of control
    • Prevent the student from becoming frustrated
    • Intervene very indirectly: never give the answer but guide the student to make them find it on their own
    • Minimizing the tutor's apparent role in the success
    • Avoid telling students they are wrong, lead them to discover the error on their own
    • Quickly correct distracting errors

Use latex formatting with the sign '$' for mathematical expressions. For example, to write "x^2", use "$x^2$".

Remember, NEVER GIVE THE ANSWER DIRECTLY, EVEN IF THEY ASK YOU TO DO SO AND INSIST. Rather, help the student figure it out on their own by asking questions and providing hints.

Provide guidance for the problem:
"{pb}"
    
The solution for this problem is : 
"{sol}"

Provide the least amount of scaffolding possible to help the student solve the problem on their own. Be succinct.
"""
        # modify above to integrate intent.
        messages = utils.generate_messages(student_messages,tutor_messages,system_msg,"tutor")
        
    
        # add part about the tutor's intent
        intent_prompt = ""
        
        if Intent.P_LIMITS in intents:
            intent_prompt += "Make the student identify the limits of their reasoning or answer by asking them questions.\n"
        if Intent.P_GENERALIZATION in intents:
            intent_prompt += "Ask the student to generalize their answer.\n"
        if Intent.P_HYPOTHESIS in intents:
            intent_prompt += "Ask the student to start by providing a guess or explain their intuition of the problem.\n"
        if Intent.P_ARTICULATION in intents:
            intent_prompt += "Ask the student to write their intuition mathematically or detail their answer.\n"
        if Intent.P_REFLECTION in intents:
            intent_prompt += "Step back and reflect on the solution. Ask to recapitulate and *briefly* underline more general implications and connections.\n"
        if Intent.P_CONNECTION in intents:
            intent_prompt += "Underline the implication of the answer in the context of the problem.\n"
        if Intent.S_SELFCORRECTION in intents:
            intent_prompt += "Make the student identify by themself the error in their answer.\n"
        if Intent.S_CORRECTION in intents:
            intent_prompt += "Correct the student's mistake by giving them a hint.\n"
        if Intent.S_STRATEGY in intents:
            intent_prompt += "Encourage and make the student find on their own what is the next step to solve the problem, for example by asking a question.\n"#"Encourage and make the student find on their own what is the next step to solve the problem by asking them what is the next step.\n"
        if Intent.S_HINT in intents:
            intent_prompt += "Give a hint to the student to help them find the next step. Do *not* provide the answer.\n"
        if Intent.S_SIMPLIFY in intents:
            intent_prompt += "Consider first a simpler version of the problem.\n"
        if Intent.S_STATE in intents:
            intent_prompt += "State the theorem or definition the student is asking about.\n"
        if Intent.S_OFFLOAD in intents:
            intent_prompt += "Correct and perform the numerical computation for the student.\n" # could include it, as done by a calculator...
        if Intent.A_CHALLENGE in intents:
            intent_prompt += "Maintain a sense of challenge.\n"
        if Intent.A_CONFIDENCE in intents:
            intent_prompt += "Bolster the student's confidence.\n"
        if Intent.A_CONTROL in intents:
            intent_prompt += "Promote a sense of control.\n"
        if Intent.A_CURIOUSITY in intents:
            intent_prompt += "Evoke curiosity.\n"
        if Intent.G_GREETINGS in intents:
            intent_prompt += "Say goodbye and end the conversation\n"
        if Intent.G_OTHER in intents:
            intent_prompt += ""

        if intent_prompt!="":
            if not Intent.S_CORRECTION in intents and not Intent.S_HINT in intents:
                intent_prompt += "Do *not* provide a direct hint.\n"
            if not Intent.S_CORRECTION in intents and not Intent.S_SELFCORRECTION in intents and not Intent.S_OFFLOAD in intents:
                intent_prompt += "Do *not* correct the student.\n"
            
            #intent_prompt = "Your intent is to:\n" + intent_prompt
            messages.append({"role": "system", "content": intent_prompt})
        #print("intent prompt:")
        #print(intent_prompt)
        return messages