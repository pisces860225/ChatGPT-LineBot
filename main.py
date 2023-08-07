from libs.service import Service
from libs.service.pinews_argparse import Args
from libs import configs

Args().debug_controller()


def pinew_linebot_program():
    app = Service(
        title=configs.SERVERTITLE,
        description=configs.DESCRIPTION,
        version=configs.VERSION,
    )
    app.service_run()


def main():
    pinew_linebot_program()


if __name__ == "__main__":
    main()
