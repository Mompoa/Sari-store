# Deploying sari/store.com to Render

This guide will walk you through the process of deploying your `sari/store.com` Flask application to Render, a cloud platform that allows you to host web services, databases, and more. By following these steps, your website will be permanently online and accessible.

## ⚠️ Important Note on Database (SQLite)

Your application uses **SQLite**, which is a file-based database (`store.db`). Render's free web services have an **ephemeral filesystem**, meaning any data written to the disk (like your `store.db` file) will be lost when the service restarts or redeploys. This is **not suitable for production environments** where data persistence is critical.

**Recommendation:** For a production-ready application, it is highly recommended to migrate to a persistent database service like **PostgreSQL** (which Render offers). For the purpose of getting your site online quickly, we will proceed with SQLite, but be aware of the data loss implications.

## 🚀 Step-by-Step Deployment Guide

### Step 1: Prepare Your Codebase

I have already made the necessary adjustments to your project for Render deployment:

-   **`requirements.txt`**: Updated to include `gunicorn` (a production-ready WSGI server) and `python-dotenv` for environment variable management.
-   **`Procfile`**: Created to tell Render how to start your web service (`web: gunicorn run:app`).
-   **`render.yaml`**: Created for Infrastructure as Code (IaC) to define your Render service configuration.
-   **`.env.example`**: Provided as a template for your environment variables.
-   **`.gitignore`**: Updated to exclude sensitive files and the database file from your repository.
-   **`run.py`**: Modified to use `gunicorn` and environment variables for configuration.
-   **`app/__init__.py`**: Modified to use environment variables for database configuration.
-   **`app/email_service.py`**: Modified to use environment variables for email credentials.
-   **`app/routes.py`**: Modified to use environment variables for the admin password.

### Step 2: Create a GitHub Repository

Render deploys directly from Git repositories. You need to create a new **public or private** GitHub repository and push your entire `sari-store` project to it.

1.  **Go to GitHub**: Navigate to [github.com/new](https://github.com/new).
2.  **Create New Repository**: Give your repository a name (e.g., `sari-store-app`). Choose whether it's public or private. **Do NOT initialize with a README, .gitignore, or license**, as your project already has these.
3.  **Push Your Code**: Open your terminal, navigate to your `sari-store` project directory, and run the following commands:

    ```bash
    cd /home/ubuntu/sari-store
    git init
    git add .
    git commit -m 
"Initial commit for sari/store.com"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git # Replace with your GitHub username and repo name
    git push -u origin main
    ```

    **Important**: Make sure to replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub details.

### Step 3: Deploy to Render

Now that your code is on GitHub, you can deploy it to Render.

1.  **Sign up or Log in to Render**: Go to [render.com](https://render.com/) and sign up for a new account or log in.
2.  **Connect GitHub**: In your Render dashboard, go to 
`New > Web Service`.
3.  **Connect Your Repository**: Select your GitHub repository (`sari-store-app`) that you created in Step 2. You might need to grant Render access to your GitHub account if you haven't already.
4.  **Configure Your Web Service (Using `render.yaml`)**:
    -   Render will detect the `render.yaml` file in your repository. This file contains the configuration for your service.
    -   **Name**: `sari-store` (or your preferred service name)
    -   **Root Directory**: Leave blank (or `/` if your code is at the root)
    -   **Branch**: `main` (or your main branch name)
    -   **Build Command**: `pip install -r requirements.txt` (This is specified in `render.yaml`)
    -   **Start Command**: `gunicorn run:app` (This is specified in `render.yaml`)
    -   **Instance Type**: `Free` (for a free tier service)
    -   **Region**: Choose a region closest to your users.
5.  **Set Environment Variables**: This is crucial for security and configuration.
    -   Go to the `Environment` section of your Render service settings.
    -   Add the following environment variables. You can find their default values in your `.env.example` file. **Make sure to change `SECRET_KEY` and `ADMIN_PASSWORD` to strong, unique values.**

    | Key               | Value (Example)                                     | Description                                                               |
    | :---------------- | :-------------------------------------------------- | :------------------------------------------------------------------------ |
    | `FLASK_ENV`       | `production`                                        | Sets Flask to production mode.                                            |
    | `SECRET_KEY`      | `your_very_secret_key_here_change_this`             | A strong, random key for session security.                                |
    | `SMTP_SERVER`     | `smtp.gmail.com`                                    | SMTP server for sending emails.                                           |
    | `SMTP_PORT`       | `587`                                               | SMTP port.                                                                |
    | `SENDER_EMAIL`    | `iglesiaalejandro21@gmail.com`                      | The email address that will send order notifications.                     |
    | `SENDER_PASSWORD` | `sbrc ztlc vbqu dmep`                               | The app-specific password for the sender email.                           |
    | `RECIPIENT_EMAIL` | `iglesiaalejandro21@gmail.com`                      | The email address that will receive order notifications.                  |
    | `ADMIN_PASSWORD`  | `Raben677`                                          | The password for your admin panel. **CHANGE THIS!**                       |
    | `DATABASE_URL`    | `sqlite:///store.db`                                | Database connection string. (See warning above about SQLite on Render)    |

    **Note on `SENDER_PASSWORD`**: If you are using Gmail, you will need to generate an **App Password** instead of using your regular Gmail password. Go to your Google Account Security settings, enable 2-Step Verification, and then generate an App Password for 
your email. [Learn more about App Passwords](https://support.google.com/accounts/answer/185833?hl=en).

6.  **Deploy**: Click "Create Web Service". Render will automatically build and deploy your application. You can monitor the deployment logs in your Render dashboard.

### Step 4: Access Your Live Website

Once the deployment is successful, Render will provide you with a public URL for your web service (e.g., `https://sari-store.onrender.com`).

-   **Your Store**: Access your live store at this URL.
-   **Admin Panel**: Access your admin panel by adding `/admin` to the URL (e.g., `https://sari-store.onrender.com/admin`).

## 🔄 Updating Your Website

To update your website, simply push new changes to your GitHub repository. Render is configured for automatic deployments, so it will detect the changes and redeploy your service.

## 🗑️ Deleting Your Service

If you wish to remove your website from Render, go to your service settings in the Render dashboard and select "Delete Service".

## 📚 References

[1] Render Documentation: [https://render.com/docs](https://render.com/docs)
[2] Gunicorn: [https://gunicorn.org/](https://gunicorn.org/)
[3] Google App Passwords: [https://support.google.com/accounts/answer/185833?hl=en](https://support.google.com/accounts/answer/185833?hl=en)
