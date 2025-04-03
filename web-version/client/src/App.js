import React from 'react';
import { Box, Container, Typography, AppBar, Toolbar, IconButton, Button } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { ThemeProvider, useThemeContext } from './contexts/ThemeContext';
import TextToSpeech from './components/modules/TTS/TextToSpeech';

// Main App component wrapped with ThemeProvider
function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

// App content separated to access theme context
function AppContent() {
  const { mode, toggleTheme } = useThemeContext();
  const [text, setText] = React.useState("Welcome to the AI-Powered Text and Audio Tool. This application is designed to improve text and audio workflows for users who need accessibility features, content creators, and anyone who works extensively with text and audio.");

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI Text & Audio Tool
          </Typography>
          <IconButton onClick={toggleTheme} color="inherit">
            {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container component="main" sx={{ mt: 4, mb: 4, flex: '1 0 auto' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome to AI Text & Audio Tool
        </Typography>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="body1" paragraph>
            {text}
          </Typography>
          <Button variant="contained" sx={{ mr: 1 }}>New Document</Button>
          <Button variant="outlined">Open Document</Button>
        </Box>

        {/* TTS Module */}
        <Box sx={{ my: 4 }}>
          <Typography variant="h5" gutterBottom>Text-to-Speech</Typography>
          <TextToSpeech text={text} />
        </Box>

        {/* Placeholder for other modules */}
        <Box sx={{ my: 4 }}>
          <Typography variant="h5" gutterBottom>Speech-to-Text</Typography>
          <Typography color="text.secondary">Speech-to-Text module will be implemented here</Typography>
        </Box>

        <Box sx={{ my: 4 }}>
          <Typography variant="h5" gutterBottom>Text Transformation</Typography>
          <Typography color="text.secondary">Text Transformation module will be implemented here</Typography>
        </Box>
      </Container>

      <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', backgroundColor: (theme) => theme.palette.mode === 'light' ? theme.palette.grey[200] : theme.palette.grey[800] }}>
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} AI Text & Audio Tool
          </Typography>
        </Container>
      </Box>
    </Box>
  );
}

export default App;