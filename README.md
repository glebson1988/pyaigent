# PyAIgent - AI Coding Agent

A powerful AI-driven coding agent built with Google Gemini 2.0 Flash that can autonomously interact with codebases, analyze code, fix bugs, and execute Python programs.

## Features

PyAIgent is designed as a true "agent" with a feedback loop that allows it to:

- **Analyze codebases** by reading files and understanding project structure
- **Execute Python code** and analyze outputs
- **Fix bugs** by modifying source code
- **Create new files** and directory structures
- **Iteratively solve complex problems** through multi-step reasoning

### Core Capabilities

1. **File System Operations**
   - List files and directories with size information
   - Read file contents (up to 10,000 characters per file)
   - Write and overwrite files with automatic directory creation

2. **Code Execution**
   - Execute Python files with timeout protection (30 seconds)
   - Capture both stdout and stderr
   - Report exit codes for debugging

3. **Intelligent Agent Loop**
   - Up to 20 iterations per task to prevent infinite loops
   - Maintains conversation context between iterations
   - Automatically stops when task is completed

4. **Security Features**
   - All operations are sandboxed to the `./calculator` directory
   - Path traversal protection
   - Input validation and error handling

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pyaigent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

### Basic Command Structure

```bash
python main.py "your prompt here" [--verbose]
```

### Command Line Options

- `--verbose`: Enable detailed logging showing function calls, token usage, and iteration details

### Example Commands

#### 1. Code Analysis
```bash
# Analyze how a function works
python main.py "explain how the calculator renders results to the console"

# Understand project structure
python main.py "read the files in the current directory and explain the project structure"

# Analyze specific functionality
python main.py "how does the calculator handle operator precedence?"
```

#### 2. Bug Detection and Fixing
```bash
# Fix mathematical bugs
python main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"

# Debug execution issues
python main.py "the calculator app outputs wrong results, find and fix the bug"

# Fix syntax or logic errors
python main.py "there's an error in the calculator code, please fix it"
```

#### 3. Code Development
```bash
# Add new features
python main.py "add support for parentheses in mathematical expressions"

# Create new functionality
python main.py "create a function to validate mathematical expressions before evaluation"

# Refactor code
python main.py "improve the error handling in the calculator"
```

#### 4. Testing and Validation
```bash
# Run tests
python main.py "run the tests and fix any failing ones"

# Create test cases
python main.py "create comprehensive tests for the calculator functionality"

# Validate specific scenarios
python main.py "test the calculator with complex expressions and edge cases"
```

#### 5. Documentation and Code Review
```bash
# Generate documentation
python main.py "add detailed comments to the calculator code"

# Code review
python main.py "review the code for potential improvements and best practices"

# Create examples
python main.py "create example usage scenarios for the calculator"
```

### Verbose Mode Examples

Use `--verbose` flag to see detailed execution:

```bash
# See step-by-step execution
python main.py "fix the calculator bug" --verbose

# Monitor token usage and function calls
python main.py "analyze the render function" --verbose
```

Example verbose output:
```
User prompt: fix the calculator bug

--- Iteration 1 ---
Prompt tokens: 338
Response tokens: 76
 - Calling function: get_files_info
-> {'result': '- README.md: file_size=12 bytes, is_dir=False\n...'}

--- Iteration 2 ---
Prompt tokens: 517
Response tokens: 47
 - Calling function: get_file_content
-> {'result': 'class Calculator:\n    def __init__(self):\n...'}

Final response:
I have fixed the operator precedence bug in the calculator...
```

## How It Works

### Agent Architecture

PyAIgent implements a feedback loop architecture:

1. **User Input**: Receives a natural language prompt
2. **LLM Processing**: Uses Google Gemini 2.0 Flash to understand the request
3. **Function Calling**: Executes appropriate functions based on the task
4. **Context Maintenance**: Keeps conversation history for multi-step reasoning
5. **Iteration**: Continues until task completion or maximum iterations reached

### Available Functions

The agent has access to four core functions:

#### `get_files_info(directory)`
Lists files and directories with metadata:
```python
# Lists files in current directory
get_files_info(".")

# Lists files in subdirectory
get_files_info("pkg")
```

#### `get_file_content(file_path)`
Reads and returns file contents:
```python
# Read a Python file
get_file_content("main.py")

# Read a configuration file
get_file_content("config.json")
```

#### `run_python_file(file_path)`
Executes Python files and captures output:
```python
# Run the main calculator
run_python_file("main.py")

# Execute tests
run_python_file("tests.py")
```

#### `write_file(file_path, content)`
Creates or overwrites files:
```python
# Create a new Python file
write_file("new_feature.py", "def new_function():\n    pass")

# Fix an existing file
write_file("calculator.py", updated_code)
```

## Working Directory

All operations are constrained to the `./calculator` directory for security. The agent can:

- Read any file within the calculator directory
- Execute Python files in the calculator directory
- Create new files and directories within the calculator directory
- Cannot access files outside this sandbox

## Error Handling

The agent includes robust error handling:

- **File not found**: Clear error messages for missing files
- **Permission errors**: Graceful handling of access issues
- **Execution timeouts**: 30-second timeout for Python execution
- **Invalid paths**: Prevention of directory traversal attacks
- **API limits**: Graceful handling of rate limits and quotas

## Limitations

- **Working Directory**: Limited to `./calculator` directory
- **File Size**: File reading limited to 10,000 characters
- **Execution Time**: Python execution timeout of 30 seconds
- **Iterations**: Maximum 20 iterations per task
- **Language**: Currently optimized for Python code

## Examples of Complex Tasks

### Bug Fixing Workflow
```bash
python main.py "the calculator gives wrong results for '3 + 7 * 2', investigate and fix"
```

This will typically:
1. List files to understand structure
2. Read calculator code
3. Identify the precedence bug
4. Fix the operator precedence
5. Test the fix
6. Confirm the correction

### Code Analysis Workflow
```bash
python main.py "explain how the calculator renders output with examples"
```

This will typically:
1. Explore the file structure
2. Read the main calculator file
3. Read the render module
4. Explain the rendering process
5. Provide examples of the output format

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Error: Please set GEMINI_API_KEY in your .env file
   ```

2. **Rate Limits**
   ```
   Error: 429 RESOURCE_EXHAUSTED
   ```
   Wait for the rate limit to reset (usually 1 minute)

3. **File Not Found**
   ```
   Error: File not found or is not a regular file
   ```
   Ensure the file exists in the calculator directory

### Getting Help

- Use `--verbose` flag to see detailed execution steps
- Check the error messages for specific issues
- Ensure your API key has sufficient quota
- Verify file paths are relative to the calculator directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details. 
