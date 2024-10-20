import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptAvailable, TranscriptsDisabled, NoTranscriptFound
import sys
import traceback
import requests

def get_transcript_info(video_id):
    try:
        # First, let's check if the video exists
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}")
        if response.status_code != 200:
            return None, [], f"Video not found or not accessible. Status code: {response.status_code}"

        # Now, let's try to get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript, ["en"], None  # Assuming English transcript
    except NoTranscriptAvailable:
        return None, [], "No transcript available for this video."
    except TranscriptsDisabled:
        return None, [], "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return None, [], "No transcript found for this video."
    except Exception as e:
        return None, [], f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"

def main():
    st.title("YouTube Transcript Debugger V6")

    st.write(f"Python version: {sys.version}")

    video_id = st.text_input("Enter YouTube Video ID:", value="")
    
    if st.button("Get Transcript"):
        st.write(f"Attempting to fetch transcript for video ID: {video_id}")
        
        transcript, available_languages, error = get_transcript_info(video_id)
        
        if transcript:
            st.success("Transcript fetched successfully!")
            st.subheader("Available Languages:")
            st.write(", ".join(available_languages))
            st.subheader("Transcript (first 500 characters):")
            full_transcript = ' '.join(entry['text'] for entry in transcript)
            st.text(full_transcript[:500] + "..." if len(full_transcript) > 500 else full_transcript)
        else:
            st.error("Failed to fetch transcript")
            st.subheader("Error details:")
            st.text(error)

        st.subheader("Debug Information:")
        st.json({
            "video_id": video_id,
            "transcript_length": len(full_transcript) if transcript else 0,
            "available_languages": available_languages,
            "error": error if error else "None"
        })

if __name__ == "__main__":
    main()