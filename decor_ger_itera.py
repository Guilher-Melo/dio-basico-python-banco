from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent


class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor_saque):
        if valor_saque > 0:
            if valor_saque < self.saldo:
                self._saldo -= valor_saque
                print(f'Valor R${valor_saque:.2f} retirado com sucesso!')
                return True
            else:
                print('Você não possui saldo suficiente para esse saque!')
                return False
        else:
            print('Valor inválido!')
            return False

    def depositar(self, valor_deposito):
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print(f'Valor R${valor_deposito:.2f} depositado com sucesso!')
        else:
            print('Insira um valor positivo')
            return False
        return True


class ContaCorrente(Conta):

    def __init__(self, cliente, numero, limite_saques=3, limite=500.00):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(cliente, numero)

    def sacar(self, valor_saque):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao['tipo']
                == Saque.__name__]
        )

        excedeu_limite = valor_saque > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print('Operação inválida! Você passou do valor limite para saque.')
        elif excedeu_saques:
            print('Número máximo de saques ultrapassado!')
        else:
            return super().sacar(valor_saque)
        return False

    def __repr__(self) -> str:
        return\
            (f'/<{self.__class__.__name__}: ("{self.agencia}", "{self.numero}"\
            ",{self.cliente.nome}")>')

    def __str__(self) -> str:
        return f"""
    Agência: {self.agencia}
    C/C: {self.numero}
    Titular: {self.cliente.nome}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime('%d-%m-%Y %H:%M:%S:%f')
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):

        for transacao in self.transacoes:
            if (tipo_transacao is None or
                    transacao['tipo'].lower() == tipo_transacao.lower()):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        lista_transacoes_dia = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao['data'], '%d-%m-%Y %H:%M:%S:%f').date()
            if data_transacao == data_atual:
                lista_transacoes_dia.append(data_atual)
        return lista_transacoes_dia


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f'''
        Agência: {conta.agencia}
        Número: {conta.numero}
        Titular: {conta.cliente.nome}
        Saldo: R$ {conta.saldo:.2f}
'''
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        LIMITE_TRANSACOES = 10
        if len(conta.historico.transacoes_do_dia()) < LIMITE_TRANSACOES:
            transacao.registrar(conta)
        else:
            print('Você excedeu o número de transições diárias!!')
            return

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        super().__init__(endereco)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.cpf}>'


def log_transacao(funcao):
    def envelope(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        data = datetime.now().strftime('%d-%m-%Y %H:%M:%S:%f')
        print(f'Data transação:{data}')
        print(f'Tipo de operação: {funcao.__name__}')
        try:
            with open(ROOT_PATH / 'log.txt', 'a', encoding='utf-8') as arquivo:
                argumentos = []
                for arg in args:
                    for kwarg in kwargs.keys():
                        argumentos.append(arg, kwarg)
                log = f'{data} Função: {funcao.__name__} com argumentos: {
                    args} e {kwargs}, retornou {resultado}\n'
                arquivo.write(log)
        except IOError as exc:
            print(exc)
        return resultado
    return envelope


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta!')
        return
    return cliente.contas[0]


def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


@log_transacao
def fazer_operacao(clientes, operacao):
    cpf = int(input('Digite apenas os números do cpf do cliente: '))
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    if operacao == 'saque':
        valor = float(
            input('Digite o valor que você deseja sacar: '))
        transacao = Saque(valor)
        fazer_operacao.__name__ = 'Saque'
    elif operacao == 'deposito':
        valor = float(
            input('Digite o valor que você deseja depositar: '))
        transacao = Deposito(valor)
        fazer_operacao.__name__ = 'Depósito'

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = int(input('Digite apenas os números do cpf do cliente: '))
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    extrato = ""

    tem_transacao = False

    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f'{transacao['data']}\n{transacao['tipo']}:\
\nR${transacao['valor']:.2f}\n\n'

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações!"

    print(extrato)
    print(f'Saldo: R$ {conta.saldo:.2f}')


@log_transacao
def criar_cliente(clientes):
    cpf = int(input('Digite apenas os números do seu cpf: '))
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print('Já existe um cliente com esses dados!')
        return

    nome = input('Digite seu nome: ')
    data_nascimento = input('Digite sua data de nascimento: ')
    endereco = input(
        'Digite seu endereco, logradouro - bairro - cidade: ')

    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    clientes.append(cliente)

    print('Cliente criado com sucesso!!')


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = int(input('Digite o cpf do seu usuário: '))
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado! Por favor se registre antes....')
        return
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com êxito!!')


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print('\n')
        print(str(conta))


def main():
    clientes = []
    contas = []
    menu = """
    Escolha uma das opções:

    [u] -> Criar usuário

    [c] -> Criar conta

    [d] -> Depositar

    [a] -> Listar contas

    [s] -> Sacar

    [e] -> Ver extrato

    [o] -> Sair

    """
    while (True):
        resposta = input(menu)
        resposta = resposta.lower()

        if resposta == 'd':
            fazer_operacao(clientes, 'deposito')

        elif resposta == 's':
            fazer_operacao(clientes, 'saque')

        elif resposta == 'e':
            exibir_extrato(clientes)

        elif resposta == 'u':
            criar_cliente(clientes)

        elif resposta == 'c':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif resposta == 'a':
            listar_contas(contas)

        elif resposta == 'o':
            break

        else:
            print('Digite um valor válido')


if __name__ == '__main__':
    main()
