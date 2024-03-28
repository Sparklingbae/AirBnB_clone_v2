AirBnB clone
======================================
![**AirBnB**](https://github.com/HucksApp/AirBnB_clone/assets/58187974/0a2d1bfa-9390-4515-aacc-b2eaf190788a)

### Description ##
This team project is part of the ALX School Full-Stack Software Engineer program. It's the second step towards building a full web application: an AirBnB clone.


## The console 🎛

### Choosing ***Storage*** mode 🗃 🛢️
The console can be run with storage instantiated in either *FileStorage* or *DBStorage* mode. The FileStorage is the default mode.

To instantiate with DBStorage, set this variables.
```
HBNB_MYSQL_USER=<username>
HBNB_MYSQL_PWD=<password>
HBNB_MYSQL_HOST=<host>
HBNB_MYSQL_DB=<database>
HBNB_TYPE_STORAGE=<db>  # defaulted to 'file'
 ```
sample 
```
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py
```

----------------------------------------------------
### Usage ###
The console works both in interactive mode and non-interactive mode, much like a Unix shell. It prints a prompt **(hbnb)** and waits for the user for input.


Description                                         | Command
----------------------------------------------------|--------------------
Run the console	                                    | `./console.py`
Quit the console	                                   | `(hbnb) quit`
Display the help for a command	                     | `(hbnb) help <command>`
Create an object (prints its id)	                   | `(hbnb) create <class>` or `(hbnb) <class>.create()` or `create <Class> <param 1> <param 2> ...` where param is -> `<attribute key>=<attribute value>`
Show an object	                                     | `(hbnb) show <class> <id>` or `(hbnb) <class>.show(<id>)`
Destroy an object	                                  | `(hbnb) destroy <class> <id>` or `(hbnb) <class>.destroy(<id>)`
Count all objects or all instances of a class       | `(hbnb) count ` or `(hbnb) count <class> ` or `(hbnb) <class>.count()` or `(hbnb) .count()`
Show all objects, or all instances of a class       |	`(hbnb) all` or `(hbnb) all <class>` or `(hbnb) .all()` or `(hbnb) <class>.all()`
Update attributes or attribute of an object                    |	`(hbnb) update <class> <id> <attribute name> "<attribute value>"` or `(hbnb) <class>.update(<id>, <attribute name>, "<attribute value>")` or `(hbnb) <class>.update(<id>, {"<attribute name>" : "<attribute value>"})`

**Non-interactive mode example**
 ```
$ echo "help" | ./console.py

 (hbnb)

  Documented commands (type help <topic>):
  ========================================`
  EOF  all  count  create  destroy  help  quit  show  update

  (hbnb)
```

**Interactive mode example**
```
$ ./console.py
(hbnb) create User
6f348019-0499-420f-8eec-ef0fdc863c02
(hbnb)
(hbnb) update User 6f348019-0499-420f-8eec-ef0fdc863c02 first_name "Holberton" 
(hbnb) show User 6f348019-0499-420f-8eec-ef0fdc863c02
[User] (6f348019-0499-420f-8eec-ef0fdc863c02) {'created_at': datetime.datetime(
2019, 2, 17, 21, 54, 39, 234382), 'first_name': 'Holberton', 'updated_at': date
time.datetime(2019, 2, 17, 21, 54, 39, 234382), 'id': '6f348019-0499-420f-8eec-
ef0fdc863c02'}
(hbnb)
```


----------------------------------------------------------------------
## Models (Data Classes) 🏺 🆑
The folder models contains all the classes used.

### File	Description	Attributes 📊

File                                            | Description                                               | Atrributes
------------------------------------------------|-----------------------------------------------------------|---------------------------------------
[base_model.py](./models/base_model.py)         |	***BaseModel*** Base Class for all other model 	          | *id*, *created_at*, *updated_at*
[user.py](./models/user.py)                     | ***User*** class for user information	                    | *email*, *password*, *first_name*, *last_name*
[amenity.py](./models/amenity.py)	              | ***Amenity*** class for amenity information	              | *name*.
[city.py](./models/city.py)	                    | ***City*** class for location information	                | *state_id*, *name*.
[state.py](./models/state.py)         	         | ***State*** class for location information	               | *name*.
[place.py](./models/place.py)    	              | ***Place*** class for accomodation information	           | *city_id*, *user_id*, *name*, *description*, *number_rooms*, *number_bathrooms*, *max_guest*,   *price_by_night*, *latitude*, *longitude*, *amenity_ids*.
[review.py](./models/review.py)   	             | ***Review*** class for user/host review information      	| *place_id*, *user_id*, *text*.

----------------------------------------------------------------
# Storage 🛄
The above classes are handled by one of either two abstracted storage engines, depending on the call - ***FileStorage*** or ***DBStorage***.

## File storage 📄 🗃
The file storage engine manages the serialization and deserialization of all the data, following a JSON format.
This  *File* mode is the default mode  `HBNB_TYPE_STORAGE=file`

A ***FileStorage*** class is defined in [file_storage.py](./models/engine/file_storage.py) with methods to follow this `flow: <object> -> to_dict() -> <dictionary> -> JSON dump -> <json string> -> FILE -> <json string> -> JSON load -> <dictionary> -> <object>`

In FileStorage mode, every time the backend is initialized, HolbertonBnB instantiates an instance of FileStorage called storage. The storage object is loaded/re-loaded from any class instances stored in the JSON file file.json. As class instances are created, updated, or deleted, the storage object is used to register corresponding changes in the *file.json*.


## Database Storage 🤖🛢️
This storage mode is a storage class define by [db_storage.py](./models/engine/db_storage.py)

Run by setting the environmental variable `HBNB_TYPE_STORAGE=db`

In DBStorage mode, every time the backend is initialized, HolbertonBnB instantiates an instance of DBStorage called storage. The storage object is loaded/re-loaded from the MySQL database specified in the environmental variable HBNB_MYSQL_DB, using the user `HBNB_MYSQL_USER`, password `HBNB_MYSQL_PW`D, and host `HBNB_MYSQL_HOST`. As class instances are created, updated, or deleted, the storage object is used to register changes in the corresponding MySQL database. Connection and querying is achieved using ***SQLAlchemy***.

This repository includes scripts *setup_mysql_dev.sql* and *setup_mysql_test.sql* to set up *hbnb_dev_db* and *hbnb_test_db* databases in a MySQL server, respectively.


---------------------------------------------------------------------

## Tests 🧑🏿‍🔬️ 🧪
Unittests for the HolbertonBnB project are defined in the [tests folder](./tests).

To run the entire test suite simultaneously, execute the following command:
```
$ python3 unittest -m discover tests
```
Alternatively, you can specify a single test file to run at a time:
```
$ python3 unittest -m tests/<test_file>
```

## Authors 🖋
__Abiodun Aremu__ ~ HucksApp@gmail.com : 



