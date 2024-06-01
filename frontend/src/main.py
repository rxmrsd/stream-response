"""main.py"""
import time
from typing import Generator

import requests
import streamlit as st


URL = "http://localhost:8000/run_stream"


def main() -> None:
    st.title("Streaming Response")

    prompt = st.text_input("Prompt", "What is baseball?")

    if st.button("Send"):
        data = {
            "message": prompt,
        }

        response = requests.post(
            url=URL,
            params=data,
            headers={'accept': 'application/json'},
            stream=True,
        )

        if response.status_code == 200:
            st.write_stream(stream_data(response.text))
        else:
            st.error(f"Error: {response.status_code}")


def stream_data(data: str) -> Generator[str, None, None]:
    for word in data:
        yield word
        time.sleep(0.02)


if __name__ == "__main__":
    main()
