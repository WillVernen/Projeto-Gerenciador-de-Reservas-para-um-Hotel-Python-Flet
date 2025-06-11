# app_flet.py

import flet as ft
from modelo import Cliente, Quarto, GerenciadorDeReservas
import datetime

# --- CÉREBRO DA APLICAÇÃO (LÓGICA DE NEGÓCIOS) ---
gerenciador = GerenciadorDeReservas()

gerenciador.adicionar_quarto(Quarto(101, "Standard", 150.00))
gerenciador.adicionar_quarto(Quarto(102, "Luxo", 250.00))
gerenciador.adicionar_quarto(Quarto(201, "Master", 450.00))
gerenciador.adicionar_quarto(Quarto(202, "Presidencial", 650.00))
# ----------------------------------------------------


def main(page: ft.Page):
    page.title = "Sistema de Reservas de Hotel"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # ou DARK

    # --- NAVEGAÇÃO PRINCIPAL ---
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.HOTEL),
        leading_width=40,
        title=ft.Text("Hotel Fantasia - Sistema de Reservas"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                ft.icons.HOME, on_click=lambda e: mostrar_tela_principal(), tooltip="Início"),
            ft.IconButton(ft.icons.BOOKMARK_ADD, on_click=lambda e: mostrar_tela_gerenciamento(
            ), tooltip="Gerenciar Reservas")
        ],
    )

    def mostrar_tela_gerenciamento(e=None):
        page.controls.clear()

        titulo = ft.Text("Gerenciamento de Reservas Ativas",
                         size=24, weight=ft.FontWeight.BOLD)

        lista_reservas_cards = ft.Column(
            spacing=15, width=700, scroll=ft.ScrollMode.AUTO)

        # Acessa a lista de reservas do nosso gerenciador
        reservas_ativas = gerenciador.reservas

        if not reservas_ativas:
            lista_reservas_cards.controls.append(
                ft.Text("Nenhuma reserva ativa no momento.",
                        size=18, italic=True)
            )
        else:
            for reserva in reservas_ativas:
                card_reserva = ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.CALENDAR_MONTH,
                                        size=40, color=ft.colors.PURPLE_400),
                                ft.Column([
                                    ft.Text(
                                        f"Cliente: {reserva.cliente.nome}", weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        f"Quarto: Nº {reserva.quarto.numero} ({reserva.quarto.tipo})"),
                                    ft.Text(
                                        f"Check-in: {reserva.data_checkin.strftime('%d/%m/%Y')} | Check-out: {reserva.data_checkout.strftime('%d/%m/%Y')}")
                                ]),
                                ft.ElevatedButton(
                                    "Cancelar Reserva",
                                    icon=ft.icons.CANCEL,
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.RED_400,
                                    # Anexamos o objeto 'reserva' ao botão
                                    data=reserva,
                                    on_click=lambda e: cancelar_reserva_click(
                                        e.control.data)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
                lista_reservas_cards.controls.append(card_reserva)

        page.add(
            ft.Column([
                titulo,
                lista_reservas_cards
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def mostrar_tela_principal(e=None):
        page.controls.clear()  # Limpa a tela antes de desenhar

        # Título da tela
        titulo = ft.Text("Quartos Disponíveis", size=24,
                         weight=ft.FontWeight.BOLD)

        # Lista para armazenar os cards dos quartos
        lista_quartos_cards = ft.Column(
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO)

        quartos_disponiveis = gerenciador.listar_quartos_disponiveis()

        if not quartos_disponiveis:
            lista_quartos_cards.controls.append(
                ft.Text("Nenhum quarto disponível no momento.",
                        size=18, italic=True)
            )
        else:
            for quarto in quartos_disponiveis:
                card_quarto = ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.KING_BED, size=40,
                                        color=ft.colors.BLUE_GREY_500),
                                ft.Column([
                                    ft.Text(
                                        f"Quarto Nº {quarto.numero}", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Tipo: {quarto.tipo}"),
                                    ft.Text(
                                        f"R$ {quarto.preco_diaria:.2f} / dia", color=ft.colors.GREEN_700)
                                ]),
                                ft.ElevatedButton(
                                    "Reservar",
                                    icon=ft.icons.BOOKMARK_ADD,
                                    # Guardando o objeto quarto no botão
                                    data=quarto,
                                    on_click=lambda e: mostrar_formulario_reserva(
                                        e.control.data)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
                lista_quartos_cards.controls.append(card_quarto)

        page.add(titulo, lista_quartos_cards)
        page.update()

    def mostrar_formulario_reserva(quarto_selecionado):
        page.controls.clear()

        # Campos de texto para os dados do cliente e da reserva
        txt_nome = ft.TextField(label="Nome Completo", width=300)
        txt_email = ft.TextField(label="Email", width=300)
        txt_telefone = ft.TextField(label="Telefone", width=300)
        txt_checkin = ft.TextField(
            label="Data de Check-in (AAAA-MM-DD)", width=200)
        txt_checkout = ft.TextField(
            label="Data de Check-out (AAAA-MM-DD)", width=200)

        def efetuar_reserva(e):
            # 1. Cria o cliente
            cliente = Cliente(
                nome=txt_nome.value,
                email=txt_email.value,
                telefone=txt_telefone.value
            )
            # 2. Chama o método do nosso "cérebro" para fazer a reserva
            reserva = gerenciador.fazer_reserva(
                cliente,
                quarto_selecionado.numero,
                txt_checkin.value,
                txt_checkout.value
            )

            if reserva:
                # Mostra uma mensagem de sucesso
                page.snack_bar = ft.SnackBar(
                    ft.Text("Reserva realizada com sucesso!"),
                    bgcolor=ft.colors.GREEN_200
                )
                page.snack_bar.open = True
                # Volta para a tela principal
                mostrar_tela_principal()
            else:
                # Mostra uma mensagem de erro
                page.snack_bar = ft.SnackBar(
                    ft.Text(
                        "Não foi possível fazer a reserva. Verifique os dados."),
                    bgcolor=ft.colors.RED_200
                )
                page.snack_bar.open = True
                page.update()

        # Monta a tela do formulário
        page.add(
            ft.Text(
                f"Reserva para o Quarto Nº {quarto_selecionado.numero} ({quarto_selecionado.tipo})", size=24, weight=ft.FontWeight.BOLD),
            txt_nome,
            txt_email,
            txt_telefone,
            ft.Row([txt_checkin, txt_checkout]),
            ft.Row(
                [
                    ft.ElevatedButton("Confirmar Reserva", icon=ft.icons.CHECK,
                                      on_click=efetuar_reserva, bgcolor=ft.colors.GREEN_100),
                    ft.ElevatedButton(
                        "Voltar", icon=ft.icons.ARROW_BACK, on_click=mostrar_tela_principal)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()

    def cancelar_reserva_click(reserva_para_cancelar):
        # Chama o método do nosso "cérebro"
        gerenciador.cancelar_reserva(reserva_para_cancelar)

        # Dá um feedback visual para o usuário
        page.snack_bar = ft.SnackBar(
            ft.Text(
                f"Reserva para o quarto {reserva_para_cancelar.quarto.numero} foi cancelada."),
            bgcolor=ft.colors.AMBER_500
        )
        page.snack_bar.open = True

        # Redesenha a tela de gerenciamento para refletir a mudança
        mostrar_tela_gerenciamento()

    # Inicia a aplicação mostrando a tela principal
    mostrar_tela_principal()


# Inicia a aplicação Flet
ft.app(target=main)
