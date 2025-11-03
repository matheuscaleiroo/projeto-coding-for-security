import logging
from datetime import datetime
import argparse
import random
import string

parser = argparse.ArgumentParser(description="Validador e gerador de senhas")
parser.add_argument("--modo", choices=["validar", "gerar"], required=True,
                    help="Escolha entre validar ou gerar senha")
args = parser.parse_args()

logging.basicConfig(filename="registro.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def validadorSenhas():
    validador = ["qwer", "tyui", "dfgh", "s3nh4", "123456", "123456789", "12345678",
                "password", "senha", "qwerty123", "qwerty1", "111111", "12345",
                "secret", "123123", " "]
    caracterEspecial = ["!", "@", "#", "$", "%", "¨¨", "&", "*", "(", ")"]
    numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    pontuacao = 0
    erros = []

    validador_norm = [s.strip().lower() for s in validador if s.strip()]

    senha = input("Digite sua senha:").strip()
    senha_lower = senha.lower()

    if len(senha) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres.")
    else:
        pontuacao += 1

    if any(c in caracterEspecial for c in senha):
        pontuacao += 1
    else:
        erros.append("A senha deve ter pelo menos um caracter especial.")
    
    if any(c.isupper() for c in senha):
        pontuacao +=1
    else:
        erros.append("Sua senha deve ter pelo menos uma letra maiuscula")
    
    if any(c.islower() for c in senha):
        pontuacao +=1
    else:
        erros.append("Sua senha deve ter pelo menos uma letra minuscula")
    
    if any(seq in senha_lower for seq in validador_norm):
        erros.append("Sua senha contem uma sequencia ou muito previsivel, ou que ja foi vazada")
    else:
        pontuacao +=1
    
    if any(c in numeros for c in senha):
        pontuacao +=1
    else:
        erros.append("Sua senha deve ter pelo menos um numero.")
    
    if len(senha) > 64:
        erros.append("Sua senha e muito longa, deve ter no maximo 64 caracteres.")
    else:
        pontuacao +=1
    
    if " " in senha:
        erros.append("Sua senha nao deve conter espacos")
    else:
        pontuacao +=1

    def tem_sequencia_generica(s, min_len=3):
        s_len = len(s)
        for L in range(min_len, s_len+1):
            for i in range(0, s_len - L + 1):
                sub = s[i:i+L]
                codes = [ord(c) for c in sub]
                diffs = [codes[j+1]-codes[j] for j in range(len(codes)-1)]
                if all(d == 1 for d in diffs) or all(d == -1 for d in diffs):
                    return True, sub
        return False, None

    seq_found, which = tem_sequencia_generica(senha_lower, min_len=3)
    if seq_found:
        erros.append(f"Sua senha contem uma sequencia previsivel: {which}")

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"Senha validada: {senha} - Pontuacao: {pontuacao} - Erros: {erros}")

    print("-- RESULTADO --")
    
    if pontuacao == 8 and not seq_found:
        print("Parabens sua senha esta segura")
    elif pontuacao >= 5 and pontuacao <= 7:
        print("Sua senha esta com riscos e pode ser melhorada!")
    else:
        print("Senha fraca, por favor melhorar ela para ter seguranca")

    if erros:
        for erro in erros:
            print(erro)
    else:
        print("Parabens sua senha nao contem nenhum problema")


def geradorDeSenhas():
    while True:
        try: 
            tamSenha = int(input("Qual numero da senha que voce quer?: "))
            if 8 <= tamSenha <= 64:
                break
            else:
                print("Digite um tamanho de senha entre 8 e 64.")
        except ValueError:
            print("Erro: digite um numero valido.")
    
    PALAVRAS_FRACAS = ["senha", "password", "123456", "admin", "qwerty", "secret"]
    
    letras_maiusculas = string.ascii_uppercase
    letras_minusculas = string.ascii_lowercase
    nums = string.digits
    caractEspcial = "!@#$%^&*+=-_?"

    senha = [
        random.choice(letras_maiusculas),
        random.choice(letras_minusculas),
        random.choice(nums),
        random.choice(caractEspcial)
    ]

    tudo = letras_maiusculas + letras_minusculas + nums + caractEspcial
    senha += random.choices(tudo, k=tamSenha - 4)

    random.shuffle(senha)
    senhaFinal = ''.join(senha) 

    for seq in ["1234", "abcd", "qwer", "asdf"]:
        if seq in senhaFinal.lower():
            return geradorDeSenhas()

    for palavra in PALAVRAS_FRACAS:
        if palavra in senhaFinal.lower():
            return geradorDeSenhas()

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"Senha gerada: {senhaFinal}")
    print(f"Senha gerada em {agora}: {senhaFinal}")
    return senhaFinal


if args.modo == "validar":
    validadorSenhas()
elif args.modo == "gerar":
    geradorDeSenhas()
