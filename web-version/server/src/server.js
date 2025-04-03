// server/src/server.js
const express = require('express');
const path = require('path');
const cors = require('cors');
const ttsRoutes = require('./api/routes/tts');

// Initialize express app
const app = express();
const PORT = process.env.PORT || 5000;

// Enable JSON parsing for request bodies
app.use(express.json());

// Enable CORS to allow frontend to communicate with backend
app.use(cors());

// Serve static files (like generated audio)
app.use('/audio', express.static(path.join(__dirname, '../temp')));

// API routes
app.use('/api/v1/tts', ttsRoutes);

// Health check route
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date() });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});