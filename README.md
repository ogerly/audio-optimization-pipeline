# Audio Optimization Pipeline

Eine Python-basierte Pipeline zur automatischen Optimierung von Audioaufnahmen mit detaillierter Performance-Analyse. Die Pipeline führt verschiedene Audiooptimierungen durch und liefert einen ausführlichen Bericht über den Verarbeitungsprozess.

## Features

- **Audio-Formatstandardisierung**
  - Konvertierung zu Mono
  - Anpassung der Abtastrate (Sample Rate)
  - Standardisierung des Audioformats

- **Rauschunterdrückung**
  - Intelligente Erkennung und Reduzierung von Hintergrundgeräuschen
  - Anpassbare Parameter für die Rauschunterdrückung

- **Frequenzoptimierung**
  - Bandpass-Filterung für den Sprachbereich (300-3400 Hz)
  - Butterworth-Filter für sanfte Frequenzübergänge

- **Lautstärkenormalisierung**
  - EBU R128 Standard
  - Konsistente Lautstärke über alle Aufnahmen

- **Performance-Analyse**
  - Detaillierte Zeitmessung für jeden Verarbeitungsschritt
  - Speicherverbrauchsanalyse
  - Ausführlicher Verarbeitungsbericht

## Installation

1. Repository klonen:
```bash
git clone https://github.com/yourusername/audio-optimization-pipeline.git
cd audio-optimization-pipeline
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate     # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Audiodatei in das `data/sample_audio` Verzeichnis legen

2. Pipeline ausführen:
```bash
python main.py
```

3. Die optimierte Audiodatei wird im `data/test_results` Verzeichnis gespeichert

## Verarbeitungsschritte

Die Pipeline durchläuft folgende Schritte:

1. **Audioeinlesung**
   - Unterstützt WAV-Format
   - Automatische Erkennung von Mono/Stereo

2. **Formatstandardisierung**
   - Konvertierung zu Mono wenn nötig
   - Anpassung der Abtastrate auf 16kHz

3. **Rauschunterdrückung**
   - Statistische Analyse des Audiosignals
   - Intelligente Rauschfilterung

4. **Frequenzfilterung**
   - Fokussierung auf den Sprachbereich
   - Entfernung störender Frequenzen

5. **Lautstärkenormalisierung**
   - Anpassung auf -23 LUFS (EBU R128)
   - Verbesserung der Hörbarkeit

## Performance-Metriken

Die Pipeline generiert einen detaillierten Bericht mit:
- Verarbeitungszeit pro Schritt
- Speicherverbrauch
- Gesamtverarbeitungszeit
- Audio-Informationen (Länge, Kanäle, Sample Rate)

Beispiel-Output:
```
=== Performanceanalyse der Audioverarbeitung ===
Audio Information:
- Sample Rate: 44100 Hz
- Länge: 98.48 Sekunden
- Kanäle: 2 -> 1 (Mono-Konvertierung)

Verarbeitungszeiten:
- Audioeinlesung: 0.03 Sekunden
- Formatstandardisierung: 0.56 Sekunden
- Rauschunterdrückung: 1.51 Sekunden
- Frequenzfilterung: 0.03 Sekunden
- Lautstärkenormalisierung: 0.05 Sekunden
- Speichern: 0.04 Sekunden

Gesamtverarbeitungszeit: 2.22 Sekunden
```

## Projektstruktur

```
audio-optimization-pipeline/
│
├── data/
│   ├── sample_audio/        # Eingabe-Audiodateien
│   └── test_results/        # Optimierte Ausgaben
│
├── src/
│   ├── __init__.py
│   └── audio_optimizer.py   # Hauptverarbeitungsklasse
│
├── main.py                  # Ausführungsskript
├── requirements.txt         # Projektabhängigkeiten
└── README.md               # Projektdokumentation
```

## Abhängigkeiten

- soundfile
- noisereduce
- scipy
- pyloudnorm
- numpy
- psutil

## Zukünftige Erweiterungen

- [ ] Unterstützung für weitere Audioformate (MP3, OGG, etc.)
- [ ] Grafische Benutzeroberfläche
- [ ] Batch-Verarbeitung mehrerer Dateien
- [ ] Anpassbare Optimierungsparameter via Konfigurationsdatei
- [ ] Spektralanalyse und Visualisierung
- [ ] API für die Integration in andere Projekte

## Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei für Details.

## Beitragen

Beiträge sind willkommen! Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) für Details zum Prozess für Pull Requests.