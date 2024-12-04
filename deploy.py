import requests
import os
import spotipy
import json
import base64
import streamlit as st
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotipy with SpotifyClientCredentials
SPOTIFY_CLIENT_ID = "<SPOTIFY_CLIENT_ID>"
SPOTIFY_CLIENT_SECRET = "<SPOTIFY_CLIENT_SECRET>"
CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

def find_playlist_tracks(playlist_uri: str) -> str:
    """
    Retrieve tracks from a Spotify playlist and display them in Streamlit df.

    Args:
        playlist_uri (str): The URI of the Spotify playlist.

    Returns:
        str: JSON string of the playlist tracks.
    """
    playlist_tracks = sp.playlist_tracks(playlist_uri)

    # Generate JSON
    playlist_json = [
        {
            "song_name": item["track"]["name"],
            "artist": ", ".join(
                [artist["name"] for artist in item["track"]["artists"]]
            ),
        }
        for item in playlist_tracks["items"]
    ]

    # Convert JSON to string
    json_string = json.dumps(playlist_json, indent=2)

    # Display dataframe
    playlist_df = pd.DataFrame(playlist_json)
    playlist_df.columns = ["Song Name", "Artist"]
    with st.expander("Checkout Your Playlist Songs"):
        st.dataframe(playlist_df.style.hide(axis="index"), use_container_width=True)

    return json_string


def create_prompt(playlist_tracks: str) -> str:
    """
    Create a prompt for generating playlist names based on the given playlist tracks.

    Args:
        playlist_tracks (str): JSON string of the playlist tracks.

    Returns:
        str: Formatted prompt string.
    """
    prompt_1 = "Can you suggest creative and catchy names for this playlist that captures its feelings, emotions, and overall mood? Use clever wordplay, puns, or literary techniques like alliteration or metaphors to make it unique and memorable. The name should be general enough to fit all the songs in the playlist, not tied to any specific song."

    prompt_2 = """
    ONLY respond with 3 playlist name suggestions in JSON format. Do not provide any explanations, commentary, or additional text. Use this exact structure for your response:

    ```json
    {
    "playlist_name_1": "",
    "playlist_name_2": "",
    "playlist_name_3": ""
    }
    """
    final_prompt = f""" Here is the playlist data in JSON format: {playlist_tracks}

    {prompt_1}

    {prompt_2} """

    return final_prompt


def fetch_playlist_names(prompt: str) -> dict:
    """
    Fetch playlist name suggestions from the Baseten API using given prompt.

    Args:
        prompt (str): The prompt string to send to the API.

    Returns:
        dict: JSON response containing playlist name suggestions.
    """
    BASETEN_API_KEY = "<BASETEN_API_KEY>"

    system_prompt = "You are a seasoned expert in the music industry, deeply knowledgeable about all genres of music. Your role is to provide thoughtful, accurate, and creative advice and answers related to music. You approach every inquiry with a passion for music, creativity, and a dedication to enriching the musical knowledge and experience of your audience."

    # Qwen 2.5 3B Truss Model Deployment 
    # resp = requests.post(
    # "<ENDPOINT_URL>",
    # headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
    # json={'text': f"{prompt}"},
    # )

    # Baseten Model Library Qwen 2.5 3B Instruct
    resp = requests.post(
        "<ENDPOINT_URL>",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json={
            "stream": True,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 256,
            "temperature": 0.9,
        },
    )

    print(f"Raw response text: {resp.text}")
    print(f"HTTP status code: {resp.status_code}")

    cleaned_str = resp.text.replace("```json\n", "").replace("```", "").strip()

    try:
        playlist_json_data = json.loads(cleaned_str)
        print(playlist_json_data)
        return playlist_json_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def generate_playlist_names(playlist_tracks: str) -> str:
    """
    Generate playlist name suggestions using the provided playlist tracks.

    Args:
        playlist_tracks (str): JSON string of the playlist tracks.

    Returns:
        str: Selected playlist name.
    """
    prompt = create_prompt(playlist_tracks)

    # Initialize session state for playlist names
    if "playlist_names" not in st.session_state:
        with st.spinner("Fetching playlist name suggestions..."):
            st.session_state["playlist_names"] = fetch_playlist_names(prompt)

    # Check if API response is valid
    if not st.session_state["playlist_names"]:
        st.error("Failed to fetch playlist names. Please try again.")
        return None

    st.write("Choose a Playlist Name")
    col1, col2, col3 = st.columns(3)
    selected_option = None
    try:
        with col1:
            if st.button(st.session_state["playlist_names"]["playlist_name_1"]):
                selected_option = st.session_state["playlist_names"]["playlist_name_1"]

        with col2:
            if st.button(st.session_state["playlist_names"]["playlist_name_2"]):
                selected_option = st.session_state["playlist_names"]["playlist_name_2"]

        with col3:
            if st.button(st.session_state["playlist_names"]["playlist_name_3"]):
                selected_option = st.session_state["playlist_names"]["playlist_name_3"]

    except KeyError as e:
        st.error(f"Invalid response format: Missing {e}")
        return None

    if st.button("Regenerate Responses"):
        with st.spinner("Regenerating playlist names..."):
            st.session_state["playlist_names"] = fetch_playlist_names(prompt)
        st.experimental_rerun()

    if selected_option:
        st.session_state["selected_playlist_name"] = selected_option
        st.success(f"You selected: {selected_option}")

    return selected_option


