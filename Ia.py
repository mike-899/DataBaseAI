import torch
import ollama
import os
from openai import OpenAI
import argparse

settingsInput = input("Ingresas: a=texto b=voz c=simbolos:  ").lower()
settingsOutput = input("Sale: a=texto b=voz c=simbolos:      ").lower()

if settingsInput == "a":
    from VARS import PINK, CYAN, YELLOW, NEON_GREEN, RESET_COLOR
elif settingsInput == "b":
    from VAT import *
elif settingsInput == "c":
    from SAT import *
elif settingsInput == "ab" or settingsInput == "ba":
    from VAT import *
else:
    from VAT import *
    from SAT import *

if settingsOutput == "a":
    pass
elif settingsOutput == "b":
    from TAV import *
elif settingsOutput == "c":
    from SAT import *
elif settingsOutput == "ab" or settingsOutput == "ba":
    from TAV import *
else:
    from TAV import *
    from SAT import *

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to get relevant context from the vault based on user input
def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the rewritten input
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context



# Function to interact with the Ollama model
def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    # Get relevant context from the vault
    relevant_context = get_relevant_context(user_input, vault_embeddings_tensor, vault_content, top_k=3)
    if relevant_context:
        # Convert list to a single string with newlines between items
        context_str = "\n".join(relevant_context)
        print("Context Pulled from Documents: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "No relevant context found." + RESET_COLOR)
    
    # Prepare the user's input by concatenating it with the relevant context
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = context_str + "\n\n" + user_input
    
    # Append the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input_with_context})
    
    # Create a message history including the system message and the conversation history
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    # Send the completion request to the Ollama model
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages
    )
    
    # Append the model's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    # Return the content of the response from the model
    return response.choices[0].message.content

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="llama3.1", help="Ollama model to use (default: llama3.1)")
args = parser.parse_args()

# Configuration for the Ollama API client
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3.1'
)

# Load the vault content
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

# Generate embeddings for the vault content using Ollama
vault_embeddings = []
for content in vault_content:
    response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
    vault_embeddings.append(response["embedding"])

# Convert to tensor and print embeddings
vault_embeddings_tensor = torch.tensor(vault_embeddings) 
print("Embeddings for each line in the vault:")
print(vault_embeddings_tensor)

# Conversation loop
conversation_history = []
system_message = "Tu eres una Genial Inteligencia Artificial tu objetivo es dar respuestas claras y simples beneficiando a la compania deberas ofrecer combos y mas."

while True:
    if settingsInput == "a":
        user_input = input(YELLOW+"Pregunta: "+RESET_COLOR).lower()
        if user_input == 'quit':
            break
    elif settingsInput == "b":
        grabar_audio()
        user_input = transcribir_audio().lower()
        if user_input == 'quit':
            break
    elif settingsInput == "c":
        pass
    elif settingsInput == "ab" or settingsInput == "ba":
        ToV = input("Texto(T) o voz(V):")
        if ToV == "T":
            user_input = input(YELLOW+"Pregunta: hya"+RESET_COLOR).lower()
        else:
            grabar_audio()
            user_input = transcribir_audio().lower()
        if user_input == 'quit':
            break
    else:
        pass

    response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history)

    if settingsOutput == "a":
        print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)
    elif settingsOutput == "b":
        texto_voz(response)
        reproducir_audio(respuesta_archivo)
    elif settingsOutput == "c":
        pass
    elif settingsOutput == "ab" or settingsOutput == "ba":
        texto_voz(response)
        reproducir_audio(respuesta_archivo)

        print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)
    else:
        texto_voz(response)
        reproducir_audio(respuesta_archivo)

        print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)
    
