# MySQL Q&A Chat App

This is a simple Streamlit App to showcase how a LLM can interact with a MySQL database. You can ask questions about data that is available in database, and the LLM will provide you answers in natural language.

## Screenshots

![App Screenshot](q&a.png)

## Steps to run the app

#### Create a virtual environment

- Create a folder in your PC, and open it in a code editor (eg. VS Code).
- Open the terminal and run following command.

```bash
  python -m venv env
```

#### Install Required dependancies

- Here we have a requirements.txt file. we can install the libraries and packages mentioned there.

```bash
  pip install -r requirements.txt
```

#### Setup database

- Here we have 'Chinook' database (Version 1.4.5) authored by Luis Rocha. This contains some tables with sample data.
- If you can access 'phpMyAdmin', just go and import the db.sql file.
- Otherwise, Run the following command in your terminal. Make sure to insert your username and password.

```bash
  mysql -u username -p < db.sql
```

#### Create .env file

- Now, you have to create a .env file and update the environmental variable.

```bash
  OPENAI_API_KEY = "sk-XXXXX"
```

```bash
  MYSQL_URI = mysql+mysqlconnector://USERNAME:PASSWORD@localhost:PORT/DBNAME
```

| Parameter  | Eg        |
| :--------- | :-------- |
| `USERNAME` | `root`    |
| `PASSWORD` | `1234`    |
| `PORT`     | `3306`    |
| `DBNAME`   | `Chinook` |

#### Run the app

- Once you get the above steps done, run the streamlit application.

```bash
  streamlit run main.py
```
