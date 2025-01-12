# By Romain Puech
import Intermediary

class Tutor():

    def __init__(self,client,pb,sol,model="gpt-4o-2024-05-13",intermediary=None,intent_history = [],assessment_history=[],open=True, version="V1") -> None:
        #print("---")
        #print("Creating tutor...")
        #print("---")
        self.client = client
        self.model = model#"myGPT4"#model
        self.pb,self.sol = pb,sol
        self.open = open
        if not intermediary is None:
            self.intermediary = intermediary
        elif version == "V2":
            self.intermediary = Intermediary.EmptyIntermediary(client = self.client,model = self.model, intent_history = intent_history, assessment_history = assessment_history)
        elif version == "V3":
            self.intermediary = Intermediary.NextStepIntermediary(client = self.client,model = self.model, intent_history = intent_history, assessment_history = assessment_history)
        else:
            # notably if V1
            self.intermediary = Intermediary.Intermediary(client = self.client,model = self.model, intent_history = intent_history, assessment_history = assessment_history)

    def update_client(self,client):
        self.client = client
        self.intermediary.update_client(client)

    def update_model(self,model):
        self.model = model
        self.intermediary.update_model(model)
        

    def get_response(self,messages_student,messages_tutor,max_tokens=1500):
        #print("\n---")
        #print("tutor called using model ", self.model)
        prompt,intent,assessment,prompt_tokens,completion_tokens = self.intermediary.get_prompt(self.pb,self.sol,messages_student,messages_tutor,open=self.open)
        #prompt.append({"role": "system", "content": "Ask the student to find by themself a problem with their answer without giving any hint"})
        #print("prompt generated:")
        #print_logs(prompt)
        

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            max_tokens=max_tokens
        )
        response = completion.choices[0].message.content

        prompt_tokens += completion.usage.prompt_tokens
        completion_tokens += completion.usage.completion_tokens
        total_tokens = prompt_tokens + completion_tokens

        response = response.replace("\(","$").replace("\)","$").replace("\[","$$").replace("\]","$$")
        #print("tutor answers:")
        #print(response)
        #print("---")
        return response, total_tokens, prompt_tokens, completion_tokens, intent, assessment
    
    def get_response_stream(self,messages_student,messages_tutor,max_tokens=1500):
        #print("\n---")
        #print("tutor called using model ", self.model)
        prompt,intent,assessment,prompt_tokens,completion_tokens = self.intermediary.get_prompt(self.pb,self.sol,messages_student,messages_tutor,open=self.open)
        #prompt.append({"role": "system", "content": "Ask the student to find by themself a problem with their answer without giving any hint"})
        #print("prompt generated:")
        #print_logs(prompt)

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            max_tokens=max_tokens,
            stream=True,
        )
        #response = response.replace("\(","$").replace("\)","$").replace("\[","$$").replace("\]","$$")
        #print("tutor answers:")
        #print(response)
        #print("---")
        return stream, 0, 0, 0, intent, assessment