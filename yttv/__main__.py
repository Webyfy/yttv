import yttv.yawebview as yawebview
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

USER_AGENT = 'Roku/DVP-23.0 (23.0.0.99999-02)'
YTTV_URL = 'https://www.youtube.com/tv'

def main():
    window = yawebview.Window(
        'YouTube on TV', YTTV_URL, scrollbars=False, context_menu=False)
    icon = resources.files("yttv").joinpath("icons", "com.webyfy.yttv-48x48.png")
    with resources.as_file(icon) as icon_file:
        window.set_icon("com.webyfy.yttv", [str(icon_file),])
        yawebview.start(USER_AGENT)

if __name__ == "__main__":
    main()
