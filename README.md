# Woosong University Student Chatbot

A friendly and helpful AI chatbot designed to assist international students at Woosong University.

## Features

*   **Conversational Interface:** Uses Streamlit to provide a user-friendly chat interface.
*   **AI-Powered Responses:** Leverages Google's Gemini API (gemini-1.5-flash model) to understand questions and generate helpful answers about campus life, academics, facilities, and more.
*   **Conversation History:** Stores chat history using SQLite for context retention within a session.
*   **Environment Variable Management:** Uses `python-dotenv` to securely manage the Gemini API key.
*   **Optimized Package Management:** Uses `uv` for fast dependency installation.

## Tech Stack

*   **Language:** Python 3.10
*   **Web Framework:** Streamlit
*   **AI Model:** Google Gemini API (gemini-1.5-flash)
*   **Database:** SQLite
*   **Package Management:** uv, pip
*   **Environment Variables:** python-dotenv

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KHJKHJKKKHHHJJJ/Woosong-Helper.git
    cd Woosong-Helper
    ```

2.  **Create and activate a virtual environment:** (Using Python 3.10 recommended)
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

3.  **Install dependencies using uv:**
    ```bash
    pip install uv # Install uv if you haven't already
    uv pip install -r requirements.txt
    ```
    *(Alternatively, use `pip install -r requirements.txt`)*

4.  **Set up environment variables:**
    *   Create a file named `.env` in the project root directory.
    *   Add your Gemini API key to the `.env` file:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
    *   Replace `"YOUR_API_KEY_HERE"` with your actual Google Gemini API key.

## How to Run

Make sure your virtual environment is activated.

```bash
streamlit run app.py
```

Or alternatively:

```bash
python -m streamlit run app.py
```

Open your web browser and navigate to the local URL provided (usually `http://localhost:8501`).

## Environment Variables

*   `GEMINI_API_KEY`: **Required.** Your API key for accessing the Google Gemini API. 