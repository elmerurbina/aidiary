import random
from datetime import datetime
import re
from textblob import TextBlob
from models.models import DiaryEntry

# List of random responses
random_responses = [
    "interesante tu mensaje ha sido guardado exitosamente!",
    "fascinante tu mensaje ha sido guardado exitosamente!",
    "increíble tu mensaje ha sido guardado exitosamente!",
    "asombroso tu mensaje ha sido guardado exitosamente!",
    "genial tu mensaje ha sido guardado exitosamente!",
    "impresionante tu mensaje ha sido guardado exitosamente!",
    "maravilloso tu mensaje ha sido guardado exitosamente!",
    "sorprendente tu mensaje ha sido guardado exitosamente!",
    "extraordinario tu mensaje ha sido guardado exitosamente!",
    "espectacular tu mensaje ha sido guardado exitosamente!"
]

WELCOME_MESSAGE = (
    "¡Bienvenido a tu diario AI! 📔\n\n"
    "Para obtener información de una fecha específica, escribe:\n"
    "`quiero saber mis entradas del dia yyyy-mm-dd`\n"
    "Reemplaza `yyyy` con el año actual, `mm` con el mes actual, y `dd` con el día actual, todo en números.\n\n"
    "Para registrar nueva información, simplemente escribe tu mensaje y envíalo.\n\n"
    "¡Estoy aquí para ayudarte!"
)


# Function to generate a random response
def generate_random_response():
    return random.choice(random_responses)


# Function to analyze sentiment of the message
def analyze_sentiment(message):
    # Create a TextBlob object
    blob = TextBlob(message)

    # Get sentiment polarity (-1 to 1 scale)
    polarity = blob.sentiment.polarity

    # Determine the sentiment emoji based on polarity
    if polarity > 0:
        sentiment_emoji = "😊"
        follow_up_message = "💬 ¡Qué bueno que tengas pensamientos positivos! Sigue así."
    elif polarity < 0:
        sentiment_emoji = "😢"
        follow_up_message = "💬 Lamento que te sientas así. Si necesitas hablar más, estoy aquí."
    else:
        sentiment_emoji = "😐"
        follow_up_message = "💬 Gracias por compartir tus pensamientos."

    return sentiment_emoji, follow_up_message


# Function to handle user messages
def handle_user_message(user_id, message):
    # Convert message to lowercase for easier processing
    message = message.lower()

    # Check if the user is greeting
    if any(greeting in message for greeting in ["hola", "buenos días", "cómo estás"]):
        return random.choice([
            "¡Hola! ¿Cómo estás hoy?",
            "¡Buenos días! ¿En qué puedo ayudarte?",
            "¡Hola! Espero que estés teniendo un gran día."
        ])

    # Check if the user is requesting entries for a specific date
    # Extract date using regex
    match = re.search(r"(\d{4}-\d{2}-\d{2})", message)
    if match:
        date_str = match.group(1)
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return "La fecha ingresada no es válida. Usa el formato yyyy-mm-dd."

        # Retrieve diary entries for the date
        entries = DiaryEntry.get_entries_by_user(user_id, date)
        print(f"User ID: {user_id}, Entry Date: {date}, Entries: {entries}")

        if entries:
            response = f"📅 Entradas para el {date_str}:\n"
            for entry in entries:
                sentiment_emoji = "😊" if entry[4] == "positive" else "😢" if entry[4] == "negative" else "😐"
                response += f"- 📝 {entry[2]} (Sentimiento: {entry[4]} {sentiment_emoji}, Hora: {entry[5].strftime('%H:%M:%S')})\n"

            # Send a follow-up message based on sentiment
            if any(entry[4] == "positive" for entry in entries):
                response += "💬 ¡Qué bueno que tengas pensamientos positivos! Sigue así."
            elif any(entry[4] == "negative" for entry in entries):
                response += "💬 Lamento que te sientas así. Si necesitas hablar más, estoy aquí."
            else:
                response += "💬 Gracias por compartir tus pensamientos."

            return response
        else:
            return f"❌ No hay entradas registradas para el {date_str}."

    # Default response for new diary entries
    DiaryEntry.create_entry(user_id, message)

    # Analyze the sentiment of the message
    sentiment_emoji, follow_up_message = analyze_sentiment(message)

    return f"{generate_random_response()} {follow_up_message}"


# Example usage in console
if __name__ == "__main__":
    # Simulate a user interaction
    user_id = 1  # Replace with the actual user ID
    print(WELCOME_MESSAGE)

    while True:
        user_message = input("\nTú: ")
        if user_message.lower() in ["salir", "exit"]:
            print("Diario AI: ¡Hasta luego!")
            break

        response = handle_user_message(user_id, user_message)
        print(f"Diario AI: {response}")
