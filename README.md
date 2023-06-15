# Products recognition in Movies

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

## Run the web application server
To run the web application server locally, run the following command from this repository's root directory
(remember to activate the python environment previously set up):

### Local database instance
To create a local database instance you need to download and install the MongoDB server from [here](https://www.mongodb.com/try/download/community).  

Run the installer with the default options.

Once the installation is complete, run the application MongoDBCompass.

You'll be exposed to a window like this:
![MongoDBCompass_home](/readme_images/mongodbcompass_home.png)  

In the **New Connection** section, fill in the **uri** section with the following string:
```
mongodb://localhost:27017
```
And then click on **Connect**.

You'll be exposed to a window like this:
![connected](/readme_images/connected.png)

Click on the "+" button to create a new database.

It will open a pop-up window like this:
![create_db](/readme_images/db_creation.png)

Fill in the **Database Name** field with the following string:
```
movies
```

and the **Collection Name** field with the following string:
```
movies_info
```

Then click on **Create Database**.


To import the data into the database, you need to click on add data and then on **Import JSON/CSV file**.
As shown below:
![import_data](/readme_images/data_import.png)

It will open a pop-up window where you need to select the file <code>mongodb_dump/movies_movies_info_dump.json</code> from this repository's root content.

Then click on **Import**.

Now you can run the application using the local database instance with the following command:
```
flask --app flaskr:create_app(use_local_db=True) run
```

### Remote database instance
To run the application using the remote database instance, you can use the following command:
```
flask --app flaskr run
```
