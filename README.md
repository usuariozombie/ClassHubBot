### Discord Class Schedules Bot

This bot is a Discord bot that allows users to add, show, edit, and delete class schedules.

**Usage:**

* To add a schedule, use the `/add` command.
* To show schedules, use the `/show` command.
* To edit a schedule, use the `/edit` command.
* To delete a schedule, use the `/delete` command.

**Commands:**

| Command | Description |
|---|---|
| `/add` | Add a schedule. |
| `/show` | Show schedules. |
| `/edit` | Edit a schedule. |
| `/delete` | Delete a schedule. |
| `/help` | Show help. |

**Example:**

To add a schedule for Monday at 9:00 AM for the subject "Math", you would use the following command:

```
/add Monday 09:00 Math
```

To show all schedules, you would use the following command:

```
/show
```

To edit a schedule for Monday at 9:00 AM to the subject "Computer Science", you would use the following command:

```
/edit Monday 09:00 Computer Science
```

To delete a schedule for Monday at 9:00 AM, you would use the following command:

```
/delete Monday 09:00
```

**Requirements:**

* Python 3.8 or higher
* Discord.py 2.0 or higher
* Requests library

**Installation:**

1. Clone this repository.

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Create a Discord bot account and obtain your bot token.
   
4. Replace the `TOKEN` placeholder in the `main.py` file with your bot token.
   
5. Replace the `API_BASE_URL` placeholder in the `main.py` file with the URL of your Spring Boot server API.
   
6. Start the bot:

```
python main.py
```

**Contributing:**

Feel free to contribute to this project by submitting bug reports and feature requests. You can also contribute by adding new features or fixing bugs.

**License:**

This project is licensed under the MIT License.
