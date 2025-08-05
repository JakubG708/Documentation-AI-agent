import ollama


class Agent:
    def __init__(self, model_name: str, model: str, system_prompt: str, temperature: float):
        self.model = model
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature

        existing_models = [m.model for m in ollama.list().models]

        if self.model_name not in existing_models:
            ollama.create(model=self.model_name, from_=self.model, system=self.system_prompt, parameters={"temperature": self.temperature})

        

    def run(self, prompt: str) -> str:
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response.get("response", "")
        except Exception as e:
            print(f"Error running prompt: {e}")
            return ""
        
    






    