# Spotify Toolkit

Spotify Toolkit is a full-featured desktop application built with PyQt5 that empowers you to manage your Spotify account and playlists with a beautiful, modern interface. Designed for music enthusiasts and power users, it provides advanced playlist management, interactive track deletion, drag-and-drop sorting, and profile viewing—all from your desktop, without needing to use the Spotify web or mobile apps.

The app uses the official Spotify Web API via Spotipy, and securely authenticates you using OAuth. All playlist operations (deleting tracks, sorting, viewing, etc.) are performed directly on your Spotify account, so changes are instantly reflected in your Spotify app.

Key technologies:
- **PyQt5** for a responsive, modern GUI
- **Spotipy** for Spotify API integration
- **python-dotenv** for secure credential management

User experience highlights:
- Playlists are displayed as visually appealing cards with cover images and names, making navigation intuitive and fun.
- Only playlists you own (created by you) are shown for editing, so you never get permission errors.
- Interactive deletion: select a playlist, then confirm each track you want to remove, with instant feedback.
- Powerful sorting: reorder tracks by drag-and-drop or use smart sort options (alphabetic, date added, release date), then save the new order to Spotify.
- Profile page: view your Spotify account details and avatar in-app.
- Secure logout: tokens are cleared and you can re-authenticate at any time.
- Consistent Spotify color palette and modern design for a professional look.

Whether you want to clean up old playlists, organize your music, or just explore your Spotify data, Spotify Toolkit makes it easy and enjoyable.

## Features
- **Login with Spotify** (OAuth)
- **View and manage your playlists**
  - Display playlists as cards with images
  - Only shows playlists you own (modifiable)
- **Delete tracks interactively**
- **Sort playlist tracks**
  - Drag-and-drop or use sort options (A-Z, date added, release date)
  - Save new order to Spotify
- **View your Spotify profile**
- **Logout securely**
- **Modern UI** with Spotify color palette and responsive layouts

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```
2. **Create and activate a Python virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure your Spotify API credentials:**
   - Create a `.env` file in the project root:
     ```
     SPOTIPY_CLIENT_ID='your-client-id'
     SPOTIPY_CLIENT_SECRET='your-client-secret'
     SPOTIPY_REDIRECT_URI='http://127.0.0.1:8888/callback'
     ```
   - Register your app at https://developer.spotify.com/dashboard/

## Usage
Run the app:
```sh
python main.py
```

## File Structure
- `main.py` — App entry point
- `gui/` — All PyQt5 GUI pages
- `services/` — Spotify API logic and authentication
- `.env` — Your Spotify credentials (not committed)
- `requirements.txt` — Python dependencies

## Contributing
Pull requests are welcome! For major changes, please open an issue first.

## License
MIT

---
Made by SalahKhadir