def generate_cover_image(playlist_name: str) -> None:
    """
    Generate a cover image for the given playlist name using the Baseten API.

    Args:
        playlist_name (str): The name of the playlist.

    Returns:
        None
    """
    BASETEN_API_KEY = "<BASETEN_API_KEY>"

    with st.spinner("Generating cover image..."):
        try:
            # Baseten model library SDXL Lightning 
            res = requests.post(
                "<ENDPOINT_URL>",
                headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
                json={"prompt": f"{playlist_name}"},
            )
            st.write(playlist_name)
            # Ensure the response is valid
            if res.status_code == 200:
                res = res.json()
                img_b64 = res.get("result")

                # Check if the result exists
                if img_b64:
                    img = base64.b64decode(img_b64)
                    st.image(img, caption=playlist_name, use_column_width=True)
                else:
                    st.error("No image was generated. Please try again.")
            else:
                st.error(
                    f"Failed to generate the image. Status code: {res.status_code}"
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Main
st.set_page_config(page_title="Playlist Refresh", page_icon="✨")
st.markdown("# Playlist Refresh ✨")
st.sidebar.header("Playlist Parameters")

playlist = ""

# User inputs public link to playlist
with st.sidebar.form(key="Form1"):
    playlist = st.text_input("Enter Playlist Link")
    submitted_playlist = st.form_submit_button(label="Find Playlist 🔎")
    st.write(
        "To make sure the program can read your playlist, please input the playlist link in this format:"
    )
    st.text("https://open.spotify.com/playlist/...")
    st.write(
        "Playlist links in this format can be found through Spotify web and desktop app, NOT the mobile app"
    )
    st.write(
        "Provided is a sample link to run a playlist analysis: https://open.spotify.com/playlist/51mwSPAk0bqVFM4Lz0IXZ1?si=f6f564a6cc564c89"
    )

if playlist == "":
    st.write(
        """
    This app transforms your Spotify playlists into personalized masterpieces by helping you craft the perfect name and custom cover photo. Here's how it works:
    """
    )

    st.markdown(
        """
        #### 1. Import Your Playlist
        Paste a link to your **public Spotify playlist** in the left sidebar under *Playlist Parameters*.

        #### 2. Generate Creative Playlist Names
        Using generative AI, the app suggests unique and imaginative playlist names that perfectly match the mood and theme of your music.

        #### 3. Choose the Perfect Name
        Browse through the suggestions, select the one that resonates with you, or regenerate new options until you find the ideal fit.

        #### 4. Create a Custom Playlist Cover Photo
        Once you've chosen a name, the app generates a stunning cover photo to visually represent your playlist.
        """
    )
    st.warning("Please input a valid playlist link to analyze.")


else:
    playlist_uri = playlist[34:56]

    # Print playlist name and list songs
    playlist_info = sp.playlist(playlist_uri)
    playlist_name = playlist_info["name"]
    st.write("### " + playlist_info["name"] + " Playlist Refresh")
    playlist_tracks = find_playlist_tracks(playlist_uri)
    st.divider()

    # Playlist Name Recommendations
    st.write("### Playlist Name Recommendations")
    playlist_name = generate_playlist_names(playlist_tracks)
    st.divider()

    # Generate Playlist Cover Photo
    st.write("### Generate Playlist Cover Image")

    if "selected_playlist_name" in st.session_state:
        # Add a button to trigger the image generation
        if st.button("Generate Image"):
            generate_cover_image(st.session_state["selected_playlist_name"])
    else:
        st.warning("Please select a playlist name first.")
