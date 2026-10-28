# 💰 SmartSpend — Personal Finance & Expense Analytics

SmartSpend is a Python-based personal finance management application designed to help users track their income, manage expenses, understand spending patterns, and forecast upcoming expenses.

Built with Streamlit, SQLite, Pandas, Plotly, and Scikit-learn, SmartSpend provides an interactive financial dashboard, transaction management, visual analytics, and machine learning-based expense prediction in one application.

## ✨ Features

### 📊 Financial Dashboard
- View total income and expenses.
- Monitor your current financial balance.
- Calculate your savings rate.
- Understand your overall financial position through dashboard metrics.

### 💸 Income and Expense Management
- Add income and expense transactions.
- Record transaction amounts, categories, dates, and descriptions.
- Organize transactions into categories such as food, travel, shopping, education, bills, healthcare, and entertainment.
- View and delete recorded transactions.

### 📈 Spending Analytics
- Visualize financial activity using interactive charts.
- Analyze spending by category.
- Explore weekly and monthly spending patterns.
- Identify trends to make more informed financial decisions.

### 🔮 Expense Prediction
- Forecast next week's expenses using Linear Regression.
- Analyze historical weekly expense totals.
- Generate predictions when sufficient historical data is available.
- Display the estimated upcoming weekly spending.

### 🔐 User Authentication
- Register a user account.
- Log in to an existing account.
- Associate transactions with individual users.
- Provide separate user and administrator experiences.

### 🛠️ Administrator Dashboard
- View registered users.
- Monitor transactions across the application.
- Review overall financial activity and system statistics.
- Restrict administrator-only sections to authorized admin accounts.

### 📥 Transaction Export
- Download transaction records as a CSV file.
- Use exported data for external analysis and personal record keeping.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web application interface |
| SQLite | Persistent relational database |
| Pandas | Data processing and financial calculations |
| Plotly | Interactive financial visualizations |
| Scikit-learn | Expense forecasting using Linear Regression |
| HTML/CSS | Custom interface styling within Streamlit |

## 🏗️ Application Architecture

SmartSpend follows a simple application architecture in which the user interface communicates with Python modules that process data and interact with the SQLite database.

```text
             User
              |
              v
      Streamlit Interface
              |
       +------+------+
       |             |
       v             v
   Analytics     Prediction
       |             |
       +------+------+
              |
              v
       Database Module
              |
              v
         SQLite DB
        (finance.db)
```

The application separates database operations, financial calculations, and prediction logic into different Python modules.

## 🔄 How It Works

1. **Register or log in:** Users access the application through the authentication interface.
2. **Record transactions:** Add income or expenses with amounts, categories, dates, and descriptions.
3. **Store data:** Transaction records are saved in the SQLite database and associated with the relevant user.
4. **Calculate financial summaries:** The application calculates total income, expenses, balance, and savings rate.
5. **Visualize spending:** Interactive charts help users understand their financial habits.
6. **Forecast future expenses:** A Linear Regression model uses historical weekly expense totals to estimate next week's spending.
7. **Manage records:** Users can view, delete, and export their transactions, while administrators can access system-wide information.

## 🧮 Expense Prediction Method

SmartSpend uses the `LinearRegression` model from Scikit-learn to estimate next week's expenses.

The prediction process is:

1. Select transactions classified as expenses.
2. Convert transaction dates into weekly periods.
3. Calculate the total expenses for each week.
4. Assign sequential week numbers.
5. Train a linear regression model on weekly totals.
6. Predict the expense total for the next week.

The application requires at least two weeks of expense data before generating a prediction.

**Note:** Predictions are estimates based on historical spending patterns, not guaranteed future expenses.

## 📁 Project Structure

```text
PremWirle/
├── .devcontainer/
│   └── devcontainer.json
├── data/
│   ├── .gitignore
│   ├── .gitkeep
│   ├── app.py
│   ├── database.py
│   ├── analytics.py
│   ├── prediction.py
│   └── requirements.txt
└── README.md
```

### Module Responsibilities

- `app.py` — Main Streamlit interface, authentication flow, dashboard, transaction management, charts, prediction page, and admin dashboard.
- `database.py` — SQLite database initialization, user registration and login, transaction operations, and administrator data retrieval.
- `analytics.py` — Calculates income, expenses, balance, and savings rate.
- `prediction.py` — Implements weekly expense forecasting using Linear Regression.
- `requirements.txt` — Lists the Python packages required by the application.
- `.devcontainer/devcontainer.json` — Development container configuration.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or another version compatible with your installed dependencies.
- Git.
- pip.

### 1. Clone the repository

```bash
git clone https://github.com/prem45-tech/PremWirle.git
cd PremWirle
```

### 2. Navigate to the application directory

```bash
cd data
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use SmartSpend.

The SQLite database is configured at `data/finance.db` relative to the application's working directory. The application initializes its database tables when it starts.

## 📦 Dependencies

The project uses the following Python packages:

- `streamlit`
- `pandas`
- `plotly`
- `scikit-learn`

SQLite support is provided through Python's built-in `sqlite3` module.

## 🔒 Security Considerations

- Use secure password hashing such as Argon2id or bcrypt for production deployments.
- Avoid hardcoded administrator credentials and require secure initial admin setup.
- Keep database files containing personal financial information out of public repositories.
- Add authorization checks to every sensitive operation.
- Validate user input and protect account sessions before deploying the application publicly.

## 🚀 Future Enhancements

Potential improvements include:

- Monthly budgets and spending limits.
- Budget threshold notifications.
- Recurring transaction management.
- Monthly savings goals.
- Advanced forecasting with additional historical features.
- PDF financial reports.
- Data visualization with customizable date filters.
- Improved account security and password recovery.
- Deployment to a cloud hosting platform.

## 🎯 Project Objective

The objective of SmartSpend is to make personal financial management simpler by combining transaction tracking, data visualization, and basic predictive analytics in an accessible web application.

## 👨‍💻 Author

**PremWirle Project**

GitHub repository: [prem45-tech/PremWirle](https://github.com/prem45-tech/PremWirle)

## 📄 License

No license is specified in this README. Add a `LICENSE` file if you intend to distribute the project under an open-source license.
