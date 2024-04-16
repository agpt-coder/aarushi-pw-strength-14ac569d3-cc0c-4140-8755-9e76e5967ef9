---
date: 2024-04-16T09:25:47.764131
author: AutoGPT <info@agpt.co>
---

# aarushi-pw-strength-1

To address the task, the system should implement an endpoint capable of accepting a password string and analyzing its strength. This analysis would involve evaluating the password based on several factors including its length, complexity (use of uppercase and lowercase letters, numbers, and special symbols), and its adherence to or deviation from common patterns which attackers might easily guess (e.g., '123456', 'password', 'qwerty'). The endpoint should then assign a score indicating the password's strength, with categories such as weak, medium, strong, or very strong. The scoring algorithm should be designed to encourage users towards creating passwords that are hard to guess or brute-force by attackers, incorporating findings from previous searches and user inputs. Based on the evaluation, the service should also offer actionable suggestions for improving password security, such as increasing length, diversifying characters, and avoiding common patterns or personal information. Best practices include not only these technical measures but also encouraging behavior like regular password updates, the use of different passwords for different sites, and the activation of multi-factor authentication where possible. For implementation, using Python and the FastAPI framework can facilitate rapid development, with PostgreSQL for database needs and Prisma as the ORM to interact with the database efficiently. This solution aims not just to evaluate passwords but also to educate users about creating stronger, more secure passwords, thus enhancing overall security.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-pw-strength-1'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
