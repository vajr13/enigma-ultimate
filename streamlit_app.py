import streamlit as st
import time

rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def rotate(rotor, offset):
    return rotor[offset:] + rotor[:offset]

def plugboard_swap(char, plugboard):
    return plugboard.get(char, char)

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

def enigma_process(message, rotor1, rotor2, rotor3, rotor_pos1, rotor_pos2, rotor_pos3, plugboard):
    processed_message = ""
    for char in message:
        if char.isalpha():
            processed_message += encrypt_character(char.upper(), rotor1, rotor2, rotor3, reflector, plugboard)
            rotor_pos1 += 1
            if rotor_pos1 > 26:
                rotor_pos1 = 1
                rotor_pos2 += 1
                if rotor_pos2 > 26:
                    rotor_pos2 = 1
                    rotor_pos3 += 1
                    if rotor_pos3 > 26:
                        rotor_pos3 = 1
            yield processed_message, rotor_pos1, rotor_pos2, rotor_pos3
        else:
            processed_message += char
            yield processed_message, rotor_pos1, rotor_pos2, rotor_pos3

st.title("Enigma Machine with Visible Rotor Movement")
st.info("Simulasi mesin Enigma dengan pergerakan rotor terlihat langsung.")

# Input pesan menggunakan text area
message = st.text_area("Masukkan pesan (paragraf dapat dimasukkan di sini):", "", height=150)

# Tampilan rotor seperti gambar (dengan tombol +/-)
st.subheader("Setel Posisi Rotor (1-26)")

# Setting awal rotor
if "rotor_pos1" not in st.session_state:
    st.session_state.rotor_pos1 = 1
if "rotor_pos2" not in st.session_state:
    st.session_state.rotor_pos2 = 2
if "rotor_pos3" not in st.session_state:
    st.session_state.rotor_pos3 = 3

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"Rotor 1: {st.session_state.rotor_pos1}")
with col2:
    st.write(f"Rotor 2: {st.session_state.rotor_pos2}")
with col3:
    st.write(f"Rotor 3: {st.session_state.rotor_pos3}")

# Plugboard
if "plugboard" not in st.session_state:
    st.session_state.plugboard = {}
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None
if "pending_pair" not in st.session_state:
    st.session_state.pending_pair = None

st.subheader("Plugboard: Klik dua huruf untuk memasangkan")

cols = st.columns(13)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i, char in enumerate(alphabet):
    col = cols[i % 13]

    paired_char = st.session_state.plugboard.get(char, "")
    col.markdown(f"<div style='text-align: center; font-size: 1.5em;'>{paired_char}</div>", unsafe_allow_html=True)

    if col.button(f"{char}", key=f"button_{char}"):
        if st.session_state.selected_button is None:
            st.session_state.selected_button = char
        elif st.session_state.selected_button == char:
            st.session_state.selected_button = None
        else:
            char1 = st.session_state.selected_button
            char2 = char
            st.session_state.pending_pair = (char1, char2)
            st.session_state.selected_button = None

if st.session_state.pending_pair:
    char1, char2 = st.session_state.pending_pair
    if char1 in st.session_state.plugboard:
        del st.session_state.plugboard[st.session_state.plugboard[char1]]
        del st.session_state.plugboard[char1]
    if char2 in st.session_state.plugboard:
        del st.session_state.plugboard[st.session_state.plugboard[char2]]
        del st.session_state.plugboard[char2]
    time.sleep(0.5)
    st.session_state.plugboard[char1] = char2
    st.session_state.plugboard[char2] = char1
    st.session_state.pending_pair = None

if st.button("Reset Plugboard"):
    st.session_state.plugboard.clear()
    st.session_state.selected_button = None
    st.write("Plugboard telah direset.")

# Buat tombol untuk tiap karakter A-Z
st.subheader("Masukkan Karakter")

button_columns = st.columns(13)
for i, char in enumerate(alphabet):
    col = button_columns[i % 13]
    if col.button(f"{char}"):
        message += char  # Menambahkan karakter yang dipilih ke pesan

# Tombol untuk memulai enkripsi
if st.button("Proses"):
    if message:
        progress = st.empty()
        rotors_display = st.empty()
        encrypted_message = ""
        for step, (encrypted_message, pos1, pos2, pos3) in enumerate(enigma_process(message, rotor_1, rotor_2, rotor_3, st.session_state.rotor_pos1, st.session_state.rotor_pos2, st.session_state.rotor_pos3, st.session_state.plugboard)):
            rotors_display.write(f"Posisi Rotor: Rotor 1 = {pos1}, Rotor 2 = {pos2}, Rotor 3 = {pos3}")
            progress.write(f"Proses: {encrypted_message}")
            time.sleep(0.1)  # Delay untuk mensimulasikan pergerakan
        st.success("Proses selesai!")
        st.write("Pesan yang diproses:", encrypted_message)
    else:
        st.warning("Masukkan pesan terlebih dahulu!")
