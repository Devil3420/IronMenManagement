import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CallbackQueryHandler, run_async
from telegram.utils.helpers import mention_html

import IronMenRobot.modules.sql.approve_sql as sql
from IronMenRobot import DRAGONS, dispatcher
from IronMenRobot.modules.disable import DisableAbleCommandHandler
from IronMenRobot.modules.helper_funcs.chat_status import user_admin
from IronMenRobot.modules.helper_funcs.extraction import extract_user
from IronMenRobot.modules.log_channel import loggable


@loggable
@user_admin
@run_async
def approve(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ!"
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status == "administrator" or member.status == "creator":
        message.reply_text(
            "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ **ᴀᴅᴍɪɴ** - ʟᴏᴄᴋꜱ, ʙʟᴏᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴀʟʀᴇᴀᴅʏ ᴅᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ."
        )
        return ""
    if sql.is_approved(message.chat_id, user_id):
        message.reply_text(
            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ{chat_title}",
            parse_mode=ParseMode.MARKDOWN,
        )
        return ""
    sql.approve(message.chat_id, user_id)
    message.reply_text(
        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) ʜᴀꜱ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title}! ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ʙᴇ ɪɢɴᴏʀᴇᴅ ʙʏ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴀᴅᴍɪɴ ᴀᴄᴛɪᴏɴꜱ ʟɪᴋᴇ ʟᴏᴄᴋꜱ, ʙʟᴏᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴀɴᴛɪꜰʟᴏᴏᴅ.",
        parse_mode=ParseMode.MARKDOWN,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#APPROVED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@loggable
@user_admin
@run_async
def disapprove(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ!"
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status == "administrator" or member.status == "creator":
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴ, ᴛʜᴇʏ ᴄᴀɴ'ᴛ ʙᴇ ᴜɴᴀᴘᴘʀᴏᴠᴇᴅ.")
        return ""
    if not sql.is_approved(message.chat_id, user_id):
        message.reply_text(f"{member.user['first_name']} isn't approved yet!")
        return ""
    sql.disapprove(message.chat_id, user_id)
    message.reply_text(
        f"{member.user['first_name']} ɪꜱ ɴᴏ ʟᴏɴɢᴇʀ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title}."
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNAPPROVED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@user_admin
@run_async
def approved(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    msg = "ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ.\n"
    approved_users = sql.list_approved(message.chat_id)
    for i in approved_users:
        member = chat.get_member(int(i.user_id))
        msg += f"- `{i.user_id}`: {member.user['first_name']}\n"
    if msg.endswith("approved.\n"):
        message.reply_text(f"ɴᴏ ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ {chat_title}.")
        return ""
    else:
        message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


@user_admin
@run_async
def approval(update, context):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    user_id = extract_user(message, args)
    member = chat.get_member(int(user_id))
    if not user_id:
        message.reply_text(
            "I ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ!"
        )
        return ""
    if sql.is_approved(message.chat_id, user_id):
        message.reply_text(
            f"{member.user['first_name']} ɪs ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀ. Lᴏᴄᴋs, ᴀɴᴛɪғʟᴏᴏᴅ, ᴀɴᴅ ʙʟᴏᴄᴋʟɪsᴛs ᴡᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ."
        )
    else:
        message.reply_text(
            f"{member.user['first_name']} s ɴᴏᴛ ᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀ. Tʜᴇʏ ᴀʀᴇ ᴀғғᴇᴄᴛᴇᴅ ʙʏ ɴᴏʀᴍᴀʟ ᴄᴏᴍᴍᴀɴᴅs."
        )


@run_async
def unapproveall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "Oɴʟʏ ᴛʜᴇ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜɴᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜsᴇʀs ᴀᴛ ᴏɴᴄᴇ."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Uɴᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜsᴇʀs", callback_data="unapproveall_user"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Cᴀɴᴄᴇʟ", callback_data="unapproveall_cancel"
                    )
                ],
            ]
        )
        update.effective_message.reply_text(
            f"Aʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ᴜɴᴀᴘᴘʀᴏᴠᴇ ALL ᴜsᴇʀs ɪɴ {chat.title}? Tʜɪs ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


@run_async
def unapproveall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "unapproveall_user":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            approved_users = sql.list_approved(chat.id)
            users = [int(i.user_id) for i in approved_users]
            for user_id in users:
                sql.disapprove(chat.id, user_id)

        if member.status == "administrator":
            query.answer("Oɴʟʏ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪs.")

        if member.status == "member":
            query.answer("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")
    elif query.data == "unapproveall_cancel":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            message.edit_text("Rᴇᴍᴏᴠɪɴɢ ᴏғ ᴀʟʟ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜsᴇʀs ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
            return ""
        if member.status == "administrator":
            query.answer("Oɴʟʏ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴄᴀɴ ᴅᴏ ᴛʜɪs.")
        if member.status == "member":
            query.answer("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ᴛʜɪs.")


APPROVE = DisableAbleCommandHandler("approve", approve)
DISAPPROVE = DisableAbleCommandHandler("unapprove", disapprove)
APPROVED = DisableAbleCommandHandler("approved", approved)
APPROVAL = DisableAbleCommandHandler("approval", approval)
UNAPPROVEALL = DisableAbleCommandHandler("unapproveall", unapproveall)
UNAPPROVEALL_BTN = CallbackQueryHandler(unapproveall_btn, pattern=r"unapproveall_.*")

dispatcher.add_handler(APPROVE)
dispatcher.add_handler(DISAPPROVE)
dispatcher.add_handler(APPROVED)
dispatcher.add_handler(APPROVAL)
dispatcher.add_handler(UNAPPROVEALL)
dispatcher.add_handler(UNAPPROVEALL_BTN)

__mod_name__ = "Aᴘᴘʀᴏᴠᴇmain"

__command_list__ = ["approve", "unapprove", "approved", "approval"]
__handlers__ = [APPROVE, DISAPPROVE, APPROVED, APPROVAL]
