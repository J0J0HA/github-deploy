import argparse
import os
import pathlib
import shutil
import prompt_toolkit

# This will have a `init` command which will generate a workflow file, add a config file, add the config file to the .gitignore file, and commit the changes
# This will have a `serve` command which will start the internal wsgi server with a webhook endpoint /deploy

def init(args):
    installation = pathlib.Path(__file__).parent.resolve()
    
    filename = args.ghwfilename or prompt_toolkit.prompt("Enter the name of the config file: ")
    name = args.ghwfilename or prompt_toolkit.prompt("Enter the name of the workflow: ")
    if os.path.exists(f".github/workflows/{filename}.yml"):
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
    parser.add_argument("--workflow-file", "-w", dest="ghwfilename", default=None, required=False, help="Filename of the workflow file")
    parser.add_argument("--workflow-name", "-n", dest="ghwname", default=None, required=False, help="Filename of the workflow file")
    args = parser.parse_args()
    if args.command == "init":
        init(args)
    elif args.command == "serve":
        serve(args.args)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()