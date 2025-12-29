from datetime import time
from services.sheets import get_portfolio_summary, get_buy_hint


async def daily_report(context):
    chat_id = context.job.chat_id

    message = (
        "📊 *Ежедневный отчёт*\n\n"
        f"{get_portfolio_summary()}\n\n"
        "🛒 *Что можно докупить:*\n"
        f"{get_buy_hint()}"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown"
    )


def enable_notifications(application, chat_id):
    application.job_queue.run_daily(
        daily_report,
        time=time(hour=10, minute=0),
        chat_id=chat_id,
        name=str(chat_id),
    )


def disable_notifications(application, chat_id):
    jobs = application.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()
