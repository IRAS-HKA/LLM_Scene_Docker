import ollama




class OllamaInteraction:

    def getObjectFromScene(role, prompt):
        return ollama.chat(model='mistral-nemo', messages=[
                {
                    'role': role,
                    'content': prompt,
                    'options': {"seed": 123},
                    "context": [],
                },
        ])
        
    def getGeneratedObjectFromScene(prompt):
        response = ollama.generate(model='mistral-nemo', prompt=prompt)
        print("RESPONSE", response["response"])
        return response["response"]