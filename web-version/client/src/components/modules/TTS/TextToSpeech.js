import React, { useState, useCallback } from 'react';
import { Box, Button, Slider, Select, MenuItem, FormControl, InputLabel, Typography, CircularProgress, Alert } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import StopIcon from '@mui/icons-material/Stop';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';

// Placeholder for API client - will be replaced with actual implementation
const apiClient = {
  post: async (url, data) => {
    console.log(`API request to ${url} with data:`, data);
    // Mock successful response with a delay
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            audioUrl: 'https://example.com/audio/placeholder.mp3',
            estimatedTokens: Math.ceil(data.text.length / 10)
          }
        });
      }, 1500);
    });
  }
};

// Text-to-Speech Component
function TextToSpeech({ text }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioSource, setAudioSource] = useState(null);
  const [audioElement, setAudioElement] = useState(null);
  const [speed, setSpeed] = useState(1.0);
  const [volume, setVolume] = useState(1.0);
  const [voice, setVoice] = useState('default-male');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tokenEstimate, setTokenEstimate] = useState(0);

  // Play/Pause handler
  const handlePlayPause = useCallback(async () => {
    setError(null); // Clear previous errors

    if (isPlaying && audioElement) {
      audioElement.pause();
      setIsPlaying(false);
    } else if (audioSource && audioElement) {
      audioElement.play().catch(err => setError(`Playback error: ${err.message}`));
      setIsPlaying(true);
    } else if (text) {
      setIsLoading(true);
      try {
        // Basic estimation (rough) - backend should do the real one
        const roughEstimate = Math.ceil(text.length / 10);
        setTokenEstimate(roughEstimate);

        const response = await apiClient.post('/api/v1/tts/synthesize', {
          text: text,
          voice: voice,
          speed: speed
        });

        if (response.data.audioUrl) {
          const audio = new Audio(response.data.audioUrl);
          audio.volume = volume;

          setAudioElement(audio);
          setAudioSource(response.data.audioUrl);
          setTokenEstimate(response.data.estimatedTokens || 0);

          audio.play().catch(err => setError(`Playback error: ${err.message}`));
          setIsPlaying(true);

          audio.onended = () => {
            setIsPlaying(false);
            setAudioElement(null);
            setAudioSource(null);
          };
          audio.onerror = (e) => {
            setError(`Audio playback error: ${e.target.error?.message || 'Unknown error'}`);
            setIsLoading(false);
            setIsPlaying(false);
          };
        } else {
          setError(response.data.error || "Failed to synthesize audio.");
        }
      } catch (err) {
        console.error("TTS Synthesis Error:", err);
        setError(err.response?.data?.error || err.message || "An unknown error occurred.");
      } finally {
        setIsLoading(false);
      }
    }
  }, [text, voice, speed, volume, isPlaying, audioElement, audioSource]);

  // Stop playback handler
  const handleStop = useCallback(() => {
    if (audioElement) {
      audioElement.pause();
      audioElement.currentTime = 0; // Reset position
      setIsPlaying(false);
      setAudioElement(null);
      setAudioSource(null);
    }
  }, [audioElement]);

  // Skip forward/backward handler
  const handleSkip = useCallback((seconds) => {
    if (audioElement) {
      audioElement.currentTime = Math.max(0, audioElement.currentTime + seconds);
    }
  }, [audioElement]);

  // Speed change handler
  const handleSpeedChange = (event, newValue) => {
    setSpeed(newValue);
  };

  // Volume change handler
  const handleVolumeChange = (event, newValue) => {
    setVolume(newValue);
    if (audioElement) {
      audioElement.volume = newValue;
    }
  };

  // Voice change handler
  const handleVoiceChange = (event) => {
    setVoice(event.target.value);
    handleStop(); // Changing voice requires re-synthesis
  };

  return (
    <Box sx={{ padding: 2, border: '1px solid grey', borderRadius: 1 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {tokenEstimate > 0 && <Typography variant="caption" display="block" sx={{ mb: 1 }}>Estimated Tokens: {tokenEstimate}</Typography>}

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
        <Button variant="contained" onClick={handlePlayPause} disabled={!text || isLoading}>
          {isLoading ? <CircularProgress size={24} /> : (isPlaying ? <PauseIcon /> : <PlayArrowIcon />)}
        </Button>
        <Button variant="outlined" onClick={handleStop} disabled={!isPlaying && !audioElement}>
          <StopIcon />
        </Button>
        <Button variant="outlined" onClick={() => handleSkip(-10)} disabled={!isPlaying && !audioElement}>
          <SkipPreviousIcon />
        </Button>
        <Button variant="outlined" onClick={() => handleSkip(10)} disabled={!isPlaying && !audioElement}>
          <SkipNextIcon />
        </Button>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography gutterBottom>Speed: {speed.toFixed(1)}x</Typography>
        <Slider
          value={speed}
          onChange={handleSpeedChange}
          aria-labelledby="speed-slider"
          valueLabelDisplay="auto"
          step={0.1}
          marks
          min={0.5}
          max={2.0}
          disabled={isLoading}
        />
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography gutterBottom>Volume</Typography>
        <Slider
          value={volume}
          onChange={handleVolumeChange}
          aria-labelledby="volume-slider"
          valueLabelDisplay="auto"
          step={0.1}
          marks
          min={0}
          max={1}
          disabled={isLoading}
        />
      </Box>

      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="voice-select-label">Voice</InputLabel>
        <Select
          labelId="voice-select-label"
          id="voice-select"
          value={voice}
          label="Voice"
          onChange={handleVoiceChange}
          disabled={isLoading}
        >
          <MenuItem value={'default-male'}>Default Male</MenuItem>
          <MenuItem value={'default-female'}>Default Female</MenuItem>
          <MenuItem value={'accent-uk-male'}>UK Male</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}

export default TextToSpeech;