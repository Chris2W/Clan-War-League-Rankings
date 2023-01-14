# Clan-War-League-Rankings
A python script used to identify top fair players in the game Clash of Clans on the basis of average stars won, participation ratio, and the difference between a member's map position and their opponent's map position.

## Situation
1. In Clan War Leagues (CWL), 7 clans war against each other in a period of a week, and at the end, displays the rankings of all clans and total stars gained in each war.
2. Stars are achieved by members attacking bases, with maximum 3 stars per base.
3. 6-8 members in each clan gets rewarded extra medals upon who gets the most stars by the clan leader.

## Problem
1. Our clan noticed a pattern where the same top members get the extra medals, as they frequently attain most if not all stars attainable. 
2. This can be done unfairly by members attacking far weaker bases, or positions lower than them on the map. This prevents other members who do attack their equal counterpart or higher from getting rewarded extra medals for effort.
3. It also prevents anyone else from having the chance to get extra medals.
4. Currently, it is tedious to track every member of every war and see who is attacking fairly and who isn't, as well as how well they perform on each attack

## Task
1. To automate the process of tracking every members' performance and fairness, then creating a ranking system to dictate which 6-8 members deserve extra medals the most on the basis of average stars won, participation ratio, and the difference between a member's map position and their opponent's map position.

## Action
1. Clash of Clans API (https://developer.clashofclans.com/#/getting-started) provides a multitude of information regarding an individual clan's status in war, capital leagues, clan war leagues, etc.

## Blockers and how I resolved them
1. Because of how the JSON data is formatted from the API, and which information I wanted to pull, I had to loop through 28 war_tags (each war_tag is one request) 3 different times, then joining them to a list
2. Implemented multithreading processes to reduce reponse time from an average of 45 seconds down to 15 seconds, using 3 threads in total. 
