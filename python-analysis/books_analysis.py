Amazon Bestseller Books Data Analysis
# This Python script analyzes a dataset of Amazon bestselling books from 2009–2019.
# The script imports the dataset, inspects the structure of the data, and performs
# cleaning steps such as standardizing column names, checking for missing values,
# and formatting numeric variables. After preparing the dataset, the script conducts
# descriptive analysis to explore patterns in user ratings, number of reviews,
# book prices, genres, and publication years. The results of this analysis help
# identify trends in reader engagement and book popularity, which are later
# visualized in an interactive Tableau dashboard and summarized in a presentation.
 #=====================================================
# INTRODUCTION
# The script analyzes the Bestselling Books dataset.
# It loads the dataset, inspects the data, prepares it
# for analysis, performs descriptive statistics, and
# exports summary files for further analysis.
# =====================================================

import pandas as pd


# =====================================================
# DATA LOADING
# =====================================================

books = pd.read_csv("bestsellers with categories.csv")

print("Columns in dataset:\n", books.columns)
print("\nPreview of dataset:\n", books.head())


# =====================================================
# INSPECT DATA STRUCTURE
# =====================================================

print("\nDataset Info:")
books.info()

print("\nNumber of Rows:", len(books))
print("\nDataset Shape:", books.shape)

print("\nStatistical Summary:\n", books.describe())


# =====================================================
# MAKE COLUMNS CONSISTENT
# =====================================================

# Standardize column names
books.columns = books.columns.str.lower().str.replace(" ", "_")

print("\nUpdated Column Names:\n", books.columns)


# =====================================================
# CLEAN AND PREPARE DATA FOR ANALYSIS
# =====================================================

# Check for missing values
print("\nMissing values in each column:\n", books.isnull().sum())

# Remove duplicate rows
books = books.drop_duplicates()

print("\nRows after removing duplicates:", len(books))

# Ensure numeric columns are correct
books["user_rating"] = pd.to_numeric(books["user_rating"])
books["reviews"] = pd.to_numeric(books["reviews"])
books["price"] = pd.to_numeric(books["price"])


# Create additional fields for analysis

# Rating category
books["rating_category"] = books["user_rating"].apply(
    lambda x: "High Rating" if x >= 4.7 else "Moderate Rating"
)

# Price category
books["price_category"] = books["price"].apply(
    lambda x: "Low Price" if x <= 10 else "High Price"
)

print("\nPreview after creating new columns:\n", books.head())


# =====================================================
# DESCRIPTIVE ANALYSIS
# =====================================================

# Books by genre
print("\nBooks by Genre:\n", books["genre"].value_counts())

# Books per year
print("\nBooks Published Per Year:\n", books["year"].value_counts().sort_index())

# Top authors with most bestselling books
print("\nTop Authors:\n", books["author"].value_counts().head(10))

# Average user rating
print("\nAverage User Rating:", books["user_rating"].mean())

# Most reviewed books
print("\nMost Reviewed Books:\n",
      books.sort_values(by="reviews", ascending=False).head(10))

# Highest rated books
print("\nHighest Rated Books:\n",
      books.sort_values(by="user_rating", ascending=False).head(10))

# Price distribution
print("\nPrice Distribution:\n", books["price"].value_counts().head(10))


# =====================================================
# ANALYZE RELATIONSHIPS BETWEEN VARIABLES
# =====================================================

# Average rating by genre
print("\nAverage Rating by Genre:\n",
      books.groupby("genre")["user_rating"].mean())

# Average price by genre
print("\nAverage Price by Genre:\n",
      books.groupby("genre")["price"].mean())

# Average number of reviews by genre
print("\nAverage Reviews by Genre:\n",
      books.groupby("genre")["reviews"].mean())

# Books by rating category
print("\nBooks by Rating Category:\n",
      books["rating_category"].value_counts())

# Books by price category
print("\nBooks by Price Category:\n",
      books["price_category"].value_counts())


# =====================================================
# CREATE SUMMARY TABLES FOR VISUALIZATION
# =====================================================

# Books by genre
genre_summary = books.groupby("genre").size().reset_index(name="book_count")

# Average rating by genre
rating_summary = books.groupby("genre")["user_rating"].mean().reset_index()

# Average price by genre
price_summary = books.groupby("genre")["price"].mean().reset_index()

# Books per year
year_summary = books.groupby("year").size().reset_index(name="books_per_year")


# =====================================================
# EXPORT FILES FOR FURTHER ANALYSIS
# =====================================================

# Export cleaned dataset
books.to_csv("cleaned_books_dataset.csv", index=False)

# Export summaries
genre_summary.to_csv("genre_summary.csv", index=False)
rating_summary.to_csv("rating_summary.csv", index=False)
price_summary.to_csv("price_summary.csv", index=False)
year_summary.to_csv("year_summary.csv", index=False)
