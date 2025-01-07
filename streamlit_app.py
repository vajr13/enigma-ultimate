import streamlit as st
import string

# Rotor dan Reflector
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Fungsi untuk Rotor dan Plugboard
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

# Inisialisasi State untuk Rotor, Plugboard, dan Pesan
if "rotor_pos1" not in st.session_state:
    st.session_state.rotor_pos1 = 1
if "rotor_pos2" not in st.session_state:
    st.session_state.rotor_pos2 = 1
if "rotor_pos3" not in st.session_state:
    st.session_state.rotor_pos3 = 1
if "processed_message" not in st.session_state:
    st.session_state.processed_message = ""
if "plugboard" not in st.session_state:
    st.session_state.plugboard = {}

# Fungsi untuk Memproses Satu Karakter
def process_character(char):
    rotor1 = rotate(rotor_1, st.session_state.rotor_pos1 - 1)
    rotor2 = rotate(rotor_2, st.session_state.rotor_pos2 - 1)
    rotor3 = rotate(rotor_3, st.session_state.rotor_pos3 - 1)

    encrypted_char = encrypt_character(
        char, rotor1, rotor2, rotor3, reflector, st.session_state.plugboard
    )
    st.session_state.processed_message += encrypted_char

    # Pergerakan Rotor
    st.session_state.rotor_pos1 += 1
    if st.session_state.rotor_pos1 > 26:
        st.session_state.rotor_pos1 = 1
        st.session_state.rotor_pos2 += 1
        if st.session_state.rotor_pos2 > 26:
            st.session_state.rotor_pos2 = 1
            st.session_state.rotor_pos3 += 1
            if st.session_state.rotor_pos3 > 26:
                st.session_state.rotor_pos3 = 1

# Judul
st.title("Enigma Machine with Real-Time Rotor Monitoring")

# Setel Posisi Rotor Awal
st.subheader("Setel Posisi Awal Rotor (1-26)")
col1, col2, col3 = st.columns(3)
with col1:
    st.number_input("Rotor 1", min_value=1, max_value=26, value=st.session_state.rotor_pos1, step=1, key="rotor_input1")
with col2:
    st.number_input("Rotor 2", min_value=1, max_value=26, value=st.session_state.rotor_pos2, step=1, key="rotor_input2")
with col3:
    st.number_input("Rotor 3", min_value=1, max_value=26, value=st.session_state.rotor_pos3, step=1, key="rotor_input3")

if st.button("Set Posisi Rotor"):
    st.session_state.rotor_pos1 = st.session_state.rotor_input1
    st.session_state.rotor_pos2 = st.session_state.rotor_input2
    st.session_state.rotor_pos3 = st.session_state.rotor_input3

# Monitoring Posisi Rotor
st.subheader("Monitoring Posisi Rotor")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Rotor 1")
    st.write(st.session_state.rotor_pos1)
with col2:
    st.markdown("### Rotor 2")
    st.write(st.session_state.rotor_pos2)
with col3:
    st.markdown("### Rotor 3")
    st.write(st.session_state.rotor_pos3)

# Konfigurasi Plugboard
st.subheader("Konfigurasi Plugboard (Opsional)")
plugboard_input = st.text_input("Masukkan pasangan plugboard (contoh: AB, CD, EF)", "")
if st.button("Set Plugboard"):
    plugboard = {}
    for pair in plugboard_input.split(","):
        pair = pair.strip().upper()
        if len(pair) == 2:
            plugboard[pair[0]] = pair[1]
            plugboard[pair[1]] = pair[0]
    st.session_state.plugboard = plugboard
st.write("Plugboard saat ini:", st.session_state.plugboard)

# Input Karakter melalui Tombol
st.subheader("Input Karakter (A-Z)")
cols = st.columns(13)
alphabet = string.ascii_uppercase

for i, char in enumerate(alphabet):
    col = cols[i % 13]
    if col.button(char):
        process_character(char)

# Reset Rotor dan Pesan
if st.button("Reset Rotor dan Pesan"):
    st.session_state.rotor_pos1 = 1
    st.session_state.rotor_pos2 = 1
    st.session_state.rotor_pos3 = 1
    st.session_state.processed_message = ""
    st.session_state.plugboard = {}

# Tampilkan Pesan Hasil Enkripsi
st.subheader("Pesan Terenkripsi")
st.write(st.session_state.processed_message)
