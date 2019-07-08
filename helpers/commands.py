# TODO: local get_show() function. search database before asking the api

import pytvmaze
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from user import User
from helpers import util


class Commands:
    # Mixin class for Telegram commands

    def start(self, update, context):
        user_id = str(update.message.from_user.id)
        user = User(user_id, self.db)

        # create a new user if user doesn't exist
        if not user.exists():
            user.create()

        update.effective_message.reply_text("Beep, boop!")

    def unknown(self, update, context):
        update.effective_message.reply_text("I don't know that command.")

    def search(self, update, context):
        search_query = " ".join(context.args)

        try:
            shows = pytvmaze.show_search(search_query)
        except Exception:
            shows = None

        if shows:
            # an inline keyboard with show names as buttons.
            # callback_data will be prefixed with "show_picked_" + show_id
            buttons = [
                    [InlineKeyboardButton(
                        show.name,
                        callback_data="show_picked_"+str(show.maze_id)
                        )] for show in shows
                    ]
            reply_markup = InlineKeyboardMarkup(buttons)
            update.effective_message.reply_text(
                    "Here's what I found.",
                    reply_markup=reply_markup
                    )

        else:
            update.effective_message.reply_text(
                    "Sorry, I couldn't find that show."
                    )

    def show_picked(self, update, context):
        user_id = str(update.effective_user.id)
        # remove leading "show_picked_"
        show_id = update.callback_query.data[12:]

        update.callback_query.answer()

        user = User(user_id, self.db)
        if user.has_show(show_id):
            button_text = "Remove from Favorites"
            button_callback_data = "remove_show_" + show_id
        else:
            button_text = "Add to Favorites"
            button_callback_data = "add_show_" + show_id

        try:
            show = self.api.get_show(maze_id=show_id)
        except Exception:
            show = None

        # get show poster
        try:
            photo = show.image["medium"]
        except Exception:
            # get rid of this
            photo = "https://via.placeholder.com/500"

        if show:
            caption = util.format_show_info(show)
            buttons = [
                    [InlineKeyboardButton(
                        button_text,
                        callback_data=button_callback_data
                        )]
                    ]
            reply_markup = InlineKeyboardMarkup(buttons)

            update.effective_message.delete()

            context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                    )
        else:
            update.effective_message.edit_text("Something went wrong..")

    def add_show(self, update, context):
        user_id = str(update.effective_user.id)
        show_id = update.callback_query.data[9:]

        update.callback_query.answer()

        try:
            # replace with database function
            show = self.api.get_show(maze_id=show_id)
            show_name = getattr(show, "name")
            user = User(user_id, self.db)

            user.add_show(show_id, show_name)

            update.effective_message.delete()
            update.effective_chat.send_message(
                    "{} was added to your favorites.".format(show_name)
                    )
        except Exception:
            update.effective_chat.send_message("Error adding show.")

    def remove_show(self, update, context):
        user_id = str(update.effective_user.id)
        # extract show_id from remove_show_<show_id>
        show_id = update.callback_query.data[12:]

        update.callback_query.answer()

        try:
            show = self.api.get_show(maze_id=show_id)
            show_name = getattr(show, "name")
            user = User(user_id, self.db)

            user.remove_show(show_id)

            update.effective_message.delete()
            update.effective_chat.send_message(
                    "{} was removed from your favorites.".format(show_name)
                    )
        except Exception:
            update.effective_chat.send_message("Error removing show.")

    def list_favorites(self, update, context):
        user_id = str(update.effective_user.id)
        user = User(user_id, self.db)

        try:
            shows = user.get_shows()
        except Exception:
            shows = []

        if shows:
            buttons = [
                    [InlineKeyboardButton(
                        show[1],
                        callback_data="show_picked_"+show[0])]
                    for show in shows
                    # show is a tuple with (show_id, show_name)
                    ]
            reply_markup = InlineKeyboardMarkup(buttons)
            update.effective_message.reply_text(
                    text="Your favorites:",
                    reply_markup=reply_markup
                    )
        else:
            update.effective_message.reply_text("Error getting favorites.")
