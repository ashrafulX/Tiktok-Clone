<div align="center">

# 🎬 TikTok Clone

**A full-stack, server-rendered social video platform** — built with Django, HTMX, and Django Channels.

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX](https://img.shields.io/badge/HTMX-1.9-3D72D7?style=flat&logo=htmx&logoColor=white)](https://htmx.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Channels-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Tailwind](https://img.shields.io/badge/TailwindCSS-4-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com/)

**[🔗 Live Demo](https://tiktok-clone-r9pl.onrender.com)**

</div>

---

## ✨ Overview

Users can upload videos and images, follow each other, comment, chat in real time, and get live notifications — all rendered server-side with HTMX, no SPA framework required.

## 🚀 Features

| Category | Highlights |
|---|---|
| 📹 **Posts** | Video/image uploads, likes, bookmarks, reposts |
| 🏠 **Feed** | Personalized feed, infinite scroll |
| 💬 **Comments** | Nested replies, @mentions |
| 👥 **Social** | Follow/unfollow, followers, mutual friends |
| 💌 **Messaging** | Real-time DMs over WebSockets |
| 🔔 **Notifications** | Live activity feed |
| 🔍 **Search** | Users and hashtags |
| 👤 **Profile** | Editable info, post tabs |
| 🔐 **Auth** | Email signup, login, password reset |

## 🛠️ Tech Stack

- **Backend:** Django · Django Channels · Daphne (ASGI)
- **Frontend:** HTMX · Tailwind CSS
- **Database:** PostgreSQL
- **Real-time:** Redis
- **Auth:** django-allauth
- **Media:** Cloudinary
- **Deployment:** Render

## 📦 Getting Started

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

```bash
cp .env.example .env
```

Fill in your own values (database, secret key, etc.) inside `.env`.

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` 🎉

---

<div align="center">

**Author:** [Ashraful](https://github.com/ashrafulX)

</div>