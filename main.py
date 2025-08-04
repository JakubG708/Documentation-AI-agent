import ollama
import os

class Agent:
    def __init__(self, system_prompt, model="deepseek-coder-v2"):
        self.model = model
        self.system_prompt = system_prompt


    def run(self, user_input):
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
        )
        return response['message']['content']
    
class RandomClass:
    def __init__(self, somethingIdk):
        self.dunno = somethingIdk
    
    def do_thing(thing):
        return 1

current_file = os.path.abspath(__file__)
with open(current_file, "r", encoding="utf-8") as f:
    code = f.read()

generator = Agent(
    system_prompt="""You are a tool for generating English documentation for provided code.
You generate concise documentation for classes, models, endpoints, functions, and scripts.
For each item, describe its purpose, inputs, outputs. Do not provide code, only names.
Return output in LaTeX format, wrapped in a full LaTeX document.
Use \\section{}, \\subsection{}, and wrap code blocks in \\begin{lstlisting} ... \\end{lstlisting}.
Document only real functional logic. Keep it minimal and clean. Omit comments, use only English characters."""
)

formator = Agent(
    system_prompt="You are a tool to format LaTeX documentation from another AI agent. Format should be: title, purpose, than sections. each class, model, endpoint, function should get its own section. each section should have subsections with input, output, short explanation, if there is something other than names, for example code, ommit it. Don't output anything other than LaTeX."
)

corrector = Agent(
    system_prompt="You are a tool to analyze and check LaTeX from another AI agent. Ensure there are no errors or AI artifacts like non-LaTeX text. If you find issues, correct them. Output only valid LaTeX. dont output something like ---latex at the beggining"
)


doc_raw = generator.run(f"Generate documentation for the following code:\n\n{code}")
doc_formatted = formator.run(f"Format the following LaTeX:\n\n{doc_raw}")
doc_corrected = corrector.run(f"Correct the LaTeX:\n\n{doc_formatted}")


output_dir = os.path.join(os.path.dirname(current_file), "output")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "documentation_output.tex")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(doc_corrected)

print(f"Documentation saved to: {output_path}")
