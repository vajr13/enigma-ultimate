import streamlit as st
import time

# Rotor dan reflector yang digunakan
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Fungsi untuk merotasi rotor berdasarkan offset
def rotate(rotor, offset):
    return rotor[offset:] + rotor[:offset]

# Fungsi untuk plugboard swap
def plugboard_swap(char, plugboard):
    return plugboard.get(char, char)

# Fungsi untuk mengenkripsi setiap karakter
def encrypt_character(char, rotor1, rotor2, rotor3, reflector, plugboard, rotor_pos1, rotor_pos2, rotor_pos3):
    # Plugboard swap
    char = plugboard_swap(char, plugboard)
    
    # Proses Enkripsi melalui rotor
    char = rotor1[(ord(char) - ord('A') + rotor_pos1) % 26]
    char = rotor2[(ord(char) - ord('A') + rotor_pos2) % 26]
    char = rotor3[(ord(char) - ord('A') + rotor_pos3) % 26]
    
    # Reflektor
    char = reflector[ord(char) - ord('A')]
    
    # Kembali melalui rotor
    char = chr(rotor3.index(char) + ord('A'))
    char = chr(rotor2.index(char) + ord('A'))
    char = chr(rotor1.index(char) + ord('A'))
    
    # Plugboard swap
    char = plugboard_swap(char, plugboard)
    return char

# Fungsi untuk melakukan proses enkripsi
def enigma_process(character, rotor1, rotor2, rotor3, rotor_pos1, rotor_pos2, rotor_pos3, plugboard):
    processed_message = ""
    if character.isalpha():
        processed_message += encrypt_character(character.upper(), rotor1, rotor2, rotor3, reflector, plugboard, rotor_pos1, rotor_pos2, rotor_pos3)
        rotor_pos1 += 1
        if rotor_pos1 > 26:
            rotor_pos1 = 1
            rotor_pos2 += 1
            if rotor_pos2 > 26:
                rotor_pos2 = 1
                rotor_pos3 += 1
                if rotor_pos3 > 26:
                    rotor_pos3 = 1
    return processed_message, rotor_pos1, rotor_pos2, rotor_pos3

# Streamlit UI
st.title("Simulasi Mesin Enigma dengan Input Tombol")
st.info("Masukkan karakter satu per satu melalui tombol dan lihat pergerakan rotor.")

# Setel posisi rotor menggunakan slider
st.subheader("Setel Posisi Rotor (1-26)")

col1, col2, col3 = st.columns(3)

# Mendefinisikan posisi rotor dengan session_state
if 'rotor_pos1' not in st.session_state:
    st.session_state.rotor_pos1 = 1
if 'rotor_pos2' not in st.session_state:
    st.session_state.rotor_pos2 = 2
if 'rotor_pos3' not in st.session_state:
    st.session_state.rotor_pos3 = 3

with col1:
    rotor_pos1 = st.number_input("Posisi Rotor 1", min_value=1, max_value=26, value=st.session_state.rotor_pos1, step=1, key="rotor_pos1")
with col2:
    rotor_pos2 = st.number_input("Posisi Rotor 2", min_value=1, max_value=26, value=st.session_state.rotor_pos2, step=1, key="rotor_pos2")
with col3:
    rotor_pos3 = st.number_input("Posisi Rotor 3", min_value=1, max_value=26, value=st.session_state.rotor_pos3, step=1, key="rotor_pos3")

# Update posisi rotor dalam session_state
st.session_state.rotor_pos1 = rotor_pos1
st.session_state.rotor_pos2 = rotor_pos2
st.session_state.rotor_pos3 = rotor_pos3

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

# Tampilan input tombol untuk karakter
st.subheader("Masukkan Karakter (Klik Tombol)")
message = ""

cols = st.columns(13)
for i, char in enumerate(alphabet):
    col = cols[i % 13]
    if col.button(f"{char}", key=f"button_char_{char}"):
        encrypted_char, rotor_pos1, rotor_pos2, rotor_pos3 = enigma_process(char, rotor_1, rotor_2, rotor_3, st.session_state.rotor_pos1, st.session_state.rotor_pos2, st.session_state.rotor_pos3, st.session_state.plugboard)
        message += encrypted_char
        
        # Update posisi rotor di session_state
        st.session_state.rotor_pos1 = rotor_pos1
        st.session_state.rotor_pos2 = rotor_pos2
        st.session_state.rotor_pos3 = rotor_pos3

        # Tampilkan posisi rotor yang diperbarui
        st.write(f"Posisi Rotor 1: {rotor_pos1}, Posisi Rotor 2: {rotor_pos2}, Posisi Rotor 3: {rotor_pos3}")
        time.sleep(0.1)  # Delay untuk mensimulasikan pergerakan

# Menampilkan hasil enkripsi secara dinamis
st.write(f"Pesan yang diproses: {message}")
