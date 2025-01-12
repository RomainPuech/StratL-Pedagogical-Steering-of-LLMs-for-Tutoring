from openai import AzureOpenAI
from openai import OpenAI

def get_key():
    with open('./key.txt', 'r') as f:
        return tuple(map(str.strip,f.readlines()))
    
def get_client():
    api_key,api_version,azure_endpoint = get_key()
    client = AzureOpenAI(
    api_key = api_key,  
    api_version = api_version,
    azure_endpoint = azure_endpoint
    )
    return client
    

#### New API key using OpenAi ####

def get_key_openAI():
    with open('./key_openAI.txt', 'r') as f:
        return str(f.readline().strip())
    
def get_client_openAI():
    api_key = get_key_openAI()
    client = OpenAI(
    api_key= api_key
    )
    return client
    