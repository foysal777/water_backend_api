# Flood Mangagement Project

This project is a web-based flood management system designed to assist users in sharing and managing flood-related information, seeking assistance, and collaborating with volunteer teams. The platform offers features such as user authentication, posting and managing flood updates, and communication with volunteer teams to improve disaster response.
There are two types of user 
1) Admin
2) User

## Admin

- Admin can log in and log out.
- Admin can manage the dashboard.
- Admin can manage profile.


## User
- user can register, login and logout.
- User can see post  details.
- User can add post give comment.
- Users can send message for response team.
- User can be add voluntter team request
- user can see her profile , update , change password 
  


## Features

- User Authentication , login ,logout
- User Management
- Volunteer Team Collaboration
- Add Post, Update & Delete
- Communication & Notifications
- Admin Capabilities
- Response team members 
- Funding collection

## Api endpoint
- POST account/register/ - Register a new user.
- POST account/login/ - User login.
- POST account/logout/ - User logout.
- POST team/post/ - Create a new post.
- PUT team/post/{id}/ - Edit a post.
- DELETE team/posts/{id}/ - Delete a post.
- GET team/members/ - List all volunteer teams.
- POST team/join-voluntter/ - Send request to join a team.
- POST team/pending_request - Send a message to a team.



## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Frameworks**: Bootstrap for responsive UI, Font Awesome for icons
- **Backend**: Django for server-side functionality and data handling
- **Database**: SQLite or PostgreSQL
- **APIs**: For potential integration with external services

## Usages
- Navigate to https://water-backend-4x3sz8hnz-foysal-hossain-munnas-projects.vercel.app in your browser.
- Register as a new user or login if you already have an account.
- Browse Post,see blog  add post , send meassage 
- Access your dashboard to manage and accept who were give request to as volunteer 

## Contact
- Email: foysal.cse11@gmail.com
- GitHub: https://github.com/foysal777




