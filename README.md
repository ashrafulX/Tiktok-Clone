# TikTok Clone

A full-stack social video platform built with Django, HTMX, and Django Channels. Users can upload videos/images, follow each other, comment, chat in real time, and get live notifications — all server-rendered, no SPA framework.

**Live Demo:** https://tiktok-clone-r9pl.onrender.com

## Features

- Video/image posts with likes, comments, bookmarks, and reposts
- Personalized feed with infinite scroll
- Nested comments with replies and mentions
- Follow system (followers, following, mutual friends)
- Real-time direct messaging via WebSockets
- Live notifications
- User search and hashtag search
- Profile pages with editable info and post tabs
- Email-based authentication (signup, login, password reset)

## Tech Stack

- **Backend:** Django, Django Channels, Daphne (ASGI)
- **Frontend:** HTMX, Tailwind CSS
- **Database:** PostgreSQL
- **Real-time:** Redis (Channels layer)
- **Auth:** django-allauth
- **Media Storage:** Cloudinary
- **Deployment:** Render

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL

### Installation

```bash
git clone https://github.com/ashrafulX/Tiktok-Clone.git
cd Tiktok-Clone

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
npm install
```

### Configuration

Copy the example environment file and fill in your own values:

```bash
cp .env.example .env
```

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000`.

## Author

**Ashraful** — [GitHub](https://github.com/ashrafulX)