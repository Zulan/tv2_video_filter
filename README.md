# TV2 Video Filter

With this simple ball of python, you can cut the paues from your Train Valley 2 Videos.

You will probably have to change the resolution / check_pos in filter.py - TODO autodetect that.


# Usage on Windows with docker:

Install docker for windows (that will setup docker and wsl2 stuff)  
We will use this dockerfile: https://github.com/janza/docker-python3-opencv  
Copy video file to project folder or do another mapping in docker
  
run in powershell in project folder to start docker and map project folder to /files inside container  
``docker run -it -v ${PWD}:/files jjanzic/docker-python3-opencv bash``  

Some commands I used but they are not needed I think:
- ``pip install --upgrade setuptools``
- ``pip install build``
- ``python -m build``  

Needed commands:  
``pip install click``

run in folder tv2_video_filter  
``python3.9 filter.py /files/your-file.mp4``

It should start now and create a new file your-file-active.mp4
