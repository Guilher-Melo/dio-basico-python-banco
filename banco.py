saldo = 0
depositos = []
saques = []
saque = 0
LIMITE_SAQUES = 3

menu = """
Escolha uma das três opções:

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
        if valor_deposito > 0:
            saldo += valor_deposito
            depositos.append(valor_deposito)
            print(f'Valor R${valor_deposito:.2f} depositado com sucesso!')
        else:
            print('Insira um valor positivo')

    elif resposta == 's':
        if saque < 3:
            valor_saque = float(
                input('Digite o valor que você deseja sacar: '))
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
        else:
            print('Limite de 3 saques diários excedido!')

    elif resposta == 'e':
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

    elif resposta == 'o':
        break

    else:
        print('Digite um valor válido')
