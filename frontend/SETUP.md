# Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

If npm is not available on your system, you'll need to install it first:

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install npm
```

**On macOS:**
```bash
brew install node
```

**On other systems:**
Visit https://nodejs.org/ to download and install Node.js (which includes npm)

### 2. Install Project Dependencies

Once npm is available:

```bash
cd frontend
npm install
```

This will install all required dependencies:
- React 18.2.0
- React DOM 18.2.0
- Vite 5.0.0
- @vitejs/plugin-react 4.2.0

### 3. Start Development Server

```bash
npm run dev
```

The application will start at http://localhost:3000

### 4. Start Backend Server

In a separate terminal, make sure the Flask backend is running:

```bash
cd ..
python run.py
```

The backend should be running at http://localhost:5000

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, Vite will automatically try the next available port (3001, 3002, etc.)

### API Connection Issues

Make sure:
1. The Flask backend is running on port 5000
2. The proxy configuration in `vite.config.js` is correct
3. CORS is properly configured in the Flask app

### Build Issues

If you encounter build issues:

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Production Build

To create a production build:

```bash
npm run build
```

The built files will be in the `dist/` directory.

To preview the production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.js          # API client functions
│   ├── components/
│   │   ├── CreationPanel.jsx  # Worker/resource creation
│   │   ├── CreationPanel.css
│   │   ├── ViewingPanel.jsx   # Active resources display
│   │   ├── ViewingPanel.css
│   │   ├── QueryPanel.jsx     # Bi-temporal queries
│   │   └── QueryPanel.css
│   ├── App.jsx                # Main app with tabs
│   ├── App.css
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html                 # HTML template
├── vite.config.js             # Vite configuration
└── package.json               # Dependencies
```

## Features

### Creation Panel
- Create new workers with initial resource records
- Update existing resources with new business time ranges
- Real-time validation and error feedback

### Active Resources Panel
- View all currently active resources (proc_end = infinity)
- Refresh data on demand
- Display all worker and resource information

### Query Panel
- Execute bi-temporal as-of queries
- Specify business date (required)
- Optionally specify processing datetime (defaults to now)
- View historical state of resources

## API Endpoints Used

- `POST /api/workers` - Create worker and resource
- `PUT /api/resources/:rid` - Update resource
- `GET /api/resources/active` - Get active resources
- `GET /api/resources/as-of` - Execute as-of query
