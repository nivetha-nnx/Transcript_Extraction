import json

transcripts = []

with open("output.txt", "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)

        if data.get("message") == "AddTranscript":
            text = data.get("metadata", {}).get("transcript")
            if text:
                transcripts.append(text.strip())

final_transcript = " ".join(transcripts)

print(final_transcript)