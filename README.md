# Installation and User Manual

## Initial Setup

### Install NODE.JS and NPM
1. Click on this [link](https://github.com/nvm-sh/nvm) and follow the instructions to download Node.js and the subsequent NPM (Node Package Manager).
   
   **Note:** The Node.js version to be installed will be v19.9.0.

### Install Python Packages
2. Inside the directory of "capstone-project-3900h19aundecided", run the command `pip3 install -r requirements.txt`. This will download all the packages required for the program to run.
   
   **Note:** Python 3.8.9 is required.

### Install Docker Desktop
3. Install Docker Desktop from this [link](https://docs.docker.com/desktop/release-notes/), downloading the v4.23.0 version. Follow the instructions on installation in this [link](https://docs.docker.com/desktop/).

## Running Tests

4. In a terminal, change to the "capstone-project-3900h19aundecided/database" directory and run the command `bash init_db.sh` to create an almost empty database for the tests.

5. In another terminal, change to the "capstone-project-3900h19aundecided/backend" directory and run the command `python3 app.py`, which will run the backend server.

6. In another terminal, change to the "capstone-project-3900h19aundecided/backend" directory, run the command `python3 -m pytest` to run and show passing tests.

## Starting the Application with a Populated Database

7. In the "capstone-project-3900h19aundecided/frontend" directory, run the command `npm install` to download all the necessary packages. After completion, run `npm start`. This should open your browser to the login page of the application. If the browser does not open, navigate to [http://localhost:3000](http://localhost:3000).

   **Note:** You only need to run `npm install` once; you can restart the frontend via `npm start`.

8. In another terminal, open the "capstone-project-3900h19aundecided/backend" directory and run the command `python3 app.py` to run the backend server.

9. In a terminal, open the "capstone-project-3900h19aundecided/database" directory and run the command `bash custom_db.sh` to create a populated database for use.

## Populated Database Information

### Users
These are the prefilled users and their details required to login and navigate on the website.

**Note:** No trailing whitespaces in the login or results in a failed login.

- **z1234561**
  - Email: z1234561@unsw.edu.au
  - Password: banana
  - Role: admin, academic, student

- **z1234562**
  - Email: z1234562@unsw.edu.au
  - Password: banana
  - Role: academic, student

- **z1234563**
  - Email: z1234563@unsw.edu.au
  - Password: banana
  - Role: student

- **z1234564**
  - Email: z1234564@unsw.edu.au
  - Password: banana
  - Role: student

- **z1234565**
  - Email: z1234565@unsw.edu.au
  - Password: banana
  - Role: student

### Courses
There are 41 courses, all COMP courses from 2023 Term 3. They have been web-scraped using Selenium, cleaned, and NLP has been applied to the raw web-scraped data to extract the skills and knowledge.

### Projects
There are 3 sample projects containing mock data, including skills and knowledge.