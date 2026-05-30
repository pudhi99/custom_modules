/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { cookie } from "@web/core/browser/cookie";

/**
 * Theme Attribute Handler
 * This script ensures that the 'data-bs-theme' attribute is correctly set on the
 * document root (<html>) based on the active Odoo color scheme.
 * This is required for Bootstrap 5.3+ components and our custom CSS overrides.
 */
function syncThemeAttribute() {
    const colorScheme = cookie.get("color_scheme") || "light";
    const isDark = colorScheme === "dark" || colorScheme.startsWith("dark_");
    
    if (isDark) {
        document.documentElement.setAttribute("data-bs-theme", "dark");
    } else {
        document.documentElement.setAttribute("data-bs-theme", "light");
    }
}

// Initial sync
syncThemeAttribute();

// Listen for theme changes (reloads usually handle this, but we can be proactive)
browser.addEventListener("load", syncThemeAttribute);
