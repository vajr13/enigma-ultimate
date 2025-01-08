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
if "is_first_input" not in st.session_state:
    st.session_state.is_first_input = True
if "is_first_delete" not in st.session_state:
    st.session_state.is_first_delete = True

# Fungsi untuk Memproses Satu Karakter
def process_character(char):
    # Naikkan rotor 1 sebelum memproses karakter jika ini input pertama
    if st.session_state.is_first_input:
        st.session_state.rotor_pos1 += 1
        if st.session_state.rotor_pos1 > 26:
            st.session_state.rotor_pos1 = 1
            st.session_state.rotor_pos2 += 1
            if st.session_state.rotor_pos2 > 26:
                st.session_state.rotor_pos2 = 1
                st.session_state.rotor_pos3 += 1
                if st.session_state.rotor_pos3 > 26:
                    st.session_state.rotor_pos3 = 1
        st.session_state.is_first_input = False

    # Enkripsi karakter
    rotor1 = rotate(rotor_1, st.session_state.rotor_pos1 - 1)
    rotor2 = rotate(rotor_2, st.session_state.rotor_pos2 - 1)
    rotor3 = rotate(rotor_3, st.session_state.rotor_pos3 - 1)

    encrypted_char = encrypt_character(
        char, rotor1, rotor2, rotor3, reflector, st.session_state.plugboard
    )

    st.session_state.input_message += char
    st.session_state.output_message += encrypted_char

    # Pergerakan rotor setelah input diproses
    st.session_state.rotor_pos1 += 1
    if st.session_state.rotor_pos1 > 26:
        st.session_state.rotor_pos1 = 1
        st.session_state.rotor_pos2 += 1
        if st.session_state.rotor_pos2 > 26:
            st.session_state.rotor_pos2 = 1
            st.session_state.rotor_pos3 += 1
            if st.session_state.rotor_pos3 > 26:
                st.session_state.rotor_pos3 = 1

# Fungsi untuk Menghapus Karakter Terakhir
def delete_last_character():
    if st.session_state.input_message:
        # Pastikan rotor bergerak turun hanya jika karakter sudah diinput sebelumnya
        if st.session_state.is_first_delete:
            st.session_state.is_first_delete = False
        else:
            st.session_state.rotor_pos1 -= 1
            if st.session_state.rotor_pos1 < 1:
                st.session_state.rotor_pos1 = 26
                st.session_state.rotor_pos2 -= 1
                if st.session_state.rotor_pos2 < 1:
                    st.session_state.rotor_pos2 = 26
                    st.session_state.rotor_pos3 -= 1
                    if st.session_state.rotor_pos3 < 1:
                        st.session_state.rotor_pos3 = 26

        st.session_state.input_message = st.session_state.input_message[:-1]
        st.session_state.output_message = st.session_state.output_message[:-1]

# Fungsi untuk Mengunci/Membuka Kunci
def toggle_lock():
    if st.session_state.is_locked:
        st.session_state.is_locked = False
        st.session_state.input_message = ""
        st.session_state.output_message = ""
        st.session_state.is_first_input = True
        st.session_state.is_first_delete = True
    else:
        st.session_state.is_locked = True

# Judul
st.title("Enigma Machine with Correct Rotor Movement")

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

# Input Karakter melalui Tombol
st.subheader("Input Karakter (A-Z)")
cols = st.columns(13)
alphabet = string.ascii_uppercase
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
