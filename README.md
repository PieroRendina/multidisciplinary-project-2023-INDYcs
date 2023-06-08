# Video Object Detection

Project of the **Multidisciplinary course** offered at Politecnico di Milano A.Y.2022/2023.

### Team members
* [Matteo Nunziante](https://github.com/matteoNunz)
* [Alessandro Pindozzi]()
* [Piero Rendina](https://github.com/PieroRendina)
* [Andrea Sanchini](https://github.com/AndreaSanchini)
* [Ioana-Ruxandra Stancioi](https://github.com/ruxandrastancioi)



## Requirements
To run the web application a Python intepreter is needed (version 3.9 or higher). 
We suggest to use a virtual environment to avoid conflicts with other Python projects.


### Virtual environment
Once you have installed Python, you can create a virtual environment with the following command:
```
python -m venv <directory>
```

You need to activate the virtual environment before installing the required packages:
``` 
<directory>\Scripts\activate.bat
``` 

To install the required packages run the following command:
```
pip install -r requirements.txt
```

### Run the web application server locally 
To run the web application server locally, run the following command from this repository's root directory
(remember to activate the python environment previously set up):
```
flask --app flaskr run
```