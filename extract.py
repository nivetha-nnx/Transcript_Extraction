import json  
transcripts = [] 

# Read the input file
with open("output.txt", "r", encoding="utf-8") as file:
    for line in file: 
        data = json.loads(line) 

        # Check if the message type is 'AddTranscript'
        if data.get("message") == "AddTranscript":
            
            # Get the transcript from metadata
            text = data.get("metadata", {}).get("transcript")
            
            # Store transcript text after removing extra spaces
            if text:
                transcripts.append(text.strip())

# Combine all transcripts into one string
final_transcript = " ".join(transcripts)

# Create a new text file and write the combined transcript
with open("combined_transcript.txt", "w", encoding="utf-8") as new_file:
    new_file.write(final_transcript)

print("New text file 'combined_transcript.txt' created with the final transcript.")
