<?php
defined('ABSPATH') or die('No script kiddies please!');

function sitesense_ai_chatbot_shortcode() {
    ob_start();
    include plugin_dir_path(__FILE__) . '../templates/chatbot-widget.php';
    return ob_get_clean();
}

add_shortcode('sitesense_ai_agent', 'sitesense_ai_chatbot_shortcode');
