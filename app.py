import matplotlib.pyplot as plt
import numpy as np
import random

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
'''
# Ryuuky: so pra mostrar o stuffing,
print("\n=== Quadros com Bit Stuffing ===")
for i, datagrama in enumerate(quadros_com_stuffing, 1):
    print(f"\nDatagrama {i}:")
    for j, quadro in enumerate(datagrama, 1):
        bits_str = ''.join(map(str, quadro))
        print(f"  Quadro {j}: {bits_str}")
        print(f"  Bits adicionados: {len(quadro)-32}")  # 32 é o tamanho original do quadro

# Ryuukyz: Tinha a impressao q os quadros estavam saindo iguais
print("\n=== Verificando quadros duplicados por datagrama ===")
for i, datagrama in enumerate(quadros_32bits, 1):
    quadros_unicos = set([''.join(map(str, quadro)) for quadro in datagrama])
    print(f"Datagrama {i}: {len(quadros_unicos)} quadros únicos de {len(datagrama)}")
'''
    
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


'''
# Lucas-all: Exibir resultados
print("\n\n\n============== Quadros com CRC ==============")
for i, datagrama in enumerate(resultado):
    print(f"\nDatagrama {i+1}:")
    for j, quadro in enumerate(datagrama):
        print(f"  Quadro {j+1}: {quadro[:10]}...[CRC: {quadro[-32:]}]")
'''


# Lucas-all: funcao que escolhe o mesmo quadro dos 3 datagramas e mostra o sinal digital em um grafico
def quadros_grafico(datagramas):
    # Lucas-all: Encontra o numero minimo de quadros entre todo os datagramas
    min_quadros = min(len(datagrama) for datagrama in datagramas)

    # Lucas-all: caso a qunatidade de quadros for 0 o programa e encerrado
    if min_quadros == 0:
        print("Nenhum quadro disponivel")
        return
    
    # Lucas-all: seleciona um numero aleatorio para todos os datagramas
    num_quadro = random.randint(0, min_quadros -1)
    print(f"\nSelecionando quadros no indice {num_quadro} de cada datagrama")

    # Lucas-all: Cria uma figura com subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 8))
    fig.suptitle(f"Sinais digitais dos Quadros Selecionados (Indice {num_quadro})")

    # Lucas-all: verifica se o datagrama tem quadros suficientes
    for i, datagrama in enumerate(datagramas):

        if len(datagrama) > num_quadro:
            quadro = datagrama[num_quadro]

            # Lucas-all: Converte para lista dfe bitys se necessario
            if isinstance(quadro, str):
                sinal = [int(bit) for bit in quadro]
            elif isinstance(quadro, list):
                sinal = quadro
            else:
                sinal = [int(bit) for bit in bin(quadro)[2:]]

            # Lucas-all: plota o sinal digital
            axs[i].step(range(len(sinal)), sinal, where='post')
            axs[i].set_title(f'Datagrama {i+1} - Quadro {num_quadro}')
            axs[i].set_xlabel('Bit Index')
            axs[i].set_ylabel('Valor')
            axs[i].set_yticks([0,1])
            axs[i].grid(True)
        else:
            print(f"Datagrama {i+1} nao possui quadros no indice {num_quadro}")

    plt.tight_layout()
    plt.show()
    return num_quadro

# Lucas-all: Variavel que recebe a funcao de adicionar os bits de paridade, recebendo os 3 datagramas com seus quadros de bits
resultado = Add_bitsParidade(quadros_com_stuffing)

# Lucas-all: recebe o indice sorteado dos quadros
indice_quadro = quadros_grafico(resultado)

#num_quadro = quadros_grafico(resultado)



# Ryuukyz: gera um tempo pra modulação
def gerar_tempo(num_bits, amostras_por_bit=100, taxa=1000):
    t_total = num_bits / taxa
    return np.linspace(0, t_total, num_bits * amostras_por_bit, endpoint=False)

# Ryuukyz: modulação ask
def modulacao_ask(bits, freq_portadora=1000, amostras_por_bit=100):
    t = gerar_tempo(len(bits), amostras_por_bit)
    sinal = [] # armazenar o sinal modulado

    for bit in bits:
        amp = 1 if bit == 1 else 0.2 # amplitude 1 para bit 1, 0.2 para bit 0
        t_bit = t[:amostras_por_bit] # pega o intervalo de tempo do bit atual
        portadora = amp * np.sin(2 * np.pi * freq_portadora * t_bit) # gera a portadora modulada
        sinal.extend(portadora) # sinal final   
        t = t[amostras_por_bit:]

    return np.array(sinal) # Retorna sinal como array 

