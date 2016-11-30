from horse import build_app

application = build_app(name=__name__, debug=True).web_app


if __name__ == "__main__":
    application.run()
