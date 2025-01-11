# Everything About Sufism
**Everything About Sufism** is a dynamic platform where users can share content and engage in discussions about various topics related to Sufism. The platform focuses on areas such as the history of Sufism, its literature, concepts, prominent Sufi figures, Sufi orders, and popular topics. Users can exchange ideas freely and connect with others who are interested in these subjects.

This project allows users to browse content without registration; however, actions like adding content, commenting, following others, and messaging require membership.

The project is divided into three main Django applications:

- **Pages:** 
    This app handles static and publicly accessible pages such as the home page, about page, and other similar pages. It also enables users to perform actions like searching, filtering content, and interacting with other publicly available features.

- **User:** 
    This app manages user-related features such as profile creation, authentication, notification management, and similar functionalities. It also handles user interactions, including following others, messaging, sending notifications, and other related tasks.

- **Content:** 
    This app deals with operations related to content creation, editing, deletion, commenting, liking, content filtering, and other content management activities.

The technical features of the project include custom authentication, middleware for unread messages and notifications, a rich text editor tool called **CKEditor 5**, and similar functionalities. On the frontend, **Bootstrap 5** is used for responsive design, while the backend is powered by **Django**.

## Purpose of the Project
The primary goal of the **Everything About Sufism** platform is to bring together individuals who wish to gain deeper knowledge about Sufism and engage in meaningful discussions.

**Features for Non-Members:**
    Non-members can access the following features:
    - Browse and read all available content.
    - Filter content by topic and type.
    - Use the site's search functionality.
    - Contact the site administration through the contact section.

**Features for Members:**
    In addition to the features available to non-members, registered members can:
    - Create and share content under various Sufi-related topics.
    - Comment on content, leave likes, and interact with other members.
    - Create a profile and upload a profile picture.
    - Explore and follow other members’ profiles, and send private messages.
    - Receive instant notifications for interactions related to their activities.
    - Filter content based on members they follow.
    - Change or reset their password via email.

## Development vs. Production Environments
- **Development Environment:** 
    The project is configured with debug=true, using Django’s default settings for easier debugging during development.
- **Production Environment:**
    For production, additional optional settings are provided to integrate services such as Cloudinary for media storage and PostgreSQL for the database. These options are configured through environment variables in the .env file.

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
- **sqlite3:** Default database used for development. In production, a more robust database (e.g., **PostgreSQL**) is recommended.
- **Pillow (11.0.0)**: Python Imaging Library for image processing.
- **sqlparse (0.5.3)**: Library for parsing SQL statements.
- **tzdata (2024.2)**: Timezone data for handling time-related functionalities.

### Cloud and Media Management
- **Cloudinary:** Used for handling media files (images, videos) in production when `USE_CLOUDINARY=True`.
    - **django-cloudinary-storage (0.3.0):** Manages media file storage in Cloudinary for the Django project.
- **Local Media Storage:** When `USE_CLOUDINARY=False`, media files are saved locally under `MEDIA_ROOT`.

### Custom Features and Middleware
- **Custom Middleware:** Includes:
    - **UnreadMessagesMiddleware:** Tracks unread messages for users.
    - **UnreadNotificationsMiddleware:** Manages unread notifications.
    - **VerificationRequiredMiddleware:** Ensures users are verified before performing certain actions.
- **Custom Authentication Backend:** Implements email-based authentication through the `user.auth_backends.EmailBackend` to manage user login.
- **Media Management:** Manages user-uploaded media files (e.g., profile pictures) using the `MEDIA_URL` and `MEDIA_ROOT` settings in Django.

## Features
- **User Interactions:**
    - Users can comment on and like content.
    - Users can follow other users and send private messages.
- **Notification System:**
    - Users receive instant notifications for interactions involving them (e.g., comments, likes, follows).
- **Content Filtering:**
    - Content can be filtered by topic, type, or users they follow.
- **Search Functionality:**
    - Users can quickly search for content across the platform.
- **Profile Management:**
    - Users can create their profiles, upload profile pictures, follow other users, and view others' profiles.

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

2. Modify the `.env` file for your preferred database configuration:

    - **SQLite** (default configuration for local development):
    ```bash
    DATABASE_ENGINE=django.db.backends.sqlite3
    DATABASE_NAME=db.sqlite3  # SQLite database file (default name)
    ```
    - **PostgreSQL** (uncomment to use):
    ```bash
    # DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
    ```
    If you prefer using PostgreSQL, uncomment the line above and replace it with your database credentials.
    - **Cloudinary Configuration**:
        - If you want to use **Cloudinary** for media storage (production environment), set `USE_CLOUDINARY=True` and provide the `CLOUDINARY_URL`:
        ```bash
        USE_CLOUDINARY=True
        CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
        ```
        - If you prefer to use **local media storage**, set `USE_CLOUDINARY=False` (default for development):
        ```bash
        Kodu kopyala
        USE_CLOUDINARY=False
        ```

