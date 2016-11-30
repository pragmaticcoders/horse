from horse import build_app

application = build_app(__name__, debug=True)


if __name__ == "__main__":
    application.run()
