/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { cookie } from "@web/core/browser/cookie";
import { session } from "@web/session";

/**
 * Sync System Color Scheme
 * If the user's preference is 'system' or not set, we listen to the browser's
 * prefers-color-scheme and set the 'color_scheme' cookie accordingly.
 */
function syncSystemColorScheme() {
    const pref = session.color_scheme_pref || 'system';
    
    if (pref === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const currentCookie = cookie.get('color_scheme');
        const expectedCookie = prefersDark ? 'dark' : 'light';
        
        if (currentCookie !== expectedCookie) {
            cookie.set('color_scheme', expectedCookie);
            // Only reload if we are already fully loaded to avoid reload loops,
            // but generally setting the cookie is enough for the next navigation
            // or we can reload immediately if it mismatches on initial load.
            if (document.readyState === 'complete') {
                browser.location.reload();
            }
        }

        // Listen for OS changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            cookie.set('color_scheme', e.matches ? 'dark' : 'light');
            browser.location.reload();
        });
    }
}

// Run the sync on load
syncSystemColorScheme();
