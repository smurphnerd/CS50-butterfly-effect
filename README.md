# The Butterfly Effect

My final project for Harvard's CS50 course.

## Description

For this project, I decided to make a website where users can make their own data tree and visualise it in a tree view.

This program could be used for a variety of different purposes such as:

- planning the future,
- making family trees,
- writing pseudocode,
- making choose your own adventures, and
- anything else you can imagine.

## Technologies

### Python/Flask

This project is built on [Flask](https://flask.palletsprojects.com/en/2.1.x/) and can be started by running [app.py](app.py). In addition to flask, other required python libraries include:

- cs50,
- werkzeug.security,
- datetime,
- functools,

and two homemade libraries:

- [helpers.py](helpers.py), and
- [bfly.py](bfly.py).

One of the functions in the **bfly.py** library is responsible for creating a .json file for the user's data tree and storing it in **/static/user_data** so that it can be later manipulated using javascript.

### Sqlite3

All user data as well as their data trees are stored in a relational database - [butterfly-effect.db](butterfly-effect.db) under three different tables:

1. users
   - id (PK)
   - username
   - password_hash
2. nodes
   - id (PK)
   - user_id (FK)
   - message
   - root_node (NULL if not a root, 1 if a root)
3. children ( relations between nodes)
   - parent_id (FK)
   - child_id (FK)

### HTML/CSS

HTML with Jinja templating used and responsive CSS built from scratch. The website's design was inspired by VSCode's dark theme.

### Javascript

Used to fetch the .json file from **/user_data** and display it on the page. Also used to give functionality to buttons that isn't possible with HTML or CSS.

## How to run

```
$ git clone https://github.com/therealSmurphy/CS50-final-project.git
$ cd butterfly-effect/
$ pip install -r requirements.txt
$ python3 app.py
```

## Future improvements

If I were to continue working on this, one thing I would change is the error message display. It currently uses the default windows alert but it might be better to have custom alerts that display on the webpage.

Another change would be to extract the tree data from the database directly into a javascript object, eliminating the need for an intermediary .json file. The only reason why I didn't go this route in the first place was because I thought I would be able to use python and jinja to display the data tree on the webpage.

The final thing I would add to this program would be another page that displays the user's data tree as a graph, using a tool like [d3js](d3js.org).
