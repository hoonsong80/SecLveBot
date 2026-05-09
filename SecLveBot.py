from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import re
from datetime import datetime

async def whos_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Fetch the chat details to find the pinned message
    chat = await context.bot.get_chat(update.effective_chat.id)
    
    if not chat.pinned_message or not chat.pinned_message.text:
        await update.message.reply_text("Please pin a text message containing the leave calendar first!")
        return

    # 2. Get text from the pinned message
    leave_data = chat.pinned_message.text
    today = datetime.now().strftime('%Y-%m-%d')
    out_today = []

    # 3. Parse the message (Expected format: @username YYYY-MM-DD YYYY-MM-DD)
    # This regex finds a username followed by two dates
    pattern = r'(@\w+)\s+(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})'
    matches = re.findall(pattern, leave_data)

    for user, start, end in matches:
        if start <= today <= end:
            out_today.append(user)

    # 4. Reply with the results
    if out_today:
        await update.message.reply_text(f"People on leave today ({today}):\n" + "\n".join(out_today))
    else:
        await update.message.reply_text(f"Everyone is in today! ({today})")

if __name__ == '__main__':
    app = ApplicationBuilder().token("YOUR_API_TOKEN_HERE").build()
    app.add_handler(CommandHandler("whosout", whos_out))
    print("Bot is running...")
    app.run_polling()
