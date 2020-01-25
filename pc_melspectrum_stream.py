"""
musicinformationretrieval.com/realtime_spectrogram.py
PyAudio example: display a live log-spectrogram in the terminal.
For more examples using PyAudio:
    https://github.com/mwickert/scikit-dsp-comm/blob/master/sk_dsp_comm/pyaudio_helper.py
"""
import librosa
import numpy
import pyaudio
import time
import socket
import struct
import time

DATA_SEND_RATE = 30 #hz
IP_ADDRESS = '192.168.137.200'
#IP_ADDRESS = 'localhost'
SCREEN_WIDTH = 150

# sound global variables
CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 1000
N_FFT = 4096
ENERGY_THRESHOLD = 0.2

# Choose the frequency range
F_LO = librosa.note_to_hz('C1')
F_HI = librosa.note_to_hz('C6')
M = librosa.filters.mel(RATE, N_FFT, SCREEN_WIDTH, fmin=F_LO, fmax=F_HI)

#init
p = pyaudio.PyAudio()
lastTime = time.time()
connected = False

#callb ack with every frame of audio
def callback(in_data, frame_count, time_info, status):
    global connected
    if not connected:
        return (in_data, pyaudio.paContinue)
    
    audio_data = numpy.frombuffer(in_data, dtype=numpy.float32)
    x_fft = numpy.fft.rfft(audio_data, n=N_FFT)
    melspectrum = M.dot(abs(x_fft))
    #compress melspectrum into 2 byte floats
    bbuf = []
    bbuf.extend(float_to_bytes(float('inf')))
    for v in melspectrum:
        bbuf.extend(float_to_bytes(v))
    global lastTime
    #only send data at the DATA_SEND_RATE
    if time.time()-lastTime > 1/DATA_SEND_RATE:
        lastTime = time.time()
        try:
            s.sendall(bytes(bbuf))
        except:
            connected = False
    return (in_data, pyaudio.paContinue)

#open socket with the stre
try:
    float_to_bytes = struct.Struct('e').pack
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,   # Do record input.
                    output=False, # Do not play back output.
                    frames_per_buffer=FRAMES_PER_BUFFER,
                    stream_callback=callback)

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not connected:
            try:
                s.connect((IP_ADDRESS, 12345))
                connected = True
                print("Connected")
            except:
                print("Connect failed, trying again...")
                time.sleep(4)
                
        stream.start_stream()
        while stream.is_active() and connected:
            time.sleep(0.100)
        if not stream.is_active():
            print("Sound stream is down")
            break

        stream.stop_stream()
        print("Lost Connection, attempting reconnect...")
            
except KeyboardInterrupt:
    print("Closing")
finally:
    stream.stop_stream()
    stream.close()
    s.close()
    p.terminate()
