import socket
import struct
import time
from datetime import datetime
import threading

NEURONE_IP = '192.168.200.220'  # IP que aparece no visor do seu NeurOne
DATA_PORT = 50000               # Porta configurada no "Target Port" do software
JOIN_PORT = 5050                # Porta fixa para o pacote JOIN (conforme manual)
BUFFER_SIZE = 65535

class FrameType:
    MEASUREMENT_START = 1
    SAMPLES = 2
    TRIGGER = 3
    MEASUREMENT_END = 4
    JOIN = 128

class neuroOne:
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.settimeout(1.0)

        self.__connected = False
        self.__status_meansurament = False
        self.__buffer = []
        self.__lock = threading.Lock()
        self.__running = False
        self.__thread = None

        self.__num_channels = 0
        self.__sampling_rate = 0

        try:
            self.__sock.bind(('', DATA_PORT))
        except Exception as e:
            print(f"✗ Erro no Bind: {e}")
    
    def start(self):
        if not self.__running:
            self.__running = True
            self.__thread = threading.Thread(target=self.__listen_loop, daemon=True)
            self.__thread.start()

    def stop(self):
        self.__running = False
        self.__close_connection()
        if self.__thread:
            self.__thread.join()

    def __listen_loop(self):
        """ Loop executado pela thread """
        while self.__running:
            if not self.__connected:
                self.__try_connect()
                time.sleep(0.5)
                continue
            else:
                try:
                    data, addr = self.__sock.recvfrom(BUFFER_SIZE)
                    if data:
                        frame_type = data[0]
                        self.__process_pack(frame_type, data)
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Erro na recepção: {e}")
            
    def get_connection(self):
        return self.__connected

    def get_status(self):
        return self.__status_meansurament
    
    def __try_connect(self):
        while not self.__connected:
            self.__send_join_packet()
            try:
                data, addr = self.__sock.recvfrom(BUFFER_SIZE)
                if not len(data) > 0:
                    self.__connected = True
            except:
                self.__connected = False

    def __send_join_packet(self):
        """ Envia o pacote JOIN para destravar o streaming do hardware """
        join_packet = struct.pack('>B3x', FrameType.JOIN) # Tipo 128 + 3 bytes padding
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(join_packet, (NEURONE_IP, JOIN_PORT))
        except Exception as e:
            print(f"✗ Erro ao enviar JOIN: {e}")
        
    def __process_pack(self, frame_type, data):
        if frame_type == FrameType.MEASUREMENT_START:
            # Parse conforme StartPacketFieldIndex do C++
            self.__sampling_rate = struct.unpack('>I', data[4:8])[0]
            self.__num_channels = struct.unpack('>H', data[16:18])[0]
            self.__status_meansurament = True

        elif frame_type == FrameType.SAMPLES:
            if self.__num_channels == 0:
                return
            # Parse conforme SamplesPacketFieldIndex do C++
            seq_no = struct.unpack('>I', data[4:8])[0]
            sample_idx = struct.unpack('>Q', data[12:20])[0]
            num_bundles = struct.unpack('>H', data[10:12])[0]
            
            # As amostras começam no byte 28. Cada amostra tem 3 bytes (int24)
            offset = 28
            for b in range(num_bundles):
                samples = []
                for i in range(self.__num_channels):
                    sample_raw = data[offset : offset + 3]
                    val_uV = int24_to_int32(sample_raw) * 0.1 # Escala DC_MODE_SCALE (100) / 1000
                    samples.append(val_uV)
                    offset += 3

                with self.__lock:
                    self.__buffer.append(samples)
            

        elif frame_type == FrameType.MEASUREMENT_END:
            self.__status_meansurament = False
            self.__num_channels = 0
            self.__sampling_rate = 0
    
    def get_buffer(self):
        if self.__connected and self.__status_meansurament and self.__running:
            with self.__lock:
                buffer = self.__buffer.copy()
                self.__buffer = []
            return buffer

    def __close_connection(self):
        self.__sock.close()
        self.__connected = False



def int24_to_int32(data_bytes):
    """ 
    Converte 3 bytes (int24 big-endian) para int32 com sinal.
    Replica a lógica C++: (val[0]<<24 | val[1]<<16 | val[2]<<8) >> 8
    """
    # Monta o valor deslocado para a esquerda para preservar o sinal no bit 31
    combined = (data_bytes[0] << 24) | (data_bytes[1] << 16) | (data_bytes[2] << 8)
    
    # Em Python, precisamos simular o comportamento do shift aritmético de 32 bits
    if combined & 0x80000000: # Se o bit de sinal (MSB) estiver ativo
        return (combined >> 8) - (1 << 24)
    else:
        return combined >> 8


if __name__ == '__main__':
    device = neuroOne()
    device.start()

    try:
        while True:
            # Simulando o processamento dos dados coletados a cada 100ms
            data = device.get_buffer()
            if data:
                print(f"Processando {len(data)} novas amostras...")
            
            time.sleep(0.1) 
    except KeyboardInterrupt:
        device.stop()
        print("Aplicação encerrada.")