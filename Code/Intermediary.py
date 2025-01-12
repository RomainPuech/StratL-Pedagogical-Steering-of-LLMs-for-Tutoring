# By Romain Puech
import PromptGenerator
import IntentSelector
import Assessor
from taxonomy import Intent

class Intermediary():
    def __init__(self,client,model,assessor = None, intentSelector=None,promptGenerator = None,intent_history = [],assessment_history=[]) -> None:
        self.client = client
        self.model = model

        self.assessor = Assessor.Assessor(self.client,self.model,assessment_history = assessment_history) if assessor is None else assessor
        self.intentSelector = IntentSelector.IntentSelector(intent_history=intent_history) if intentSelector is None else intentSelector
        self.promptGenerator = PromptGenerator.RigidPromptGenerator() if promptGenerator is None else promptGenerator

    def update_client(self,client):
        self.client = client
        self.assessor.client = client
        self.intentSelector.client = client
        self.promptGenerator.client = client
            
    def update_model(self,model):
        self.model = model
        self.assessor.model = model
        self.intentSelector.model = model
        self.promptGenerator.model = model

    def get_prompt(self,pb,sol,student_messages,tutor_messages,open=True):
        #print("generating tutor's prompt...")
        assessment,assessor_prompt_tokens,assessor_completion_tokens = self.assessor.assess(pb,sol,student_messages,tutor_messages)
        intent = self.intentSelector.get_intent(assessment,open=open)
        prompt = self.promptGenerator.get_prompt(pb,sol,student_messages,tutor_messages,intent)
        return prompt,intent,assessment,assessor_prompt_tokens,assessor_completion_tokens
    
class EmptyIntermediary(Intermediary):
    def get_prompt(self, pb, sol, student_messages, tutor_messages, open=True):
        #print("generating tutor's prompt...")
        prompt = self.promptGenerator.get_prompt(pb,sol,student_messages,tutor_messages,[])
        return prompt,[],[],0,0

class NextStepIntermediary(Intermediary):
    def __init__(self,client,model,assessor = None, intentSelector=None,promptGenerator = None,intent_history = [],assessment_history=[]) -> None:
        self.client = client
        self.model = model

        self.assessor = Assessor.Assessor(self.client,self.model,assessment_history = assessment_history) if assessor is None else assessor
        self.intentSelector = IntentSelector.StrategyIntentSelector(intent_history=intent_history) if intentSelector is None else intentSelector
        self.promptGenerator = PromptGenerator.RigidPromptGenerator() if promptGenerator is None else promptGenerator

class LLMIntermediary(Intermediary):
    def __init__(self,client,model,assessor = None, intentSelector=None,promptGenerator = None,intent_history = [],assessment_history=[]) -> None:
        self.client = client
        self.model = model

        self.assessor = Assessor.Assessor(self.client,self.model,assessment_history = assessment_history) if assessor is None else assessor
        self.intentSelector = IntentSelector.LLMIntentSelector(client,intent_history=intent_history) if intentSelector is None else intentSelector
        self.promptGenerator = PromptGenerator.RigidPromptGenerator() if promptGenerator is None else promptGenerator


class FlexibleIntermediary(Intermediary):
    def __init__(self,client,model,assessor = None, intentSelector=None,promptGenerator = None,intent_history = [],assessment_history=[]) -> None:
        self.client = client
        self.model = model

        self.assessor = Assessor.Assessor(self.client,self.model,assessment_history = assessment_history) if assessor is None else assessor
        self.intentSelector = IntentSelector.IntentSelector(intent_history=intent_history) if intentSelector is None else intentSelector
        self.promptGenerator = PromptGenerator.FlexiblePromptGenerator() if promptGenerator is None else promptGenerator
