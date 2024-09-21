import os
import networkx as nx

def rank_files_by_importance(G):
    """Rank files by importance using PageRank and return sorted list."""
    pagerank_scores = nx.pagerank(G)
    
    # Sort files by PageRank score in descending order
    sorted_files = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Format the output with numbering and new lines
    formatted_list = "\n".join([f"{i + 1}. {file}" for i, (file, _) in enumerate(sorted_files)])
    
    return formatted_list

def extract_dependencies(file_content, language_name):
    """Extract dependencies based on language type (e.g., imports, requires)."""
    dependencies = []
    
    if language_name == "python":
        # Extract Python imports
        for line in file_content.splitlines():
            if line.startswith('import') or line.startswith('from'):
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1])  # Extract the module name

    elif language_name == "javascript" or language_name == "typescript":
        # Extract JS/TS requires or imports
        for line in file_content.splitlines():
            if "require(" in line or "import " in line:
                parts = line.split()
                if 'from' in parts or 'require(' in parts:
                    # Extract module after 'from' or 'require('
                    module_name = parts[-1].strip().strip(';').strip('"').strip("'")
                    dependencies.append(module_name)
    
    elif language_name == "java":
        # Extract Java imports
        for line in file_content.splitlines():
            if line.startswith("import"):
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1].strip(";"))  # Remove semicolon if present

    elif language_name == "c" or language_name == "cpp":
        # Extract C/C++ includes
        for line in file_content.splitlines():
            if line.startswith("#include"):
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1].strip("<>").strip('"'))  # Extract the included file
    
    elif language_name == "php":
        # Extract PHP requires or includes
        for line in file_content.splitlines():
            if "require(" in line or "include(" in line:
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1].strip(';').strip('"').strip("'"))

    elif language_name == "ruby":
        # Extract Ruby requires
        for line in file_content.splitlines():
            if line.startswith("require"):
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1].strip('"').strip("'"))
    
    elif language_name == "go":
        # Extract Go imports
        in_import_block = False
        for line in file_content.splitlines():
            if line.startswith("import ("):
                in_import_block = True
            elif line.startswith(")"):
                in_import_block = False
            elif line.startswith("import"):
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1].strip('"'))
            elif in_import_block:
                # In import block, extract module names
                parts = line.split()
                if len(parts) > 0:
                    dependencies.append(parts[0].strip('"'))
    
    elif language_name == "swift":
        # Extract Swift imports
        for line in file_content.splitlines():
            if line.startswith("import"):
                parts = line.split()
                if len(parts) > 1:
                    dependencies.append(parts[1])
    
    # Add more language-specific dependency extraction logic as needed
    
    return dependencies
