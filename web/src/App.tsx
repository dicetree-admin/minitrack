import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SplashScreen from './screens/SplashScreen';
import MainScreen from './screens/MainScreen';
import BallTrackingScreen from './screens/BallTrackingScreen';
import ResultScreen from './screens/ResultScreen';
import VideoGalleryScreen from './screens/VideoGalleryScreen';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/splash" replace />} />
          <Route path="/splash" element={<SplashScreen />} />
          <Route path="/main" element={<MainScreen />} />
          <Route path="/ball-tracking" element={<BallTrackingScreen />} />
          <Route path="/result" element={<ResultScreen />} />
          <Route path="/gallery" element={<VideoGalleryScreen />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
