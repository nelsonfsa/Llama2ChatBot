from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json


template = """
Answer the question below.

Heres the conversation history: {context}

Question: {question}

Answer:

"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def get_data():

    context = ""
    #Load messages
    with open('messages.json', 'r') as f:
        messages = json.load(f)

    context_to_learn = ""
    for i, message in enumerate(messages):
        context_to_learn += json.dumps(message) + "\n"
        print(f"working on message: {i}/{len(messages)}")
        if (i + 1) % 20 == 0:
            context += chain.invoke({"context": "messages:" + context_to_learn, "question": "Learn this"})

    return context    

def handle_conversation():

    context = ""
    print("Welcome, type 'exit to quit")
    while True: 
        user_input = input("You: ")
        if user_input == "exit":
            break

        result = chain.invoke({"context" : context, "question" : user_input})
        print("Ollama: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()

def answer_question(question):
    result = chain.invoke({"context" : "", "question" : question})
    return result


