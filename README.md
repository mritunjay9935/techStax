# GitHub Webhook Event Handler

This is a simple Flask application that listens for GitHub webhook events and stores them in a MongoDB database. It also provides an endpoint to fetch and display these events in a web interface.

## Prerequisites

- Python 3.8 or higher
- MongoDB
- Flask
- PyMongo
- ngrok

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/webhook-repo.git
    cd webhook-repo
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python main.py
    ```

The application will start running at `http://localhost:5000`.

## Using ngrok

1. Download and install ngrok from the [official website](https://ngrok.com/download).

2. Once you have ngrok installed, you can start your Flask application:

    ```bash
    python main.py
    ```

   Your application should now be running at `http://localhost:5000`.

3. Open a new terminal window and start ngrok on the same port where your Flask application is running:

    ```bash
    ./ngrok http 5000
    ```

   Replace `./ngrok` with the path to your ngrok executable if it's not in the current directory.

4. Ngrok will display a public URL in the terminal. You can use this URL to access your local web server from the internet. The URL will look something like `http://12345678.ngrok.io`.

5. You can now use this public URL to set up your GitHub webhooks. Remember to append `/webhook` to the URL when setting up the webhook, like so: `http://12345678.ngrok.io/webhook`.

Please note that the ngrok URL is temporary and will change every time you restart ngrok. If you need a permanent URL, you can sign up for a paid ngrok account.

## Usage

1. To test the webhook event handler, you can send a POST request to `http://localhost:5000/webhook` with the GitHub event payload.

2. To view the events, navigate to `http://localhost:5000/events` in your web browser. The page will automatically refresh every 15 seconds to display the latest events.
