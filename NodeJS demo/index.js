const express = require('express');             // Import Express module
const app = express();                          // Create an Express app instance
const port = 3000;                              // Define the port to listen on

// Middleware to log request details
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next(); // Call next middleware or route handler
});

app.use(express.json()); // Parse JSON bodies of incoming requests

// Define different routes
app.get('/', (req, res) => res.send('Welcome to the CI/CD Node.js App!'));

app.get('/about', (req, res) =>
    res.send('This is a sample Node.js app to demonstrate GitHub Actions CI/CD.'));

app.get('/status', (req, res) =>
    res.json({ status: 'OK', timestamp: new Date().toISOString() }));

app.get('/user/:username', (req, res) =>
    res.send(`Hello, ${req.params.username}!`));

app.post('/api/data', (req, res) => {
    const data = req.body;
    if (!data.name || !data.value) {
        return res.status(400).json({ error: 'Invalid data format' });
    }
    res.status(201).json({ message: 'Data received successfully', received: data });
});

app.get('/health', (req, res) => res.send('App is healthy and running!'));

// Start the server
app.listen(port, () => console.log(`Server running at http://localhost:${port}`));