# azure-open-commit

A Python script that generates concise git commit messages by analyzing `git diff --staged` output. It uses Azure OpenAI's GPT-35-Turbo model for natural language generation.

## Prerequisites

- Python 3
- `git` command-line tool
- `openai` and `rich` Python libraries

## Setup

- Clone the repository
- Install required libraries

## Configuration

Set environment variables:

- `AZURE_OPENAI_BASE`
- `AZURE_OPENAI_VERSION`
- `AZURE_OPENAI_KEY`

## Usage

1. Run the script: `python3 main.py`.
2. Review the changes made (output of `git diff --staged`).
3. Carefully review the generated commit message and make any necessary adjustments.
4. Decide whether to commit the changes or not, and whether to push to the remote repository.

## Script Flow

1. Retrieves the diff of the staged changes using `git diff --staged`.
2. If there are no changes, checks the repository status and offers options accordingly.
3. If there are unstaged files, displays them and offers the option to stage all of them.
4. Generates a commit message using the GPT model by providing a prompt and the diff output.
5. Presents the generated commit message to the user and offers the option to commit or generate a new message.
6. Upon committing, offers the option to push the changes to the remote repository.

## License

This project is licensed under the MIT License.