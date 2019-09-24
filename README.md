# Project Mongo

## Problem to be solved

You recently created a new company in the `GAMING industry`, **Nacho's Industries**. The company will have the following scheme:
- 20 Designers
- 5 UI/UX Engineers
- 10 Frontend Developers
- 15 Data Engineers
- 5 Backend Developers
- 20 Account Managers
- 10 Executives
- 1 CEO/President

As a data engineer you have asked all the employees to show their preferences on where to place the new office.
Your goal is to place the **new company offices** in the best place for the company to grow.
You have to found a place that **more or less covers all the following requirements**.

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like **Starbucks** A LOT. Ensure there's a starbucks not to far.
- All people in the company have between 25 and 40 years, give them some place to go to party.
- The CEO is Vegan. Given that he was a pain in the neck the CEO was changed. The new CEO likes to go have lunch with his employees at **burger joints and mexican restaurants**. He is Irish so at least 2 times a week the whole team does **afterwork at an Irish pub**.

## Process

First, we filter the companies database to keep only the companies that have raised more than 1 million dollars or euros and we filtered to get only companies similar to ours, by this I mean the categories are related in some way. This companies are mostly all around Europe and the US.

Second, we use the google places API to enrich our database with some extra requirements such as mexican restaurants, burger joints, pubs, nightclubs and comic shops, why comics? comics inspire our designers to create amazing outfits for the heroes in our games. This extras will make our employees happier and therefore more efficient. 

Finally, using the geonear function from MongoDB we analyse which office has the highest amount of companies and extras around it and there is where we will have our office.

Link tableau: https://public.tableau.com/profile/ignacio5899#!/vizhome/mongo-projectNachoLaiseca/OfficeLocationDetails



