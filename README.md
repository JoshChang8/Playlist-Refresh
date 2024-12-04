# Playlist Refresh ✨
> _Leveraging Baseten’s fast inference times to use generative AI to enhance a Spotify User’s playlist._


 # Introduction
**Playlist Refresh ✨** is a web app that elevates the way you experience and share your Spotify playlists. By combining the power of generative AI with creative design, this app transforms your playlists with custom names and visually striking cover photos.

This project highlights my implementation of Baseten's Truss framework to deploy custom open-source models on Hugging Face. I also used Baseten's library of open-source models, integrating them into the app through APIs.

---

# Motivation
After learning about Baseten's internship position for a Forward Deployed Engineer, I was eager to dive deeper into the company and its offerings. As I explored the role, I discovered that a key responsibility would involve working extensively with Baseten's Truss framework to help customers deploy their models effectively. To better understand the role and Baseten's technologies, I decided to undertake a hands-on project using the Truss framework.

When choosing the focus of my project, it felt natural to build upon one of my existing projects—my [Spotify Song Recommender](https://www.google.com/url?q=https://medium.com/@joshjc038/data-driven-music-exploration-building-a-spotify-song-recommender-5780cabfe194&sa=D&source=docs&ust=1733263896518963&usg=AOvVaw0QIP8q7Tp31xMzCoG5WNXs). Shifting the focus to generative AI, I aimed to enhance the user experience by generating creative and catchy playlist names and expressive cover art for playlists. This project allowed me to explore the potential of generative AI while showcasing the practical application of Baseten’s tools.

---

# Overview of Tools and Models Used

### Baseten Truss Framework with Qwen 2.5 3B LLM
The Baseten Truss framework was used to deploy [Qwen's 2.5 3B parameter](https://www.google.com/url?q=https://huggingface.co/Qwen/Qwen2.5-3B-Instruct&sa=D&source=docs&ust=1733263567238477&usg=AOvVaw2ekOPmX1P3RTPF-JX9HG7y) open-source language model from Hugging Face, which generates creative playlist name suggestions based on playlist song data. This feature draws inspiration from Spotify's curated playlist names.

### Baseten Model Library - SDXL Lightning
The [Stable Diffusion SDXL Lightning model](https://www.google.com/url?q=https://www.baseten.co/library/sdxl-lightning/&sa=D&source=docs&ust=1733264072013610&usg=AOvVaw0eiileQgJCqG3BxGKdyz-n), accessed via Baseten’s Model Library, was used to generate custom playlist cover art. Integration was straightforward, requiring only API calls, making it an efficient solution for generating expressive visuals.

> At [Keplar.io](https://keplar-site-redesign.webflow.io/), a SF startup where I was an ML engineer, I worked with generative image models like Stable Diffusion for product co-creation to help aid product designers in the concept design phase of products.

### Spotify Web API
The Spotify Web API was used to retrieve song and artist data from public playlists provided by the user. This information serves as the foundation for generating personalized playlist names.

### Streamlit Web App
A lightweight and user-friendly Python package, Streamlit was used to build the app's interactive interface. It allows users to input their playlist, view AI-generated playlist names, and see the resulting cover art seamlessly.

---

# Project Workflow

### Input Your Spotify Playlist
Provide a link to your public Spotify playlist. The app extracts song and artist details using the Spotify Web API.  
To ensure the program can read your playlist, the playlist link must be formatted as follows:  
`https://open.spotify.com/playlist/...`

### Generate Playlist Names
Leveraging a generative AI model (Qwen LLM deployed via Baseten Truss), the app analyzes the playlist to suggest creative, tailored names that resonate with the content of your music.  
You can regenerate options until you find the perfect match.

### Design Custom Playlist Cover
Using the selected name as inspiration, the app employs Stable Diffusion (SDXL Lightning from Baseten’s Model Library) to generate visually captivating and expressive cover art that represents your playlist.

---

# Key Takeaways

### Ease of Deployment with Truss Framework
The Truss framework offers a high-level abstraction for deploying models, providing flexibility without the constraints of pre-configured options like those in Baseten's Model Library.  
It simplifies the process of creating custom deployments while maintaining the ability to customize resources and configurations as needed.

### Understanding Compute Requirements
Through this project, I gained valuable insights into the compute resources required to run AI models effectively. While the API-based approach from Baseten’s Model Library was quick and simple, configuring resources with Truss involved some trial and error.  
Using Baseten's documentation was crucial in determining the appropriate setup to ensure optimal performance.

### Debugging and Workflow Challenges
During the deployment process, I encountered challenges with authentication. Initially, I wasn’t prompted for an API key when running `truss push`, which delayed progress.  
After troubleshooting, I discovered the necessary commands (`truss login` and `truss whoami`) to properly configure the API key and resolve the issue.  

This experience underscored the importance of understanding tool-specific workflows and debugging effectively.

---

# How to Run the Project on Your Local Machine

Follow these steps to set up and run the project on your local machine:

### 1. Clone the Repository
Clone the GitHub repository to your local machine and install the required Python packages:

```bash
git clone <repository_url>
cd <repository_folder>
pip install -r requirements.txt
```

### 2. Set Up Your Baseten Account
Create an account on [Baseten](https://baseten.co/).
Use Baseten’s documentation to deploy your own model using the Truss framework.
Alternatively, leverage Baseten’s pre-deployed Qwen 2.5B parameter model available in their Model Library.

### 3. Deploy the SDXL Lightning Model
Deploy the Stable Diffusion SDXL Lightning model from Baseten’s Model Library by following the documentation provided on their platform.

### 4. Update API Credentials
Within the codebase, update the code with your personal API credentials:

Spotify API:
Obtain your Spotify API credentials by creating a developer account at [Spotify Developer](https://developer.spotify.com/).

Baseten API:
Use the API key provided in your Baseten account settings.


### 5. Run the Streamlit App
Launch the Streamlit app locally using the following command:
```bash
streamlit run deploy.py
```

### 6. Interact with the App
Open the provided local URL in your web browser to interact with the app.

Input a Spotify playlist to explore AI-generated playlist names.
Generate custom cover art for your playlist using the Stable Diffusion model.


