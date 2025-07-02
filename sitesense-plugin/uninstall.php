<?php
// If uninstall.php is not called by WordPress, exit to prevent direct access
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit();
}

// Delete plugin options
delete_option( 'sitesense_ai_site_name' );
delete_option( 'sitesense_ai_domain_tool_enabled' );
