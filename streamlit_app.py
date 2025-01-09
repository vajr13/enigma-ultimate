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
def initialize_state():
    defaults = {
        "rotor_pos1": 1,
        "rotor_pos2": 1,
        "rotor_pos3": 1,
        "input_message": "",
        "output_message": "",
        "plugboard": {},
        "selected_plugboard": [],
        "is_locked": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_state()

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

# Fungsi untuk Reset Plugboard
def reset_plugboard():
    st.session_state.plugboard.clear()
    st.session_state.selected_plugboard = []

# Fungsi untuk Menambah Pasangan Plugboard
def add_plugboard_pair(char):
    st.session_state.selected_plugboard.append(char)
    if len(st.session_state.selected_plugboard) == 2:
        a, b = st.session_state.selected_plugboard
        st.session_state.plugboard[a] = b
        st.session_state.plugboard[b] = a
        st.session_state.selected_plugboard = []

# Judul
st.title("Enigma Machine with Real-Time Output")

# Tombol Lock/Unlock
if st.button("Toggle Lock"):
    st.session_state.is_locked = not st.session_state.is_locked

st.subheader("Setel dan Monitoring Posisi Rotor (1-26)")
col1, col2, col3 = st.columns(3)
with col1:
    rotor1_input = st.number_input("Rotor 1", min_value=1, max_value=26, value=st.session_state.rotor_pos1, step=1, disabled=st.session_state.is_locked)
    st.markdown(f"**Posisi Rotor 1:** {st.session_state.rotor_pos1}")
with col2:
    rotor2_input = st.number_input("Rotor 2", min_value=1, max_value=26, value=st.session_state.rotor_pos2, step=1, disabled=st.session_state.is_locked)
    st.markdown(f"**Posisi Rotor 2:** {st.session_state.rotor_pos2}")
with col3:
    rotor3_input = st.number_input("Rotor 3", min_value=1, max_value=26, value=st.session_state.rotor_pos3, step=1, disabled=st.session_state.is_locked)
    st.markdown(f"**Posisi Rotor 3:** {st.session_state.rotor_pos3}")

if not st.session_state.is_locked and st.button("Set Posisi Rotor"):
    st.session_state.rotor_pos1 = rotor1_input
    st.session_state.rotor_pos2 = rotor2_input
    st.session_state.rotor_pos3 = rotor3_input

# Konfigurasi Plugboard
st.subheader("Konfigurasi Plugboard")
cols = st.columns(13)
alphabet = string.ascii_uppercase
for i, char in enumerate(alphabet):
    col = cols[i % 13]
    if char in st.session_state.plugboard:
        pair_char = st.session_state.plugboard[char]
        color = plugboard_colors[alphabet.index(pair_char) % len(plugboard_colors)]
    else:
        color = "white"
    if not st.session_state.is_locked and col.button(char):
        add_plugboard_pair(char)
    col.markdown(f"<div style='background-color: {color}; text-align: center;'>{char}</div>", unsafe_allow_html=True)

if not st.session_state.is_locked and st.button("Reset Plugboard"):
    reset_plugboard()

# Input Karakter melalui Tombol
st.subheader("Input Karakter (A-Z)")
cols = st.columns(13)
if st.session_state.is_locked:
    for i, char in enumerate(alphabet):
        col = cols[i % 13]
        if col.button(char):
            process_character(char)

# Pesan Input dan Output
st.subheader("Pesan Input dan Output")
col1, col2 = st.columns(2)
with col1:
    st.text_area("Teks Input", value=st.session_state.input_message, height=200)
with col2:
    st.text_area("Teks Output (Terenkripsi)", value=st.session_state.output_message, height=200)
