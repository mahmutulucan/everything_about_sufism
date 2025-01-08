# Everything About Sufism
**Everything About Sufism** is a dynamic platform where users can share content and engage in discussions about various topics related to Sufism. The platform focuses on areas such as the history of Sufism, its literature, concepts, prominent Sufi figures, Sufi orders, and popular topics. Users can exchange ideas freely and connect with others who are interested in these subjects.

This project allows users to browse content without registration; however, actions like adding content, commenting, following others, and messaging require membership.

The project is divided into three main Django applications:

- **Pages:** This app handles static and publicly accessible pages such as the home page, about page, and other similar pages. It also enables users to perform actions like searching, filtering content, and interacting with other publicly available features.

- **User:** This app manages user-related features such as profile creation, authentication, notification management, and similar functionalities. It also handles user interactions, including following others, messaging, sending notifications, and other related tasks.

- **Content:** This app deals with operations related to content creation, editing, deletion, commenting, liking, content filtering, and other content management activities.

The technical features of the project include custom authentication, middleware for unread messages and notifications, a rich text editor tool called **CKEditor 5**, and similar functionalities. On the frontend, **Bootstrap 5** is used for responsive design, while the backend is powered by **Django**.

## Purpose of the Project
The primary goal of the **Everything About Sufism** platform is to bring together individuals who wish to gain deeper knowledge about Sufism and engage in meaningful discussions.

**Features for Non-Members:**
- Access all available content.
- Filter content by topic and type.
- Use the site's search functionality.
- Communicate with the site administration via the contact section.

**Features for Members:** In addition to the features available to non-members, members can:
- Create and share content under various Sufi-related topics.
- Comment on content, leave likes, and interact with other members.
- Create a profile and upload a profile picture.
- Explore other members' profiles, follow them, and send private messages.
- Receive instant notifications for interactions related to their activities.
- Filter content based on members they follow.
- Change or reset their password using their email address.

## Technologies and Tools
### Core Frameworks and Libraries
- **Django (5.0.6):** Backend framework for building robust web applications.
- **asgiref (3.8.1):** Provides support for Django's asynchronous capabilities, enabling efficient handling of asynchronous requests and background tasks.

### Frontend Tools and Libraries
- **Bootstrap 5:** Frontend framework for responsive and mobile-first design, used for form rendering and styling.
- **django-crispy-forms (2.2):** Simplifies form management and rendering in Django, providing Bootstrap-compatible form styling.
- **Crispy-Bootstrap5 (0.7):** Provides Bootstrap 5-compatible form styling for Django and is used together with **django-crispy-forms**.

### Text and Content Management
- **django-ckeditor-5 (0.2.13):** A rich text editor with extensive customization options, including a custom toolbar, color palette, and image upload support.

### Environment and Configuration
- **django-environ (0.11.2)**: Used for handling environment variables in a secure and convenient way.
- **dotenv:** Loads environment variables from the `.env` file securely using the `python-dotenv` package. It is used in integration with `django-environ` in the project.

### Data and Storage
- **sqlite3:** Default database used for development. In production, a more robust database (e.g., PostgreSQL) is recommended.
- **Pillow (11.0.0)**: Python Imaging Library for image processing.
- **sqlparse (0.5.3)**: Library for parsing SQL statements.
- **tzdata (2024.2)**: Timezone data for handling time-related functionalities.

### Custom Features and Middleware
- **Custom Middleware:** Includes:
    - **UnreadMessagesMiddleware:** Tracks unread messages for users.
    - **UnreadNotificationsMiddleware:** Manages unread notifications.
    - **VerificationRequiredMiddleware:** Ensures users are verified before performing certain actions.
- **Custom Authentication Backend:** Implements email-based authentication through the `user.auth_backends.EmailBackend` to manage user login.
- **Media Management:** Manages user-uploaded media files (e.g., profile pictures) using the `MEDIA_URL` and `MEDIA_ROOT` settings in Django.

## Features
- **User Interactions:** Users can comment on and like content, follow other users, and send private messages.
- **Notification System:** Users receive instant notifications for interactions involving them.
- **Content Filtering:** Content can be filtered by topic, type, or followed users.
- **Search Functionality:** Users can quickly search the site to find desired content.
- **Profile Creation:** Users can create their profiles, follow other users, and view others' profiles.

## Setup and Running
To run your project in the development environment, follow the steps below:

### 1. Clone the Repository:
First, clone the project to your local machine:
```bash
git clone https://github.com/mahmutulucan/everything_about_sufism.git
cd everything_about_sufism
```

