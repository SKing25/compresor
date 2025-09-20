#!/usr/bin/env python3

import os
import wave
import heapq
import struct
import argparse
from collections import Counter
from pydub import AudioSegment


class MP3HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanMP3Compressor:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def _build_frequency_table(self, data):
        return Counter(data)

    def _build_huffman_tree(self, freq_table):
        heap = []

        for char, freq in freq_table.items():
            node = MP3HuffmanNode(char, freq)
            heapq.heappush(heap, node)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = MP3HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        return heap[0] if heap else None

    def _generate_codes(self, root):
        if not root:
            return

        def _generate_codes_helper(node, code):
            if node:
                if node.char is not None:
                    self.codes[node.char] = code if code else "0"
                    self.reverse_codes[code if code else "0"] = node.char
                    return
                _generate_codes_helper(node.left, code + "0")
                _generate_codes_helper(node.right, code + "1")

        _generate_codes_helper(root, "")

    def _apply_huffman_quantization(self, samples, quantization_bits=8):
        """
        Aplica cuantización Huffman a los samples de audio
        """
        print(f"Aplicando cuantización Huffman ({quantization_bits} bits)...")

        # Reducir rango de valores para optimizar Huffman
        max_val = 2 ** (quantization_bits - 1) - 1
        min_val = -(2 ** (quantization_bits - 1))

        quantized_samples = []
        for sample in samples:
            # Normalizar de 16 bits a N bits
            normalized = sample // (2 ** (16 - quantization_bits))
            quantized = max(min_val, min(max_val, normalized))
            quantized_samples.append(quantized)

        # Construir árbol Huffman
        freq_table = self._build_frequency_table(quantized_samples)
        root = self._build_huffman_tree(freq_table)

        self.codes = {}
        self.reverse_codes = {}
        self._generate_codes(root)

        print(f"   - Símbolos únicos: {len(self.codes)}")
        print(f"   - Rango de valores: {min_val} a {max_val}")

        return quantized_samples, quantization_bits

    def _apply_huffman_compression(self, quantized_samples, compression_factor=4):
        """
        Aplica compresión simulando el algoritmo Huffman
        """
        print(f"Aplicando compresión Huffman (factor: {compression_factor})...")

        # Submuestrear usando los códigos Huffman como guía
        # Los valores más frecuentes (códigos más cortos) se preservan mejor

        # Calcular importancia basada en frecuencia (simulando Huffman)
        freq_map = {}
        for sample in quantized_samples:
            freq_map[sample] = freq_map.get(sample, 0) + 1

        # Comprimir manteniendo samples importantes
        compressed_samples = []
        for i in range(0, len(quantized_samples), compression_factor):
            chunk = quantized_samples[i:i + compression_factor]

            if chunk:
                # Seleccionar el valor más frecuente del chunk
                best_sample = max(chunk, key=lambda x: freq_map.get(x, 0))
                compressed_samples.append(best_sample)

        print(f"   - Samples originales: {len(quantized_samples):,}")
        print(f"   - Samples comprimidos: {len(compressed_samples):,}")
        print(f"   - Reducción Huffman: {(1 - len(compressed_samples) / len(quantized_samples)) * 100:.1f}%")

        return compressed_samples

    def _restore_audio_length(self, compressed_samples, original_length, quantization_bits, compression_factor):
        """
        Restaura la longitud original del audio expandiendo los samples
        """
        print("Restaurando longitud de audio...")

        expanded_samples = []
        for sample in compressed_samples:
            # Expandir cada sample comprimido
            for _ in range(compression_factor):
                # Escalar de vuelta a 16 bits
                scaled_sample = sample * (2 ** (16 - quantization_bits))
                expanded_samples.append(int(scaled_sample))

        # Ajustar longitud exacta
        while len(expanded_samples) < original_length:
            expanded_samples.append(0)

        expanded_samples = expanded_samples[:original_length]

        print(f"   - Longitud restaurada: {len(expanded_samples):,} samples")

        return expanded_samples

    def compress_wav_to_mp3_with_huffman(self, input_file, output_file=None, bitrate="128k", quality="medium"):
        """
        Comprime WAV usando Huffman + MP3 real
        """
        if not os.path.exists(input_file):
            print(f"El archivo {input_file} no existe")
            return False

        if not input_file.lower().endswith('.wav'):
            print("❌ El archivo debe ser un WAV")
            return False

        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_huffman.mp3"

        try:
            print(f"Iniciando compresión Huffman + MP3: {input_file}")
            print("=" * 60)

            # PASO 1: Leer archivo WAV original
            print("PASO 1: Leyendo archivo WAV...")
            with wave.open(input_file, 'rb') as wav_file:
                params = wav_file.getparams()
                frames = wav_file.readframes(-1)

            if len(frames) == 0:
                print("El archivo WAV está vacío")
                return False

            print(f"Información del archivo:")
            print(f"   - Duración: {len(frames) / (params.framerate * params.nchannels * params.sampwidth):.2f}s")
            print(f"   - Canales: {params.nchannels}")
            print(f"   - Sample Rate: {params.framerate} Hz")
            print(f"   - Bits por sample: {params.sampwidth * 8}")
            print(f"   - Tamaño: {len(frames) / (1024 * 1024):.2f} MB")

            # PASO 2: Convertir a samples de 16 bits
            print("\nPASO 2: Procesando samples de audio...")
            if params.sampwidth == 2:  # 16 bits
                samples = list(struct.unpack(f'<{len(frames) // 2}h', frames))
            elif params.sampwidth == 1:  # 8 bits
                samples = [int.from_bytes([b], 'big', signed=False) - 128 for b in frames]
            else:
                print(f"❌ Formato no soportado: {params.sampwidth * 8} bits")
                return False

            print(f"   - Total samples: {len(samples):,}")

            # PASO 3: Aplicar cuantización Huffman
            print("\nPASO 3: Aplicando pre-compresión Huffman...")
            quantization_bits = 8
            quantized_samples, used_bits = self._apply_huffman_quantization(samples, quantization_bits)

            # PASO 4: Comprimir usando frecuencias Huffman
            compression_factor = 3
            compressed_samples = self._apply_huffman_compression(quantized_samples, compression_factor)

            # PASO 5: Restaurar longitud original
            print("\nPASO 4: Restaurando estructura de audio...")
            restored_samples = self._restore_audio_length(
                compressed_samples,
                len(samples),
                used_bits,
                compression_factor
            )

            # PASO 6: Convertir de vuelta a bytes
            print("\nPASO 5: Generando WAV temporal...")
            try:
                # Asegurar que los valores estén en rango válido para 16 bits
                clipped_samples = []
                for sample in restored_samples:
                    clipped = max(-32768, min(32767, sample))
                    clipped_samples.append(clipped)

                compressed_frames = struct.pack(f'<{len(clipped_samples)}h', *clipped_samples)
            except struct.error as e:
                print(f"Error en conversión de samples: {e}")
                return False

            # Crear WAV temporal con datos comprimidos por Huffman
            temp_wav = "temp_huffman_compressed.wav"
            with wave.open(temp_wav, 'wb') as wav_out:
                wav_out.setparams(params)
                wav_out.writeframes(compressed_frames)

            huffman_size = os.path.getsize(temp_wav)
            huffman_compression = (1 - huffman_size / len(frames)) * 100

            print(f"   - WAV temporal: {huffman_size / (1024 * 1024):.2f} MB")
            print(f"   - Compresión Huffman: {huffman_compression:.1f}%")

            # PASO 7: Convertir WAV comprimido a MP3 REAL
            print(f"\nPASO 6: Convirtiendo a MP3 real (bitrate: {bitrate})...")

            # Configurar parámetros de calidad MP3
            codec_params = ["-b:a", bitrate]

            if quality == "high":
                codec_params.extend(["-q:a", "0"])
            elif quality == "medium":
                codec_params.extend(["-q:a", "4"])
            elif quality == "low":
                codec_params.extend(["-q:a", "9"])

            # Cargar WAV temporal y exportar como MP3
            audio = AudioSegment.from_wav(temp_wav)
            audio.export(
                output_file,
                format="mp3",
                bitrate=bitrate,
                parameters=codec_params
            )

            # PASO 8: Limpiar archivo temporal
            os.remove(temp_wav)

            # PASO 9: Mostrar resultados finales
            print("\nRESULTADOS FINALES:")
            print("=" * 40)

            original_size = len(frames)
            final_size = os.path.getsize(output_file)
            total_compression = (1 - final_size / original_size) * 100

            print(f"Compresión Huffman + MP3 completada!")
            print(f"Archivo final: {output_file}")
            print(f"Tamaño original: {original_size / (1024 * 1024):.2f} MB")
            print(f"Tamaño final: {final_size / (1024 * 1024):.2f} MB")
            print(f"Compresión total: {total_compression:.1f}%")
            print(f"Archivo MP3 REAL - ¡Reproducible en cualquier reproductor!")

            # Verificar que el MP3 es válido
            try:
                test_audio = AudioSegment.from_mp3(output_file)
                print(f"MP3 válido - Duración: {len(test_audio) / 1000:.2f}s")
            except Exception as e:
                print(f"Advertencia al verificar MP3: {e}")

            return True

        except Exception as e:
            print(f"Error durante la compresión: {e}")
            import traceback
            traceback.print_exc()

            # Limpiar archivos temporales en caso de error
            if os.path.exists("temp_huffman_compressed.wav"):
                os.remove("temp_huffman_compressed.wav")

            return False

    def convert_mp3_to_wav(self, input_file, output_file=None):
        """
        Convierte MP3 de vuelta a WAV (funcionalidad extra)
        """
        if not os.path.exists(input_file):
            print(f"El archivo {input_file} no existe")
            return False

        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_from_mp3.wav"

        try:
            print(f"🔄 Convirtiendo MP3 a WAV: {input_file}")

            # Cargar MP3
            audio = AudioSegment.from_mp3(input_file)

            # Exportar como WAV
            audio.export(output_file, format="wav")

            print(f"Conversión MP3→WAV completada!")
            print(f"Archivo guardado como: {output_file}")

            return True

        except Exception as e:
            print(f"Error durante la conversión: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Compresor WAV a MP3 usando Huffman + pydub",
        epilog="""
Ejemplos:
  # Comprimir WAV con Huffman + MP3
  python huffman_mp3.py -c archivo.wav

  # Con bitrate y calidad específicos
  python huffman_mp3.py -c archivo.wav -b 192k -q high

  # Convertir MP3 a WAV
  python huffman_mp3.py -d archivo.mp3

  # Especificar archivo de salida
  python huffman_mp3.py -c archivo.wav -o musica_comprimida.mp3
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--compress", help="Comprimir WAV usando Huffman + MP3")
    group.add_argument("-d", "--decompress", help="Convertir MP3 a WAV")

    parser.add_argument("-o", "--output", help="Archivo de salida")
    parser.add_argument("-b", "--bitrate", default="128k",
                        help="Bitrate del MP3 (ej: 128k, 192k, 320k)")
    parser.add_argument("-q", "--quality", choices=["low", "medium", "high"],
                        default="medium", help="Calidad de compresión MP3")

    args = parser.parse_args()

    compressor = HuffmanMP3Compressor()

    print("Compresor Huffman + MP3")
    print("Combina algoritmo Huffman con MP3 real")
    print("=" * 50)

    if args.compress:
        success = compressor.compress_wav_to_mp3_with_huffman(
            args.compress,
            args.output,
            args.bitrate,
            args.quality
        )
        if success:
            print("\n¡Proceso completado exitosamente!")
        else:
            print("\n❌ El proceso falló")

    elif args.decompress:
        success = compressor.convert_mp3_to_wav(args.decompress, args.output)
        if success:
            print("\n¡Conversión completada!")
        else:
            print("\nLa conversión falló")


if __name__ == "__main__":
    main()
