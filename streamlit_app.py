import streamlit as st
import string

# Rotor dan Reflector
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Warna untuk Plugboard
plugboard_colors = [
    "#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6", 
    "#1ABC9C", "#E74C3C", "#8E44AD", "#27AE60", "#2980B9", 
    "#F39C12", "#D35400", "#34495E"
]

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

# Inisialisasi State
if "rotor_pos1" not in st.session_state:
    st.session_state.rotor_pos1 = 1
if "rotor_pos2" not in st.session_state:
    st.session_state.rotor_pos2 = 1
if "rotor_pos3" not in st.session_state:
    st.session_state.rotor_pos3 = 1
if "input_message" not in st.session_state:
    st.session_state.input_message = ""
if "output_message" not in st.session_state:
    st.session_state.output_message = ""
if "plugboard" not in st.session_state:
    st.session_state.plugboard = {}
if "is_locked" not in st.session_state:
    st.session_state.is_locked = False
if "selected_plugboard" not in st.session_state:
    st.session_state.selected_plugboard = []

# Fungsi untuk Memproses Satu Karakter
def process_character(char):
    # Rotor 1 bergerak sebelum memproses karakter
    st.session_state.rotor_pos1 += 1
    if st.session_state.rotor_pos1 > 26:
        st.session_state.rotor_pos1 = 1
        st.session_state.rotor_pos2 += 1
        if st.session_state.rotor_pos2 > 26:
            st.session_state.rotor_pos2 = 1
            st.session_state.rotor_pos3 += 1
            if st.session_state.rotor_pos3 > 26:
                st.session_state.rotor_pos3 = 1

    # Update posisi rotor setelah pergerakan
    rotor1 = rotate(rotor_1, st.session_state.rotor_pos1 - 1)
    rotor2 = rotate(rotor_2, st.session_state.rotor_pos2 - 1)
    rotor3 = rotate(rotor_3, st.session_state.rotor_pos3 - 1)

    # Enkripsi karakter
    encrypted_char = encrypt_character(
        char, rotor1, rotor2, rotor3, reflector, st.session_state.plugboard
    )
    st.session_state.input_message += char
    st.session_state.output_message += encrypted_char

# Fungsi untuk Menghapus Karakter Terakhir
def delete_last_character():
    if st.session_state.input_message:
        st.session_state.input_message = st.session_state.input_message[:-1]
        st.session_state.output_message = st.session_state.output_message[:-1]

        # Putar rotor mundur
        st.session_state.rotor_pos1 -= 1
        if st.session_state.rotor_pos1 < 1:
            st.session_state.rotor_pos1 = 26
            st.session_state.rotor_pos2 -= 1
            if st.session_state.rotor_pos2 < 1:
                st.session_state.rotor_pos2 = 26
                st.session_state.rotor_pos3 -= 1
                if st.session_state.rotor_pos3 < 1:
                    st.session_state.rotor_pos3 = 26

# Fungsi untuk Mengunci/Membuka Kunci
def toggle_lock():
    if st.session_state.is_locked:
        st.session_state.is_locked = False
        st.session_state.input_message = ""
        st.session_state.output_message = ""
    else:
        st.session_state.is_locked = True

# Judul
st.title("Enigma Machine with Real-Time Plugboard Colors and Rotor Fix")

# Tombol Lock/Unlock
if st.session_state.is_locked:
    if st.button("Unlock Machine"):
        toggle_lock()
else:
    if st.button("Lock Machine"):
        toggle_lock()

# Setel dan Monitoring Posisi Rotor
st.subheader("Setel dan Monitoring Posisi Rotor (1-26)")
col1, col2, col3 = st.columns(3)
with col1:
    rotor1_input = st.number_input("Rotor 1", min_value=1, max_value=26, value=st.session_state.rotor_pos1, step=1, disabled=st.session_state.is_locked)
with col2:
    rotor2_input = st.number_input("Rotor 2", min_value=1, max_value=26, value=st.session_state.rotor_pos2, step=1, disabled=st.session_state.is_locked)
with col3:
    rotor3_input = st.number_input("Rotor 3", min_value=1, max_value=26, value=st.session_state.rotor_pos3, step=1, disabled=st.session_state.is_locked)

if not st.session_state.is_locked and st.button("Set Posisi Rotor"):
    st.session_state.rotor_pos1 = rotor1_input
    st.session_state.rotor_pos2 = rotor2_input
    st.session_state.rotor_pos3 = rotor3_input

# Konfigurasi Plugboard
st.subheader("Konfigurasi Plugboard (Klik Dua Huruf untuk Memasangkan)")
cols = st.columns(13)
alphabet = string.ascii_uppercase
for i, char in enumerate(alphabet):
    col = cols[i % 13]
    color = next((plugboard_colors[i] for i, (k, v) in enumerate(st.session_state.plugboard.items()) if k == char or v == char), "white")
    if not st.session_state.is_locked:
        if col.button(char):
            st.session_state.selected_plugboard.append(char)
            if len(st.session_state.selected_plugboard) == 2:
                a, b = st.session_state.selected_plugboard
                st.session_state.plugboard[a] = b
                st.session_state.plugboard[b] = a
                st.session_state.selected_plugboard = []
    col.markdown(f"<div style='background-color: {color}; text-align: center;'>{char}</div>", unsafe_allow_html=True)

if not st.session_state.is_locked and st.button("Reset Plugboard"):
    st.session_state.plugboard.clear()

# Input Karakter melalui Tombol
st.subheader("Input Karakter (A-Z)")
cols = st.columns(13)
if st.session_state.is_locked:
    for i, char in enumerate(alphabet):
        col = cols[i % 13]
        if col.button(char):
            process_character(char)

# Tombol Hapus
if st.button("Hapus Karakter Terakhir"):
    delete_last_character()

# Pesan Input dan Output
st.subheader("Pesan Input dan Output")
col1, col2 = st.columns(2)
with col1:
    st.text_area("Teks Input", value=st.session_state.input_message, height=200)
with col2:
    st.text_area("Teks Output (Terenkripsi)", value=st.session_state.output_message, height=200)
