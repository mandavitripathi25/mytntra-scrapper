# mytntra-scrapper
# 🛍️ Myntra Scraper

A Python-based web scraping project that extracts product information from Myntra using Selenium and BeautifulSoup. The scraped data can be analyzed, visualized, or stored in a database for further processing.

## 🚀 Features

- Scrape product details from Myntra
- Extract:
  - Product Name
  - Brand
  - Price
  - Discount
  - Ratings
  - Product URL
  - Product Image URL
- Store data in a database
- Interactive dashboard using Streamlit
- Data visualization with Plotly
- Environment variable support using `.env`

---

## 🛠️ Tech Stack

- Python 3.10+
- Selenium
- BeautifulSoup (bs4)
- Pandas
- NumPy
- Streamlit
- Plotly
- Flask-CORS
- Gunicorn

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

### Requirements

```text
bs4==0.0.1
chromedriver-binary==121.0.6115.2.0
database-connect==0.1.66
flask-cors==4.0.0
gunicorn==21.2.0
ipykernel==6.26.0
numpy==1.24.4
pandas==2.0.3
plotly==5.18.0
pysocks==1.7.1
python-dotenv==1.0.1
selenium==4.15.2
streamlit==1.28.0
tiktoken==0.4.0
```

---

## 📁 Project Structure

```
myntra-scraper/
│
├── app.py                  # Streamlit application
├── scraper.py              # Selenium scraping logic
├── database.py             # Database connection
├── utils.py                # Helper functions
├── .env                    # Environment variables
├── requirements.txt
├── README.md
└── data/
    └── products.csv
```

---

## ⚙️ Configuration

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_database_connection_string
```

---

## ▶️ Running the Project

### Run the scraper

```bash
python scraper.py
```

### Run the Streamlit Dashboard

```bash
streamlit run app.py
```

---

## 📊 Sample Output

| Brand | Product | Price | Rating |
|--------|---------|-------|--------|
| Nike | Running Shoes | ₹2,999 | 4.5 |
| Puma | Sneakers | ₹1,999 | 4.3 |
| Adidas | T-shirt | ₹999 | 4.4 |

---

## 📈 Dashboard

The Streamlit dashboard provides:

- Product Listings
- Price Analysis
- Brand-wise Comparison
- Interactive Charts
- Search & Filter Options

---

## 🔧 Technologies Used

| Library | Purpose |
|----------|----------|
| Selenium | Browser Automation |
| BeautifulSoup | HTML Parsing |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| Plotly | Interactive Charts |
| Streamlit | Dashboard |
| Flask-CORS | API CORS Support |
| Gunicorn | Production Deployment |
| dotenv | Environment Variables |

---

## ⚠️ Disclaimer

This project is intended **only for educational and learning purposes**.

Please respect Myntra's Terms of Service and robots.txt. Avoid sending excessive requests that may affect their servers.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

