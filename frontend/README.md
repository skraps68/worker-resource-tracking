# Worker Resource Tracking - Frontend

React-based frontend for the Worker Resource Tracking System.

## Setup

### Prerequisites

- Node.js 18+ with npm

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:3000

The development server is configured to proxy API requests to the backend at http://localhost:5000

### Build

Build for production:

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.js          # API client for backend communication
│   ├── components/
│   │   ├── CreationPanel.jsx  # Worker/resource creation and update
│   │   ├── ViewingPanel.jsx   # Active resources display
│   │   └── QueryPanel.jsx     # Bi-temporal query interface
│   ├── App.jsx                # Main application component
│   ├── App.css                # Application styles
│   ├── main.jsx               # Application entry point
│   └── index.css              # Global styles
├── index.html                 # HTML template
├── vite.config.js             # Vite configuration
└── package.json               # Dependencies and scripts
```

## Components

### CreationPanel
- Create new workers with associated resources
- Update existing resources with new business time ranges

### ViewingPanel
- Display all currently active resources
- Show worker information alongside resource data

### QueryPanel
- Execute bi-temporal as-of queries
- View historical state of resources at specific points in time

## API Integration

The frontend communicates with the Flask backend through the following endpoints:

- `POST /api/workers` - Create worker and resource
- `PUT /api/resources/:rid` - Update resource
- `GET /api/resources/active` - Get active resources
- `GET /api/resources/as-of` - Execute as-of query
