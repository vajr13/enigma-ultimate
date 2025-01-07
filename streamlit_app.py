import streamlit as st
import string

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

# Inisialisasi posisi rotor di session state
if "rotor_pos1" not in st.session_state:
    st.session_state.rotor_pos1 = 1
if "rotor_pos2" not in st.session_state:
    st.session_state.rotor_pos2 = 1
if "rotor_pos3" not in st.session_state:
    st.session_state.rotor_pos3 = 1
if "processed_message" not in st.session_state:
    st.session_state.processed_message = ""

# Fungsi untuk memproses satu karakter
def process_character(char):
    rotor1 = rotate(rotor_1, st.session_state.rotor_pos1 - 1)
    rotor2 = rotate(rotor_2, st.session_state.rotor_pos2 - 1)
    rotor3 = rotate(rotor_3, st.session_state.rotor_pos3 - 1)

    encrypted_char = encrypt_character(
        char, rotor1, rotor2, rotor3, reflector, {}
    )
    st.session_state.processed_message += encrypted_char

    # Pergerakan rotor
    st.session_state.rotor_pos1 += 1
    if st.session_state.rotor_pos1 > 26:
        st.session_state.rotor_pos1 = 1
        st.session_state.rotor_pos2 += 1
        if st.session_state.rotor_pos2 > 26:
            st.session_state.rotor_pos2 = 1
            st.session_state.rotor_pos3 += 1
            if st.session_state.rotor_pos3 > 26:
                st.session_state.rotor_pos3 = 1

st.title("Enigma Machine with Real-Time Rotor Movement")
st.subheader("Setel Posisi Rotor (1-26)")

# Tampilan rotor
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

# Input melalui tombol
st.subheader("Input Karakter (A-Z)")

cols = st.columns(13)
alphabet = string.ascii_uppercase

for i, char in enumerate(alphabet):
    col = cols[i % 13]
    if col.button(char):
        process_character(char)

# Reset rotor
if st.button("Reset Rotor"):
    st.session_state.rotor_pos1 = 1
    st.session_state.rotor_pos2 = 1
    st.session_state.rotor_pos3 = 1
    st.session_state.processed_message = ""

# Menampilkan pesan hasil enkripsi
st.subheader("Pesan Terenkripsi")
st.write(st.session_state.processed_message)
