menu = '''
==========================
[d] - Depositar
[s] - Sacar
[e] - Extrato
[q] - Sair
==========================
=> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)
    print()

    if opcao == "d":
        valor_deposito = float(input("Digite o valor que deseja depositar: R$"))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n"

        else:
            print("O valor informado é inválido, tente novamente!")

    elif opcao == "s":
        valor_saque = 0

        if numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")
            
        else:
            valor_saque = float(input("Digite o valor que deseja sacar: R$"))
            if valor_saque >= limite:
                print("Saque não permitido, excedeu o limite!")
            
            elif valor_saque < limite:
                
                if valor_saque < saldo:
                    print(f"Saldo restante: R${saldo-valor_saque:.2f}")
                    saldo = saldo - valor_saque
                    extrato += f"Saque: R$ {valor_saque:.2f}\n"
                    numero_saques += 1

                elif valor_saque > saldo:
                    print("Não é possível sacar, saldo insuficiente!")

            
    elif opcao == "e":
        print("\n-------------- Extrato --------------")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R${saldo:.2f}")
        print("\n-------------------------------------")

    elif opcao == "q":
        break

    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.")
