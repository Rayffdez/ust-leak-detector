
# UST Leak Detector - Phase 2
# Upload audio, enter tank data, visualize spectrum and estimate leak proximity

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.fftpack import fft
import io

st.set_page_config(page_title="UST Leak Analyzer", layout="centered")
st.title("🔊 UST Leak Detector - Audio + Tank Data")

# --- Tank Info Form ---
st.sidebar.header("Tank Information")
tank_length = st.sidebar.number_input("Tank Length (feet)", min_value=1.0, step=1.0)
tank_diameter = st.sidebar.number_input("Tank Diameter (feet)", min_value=1.0, step=1.0)
fuel_volume = st.sidebar.number_input("Fuel Volume in Tank (gallons)", min_value=0.0)
mic_location = st.sidebar.selectbox("Mic Placement", ["Top", "Bottom", "End", "Center"])
vacuum_level = st.sidebar.number_input("Vacuum Level (inHg)", min_value=0.0, max_value=30.0, step=0.1)
test_duration = st.sidebar.number_input("Test Duration (hours)", min_value=0.1, step=0.1)

# --- Upload Section ---
uploaded_file = st.file_uploader("Upload a WAV file (from your ultrasonic mic)", type="wav")

if uploaded_file is not None:
    rate, data = wav.read(io.BytesIO(uploaded_file.read()))

    if data.ndim > 1:
        data = data[:, 0]

    duration = len(data) / rate
    st.write(f"Sample Rate: {rate} Hz")
    st.write(f"Duration: {duration:.2f} seconds")

    time = np.linspace(0, duration, num=len(data))
    st.subheader("Waveform")
    fig1, ax1 = plt.subplots(figsize=(10, 3))
    ax1.plot(time, data, linewidth=0.5)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Raw Audio Waveform")
    st.pyplot(fig1)

    # FFT
    st.subheader("Frequency Spectrum")
    N = len(data)
    yf = fft(data)
    xf = np.linspace(0.0, rate / 2.0, N // 2)
    db = 20 * np.log10(np.abs(yf[:N // 2]) + 1e-6)

    fig2, ax2 = plt.subplots(figsize=(10, 3))
    ax2.plot(xf, db, linewidth=0.5)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Amplitude (dB)")
    ax2.set_title("Frequency Spectrum")
    ax2.set_xlim(0, 50000)
    st.pyplot(fig2)

    # Leak Estimator Logic (very simple for now)
    peak_freq = xf[np.argmax(db)]
    st.info(f"Peak Detected Frequency: {peak_freq:.2f} Hz")

    # Dummy distance logic for now (we’ll upgrade it in Phase 3)
    if peak_freq > 25000:
        leak_estimate = "Leak may be close to the mic."
    elif 20000 < peak_freq <= 25000:
        leak_estimate = "Leak may be mid-range inside the tank."
    else:
        leak_estimate = "No strong ultrasonic leak pattern detected."

    st.success(f"Leak Estimation: {leak_estimate}")
else:
    st.info("Upload a .wav file to begin analysis.")
