import streamlit as st
import random
import string

def generate_password(length, use_digits, use_special):
    # Basis: Groß- und Kleinbuchstaben
    characters = string.ascii_letters
    
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    # Passwort zufällig zusammenbauen
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    st.title("🔐 Sicherer Passwort-Generator")
    st.write("Erstelle im Handumdrehen sichere Passwörter für deine Konten.")

    # Einstellungen in der Seitenleiste oder Hauptseite
    length = st.slider("Passwortlänge", min_value=6, max_value=32, value=12)
    use_digits = st.checkbox("Zahlen einschließen (0-9)", value=True)
    use_special = st.checkbox("Sonderzeichen einschließen (!@#$...)", value=True)

    # Button zum Generieren
    if st.button("Passwort generieren", type="primary"):
        password = generate_password(length, use_digits, use_special)
        
        # Ergebnis anzeigen
        st.success("Dein neues Passwort:")
        st.code(password, language="")
        st.caption("Klicke rechts oben in der Box, um das Passwort zu kopieren!")

if __name__ == "__main__":
    main()
