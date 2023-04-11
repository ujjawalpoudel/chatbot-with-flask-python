# ChatBot Application With Flask

This is a chatbot application built using Flask and MongoDB. Please note that this is a practice project for a college assignment, so we have focused on delivering a simple and efficient solution.

## Requirements
Before setting up the application, ensure that you have the following requirements installed on your system:

* Python (version 3.6 or higher)
* pip (Python package installer)
* Virtualenv (tool to create isolated Python environments)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python package.

1. Clone the repository to your local machine.
  ```bash
  git clone git@github.com:ujjawalpoudel/chatbot-with-flask-python.git
  ```

2. Navigate to the project directory.
  ```bash
  cd chatbot-with-flask-python  
  ```

3. Create a virtual environment.
  Use the version number of python installed on your computer.
  check it using python --version
  ```bash
  python3.11 -m venv chatbot_env 
  ```

4. Activate the virtual environment.
  a. For mac:
  ```bash
  source chatbot_env/bin/activate
  ```
  b. For windows:
  ```bash
  chatbot_env\Scripts\activate.bat
  ```

5. Install the required Python packages.
  ```bash
  pip install -r requirements.txt
  ```

## Running the Application
  1. Activate the virtual environment.
  ```bash
  source chatbot_env/bin/activate
  ```

  2. Start the Flask development server.
  ```bash
  python main.py
  ```

  3. Access the application in a web browser by navigating to `http://localhost:5000`.

## API Documentation
For detailed API documentation, please refer to the [Postman Collection](https://www.postman.com/gold-robot-526148/workspace/python-term-project/collection/17813876-44ad6e56-102f-4490-aa05-4c31b83c2dfa?action=share&creator=17813876).

## Conclusion

This concludes the setup readme for the Flask application. If you encounter any issues during setup or usage, please get in touch with the project maintainer for assistance.


## Contributing

Pull requests are welcome. For significant changes, please open an issue first
to discuss what you would like to change.
