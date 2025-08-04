import ollama
import os

current_file = os.path.abspath(__file__)

with open(current_file, "r", encoding="utf-8") as f:
    code = f.read()


model = ollama.create(model='deepseek-coder-v2', from_='deepseek-coder-v2', system = """You are a tool for generating eglish documentation for provided code.
You generate concise documentation for classes, models, endpoints, functions, and scripts.
For each item, describe its purpose, inputs, outputs, and provide a usage example.
Return output in LaTeX format, wrapped in a full LaTeX document.
Use \\section{}, \\subsection{}, and wrap code blocks in \\begin{lstlisting} ... \\end{lstlisting}.
Document only real functional logic. Keep it minimal and clean. if there are polish signs or any other language signs that arent standard for english, bypass them for example turn ć to c"""
)

response = ollama.chat(model='deepseek-coder-v2',
                        messages=[{"role": "user", "content": f"generate documentation for provided code, write just latex nothing else: \n\n{code}"}

    ] )

latex_content = response['message']['content']

base_dir = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(base_dir, "output")

os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "documentation_output.tex")

os.makedirs(output_dir, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(latex_content)

print(f" Dokumentacja zapisana do: {output_path}")


