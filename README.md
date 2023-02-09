# ActivityTracker
<p align="center">
    <img src="/sampleImages/sample1.JPG#center">
</p>

## Description
This is an activity tracker to record the run time of processes running on a Windows OS. The activity tracker is built using Python and tkinter library. The tracker allows the user to monitor a maximum of 5 programs and saves their run time. The user can add or remove programs to be tracked, and the run time will be saved in a json file.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites
Python3, Tkinter library
### Installation
-Clone the repository to your local machine
```
git clone https://github.com/Isaiahdaiz/ActivityTracker.git
```
-Install the required libraries
```
pip install tkinter
```
### Running the program
```
python ActivityTracker.py
```
### Built With
-Python
-Tkinter

## Problems and Solutions
### The following describes problems I encoutered while developing the Activity Tracker and my solution
Problem 1: Adding too many programs to check whether they are running slows down the program a lot.
Solution 1: Limit amount of applications allowed to 5

Problem 2: Cannot store tk objects into json file
Solution 2: Load data by pulling json data and convert from int to IntVar (tk object) and vice versa to store
