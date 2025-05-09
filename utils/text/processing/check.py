import re

def has_latex_math(text: str) -> bool:
    patterns = [
        r'\$\$(.*?)\$\$',                          # $$...$$
        r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',    # $...$
        r'\\\[(.*?)\\\]',                          # \[...\]
        r'\\\((.*?)\\\)',                          # \(...\)
        r'\\begin\{.*?\}(.*?)\\end\{.*?\}'         # \begin{...}...\end{...}
    ]
    
    combined_pattern = '|'.join(patterns)
    return bool(re.search(combined_pattern, text, re.DOTALL))