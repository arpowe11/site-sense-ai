<?php
// Exit if accessed directly
defined('ABSPATH') or die('No script kiddies please!');

// Automatically load REST API URL for settings
add_action('rest_api_init', function () {
    register_rest_route('sitesense-ai/v1', '/backend-info', array(
        'methods' => 'GET',
        'callback' => 'sitesense_ai_send_backend_info',
        'permission_callback' => function () { 
            return is_user_logged_in() && current_user_can('manage_options');
        }// change permission to '__return_true' for testing
    ));
});

function sitesense_ai_send_backend_info() {
    return array(
        'settings_url' => rest_url('sitesense-ai/v1/settings'), // WP settings API endpoint
        'site_url'     => get_site_url(),                      // Full domain (e.g., https://example.com)
        'site_name'    => get_bloginfo('name'),                // Optional: site title
    );
}
