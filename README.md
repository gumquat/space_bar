# Space_Bar

![space bar](https://github.com/gumquat/space_bar/assets/23125776/2ee6ae0f-177c-43bd-9810-b795fe3cd85c)

## Sphinx Documentation

[please refer to the index file in /docs to see further information](/docs/index.rst)

### Our Figma Design

![Figma Design](/Design%20Documents/figma.png)

### Our Notion Write-Up

[Notion Write-Up](https://www.notion.so/Space_Bar-56ff5c968bba4a959e6cca2a1611f0b9)
or
![Notion Write-Up](/Design%20Documents/notion.png)

## Docker Setup

For right now the docker works best in the branch dockerworkhere
Are branches accessible for all???

### Introduction

The way our docker container(s) are setup is through docker-compose.
That way we can easily setup multiple different containers that are automatically connected to one another.
The two containers we have running as of now are the PostgreSQL database server and the Flask server for hosting our APIs. I believe I will be adding a third container to this setup for hosting the Frontend of the webpage.
Another process that happens along side the two servers is also running two scripts:
| Drinks Table | Users Table |
|--------------|-------------|
|![sql_tables](/Design%20Documents/space-bar-diagram.png) | placeholder |

1. makeTables.py (Sets up the PostgreSQL tables for drinks and users)

    [SQL Tables](/Design%20Documents/spaceBarSQL.sql)

2. json2Postgres_01.py (redundant name but don't want to change because it'll break code)

This basically sets up the tables, then loads them with the data we have in a local directory.

#### .env

We need to make sure the .env is setup so that the docker-compose will work without issues!

```bash
~/space_bar $ cp .env.example .env
```

This command will copy the example .env file into (or create) the .env file. For testing purposes we have the variables setup already in the example file even though this is not best practice!

#### Docker-Compose commands

We have these commands the most common being build, up, and exec.

```Makefile
build up down clean logs exec
```

A typical use of these commands would look something like this:

```bash
~/space_bar$ docker-compose build
[+] Building 0.8s (14/14) FINISHED
...........
docker.io/library/ubuntu:22.04   0.7s
...........
 => => transferring context: 36B                                      0.0s
 => CACHED [app 2/9] RUN apt-get update && apt-get install -y     cu  0.0s
 => CACHED [app 3/9] RUN locale-gen en_US.UTF-8                       0.0s
 => CACHED [app 4/9] COPY wait-for-it.sh /wait-for-it.sh              0.0s
 => CACHED [app 5/9] RUN chmod +x /wait-for-it.sh
 ..........
 => => naming to docker.io/library/space_bar-app                      0.0s
```

(_shortened because all of it is not needed for demonstration_)

```bash
~/space_bar$ docker-compose up
[+] Running 2/0
 ✔ Container postgres_space_bar  Cr...                                0.0s
 ✔ Container space_bar           Created                              0.0s
Attaching to postgres_space_bar, space_bar
...........
postgres_space_bar  | 2024-04-14 18:57:27.295 UTC [29] LOG:  database system was shut down at 2024-04-14 18:53:32 UTC
postgres_space_bar  | 2024-04-14 18:57:27.300 UTC [1] LOG:  database system is ready to accept connections
space_bar           | wait-for-it.sh: waiting 15 seconds for postgres:5432
space_bar           | wait-for-it.sh: postgres:5432 is available after 0 seconds
space_bar           |  * Serving Flask app 'app.py'
space_bar           |  * Debug mode: off
```

That is the servers running now (two separate servers ran together)

```bash
~/space_bar$ docker-compose exec app bash
root@57ac362b9ab3:/space_bar#
```

This is the very simple one as it isn't running the servers, but connecting to the container made, and connected to your repository for running the commands necessary to manage the server, or test the different processes and APIs.

#### Testing APIs

We have a few different APIs available just for querying the many different drinks available in our selection:

```python
/drinks
/cocktails
/beers
/wines
/budget_drinks
```

(_one of the shorter examples of the drink queries_)

```bash
root@57ac362b9ab3:/space_bar# curl http://localhost:5000/wines
[{"description":"A dark, brooding red wine with a hint of smoke and ash, evoking the hellish landscape of the planet Mustafar.","drink_id":28,"drink_name":"Mustafar Merlot","drink_type":"Wine","ingredients":null,"price":"14.99"},{"description":"A vibrant red wine blend that's as complex and intriguing as the celestial bodies it's named after.","drink_id":32,"drink_name":"Red Dwarf Red","drink_type":"Wine","ingredients":null,"price":"14.99"}]
root@57ac362b9ab3:/space_bar#
```

I would show more but because of our large selection of drinks it would be too much to show here.

##### User Authentication

```python
/register
/login
/logout
```

With our user authentication APIs we can successfully setup users into our database:

```bash
~/space_bar$ docker-compose exec app bash
root@57ac362b9ab3:/space_bar# curl http://localhost:5000/register -d "username=user&password=test&email=email@email.com"
{"message":"You have successfully registered. Please log in."}
root@57ac362b9ab3:/space_bar# curl http://localhost:5000/login -d "username=user&password=test"
{"message":"You have successfully signed in as user"}
root@57ac362b9ab3:/space_bar# curl http://localhost:5000/logout
{"message":"You have been logged out"}
root@57ac362b9ab3:/space_bar#
```

### Frontend

#### Setting up frontend

For a simple frontend, I went ahead and ran in in the docker container as well, regardless if it was necessary or not.

```bash
~/space_bar$ docker-compose exec app bash
root@57ac362b9ab3:/space_bar# python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

This is the command to run the frontend server, and then you can access it through your browser at `http://localhost:8080/`
Our frontend has come together, we were somehow able to get it barebones functional with the APIs we have setup.
It is not the prettiest, but it is functional.
We will be working on it more in the future to make it more user friendly and visually appealing.

## Authors

Evan Newman:

Evan Richardson: Hey there, I'm Evan Richardson, a Backend-focused FS Engineer with a passion for turning ideas into reality through code! When I'm not coding, you'll likely find me tinkering with computers or enjoying good games. Find me on LinkedIn! Feel free to explore more of my projects on Github or my personal website!

Tayler Coon: Hey there, I'm Tayler Coon, a Full-Stack Engineer with a passion for turning ideas into reality through code! When I'm not coding, you'll likely find me tinkering under my Datsun or mastering the art of Disc Golf. Let's connect on LinkedIn! Feel free to explore more of my projects on Github