# Ryuukyz: modulação QPSK
def modulacao_qpsk(bits, freq_portadora=1000, amostras_por_bit=100):
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)  # adciona padding se o numero de bits for impar

    t = gerar_tempo(len(bits) // 2, amostras_por_bit)
    sinal = [] # armazenar o sinal modulado

    # mapeando bits para fase
    # (0,0=0°; 0,1=90°; 1,1=180°; 1,0=270°)
    mapa_fase = {
        (0, 0): 0,
        (0, 1): np.pi/2,
        (1, 1): np.pi,
        (1, 0): 3*np.pi/2
    }

    for i in range(0, len(bits), 2): # processa 2 bits por vez   
        par = (bits[i], bits[i+1]) # pega os dois bits
        fase = mapa_fase.get(tuple(par), 0) # obtem fase correspondente
        t_simbolo = t[:amostras_por_bit] # pega o intervalo de tempo do simbolo atual
        portadora = np.sin(2 * np.pi * freq_portadora * t_simbolo + fase) # gera a portadora modulada   
        sinal.extend(portadora) # sinal final  
        t = t[amostras_por_bit:]

    return np.array(sinal)


# Ryuukyz: Verifica se tem quadros disponiveis
if indice_quadro is None:
    print("Erro: Nenhum quadro disponível para modulação.")
else:
    quadro_aleatorio = [resultado[i][indice_quadro] for i in range(3)]
    quadros_bin = [[int(bit) for bit in quadro] for quadro in quadro_aleatorio]

    sinais_ask = [modulacao_ask(bits) for bits in quadros_bin] # Sinais ask
    sinais_qpsk = [modulacao_qpsk(bits) for bits in quadros_bin] # Sinais qpsk

# So pra  mostrar os primeiros valores de cada sinal modulado
    print("\n======= Sinais Modulados (ASK e QPSK) =======")
    for i in range(3):
        print(f"\nDatagrama {i+1} - Quadro {indice_quadro+1}")
        print("  ASK: ", sinais_ask[i][:10])
        print("  QPSK:", sinais_qpsk[i][:10])



# Lucas-all: processa os quadros especificos dos 3 datagramas (FDM)
def generate_fdm_from_datagrams(datagramas, indice_quadro, frequencias=[5, 10, 15]):
    """
    Retorna:
    (sinal_fdm, componentes, quadros_selecionados)
    """
    # Lucas-all: Validacao
    if len(datagramas) != 3:
        raise ValueError("Deve fornecer exatamente 3 datagramas")
    
    # Lucas-all: Seleciona os quadros no índice especificado
    quadros_selecionados = []
    for i, datagrama in enumerate(datagramas):
        if indice_quadro >= len(datagrama):
            raise IndexError(f"Datagrama {i+1} não tem quadro no índice {indice_quadro}")
        
        quadro = datagrama[indice_quadro]
        # Lucas-all: Remove CRC (últimos 32 bits) para modulação
        dados_sem_crc = quadro[:-32]  
        quadros_selecionados.append(dados_sem_crc)
    
    # Lucas-all: Configuração do FDM
    max_len = max(len(q) for q in quadros_selecionados)
    t = np.linspace(0, 1, max_len)  # Lucas-all: Tempo normalizado
    
    # Lucas-all: Modulação
    componentes = []
    for i, (quadro, freq) in enumerate(zip(quadros_selecionados, frequencias)):
        # Lucas-all: Converte string binária para array de floats
        sinal = np.array([float(bit) for bit in quadro])
        portadora = np.sin(2 * np.pi * freq * t)
        
        # Lucas-all: Modulação ASK
        sinal_modulado = sinal * portadora[:len(sinal)]
        sinal_modulado = np.pad(sinal_modulado, (0, max_len - len(sinal)))
        componentes.append(sinal_modulado)
    
    # Lucas-all: Combina os sinais
    fdm_signal = np.sum(componentes, axis=0)
    
    return fdm_signal, componentes, quadros_selecionados


frequencias = [5, 10, 15]
try:
    # Lucas-all: Gera o FDM
    fdm_sinal, componentes, quadros_sel = generate_fdm_from_datagrams(
        datagramas=resultado,
        indice_quadro=indice_quadro
    )
    
    # Lucas-all: Visualização
    plt.figure(figsize=(15, 10))
    
    # Lucas-all: Plot dos quadros originais
    for i, quadro in enumerate(quadros_sel, 1):
        plt.subplot(3, 2, 2*i-1)
        plt.step(range(len(quadro)), [int(b) for b in quadro], where='post')
        plt.title(f'Quadro {i} (Dados sem CRC)')
        plt.grid(True)
    
    # Lucas-all: Plot dos componentes FDM
    for i, comp in enumerate(componentes, 1):
        plt.subplot(3, 2, 2*i)
        plt.plot(comp)
        plt.title(f'Componente {i} @ {frequencias[i-1]}Hz')
        plt.grid(True)
    
    plt.tight_layout()
    
    # Lucas-all: Plot do sinal combinado
    plt.figure(figsize=(12, 4))
    plt.plot(fdm_sinal, 'purple', linewidth=1.5)
    plt.title('Sinal FDM Combinado')
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"Erro: {e}")


