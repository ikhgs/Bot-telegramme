from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Dictionnaire pour stocker l'historique de chaque utilisateur
user_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour! Posez-moi une question.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Récupérer l'historique de l'utilisateur, limiter à 5 derniers échanges
    history = user_history.get(user_id, [])
    
    # Ajouter le nouveau message à l'historique
    history.append(user_message)
    
    # Limiter l'historique à 5 derniers échanges
    if len(history) > 5:
        history = history[-5:]

    # Construire la requête avec l'historique
    concatenated_history = ' '.join(history)
    response = requests.get(f"https://llama3-70b.vercel.app/api?ask={concatenated_history}")
    
    # Extraire la réponse JSON
    bot_reply = response.json().get("response", "Désolé, je n'ai pas compris votre demande.")
    
    # Ajouter la réponse de l'API à l'historique
    history.append(bot_reply)
    
    # Stocker l'historique mis à jour
    user_history[user_id] = history

    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token('VOTRE_TELEGRAM_BOT_TOKEN').build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
  
