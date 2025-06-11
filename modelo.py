import datetime


class Cliente:
    '''Representa um cliente do hotel.'''

    def __init__(self, nome: str, email: str, telefone: str):
        '''
        Inicializa um novo cliente.

        Args:
            nome (str): O nome completo do cliente.
            email (str): O email de contato do cliente.
            telefone (str): O telefone de contato do cliente.
        '''
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def __str__(self):
        '''Retorna uma representação em string do cliente.'''
        return f"Cliente: {self.nome}, Email: {self.email}"


class Quarto:
    '''Representa um quarto do hotel.'''

    def __init__(self, numero: int, tipo: str, preco_diaria: float):
        '''
        Inicializa umnovo quarto.

        Args:
            numero (int): O número do quarto.
            tipo (str): O tipo do quarto (ex: "Simples", "Duplo", "Luxo").
            preco_diaria (float): O preço da diária do quarto.
        '''
        self.numero = numero
        self.tipo = tipo
        self.preco_diaria = preco_diaria
        self.disponivel = True  # Padrão, um quarto sempre começa disponível.

    def __str__(self):
        '''Retorna uma representação em string do quarto.'''
        status = "Disponível" if self.disponivel else "Ocupado"
        return (
            f"Quarto No. {self.numero} ({self.tipo}) - "
            f"R$ {self.preco_diaria:.2f}/dia - Status: {status}"
        )


class Reserva:
    '''Representa uma reserva feita por um cliente em um quarto.'''

    def __init__(
        self,
        cliente: Cliente,
        quarto: Quarto,
        data_checkin: datetime.date,
        data_checkout: datetime.date
    ):
        '''
        Inicializa uma nova reserva.

        Args:
            cliente (Cliente): O objeto Cliente que está fazendo a reserva.
            quarto (Quarto): O objeto Quarto que está sendo reservado.
            data_checkin (datetime.date): A data de entrada.
            data_checkout (datetime.date): A data de saída.
        '''
        self.cliente = cliente
        self.quarto = quarto
        self.data_checkin = data_checkin
        self.data_checkout = data_checkout
        # Validação simples para garantir que a data de checkout é
        # após o check-in
        if data_checkout <= data_checkin:
            raise ValueError(
                "A data de checkout deve ser posterior à data de check-in.")

    def __str__(self):
        '''Retorna uma representação em string da reserva.'''
        return (
            f"Reserva para {self.cliente.nome} no {self.quarto.tipo} "
            f"No. {self.quarto.numero} | "
            f"Check-in: {self.data_checkin} | "
            f"Check-out: {self.data_checkout}"
        )


class GerenciadorDeReservas:
    '''Gerencia todas as operações de quartos, clientes e reservas.'''

    def __init__(self):
        self.quartos = []
        self.clientes = []
        self.reservas = []
        self._proximo_id_reserva = 1

    def adicionar_quarto(self, quarto: Quarto):
        self.quartos.append(quarto)
        print(f"Quarto No. {quarto.numero} adicionado ao sistema.")

    def registrar_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)
        print(f"Cliente {cliente.nome} registrado no sistema.")

    def listar_quartos_disponiveis(self):
        # Por enquanto, uma lógica simples. Vamos melhorá-la depois.
        return [q for q in self.quartos if q.disponivel]

    def fazer_reserva(
        self,
        cliente: Cliente,
        numero_quarto: int,
        data_checkin: str,
        data_checkout: str
    ):
        # Encontra o quarto pelo número
        quarto_selecionado = None
        for q in self.quartos:
            if q.numero == numero_quarto:
                quarto_selecionado = q
                break

        if not quarto_selecionado:
            print(f"Erro: Quarto No. {numero_quarto} não encontrado.")
            return None

        if not quarto_selecionado.disponivel:
            print(f"Erro: Quarto No. {numero_quarto} não está disponível.")
            return None

        # Converte as strings de data para objetos date
        try:
            checkin_date = datetime.datetime.strptime(
                data_checkin, '%Y-%m-%d').date()
            checkout_date = datetime.datetime.strptime(
                data_checkout, '%Y-%m-%d').date()
        except ValueError:
            print("Formato de data inválido. Use AAAA-MM-DD.")
            return None

        # Cria a reserva
        nova_reserva = Reserva(cliente, quarto_selecionado,
                               checkin_date, checkout_date)
        self.reservas.append(nova_reserva)

        # Marca o quarto como ocupado
        quarto_selecionado.disponivel = False

        print("-" * 30)
        print("Reserva realizada com sucesso!")
        print(nova_reserva)
        print("-" * 30)
        return nova_reserva

    def cancelar_reserva(self, reserva: Reserva):
        if reserva in self.reservas:
            # Torna o quarto disponível novamente
            reserva.quarto.disponivel = True
            self.reservas.remove(reserva)
            print(f"Reserva para o quarto {reserva.quarto.numero} cancelada.")
        else:
            print("Erro: Reserva não encontrada.")

    def listar_todas_as_reservas(self):
        if not self.reservas:
            print("Nenhuma reserva ativa no momento.")
            return

        print("--- Lista de Todas as Reservas ---")
        for r in self.reservas:
            print(r)
        print("-" * 33)
