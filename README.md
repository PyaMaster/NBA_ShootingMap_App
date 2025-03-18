# NBA Analytics Web App

### Overview

This project is a Streamlit-based web application designed to provide an interactive and visually appealing way for users to explore NBA player statistics and shooting performance across different seasons. The application fetches player data, generates shooting maps, and presents statistical insights.

### Features

- 🏀 Select an NBA player from a list of all players.

- 📆 View available seasons for the selected player.

- 📊 Display detailed player statistics for a selected season.

- 🎯 Visualize shooting maps using different methods: Shot Chart, Hex Map, Shot Zones, and Heatmap.

- 💡 Interactive user interface built with Streamlit.

### File Structure
```
📂 NBA-Analytics-WebApp
├── 📄 app.py            # Main Streamlit application
├── 📄 draw_chart.py     # Functions for generating shooting maps
├── 📄 get_NBA_data.py   # Fetches player names, career stats, and shooting data
├── 📄 requirements.txt  # Python dependencies
```
### Installation

1️⃣ **Clone the repository**
```
git clone <repository-url>
cd <project-directory>
```
2️⃣ **Create a virtual environment (optional but recommended)**
```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
3️⃣ **Install dependencies**
```
pip install -r requirements.txt
```
### Running the Application 🚀

To start the Streamlit application, run:
```
streamlit run app.py
```
This will open the web app in your browser.

### Dependencies 📦

The project requires several Python libraries, listed in requirements.txt, including:

- ```streamlit```

- ```nba_api```

- ```matplotlib```

- ```seaborn```

- ```pandas```

- ```numpy```

### Credits 🙌

This project leverages the [NBA API](https://github.com/swar/nba_api) for fetching player statistics and shooting data. It’s also inspired by the [nba-shotcharts](https://github.com/hkair/nba-shotcharts) repository, which helped shape the shot chart visualizations.

### License 📜

This project is open-source and available for modification and redistribution under an appropriate license.

https://github.com/user-attachments/assets/20802c7d-c301-408a-b746-8a71c767d258
