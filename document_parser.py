from docx import Document
import json
import re

doc = Document("sample_BRD.docx")

sections = {
    "Features": [],
    "Modules": [],
    "UserStories": [],
    "Issues": []
}

current_section = None

for para in doc.paragraphs:
    text = para.text.strip()

    if not text:
        continue

    lower = text.lower()

    # Detect sections
    if "functional requirements" in lower:
        current_section = "Features"

    elif "architecture overview" in lower:
        current_section = "Modules"

    elif "risks" in lower or "constraints" in lower:
        current_section = "Issues"

    # Extract user story style lines
    if re.match(r"FR\d+", text):
        sections["UserStories"].append(text)

    # Store content
    if current_section == "Features":
        sections["Features"].append(text)

    elif current_section == "Modules":
        sections["Modules"].append(text)

    elif current_section == "Issues":
        sections["Issues"].append(text)

# Convert lists to single text block
final_dict = {k: "\n".join(v) for k, v in sections.items()}

# Save JSON
with open("parsed_brd.json", "w") as f:
    json.dump(final_dict, f, indent=4)

print("JSON saved successfully")