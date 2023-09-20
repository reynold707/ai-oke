import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import time

# Set page config to wide layout
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Create two columns for layout
col1, col2 = st.columns([2, 3])

# Title and description in Column 1
with col1:
    st.title("AI-Oke, AI Supported Karaoke")
    st.write("Enter a YouTube video URL to extract and display captions.")
    
    # Input field for the YouTube URL in Column 1
    video_url = st.text_input("Enter YouTube Video URL:", "https://www.youtube.com/watch?v=fJ9rUzIMcZQ")

    # Button to trigger caption extraction in Column 1
    if st.button("Extract Captions"):
        # Function to extract and display captions
        try:
            # Get the video captions
            video_id = video_url.split("?v=")[1]
            captions = YouTubeTranscriptApi.get_transcript(video_id)

            # Display the current time ticker at the top
            with col1:
                video = YouTube(video_url)
                total_time = video.length
                current_time = st.empty()
                current_caption = st.empty()  # Initialize with an empty string

            # Display the embedded video in Column 2
            with col2:
                st.video(video_url)

            # Display captions at the correct time in Column 1
            with col1:
                start_time = 0
                current_caption_index = 0
                for caption in captions:
                    caption_start = caption['start']
                    caption_end = caption_start + caption['duration']

                    # Update the current time ticker
                    while start_time <= caption_start:
                        current_time.text(f"Current Time: {start_time:.2f} seconds")
                        time.sleep(1)  # Sleep for 1 second to update the time
                        start_time += 1

                    # Update the current caption text when its time comes
                    current_caption.text(caption['text'])

                    # Check if the next caption starts within 10 seconds
                    if current_caption_index < len(captions) - 1:
                        next_caption_start = captions[current_caption_index + 1]['start']
                        if next_caption_start - caption_start <= 10:
                            current_caption.text(f"Next Caption: {captions[current_caption_index + 1]['text']}")
                        else:
                            current_caption.text("")
                    else:
                        current_caption.text("")

                    current_caption_index += 1

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.write("Built with ❤️ by De La Montagne")
st.write("Disclaimer: All rights with original owners.")
