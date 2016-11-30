from horse import build_app

application = build_app(__name__)


if __name__ == "__main__":
    application.debug = True
    application.run()
