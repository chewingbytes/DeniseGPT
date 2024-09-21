IGNORE_EXTENSIONS = [
    ".jpg", ".png", ".mp3", ".mp4", ".pdf", ".zip", ".tar", ".exe", ".dll", ".bin", ".obj", ".o",
    ".log", ".tmp", ".bak", ".doc", ".docx", ".xls", ".xlsx"
]

IGNORE_FOLDERS = [
    "node_modules", "dist", "build", "out", ".git", ".svn", ".hg", "venv", "__pycache__",
    "target", ".gradle", ".idea", ".vscode", "test", "tests", "logs", "coverage", ".cache"
]

IGNORE_FILES = [
    "package-lock.json", "yarn.lock", "composer.lock", "Thumbs.db", ".DS_Store", "desktop.ini",
    "Pipfile.lock", "Cargo.lock", ".gitignore", ".gitattributes"
]

file_types = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".go": "go",
    ".rb": "ruby",
    ".rs": "rust",
    ".php": "php",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".xml": "xml",
    ".lua": "lua",
    ".h": "c", 
    ".hpp": "cpp",
    ".m": "objective-c",
    ".swift": "swift",
    ".sh": "bash",
    ".sql": "sql",
    ".r": "r",
    ".scss": "scss",  
    ".jsx": "jsx",
    ".tsx": "tsx",  
    ".md": "markdown",
    ".yaml": "yaml",
    ".toml": "toml",
}