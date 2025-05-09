from datetime import datetime
import re


def generate_file_name(prompt: str) -> str:
    clean_prompt = re.sub(r'[^\w\s-]', '', prompt)[:25].strip().replace(' ', '_')
    time_part = datetime.now().strftime("%H%M%S")
    return f"{clean_prompt}_{time_part}"