-- Query the sum of film durations
SELECT SUM(duration) AS total_duration
FROM films;

-- Calculate the average duration of all films
SELECT AVG(duration) AS average_duration
FROM films;

-- Find the latest release_year
SELECT MAX(release_year) AS latest_year
FROM films;

-- Find the duration of the shortest film
SELECT MIN(duration) AS shortest_film
FROM films;

Combining aggregate functions with WHERE
When combining aggregate functions with WHERE, you get a powerful tool that allows you to get more granular with your insights, for example, to get the total budget of movies made from the year 2010 onwards.

This combination is useful when you only want to summarize a subset of your data. In your film-industry role, as an example, you may like to summarize each certification category to compare how they each perform or if one certification has a higher average budget than another.

Let's see what insights you can gain about the financials in the dataset.

-- Calculate the sum of gross from the year 2000 or later
SELECT SUM(gross) AS total_gross
FROM films
WHERE release_year >= 2000;

-- Calculate the average gross of films that start with A
SELECT AVG(gross) AS avg_gross_A
FROM films
WHERE title LIKE 'A%';

-- Calculate the lowest gross film in 1994
SELECT MIN(gross) AS lowest_gross
FROM films
WHERE release_year = 1994;

-- Calculate the highest gross film released between 2000-2012
SELECT MAX(gross) AS highest_gross
FROM films
WHERE release_year BETWEEN 2000 AND 2012;

-- Round the average number of facebook_likes to one decimal place
SELECT ROUND(AVG(facebook_likes), 1) AS avg_facebook_likes
FROM reviews;

ROUND() with a negative parameter
A useful thing you can do with ROUND() is have a negative number as the decimal place parameter. This can come in handy if your manager only needs to know the average number of facebook_likes to the hundreds since granularity below one hundred likes won't impact decision making.

Social media plays a significant role in determining success. If a movie trailer is posted and barely gets any likes, the movie itself may not be successful. Remember how 2020's "Sonic the Hedgehog" movie got a revamp after the public saw the trailer?

Let's apply this to other parts of the dataset and see what the benchmark is for movie budgets so, in the future, it's clear whether the film is above or below budget.

-- Calculate the average budget rounded to the thousands
SELECT ROUND(AVG(budget), -3) AS avg_budget_thousands
FROM films;

Aliasing with functions
Aliasing can be a lifesaver, especially as we start to do more complex SQL queries with multiple criteria. Aliases help you keep your code clean and readable. For example, if you want to find the MAX() value of several fields without aliasing, you'll end up with the result with several columns called max and no idea which is which. You can fix this with aliasing.

Now, it's over to you to clean up the following queries.

-- Calculate the title and duration_hours from films
SELECT title, duration / 60.0 AS duration_hours
FROM films;

-- Calculate the percentage of people who are no longer alive
SELECT COUNT(deathdate) * 100.0 / COUNT(*) AS percentage_dead
FROM people;

-- Find the number of decades in the films table
SELECT (MAX(release_year) - MIN(release_year)) / 10.0 AS number_of_decades
FROM films;
-- Round duration_hours to two decimal places
SELECT title, ROUND(duration / 60.0, 2) AS duration_hours
FROM films;

