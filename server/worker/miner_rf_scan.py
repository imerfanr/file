import numpy as np
from rtlsdr import RtlSdr

def scan_rf(freqs, bandwidth, samples):
    sdr = RtlSdr()
    sdr.sample_rate = bandwidth
    sdr.gain = 'auto'
    results = []
    for f in freqs:
        sdr.center_freq = f
        iq_samples = sdr.read_samples(samples)
        spectrum = np.abs(np.fft.fft(iq_samples))**2
        # ... تحلیل سیگنال و پیدا کردن signature خاص ماینر
        results.append({"freq": f, "power": np.max(spectrum)})
    sdr.close()
    return results