### 2. Create and Activate a Virtual Environment:
Then, create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate
```

### 3. Install Required Dependencies:
To install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure the `.env` File:
The project uses environment variables stored in a `.env` file for sensitive settings like **email configurations**, **security keys**, and **database details**. To set this up:

1. Copy the [.env.example](.env.example) file to create your own `.env` file:
```bash
cp .env.example .env
```

2. The [.env.example](.env.example) file is preconfigured for **SQLite** (default for local development). If you wish to use **PostgreSQL** or **MySQL**, you can set the `DATABASE_URL` environment variable or directly configure the database settings by uncommenting and modifying the appropriate lines. The configuration for all three options (SQLite, PostgreSQL, MySQL) is included in the [.env.example](.env.example) file:

    - **SQLite** (default configuration for local development):
    ```bash
    DATABASE_ENGINE=django.db.backends.sqlite3
    DATABASE_NAME=db.sqlite3  # SQLite database file (default name)
    ```
    - **PostgreSQL**:
    ```bash
    # DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>  # Uncomment this line to use PostgreSQL
    ```
    If using PostgreSQL, ensure that the `DATABASE_URL` is set correctly. If `DATABASE_URL` is not set, you can configure PostgreSQL directly by uncommenting the PostgreSQL configuration block.
    - **MySQL**:
    ```bash
    # DATABASE_ENGINE=django.db.backends.mysql  # Uncomment this line to use MySQL
    # DATABASE_NAME=<DB_NAME>  # Example: my_database_name
    # DATABASE_USER=<DB_USER>  # Example: my_database_user
    # DATABASE_PASSWORD=<DB_PASSWORD>  # Example: my_secure_password
    # DATABASE_HOST=<DB_HOST>  # Example: randomhost12345.com
    # DATABASE_PORT=<DB_PORT>  # Example: 3306
    ```
    If you choose to use MySQL, uncomment the MySQL configuration block and update the details.

By default, if neither DATABASE_URL nor the direct database settings are provided, SQLite will be used.

Update the `.env` file with your desired database settings based on these examples.

### 5. Database Migrations:
When running the project for the first time or making changes to the models, you will need to apply database migrations to update the database schema.
    1. **Create Migration Files:**
    ```bash
    python manage.py makemigrations
    ```
    2. **Apply Migrations to the Database:**
    ```bash
    python manage.py migrate
    ```
These steps will update your database schema with the changes made to the models and ensure that the application works properly.

### 6. Create a Superuser:
Create a superuser (administrator) for the project:
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files:
Run the following command to collect static files for your project:
```bash
python manage.py collectstatic
```
This will gather all static files, including those from third-party apps like **django-ckeditor-5** and Django's admin interface, into the `STATIC_ROOT` directory.

**Note:** This step is required for CKEditor and other static files to work properly, even during development.

**Note:** `staticfiles/` folder is automatically generated using the collectstatic command and is excluded from version control via `.gitignore`. This ensures that only necessary static files are served, reducing repository size and avoiding duplication.

### 8. Start the Server:
Start the development server:
```bash
python manage.py runserver
```

You can now access the project at http://127.0.0.1:8000.

## Special Settings
The project requires the `.env` file for various features to work. Ensure that you include the following information in this file:

- **Email server settings:** For email verification and password reset
- **Security keys and secrets:** To enable Django's security features, such as signing cookies and sessions.
- **Don't forget to set `DEBUG=False` in the production environment** to ensure security and prevent sensitive information from being exposed.

## Static Folder
The `static/` folder contains essential files required for the project, such as:

- **Images (`img/`):** Contains static images used in the project, including the default profile picture (`default_profile_pic.jpg`).
- **CSS (`css/`) and JS (`js/`):** Contains Bootstrap files and other custom stylesheets or scripts.
- **Favicon (`favicon.ico`):** The icon displayed in the browser tab for the site.

## Media Folder Setup
Since the `media/` folder is ignored by Git (via `.gitignore`), it won't be included when you clone the project from GitHub. The `media/` folder is essential for storing user-uploaded content, such as profile pictures and other media files.

### Why This Is Necessary
The `media/` folder is essential for handling user-uploaded content such as profile pictures and other files related to the content added by users. Without this folder and its structure, uploaded files won't be saved correctly. Follow these steps to ensure proper configuration:

### Steps to Set Up the Media Folder
1. **Create the `media/` folder:** In your project root directory, create the `media/` folder if it doesn't already exist:
```bash
mkdir media
```

2. **Create the `profile_pics/` folder inside `media/`:** Inside the `media/` folder, create the `profile_pics/` folder where the uploaded profile pictures will be stored:
```bash
mkdir media/profile_pics
```

3. **Create the `content_images/` folder inside `media/`:** Similarly, create the `content_images/` folder to store images that users upload with their content:
```bash
mkdir media/content_images
```

4. **Default Profile Picture:** The project uses a default profile picture if the user has not uploaded one. This default image is stored in the `static/` directory as `static/img/default_profile_pic.jpg`. When a user does not upload a profile picture, this image will be used automatically. Ensure this file exists in the `static/` directory.

5. **Content Images Default Mapping:** If a user doesn't upload an image for their content, the project uses a default image based on the content type. These default images are stored in the `static/img/` directory. The `get_image_url` function in the `Content` model will return a default image for each content type. The mapping is as follows:

- **Academic Article:** `static/img/academic_article.jpg`
- **Insightful Essay:** `static/img/insightful_essay.jpg`
- **Sufi Experience:** `static/img/sufi_experience.jpg`
- **Question and Answer:** `static/img/question_answer.jpg`
- **Book Review:** `static/img/book_review.jpg`
- **Other Types:** `static/img/default.jpg`

Ensure these images exist in the `static/img/` directory, as the project uses them when no content image is uploaded.

This setup ensures that user-uploaded profile pictures and content images are stored properly, and the default profile and content images are used when needed.

## Note on `.gitignore`
The project’s `.gitignore` file excludes certain files and directories to keep the repository clean and secure. Here's why they are excluded:

- `venv/`, `env/`: Virtual environments are user-specific and should be created locally.
- `db.sqlite3`: The database file is excluded for security and to encourage setting up local or production-ready databases.
- `media/`: This folder contains user-uploaded files and needs to be created locally.
- `staticfiles/`: Static files are generated via the `collectstatic` command, avoiding redundancy in the repository.

## Contributing
If you would like to contribute to the project, please check the [CONTRIBUTING](CONTRIBUTING.md) file for detailed contribution steps and software guidelines.

While contributing, please consider the security requirements of the software.

## License
This project is licensed under the **MIT License**. For detailed terms and conditions, please refer to the [LICENSE](LICENSE.txt) file.

## Contact
If you have any questions or need further information about the project, please don't hesitate to contact me at: **everythingaboutsufism@gmail.com**
