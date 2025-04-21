
import numpy as np

# Lucas-all: Funcao que gera um Array com um Kbit de dados Binarios(1024 de bits)
def KbitGeneretion (): # So precisa chamar essa funcao para gerar o array 
    Kbits = np.random.randint(0, 2, 1024)
    return Kbits

# Ryuukyz: daq vou fazer o datagrama logo q é praticamente a mesma coisa
datagramas = [KbitGeneretion() for _ in range(3)]

# Ryuukyz: Lista para salvar todos as divisoes do array principal em partes de 32bits
quadros_32bits = []

# Ryuukyz: Divisor dos datagramas pra 32 bits
for datagrama in datagramas:
    # Ryuukyz: Dividindo a lista em partes de 32 bits
    quadros = [datagrama[i*32:(i+1)*32] for i in range(32)]
    # Ryuukyz: Adcionando os datagramas a lista principal
    quadros_32bits.append(quadros)

# Ryuukyz: Função pra separar o datagrama em bit stuffing
def bit_stuffing(datagrama, flag_sequence='01111110'):
    # Ryuukyz: Convertendo a lista de inteiros
    dados = datagrama.tolist() if isinstance(datagrama, np.ndarray) else datagrama
    novos_dados = []
    contador_um = 0 

    # Ryuukyz: Bit Stuffing
    # Ryuuky: De maneira mais direta, tem um contador que conta os numeros 1, a cada 5 numeros 1, ele coloca um 0 após o quinto 1
    for bit in dados:
        novos_dados.append(bit)
        if bit == 1:
            contador_um += 1
            if contador_um == 5:
                novos_dados.append(0)
                contador_um = 0
        else:
            contador_um = 0
    
    # Ryuukyz: adcionando asa flags, ta convertendo pra inteiros
    flag_bits = [int(b) for b in flag_sequence]  
    return flag_bits + novos_dados + flag_bits

# Ryuukyz: quadros com o bit stuffing
quadros_com_stuffing = []

# Ryuukyz: aplicando o stuffing aos quadros separados
for datagrama in quadros_32bits:
    quadros_stuffing = [bit_stuffing(quadro) for quadro in datagrama]
    quadros_com_stuffing.append(quadros_stuffing)


# Lucas-all: Converte a lista de bits para string binaria
def bits_list_para_string(lista_bits):
    return ''.join(str(bit) for bit in lista_bits)


# Lucas-all: Funcao que calcula o CRC
def Calc_CRC(dado):
    if isinstance(dado, list):
        bits_quadro = bits_list_para_string(dado)
    elif isinstance(dado, str):
        bits_quadro = dado
    elif isinstance(dado, int):
        bits_quadro = bin(dado)[2:]
    else:
        raise TypeError("Tipo de dado não suportado")

    # Lucas-all: Polinomio CRC-32
    polinomio = 0x04C11DB7

    # Lucas-all: Adiciona 32 bits '0' temporarios
    bits_quadro += '0' * 32

    # Lucas-all: Converte para inteiro (base 2)
    quadro_int = int(bits_quadro, 2)

    # Lucas-all: Tamanho do polinomio
    tamanho_polinomio = 32

    # Lucas-all: Divisao binaria (XOR)
    for i in range(len(bits_quadro) - tamanho_polinomio):
        if quadro_int & (1 << (len(bits_quadro) - i - 1)):
            quadro_int ^= (polinomio << (len(bits_quadro) - i - tamanho_polinomio - 1))
    
    # Lucas-all: retorna os 32 bits
    return format(quadro_int & 0xFFFFFFFF, '032b')


# Lucas-all: Funcao que adiciona os bits de paridade nos quadros
def Add_bitsParidade(datagramas):
    resultado_final = []
    
    for i, datagrama in enumerate(datagramas): # Lucas-all: Percorre cada datagrama
        try:
            datagrama_processado = []
            
            for j, quadro in enumerate(datagrama): # Lucas-all: percorre cada quadro dentro do datagrama
                if isinstance(quadro, list) and all(b in (0,1) for b in quadro):
                    quadro_str = bits_list_para_string(quadro)
                else:
                    quadro_str = str(quadro)
                
                crc = Calc_CRC(quadro_str) # Lucas-all: Passa o quadro para calculo
                quadro_com_crc = quadro_str + crc # Lucas-all: Adiciona CRC ao quadro original
                datagrama_processado.append(quadro_com_crc) # Lucas-all: Adiciona a lista de quadros do datagrama
            
            resultado_final.append(datagrama_processado)
        
        except Exception as e:
            print(f"Erro no processamento do datagrama {i+1}: {str(e)}")
            raise
    
    return resultado_final

# Lucas-all: Variavel que recebe a funcao de adicionar os bits de paridade, recebendo os 3 datagramas com seus quadros de bits
resultado = Add_bitsParidade(quadros_com_stuffing)


def quadros_grafico(datagrama_crc):
    datagramas_quadros = []

    for i, datagrama in enumerate(datagrama_crc):
        #datagrama_in = []
        for j, quadro in enumerate(datagrama):
            tamanho = len(quadro)
            datagramas_quadros = tamanho
    return datagramas_quadros

graficos = quadros_grafico(resultado)

print(graficos)
