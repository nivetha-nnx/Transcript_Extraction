import json
import re

input_file = "output.txt"
output_file = "combined_transcript.txt"

current_sentence = ""
current_start_time = None
sentences = []

sentence_end = {".", "?"}

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)

        if data.get("message") != "AddTranscript":
            continue

        metadata = data.get("metadata", {})
        text = metadata.get("transcript", "").strip()
        start_time = metadata.get("start_time", 0)
        attaches_to = metadata.get("attaches_to")

        if not text:
            continue

        # start new sentence timing
        if current_start_time is None:
            current_start_time = start_time

        # apply attaches_to rule
        if attaches_to == "previous":
            current_sentence += text
        else:
            if current_sentence:
                current_sentence += " " + text
            else:
                current_sentence = text

        # remove accidental spaces before punctuation
        current_sentence = re.sub(r"\s+([.,?])", r"\1", current_sentence)

        # break sentence
        if text in sentence_end:
            sentences.append(f"{current_start_time:.2f}  {current_sentence.strip()}")
            current_sentence = ""
            current_start_time = None

with open(output_file, "w", encoding="utf-8") as f:
    for s in sentences:
        f.write(s + "\n")

print("Transcript formatted successfully")
