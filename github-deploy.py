import argparse
import os
import pathlib
import shutil
import time
import prompt_toolkit as pt


class YesNoValidator(pt.validation.Validator):
    DICT = {
        "y": True,
        "yes": True,
        "true": True,
        "n": False,
        "no": False,
        "false": False,
    }

    def __init__(self, accept_empty=False):
        self.accept_empty = accept_empty

    def validate(self, document):
        text = document.text

        if text:
            if text.lower() in self.DICT.keys():
                return
            raise pt.validation.ValidationError(
                message="The input must be one of: " + ", ".join(self.DICT.keys()),
                cursor_position=0,
            )
        elif not self.accept_empty:
            raise pt.validation.ValidationError(
                message="The input must not be empty", cursor_position=0
            )


class FileNameValidator(pt.validation.Validator):
    def __init__(self, extension="", assert_exists=None, directory=""):
        self.extension = extension
        self.assert_exists = assert_exists
        self.directory = directory

    def validate(self, document):
        text = document.text

        if text:
            if not text.endswith(self.extension):
                raise pt.validation.ValidationError(
                message="The filename must have the following extension: " + self.extension,
                cursor_position=len(text) -1,
            )
            if self.assert_exists is not None and (os.path.exists(f"{self.directory}{text}") is not self.assert_exists):
                    raise pt.validation.ValidationError(
                        message=f"The file must {'not ' if not self.assert_exists else ''}exist.", cursor_position=0
                    )
        else:
            raise pt.validation.ValidationError(
                message="The filename must not be empty.", cursor_position=0
            )


def init(args):
    installation = pathlib.Path(__file__).parent.resolve()
    pts = pt.PromptSession()
    style = pt.styles.Style.from_dict(
        {
            "": "#ffffff", # Default (White)
            "t": "#00FFE7", # Turquoise
            "g": "#23FF00", # Green
            "r": "#D52200", # Red
            "lg": "#565656", # Light Gray
        }
    )

    _ = pts.prompt(
        [
            (
                "class:t",
                "Do you already have a deployment workflow file you would like to add the deploy job to?",
            ),
            ("", " "),
            ("class:lg", "["),
            ("class:g", "y"),
            ("class:lg", "/"),
            ("class:r", "n"),
            ("class:lg", "]"),
            ("", " "),
        ],
        validator=YesNoValidator(),
        validate_while_typing=True,
        style=style,
    )
    add_to_existing = YesNoValidator().DICT[_]
    filename = pts.prompt(
        [
            (
                "class:t",
                "Enter the name of the workflow file:",
            ),
            ("", " "),
            ("class:lg", ".github/workflows/"),
        ],
        style=style,
        validator=FileNameValidator(".yml", assert_exists=add_to_existing, directory=".github/workflows/"),
        validate_while_typing=True,
    )
    if not add_to_existing:
        name = pts.prompt("Enter the name of the workflow: ")
        if os.path.exists(f".github/workflows/{filename}"):
            raise Exception("Workflow file already exists")
    if not os.path.exists(".github"):
        os.mkdir(".github")
    if not os.path.exists(".github/workflows"):
        os.mkdir(".github/workflows")
    with open(installation / "workflow.yml", "r", encoding="UTF-8") as ff:
        with open(f".github/workflows/{filename}.yml", "w", encoding="UTF-8") as wf:
            wf.write(ff.read().format(name=name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["init", "serve"], help="The command to run")
    args = parser.parse_args()
    if args.command == "init":
        init(args)
    elif args.command == "serve":
        serve(args.args)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
