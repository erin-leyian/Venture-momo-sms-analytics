# MoMo SMS Analytics Dashboard

## Project Description
This project processes MoMo SMS data in XML format, cleans and categorizes the transactions, stores them in a relational database (SQLite), and provides a simple frontend dashboard to analyze and visualize the data.

## Team Members
- Erin Leyian
- Kenny Gael Ishimwe Gatete
- Belyse INTWAZA

## High-Level System Architecture
Architecture diagram:
https://drive.google.com/file/d/1LdLmCNTx0AVMPfHcpYz2l_qiHtIG0kzN/view?usp=gmail

Flow (high level):
- XML input (MoMo SMS) → ETL pipeline (parse, clean, categorize)
- Store transactions in SQLite database
- Export aggregated analytics to JSON
- Frontend dashboard reads JSON and visualizes insights

## Scrum Board
(I will add the Scrum board link here once created.)

## Planned Project Structure
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── db.sqlite3
│   └── logs/
├── etl/
├── api/
├── scripts/
└── tests/
