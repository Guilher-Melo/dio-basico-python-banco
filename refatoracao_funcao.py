
def sacar(*, saque, saldo, valor_saque, saques):
    if valor_saque <= 500 and valor_saque > 0:
        if valor_saque < saldo:
            saldo -= valor_saque
            print(f'Valor R${valor_saque:.2f} retirado com sucesso!')
            saques.append(valor_saque)
            saque += 1
        else:
            print('Você não possui saldo suficiente para esse saque!')
    else:
        print('Valor inválido! Limite de 500 reais por saque')
    return saldo, saque


def depositar(saldo, valor_deposito, depositos):
    if valor_deposito > 0:
        saldo += valor_deposito
        depositos.append(valor_deposito)
        print(f'Valor R${valor_deposito:.2f} depositado com sucesso!')
    else:
        print('Insira um valor positivo')
    return saldo


def extrato(depositos, saques, saldo):
    if len(depositos) > 0 or len(saques) > 0:
        if len(depositos) > 0:
            print('Depósitos:')
            for deposito in depositos:
                print(f'R$ {deposito:.2f}')
        if len(saques) > 0:
            print('Saques:')
            for saque in saques:
                print(f'R$ {saque:.2f}')
        print(f'Saldo total: R$ {saldo:.2f}')
    else:
        print('Não foram realizadas movimentações')


def criar_usuario(cpf, nome, data_nascimento, endereco, usuarios):
    if usuarios:
        for usuario in usuarios:
            if cpf not in usuario:
                dicionario = {cpf: [nome, data_nascimento, endereco]}
                usuarios.append(dicionario)
                print('Usuário criado com sucesso')
                return dicionario
            else:
                print('Usuário já existe')
    else:
        dicionario = {cpf: [nome, data_nascimento, endereco]}
        usuarios.append(dicionario)
        print('Usuário criado com sucesso!')
        return dicionario


def criar_conta(usuario, numero_conta, usuarios, contas, agencia='0001'):
    if usuarios:
        for dicionario in usuarios:
            if usuario in dicionario:
                conta = {"cpf": usuario,
                         "numero_conta": numero_conta, "Agência": agencia}
                contas.append(conta)
                print('Conta criada com sucesso!')
                return conta
            else:
                print("Usuário não existe, crie um usuário antes")
    else:
        print("Usuário não existe, crie um usuário antes")


def listar_usuarios(usuarios):
    if len(usuarios) > 0:
        for dicionario in usuarios:
            for key, values in dicionario.items():
                print(f'{key}:')
                for value in values:
                    print(value)
            print('\n-----------')
    else:
        print('O sistema ainda não possui usuários')


def listar_contas(contas):
    if len(contas) > 0:
        for dicionario in contas:
            for key, value in dicionario.items():
                print(f'{key}: {value}')
            print('\n-----------')
    else:
        print('O sistema ainda não possui contas')


def main():
    saldo = 0
    depositos = []
    saques = []
    saques_efetuados = 0
    LIMITE_SAQUES = 3

    usuarios = []
    contas = []
    numero_conta = 1

    menu = """
    Escolha uma das opções:

    [u] -> Criar usuário

    [v] -> Listar usuários

    [c] -> Criar conta

    [a] -> Listar contas

    [d] -> Depositar

    [s] -> Sacar

    [e] -> Ver extrato

    [o] -> Sair

    """
    while (True):
        resposta = input(menu)
        resposta = resposta.lower()

        if resposta == 'd':
            valor_deposito = float(
                input('Digite o valor que você deseja depositar: '))
            saldo = depositar(saldo, valor_deposito, depositos)

        elif resposta == 's':
            if saques_efetuados < LIMITE_SAQUES:
                valor_saque = float(
                    input('Digite o valor que você deseja sacar: '))
                saldo, saques_efetuados = sacar(saque=saques_efetuados,
                                                saldo=saldo,
                                                valor_saque=valor_saque,
                                                saques=saques)
            else:
                print(f'Limite de {LIMITE_SAQUES} saques diários excedido!')

        elif resposta == 'e':
            extrato(depositos, saques, saldo=saldo)

        elif resposta == 'u':
            cpf = int(input('Digite apenas os números do seu cpf: '))
            nome = input('Digite seu nome: ')
            data_nascimento = input('Digite sua data de nascimento: ')
            endereco = input(
                'Digite seu endereco, logradouro - bairro - cidade: ')
            if type(cpf) is int:
                criar_usuario(cpf=cpf, nome=nome,
                              data_nascimento=data_nascimento,
                              endereco=endereco,
                              usuarios=usuarios)
            else:
                print('Digite apenas numeros no seu cpf')

        elif resposta == 'c':
            usuario = int(input('Digite o cpf do seu usuário: '))
            retorno_criar_conta = criar_conta(
                usuario, numero_conta, usuarios, contas)
            if retorno_criar_conta is not None:
                numero_conta = retorno_criar_conta.get('numero_conta')
                numero_conta += 1
            else:
                print('Não foi possível criar a conta')
        elif resposta == 'v':
            listar_usuarios(usuarios)

        elif resposta == 'a':
            listar_contas(contas)

        elif resposta == 'o':
            break

        else:
            print('Digite um valor válido')


if __name__ == '__main__':
    main()
