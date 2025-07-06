<?php
/**
 * Plugin Name: BEAT ADDICTS Music Production AI
 * Description: Professional AI-powered music generation system with multiple genres and voice assignment
 * Version: 2.0.0
 * Author: BEAT ADDICTS Team
 * License: GPL v2 or later
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('BEAT_ADDICTS_VERSION', '2.0.0');
define('BEAT_ADDICTS_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('BEAT_ADDICTS_PLUGIN_URL', plugin_dir_url(__FILE__));

class BeatAddictsWordPress {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('wp_ajax_beat_addicts_generate', array($this, 'ajax_generate_music'));
        add_action('wp_ajax_nopriv_beat_addicts_generate', array($this, 'ajax_generate_music'));
        
        // Add admin menu
        add_action('admin_menu', array($this, 'add_admin_menu'));
        
        // Add shortcode
        add_shortcode('beat_addicts', array($this, 'shortcode_handler'));
    }
    
    public function init() {
        // Initialize BEAT ADDICTS system
        $this->start_beat_addicts_services();
    }
    
    public function enqueue_scripts() {
        wp_enqueue_script('beat-addicts-js', BEAT_ADDICTS_PLUGIN_URL . 'assets/beat-addicts.js', array('jquery'), BEAT_ADDICTS_VERSION, true);
        wp_enqueue_style('beat-addicts-css', BEAT_ADDICTS_PLUGIN_URL . 'assets/beat-addicts.css', array(), BEAT_ADDICTS_VERSION);
        
        // Localize script for AJAX
        wp_localize_script('beat-addicts-js', 'beatAddicts', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('beat_addicts_nonce')
        ));
    }
    
    public function add_admin_menu() {
        add_menu_page(
            'BEAT ADDICTS',
            'BEAT ADDICTS',
            'manage_options',
            'beat-addicts',
            array($this, 'admin_page'),
            'dashicons-format-audio',
            30
        );
    }
    
    public function admin_page() {
        include BEAT_ADDICTS_PLUGIN_DIR . 'admin/admin-page.php';
    }
    
    public function shortcode_handler($atts) {
        $atts = shortcode_atts(array(
            'generator' => 'universal',
            'style' => 'modern',
            'width' => '100%',
            'height' => '600px'
        ), $atts);
        
        ob_start();
        include BEAT_ADDICTS_PLUGIN_DIR . 'templates/music-generator.php';
        return ob_get_clean();
    }
    
    public function ajax_generate_music() {
        check_ajax_referer('beat_addicts_nonce', 'nonce');
        
        $generator = sanitize_text_field($_POST['generator']);
        $tempo = intval($_POST['tempo']);
        $duration = intval($_POST['duration']);
        
        // Call Python backend
        $result = $this->call_python_generator($generator, $tempo, $duration);
        
        wp_send_json_success($result);
    }
    
    private function start_beat_addicts_services() {
        // Start Python services if not already running
        $python_path = $this->get_python_path();
        $script_path = BEAT_ADDICTS_PLUGIN_DIR . '../beat-addicts-core/master_launcher.py';
        
        if (file_exists($script_path)) {
            // Check if services are running, start if needed
            $this->ensure_services_running($python_path, $script_path);
        }
    }
    
    private function call_python_generator($generator, $tempo, $duration) {
        $api_url = 'http://localhost:5001/api/generate/' . $generator;
        
        $data = array(
            'tempo' => $tempo,
            'duration' => $duration,
            'complexity' => 'medium'
        );
        
        $response = wp_remote_post($api_url, array(
            'body' => json_encode($data),
            'headers' => array('Content-Type' => 'application/json'),
            'timeout' => 30
        ));
        
        if (is_wp_error($response)) {
            return array('error' => 'Failed to connect to BEAT ADDICTS API');
        }
        
        return json_decode(wp_remote_retrieve_body($response), true);
    }
    
    private function get_python_path() {
        // Try to find Python
        $python_commands = array('python3', 'python', 'py');
        
        foreach ($python_commands as $cmd) {
            $output = shell_exec("which $cmd 2>/dev/null");
            if (!empty($output)) {
                return trim($output);
            }
        }
        
        return 'python'; // Fallback
    }
    
    private function ensure_services_running($python_path, $script_path) {
        // Check if services are running by testing API endpoint
        $response = wp_remote_get('http://localhost:5001/api/master/status', array('timeout' => 5));
        
        if (is_wp_error($response)) {
            // Services not running, start them
            $command = "$python_path $script_path > /dev/null 2>&1 &";
            shell_exec($command);
        }
    }
}

// Initialize the plugin
new BeatAddictsWordPress();

// Activation hook
register_activation_hook(__FILE__, 'beat_addicts_activate');
function beat_addicts_activate() {
    // Create necessary database tables or options
    add_option('beat_addicts_version', BEAT_ADDICTS_VERSION);
}

// Deactivation hook
register_deactivation_hook(__FILE__, 'beat_addicts_deactivate');
function beat_addicts_deactivate() {
    // Stop Python services
    shell_exec('pkill -f "master_launcher.py"');
}
?>