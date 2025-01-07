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
    rotor1 = rotate(rotor1, rotor_pos1 - 1)
    rotor2 = rotate(rotor2, rotor_pos2 - 1)
    rotor3 = rotate(rotor3, rotor_pos3 - 1)
    for char in message:
        if char.isalpha():
            processed_message += encrypt_character(char.upper(), rotor1, rotor2, rotor3, reflector, plugboard)
            rotor1 = rotate(rotor1, 1)
    return processed_message

st.title("Enigma Machine Project - 2C")
st.info("Simulasi mesin Enigma. Gunakan Ctrl+Enter untuk memulai enkripsi/dekripsi.")

# Input pesan menggunakan text area
message = st.text_area("Masukkan pesan (paragraf dapat dimasukkan di sini):", "", height=150)

# Tampilan rotor seperti gambar (dengan tombol +/-)
st.subheader("Setel Posisi Rotor (1-26)")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Rotor 1 Setting")
    rotor_pos1 = st.number_input("", min_value=1, max_value=26, value=1, step=1, label_visibility="collapsed")

with col2:
    st.write("Rotor 2 Setting")
    rotor_pos2 = st.number_input("", min_value=1, max_value=26, value=2, step=1, label_visibility="collapsed")

with col3:
    st.write("Rotor 3 Setting")
    rotor_pos3 = st.number_input("", min_value=1, max_value=26, value=3, step=1, label_visibility="collapsed")

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

# Proses enkripsi/dekripsi menggunakan Ctrl+Enter
if st.button("Proses (Ctrl+Enter untuk shortcut)"):
    if message:
        processed_message = enigma_process(message, rotor_1, rotor_2, rotor_3, rotor_pos1, rotor_pos2, rotor_pos3, st.session_state.plugboard)
        st.write("Pesan yang diproses:", processed_message)
    else:
        st.warning("Masukkan pesan terlebih dahulu!")
