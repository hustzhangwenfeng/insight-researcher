import markdown
from .logs import PROJECT_ROOT
from pathlib import Path


def write_report_to_file(task_id: str, text: str) -> None:
    path = Path(PROJECT_ROOT / "outputs/")
    path.mkdir(parents=True, exist_ok=True)
    filename = str(path / task_id)
    # Convert text to UTF-8, replacing any problematic characters
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')
    with open(f'{filename}.md', "w", encoding='utf-8') as file:
        file.write(text_utf8)

    html = markdown.markdown(text_utf8)
    with open(f'{filename}.html', 'w', encoding='utf-8') as file:
        file.write(html)