import json
import os
from pathlib import Path

from src.cli.config import TRANSLATE_DIR, TRANSLATE_FILE_TEMPLATE
from src.core.enum.language import LanguageEnum


def read_translate_file(lang: LanguageEnum) -> dict:
    language_code = lang.name
    translate_dir = Path(TRANSLATE_DIR)
    translate_file_path = translate_dir / f"{language_code}.json"
    if not os.path.exists(translate_file_path):
        raise FileNotFoundError(f"{translate_file_path}")
    with open(translate_file_path) as translate_file:
        translate_file_content = json.load(translate_file)
    return translate_file_content


def create_translate_file(lang: LanguageEnum) -> str:
    language_code = lang.name
    translate_dir = Path(TRANSLATE_DIR)
    translate_file_path = translate_dir / f"{language_code}.json"
    if os.path.exists(translate_file_path):
        raise FileExistsError(f"{translate_file_path}")
    template_path = Path(TRANSLATE_FILE_TEMPLATE)
    with open(template_path) as template_file:
        template_json = json.load(template_file)
    with open(translate_file_path, "w") as translate_file:
        json.dump(template_json, translate_file)
    return str(template_path)


def write_block_translate_file(block: str, lang: LanguageEnum, content: dict):
    language_code = lang.name
    translate_dir = Path(TRANSLATE_DIR)
    translate_file_path = translate_dir / f"{language_code}.json"
    with open(translate_file_path) as translate_file:
        translate_file_content = json.load(translate_file)
    translate_file_content[block] = content
    with open(translate_file_path, "w") as translate_file:
        json.dump(translate_file_content, translate_file, ensure_ascii=False, indent=4)
