# OpenAI GPT Interaction Tools

This repository contains a set of Python tools designed to interact with OpenAI's GPT models. It aims to provide a structured and extensible codebase for building applications that leverage the powerful capabilities of GPT.

## Features

- **ToolManager**: A central manager that facilitates the discovery and execution of various tools within the project.
- **GptTool**: Responsible for communicating with the OpenAI GPT API.
- **ExecTool**: Executes Python code within a safe sandbox environment.
- **ShellTool**: Allows executing shell commands.
- **SnapTool**: Provides a snapshot of the current project's code for debugging or state transfer.
- **PipelineTool, FileTool**: Additional tools for more complex workflows and file operations.

## Testing

Testing is a crucial part of the project, ensuring the reliability and stability of the tools provided. The tests are written using the `pytest` framework, which allows for clean and concise test code.

## CI/CD Pipeline with GitHub Actions

The repository includes a CI/CD pipeline implemented using GitHub Actions. The pipeline automates the process of running tests and deploying the code when changes are pushed or a pull request is made.

## Usage

Before running the project, make sure to install all the required dependencies:

```bash
pip install -r requirements.txt
```

To execute the tools:

```bash
python main.py "<your prompt>"
```

Use the testing framework by executing:

```bash
pytest
```

## Contributing

If you're interested in contributing to this project, please feel free to open an issue or submit a pull request. Contributors are encouraged to follow the existing code structure and include tests for new features.

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy building with OpenAI GPT models!