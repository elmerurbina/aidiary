import random
from datetime import datetime
from models import DiaryEntry

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

# Welcome message in Spanish
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
    if "quiero saber mis entradas del dia" in message:
        try:
            # Extract the date from the message
            date_str = message.split("del dia ")[1].strip()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Retrieve entries for the specified date
            entries = DiaryEntry.get_entries_by_user(user_id)
            entries_for_date = [entry for entry in entries if entry[2] == date]

            if entries_for_date:
                response = f"Entradas para el {date_str}:\n"
                for entry in entries_for_date:
                    response += f"- {entry[3]}\n"
                return response
            else:
                return f"No hay entradas para el {date_str}."
        except Exception as e:
            return "Lo siento, no pude entender la fecha. Asegúrate de usar el formato yyyy-mm-dd."

    # Default response for new diary entries
    return f"{generate_random_response()}."

# Example usage
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