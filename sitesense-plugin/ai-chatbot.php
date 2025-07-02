<?php
/*
Plugin Name: SiteSense AI Agent
Description: Adds AI chatbot functionality to your WordPress site.
Version: 1.6
Author: Alexander Powell
*/

defined('ABSPATH') or die('No script kiddies please!');

// Load plugin components
require_once plugin_dir_path(__FILE__) . 'inc/enqueue.php';
require_once plugin_dir_path(__FILE__) . 'inc/shortcode.php';
// require_once plugin_dir_path(__FILE__) . 'inc/settings-page.php';
// require_once plugin_dir_path(__FILE__) . 'inc/api.php';
