# NOTE: some pytvmaze functions are outside the TVMaze class

# TODO: send chat actions (typing...) while processing
# TODO: scrollable menus

import logging

import pytvmaze
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, \
        MessageHandler, Filters

from helpers.commands import Commands
from helpers.db import DB

# logging.basicConfig(
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         level=logging.INFO
#         )


class TvTime(Commands):
    def __init__(self, access_token, database_url):
        self.api = pytvmaze.TVMaze()
        self.db = DB(database_url)
        self.access_token = access_token

        self.updater = Updater(token=self.access_token, use_context=True)
        dispatcher = self.updater.dispatcher

        start_handler = CommandHandler("start", self.start)
        search_handler = CommandHandler("search", self.search)
        list_handler = CommandHandler("list", self.list_favorites)
        show_picked_handler = CallbackQueryHandler(
                self.show_picked,
                pattern="show_picked_*"
                )
        add_show_handler = CallbackQueryHandler(
                self.add_show,
                pattern="add_show_*"
                )
        remove_show_handler = CallbackQueryHandler(
                self.remove_show,
                pattern="remove_show_*"
                )
        unknown_handler = MessageHandler(Filters.command, self.unknown)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(search_handler)
        dispatcher.add_handler(add_show_handler)
        dispatcher.add_handler(remove_show_handler)
        dispatcher.add_handler(show_picked_handler)
        dispatcher.add_handler(list_handler)
        dispatcher.add_handler(unknown_handler)

    def run(self, app_url=None, port=8443, url_path="/tvtimebot"):
        if app_url:
            print("running webhook on " + app_url)
            self.updater.start_webhook(
                    listen="0.0.0.0",
                    port=port,
                    url_path=url_path
                    )
            self.updater.bot.set_webhook(app_url.rstrip("/")+url_path)
            self.updater.idle()
        else:
            print("polling")
            self.updater.start_polling()
