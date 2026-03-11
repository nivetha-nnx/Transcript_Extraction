import json
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

input_file = "output.txt"
output_file = "combined_transcript.txt"

current_sentence = ""
current_start_time = None
sentences = []

def append_text(current, new_text, attaches_to):
    """Append text depending on attaches_to"""
    if attaches_to == "previous":
        # No space if attaching to previous
        return current.rstrip() + new_text
    else:
        # Add space if not attaching
        return (current + " " + new_text).strip() if current else new_text

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)

        if data.get("message") != "AddTranscript":
            continue

        metadata = data.get("metadata", {})
        text = metadata.get("transcript", "").strip()
        start_time = metadata.get("start_time", 0)

        # Check if attaches_to exists in any of the results
        attaches_to = None
        if "results" in data and data["results"]:
            attaches_to = data["results"][-1].get("attaches_to")

        if not text:
            continue

        if current_start_time is None:
            current_start_time = start_time

        # Append text properly based on attaches_to
        current_sentence = append_text(current_sentence, text, attaches_to)

        # Split sentences only if needed (optional, can remove if you want raw concatenation)
        split_sentences = sent_tokenize(current_sentence)
        if len(split_sentences) > 1:
            for s in split_sentences[:-1]:
                sentences.append(f"{current_start_time:.2f}  {s.strip()}")
            current_sentence = split_sentences[-1]
            current_start_time = start_time

# Add last sentence
if current_sentence:
    sentences.append(f"{current_start_time:.2f}  {current_sentence.strip()}")

# Write to output
with open(output_file, "w", encoding="utf-8") as f:
    for s in sentences:
        f.write(s + "\n")

print("Transcript updated in text file.")
