# Twitter Follower Prune Bot

A Python script to unfollow Twitter users who have less than a certain number of followers and are not following you back.

## Prerequisites

Before running this script, you will need:

- Python 3 installed on your machine
- A Twitter developer account and app with valid API keys

## Installation

1. Clone this repository or download the ZIP file.
2. Install the required Python packages by running:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a file called `authfile.py` in the same directory as the script.
4. In `authfile.py`, define the following variables with your Twitter API credentials:

    ```py
    api_key = 'your_api_key_here'
    api_secret = 'your_api_secret_here'
    access_token = 'your_access_token_here'
    access_secret = 'your_access_secret_here'
    ```
5. You would be prompted to input minimum number of followers for a Twitter user to be considered an influencer to you.
6. Run the script using `python follower-prune.py`.

## Usage

The script will first get a list of all people you follow on Twitter with followers less than the minimum number of followers you specified. It will then check if these users are following you, and if not- it will unfollow them.
