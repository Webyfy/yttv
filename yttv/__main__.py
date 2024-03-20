import yawebview

USER_AGENT = 'Roku/DVP-23.0 (23.0.0.99999-02)'
YTTV_URL = 'https://www.youtube.com/tv'


def main():
    window = yawebview.Window(
        'YouTube on TV', YTTV_URL, scrollbars=False, context_menu=False)
    yawebview.start(USER_AGENT)


if __name__ == "__main__":
    main()
