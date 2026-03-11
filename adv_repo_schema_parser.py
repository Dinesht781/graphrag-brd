import os
import json
import fnmatch
from tree_sitter import Language, Parser
import tree_sitter_python

# -----------------------------
# Tree-sitter setup
# -----------------------------
PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser(PY_LANGUAGE)


# -----------------------------
# Default ignore patterns
# -----------------------------
DEFAULT_IGNORE = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build"
}


# -----------------------------
# Load .kgignore
# -----------------------------
def load_ignore(repo_path):

    ignore_file = os.path.join(repo_path, ".kgignore")

    patterns = set(DEFAULT_IGNORE)

    if os.path.exists(ignore_file):

        with open(ignore_file) as f:

            for line in f:
                line = line.strip()

                if line and not line.startswith("#"):
                    patterns.add(line)

    return patterns


# -----------------------------
# Ignore logic
# -----------------------------
def should_ignore(path, patterns):

    for pattern in patterns:

        if fnmatch.fnmatch(path, pattern) or pattern in path:
            return True

    return False


# -----------------------------
# Helper
# -----------------------------
def get_text(node, source):

    return source[node.start_byte:node.end_byte].decode("utf8")


# -----------------------------
# Extract imports
# -----------------------------
def extract_imports(root, source):

    imports = []

    for node in root.children:

        if node.type == "import_statement":
            imports.append(get_text(node, source))

        if node.type == "import_from_statement":
            imports.append(get_text(node, source))

    return imports


# -----------------------------
# Extract function calls
# -----------------------------
def extract_calls(node, source):

    calls = []

    def walk(n):

        if n.type == "call":

            func = n.child_by_field_name("function")

            if func:
                calls.append(get_text(func, source))

        for c in n.children:
            walk(c)

    walk(node)

    return calls


# -----------------------------
# Extract methods inside class
# -----------------------------
def extract_methods(class_node, source):

    methods = []

    for child in class_node.walk():

        if child.type == "function_definition":

            name_node = child.child_by_field_name("name")

            methods.append({
                "name": get_text(name_node, source),
                "start_line": child.start_point[0] + 1,
                "end_line": child.end_point[0] + 1,
                "calls": extract_calls(child, source)
            })

    return methods


# -----------------------------
# Extract classes
# -----------------------------
def extract_classes(root, source):

    classes = []

    def walk(node):

        if node.type == "class_definition":

            name_node = node.child_by_field_name("name")

            methods = []

            body = node.child_by_field_name("body")

            if body:

                for child in body.children:

                    if child.type == "function_definition":

                        name = child.child_by_field_name("name")

                        methods.append({
                            "name": get_text(name, source),
                            "start_line": child.start_point[0] + 1,
                            "end_line": child.end_point[0] + 1,
                            "calls": extract_calls(child, source)
                        })

            classes.append({
                "name": get_text(name_node, source),
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "methods": methods
            })

        for child in node.children:
            walk(child)

    walk(root)

    return classes


# -----------------------------
# Extract standalone functions
# -----------------------------
def extract_functions(root, source):

    functions = []

    for node in root.children:

        if node.type == "function_definition":

            name_node = node.child_by_field_name("name")

            functions.append({
                "name": get_text(name_node, source),
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "calls": extract_calls(node, source)
            })

    return functions


# -----------------------------
# Parse single file
# -----------------------------
def parse_python_file(file_path):

    with open(file_path, "rb") as f:
        source = f.read()

    tree = parser.parse(source)

    root = tree.root_node

    return {

        "file": file_path,

        "imports": extract_imports(root, source),

        "classes": extract_classes(root, source),

        "functions": extract_functions(root, source)
    }


# -----------------------------
# Parse repository
# -----------------------------
def parse_repository(repo_path):

    ignore_patterns = load_ignore(repo_path)

    graph = {
        "repository": repo_path,
        "directories": [],
        "files": []
    }

    for root, dirs, files in os.walk(repo_path):

        # remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]

        graph["directories"].append(root)

        for file in files:

            if not file.endswith(".py"):
                continue

            if should_ignore(file, ignore_patterns):
                continue

            path = os.path.join(root, file)

            try:

                parsed = parse_python_file(path)

                graph["files"].append(parsed)

            except Exception as e:

                print("Error parsing:", path, e)

    return graph


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    repo_path = "C:\projects\Ask-docs"

    graph_data = parse_repository(repo_path)

    with open("adv_repo_kg.json", "w") as f:
        json.dump(graph_data, f, indent=4)

    print("Repository knowledge graph extracted")