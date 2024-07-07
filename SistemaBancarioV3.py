from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime

class Conta():
    def __init__ (self, numero, cliente):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def novaConta(cls, cliente, numero):
        return cls(numero, cliente)

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
    
    def sacar(self, valorSaque):
        saldo = self.saldo

        if valorSaque > saldo:
            print("Não é possível sacar, saldo insuficiente!")
        
        elif valorSaque > 0:
            self._saldo -= valorSaque
            print("Saque realizado com sucesso!")
            return True
        else:
            print("O valor informado é inválido.")

        return False
        

    def depositar(self, valorDeposito):
        if valorDeposito > 0:
            self._saldo += valorDeposito
            print("Depósito realizado com sucesso!")
        else:
            print("O valor informado é inválido.")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limiteSaques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limiteSaques = limiteSaques

    def sacar(self, valorSaque):
        numeroSaques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == Saque.
             __name__]
        )

        if valorSaque > self.limite:
            print("Saque não permitido, excedeu o limite!")

        elif numeroSaques >= self.limiteSaques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valorSaque)
        
        return False
    
    def __str__(self):
        return f'''
Agência: {self.agencia}
C/C: {self.numero}
Titular: {self.cliente.nome}
'''

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionarTransacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            }
        )

class Cliente: 
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizarTransacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionarConta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, dataNascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.dataNascimento = dataNascimento

class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, Conta):
        pass

class Saque(Transacao):
    def __init__(self, valorSaque):
        self._valorSaque = valorSaque

    @property
    def valor(self):
        return self._valorSaque
    
    def registrar(self, conta):
        if conta.sacar(self.valor) == True:
            conta.historico.adicionarTransacao(self)

class Deposito(Transacao):
    def __init__(self, valorDeposito):
        self._valorDeposito = valorDeposito

    @property
    def valor(self):
        return self._valorDeposito
    
    def registrar(self, conta):
        if conta.depositar(self.valor) == True:
            conta.historico.adicionarTransacao(self)

def menu():

    menu = '''
=============== SISTEMA BANCARIO ==================
[d] - Depositar
[s] - Sacar
[e] - Extrato
[u] - Novo usuário
[c] - Nova conta
[l] - Listar contas
[q] - Sair
===================================================
=> '''
    return input(menu)

def depositar(clientes):
    cpf  = input("Digite o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: R$"))
    transacao = Deposito(valor)

    conta = recuperarContaCliente(cliente)
    if not conta:
        return
    
    cliente.realizarTransacao(conta, transacao)

def sacar(clientes):
    cpf  = input("Digite o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valorSaque = float(input("Informe o valor do saque: R$"))
    transacao = Saque(valorSaque)

    conta = recuperarContaCliente(cliente)
    if not conta:
        return
    
    cliente.realizarTransacao(conta, transacao)

def exibirExtrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    conta = recuperarContaCliente(cliente)
    if not conta:
        return
    
    print("\n================== EXTRATO ======================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            tipo_transacao = transacao["tipo"]
            valor_transacao = transacao["valor"]
            print(f"{tipo_transacao}: R$ {valor_transacao:.2f}")

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==================================================")
           
def criarCliente(clientes):
    cpf = input("Digite seu CPF (somente número): ")
    cliente = filtrarCliente(cpf, clientes)

    if cliente:
        print("Já existe um cliente com o CPF informado!")
        return
    
    nome = input("Digite o nome completo: ")
    dataNascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, n° - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf=cpf, nome=nome, dataNascimento=dataNascimento,  endereco=endereco)
    
    clientes.append(cliente)

    print("Cliente criado com sucesso!")

def filtrarCliente(cpf, clientes):
    clientesFiltrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientesFiltrados[0] if clientesFiltrados else None

def recuperarContaCliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return False
    return cliente.contas[0]

def criarConta(numeroConta, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return 
    
    conta = ContaCorrente.novaConta(cliente=cliente, numero=numeroConta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listarContas(contas):
    if contas:
        for conta in contas:
            print("----------------------------------------------------")
            print(str(conta))
    else:
        print("Não há contas associadas!") 
        
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        print()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)
                
        elif opcao == "e":
            exibirExtrato(clientes)

        elif opcao == "u":
            criarCliente(clientes)

        elif opcao == "c":
            numeroConta = len(contas) + 1
            criarConta(numeroConta, clientes, contas)

        elif opcao == "l":
            listarContas(contas)

        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.")

main()