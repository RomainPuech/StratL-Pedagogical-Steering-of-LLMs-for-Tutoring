# list of problems and their solutions



# "Country"
invention_problem = \
"""A new country has recently been founded.
The country is split into six states, call them A, B, C, D, E, and F. 
The population of state A is 1,646,000 people, the population of state B is 6,936,000 people, the population of state C is 154,000 people, the population of state D is 2,091,000 people, the population of state E is 685,000 people, and the population of state F is 988,000 people.
There are 250 seats available on a legislative body to govern the new country. 
How many seats should be assigned to each state so that each state would receive a fair representation? 
Show your work and justify why you think your method is correct."""



solution_invention = \
"""To solve this problem, we want to assign the 250 legislative seats to each state in such a way that the representation aligns as closely as possible with the population of each state. A common method to distribute seats in a way that is proportionally fair is using the method of largest remainders (also known as the Hamilton method). Here's a step-by-step process:

1. **Calculate the total population.**
   Add up the populations of all the states to find the total population of the country.

   Total population = 1,646,000 (A) + 6,936,000 (B) + 154,000 (C) + 2,091,000 (D) + 685,000 (E) + 988,000 (F)      
                     = 12,500,000

2. **Calculate the standard divisor.**
   Divide the total population by the number of available seats to determine the standard divisor, which is the average population represented by one seat.

   Standard divisor = Total population / Number of seats
                    = 12,500,000 / 250
                    = 50,000

3. **Calculate the initial quota for each state.**
   Divide the population of each state by the standard divisor to determine how many whole seats each state should receive initially, rounding down to the nearest whole number.

   Initial quotas:
   - A: 1,646,000 / 50,000 = 32.92 -> 32 seats
   - B: 6,936,000 / 50,000 = 138.72 -> 138 seats
   - C: 154,000 / 50,000 = 3.08 -> 3 seats
   - D: 2,091,000 / 50,000 = 41.82 -> 41 seats
   - E: 685,000 / 50,000 = 13.70 -> 13 seats
   - F: 988,000 / 50,000 = 19.76 -> 19 seats

4. **Add up the initial quotas and calculate the surplus seats.**
   After assigning the initial whole number of seats, see how many seats are left over that need to be distributed.

   Total initial seats assigned = 32 + 138 + 3 + 41 + 13 + 19
                               = 246

   Seats left to distribute = 250 - 246
                            = 4

5. **Distribute the surplus seats based on largest remainders.**
   The remainders from the initial quotas will determine who gets the surplus seats. Assign these seats to the states with the largest remainders until all surplus seats are distributed.

   Remainders:
   - A: 0.92
   - B: 0.72
   - C: 0.08
   - D: 0.82
   - E: 0.70
   - F: 0.76

   The four highest remainders are from states A, B, D, and F. Give one extra seat to each.

6. **Final seat distribution.**
   Update the initial quotas with the surplus seats distributed:

   Final distribution:
   - A: 32 + 1 = 33 seats
   - B: 138 + 1 = 139 seats
   - C: 3 + 0 = 3 seats
   - D: 41 + 1 = 42 seats
   - E: 13 + 0 = 13 seats
   - F: 19 + 1 = 20 seats

   Check: 33 + 139 + 3 + 42 + 13 + 20 = 250 seats

Therefore, the final fair representation based on the largest remainder method would assign 33 seats to state A, 139 seats to state B, 3 seats to state C, 42 seats to state D, 13 seats to state E, and 20 seats to state F for a total of 250 seats. This approach ensures that the representation is as proportionally fair as possible according to the populations of the states."""

# "Consistency"
consistency_pb = \
"""The organizers of the Premier League Federation have to decide which one of the three players Mike Arwen, Dave Backhand and Ivan Right - should receive the "The Most Consistent Player for the Past 5 Years" award. Table 1 shows the number of goals that each striker scored between 2019 and 2023.

The organizers agreed to approach this decision mathematically by designing a measure of consistency. They decided to get your help. Here is what you must do:
(1) Design as many different measures of consistency as you can.
(2) Your measure of consistency should make use of all data points in the table.


Table 1. Number of goals scored by the three players in the Premier League between 2007 and 2011.

| Year | Mike Arwen | Dave Backhand | Ivan Right |
| :--- | :--------: | :-----------: | :--------: |
| 2007 |     13     |      12       |     14     |
| 2008 |     12     |      14       |     10     |
| 2009 |     15     |      16       |     18     |
| 2010 |     17     |      15       |     18     |
| 2011 |     13     |      13       |     15     |"""


solution_consistency = \
"""The concept of variance and standard deviation is unknown to students.
Any measure proposed by the student is acceptable as long as it can be justified to measure consistency.
The goal is for them to construct their own measure of consistency and justify it based on the data provided.

Example of canonical solution: computing the variance (or standard deviation) for each player (standard deviation is also valid):
First, compute the mean:
Mean number of goals for Mike: 14
Mean number of goals for Dave: 14
Mean number of goals for Ivan: 15

Then, compute the sum of square deviations from the mean for each player:
Sum squared deviation for Mike: 16
Sum squared deviation for Dave: 10
Sum squared deviation for Ivan: 44

Then devide by the number of data points to get the variance:
Variance for Mike: 12/5 = 3.2
Variance for Dave: 10/5 = 2
Variance for Ivan: 44/5 = 8.8

So according to the variance, Dave is the most consistent player.

"""

def get_pb_sol(topic):
    eq = {"country":(invention_problem,solution_invention),"consistency":(consistency_pb,solution_consistency)}
    pb,sol = eq[topic]
    return pb,sol