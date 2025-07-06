-- Database backup for SunoAI application
-- Generated on: 2024-01-01

-- Create database schema
CREATE DATABASE IF NOT EXISTS sunoai_db;
USE sunoai_db;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Audio tracks table
CREATE TABLE audio_tracks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    duration INT NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Sample data
INSERT INTO users (username, email, password_hash) VALUES
('john_doe', 'john@example.com', '$2b$12$hash1'),
('jane_smith', 'jane@example.com', '$2b$12$hash2'),
('music_lover', 'lover@example.com', '$2b$12$hash3');

INSERT INTO audio_tracks (user_id, title, duration, file_path) VALUES
(1, 'My First Song', 180, '/uploads/song1.mp3'),
(1, 'Ambient Dreams', 240, '/uploads/song2.mp3'),
(2, 'Rock Anthem', 200, '/uploads/song3.mp3');

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tracks_user ON audio_tracks(user_id);
CREATE INDEX idx_tracks_created ON audio_tracks(created_at);
