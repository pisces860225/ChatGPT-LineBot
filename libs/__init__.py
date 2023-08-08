from libs import configs
from libs.service import Service
from libs.service.pinews_argparse import Args


Args().debug_controller()


def pinew_linebot_program() -> None:
    app = Service(
        title=configs.SERVERTITLE,
        description=configs.DESCRIPTION,
        version=configs.VERSION,
    )
    app.service_run()
