# Summer 2026 Belgium DoC Project Template

This is a template repo for Summer 2026 CS 4973, part of the Belgium Dialogue run by Dr. Gerber and Dr. Fontenot.

It includes most of the infrastructure setup (containers), sample databases, and example UI pages. Explore it fully and ask questions!

## Prerequisites

See [docs/PreReq.md](docs/PreReq.md) for full setup instructions, including Python environment setup with Anaconda/Miniconda or the standard Python virtual environment tool, required tools, and IDE configuration.

## Structure of the Repo

- This repository is organized into six main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets
  - `./ml-src` - folder for ML model development (Jupyter notebooks, training scripts)
  - `./docs` - project documentation

- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database.

## Suggestion for Learning the Project Code Base

If you are not familiar with web app development, this code base might be confusing. But don't worry, we'll get through it together. Here are some suggestions for learning the code base:

1. Start by exploring the `./app` directory. This is where the Streamlit app is located. The Streamlit app is a Python-based web app that is used to interact with the user. It's a great way to build a simple web app without having to learn a lot of web development.
1. Next, explore the `./api` directory. This is where the Flask REST API is located. The REST API is used to interact with the database and perform other server-side tasks. You might also consider this the "application logic" or "business logic" layer of your app. 
1. Finally, explore the `./database-files` directory. This is where the SQL scripts are located that will be used to initialize the MySQL database.
1. Bonus: If you want a totally separate copy of the template repo on your laptop to explore and experiment with without affecting your team repo, see the *Setting Up a Personal Sandbox Repo* section in [docs/RepoSetup.md](docs/RepoSetup.md).

## Setting Up the Repos

See [docs/RepoSetup.md](docs/RepoSetup.md) for full instructions on forking and configuring the team repo, setting up the `.env` file, and running the Docker containers. An optional section there also covers setting up a personal sandbox repo for individual experimentation.

## Important Tips

1. In general, any changes you make to the api code base (REST API) or the Streamlit app code should be *hot reloaded* when the files are saved.  This means that the changes should be immediately available.  
   1. Don't forget to click the **Always Rerun** button in the browser tab of the Streamlit app for it to reload with changes.
   1. Sometimes, a bug in the code will shut the containers down.  If this is the case, try and fix the bug in the code.  Then you can restart the `app` container in Docker Desktop or restart all the containers with `docker compose restart` (no *-d* flag).
1. The MySQL Container is different. 
   1. When the MySQL container is ***created*** the first time, it will execute any `.sql` files in the `./database-files` folder. **Important:** it will execute them in alphabetical order.  
   1. The MySQL Container's log files are your friend! Remember, you can access them in Docker Desktop by going to the MySQL Container, and clicking on the `Logs` tab.  If there are errors in your .sql files as it is trying to run them, there will be a message in the logs. You can search 🔍 for `Error` to find them more quickly. 
   1. If you need to update anything in any of your SQL files, you **MUST** recreate the MySQL container (rather than just stopping and restarting it).  You can recreate the MySQL container by using the following command: `docker compose down db -v && docker compose up db -d`. 
      1. `docker compose down db -v` stops and deletes the MySQL container and the volume attached to it. 
      1. `docker compose up db -d` will create a new db container and re-run the files in the `database-files` folder. 

## Handling User Role Access and Control

This project uses a simple Role-based Access Control (RBAC) system implemented in Streamlit. The template ships with example roles (*Political Strategist*, *USAID Worker*, *System Administrator*) to illustrate the pattern — **your team will replace these with the personas specific to your project**.

See [docs/RBAC.md](docs/RBAC.md) for a full explanation of how the RBAC system works and step-by-step instructions for adapting it to your own roles.


## Incorporating a Predictive ML Model into your Project

**Note:** Every project is required to include a predictive ML model. This section walks through how the template infrastructure supports that. The template currently contains a placeholder (fake) model — your team will replace it with a real trained model.

1. Collect and preprocess necessary datasets for your ML models.
1. Build, train, and test your ML model in a Jupyter Notebook.
   - You can store your datasets in the `datasets` folder. You can also store your Jupyter Notebook in the `ml-src` folder.
1. Once your team is happy with the model's performance, convert your Jupyter Notebook code for the ML model to a pure Python script.
   - You can include the `training` and `testing` functionality as well as the `prediction` functionality.
   - Develop and test this pure Python script first in the `ml-src` folder.
   - You may or may not need to include data cleaning, though.
1. Review the `api/backend/ml_models` module. In this folder,
   - We've put a sample (read _fake_) ML model in the `model01.py` file. The `predict` function will be called by the Flask REST API to perform '_real-time_' prediction based on model parameter values that are stored in the database. **Important**: you would never want to hard code the model parameter weights directly in the prediction function.
1. The prediction route for the REST API is in `api/backend/simple/simple_routes.py`. Basically, it accepts two URL parameters and passes them to the `prediction` function in the `ml_models` module. The `prediction` route/function packages up the value(s) it receives from the model's `predict` function and sends it back to Streamlit as JSON.
1. Back in Streamlit, check out `app/src/pages/11_Prediction.py`. Here, two numeric input fields are created. When the button is pressed, it makes a request to the REST API at `/prediction/{var_01}/{var_02}` and passes the values from the two inputs as URL path parameters. It gets back the results from the route and displays them.