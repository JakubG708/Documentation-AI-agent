import ollama
import os
from classes.agent import Agent
import re

def clean_latex_output(latex: str) -> str:
    latex = latex.strip()
    if latex.startswith("---latex"):
        latex = latex[len("---latex"):].lstrip()
    if latex.endswith("---"):
        latex = latex[:-len("---")].rstrip()

    latex = re.sub(r"^```(?:latex)?\s*", "", latex)
    latex = re.sub(r"\s*```$", "", latex)
    return latex

current_file = os.path.abspath(__file__)
with open(current_file, "r", encoding="utf-8") as f:
    code = f.read()

DEFAULT_MODEL = "deepseek-coder-v2"
TEMPERATURE = 0.1

generator = Agent(
    model_name="doc-generator-agent",
    model=DEFAULT_MODEL,
    system_prompt="""You are a tool for generating English documentation for provided code.
You generate concise documentation for classes, models, endpoints, functions, and scripts.
For each item, describe its purpose, inputs, outputs. Do not provide code, only names.
Return output in LaTeX format, wrapped in a full LaTeX document.
Use \\section{}, \\subsection{}, and wrap code blocks in \\begin{lstlisting} ... \\end{lstlisting}.
Document only real functional logic. Keep it minimal and clean. Omit comments, use only English characters.""",
    temperature=TEMPERATURE
)

formator = Agent(
    model_name="doc-formatter-agent",
    model=DEFAULT_MODEL,
    system_prompt="""You are a tool to format LaTeX documentation from another AI agent. Format should be: title, purpose, then sections.
Each class, model, endpoint, and function should get its own section.
Each section should have subsections with input, output, and short explanation.
If there is something other than names, for example code, omit it. Don't output anything other than LaTeX.""",
    temperature=TEMPERATURE
)

corrector = Agent(
    model_name="doc-corrector-agent",
    model=DEFAULT_MODEL,
    system_prompt="""You are a tool to analyze and check LaTeX from another AI agent.
Ensure there are no errors or AI artifacts like non-LaTeX text.
If you find issues, correct them. Output only valid LaTeX. Do not output anything like ---latex at the beginning.""",
    temperature=TEMPERATURE
)


doc_raw = generator.run(f"Generate documentation for the following code:\n\n{code}")
doc_formatted = formator.run(f"Format the following LaTeX:\n\n{doc_raw}")
doc_corrected = corrector.run(f"Correct the LaTeX:\n\n{doc_formatted}")

doc_clean = clean_latex_output(doc_corrected)


output_dir = os.path.join(os.path.dirname(current_file), "output")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "documentation_output.tex")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(doc_clean)

print(f"Documentation saved to: {output_path}")
