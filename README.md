# Final Year Project for BSc. Computer Science
## Evolutionary Algorithm Design for A Chinese-Style Pattern Generation System

### Abstract
This project aims to generate Chinese-Style pattern with an evolutionary algorithm. Generative Arts has always been discussed as an alternative design method in contrast with the traditional man-intensive design. In Chinese architecture, there are an immense amount of housing elements that involve designing patterns for usages such as for windows, doors, corridors, and etc., providing diversity in the design itself. This dissertation combines the 2 using an evolutionary approach to generate innovative design patterns with a Chinese architectural style automatically, using a self-devised algorithm. It is hoped that this dissertation would be able to benefit and contribute to graphics designers, interior designers, game art designers, and anyone who would like to add a little Chinese element to their lives.

The entire project is written in Python, where Python version 3.8.5 is used. Testing files and data analytic files (written using MATLAB) are not included in the project directory. 

### Package specifications:
#### Python version
- Python 3.8.5

#### User Interface:
- PyGame, install with `python3 -m pip install -U pygame --user`


#### Other standard libraries used:
- math
- numpy
- random
- time

### Starting the Application/ Software
#### How to use the application
1. Download repository from GitLab using command `git clone`.
	- Git clone with https: `git clone https://git-teaching.cs.bham.ac.uk/mod-ug-proj-2021/ycn992`
	- Git clone with SSH: `git clone git@git-teaching.cs.bham.ac.uk:mod-ug-proj-2021/ycn992.git`, for information regarding how to add SSH keys, please read [this page](https://git-teaching.cs.bham.ac.uk/help/ssh/index.md). 
2. Start a terminal window for Linux/ macOS systems, or start a command prompt window for Windows system.
3. Change directory to the file that contains the code.
`cd your_path_to_project/src/main/code`
4. Start the application using 
	- `python main.py` or 
	- `python3 main.py` if you have both python 2 and python 3 installed.
	
	The command should be the same for all Linux, macOS and Windows systems. 

5. A window should open up, you can start generating patterns by clicking the "Start/ Evolve" button at the bottom. Each time pressing it, it will evolve the population for 10 generations in the background then show the resulting patterns to you. 
6. The current generation number can be tracked at the bottom right corner, e.g. generation 150 is displayed as "Gen: 150". The generations increments by 10 each time the "Start/ Evolve" button is pressed since 10 background evolution generations are run each time. 
7. If you do not find the patterns in the current population interesting, click the "Refresh" button at the bottom left of the window. This will restart the evolution process and re-initialise a new population for you. You can refresh the population for as many times as you like, until you find an initial population that you are content with. The generation number at the bottom right is reset to 0 every time the "refresh" buttom is clicked, i.e. the display is changed to "Gen: 0". 

#### Points to note
- Starting with an initial population with more different elements contained in it encourages the application to generate more unique design patterns.
- If you want to generate distinct patterns without a specific preference, let the system evolve on its own without inputting preference would be able to generate more unique patterns.
- If you want to see more patterns that are similar to a specific pattern that is shown to you in a given population, select the pattern by single-clicking it. A notification will pop up to notify you of your selection, where you can press "OK" to dismiss the notification. Then you can continue the evolution, the next 10 generations will be evolved considering the preferred input pattern you selected. Of course, which strategy you want to use is entirely up to you! :D

I hope you enjoy using the application! 