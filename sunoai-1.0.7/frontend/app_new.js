import React, { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

const App = () => {
    const [prompt, setPrompt] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);
    const [tracks, setTracks] = useState([]);
    const [currentlyPlaying, setCurrentlyPlaying] = useState(null);
    const audioRefs = useRef({});

    const handleGenerate = async () => {
        if (!prompt.trim() || isGenerating) return;
        
        setIsGenerating(true);
        try {
            const response = await fetch('/drop_beat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    prompt: prompt,
                    genre: prompt, // Using prompt as genre for simplicity
                    mood: 'energetic', // Default mood
                    duration: 180 // Default 3 minutes
                })
            });
            
            const data = await response.json();
            if (data.success && data.result) {
                const newTrack = {
                    id: Date.now().toString(),
                    title: data.result.title,
                    prompt: prompt,
                    audioUrl: `/static/generated/${data.result.filename}`,
                    filename: data.result.filename
                };
                setTracks(prev => [newTrack, ...prev]);
            }
        } catch (error) {
            console.error('Generation failed:', error);
        } finally {
            setIsGenerating(false);
            setPrompt('');
        }
    };

    const handlePlay = (trackId) => {
        Object.keys(audioRefs.current).forEach(id => {
            if (id !== trackId && audioRefs.current[id]) {
                audioRefs.current[id].pause();
            }
        });
        setCurrentlyPlaying(trackId);
    };

    return (
        <div className="app">
            <header className="header">
                <h1 className="logo">AI Music Studio</h1>
                <nav className="nav">
                    <button className="nav-btn active">Create</button>
                    <button className="nav-btn">Library</button>
                    <button className="nav-btn">Explore</button>
                </nav>
            </header>

            <main className="main">
                <div className="create-section">
                    <h2 className="section-title">Create a song</h2>
                    <div className="input-container">
                        <textarea
                            className="prompt-input"
                            placeholder="Describe the music you want to create..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleGenerate()}
                        />
                        <button 
                            className={`generate-btn ${isGenerating ? 'generating' : ''}`}
                            onClick={handleGenerate}
                            disabled={!prompt.trim() || isGenerating}
                        >
                            {isGenerating ? 'Creating...' : 'Create'}
                        </button>
                    </div>
                </div>

                <div className="tracks-grid">
                    {tracks.map((track) => (
                        <div key={track.id} className="track-card">
                            <div className="track-image">
                                <div className="play-overlay">
                                    <button 
                                        className="play-btn"
                                        onClick={() => {
                                            const audio = audioRefs.current[track.id];
                                            if (audio.paused) {
                                                audio.play();
                                                handlePlay(track.id);
                                            } else {
                                                audio.pause();
                                                setCurrentlyPlaying(null);
                                            }
                                        }}
                                    >
                                        {currentlyPlaying === track.id ? '⏸' : '▶'}
                                    </button>
                                </div>
                            </div>
                            <div className="track-info">
                                <h3 className="track-title">{track.title || 'Untitled'}</h3>
                                <p className="track-prompt">{track.prompt}</p>
                                <div className="track-actions">
                                    <button className="action-btn">♥</button>
                                    <button className="action-btn">⋯</button>
                                </div>
                            </div>
                            <audio
                                ref={el => audioRefs.current[track.id] = el}
                                src={track.audioUrl}
                                onEnded={() => setCurrentlyPlaying(null)}
                            />
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);