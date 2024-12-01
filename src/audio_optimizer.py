import soundfile as sf
import noisereduce as nr
from scipy.signal import butter, filtfilt
import pyloudnorm as pyln
import numpy as np
import time
from datetime import datetime
import os
import json

class AudioOptimizer:
    def __init__(self, input_path, output_dir="optimized_audio"):
        self.input_path = input_path
        self.output_dir = output_dir
        self.performance_metrics = {}
        self.total_start_time = None
        os.makedirs(output_dir, exist_ok=True)

    def start_timing(self, step_name):
        self.performance_metrics[step_name] = {
            'start_time': time.time(),
            'memory_before': self._get_memory_usage()
        }

    def end_timing(self, step_name):
        end_time = time.time()
        self.performance_metrics[step_name].update({
            'end_time': end_time,
            'duration': end_time - self.performance_metrics[step_name]['start_time'],
            'memory_after': self._get_memory_usage()
        })

    def _get_memory_usage(self):
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    def verify_audio(self, data, sr):
        """Überprüft die Audiodaten auf Gültigkeit"""
        if len(data) == 0:
            raise ValueError("Audiodatei enthält keine Daten")
        
        print(f"Audio Information:")
        print(f"Sample Rate: {sr} Hz")
        print(f"Länge: {len(data)} samples ({len(data)/sr:.2f} Sekunden)")
        print(f"Kanäle: {2 if len(data.shape) > 1 else 1}")
        
        return True

    def standardize_format(self, data, original_sr, target_sr=16000):
        """Standardisiert das Audioformat"""
        self.start_timing('format_standardization')
        
        # Konvertiere zu Mono wenn Stereo
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        # Resampling wenn nötig
        if original_sr != target_sr:
            from scipy.signal import resample
            samples = len(data)
            new_samples = int(samples * target_sr / original_sr)
            data = resample(data, new_samples)
        
        self.end_timing('format_standardization')
        return data, target_sr

    def reduce_noise(self, data, sr):
        """Reduziert Hintergrundgeräusche"""
        self.start_timing('noise_reduction')
        
        # Anpassung der Parameter für kurze Audiodateien
        prop_decrease = 0.75
        chunk_size = min(len(data), sr)  # Chunk-Größe auf maximal 1 Sekunde begrenzen
        
        reduced_noise = nr.reduce_noise(
            y=data,
            sr=sr,
            prop_decrease=prop_decrease,
            chunk_size=chunk_size,
            stationary=True,
            n_fft=min(2048, len(data))
        )
        
        self.end_timing('noise_reduction')
        return reduced_noise

    def apply_frequency_filter(self, data, sr, lowcut=300, highcut=3400):
        """Wendet Frequenzfilterung an"""
        self.start_timing('frequency_filtering')
        
        nyquist = 0.5 * sr
        low = lowcut / nyquist
        high = highcut / nyquist
        
        # Stelle sicher, dass die Frequenzen im gültigen Bereich liegen
        low = max(0.001, min(low, 0.99))
        high = max(low + 0.001, min(high, 0.99))
        
        b, a = butter(5, [low, high], btype='band')
        filtered_data = filtfilt(b, a, data)
        
        self.end_timing('frequency_filtering')
        return filtered_data

    def normalize_loudness(self, data, sr, target_loudness=-23.0):
        """Normalisiert die Lautstärke nach EBU R128"""
        self.start_timing('loudness_normalization')
        
        # Stelle sicher, dass die Daten float32 sind
        data = data.astype(np.float32)
        
        try:
            meter = pyln.Meter(sr)
            loudness = meter.integrated_loudness(data)
            normalized_audio = pyln.normalize.loudness(data, loudness, target_loudness)
        except Exception as e:
            print(f"Warnung bei Lautstärkenormalisierung: {e}")
            normalized_audio = data  # Behalte Originaldaten bei Fehler
        
        self.end_timing('loudness_normalization')
        return normalized_audio

    def process_audio(self):
        """Führt die gesamte Audioverarbeitung durch"""
        self.total_start_time = time.time()
        
        try:
            # Audio einlesen
            self.start_timing('audio_loading')
            data, sr = sf.read(self.input_path)
            self.end_timing('audio_loading')
            
            # Überprüfe Audio
            self.verify_audio(data, sr)
            
            # Verarbeitungsschritte
            data, sr = self.standardize_format(data, sr)
            data = self.reduce_noise(data, sr)
            data = self.apply_frequency_filter(data, sr)
            data = self.normalize_loudness(data, sr)
            
            # Ergebnis speichern
            self.start_timing('saving_result')
            output_path = os.path.join(
                self.output_dir,
                f"optimized_{os.path.basename(self.input_path)}"
            )
            sf.write(output_path, data, sr)
            self.end_timing('saving_result')
            
            # Gesamtzeit berechnen
            self.performance_metrics['total_time'] = time.time() - self.total_start_time
            
            return output_path
            
        except Exception as e:
            print(f"Fehler während der Audioverarbeitung: {str(e)}")
            raise

    def generate_report(self):
        """Generiert einen detaillierten Analysebericht"""
        report = {
            "Verarbeitungszeitpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Eingabedatei": self.input_path,
            "Gesamtverarbeitungszeit": f"{self.performance_metrics['total_time']:.2f} Sekunden",
            "Schrittweise_Analyse": {}
        }

        for step, metrics in self.performance_metrics.items():
            if step != 'total_time':
                report["Schrittweise_Analyse"][step] = {
                    "Dauer": f"{metrics['duration']:.2f} Sekunden",
                    "Speichernutzung": {
                        "Vorher": f"{metrics['memory_before']:.2f} MB",
                        "Nachher": f"{metrics['memory_after']:.2f} MB",
                        "Differenz": f"{metrics['memory_after'] - metrics['memory_before']:.2f} MB"
                    }
                }

        return report