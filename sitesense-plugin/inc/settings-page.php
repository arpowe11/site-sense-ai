<?php

// Add the settings menu
add_action('admin_menu', 'sitesense_ai_add_admin_menu');
function sitesense_ai_add_admin_menu() {
    add_menu_page(
        'SiteSense AI Settings',
        'SiteSense AI',
        'manage_options',
        'sitesense-ai-settings',
        'sitesense_ai_settings_page'
    );
}

// Register settings
add_action('admin_init', 'sitesense_ai_register_settings');
function sitesense_ai_register_settings() {
    // Register settings
    register_setting('sitesense_ai_settings_group', 'sitesense_ai_site_name');
    register_setting('sitesense_ai_settings_group', 'sitesense_ai_domain_tool_enabled');

    // Settings section
    add_settings_section('sitesense_ai_main_section', 'AI Configuration', null, 'sitesense-ai-settings');

    // Site name field
    add_settings_field(
        'sitesense_ai_site_name',
        'Site Name',
        'sitesense_ai_site_name_field',
        'sitesense-ai-settings',
        'sitesense_ai_main_section'
    );

    // Domain tool toggle
    add_settings_field(
        'sitesense_ai_domain_tool_enabled',
        'Enable Domain Tool',
        'sitesense_ai_domain_tool_enabled_field',
        'sitesense-ai-settings',
        'sitesense_ai_main_section'
    );
}

// Site name input
function sitesense_ai_site_name_field() {
    $value = esc_attr(get_option('sitesense_ai_site_name', ''));
    echo "<input type='text' name='sitesense_ai_site_name' value='$value' class='regular-text' />";
}

// Domain tool toggle
function sitesense_ai_domain_tool_enabled_field() {
    $enabled = get_option('sitesense_ai_domain_tool_enabled', false);
    $checked = $enabled ? 'checked' : '';
    echo "<label><input type='checkbox' name='sitesense_ai_domain_tool_enabled' value='1' $checked /> Enable</label>";
}

// Page layout
function sitesense_ai_settings_page() {
    ?>
    <div class="wrap">
        <h1>SiteSense AI Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('sitesense_ai_settings_group');
            do_settings_sections('sitesense-ai-settings');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
