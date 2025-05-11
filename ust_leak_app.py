
# UST Leak Detector - Phase 1
# Upload audio file and visualize Hz (frequency) and dB (amplitude)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.fftpack import fft
import io

st.set_page_config(page_title="UST Leak Analyzer", layout="centered")
st.title("🔊 UST Leak Detector - Audio Analysis")

uploaded_file = st.file_uploader("Upload a WAV file (from your ultrasonic mic)", type="wav")

if uploaded_file is not None:
    # Read WAV file
    rate, data = wav.read(io.BytesIO(uploaded_file.read()))

    if data.ndim > 1:
        data = data[:, 0]  # take only one channel if stereo

    duration = len(data) / rate
    st.write(f"Sample Rate: {rate} Hz")
    st.write(f"Duration: {duration:.2f} seconds")

    # Display waveform
    time = np.linspace(0, duration, num=len(data))
    st.subheader("Waveform")
    fig1, ax1 = plt.subplots(figsize=(10, 3))
    ax1.plot(time, data, linewidth=0.5)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Raw Audio Waveform")
    st.pyplot(fig1)

    # Frequency analysis (FFT)
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
    ax2.set_xlim(0, 50000)  # limit to ultrasonic range
    st.pyplot(fig2)

    st.success("Audio processed and visualized. Ready to move to leak logic!")
else:
    st.info("Upload a .wav file to begin analysis.")
