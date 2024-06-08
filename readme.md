# Sponsorenlauf (Charity Run) Tracking Software

This software is designed to track the progress of a charity run. Each participant is assigned a personal number which is used to monitor their progress throughout the event.

## Features

- **Participant Registration**: The software allows for the registration of participants, storing their names, classes, and unique codes.
- **Progress Tracking**: The software tracks the distance covered by each participant. It works be scanning the number of the participant after each round. For this we used Tyvek bands with barcodes together with barcode scanners. When a number is scanned, the software will automatically log the round and measure the time.
- **Live Scoreboard**: The software features a live score board to show the students and classes with the greatest distance.
![scoreboard](https://raw.githubusercontent.com/L-S-2020/sponsorenlauf_server/master/images/scoreboard.png)
- **Personal Analytics Site**: The students can view their personal stats (number of rounds, distance and time they took for a round) by typing their personal number on the front page.
![mainpage](https://raw.githubusercontent.com/L-S-2020/sponsorenlauf_server/master/images/mainpage.png)![personal stats](https://raw.githubusercontent.com/L-S-2020/sponsorenlauf_server/master/images/stats.png)
- **Export Functionality**: The software can export the data of all participants, including the distance they've covered, into an Excel file.

## Setup (backend)

1. Clone the repository to your local machine.
2. To add a logo replace the file in `static/assets/img`
3. Install the required Python packages using pip: `pip install -r requirements.txt`
4. Create the database (I would recommend to use a Postgresql database in production): `python manage.py migrate`
5. Create a superuser to access the admin panel: `python manage.py createsuperuser`
6. Start the server (In production you should use NGINX to host the site): `python manage.py runserver`
7. Login into the admin panel and create a school and an api key object.
8. Fill in the api key in clients/env to use the client scripts.

## Client Scripts

- `create.py`: This script is used for participant registration. It works be taking the data from an excel file and uploading them.
- `scan.py`: This script is used to scan the codes of participants and track their progress.
- `export.py`: This script is used to export the data of all participants into an Excel file.

## Technologies Used

- Python
- Django
- HTML + Bootstrap CSS (For the website part) 
- Requests library for API calls
- Pandas library for data manipulation and analysis
- dotenv library for environment variable management

## Urls

- `/` : Main page to view personal stats with the participant code
- `stats/'code'` : Display stats (you'll get redirected from main page)
- `/leaderboard` : Live score board
- `/admin`: Django admin panel
- `api/create/'name'/'class'/'code'` : Endpoint to create participant object
- `api/createklasse/'name'` : Endpoint to create class object
- `api/scanned/'code'` : Endpoint to add a round to a participant
- `api/start` : Endpoint to reset all stats and start the timers for the first round
- `api/test` : Endpoint to test if the API key is valid
- `api/leaderboard` : Get score board data for other application (only returns data when updated)
- `api/leaderboardforce` : Get score board data for other application (always returns data)
- `api/meter/'code'` : Get personal stats for export

## Used for

- Spendenlauf des Geschwister-Scholl-Gymnasium Waldkirch 2023 (Germany)
https://www.badische-zeitung.de/spendenlauf-in-waldkirch-laufen-fuer-eine-bessere-schulbildung-in-uganda
https://www.badische-zeitung.de/waldkircher-schueler-rennen-fuer-eine-oberstufe-in-schule-von-uganda


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Note

You're welcome to use this software for your own charity runs or races. If you need help for the deployment or use of the software, you have a question or just want some ideas for organizing such an event, feel free to open a commit.

## License

This project is licensed under the MIT License.