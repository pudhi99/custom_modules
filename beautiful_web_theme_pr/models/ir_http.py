from odoo import models
from odoo.http import request

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def color_scheme(self):
        try:
            if request and request.httprequest:
                user = request.env.user
                is_logged_in = user and hasattr(user, 'color_scheme')

                # Determine base scheme (light/dark)
                base_scheme = 'light'
                if is_logged_in and user.color_scheme != 'system':
                    base_scheme = user.color_scheme
                else:
                    # Fallback to cookie for system or public user
                    cookie_val = request.httprequest.cookies.get('color_scheme')
                    if cookie_val == 'dark':
                        base_scheme = 'dark'

                if base_scheme == 'dark':
                    # If dark mode is active, check the theme
                    if is_logged_in and user.dark_mode_theme and user.dark_mode_theme != 'dark_default':
                        return user.dark_mode_theme
                    return 'dark'
                return 'light'
        except RuntimeError:
            pass
        return super().color_scheme()

    def session_info(self):
        session_info = super().session_info()
        user = request.env.user
        if user and hasattr(user, 'color_scheme'):
            session_info['color_scheme_pref'] = user.color_scheme
            session_info['dark_mode_theme_pref'] = user.dark_mode_theme
            # Add the resolved scheme (e.g. 'dark_midnight') so JS knows exactly what's active
            session_info['resolved_color_scheme'] = self.color_scheme()
        return session_info

    def get_frontend_session_info(self):
        session_info = super().get_frontend_session_info()
        user = request.env.user
        if user and hasattr(user, 'color_scheme'):
            session_info['color_scheme_pref'] = user.color_scheme
            session_info['dark_mode_theme_pref'] = user.dark_mode_theme
            session_info['resolved_color_scheme'] = self.color_scheme()
        return session_info
