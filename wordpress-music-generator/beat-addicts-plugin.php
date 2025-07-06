<?php
/**
 * Plugin Name: Beat Addicts Music Generator
 * Description: AI-powered music generation plugin for WordPress
 * Version: 1.0.0
 * Author: Beat Addicts
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class BeatAddictsPlugin {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('beat_generator', array($this, 'render_generator'));
        add_action('wp_ajax_generate_beat', array($this, 'handle_generate_beat'));
        add_action('wp_ajax_nopriv_generate_beat', array($this, 'handle_generate_beat'));
    }
    
    public function init() {
        // Plugin initialization
    }
    
    public function enqueue_scripts() {
        wp_enqueue_script('beat-addicts-js', plugin_dir_url(__FILE__) . 'assets/beat-addicts.js', array('jquery'), '1.0.0', true);
        wp_enqueue_style('beat-addicts-css', plugin_dir_url(__FILE__) . 'assets/beat-addicts.css', array(), '1.0.0');
        
        wp_localize_script('beat-addicts-js', 'beatAddicts', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('beat_addicts_nonce')
        ));
    }
    
    public function render_generator($atts) {
        $atts = shortcode_atts(array(
            'style' => 'modern'
        ), $atts);
        
        ob_start();
        include plugin_dir_path(__FILE__) . 'templates/generator.php';
        return ob_get_clean();
    }
    
    public function handle_generate_beat() {
        check_ajax_referer('beat_addicts_nonce', 'nonce');
        
        $prompt = sanitize_text_field($_POST['prompt']);
        $genre = sanitize_text_field($_POST['genre']);
        $mood = sanitize_text_field($_POST['mood']);
        $duration = intval($_POST['duration']);
        
        // Simulate music generation (replace with actual API call)
        $result = $this->generate_music($prompt, $genre, $mood, $duration);
        
        wp_send_json_success($result);
    }
    
    private function generate_music($prompt, $genre, $mood, $duration) {
        // This would integrate with your actual music generation API
        // For demo purposes, returning mock data
        return array(
            'id' => uniqid(),
            'title' => 'Generated Beat #' . rand(1000, 9999),
            'filename' => 'beat_' . time() . '.mp3',
            'duration' => $duration,
            'genre' => $genre,
            'mood' => $mood,
            'prompt' => $prompt,
            'audio_url' => plugin_dir_url(__FILE__) . 'generated/demo.mp3',
            'lyrics' => "Generated lyrics based on: " . $prompt,
            'file_size' => '3.2 MB'
        );
    }
}

new BeatAddictsPlugin();
?>