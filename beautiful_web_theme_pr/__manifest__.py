# -*- coding: utf-8 -*-
{
    'name': 'Dark Theme Pro — Enterprise Home Menu & Fuzzy Search',
    'version': '19.0.1.0.0',
    'category': 'Themes/Backend',
    'summary': 'Enterprise-style dark theme with fuzzy search, glassmorphism UI & 5 color palettes for Odoo 19 Community',
    'description': """
        Dark Theme for Odoo 19 Community — Enterprise-Style UI
        ========================================================
        Beautiful Web Theme Pro brings Enterprise-quality features to Odoo Community:

        KEY FEATURES
        ------------
        - Enterprise-style fuzzy search: type anywhere on the home screen to instantly search apps
        - Full-screen app grid home menu (like Odoo Enterprise)
        - Glassmorphism navbar with backdrop blur effect
        - 5 dark color themes: Amethyst, Midnight Blue, Emerald Forest, Royal Red, Oceanic Blue
        - Light mode support
        - Accessibility fixes for search panels, company switcher, spreadsheet dashboards

        KEYWORDS
        --------
        dark mode, dark theme, enterprise theme, glassmorphism, fuzzy search, home menu,
        community enterprise features, backend theme, Odoo 19 theme, beautiful theme,
        UI theme, color theme, custom theme, modern theme
    """,
    'author': 'Beautiful Themes PR',
    'support': 'prudhvi.inumarthi99bkp@gmail.com',
    'website': 'https://www.beautiful-odoo-themes.com',
    'license': 'OPL-1',
    'price': 5.00,
    'currency': 'USD',
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
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Midnight Dark Mode
        'web.assets_web_dark_midnight': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.midnight.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Emerald Forest Dark Mode
        'web.assets_web_dark_emerald': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.emerald.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Royal Red Dark Mode
        'web.assets_web_dark_crimson': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.crimson.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
            'beautiful_web_theme_pr/static/src/scss/notebook_overrides.scss',
            'beautiful_web_theme_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Oceanic Blue Dark Mode
        'web.assets_web_dark_oceanic': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'beautiful_web_theme_pr/static/src/scss/primary_variables.oceanic.scss'),
            'beautiful_web_theme_pr/static/src/home_menu/home_menu.dark.scss',
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
