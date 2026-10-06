import json
import os
from litellm import completion

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- 1. VERIFY GEMINI API KEY ---
if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it or add it to a .env file.")

# 2. Automatically find and load the document structure file
json_path = "results/document_structure.json" if os.path.exists("results/document_structure.json") else "document_structure.json"
with open(json_path, "r", encoding="utf-8") as f:
    tree = json.load(f)

# 3. Strip heavy text for the structural reasoning phase
def extract_metadata(node):
    clean = {"node_id": node.get("node_id"), "title": node.get("title")}
    if "nodes" in node:
        clean["nodes"] = [extract_metadata(child) for child in node["nodes"]]
    return clean

def ask_ai(query):
    # Step A: Ask Gemini which section to read
    prompt = f"""You are analyzing a document tree structure to answer a user's question.
    Question: {query}
    Tree: {json.dumps(extract_metadata(tree))}
    Reply ONLY with a comma-separated list of relevant node_ids (e.g., node_1, node_3)."""

    response = completion(
        model="gemini/gemini-1.5-pro-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    target_ids = [n.strip() for n in response.choices[0].message.content.split(",")]

    # Step B: Extract only the targeted text sections
    def get_text(targets, node):
        text = ""
        if node.get("node_id") in targets:
            text += f"\nSection: {node.get('title')}\n{node.get('text', '')}\n"
        for child in node.get("nodes", []):
            text += get_text(targets, child)
        return text

    context = get_text(target_ids, tree)

    # Step C: Answer the question using only the retrieved legal fine print
    final_prompt = f"""You are a helpful consumer advocate. Using ONLY this text from the user's credit card guide, answer their question.
    Context:
    {context}

    Question: {query}"""

    final_response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"role": "user", "content": final_prompt}]
    )
    return final_response.choices[0].message.content

# --- 4. TEST QUESTION ---
my_question = "I dropped my new phone and shattered the screen. Am I covered?"

print("\nThinking with Gemini...\n")
print(ask_ai(my_question))