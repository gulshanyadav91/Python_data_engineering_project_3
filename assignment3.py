import pandas as pd
import json
from tabulate import tabulate

with open("books.json", "r", encoding="utf-8") as file:
    books = json.load(file)

df = pd.DataFrame(books['books'])
def clean_price(price):
    price = price.replace("£", "").replace("Â", "").strip()
    return float(price)

# print(clean_price("£51.77"))

df['actual_price'] = df['price'].apply(clean_price)
df['actual_price'] = df['actual_price'].astype(float)
df['inr_price']  =  df['actual_price'] * 127.15
average_price = df['actual_price'].mean()


books['books'] = df.to_dict("records")

with open("books.json", "w", encoding="utf-8") as file:
    json.dump(books, file, indent=4, ensure_ascii=False)

with open("users.json", "r", encoding="utf-8") as file:
    users = json.load(file)

df_users = pd.DataFrame(users)

print("\033[38;5;208m-------       Total records in each file (book information) :        --------", "\033[0m")
print(df)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")
print("\n")
print("\033[38;5;208m-------       Total records in each file: (user information)       --------", "\033[0m")
print(df_users)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")
print("\n")

# print(df['price'])


# print(average_price)


# df.to_json("books.json", orient="records", indent=4)


# print("\033[1;32m-------       Display all book titles with rating greater than 4 :        --------", "\033[0m")
print("\033[38;5;208m-------       Display all book titles with rating greater than 4 :        --------", "\033[0m")
resultRating = df[df['rating'] > 4][['title', 'actual_price', 'inr_price', 'rating']]
print(resultRating)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")
print("\n")

resultCompany = df_users[df_users['company'].str.contains('Group')][['name', 'email', 'company']]
print("\033[38;5;208m-------       Display all users whose company name contains 'Group' :        --------", "\033[0m")
print(resultCompany)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")
print("\n")




total_users = df_users.shape[0]
total_books = df.shape[0]

report = {
    "total_users": total_users,
    "total_books": total_books,
    "average_price": round(average_price, 2)
}


# Save report to a new JSON file
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)


print("\033[38;5;208m-------       Report saved to report.json       --------", "\033[0m")
print(report)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")
print("\n")


### User Analysis

# - Total Users
# - Unique Companies
# - Top 5 Companies (Alphabetically)

print("\033[38;5;208m-------       User Analysis       --------", "\033[0m")

total_users = df_users.shape[0]
unique_companies = df_users['company'].nunique()
top_5_companies = df_users['company'].value_counts().head(5)

print('Total Users are :', total_users)
print('Unique Companies are : ', unique_companies)
print('----------------------------------------------')
print('Top 5 Companies are : ')
# print("\033[38;5;208m-------       Top 5 Companies :        --------", "\033[0m")
print(top_5_companies)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")
print("\n")

### Book Analysis

# - Average Price
# - Highest Rated Books
# - Number of Books in Each Rating Category


average_price = df['actual_price'].mean()
highest_rated_books = df[df['rating'] == df['rating'].max()][['title', 'rating']]
rating_counts = df['rating'].value_counts().sort_index()

print("\033[38;5;208m-------       Book Analysis       --------", "\033[0m")
print('Average Price of Books :', round(average_price, 2))
print('Highest Rated Books :')
print(highest_rated_books)
print("-------------------------------------------------------------")
print('Number of Books in Each Rating Category :')
print(rating_counts)
print("\033[38;5;208m-------  -----------------------------------------------------------------------   --------", "\033[0m")



report = {
    "users": {
        "total_users": total_users,
        "unique_companies": unique_companies,
        "top_5_companies": top_5_companies.to_dict()
    },

    "books": {
        "total_books": total_books,
        "average_price": round(average_price, 2),
        "highest_rated_books": highest_rated_books.to_dict("records"),
        "rating_counts": rating_counts.to_dict()
    }
}

with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

print("\033[38;5;208m---------------- Full Report Saved to report.json ------------------\033[0m")

