# LoginLogoutTracker

LoginLogoutTracker is a simple Python application that allows you to record user login and logout times and generate reports.

## Features

- **User login/logout recording:** Record the login and logout times of users.
- **Display user sessions:** View the current user sessions along with their login and logout times.
- **Generate report:** Generate a report of all user sessions and export it to an Excel file.

## Requirements

- Python 3.x
- `openpyxl` library (for Excel file manipulation)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ajmalrasouli/LoginLogoutTracker.git
    ```

2. **Install the required dependencies:**

    ```bash
    pip install openpyxl
    ```

## Usage

1. **Run the `LoginLogoutTracker.py` script:**

    ```bash
    python LoginLogoutTracker.py
    ```

2. **Follow the on-screen prompts to interact with the application:**
   - Enter 1 to login a user.
   - Enter 2 to logout a user.
   - Enter 3 to display user sessions.
   - Enter 4 to generate a report and export it to an Excel file.
   - Enter 5 to exit the application.

## Database

- The application uses SQLite as the database to store user sessions.
- The database file is named `user_sessions.db`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
