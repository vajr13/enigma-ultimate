import streamlit as st
import time

# Rotor default dan reflector
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Fungsi rotor
def rotate(rotor, offset):
    return rotor[offset:] + rotor[:offset]

# Fungsi plugboard
def plugboard_swap(char, plugboard):
    return plugboard.get(char, char)

# Fungsi enkripsi karakter
def encrypt_character(char, rotor1, rotor2, rotor3, reflector, plugboard):
    char = plugboard_swap(char, plugboard)
    char = rotor1[ord(char) - ord('A')]
    char = rotor2[ord(char) - ord('A')]
    char = rotor3[ord(char) - ord('A')]
    char = reflector[ord(char) - ord('A')]
    char = chr(rotor3.index(char) + ord('A'))
    char = chr(rotor2.index(char) + ord('A'))
    char = chr(rotor1.index(char) + ord('A'))
    char = plugboard_swap(char, plugboard)
    return char

# Streamlit UI
st.title("Enigma Machine with Dynamic Rotor Visualization")

# Input pesan
message = st.text_input("Masukkan pesan (A-Z):", "")

# Pengaturan rotor awal
st.subheader("Setel Rotor")
rotor_input_1 = st.text_input("Rotor 1", rotor_1)
rotor_input_2 = st.text_input("Rotor 2", rotor_2)
rotor_input_3 = st.text_input("Rotor 3", rotor_3)

# Validasi panjang rotor
if len(rotor_input_1) != 26 or len(rotor_input_2) != 26 or len(rotor_input_3) != 26:
    st.error("Rotor harus memiliki panjang 26 karakter.")
    st.stop()

# Posisi awal rotor
rotor_pos1 = st.slider("Posisi Rotor 1 (1-26)", 1, 26, 1)
rotor_pos2 = st.slider("Posisi Rotor 2 (1-26)", 1, 26, 1)
rotor_pos3 = st.slider("Posisi Rotor 3 (1-26)", 1, 26, 1)

# Plugboard setup
st.subheader("Plugboard")
plugboard = {}
plugboard_input = st.text_area("Masukkan pasangan plugboard (contoh: AB CD EF)", "")
for pair in plugboard_input.split():
    if len(pair) == 2:
        plugboard[pair[0].upper()] = pair[1].upper()
        plugboard[pair[1].upper()] = pair[0].upper()

# Proses enkripsi
if message:
    processed_message = ""
    rotor1 = rotate(rotor_input_1, rotor_pos1 - 1)
    rotor2 = rotate(rotor_input_2, rotor_pos2 - 1)
    rotor3 = rotate(rotor_input_3, rotor_pos3 - 1)
    rotor_display = []

    for i, char in enumerate(message):
        if char.isalpha():
            # Enkripsi karakter
            encrypted_char = encrypt_character(char.upper(), rotor1, rotor2, rotor3, reflector, plugboard)
            processed_message += encrypted_char

            # Rotasi rotor dan log pergerakan
            rotor1 = rotate(rotor1, 1)
            if i % 26 == 25:  # Rotor 2 bergerak setelah 26 rotasi
                rotor2 = rotate(rotor2, 1)
            if i % (26 * 26) == (26 * 26 - 1):  # Rotor 3 bergerak setelah 26*26 rotasi
                rotor3 = rotate(rotor3, 1)

            # Simpan keadaan rotor
            rotor_display.append(f"Step {i + 1}: Rotor1={rotor1}, Rotor2={rotor2}, Rotor3={rotor3}")

    # Tampilkan hasil
    st.subheader("Hasil Enkripsi")
    st.write("Pesan Terproses:", processed_message)

    # Tampilkan log pergerakan rotor
    st.subheader("Visualisasi Pergerakan Rotor")
    for step in rotor_display:
        st.text(step)
