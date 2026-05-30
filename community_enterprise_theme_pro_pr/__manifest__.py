# -*- coding: utf-8 -*-
{
    'name': 'Odoo 19 Community to Enterprise Theme PRO | Dark Mode, Home Menu & Fuzzy Search',
    'version': '19.0.1.0.0',
    'category': 'Themes/Backend',
    'summary': 'Transform Odoo 19 Community UI to Enterprise-style — 5 dark palettes, home menu, fuzzy search. No Enterprise license needed.',
    'description': """
        Odoo 19 Community to Enterprise Theme PRO
        ==========================================
        The most complete Enterprise-style UI transformation for Odoo 19 Community Edition.
        No Enterprise license required. Install and it just works.

        WHY THIS MODULE?
        ----------------
        Odoo Community Edition lacks the polished Enterprise UI that makes daily work
        enjoyable and productive. This module brings the full Enterprise experience to
        Community — without the expensive license cost.

        KEY FEATURES (PRO)
        ------------------
        * Enterprise-Style Home Menu  : Full-screen /odoo app grid — exactly like Odoo Enterprise
        * Fuzzy Search                : Type anywhere on home screen, find any app or menu instantly
        * 5 Dark Color Palettes       : Amethyst, Midnight Blue, Emerald Forest, Royal Red, Oceanic Blue
        * Light Mode                  : Clean Enterprise-style light theme with home menu
        * Glassmorphism Navbar        : Frosted-glass backdrop blur on the navigation bar
        * Per-User Theme Choice       : Each user sets their own color scheme from Preferences
        * System Auto-Theme           : Automatically follows OS dark/light mode preference
        * Accessibility Fixes         : Search panels, company switcher, spreadsheet dashboards
        * Mail Shadow DOM Fix         : Correct text color in email messages in all themes

        COMMUNITY vs ENTERPRISE vs THIS MODULE
        ----------------------------------------
        Feature                         Community   Enterprise   This PRO
        -----------------------------------------------------------------
        /odoo Home Dashboard              No          Yes          Yes
        Full-Screen App Grid Menu         No          Yes          Yes
        Enterprise Fuzzy App Search       No          Yes          Yes
        Dark Mode                         No          Yes          Yes (5 palettes)
        Multiple Color Themes             No          Limited      Yes
        Glassmorphism Navbar              No          Partial      Yes
        Per-User Theme Preferences        No          Limited      Yes
        System Auto Dark/Light            No          Yes          Yes

        FREE LITE VERSION ALSO AVAILABLE
        ---------------------------------
        Want to try before buying? Our FREE Lite version includes the Enterprise
        Home Menu + Light Theme. Search "Community to Enterprise Theme Lite" on App Store.

        KEYWORDS
        --------
        odoo 19 community to enterprise theme, odoo enterprise look community edition,
        odoo dark mode, odoo 19 dark theme pro, enterprise home menu odoo community,
        odoo community enterprise ui, odoo 19 professional theme, odoo color palette,
        fuzzy search odoo, home menu odoo, odoo glassmorphism, dark mode odoo 19,
        odoo night mode, enterprise features community, odoo backend theme pro,
        odoo 19 enterprise style, community enterprise conversion odoo
    """,
    'author': 'Beautiful Themes PR',
    'support': 'prudhvi.inumarthi99bkp@gmail.com',
    'website': 'https://www.beautiful-odoo-themes.com',
    'license': 'OPL-1',
    'price': 19.00,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
        # 'static/description/main_screenshot.png',
        'static/description/screenshot_home.png',
        'static/description/screenshot_search.png',
        'static/description/screenshot_home1.png',
    ],
    'depends': ['web'],
    'data': [
        'views/res_users_views.xml',
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'community_enterprise_theme_pro_pr/static/src/home_menu/home_menu.scss',
            'community_enterprise_theme_pro_pr/static/src/webclient/navbar/navbar.scss',
            'community_enterprise_theme_pro_pr/static/src/**/*.js',
            'community_enterprise_theme_pro_pr/static/src/**/*.xml',
        ],
        # Default Dark — Amethyst
        'web.assets_web_dark': [
            ('include', 'web.assets_web'),
            ('before', 'web/static/src/scss/primary_variables.scss',
             'community_enterprise_theme_pro_pr/static/src/scss/primary_variables.default_dark.scss'),
            'community_enterprise_theme_pro_pr/static/src/home_menu/home_menu.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/webclient/navbar/navbar.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/notebook_overrides.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Midnight Blue
        'web.assets_web_dark_midnight': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss',
             'community_enterprise_theme_pro_pr/static/src/scss/primary_variables.midnight.scss'),
            'community_enterprise_theme_pro_pr/static/src/home_menu/home_menu.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/webclient/navbar/navbar.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/notebook_overrides.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Emerald Forest
        'web.assets_web_dark_emerald': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss',
             'community_enterprise_theme_pro_pr/static/src/scss/primary_variables.emerald.scss'),
            'community_enterprise_theme_pro_pr/static/src/home_menu/home_menu.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/webclient/navbar/navbar.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/notebook_overrides.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Royal Red
        'web.assets_web_dark_crimson': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss',
             'community_enterprise_theme_pro_pr/static/src/scss/primary_variables.crimson.scss'),
            'community_enterprise_theme_pro_pr/static/src/home_menu/home_menu.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/webclient/navbar/navbar.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/notebook_overrides.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/search_panel_dark.scss',
        ],
        # Oceanic Blue
        'web.assets_web_dark_oceanic': [
            ('include', 'web.assets_web_dark'),
            ('before', 'web/static/src/scss/primary_variables.scss',
             'community_enterprise_theme_pro_pr/static/src/scss/primary_variables.oceanic.scss'),
            'community_enterprise_theme_pro_pr/static/src/home_menu/home_menu.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/webclient/navbar/navbar.dark.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/notebook_overrides.scss',
            'community_enterprise_theme_pro_pr/static/src/scss/search_panel_dark.scss',
        ],
        'mail.assets_message_email': [
            'community_enterprise_theme_pro_pr/static/src/scss/mail_message_shadow.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
