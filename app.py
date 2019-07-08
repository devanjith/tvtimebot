#!/usr/bin/env python3
# main

import os
from tvtime import TvTime

if __name__ == "__main__":
    # get environment variables
    ACCESS_TOKEN = os.environ["TELEGRAM_ACCESS_TOKEN"]
    DATABASE_URL = os.environ["DATABASE_URL"]
    PORT = int(os.environ.get("PORT", "8443"))
    APP_URL = os.environ.get("APP_URL", None)

    app = TvTime(
            access_token=ACCESS_TOKEN,
            database_url=DATABASE_URL
            )

    # will use a webhook if APP_URL is present
    app.run(app_url=APP_URL, port=PORT)
