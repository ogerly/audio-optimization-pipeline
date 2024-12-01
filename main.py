# main.py
from src.audio_optimizer import AudioOptimizer
import os

def main():
    # Projektverzeichnis
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Pfad zum sample_audio Verzeichnis
    audio_dir = os.path.join(project_dir, "data", "sample_audio")
    
    # Pfad für optimierte Ausgaben
    output_dir = os.path.join(project_dir, "data", "test_results")
    os.makedirs(output_dir, exist_ok=True)
    
    # WAV-Dateien im sample_audio Verzeichnis suchen
    wav_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
    
    if not wav_files:
        print(f"Keine WAV-Dateien in {audio_dir} gefunden.")
        return
    
    print(f"Gefundene WAV-Dateien: {wav_files}")
    
    # Erste WAV-Datei verwenden
    input_file = os.path.join(audio_dir, wav_files[0])
    print(f"\nVerarbeite Datei: {wav_files[0]}")
    
    # Audio-Optimizer initialisieren und ausführen
    optimizer = AudioOptimizer(input_file, output_dir)
    
    try:
        # Audio verarbeiten
        output_path = optimizer.process_audio()
        
        # Bericht generieren und ausgeben
        report = optimizer.generate_report()
        print("\n=== Performanceanalyse der Audioverarbeitung ===")
        print(f"Eingabedatei: {wav_files[0]}")
        print(f"Ausgabedatei: {os.path.basename(output_path)}\n")
        
        for step, metrics in report["Schrittweise_Analyse"].items():
            print(f"\n{step}:")
            print(f"  Dauer: {metrics['Dauer']}")
            print(f"  Speichernutzung:")
            print(f"    Vorher: {metrics['Speichernutzung']['Vorher']}")
            print(f"    Nachher: {metrics['Speichernutzung']['Nachher']}")
            print(f"    Differenz: {metrics['Speichernutzung']['Differenz']}")
        
        print(f"\nGesamtverarbeitungszeit: {report['Gesamtverarbeitungszeit']}")
        
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")

if __name__ == "__main__":
    main()