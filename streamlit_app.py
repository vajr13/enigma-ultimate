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
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None
if "pending_pair" not in st.session_state:
    st.session_state.pending_pair = None

# Fungsi untuk Memproses Satu Karakter
def process_character(char):
    rotor1 = rotate(rotor_1, st.session_state.rotor_pos1 - 1)
    rotor2 = rotate(rotor_2, st.session_state.rotor_pos2 - 1)
    rotor3 = rotate(rotor_3, st.session_state.rotor_pos3 - 1)

    encrypted_char = encrypt_character(
        char, rotor1, rotor2, rotor3, reflector, st.session_state.plugboard
    )
    st.session_state.input_message += char
    st.session_state.output_message += encrypted_char

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
st.title("Enigma Machine with Integrated Rotor Input and Monitoring")

# Setel dan Monitoring Posisi Rotor
st.subheader("Setel dan Monitoring Posisi Rotor (1-26)")
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

# Konfigurasi Plugboard
st.subheader("Konfigurasi Plugboard: Klik Dua Huruf untuk Memasangkan")
cols = st.columns(13)
alphabet = string.ascii_uppercase

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
    st.session_state.plugboard[char1] = char2
    st.session_state.plugboard[char2] = char1
    st.session_state.pending_pair = None

if st.button("Reset Plugboard"):
    st.session_state.plugboard.clear()

# Input Karakter melalui Tombol
st.subheader("Input Karakter (A-Z)")
cols = st.columns(13)
for i, char in enumerate(alphabet):
    col = cols[i % 13]
    if col.button(char):
        process_character(char)

# Tombol untuk Menghapus Karakter Terakhir
if st.button("Hapus Karakter Terakhir"):
    if st.session_state.input_message:
        st.session_state.input_message = st.session_state.input_message[:-1]
        st.session_state.output_message = st.session_state.output_message[:-1]

# Dua Area untuk Teks Input dan Output
st.subheader("Pesan Input dan Output")
col1, col2 = st.columns(2)
with col1:
    st.text_area("Teks Input", value=st.session_state.input_message, height=200)
with col2:
    st.text_area("Teks Output (Terenkripsi)", value=st.session_state.output_message, height=200)

# Tombol untuk Reset
if st.button("Reset Rotor dan Pesan"):
    st.session_state.rotor_pos1 = 1
    st.session_state.rotor_pos2 = 1
    st.session_state.rotor_pos3 = 1
    st.session_state.input_message = ""
    st.session_state.output_message = ""