# Lucas-all: funcao que gera ruido no canal
def adicionar_ruido_numpy(dados_binarios, probabilidade=0.01):
    # Lucas-all: Converte para array numpy
    if isinstance(dados_binarios, str):
        arr = np.array([int(bit) for bit in dados_binarios])
    else:
        arr = np.array(dados_binarios)
    
    # Lucas-all: Gera máscara de ruído
    mascara_ruido = np.random.random(arr.shape) < probabilidade
    
    # Lucas-all: Aplica flip nos bits selecionados
    arr[mascara_ruido] = 1 - arr[mascara_ruido]
    
    # Lucas-all: Retorna no formato original
    if isinstance(dados_binarios, str):
        return ''.join(arr.astype(str))
    else:
        return arr.tolist()
    


# Lucas-all: Simula ruído no sinal FDM transmitido
prob_ruido = 0.005 
fdm_com_ruido = adicionar_ruido_numpy(fdm_sinal, prob_ruido/10)  # Lucas-all: Menos ruído no canal


def demodular_fdm(sinal_fdm, frequencias=[5, 10, 15], duracao=1.0, taxa_amostragem=1000):

    t = np.linspace(0, duracao, len(sinal_fdm))
    quadros_demodulados = []
    
    for freq in frequencias:
        # 1. Gera a portadora de demodulação
        portadora = np.sin(2 * np.pi * freq * t)
        
        # 2. Multiplica pelo sinal FDM (mistura)
        sinal_demod = sinal_fdm * portadora
        
        # 3. Filtro passa-baixa (simplificado)
        sinal_filtrado = np.convolve(sinal_demod, np.ones(10)/10, mode='same')
        
        # 4. Decodificação dos bits
        bits = []
        limiar = 0.5  # Limiar de decisão
        for i in range(0, len(sinal_filtrado), len(sinal_filtrado)//32):  # 32 bits por quadro
            media = np.mean(sinal_filtrado[i:i+len(sinal_filtrado)//32])
            bits.append('1' if media > limiar else '0')
        
        quadros_demodulados.append(''.join(bits))
    
    return quadros_demodulados



def remover_stuffing(quadro, flag='01111110'):
    """Remove bit stuffing e flags"""
    flag_bits = len(flag)
    # Remove flags do início e fim
    dados = quadro[flag_bits:-flag_bits]
    
    # Remove bits 0 inseridos após 5 '1's consecutivos
    bits_limpos = []
    contador_um = 0
    
    for bit in dados:
        bits_limpos.append(bit)
        if bit == '1':
            contador_um += 1
            if contador_um == 5:
                contador_um = 0
                # Pula o próximo bit (0 inserido)
                next_bit = True
        else:
            contador_um = 0
    
    return ''.join(bits_limpos)


# Lucas-all: Demodulacao FDM
quadros_recebidos = demodular_fdm(
    sinal_fdm=fdm_com_ruido,
    frequencias=frequencias,
    duracao=1.0,
    taxa_amostragem=1000
)

# Lucas-all: Processamento dos quadros recebidos
for i, quadro_rx in enumerate(quadros_recebidos):
    # Remove stuffing
    quadro_sem_stuffing = remover_stuffing(quadro_rx)
    
    # Separa dados e CRC
    dados_recebidos = quadro_sem_stuffing[:-32]
    crc_recebido = quadro_sem_stuffing[-32:]
    
    # Calcula CRC localmente
    crc_calculado = Calc_CRC(dados_recebidos)
    
    # Verifica integridade
    if crc_recebido == crc_calculado:
        print(f"Quadro {i+1} recebido corretamente! CRC válido.")
        print(f"Dados: {dados_recebidos[:20]}...")
    else:
        print(f"ERRO no Quadro {i+1}! CRC não corresponde.")
        print(f"Dados corrompidos: {dados_recebidos[:20]}...")



# Visualização dos resultados
plt.figure(figsize=(15, 10))

# Quadros originais (antes do FDM)
for i, quadro in enumerate(quadros_sel, 1):
    plt.subplot(3, 3, i)
    plt.step(range(len(quadro)), [int(b) for b in quadro], where='post')
    plt.title(f'Quadro {i} Original')

# Quadros recebidos (após demodulação)
for i, quadro in enumerate(quadros_recebidos, 4):
    plt.subplot(3, 3, i)
    plt.step(range(len(quadro)), [int(b) for b in quadro], where='post')
    plt.title(f'Quadro {i-3} Recebido')

plt.tight_layout()
plt.show()