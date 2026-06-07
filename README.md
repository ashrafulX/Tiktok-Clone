# TikTok Clone

A full-stack social video platform built with **Django**, **HTMX**, **Tailwind CSS**, and **Django Channels**. Personalized feed, video uploads, nested comments, follows, real-time DMs over WebSockets, and live notifications — entirely server-rendered, no SPA framework.

**[Live demo →](https://your-live-demo.example.com)** · Demo login: `demo@tiktok-clone.com` / `demopass123`

![App screenshot](docs/screenshots/feed.png)

---

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | Django 5.2 (Python 3.10), Django Channels 4, Daphne (ASGI) |
| Database | PostgreSQL 14+ |
| Cache / Pub-Sub | Redis (Channels layer in production) |
| Frontend | HTMX, Alpine.js, Tailwind CSS v4, emoji-mart |
| Auth | django-allauth (email verification, password reset) |
| Media | Cloudinary (production), local filesystem (dev) |
| Static | WhiteNoise |
| Deploy | Render (app + Postgres + Redis via `render.yaml` Blueprint), Cloudinary for media |

---

## Features

### Posts
- Image and video uploads with auto-detected type routing
- Likes, bookmarks, reposts (each tracked via through-models)
- Hashtags with click-through search and per-tag post count
- Edit / delete (author-only) and share modal with Facebook and X
- Open Graph + Twitter Card meta tags for rich link previews

### Feed
- Personalized feed of posts from accounts you follow, with an empty-state CTA
- Reposts merged into the feed timeline and attributed to the reposter
- Infinite scroll via HTMX `intersect once`
- Explore page with dynamic tag filter pills

### Comments
- Nested replies with `@mention` profile links
- Per-comment likes
- Author-only delete with a confirmation modal
- Reply form loaded inline via HTMX
- Real-time comment count updates via out-of-band swaps

### Follow System
- Follow / unfollow with HTMX OOB swaps that update every follower/following count on the page
- **Following**, **Friends** (mutual follows), and **Followers** discovery pages
- Suggested accounts ranked by total post likes
- Clickable Following / Followers counts open a list modal on the profile

### Profile
- Tabs (Posts, Reposts, Liked, Bookmarked) lazy-loaded on click
- Sort: newest, oldest, most-liked
- Profile editing, password change, account deletion
- Shareable profile link with copy-to-clipboard

### Search
- Live suggestions for users and tags as you type (300ms debounce)
- Full results page with Posts / Users tabs
- Tag autocomplete inside the post upload form

### Notifications
- Unified activity feed merging follows, post likes, comment likes, comments, replies, and reposts
- Unread indicator dot, polled every 10 seconds via HTMX
- Per-user last-seen tracking — opening the panel clears the dot
- Welcome banner on first visit

### Direct Messages
- **Real-time chat over WebSockets** (Django Channels with Redis in production)
- Image attachments with auto-scroll on load
- Emoji picker (emoji-mart) and large standalone-emoji rendering
- Per-conversation unread badge and a global unread-messages dot
- Live presence tracking — the recipient's unread count doesn't increment while they're viewing the chat
- Self-chat (message yourself)
- Sender-only message delete

---

## Architecture Highlights

**Server-rendered with HTMX.** No SPA framework, no client-side routing. State sync across the page (like counts, follow buttons, unread badges, notification dots) is handled with HTMX out-of-band swaps from the same response that performs the action.

**WebSockets for chat.** Django Channels with an in-memory layer in development and `channels_redis` in production. Each conversation joins a per-chat group; sending a message broadcasts a rendered HTML fragment to every connected client, which HTMX swaps into the message list.

**Modular Django apps.** Each domain lives in its own app — `_users`, `_posts`, `_network`, `_search`, `_notifications`, `_messages`, `_channels` — owning its own models, views, templates, and consumers.

**Performance.**
- `select_related` / `prefetch_related` on hot paths (notifications feed, conversations list, profile tabs)
- Denormalized counters (`Tag.count`, `ConvUser.unread_count`) updated atomically with `F()` expressions
- Lazy tab loading on profile pages and per-route query gating

**Security.**
- Custom middleware sets `Cache-Control: no-store` on authenticated responses so the browser back button can't reveal a logged-out user's pages
- Author-only checks on every mutation (post edit/delete, comment delete, message delete)
- CSRF tokens passed through HTMX headers via the base template

---

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 20+
- PostgreSQL 14+
- (Optional) Redis 7+ if you want to run the production Channels layer locally

### Install

```bash
git clone https://github.com/<your-username>/tiktok-clone.git
cd tiktok-clone
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
pip install -r requirements.txt
npm install
```

### Environment

Copy the template and fill in the values:

```bash
cp .env.example .env
```

```env
ENVIRONMENT=development
SECRET_KEY=<any-long-random-string>
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=tiktok
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```

### Run

Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Start the Tailwind watcher and the dev server in separate terminals:

```bash
# Terminal 1
npm run css

# Terminal 2
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

---

## Project Structure

```
.
├── _core/           Project settings, ASGI/WSGI, URLs, middleware
├── _channels/       WebSocket URL routing
├── _users/          CustomUser, profile, allauth integration
├── _posts/          Post, Tag, Comment, LikedPost, BookmarkedPost, Repost
├── _network/        Follow model, friends and following discovery
├── _search/         User, post, and tag search with live suggestions
├── _notifications/  Aggregated activity feed and unread tracking
├── _messages/       Direct messages, Channels consumer, conversations
├── templates/       Base layout, sidebar, navigation, modals
├── static/css/      Tailwind source and build output
└── manage.py
```

---

## License

MIT