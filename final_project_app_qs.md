# SI 364 - Final Project questions

## Overall

* **What's a one-two sentence description of what your app will do?**
User enters a Twitter handle and then they see that handle's most recent most recent follow and most recent tweet


## The Data

* **What data will your app use? From where will you get it? (e.g. scraping a site? what site? -- careful not to run it too much. An API? Which API?)**
Twitter API

* **What data will a user need to enter into a form?**
Their own name (Allison Wanderer)
Their Twitter handle or any Twitter handle (@beyonce?)

* **How many fields will your form have? What's an example of some data user might enter into it?**
Two fields at a minimum. First one to enter their own name then another one to enter the Twitter handle they're interested in ["Enter username here to see most recent follow and most recent tweet"]. 
Perhaps there will be a field where the user can enter many Twitter handles to compare the answers between 2 Twitter handles

* **After a user enters data into the form, what happens? Does that data help a user search for more data? Does that data get saved in a database? Does that determine what already-saved data the user should see?**
After the user enters the data, it leads them to the next page where the most recent tweet and most recent follow is displayed. this is the end of the journey. they will have an option to return back to the form and do another search. 
the data does get saved in a database. it does not determine what already-saved data the user should see as the information displayed (most recent follow and tweet) is subject to change


* **What models will you have in your application?**
User model, recent follow model, recent tweet model 

* **What fields will each model have?**
user model = email, id, text name
recent follow model = id, twitter_username
recent tweet model = id, twitter_username


* **What uniqueness constraints will there be on each table? (e.g. can't add a song with the same title as an existing song)**
if in the search session, there is no change in information (Donald Trump has not tweeted anything or followed anyone in the past 5 minutes) then the same recent tweet and recent follow will not be saved in the database twice. this information will display on the web page as well. 

* **What relationships will exist between the tables? What's a 1:many relationship between? What about a many:many relationship?**
1: many = user (Allison Wanderer) searching for many users (beyonce, donald trump, mindy kaling)
many:many = each twitter user (beyonce, donald trump, mindy kaling) can have many "most recent follow" and "most recent tweet" updates 

* **How many get_or_create functions will you need? In what order will you invoke them? Which one will need to invoke at least one of the others?**
Four, in this order: 
get or create user(Allison Wanderer) - logical to enter your info first
get or create twitter handle (Beyonce) - the following two functions are dependent on this function
get or create follow (most recent follow)
get or create tweet (most recent tweet)


## The Pages

* **How many pages (routes) will your application have?**
Two

* **How many different views will a user be able to see, NOT counting errors?**
Two - each page 

* **Basically, what will a user see on each page / at each route? Will it change depending on something else -- e.g. they see a form if they haven't submitted anything, but they see a list of things if they have?**
First page - form, with min 3 fields (their name, their email addrress, twitter handle they want to look up). there could maybe be a third form field where they enter a second twitter handle to compare. this is constant
Second page - the twitter handle they entered most recent follow and most recent tweet. this changes depending on what twitter user they put into the form

## Extras

* **Why might your application send email?**
to the user to tell them what user they have looked up

* **If you plan to have user accounts, what information will be specific to a user account? What can you only see if you're logged in? What will you see if you're not logged in -- anything?**
specific to a user account when they're logged in: what twitter handles they have looked up
not logged in: form 

* **What are your biggest concerns about the process of building this application?**
user account as mentioned in the question above. not sure exactly how to go about this...