By default, if no `DATABASE_URL` or `CLOUDINARY_URL` are provided, **SQLite** and **local media storage** will be used.

### 5. Database Migrations:
Apply the necessary migrations to set up your database schema:
    1. **Create Migration Files:**
    ```bash
    python manage.py makemigrations
    ```
    2. **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```

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

**Note:** The `staticfiles/` folder is excluded from version control via `.gitignore` to reduce repository size.

### 8. Start the Server:
Start the development server:
```bash
python manage.py runserver
```

You can now access the project at http://127.0.0.1:8000.

## Special Settings
To ensure the project functions correctly, you need to configure several settings in the `.env` file. The following information is essential:

- **Email server settings:**  These are required for functionalities like email verification, password reset, and notification services.
- **Security keys and secrets:** Used to enable Django's security features, such as signing cookies, sessions, and CSRF protection. These should be securely stored in the `.env` file.
- **Set `DEBUG=False` in the production environment:** This is crucial for security purposes. Having `DEBUG=True` in production can expose sensitive information, which is a significant security risk. Make sure to set it to `False` when deploying the application in a production environment.

Additionally, make sure you configure your database settings (either **SQLite** for development or **PostgreSQL** for production) and **Cloudinary** media settings based on your environment (development or production).

## Static Folder
The `static/` folder contains essential files required for the project, organized into subdirectories for better structure and maintenance:

- **Images (`img/`):** This folder includes static images used throughout the project, including assets like the default profile picture (`default_profile_pic.jpg`) and other images used in the frontend.
- **CSS (`css/`) and JS (`js/`):** This folder contains CSS and JavaScript files, including:
    - **Bootstrap files** for styling and layout.
    - Custom stylesheets and scripts that are tailored to the project’s design and functionality.
- **Favicon (`favicon.ico`):** This file is the small icon displayed in the browser tab for the site, giving it a recognizable branding element.

These static files are essential for the frontend and are managed using Django’s static file handling system. When running the project in production, the `collectstatic` command is used to gather all static files into a single directory, making them ready to serve efficiently.

## Media Folder Setup (For Local Storage)
Since the `media/` folder is ignored by Git (via `.gitignore`), it won't be included when you clone the project from GitHub. The `media/` folder is essential for storing user-uploaded content, such as profile pictures and other media files when **Cloudinary is not used**.

### Why This Is Necessary
The `media/` folder is crucial for handling user-uploaded content, including profile pictures and other files related to user-generated content. Without this folder and its proper structure, uploaded files won't be saved correctly. Follow these steps to ensure proper configuration **if you are not using Cloudinary** for media file management:

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

### Conclusion
This setup ensures that user-uploaded profile pictures and content images are stored properly in the `media/` folder **when Cloudinary is not used**. If a user has not uploaded an image, default images will be used automatically based on the content or profile picture type.

### Cloudinary Integration (If Used)
If you are using **Cloudinary** for media management, the media files are handled differently, and they will not be stored locally. In this case, the `USE_CLOUDINARY=True` setting should be enabled in the `.env` file, and media files will be uploaded and retrieved from Cloudinary's cloud storage, bypassing the local `media/` folder entirely.

## Note on `.gitignore`
The project’s `.gitignore` file is designed to exclude certain files and directories from version control, keeping the repository clean, secure, and free of sensitive or unnecessary data. Here's why the following are excluded:

- `venv/`, `env/`: Virtual environments are specific to each developer's local environment and should be recreated locally. These folders contain installed dependencies that vary by system.
- `db.sqlite3`: The SQLite database file is excluded to prevent the inclusion of local database data and encourage the use of a production-ready or local database setup.
- `media/`: This folder contains user-uploaded files such as profile pictures and content images. Since this data is unique to each deployment, it is excluded from version control.
- `staticfiles/`: The `staticfiles/` folder contains files generated via the `collectstatic` command. These files are specific to the environment (e.g., development, production) and should not be included in the repository to avoid redundancy.

## Contributing
If you would like to contribute to the project, please refer to the [CONTRIBUTING](CONTRIBUTING.md) file for detailed guidelines on how to contribute and the software standards to follow.

While contributing, please ensure to adhere to the security requirements of the software and review any updates to the `.gitignore` or configuration files that may affect contributions.

## License
This project is licensed under the **MIT License**. For detailed terms and conditions, please refer to the [LICENSE](LICENSE.txt) file.

## Contact
If you have any questions or need further information about the project, please don't hesitate to contact me at: **everythingaboutsufism@gmail.com**
