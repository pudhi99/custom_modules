/** @odoo-module **/

/**
 * HomeMenu Component — Full-screen app grid with fuzzy search via Command Palette.
 *
 * This component renders a full-screen overlay showing all installed apps
 * as a grid of icons, similar to Odoo Enterprise's home menu.
 * 
 * Keystrokes are captured by a hidden input and passed to Odoo's built-in
 * Command Palette for a seamless, Enterprise-like fuzzy search experience.
 */

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { computeAppsAndMenuItems } from "@web/webclient/menus/menu_helpers";
import { hasTouch } from "@web/core/browser/feature_detection";

import { session } from "@web/session";

export class HomeMenu extends Component {
    static template = "beautiful_web_theme_pr.HomeMenu";
    static props = {
        onAppClick: { type: Function, optional: true },
    };

    setup() {
        this.menuService = useService("menu");
        this.command = useService("command");
        this.ui = useService("ui");

        // Ref for the hidden search input
        this.searchInputRef = useRef("searchInput");
        this.compositionStart = false;

        onMounted(() => {
            if (!hasTouch()) {
                this._focusInput();
            }
        });
    }

    /**
     * Computes apps and menu items from the menu tree.
     */
    get appsAndMenuItems() {
        const menuTree = this.menuService.getMenuAsTree("root");
        return computeAppsAndMenuItems(menuTree);
    }

    /**
     * Returns the list of apps to display in the grid.
     */
    get displayedApps() {
        const { apps } = this.appsAndMenuItems;
        return apps.map(app => {
            if (app.webIconData && !app.webIconData.startsWith("data:image")) {
                const prefix = app.webIconData.startsWith("P")
                    ? "data:image/svg+xml;base64,"
                    : "data:image/png;base64,";
                app.webIconData = prefix + app.webIconData.replace(/\s/g, "");
            }
            return app;
        });
    }

    /**
     * Computes the dynamic background image style from user preferences.
     */
    get backgroundImageStyle() {
        const resolvedScheme = session.resolved_color_scheme || "light";

        // Define the mapping for dark themes
        const darkBackgrounds = {
            'dark': 'default.jpg',
            'dark_default': 'default.jpg',
            'dark_midnight': 'deep-blue.jpg',
            'dark_emerald': 'ocean-blue.jpg',
            'dark_oceanic': 'ocean-blue.jpg',
            'dark_crimson': 'red.jpg',
        };

        let bgFilename = "";
        let themeMode = "light";

        if (resolvedScheme.startsWith('dark')) {
            themeMode = "dark";
            bgFilename = darkBackgrounds[resolvedScheme] || 'default.jpg';
        } else {
            themeMode = "light";
            bgFilename = 'background-light.jpg';
        }

        if (bgFilename) {
            const url = `/beautiful_web_theme_pr/static/img/${themeMode}/${bgFilename}`;
            return `background-image: url("${url}") !important; background-size: cover !important; background-position: center !important; background-repeat: no-repeat !important;`;
        }
        return "";
    }

    _focusInput() {
        if (this.searchInputRef.el) {
            this.searchInputRef.el.focus({ preventScroll: true });
        }
    }

    /**
     * Handle search input changes.
     * Captures the input value and opens the Command Palette.
     */
    onSearchInput(ev) {
        const onClose = () => {
            this._focusInput();
            if (this.searchInputRef.el) {
                this.searchInputRef.el.value = "";
            }
        };
        const searchValue = this.compositionStart ? "/" : `/${this.searchInputRef.el.value.trim()}`;
        this.compositionStart = false;

        // Open the Command Palette exactly like Enterprise does
        this.command.openMainPalette({ searchValue }, onClose);
    }

    onSearchBlur() {
        if (hasTouch()) {
            return;
        }
        // if we blur search input to focus on body, restore focus
        setTimeout(() => {
            if (document.activeElement === document.body && this.ui.activeElement === document) {
                this._focusInput();
            }
        }, 0);
    }

    onCompositionStart() {
        this.compositionStart = true;
    }

    /**
     * Handle clicking an app icon.
     * Tells the menu service to select this menu item, which naturally triggers ActionManager to load it.
     */
    onAppClicked(app) {
        this.menuService.selectMenu(app);
    }
}
