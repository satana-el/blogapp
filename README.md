# <kernelnotes.blog>
#### Video Demo:  <https://youtu.be/xEgA1NS5EgA>
#### Description:
A minimalist blogging website written with flask. Users can create accounts, read and write blogs.

Welcome to your Flask-based Blogging Website! This application allows users to create, edit, and share blog posts. Additionally, users can manage their accounts, including profile information and security settings.

I have used flask for this project because it just renders html pages, it is low on resources. I used the app factory layout because version control is easier with it.

## Installation

To set up the Flask Blogging Website, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/satana-el/kernalnotes.blog
    cd kernalnotes.blog
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create the database:

    ```bash
    flask db init
    ```

4. Run the application:

    ```bash
    flask run
    ```

The application will be accessible at `http://127.0.0.1:5000/` by default.

## Usage

1. Navigate to the registration page (`/register`) to create an account.
2. Log in with your credentials at the login page (`/login`).
3. Explore the blogging features, create, edit, and view posts at the blog section (`/blog`).
4. Manage your account settings, including bio, profile, and monetization preferences, at the account section (`/account`).

## Directory Structure

The project is organized as follows:
```bash
├── app
│   ├── account.py
│   ├── auth.py
│   ├── blog.py
│   ├── db.py
│   ├── __init__.py
│   ├── schema.sql
│   ├── static
│   │   ├── bootstrap.bundle.min.js
│   │   ├── bootstrap.min.css
│   │   ├── pics
│   │   │   ├── baseline_rss_feed_black_24dp.png
│   │   │   ├── baseline_rss_feed_white_24dp.png
│   │   │   ├── btc.webp
│   │   │   └── xmr.webp
│   │   └── style.css
│   └── templates
│       ├── account
│       │   ├── bio.html
│       │   ├── blogs.html
│       │   ├── btc.html
│       │   ├── monetization.html
│       │   ├── profile.html
│       │   └── xmr.html
│       ├── account.html
│       ├── auth
│       │   ├── change_password.html
│       │   ├── change_username.html
│       │   ├── login.html
│       │   └── register.html
│       ├── blog
│       │   ├── create.html
│       │   ├── edit.html
│       │   ├── index.html
│       │   ├── not_found.html
│       │   └── post.html
│       └── layout.html
├── instance
│   └── app.sqlite
├── LICENSE
├── README.md
└── requirements.txt
```

## Features

- User Registration and Authentication
- Blog Post Creation and Editing
- Account Management
  - Bio, Profile, and Monetization Settings
- Responsive Design with Bootstrap
- Static Assets for Styling

## Contributing

Feel free to contribute to the development of this Flask Blogging Website. Follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## License

This project is licensed under the [GPL v3](LICENSE). Feel free to use, modify, and distribute it as needed. Just make sure your changes are under the same license.


**TODO**
1. Add comments
2. Fiat Monetization
3. Tags
4. Search functionality
