# Olympic Games History - Interactive Dashboard

![Olympic Rings](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/1200px-Olympic_rings_without_rims.svg.png)

This project is an interactive web application built with Streamlit that analyzes historical data of the Olympic Games. The dashboard allows users to explore various statistics, including medal tallies, participation trends, and athlete demographics from 1896 to 2016.

The application fetches data from a MySQL database, which is populated by a Python script that cleans and processes a raw CSV file containing over 250,000 records.

## Features

The dashboard is organized into four main sections for a comprehensive analysis:

*   **Medal Tally:**
    *   View the number of Gold, Silver, and Bronze medals won by each country.
    *   Filter the tally by a specific year or view the overall historical count.
    *   Filter results for a single country's performance.

*   **Overall Analysis:**
    *   Display top-level statistics such as the total number of Olympic editions, host cities, sports, and participating nations.
    *   Visualize trends over time, including the growth in the number of participating countries and events per edition.

*   **Country-wise Analysis:**
    *   Select a country to see a detailed breakdown of its performance over the years.
    *   View an interactive line chart showing the country's medal count over time.
    *   See a list of the top 10 sports where the country has won the most medals.

*   **Athlete Analysis:**
    *   Analyze the distribution of athlete attributes like age, height, and weight through interactive histograms and scatter plots.
    *   Filter the Height vs. Weight analysis by sport to discover trends specific to different athletic disciplines.

## Technologies Used

This project utilizes a modern data stack for processing, storage, and visualization:

*   **Backend & Data Processing:** Python
*   **Data Manipulation:** Pandas
*   **Database:** MySQL
*   **Web Framework:** Streamlit
*   **Data Visualization:** Plotly Express
*   **Database Connector:** `mysql-connector-python`

## Dataset

The project uses the "120 years of Olympic history: athletes and results" dataset, which contains detailed records of every athlete's participation in the Olympic Games.

**Data Cleaning Steps Performed:**
1.  Rows with missing values for `Age`, `Height`, or `Weight` were dropped to ensure data quality for athlete analysis.
2.  The `Sex` column was mapped from ('M', 'F') to ('Male', 'Female') for better readability.
3.  The `Medal` column's `NaN` values were replaced with 'No Medal' to represent non-medal-winning participations.

## Local Setup and Installation

To run this project on your local machine, follow these steps.

### 1. Prerequisites

*   Python 3.8 or higher
*   MySQL Server
*   Git

### 2. Clone the Repository

```
git clone https://github.com/Pankajsh3002/Web-Application.git
cd olympic-analysis-dashboard
```

### 3. Set Up the Database

First, you need to populate the MySQL database.
*   Save the initial Python script you created (for connecting to MySQL and inserting data) as `setup_database.py`.
*   Place your `Olympic History.csv` file in the correct path as specified in the script.
*   Run the script to create the database, table, and insert the data:

```
python setup_database.py
```
**Note:** Ensure your MySQL server is running and the credentials (`host`, `user`, `password`) in the script are correct.

### 4. Install Dependencies

Create a `requirements.txt` file with the following content:

```
pandas
streamlit
plotly
mysql-connector-python
```

Then, install the required packages using pip:

```
pip install -r requirements.txt
```

### 5. Run the Streamlit App

Once the database is ready and dependencies are installed, run the Streamlit application:

```
streamlit run app.py
```
