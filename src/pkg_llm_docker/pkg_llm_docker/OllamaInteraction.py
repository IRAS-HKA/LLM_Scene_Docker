import ollama

# Using this class to interact with Ollama API
# Its possible to get an object from a scene or generate an object from a prompt
# Generating is deterministic and chat is non-deterministic
# Generation is used for the command feature, otherwise the given format is unparseable most of the time

# Change the model by download it the Dockerfile and change the model name in the function calls
class OllamaInteraction:

    # Chat functionality with Ollama API
    def getObjectFromScene(role, prompt):
        return ollama.chat(model='mistral-nemo', messages=[
                {
                    'role': role,
                    'content': prompt,
                    'options': {"seed": 123},
                    "context": [],
                },
        ])
    
    # Generation functionality with Ollama API
    def getGeneratedObjectFromScene(prompt):
        response = ollama.generate(model='mistral-nemo', prompt=prompt)
        print("RESPONSE", response["response"])
        return response["response"]