from htmlcss import reserved

regular_tokens = [
    'css_comment', 'css_string', 'css_important','css_vendor_hack',
    'css_uri', 'css_ms_filter', 'css_keyframe_selector', 'css_media_feature',
    'less_comment', 'less_open_format', 'less_when', 'less_and', 'less_not',
    't_ws', 't_popen', 't_pclose', 't_semicolon', 't_tilde', 't_colon',
    't_comma', 't_eopen', 't_eclose', 't_isopen', 't_isclose', 't_bopen', 't_bclose'
]

significant_ws_literals = ['&']

significant_ws_tokens = [
    'css_class', 'css_id', 'css_dom', 'css_property', 'css_vendor_property',
    'css_user_property', 'css_ident', 'css_number', 'css_color', 'css_media_type',
    'css_filter', 'less_variable', 't_and', 't_not', 't_only'
]

literals = '<>=%!/*-+'.join(significant_ws_literals)

tokens = regular_tokens + significant_ws_tokens + list(set(reserved.tokens.values()))
significant_ws = significant_ws_tokens + significant_ws_literals + list(set(reserved.tokens.values()))