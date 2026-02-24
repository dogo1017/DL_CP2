# file_handler.py
# Handles all reading and writing for the document
# Every function that touches the actual text file lives here
# Called by main.py to keep file logic separate from the menu logic

# Opens the file and returns the full contents as one string including word count lines
def read_document(file_path):
    file = open(file_path, "r")
    content = file.read()
    file.close()
    return content

# Reads the file and skips any lines that start with Word Count or Last Updated
# This gives back just the actual document text without the tracking info at the bottom
# Used whenever we need to count words or show numbered lines for editing
def get_clean_content(file_path):
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()

    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Word Count:") or stripped.startswith("Last Updated:"):
            continue
        clean_lines.append(line)

    # Join the kept lines back together and strip any trailing blank lines
    clean_text = "".join(clean_lines)
    clean_text = clean_text.rstrip()
    return clean_text

# Splits the content on spaces and returns the total number of words
def count_words(clean_content):
    words = clean_content.split()
    return len(words)

# Writes content directly to the file replacing whatever was there before
# Used by the edit line feature and the overwrite option
def write_clean_content(file_path, content):
    file = open(file_path, "w")
    file.write(content)
    file.close()

# Strips the old word count lines then rewrites the file with the new content added at the bottom
# This keeps the existing text and just tacks the new stuff onto the end
def add_content_to_document(file_path, new_content):
    clean_text = get_clean_content(file_path)
    file = open(file_path, "w")
    file.write(clean_text + "\n" + new_content)
    file.close()

# Strips the old word count and timestamp then writes a fresh one at the bottom of the file
# Keeping only one copy prevents the numbers from stacking up and throwing off the count
def update_document_info(file_path, word_count, timestamp):
    clean_text = get_clean_content(file_path)
    file = open(file_path, "w")
    file.write(clean_text)
    file.write("\n\nWord Count: " + str(word_count))
    file.write("\nLast Updated: " + timestamp + "\n")
    file.close()