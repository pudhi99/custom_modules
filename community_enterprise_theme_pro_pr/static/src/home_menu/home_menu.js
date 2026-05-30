/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { computeAppsAndMenuItems } from "@web/webclient/menus/menu_helpers";
import { hasTouch } from "@web/core/browser/feature_detection";
import { session } from "@web/session";

export class HomeMenu extends Component {
    static template = "community_enterprise_theme_pro_pr.HomeMenu";
    static props = {
        onAppClick: { type: Function, optional: true },
    };

    setup() {
        this.menuService = useService("menu");
        this.command = useService("command");
        this.ui = useService("ui");

        this.searchInputRef = useRef("searchInput");
        this.compositionStart = false;

        onMounted(() => {
            if (!hasTouch()) {
                this._focusInput();
            }
        });
    }

    get appsAndMenuItems() {
        const menuTree = this.menuService.getMenuAsTree("root");
        return computeAppsAndMenuItems(menuTree);
    }

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

    get backgroundImageStyle() {
        const resolvedScheme = session.resolved_color_scheme || "light";

        const darkBackgrounds = {
            'dark':          'default.jpg',
            'dark_default':  'default.jpg',
            'dark_midnight': 'deep-blue.jpg',
            'dark_emerald':  'ocean-blue.jpg',
            'dark_oceanic':  'ocean-blue.jpg',
            'dark_crimson':  'red.jpg',
        };

        let bgFilename = "";
        let themeMode  = "light";

        if (resolvedScheme.startsWith('dark')) {
            themeMode  = "dark";
            bgFilename = darkBackgrounds[resolvedScheme] || 'default.jpg';
        } else {
            bgFilename = 'background-light.jpg';
        }

        const url = `/community_enterprise_theme_pro_pr/static/img/${themeMode}/${bgFilename}`;
        return `background-image: url("${url}") !important; background-size: cover !important; background-position: center !important; background-repeat: no-repeat !important;`;
    }

    _focusInput() {
        if (this.searchInputRef.el) {
            this.searchInputRef.el.focus({ preventScroll: true });
        }
    }

    onSearchInput() {
        const onClose = () => {
            this._focusInput();
            if (this.searchInputRef.el) {
                this.searchInputRef.el.value = "";
            }
        };
        const searchValue = this.compositionStart
            ? "/"
            : `/${this.searchInputRef.el.value.trim()}`;
        this.compositionStart = false;
        this.command.openMainPalette({ searchValue }, onClose);
    }

    onSearchBlur() {
        if (hasTouch()) { return; }
        setTimeout(() => {
            if (document.activeElement === document.body && this.ui.activeElement === document) {
                this._focusInput();
            }
        }, 0);
    }

    onCompositionStart() {
        this.compositionStart = true;
    }

    onAppClicked(app) {
        this.menuService.selectMenu(app);
    }
}
