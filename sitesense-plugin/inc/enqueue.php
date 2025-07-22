<?php
defined('ABSPATH') or die('No script kiddies please!');

function sitesense_ai_enqueue_scripts() {
    wp_enqueue_style(
        'sitesense-ai-style',
        plugin_dir_url(__FILE__) . '../assets/css/sitesense-styles.css',
        array(),
        '1.0'
    );

    wp_enqueue_script(
        'sitesense-ai-js',
        plugin_dir_url(__FILE__) . '../assets/js/sitesense-script.js',
        array('jquery'),
        '1.0',
        true
    );

        // Load external libraries
    wp_enqueue_script(
        'marked-js',
        'https://cdnjs.cloudflare.com/ajax/libs/marked/10.0.0/marked.min.js',
        array(),
        '10.0.0',
        true
    );

    wp_enqueue_script(
        'dompurify-js',
        'https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.5/purify.min.js',
        array(),
        '3.0.5',
        true
    );


    // Pass the REST API endpoint URL or to JS
    wp_localize_script('sitesense-ai-js', 'sitesenseAI', array(
        'apiUrl' => ''
    ));
}

add_action('wp_enqueue_scripts', 'sitesense_ai_enqueue_scripts');
