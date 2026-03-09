import json

def load_transcript(file_path):
    """Load JSON lines from file"""
    data = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))

    return data

def format_transcript(data):
    formatted = ""
    sentence_start = True

    for item in data:

        if item.get("message") != "AddTranscript":
            continue

        metadata = item.get("metadata", {})
        transcript = metadata.get("transcript", "")
        start_time = metadata.get("start_time", "")

        results = item.get("results", [])
        attaches_to = ""

        if results and "attaches_to" in results[0]:
            attaches_to = results[0]["attaches_to"]

        # Add start time at beginning of sentence
        if sentence_start:
            formatted += f"{start_time:.2f} "
            sentence_start = False

        # punctuation attachment
        if attaches_to == "previous":
            formatted += transcript
        else:
            if formatted and not formatted.endswith("\n"):
                formatted += " "
            formatted += transcript

        # sentence break
        if transcript in [".", "?"]:
            formatted += "\n"
            sentence_start = True

    return formatted.strip()

def save_output(text, file):
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    input_file = "output.txt"
    output_file = "updated_combined_transcript.txt"

    data = load_transcript(input_file)

    formatted_text = format_transcript(data)

    save_output(formatted_text, output_file)

if __name__ == "__main__":
    main()
