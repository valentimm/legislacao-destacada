# Legislação Destacada Downloader

## Description

<p align="center">A script to download files from the Legislação Destacada course </p>

## Requirements

- Python 3.6+
- [Requests](https://pypi.org/project/requests/)

## Usage

1. Create a file named `config.py` with the following content:

    ```python
    username = "your_username",
    password = "your_password"
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

4. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

5. Then run the script:

    ```bash
    python3 main.py
    ```

If the login is successful, you'll need to enter the number of days from the course you want to download.
Then you will put the name of the folder where the files will be downloaded.
After the script finishes, you will have a folder with the name you chose with all the files from the course.
