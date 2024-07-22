from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from keep_alive import keep_alive

keep_alive()
TOKEN = '6331990398:AAHwnvku4_nTpUUCUMizqEfVENW0Y6ZJAyM'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "خوش آمدید برای شروع /start را بزنید.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("شروع", callback_data='start')]
        ])
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="موسسه روانپژوهی رویش، مرکز تخصصی خدمات دانشجویی. برای ادامه یک مورد را انتخاب کنید.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("درباره ما", callback_data='about')],
            [InlineKeyboardButton("درخواست مشاوره تلفنی", callback_data='consultation')],
            [InlineKeyboardButton("تماس با ما", callback_data='contact')],
            [InlineKeyboardButton("ثبت پروژه", url='https://t.me/rouyeshno_bot')]
        ])
    )


async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="متن درباره ما.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت", callback_data='start')]
        ])
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="پاسخگویی از شنبه تا چهارشنبه از 8 الی 17\nشماره تماس موسسه : 09180000000\nتلگرام موسسه: ajhdkasd",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت", callback_data='start')]
        ])
    )


async def handle_consultation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="یکی از موارد زیر را انتخاب کنید.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("مشاوره برای پایان نامه", callback_data='thesis')],
            [InlineKeyboardButton("مشاوره برای مقاله", callback_data='article')],
            [InlineKeyboardButton("بازگشت", callback_data='start')]
        ])
    )


async def handle_thesis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['consultation_type'] = 'thesis'
    await query.edit_message_text(
        text="مقطع خود را انتخاب کنید.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("کارشناسی ارشد", callback_data='masters')],
            [InlineKeyboardButton("دکتری", callback_data='phd')],
            [InlineKeyboardButton("بازگشت", callback_data='consultation')]
        ])
    )


async def handle_article(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['consultation_type'] = 'article'
    await query.edit_message_text(
        text="نام و نام خانوادگی و شماره تماس خود را وارد کنید."
    )
    context.user_data['expecting_contact_info'] = True


async def handle_university_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['degree_level'] = query.data
    await query.edit_message_text(
        text="نوع دانشگاه خود را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("دانشگاه آزاد", callback_data='azad')],
            [InlineKeyboardButton("دانشگاه پیام نور", callback_data='payamnoor')],
            [InlineKeyboardButton("دانشگاه دولتی", callback_data='state')],
            [InlineKeyboardButton("دانشگاه غیر انتفاعی", callback_data='nonprofit')],
        ])
    )


async def handle_thesis_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['university_type'] = query.data
    await query.edit_message_text(
        text="موضوع پایان نامه دارید؟",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("موضوع دارم", callback_data='has_topic')],
            [InlineKeyboardButton("موضوع ندارم", callback_data='no_topic')],
        ])
    )


async def handle_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['has_topic'] = query.data == 'has_topic'
    await query.edit_message_text(
        text="پروپوزال دارید؟",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("پروپوزال دارم", callback_data='has_proposal')],
            [InlineKeyboardButton("پروپوزال ندارم", callback_data='no_proposal')],
        ])
    )


async def handle_contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['has_proposal'] = query.data == 'has_proposal'
    await query.edit_message_text(
        text="نام و نام خانوادگی و شماره تماس خود را وارد کنید."
    )
    context.user_data['expecting_contact_info'] = True


async def handle_contact_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('expecting_contact_info'):
        context.user_data['contact_info'] = update.message.text
        context.user_data['expecting_contact_info'] = False
        await update.message.reply_text(
            "اطلاعات با موفقیت ثبت شد. در سریع ترین زمان ممکن با شما تماس خواهیم گرفت.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("بازگشت", callback_data='start')]
            ])
        )


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_start, pattern='^start$'))
    application.add_handler(CallbackQueryHandler(handle_about, pattern='^about$'))
    application.add_handler(CallbackQueryHandler(handle_contact, pattern='^contact$'))
    application.add_handler(CallbackQueryHandler(handle_consultation, pattern='^consultation$'))
    application.add_handler(CallbackQueryHandler(handle_thesis, pattern='^thesis$'))
    application.add_handler(CallbackQueryHandler(handle_article, pattern='^article$'))
    application.add_handler(CallbackQueryHandler(handle_university_type, pattern='^(masters|phd)$'))
    application.add_handler(CallbackQueryHandler(handle_thesis_topic, pattern='^(azad|payamnoor|state|nonprofit)$'))
    application.add_handler(CallbackQueryHandler(handle_proposal, pattern='has_topic'))
    application.add_handler(CallbackQueryHandler(handle_contact_info, pattern='(no_topic|has_proposal|no_proposal)'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contact_message))

    application.run_polling()


if __name__ == '__main__':
    main()
