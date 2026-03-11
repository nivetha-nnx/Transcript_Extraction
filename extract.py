import json
 
def parse_transcript(input_file, output_file):
    tokens = []  # List of dicts: {content, start_time, attaches_to, is_eos, type}
 
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
 
            if data.get("message") != "AddTranscript":
                continue
 
            results = data.get("results", [])
            if not results:
                continue
 
            for result in results:
                alt = result.get("alternatives", [{}])[0]
                content = alt.get("content", "")
                if not content:
                    continue
 
                token = {
                    "content": content,
                    "start_time": result.get("start_time", 0.0),
                    "end_time": result.get("end_time", 0.0),
                    "attaches_to": result.get("attaches_to", None),
                    "is_eos": result.get("is_eos", False),
                    "type": result.get("type", "word"),
                    "speaker": alt.get("speaker", ""),
                }
                tokens.append(token)
 
    # Build sentences
    sentences = []       
    current_sentence = None
 
    for token in tokens:
        content = token["content"]
        attaches = token["attaches_to"] == "previous"
        is_eos = token["is_eos"]
        start_time = token["start_time"]
 
        # Start a new sentence if there's none yet
        if current_sentence is None:
            current_sentence = {"start_time": start_time, "parts": []}
 
        if attaches:
            # No space before this token — attach directly to previous
            current_sentence["parts"].append(content)
        else:
            if current_sentence["parts"]:
                current_sentence["parts"].append(" " + content)
            else:
                current_sentence["parts"].append(content)
 
        # If end-of-sentence punctuation, close and save the sentence
        if is_eos:
            sentences.append(current_sentence)
            current_sentence = None
 
    # Any remaining tokens not closed by EOS
    if current_sentence and current_sentence["parts"]:
        sentences.append(current_sentence)
 
    # Write output
    with open(output_file, "w") as out:
        for sentence in sentences:
            start = sentence["start_time"]
            text = "".join(sentence["parts"])
            out.write(f"{start:.2f} {text}\n")
 
    print(f"Done! {len(sentences)} sentences written to '{output_file}'")
 
if __name__ == "__main__":
    input_file = "output.txt"
    output_file = "combined_transcript.txt"

    parse_transcript(input_file, output_file)
