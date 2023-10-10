#!/usr/bin/env python3

import os
import re
import json
import subprocess

import openai
from rich.console import Console

# Azure OpenAI API
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_BASE")
openai.api_version = os.getenv("AZURE_OPENAI_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
model = "gpt-35-turbo"

console = Console()

def generate_commit_message(diff_output):
    print("\nGenerating commit message...")

    prompt = (f"""You are a git commit message writer. Please write a concise git commit message after carefully reviewing the "git diff --staged" output. Only include the changes made and nothing else. Commit message output format:

    ```
    <type> (<changed file>): <message>
    ```

    You can choose any type from options like "improvement", "feat," "fix," "chore," "docs," "refactor," "style," "test," "perf," "build," "ci," "revert," "improvement," "security," "breaking," etc.

    The <changed file> should be the name of the modified file, and <message> should be your brief interpretation of the git diff. Keep it concise.

    Diff: <<<{diff_output}>>>""")

    res = openai.ChatCompletion.create(
        engine=model,
        max_tokens=3000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )
    return res['choices'][0]['message']['content']

def remove_quotes(string):
    if string.startswith("'") or string.startswith('"'):
        string = string[1:]
    if string.endswith("'") or string.endswith('"'):
        string = string[:-1]
    return string

def get_diff_output():
    return subprocess.check_output(["git", "diff", "--staged"]).decode()

def get_git_status_output():
    return subprocess.check_output(["git", "status"]).decode()

def get_unstaged_files():
    return subprocess.check_output(["git", "status", "--short"]).decode().strip().split('\n')

def print_unstaged_files(unstaged_files):
    console.print("\nUnstaged files:", style="bold white")
    for file in unstaged_files:
        console.print(file.strip(), style="bold Magenta")

def stage_all_files():
    subprocess.run(["git", "add", "."])

def commit_changes(message):
    subprocess.run(["git", "commit", "-m", f"""{message}"""])

def push_changes():
    subprocess.run(["git", "push"])

def main():
    try:
        diff_output = get_diff_output()

        if not diff_output.strip():
            git_status_output = get_git_status_output()

            if "nothing to commit, working tree clean" in git_status_output:
                ahead_pattern = re.compile(r"Your branch is ahead of 'origin/main' by (\d+) commit")
                match = ahead_pattern.search(git_status_output)
                if match:
                    console.print("\nWorking tree clean.\nYour branch is ahead of 'origin/main' by {} commit(s).".format(match.group(1)))

                    push = console.input("\n[bold]Would you like to [blue]push[/blue] to the remote repository? (y/n)[/bold]\n\[y]: ") or "y"
                    if push.lower() == "y":
                        push_changes()

                else:
                    console.print(git_status_output)
            else:
                unstaged_files = get_unstaged_files()
                print_unstaged_files(unstaged_files)

                stage_all = console.input("\n[bold]Would you like to [blue]add[/blue] all files to be staged? (y/n)[/bold]\n\[y]: ") or "y"
                if stage_all.lower() == "y":
                    stage_all_files()
                    diff_output = get_diff_output()

        if diff_output.strip():
            message = generate_commit_message(diff_output)
            message = remove_quotes(message)

            while True:
                console.print(message, style="bold green")

                commit = console.input(f"\n[bold]Would you like to [blue]commit[/blue] the changes? (y/n/re)\n\[y]: ") or "y"

                if commit.lower() == "y":
                    commit_changes(message)

                    push = console.input("\n[bold]Would you like to [blue]push[/blue] to the remote repository? (y/n)[/bold]\n\[y]: ") or "y"
                    if push.lower() == "y":
                        push_changes()
                    break
                elif commit.lower() == "re":
                    message = generate_commit_message(diff_output)
                    message = remove_quotes(message)
                else:
                    break
    except KeyboardInterrupt:
        console.print("\n\nOperation cancelled", style="bold yellow")

if __name__ == "__main__":
    main()