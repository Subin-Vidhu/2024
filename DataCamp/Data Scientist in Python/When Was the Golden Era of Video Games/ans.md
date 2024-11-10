-- best_selling_games
-- Select all information for the top ten best-selling games
-- Order the results from best-selling game down to tenth best-selling

SELECT *
FROM game_sales
ORDER BY games_sold DESC
LIMIT 10;

-- critics_top_ten_years
-- Select release year and average critic score for each year, rounded and aliased
-- Join the game_sales and reviews tables
-- Group by release year
-- Order the data from highest to lowest avg_critic_score and limit to 10 results

SELECT g.year, COUNT(g.name) AS num_games, ROUND(AVG(r.critic_score),2) AS avg_critic_score
FROM game_sales g
INNER JOIN reviews r
ON g.name = r.name
GROUP BY g.year
HAVING COUNT(g.name) >= 4
ORDER BY avg_critic_score DESC
LIMIT 10;

-- golden_years
-- Select year, num_games, avg_critic_score, avg_user_score and the difference between the user and critic scores as avg_score.
-- Join critics_top_ten_years and users_top_years on the year column
-- Where the average user or critic rating for the year was over 9.
-- Order data by diff in ascending order

SELECT u.year, u.num_games, c.avg_critic_score, u.avg_user_score, c.avg_critic_score - u.avg_user_score AS diff
FROM critics_avg_year_rating c
INNER JOIN users_avg_year_rating u
ON c.year = u.year
WHERE c.avg_critic_score > 9 OR u.avg_user_score > 9
ORDER BY year ASC