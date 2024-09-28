#  Copyright (c) 2024
#  by St3vebrush <steve@d3velopment.fr> with love for D3velopment

import sys

sys.path = ['/app/app'] + sys.path

from app import app as app

application = app
