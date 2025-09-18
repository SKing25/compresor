#!/usr/bin/env python3
"""
Compresor de Audio WAV a MP3
Convierte archivos WAV a MP3 con diferentes niveles de compresión
"""

import os
from pydub import AudioSegment
from pydub.utils import which
import argparse


class AudioCompressor:
    def __init__(self):
        """Inicializa el compresor de audio"""
        self.check_ffmpeg()

    def check_ffmpeg(self):
        """Verifica que FFmpeg esté instalado"""
        if not which("ffmpeg"):
            print("⚠️  FFmpeg no está instalado o no está en el PATH")
            print("📥 Instala FFmpeg desde: https://ffmpeg.org/download.html")
            print("🐧 En Linux: sudo apt install ffmpeg")
            print("🍎 En macOS: brew install ffmpeg")
            print("🪟 En Windows: descargar desde el sitio oficial")

    def get_audio_info(self, file_path):
        """Obtiene información del archivo de audio"""
        try:
            audio = AudioSegment.from_wav(file_path)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            duration = len(audio) / 1000  # en segundos

            return {
                'duration': duration,
                'size_mb': size_mb,
                'channels': audio.channels,
                'sample_rate': audio.frame_rate,
                'bit_depth': audio.sample_width * 8
            }
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return None

    def compress_to_mp3(self, input_file, output_file=None, bitrate="128k", quality="medium"):
        """
        Convierte WAV a MP3 con compresión

        Args:
            input_file (str): Ruta del archivo WAV de entrada
            output_file (str): Ruta del archivo MP3 de salida (opcional)
            bitrate (str): Bitrate del MP3 ("64k", "128k", "192k", "256k", "320k")
            quality (str): Calidad de compresión ("low", "medium", "high")
        """

        # Validar archivo de entrada
        if not os.path.exists(input_file):
            print(f"❌ El archivo {input_file} no existe")
            return False

        if not input_file.lower().endswith('.wav'):
            print("❌ El archivo debe ser un WAV")
            return False

        # Generar nombre de salida si no se especifica
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_compressed.mp3"

        try:
            print(f"🔄 Cargando archivo: {input_file}")

            # Obtener información del archivo original
            original_info = self.get_audio_info(input_file)
            if original_info:
                print(f"📊 Información original:")
                print(f"   - Duración: {original_info['duration']:.2f} segundos")
                print(f"   - Tamaño: {original_info['size_mb']:.2f} MB")
                print(f"   - Canales: {original_info['channels']}")
                print(f"   - Sample Rate: {original_info['sample_rate']} Hz")
                print(f"   - Bit Depth: {original_info['bit_depth']} bits")

            # Cargar audio
            audio = AudioSegment.from_wav(input_file)

            # Configurar parámetros de calidad
            codec_params = self._get_codec_params(quality)

            print(f"🎵 Comprimiendo a MP3 con bitrate {bitrate}...")

            # Exportar a MP3
            audio.export(
                output_file,
                format="mp3",
                bitrate=bitrate,
                parameters=codec_params
            )

            # Mostrar información del archivo comprimido
            compressed_size = os.path.getsize(output_file) / (1024 * 1024)
            compression_ratio = (original_info['size_mb'] - compressed_size) / original_info['size_mb'] * 100

            print(f"✅ Compresión completada!")
            print(f"📁 Archivo guardado como: {output_file}")
            print(f"📊 Tamaño comprimido: {compressed_size:.2f} MB")
            print(f"📉 Reducción de tamaño: {compression_ratio:.1f}%")

            return True

        except Exception as e:
            print(f"❌ Error durante la compresión: {e}")
            return False

    def _get_codec_params(self, quality):
        """Obtiene parámetros del codec según la calidad"""
        quality_params = {
            "low": ["-q:a", "9"],  # Calidad baja, máxima compresión
            "medium": ["-q:a", "5"],  # Calidad media
            "high": ["-q:a", "2"]  # Calidad alta, menos compresión
        }
        return quality_params.get(quality, quality_params["medium"])

    def batch_compress(self, input_folder, output_folder=None, bitrate="128k", quality="medium"):
        """Comprime múltiples archivos WAV en una carpeta"""

        if not os.path.exists(input_folder):
            print(f"❌ La carpeta {input_folder} no existe")
            return

        if output_folder is None:
            output_folder = os.path.join(input_folder, "compressed")

        # Crear carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)

        # Buscar archivos WAV
        wav_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.wav')]

        if not wav_files:
            print("❌ No se encontraron archivos WAV en la carpeta")
            return

        print(f"📁 Procesando {len(wav_files)} archivos WAV...")

        successful = 0
        for i, wav_file in enumerate(wav_files, 1):
            input_path = os.path.join(input_folder, wav_file)
            output_name = os.path.splitext(wav_file)[0] + ".mp3"
            output_path = os.path.join(output_folder, output_name)

            print(f"\n[{i}/{len(wav_files)}] Procesando: {wav_file}")

            if self.compress_to_mp3(input_path, output_path, bitrate, quality):
                successful += 1

        print(f"\n🎉 Proceso completado: {successful}/{len(wav_files)} archivos convertidos")


def main():
    """Función principal con interfaz de línea de comandos"""

    parser = argparse.ArgumentParser(
        description="Compresor de Audio WAV a MP3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python audio_compressor.py archivo.wav
  python audio_compressor.py archivo.wav -o salida.mp3 -b 192k -q high
  python audio_compressor.py -f carpeta_wav/ -b 128k -q medium
        """
    )

    # Argumentos principales
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--input", help="Archivo WAV de entrada")
    group.add_argument("-f", "--folder", help="Carpeta con archivos WAV para procesamiento en lote")

    # Argumentos opcionales
    parser.add_argument("-o", "--output", help="Archivo de salida (solo para archivo único)")
    parser.add_argument("-b", "--bitrate", default="128k",
                        choices=["64k", "128k", "192k", "256k", "320k"],
                        help="Bitrate del MP3 (default: 128k)")
    parser.add_argument("-q", "--quality", default="medium",
                        choices=["low", "medium", "high"],
                        help="Calidad de compresión (default: medium)")

    args = parser.parse_args()

    # Crear compresor
    compressor = AudioCompressor()

    print("🎵 Compresor de Audio WAV a MP3")
    print("=" * 40)

    if args.input:
        # Procesar archivo único
        compressor.compress_to_mp3(
            args.input,
            args.output,
            args.bitrate,
            args.quality
        )
    elif args.folder:
        # Procesar carpeta
        compressor.batch_compress(
            args.folder,
            None,
            args.bitrate,
            args.quality
        )


if __name__ == "__main__":
    main()