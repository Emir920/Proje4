# Message Board - Final Project

A modern, responsive Django-based message board application with user authentication, reactions, search, and pagination.

## Features

### Core Functionality
- **User Authentication**: Sign up, log in, and log out functionality
- **Message Posting**: Users can post messages with rich text support
- **Reactions**: 6 different reaction types (❤️, 😂, 😢, 🔥, 👍, 😠)
- **Message Management**: Users can delete their own messages
- **Real-time Updates**: AJAX-powered reactions without page refresh

### Advanced Features
- **Search**: Search messages by content or author username
- **Pagination**: Efficient handling of large message lists (10 messages per page)
- **User Profiles**: View personal stats and message history
- **Responsive Design**: Mobile-friendly Bootstrap interface
- **Modern UI**: Clean, intuitive design with Font Awesome icons

### Technical Features
- **Form Validation**: Comprehensive client and server-side validation
- **Error Handling**: User-friendly error messages and notifications
- **Security**: CSRF protection, authentication decorators
- **Performance**: Optimized database queries and pagination

## Screenshots

### Landing Page
<img width="1917" height="946" alt="Landing Page" src="https://github.com/user-attachments/assets/3fd4e3ef-d957-4edf-8b87-6d65cdb0c2fb" />

### Sign Up Page
<img width="1918" height="946" alt="Sign Up" src="https://github.com/user-attachments/assets/4bc97ba7-5019-43f6-bffb-29935eafb014" />

### Message Wall
<img width="1914" height="951" alt="Message Wall" src="https://github.com/user-attachments/assets/a4fb248f-0687-470c-896a-24fa3ca33c27" />

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd proje4
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

1. **Sign Up**: Create a new account using the Sign Up link
2. **Log In**: Use your credentials to log in
3. **Post Messages**: Write and post messages on the message wall
4. **React**: Click on reaction icons to react to messages
5. **Search**: Use the search bar to find specific messages
6. **Profile**: View your profile to see your messages and stats
7. **Delete**: Remove your own messages using the delete button

## Project Structure

```
proje4/
├── messageboard/          # Django project settings
├── messaging/            # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Form classes
│   ├── urls.py           # URL patterns
│   ├── templates/        # HTML templates
│   └── migrations/       # Database migrations
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
└── README.md             # This file
```

## Technologies Used

- **Backend**: Django 4.x, Python 3.x
- **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **JavaScript**: Vanilla JS for AJAX functionality

## API Endpoints

- `GET /` - Message list (authenticated users only)
- `POST /add/` - Add new message
- `POST /react/<message_id>/<reaction_type>/` - React to message
- `POST /<message_id>/delete/` - Delete message
- `GET /profile/` - User profile
- `GET /signup/` - Sign up form
- `GET /login/` - Login form
- `POST /logout/` - Logout

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- Real-time notifications with WebSockets
- Message threading and replies
- User avatars and profiles
- Admin panel for moderation
- API for mobile app integration
- Email notifications
