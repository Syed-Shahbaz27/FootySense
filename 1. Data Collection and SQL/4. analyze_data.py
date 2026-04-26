import sqlite3
# Connect to  existing database (footysense.db file) 
conn = sqlite3.connect('footysense.db')
cursor = conn.cursor()

#Question 1: Which team plays at Stamford Bridge?
cursor.execute("SELECT name from teams WHERE venue = 'Stamford Bridge'")
result_1 = cursor.fetchone()
print("Question 1: Which teams plays at StamFord Bridge?\n")
print(result_1[0]) # Extract just the name from the tuple

# Question 2: Who scored the most goals?
cursor.execute("SELECT player_name FROM scorers WHERE goals = (SELECT MAX(goals) FROM scorers)")
print("Who is the top goalscorer this season? \n")
result_2 = cursor.fetchone()
print(result_2[0])

# Question 3: What's the total goals from all scorers?
cursor.execute("SELECT SUM(goals) FROM scorers")
result_3 = cursor.fetchone()
print("\nQuestion 3: total goals")
print(result_3[0] )

conn.close()
