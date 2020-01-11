# [Terming For Learning](deployment link here)

### Welcome to my Terming For Learning website!

Calling everyone who has an unquenchable thirst for learning!
The main aim of this program is to jot down, share, and like terms which you either simply like alone or feel further your understanding of a particular programming language. But it doesn't have to stop there. Use it for any terms for any subject.
This program was put together for The Code Institute as my third milestone project (Data Centric Development Milestone Project), which introduces the Back-End for the first time, focusing on logic, driven by Python and made simple by 
Flask and the Jinja2 templating system.
In this program, I've called on a database structure for the first time, too; MongoDB. The program also calls on old hands for interactivity, such as Javascript and jQuery, as well as the necessary HTML5, CSS, and the Materialize framework. Enjoy!

# UX

## User Stories
- As a user of this website, I would like to be able to do the following: 
- Register an account with my chosen email address, username, profile image, and password.
- Login and retrieve my account.
- Delete my account, should I no longer wish to use this program/website.
- Search for, and read other users' uploaded terms as well as save them.
- Add, edit, save, or delete my own terms.
- Add a new category when adding a new term, should that category not already be saved by that particular user.
- See a separate list of the terms I have save and also a separate list of the categories I have added.
- See a laymen's-type of definition, which may make more sense to beginners.
# TODO
- Vote up/like a laymen's definition to highlight its helpfulness.
- Edit my account infomation - username, password, or profile image - and save it to be retrieved at a later stage. 

## Wireframe
At the suggestion by my wise mentor, Nishant Kumar, I decided to use https://proto.io/ to help me with my wireframe.

### Desktop & ipad Pro
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_dw_1.JPG)
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_dw_2.JPG)
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_dw_3.JPG)
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_dw_4.JPG)

### Mobile
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_mw_1.JPG)
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_mw_2.JPG)
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_mw_3.JPG)
![Desktop & ipad Pro](https://adrianhavengabennett.github.io/terming-for-learning/static/images/wireframe/p_3_mw_4.JPG)


## Features

### - Existing features
User has the ability to do the following:
- Create an account by registering their email, username, and password.
- Sign in an out of their registered accounts.
- Delete their account(s).
- Add a term.
- Edit or delete both terms and categories.
- Search all global terms or search user's saved terms.
- Rate a noob definition (rating is based on definition's Laymen's level - a handy tooltip offers guidance) - The idea is to help new programers.
- Save (shortlist) terms which he/she has determined will require further insights (also removing from shortlist). This will be presented (on desktop - separate screen for mobile) as something similar to Outlook's flagged email system.

# TODO
- Upload a profile image.
- Edit their account(s) information: username, password, profile image


### - Features left to implement

There are currently no pressing features left to implement as the project is completed to the expectation of what it was designed for (student project). 
However, should this program be made available to the public, further client and server-side validation for user's information safety will be necessary. At the moment, it's at an extreme basic level.

## Technologies Used

Technologies used in this project:

## HTML5:
- https://en.wikipedia.org/wiki/HTML

## CSS3:
- https://en.wikipedia.org/wiki/Cascading_Style_Sheets

## Materialize:
- https://materializecss.com/

## Javascript:
- https://en.wikipedia.org/wiki/JavaScript

## jQuery
- https://en.wikipedia.org/wiki/JQuery

## Python
- https://en.wikipedia.org/wiki/Python_(programming_language)

## Flask
- https://en.wikipedia.org/wiki/Flask_(web_framework)

## Jinja2
- https://en.wikipedia.org/wiki/Jinja_(template_engine)

## Testing

### User Testing
The following test cases have been performed to test funtionality:
- Signing in - expected result = Profile page and user welcome loaded | PASS
- Register - expected result = Profile page and user welcome loaded | PASS
- Clicking my terms - expected result = user's terms presented | PASS
- Clicking all terms - expected result = all users' terms presented | PASS
- Create new term - expected result = form loads and upon completion and save, user's terms presented with new term at bottom of list | PASS
- Edit term - expected result = form loads with current category name, and upon completion and save, user's terms presented | PASS
- Save term - expected result = clones the term, changes the id, and populates saved_by to generate saved list / user's saved terms presented to user | PASS

- Edit saved term - expected result = term is updated in saved collection | FAIL

- HTML validated via https://validator.w3.org/ - Pass
- CSS validated via https://jigsaw.w3.org/css-validator/ - Pass

## Deployment TODO
For this project, I have used Heroku to deploy and host the application.

Below are the steps I have taken to achieve this:

1. 
2. 
3. 

![Deployment](deployment image)

### Heroku Link
- 

## Version Control
For this project, I have used Github for version control:
- https://github.com/AdrianHavengaBennett/terming-for-learning

## Credits
Special thanks goes out to Nishant Kumar, my mentor, for his patience and guidance when I've needed it most.

I drew inspiration from my love of learning.

Copyright 2020 - Adrian Havenga-Bennett