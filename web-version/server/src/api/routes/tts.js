// server/src/api/routes/tts.js
const express = require('express');
const { synthesizeSpeech, estimateTtsTokens } = require('../../services/ai/aiTtsService'); 

const router = express.Router();

// POST /api/v1/tts/synthesize
router.post('/synthesize', async (req, res) => {
    const { text, voice, speed } = req.body;

    if (!text) {
        return res.status(400).json({ error: 'Text is required.' });
    }

    try {
        // 1. Estimate cost before making the expensive call
        const estimatedTokens = estimateTtsTokens(text, voice);

        // Optional: Check user token balance or implement confirmation logic here if needed

        // 2. Perform the synthesis
        const synthesisResult = await synthesizeSpeech(text, voice, speed);

        if (synthesisResult.success && synthesisResult.audioFilePath) {
             // For a local development setup, assuming we're serving static files
             // In production, you'd use cloud storage and proper URL generation
             console.log(`Generated TTS, estimated tokens: ${estimatedTokens}`);
             
             // Extract the filename for a simple demo response
             const fileName = synthesisResult.audioFilePath.split('/').pop();
             res.json({
                 audioUrl: `/audio/${fileName}`, // URL that your frontend can access
                 estimatedTokens: estimatedTokens
             });
        } else {
            res.status(500).json({ error: synthesisResult.error || 'Failed to synthesize speech.' });
        }
    } catch (error) {
        console.error('TTS Synthesis Endpoint Error:', error);
        res.status(500).json({ error: error.message || 'Internal server error during speech synthesis.' });
    }
});

module.exports = router;