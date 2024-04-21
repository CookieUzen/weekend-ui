import streamlit as st
import time

# Loading status bar
with st.status("Loading", expanded=True, state="running") as status:
    # Task 1
    progress_text = "Loading model"
    my_bar = st.progress(0, text=progress_text)

    # Replace with model loading function
    for percent_complete in range(100):
        time.sleep(0.01)
        # increment the progress bar
        my_bar.progress(percent_complete + 1, text=progress_text)

    # Delay before bar disappears
    # time.sleep(1)
    # my_bar.empty()

    # Task 2
    progress_text = "Making Predictions"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)

    time.sleep(1)
    status.update(label="Done!", state="complete", expanded=False)
