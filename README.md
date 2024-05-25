# Face Swapping API (Backend)

This API handles the face swapping functionality for the web application. It is built using Python and Flask.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following software installed on your machine:

- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/face-swapping-api.git
   ```

2. **Navigate to the backend directory:**

   ```bash
   cd face-swapping-api/backend
   ```

3. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server:**

   ```bash
   python app.py
   ```

2. **The API will be running on [http://localhost:5000](http://localhost:5000).**

## Endpoints

- `POST /upload`: Upload two images and swap their faces. Returns the URLs of the swapped images.

## Project Structure

```
backend/
│
├── static/
│   ├── swapped/
│   └── ...
│
├── templates/
│   └── ...
│
├── venv/
│   └── ...
│
├── app.py
├── face_swap.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Technologies Used

- **Python**: A programming language.
- **Flask**: A lightweight WSGI web application framework.
- **OpenCV**: A library of programming functions mainly aimed at real-time computer vision.
