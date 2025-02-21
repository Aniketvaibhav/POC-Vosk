const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;

// Basic test endpoint to verify server is running
app.get('/', (req, res) => {
  res.send('Server is running!');
});

// Endpoint to handle audio transcription
app.post('/transcribe', (req, res) => {
    try {
        // Use the test_audio.wav directly from project directory
        const audioFilePath = path.join(__dirname, 'test_audio.wav');
        console.log('Using audio file:', audioFilePath);

        const pythonProcess = spawn('python', [
            path.join(__dirname, 'transcribe.py'),
            audioFilePath
        ]);

        let transcription = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
            transcription += data.toString();
            console.log('Transcription progress:', data.toString());
        });

        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
            console.error('Python error:', data.toString());
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                res.json({
                    success: true,
                    transcription: transcription.trim()
                });
            } else {
                res.status(500).json({
                    success: false,
                    message: 'Transcription failed',
                    error: errorOutput
                });
            }
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({
            success: false,
            message: 'Server error during transcription',
            error: error.message
        });
    }
});

// Start Express Server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
}).on('error', (err) => {
  console.error('Failed to start server:', err);
});
