from modelo import Cliente, Quarto, GerenciadorDeReservas

# 1. Inicializar o sistema
gerenciador = GerenciadorDeReservas()

# 2. adicionar quartos ao hotel
gerenciador.adicionar_quarto(Quarto(101, "Standard", 150.00))
gerenciador.adicionar_quarto(Quarto(102, "Luxo", 250.00))
gerenciador.adicionar_quarto(Quarto(103, "Master", 450.00))
print("\n")

# 3. Registrar um cliente
cliente1 = Cliente("Will Vernen", "willvernen@gmail.com", "85996972130")
gerenciador.registrar_cliente(cliente1)
print("\n")

# 4. Listar quartos disponíveis
print("--- Quartos Disponíveis ---")
for quarto in gerenciador.listar_quartos_disponiveis():
    print(quarto)
print("--------------------------\n")

# 5. Fazer uma reserva
reserva1 = gerenciador.fazer_reserva(cliente1, 102, "2025-07-10", "2025-07-15")
print("\n")

# 6. Tentar reservar o mesmo quarto novamente
gerenciador.fazer_reserva(cliente1, 102, "2025-08-01", "2025-08-05")
print("\n")

# 7. Listar quartos disponíveis novamente (o 102 deve estar ocupado)
print("--- Quartos Disponíveis Após Reserva ---")
for quarto in gerenciador.listar_quartos_disponiveis():
    print(quarto)
print("--------------------------------------\n")

# 8. Listar todas as reservas ativas
gerenciador.listar_todas_as_reservas()
print("\n")

# 9. Cancelar a reserva
if reserva1:
    gerenciador.cancelar_reserva(reserva1)

# 10. Listar quartos novamente para ver o 102 disponível
print("\n--- Quartos Disponíveis Após Cancelamento ---")
for quarto in gerenciador.listar_quartos_disponiveis():
    print(quarto)
print("-------------------------------------------\n")
