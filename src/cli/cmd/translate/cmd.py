import click

from src.cli.cmd.util import create_translate_file, read_translate_file, write_block_translate_file
from src.core.enum import LanguageEnum
from src.core.enum.base.translation import TranslationEnum


@click.group()
def translate():
    pass


def enum_block_check():
    block_name = "enum"
    click.secho(f"Update translate block {block_name}", fg="green", bold=True)
    translate_subcls_list = TranslationEnum.__subclasses__()
    error_msg_list = []
    for lang in LanguageEnum:
        click.secho("")
        try:
            content = read_translate_file(lang=lang)
            click.secho(f"Success read {lang.name}", fg="green", bold=True)
        except FileNotFoundError:
            created_path = create_translate_file(lang=lang)
            click.secho(f"Translate {lang.name} not found, created by path: {created_path}", fg="red", bold=True)
            content = read_translate_file(lang=lang)
        block = content.get(block_name, {})
        enum_names = [enum_cls.__name__ for enum_cls in translate_subcls_list]
        for enum_cls in translate_subcls_list:
            enum_cls_name = enum_cls.__name__
            enum_block = block.get(enum_cls_name, {})
            enum_cls_names = [_enum.name for _enum in enum_cls]
            for name in enum_cls_names:
                enum_name_translate = enum_block.get(name)
                if enum_name_translate is None:
                    enum_block[name] = None
                    msg = f"Detect empty value in {block_name}.{enum_cls_name}.{name}"
                    error_msg_list.append(msg)
                    click.secho(msg, fg="yellow", bold=True)
            delete_names = []
            for name in enum_block:
                if name in enum_cls_names:
                    continue
                delete_names.append(name)
                click.secho(f"Detect deleted lang in {enum_cls_name}.{name}, was removed", fg="red", bold=True)
            for name in delete_names:
                del enum_block[name]
            block[enum_cls_name] = enum_block
        delete_names = []
        for name in block:
            if name in enum_names:
                continue
            delete_names.append(name)
            click.secho(f"Detect deleted enum in {lang}.{block_name}.{name}, was removed", fg="red", bold=True)
        for name in delete_names:
            del block[name]
        write_block_translate_file(block=block_name, lang=lang, content=block)
    return error_msg_list


@translate.command()
def enum() -> list[str]:
    enum_block_check()


@translate.command()
def verify():
    click.secho("Boot translate verify", fg="green", bold=True)
    errors = []
    errors.extend(enum_block_check())
    if len(errors) != 0:
        click.secho("Translate errors found:", fg="red", bold=True)
        for err in errors:
            click.secho(err, fg="red", bold=True)
        exit(1)
    click.secho("Translate ok", fg="green", bold=True)
