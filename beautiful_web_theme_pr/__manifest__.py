# -*- coding: utf-8 -*-
{
    'name': 'Odoo 19 Enterprise Look — Dark Theme, Home Menu & Fuzzy Search',
    'version': '19.0.1.1.0',
    'category': 'Themes/Backend',
    'summary': 'Get Enterprise home menu, fuzzy search & 5 dark color palettes in Odoo 19 Community — no Enterprise license needed',
    'description': """
        Odoo 19 Enterprise Look for Community Edition
        =============================================
        Transform your Odoo 19 Community into a premium Enterprise-grade experience.
        No Enterprise license required. Install and go.

        KEY FEATURES
        ------------
        * Enterprise-Style Home Menu: Full-screen app grid at /odoo — just like Odoo Enterprise
        * Fuzzy Search: Type anywhere on the home screen to instantly find any app or menu item
        * 5 Dark Color Palettes: Amethyst (default), Midnight Blue, Emerald Forest, Royal Red, Oceanic Blue
        * Glassmorphism Navbar: Frosted-glass backdrop blur effect on the top navigation bar
        * Light Mode Support: Clean, modern light theme with the same Enterprise-style layout
        * Per-User Preferences: Each user picks their own color scheme from Preferences settings
        * Accessibility Fixes: Correct contrast and colors in search panels, company switcher, spreadsheets
        * Zero Performance Cost: Pure CSS animations using GPU-accelerated transform and opacity

        WHAT YOU GET THAT COMMUNITY LACKS
        -----------------------------------
        Community Edition missing feature   →   This module adds it
        -------------------------------------------------------------------
        /odoo home dashboard page           →   Full-screen app icon grid
        Enterprise fuzzy app search         →   Command Palette integration
        Dark mode / color themes            →   5 palettes + light mode
        Modern glassmorphism navbar         →   Backdrop-blur frosted glass

        KEYWORDS
        --------
        odoo 19 dark mode, odoo 19 enterprise look, odoo community enterprise features,
        enterprise home menu odoo, odoo dark theme, odoo 19 theme, beautiful theme odoo,
        odoo ui theme, odoo backend theme, odoo color theme, odoo professional theme,
        fuzzy search odoo, home menu odoo community, glassmorphism odoo,
        dark mode odoo 19, odoo community dark, odoo enterprise style community,
        odoo 19 color palette, modern odoo theme, odoo night mode
    """,
    'author': 'Beautiful Themes PR',
    'support': 'prudhvi.inumarthi99bkp@gmail.com',
    'website': 'https://www.beautiful-odoo-themes.com',
    'license': 'OPL-1',
    'price': 5.00,
    'currency': 'USD',
    'video': 'https://www.youtube.com/watch?v=J4tltGK5RaI',
    'images': [
        'static/description/banner.gif',
        'static/description/feature_overview.png',
        'static/description/screenshot_home.png',
        'static/description/feature_search.png',
        'static/description/screenshot_search.png',
        'static/description/feature_palettes.png',
        'static/description/screenshot_home1.png',
    ],
    'depends': ['web'],
    'data': [
        'views/res_users_views.xml',
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.scss',
            'beautiful_web_theme_pr/static/src/webclient/navbar/navbar.scss',
            'beautiful_web_theme_pr/static/src/**/*.js',
            'beautiful_web_theme_pr/static/src/**/*.xml',
        ],
        # Default Dark Mode
        'web.assets_web_dark': [
            ('include', 'web.assets_web'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.default_dark.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/webclient/navbar/navbar.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Midnight Dark Mode
        'web.assets_web_dark_midnight': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.midnight.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/webclient/navbar/navbar.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Emerald Forest Dark Mode
        'web.assets_web_dark_emerald': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.emerald.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/webclient/navbar/navbar.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Royal Red Dark Mode
        'web.assets_web_dark_crimson': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.crimson.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/webclient/navbar/navbar.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Oceanic Blue Dark Mode
        'web.assets_web_dark_oceanic': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.oceanic.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/webclient/navbar/navbar.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        'mail.assets_message_email': [
            'beautiful_web_theme_pr/static/src/scss/mail_message_shadow.scss',
        ],
    },
    'installable': True,
    'application': False,  # This is a theme, not a standalone app
    'auto_install': False,

}
