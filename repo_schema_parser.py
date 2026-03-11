import os
import json
from tree_sitter import Language, Parser
import tree_sitter_python

PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser(PY_LANGUAGE)


def get_text(node, source):
    return source[node.start_byte:node.end_byte].decode("utf8")


# -----------------------------
# IMPORTS
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
# FUNCTION CALLS
# -----------------------------
def extract_calls(node, source):

    calls = []

    def walk(n):

        if n.type == "call":

            func = n.child_by_field_name("function")

            if func:
                calls.append(get_text(func, source))

        for child in n.children:
            walk(child)

    walk(node)

    return calls


# -----------------------------
# DECORATORS
# -----------------------------
def extract_decorators(node, source):

    decorators = []

    for child in node.children:

        if child.type == "decorated_definition":

            for sub in child.children:

                if sub.type == "decorator":
                    decorators.append(get_text(sub, source))

    return decorators


# -----------------------------
# DOCSTRING
# -----------------------------
def extract_docstring(body_node, source):

    if body_node and body_node.children:

        first = body_node.children[0]

        if first.type == "expression_statement":
            text = get_text(first, source)

            if text.startswith(("\"", "'")):
                return text

    return None


# -----------------------------
# FUNCTIONS
# -----------------------------
def extract_functions(root, source):

    functions = []

    def walk(node):

        if node.type == "function_definition":

            name_node = node.child_by_field_name("name")
            body_node = node.child_by_field_name("body")

            functions.append({
                "name": get_text(name_node, source),
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "docstring": extract_docstring(body_node, source),
                "calls": extract_calls(node, source)
            })

        for child in node.children:
            walk(child)

    walk(root)

    return functions


# -----------------------------
# CLASSES
# -----------------------------
def extract_classes(root, source):

    classes = []

    def walk(node):

        if node.type == "class_definition":

            name_node = node.child_by_field_name("name")
            body_node = node.child_by_field_name("body")

            # inheritance
            bases = []
            for child in node.children:
                if child.type == "argument_list":
                    bases.append(get_text(child, source))

            classes.append({
                "name": get_text(name_node, source),
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "docstring": extract_docstring(body_node, source),
                "inherits": bases
            })

        for child in node.children:
            walk(child)

    walk(root)

    return classes


# -----------------------------
# FILE PARSER
# -----------------------------
def parse_python_file(file_path):

    with open(file_path, "rb") as f:
        source = f.read()

    tree = parser.parse(source)
    root = tree.root_node

    data = {
        "file": file_path,
        "imports": extract_imports(root, source),
        "classes": extract_classes(root, source),
        "functions": extract_functions(root, source),
    }

    return data


# -----------------------------
# REPOSITORY PARSER
# -----------------------------
def parse_repo(repo_path):

    repo_data = {
        "repository": repo_path,
        "files": []
    }

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                try:

                    parsed = parse_python_file(path)

                    repo_data["files"].append(parsed)

                except Exception as e:

                    print("Error parsing", path, e)

    return repo_data


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    repo_path = "C:\projects\Ask-docs"

    graph_data = parse_repo(repo_path)

    with open("repo_knowledge_graph.json", "w") as f:
        json.dump(graph_data, f, indent=4)

    print("Knowledge graph extraction complete")