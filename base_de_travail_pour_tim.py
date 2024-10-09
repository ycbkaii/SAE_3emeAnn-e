import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading the CSV file and cleaning it
data = pd.read_csv("csv/bigboss_book.csv")


variables = ['author', 'rating_count', 'review_count', 'average_rating', 'genre_and_votes', 'series', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages', 'publisher', 'date_published']

# Cleaning and keeping only the data we will use
data = data[variables]

print(data)

# We can start the analysis


# Selecting the rating columns
ratings_columns = ['five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings']

# Calculating the means and standard deviations of the ratings by star category
mean_values = data[ratings_columns].mean()
std_values = data[ratings_columns].std()

# Population size (here, we assume n = number of books in each category)
n = len(data)

# Calculating the 95% confidence interval
ci = 1.96 * std_values / np.sqrt(n)

# Creating the chart
plt.figure()
x = np.array([5, 4, 3, 2, 1])  # Star categories
y = mean_values.values

plt.plot(x, y, marker='o', linestyle='-', color='b', label='Average Ratings')
plt.fill_between(x, (y - ci), (y + ci), color='b', alpha=0.1, label='95% Confidence Interval')

# Customizing the chart
plt.xlabel('Number of Stars')
plt.ylabel('Average Number of Ratings')
plt.title('Average Number of Ratings by Star Category with 95% Confidence Interval')
plt.xticks([5, 4, 3, 2, 1], ['5 stars', '4 stars', '3 stars', '2 stars', '1 star'])
plt.legend()
plt.grid(True)

# Displaying the chart
plt.show()


# Part 2: Box Plot

# Creating the box plot
plt.figure(figsize=(10, 5))
data[ratings_columns].plot.box()
plt.title("Box Plot of Ratings by Star Category")
plt.ylabel("Number of Ratings")
plt.xticks([1, 2, 3, 4, 5], ['5 stars', '4 stars', '3 stars', '2 stars', '1 star'])
plt.grid(True)
plt.show()
