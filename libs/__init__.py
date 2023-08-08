from libs import configs
from libs.service import Service
from libs.service.pinews_argparse import Args


def pinew_linebot_program() -> None:
    Args().debug_controller()

    app = Service(
        title=configs.SERVERTITLE,
        description=configs.DESCRIPTION,
        version=configs.VERSION,
    )
    app.service_run()
