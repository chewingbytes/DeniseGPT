import re

# Define regex patterns for each language
LANGUAGE_PATTERNS = {
    'python': {
        'class': re.compile(r'^\s*class\s+(\w+)\s*(\(|:|$)'),  # Match Python class definition
        'function': re.compile(r'^\s*def\s+(\w+)\s*\((.*?)\)'),  # Match Python function definition with parameters
        'variable': re.compile(r'^\s*(\w+)\s*=\s*(.*)'),  # Match Python variable assignments
    },
    'javascript': {
        'class': re.compile(r'^\s*class\s+(\w+)\s*\{'),  # Match JS class definition
        'function': re.compile(r'^\s*(async\s+)?function\s+(\w+)\s*\((.*?)\)'),  # Match JS function and async function definitions with parameters
        'variable': re.compile(r'^\s*(const|let|var)\s+(\w+)\s*=\s*(.*)'),  # Match JS variable assignments
    },
    'typescript': {
        'class': re.compile(r'^\s*class\s+(\w+)\s*\{'),  # Match TS class definition
        'function': re.compile(r'^\s*(async\s+)?\w+\s+(\w+)\s*\((.*?)\)'),  # Match TS function and async function definitions with parameters
        'variable': re.compile(r'^\s*(const|let|var)\s+(\w+)\s*:\s*\w+\s*=\s*(.*)'),  # Match TS variable assignments
    },
    'java': {
        'class': re.compile(r'^\s*(public|private|protected)?\s*class\s+(\w+)\s*{'),  # Match Java class definition
        'function': re.compile(r'^\s*(public|private|protected)?\s*(\w+)\s+(\w+)\s*\((.*?)\)'),  # Match Java method definition with parameters
        'variable': re.compile(r'^\s*(public|private|protected)?\s*(static\s+)?(\w+)\s+(\w+)\s*=\s*(.*)'),  # Match Java variable assignments
    },
    'c': {
        'function': re.compile(r'^\s*(\w+\s*\**\w+)\s*\((.*?)\)'),  # Match C function definition with parameters
        'variable': re.compile(r'^\s*(\w+\s*\**\w+)\s+(\w+)\s*=\s*(.*)'),  # Match C variable assignments
    },
    'mjs': {
        'class': re.compile(r'^\s*class\s+(\w+)\s*\{'),  # Match .mjs class definition
        'function': re.compile(r'^\s*(async\s+)?function\s+(\w+)\s*\((.*?)\)'),  # Match .mjs function and async function definitions with parameters
        'variable': re.compile(r'^\s*(const|let)\s+(\w+)\s*=\s*(.*)'),  # Match .mjs variable assignments
    }
}

# Function to process each file line by line and extract classes, functions, and variables
async def parse_code(file_path, language, file_content):
    if language not in LANGUAGE_PATTERNS:
        raise ValueError(f"Language {language} is not supported.")

    patterns = LANGUAGE_PATTERNS[language]
    definitions = {
        'file_path': file_path,
        'classes': [],
        'functions': [],
        'variables': []
    }

    lines = file_content.splitlines()
    
    for line_no, line in enumerate(lines, start=1):
        # Check for class definitions
        if 'class' in patterns and (match := patterns['class'].match(line)):
            class_name = match.group(1)
            definitions['classes'].append((line_no, class_name, line.strip()))

        # Check for function definitions
        if 'function' in patterns and (match := patterns['function'].match(line)):
            function_name = match.group(1)  # Function name is group 2
            definitions['functions'].append((line_no, function_name, line.strip()))

        # Check for variable assignments
        if 'variable' in patterns and (match := patterns['variable'].match(line)):
            variable_name = match.group(1)  
            definitions['variables'].append((line_no, variable_name, line.strip()))

    # Return None if no classes, functions, or variables are found
    if not definitions['classes'] and not definitions['functions'] and not definitions['variables']:
        print(None)
        return None

    print(definitions)
    return definitions
