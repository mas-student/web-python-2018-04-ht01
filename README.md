# Grammar analyzer

Grammar analyzer is the library that find most frequently verbs in python projects.

## Prerequisites

### OS

Ubuntu LTS version will be enough.

### Python

```
sudo apt-get install python3
```

### Pip

```
sudo apt-get install python3-pip
```

### Git

```
sudo apt-get install git
```

## Installing

### Clone repo

```
git clone git@github.com:mas-student/web-python-2018-04-ht01.git
```

### Install requirements
```
pip install -r requirements.txt
```

### Example
Try example

```
>>> import grammaranalyzer
>>> grammaranalyzer.get_top_function_name_verbs_in_path('flask')
[('get', 58), ('add', 34), ('make', 16), ('run', 16), ('find', 8), ('expect', 3), ('save', 3), ('do', 2), ('keep', 2), ('finalize', 1)]
```

## Running the tests

```
python3 setup.py nosetests
```

## Authors

* **Student** - *Initial work* - [Student](https://github.com/mas-student)
