import difflib

# A dictionary of your commands and their descriptions
commands = {
    "create-note": "Create a new note in the system.",
    "list-notes": "List all existing notes.",
    "delete-note": "Remove a note by its ID."
}

def search_commands(query):
    # Find keys in the dictionary that match the query
    matches = difflib.get_close_matches(query, commands.keys(), n=3, cutoff=0.3)
    if matches:
        print(f"Did you mean: {', '.join(matches)}?")
    else:
        print("No matching commands found.")
