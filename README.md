# MoneyCounter - Indian Rupee Coin Detection System

MoneyCounter is a computer vision-based application that detects and identifies Indian Rupee coins using a camera. The system uses OpenCV image processing techniques to detect circular coins and classify them based on their color characteristics and size.

## Project Overview

The system is designed to automatically detect Indian Rupee coins placed in front of a camera and calculate their total value.

It uses:

- Hough Circle Transform for detecting coins
- HSV color analysis for identifying coin types
- Radius-based classification for distinguishing similar silver-colored coins
- OpenCV for real-time image processing
- NumPy for numerical operations

The application displays the detected coins, their denominations, and the total monetary value on the screen.

## Features

- Real-time coin detection using a camera
- Detection of multiple coins
- Indian Rupee coin classification
- Identification of Rs 1, Rs 2, Rs 5 and Rs 10 coins
- Automatic calculation of the total amount
- Visual display of detected circles
- Displays the denomination of each detected coin
- Uses image processing without deep learning

## Technologies Used

- Python
- OpenCV
- NumPy
- Hough Circle Transform
- HSV Color Space
- Computer Vision

## Project Structure

```text
MoneyCounter/
│
├── coin.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
How It Works

The system follows these main steps:

1. Capture Image

The application accesses the camera using OpenCV.

2. Convert Image to Grayscale

The captured frame is converted into grayscale to make circle detection easier.

3. Apply Gaussian Blur

Gaussian blur is applied to reduce image noise and improve circle detection.

4. Detect Coins

The Hough Circle Transform is used to detect circular objects in the image.

5. Analyze Coin Color

The detected coin regions are converted into HSV color space.

The HSV values are used to distinguish:

Gold-colored coins
Silver-colored coins
Two-tone coins
6. Identify Denomination

The system uses color and radius information to classify the coins.

The supported denominations are:

Coin	Detection Method
Rs 1	Radius-based classification
Rs 2	Radius-based classification
Rs 5	Gold-color detection
Rs 10	Gold outer region + silver inner region
7. Calculate Total

The value of every detected coin is added together.

For example:

Detected Coins:

Rs 10
Rs 5
Rs 2
Rs 1

Total: Rs 18
Installation
Step 1: Clone the Repository
git clone https://github.com/meghanavaddi2402/MoneyCounter.git

Move into the project directory:

cd MoneyCounter
Step 2: Create a Virtual Environment
python -m venv .venv

Activate the virtual environment on Windows:

.\.venv\Scripts\Activate.ps1
Step 3: Install Dependencies
pip install -r requirements.txt
Requirements

The project requires:

opencv-python
numpy

These dependencies are included in requirements.txt.

Running the Application

Activate the virtual environment:

.\.venv\Scripts\Activate.ps1

Then run:

python coin.py

The camera window will open and the application will start detecting coins.

Press:

ESC

to close the application.

Camera Configuration

The camera index is defined in coin.py:

CAM_INDEX = 1

If the camera is not detected, try:

CAM_INDEX = 0

The correct camera index depends on the camera configuration of the computer.

Detection Parameters

The project uses the following Hough Circle parameters:

DP = 1.2
MIN_DIST = 60
PARAM1 = 100
PARAM2 = 28
MIN_RADIUS = 30
MAX_RADIUS = 160

These parameters can be adjusted depending on the camera resolution, lighting conditions, and distance between the camera and coins.

Limitations
Detection accuracy depends on lighting conditions.
Coins should be sufficiently separated for reliable detection.
Camera quality can affect circle detection.
Reflections and shadows may affect HSV-based classification.
Similar-sized coins are distinguished using calibrated radius values.
The current implementation requires a working camera.
Future Enhancements

Possible improvements include:

Add support for more coin types and currencies.
Improve detection under different lighting conditions.
Add a graphical user interface.
Add image upload functionality instead of requiring a camera.
Improve classification using machine learning or deep learning.
Add automatic camera detection.
Improve accuracy using contour and shape analysis.
Add voice output for the detected total.
Create a mobile or web-based version.
Learning Outcomes

Through this project, the following concepts were implemented:

Python programming
OpenCV
NumPy
Image preprocessing
Grayscale conversion
Gaussian filtering
Hough Circle Transform
HSV color space
Object detection
Basic computer vision
Real-time image processing
