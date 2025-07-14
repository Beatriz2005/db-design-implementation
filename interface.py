import customtkinter
from tkinter import messagebox
import connection
from PIL import Image

#janela de cadastrar usuário
class UserWindow(customtkinter.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Cadastrar novo usuário")
        self.geometry("400x450")
        self.grid_columnconfigure(1, weight=1)
        self.configure(fg_color="#242424")

        # widgets
        labels = ["nome de usuário:", "nome completo:", "e-mail:", "senha:", "tipo de usuário:"]
        for i, label_text in enumerate(labels):
            label = customtkinter.CTkLabel(self, text=label_text)
            label.grid(row=i, column=0, padx=20, pady=(10 if i == 0 else 5), sticky="w")

        self.entry_usuario = customtkinter.CTkEntry(self, placeholder_text="ex: joao.silva")
        self.entry_usuario.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="ew")

        self.entry_nome = customtkinter.CTkEntry(self, placeholder_text="joão silva")
        self.entry_nome.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        self.entry_email = customtkinter.CTkEntry(self, placeholder_text="joao_silva@email.com")
        self.entry_email.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        self.entry_senha = customtkinter.CTkEntry(self, show="*")
        self.entry_senha.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        self.combobox_tipo_usuario = customtkinter.CTkComboBox(self, values=["USUARIO_COMUM", "ORGAO_PUBLICO"],
                                                               command=self.toggle_cpf_cnpj)
        self.combobox_tipo_usuario.grid(row=4, column=1, padx=20, pady=5, sticky="ew")
        self.combobox_tipo_usuario.set("USUARIO_COMUM")

        self.label_cpf = customtkinter.CTkLabel(self, text="cpf (só números):")
        self.entry_cpf = customtkinter.CTkEntry(self)
        self.label_cnpj = customtkinter.CTkLabel(self, text="cnpj (só números):")
        self.entry_cnpj = customtkinter.CTkEntry(self)

        self.toggle_cpf_cnpj()

        self.button_cadastrar = customtkinter.CTkButton(self, text="cadastrar", command=self.cadastrar_usuario,
                                                        fg_color="#4a4a4a", hover_color="#5c5c5c")
        self.button_cadastrar.grid(row=7, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        # aplica estilos
        for widget in self.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel):
                widget.configure(text_color="#d1d1d1")
            elif isinstance(widget, (customtkinter.CTkEntry, customtkinter.CTkComboBox)):
                widget.configure(fg_color="#333333", border_color="#555555", text_color="#d1d1d1")

    def toggle_cpf_cnpj(self):
        if self.combobox_tipo_usuario.get() == "USUARIO_COMUM":
            self.label_cnpj.grid_remove()
            self.entry_cnpj.grid_remove()
            self.label_cpf.grid(row=5, column=0, padx=20, pady=5, sticky="w")
            self.entry_cpf.grid(row=5, column=1, padx=20, pady=5, sticky="ew")
        else:
            self.label_cpf.grid_remove()
            self.entry_cpf.grid_remove()
            self.label_cnpj.grid(row=5, column=0, padx=20, pady=5, sticky="w")
            self.entry_cnpj.grid(row=5, column=1, padx=20, pady=5, sticky="ew")

    def cadastrar_usuario(self):
        p_usuario = self.entry_usuario.get()
        p_nome = self.entry_nome.get()
        p_email = self.entry_email.get()
        p_senha = self.entry_senha.get()
        p_tipo_usuario = self.combobox_tipo_usuario.get()
        p_cpf = self.entry_cpf.get() if p_tipo_usuario == 'USUARIO_COMUM' else None
        p_cnpj = self.entry_cnpj.get() if p_tipo_usuario == 'ORGAO_PUBLICO' else None

        sucesso, mensagem = connection.cadastrar_usuario_db(p_usuario, p_nome, p_email, p_senha, p_tipo_usuario, p_cpf,
                                                          p_cnpj)

        if sucesso:
            messagebox.showinfo("sucesso", mensagem)
            self.destroy()
        else:
            messagebox.showerror("erro", mensagem)

#janela de adicionar imóvel a um usuário
class PropertyWindow(customtkinter.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Adicionar novo imóvel")
        self.geometry("450x550")
        self.grid_columnconfigure(1, weight=1)
        self.configure(fg_color="#242424")

        # widgets
        self.label_loc = customtkinter.CTkLabel(self, text="dados da localização",
                                                font=customtkinter.CTkFont(weight="bold"))
        self.label_loc.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.entry_rua = customtkinter.CTkEntry(self, placeholder_text="rua")
        self.entry_rua.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.entry_numero = customtkinter.CTkEntry(self, placeholder_text="número")
        self.entry_numero.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="ew")
        self.entry_bairro = customtkinter.CTkEntry(self, placeholder_text="bairro")
        self.entry_bairro.grid(row=2, column=1, padx=(5, 20), pady=5, sticky="ew")
        self.entry_cidade = customtkinter.CTkEntry(self, placeholder_text="cidade")
        self.entry_cidade.grid(row=3, column=0, padx=(20, 5), pady=5, sticky="ew")
        self.entry_estado = customtkinter.CTkEntry(self, placeholder_text="estado (uf)", width=80)
        self.entry_estado.grid(row=3, column=1, padx=(5, 20), pady=5, sticky="w")
        self.entry_cep = customtkinter.CTkEntry(self, placeholder_text="cep (só números)")
        self.entry_cep.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        self.label_imovel = customtkinter.CTkLabel(self, text="dados do imóvel",
                                                   font=customtkinter.CTkFont(weight="bold"))
        self.label_imovel.grid(row=5, column=0, columnspan=2, pady=(20, 5))

        self.combobox_concessionaria = customtkinter.CTkComboBox(self, values=['ENEL', 'CPFL', 'LIGHT', 'ELETROBRAS'])
        self.combobox_concessionaria.grid(row=6, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.combobox_status = customtkinter.CTkComboBox(self, values=['ATIVO', 'INATIVO', 'PENDENTE'])
        self.combobox_status.grid(row=7, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.combobox_tipo = customtkinter.CTkComboBox(self, values=['RESIDENCIAL', 'COMERCIAL', 'INDUSTRIAL', 'RURAL'])
        self.combobox_tipo.grid(row=8, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        self.label_user_id = customtkinter.CTkLabel(self, text="id do usuário a ser associado:")
        self.label_user_id.grid(row=9, column=0, padx=(20, 5), pady=(20, 5), sticky="w")
        self.entry_user_id = customtkinter.CTkEntry(self)
        self.entry_user_id.grid(row=9, column=1, padx=(5, 20), pady=20, sticky="ew")

        self.button_cadastrar = customtkinter.CTkButton(self, text="adicionar imóvel", command=self.cadastrar_imovel,
                                                        fg_color="#4a4a4a", hover_color="#5c5c5c")
        self.button_cadastrar.grid(row=10, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # aplica estilos
        for widget in self.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel):
                widget.configure(text_color="#d1d1d1")
            elif isinstance(widget, (customtkinter.CTkEntry, customtkinter.CTkComboBox)):
                widget.configure(fg_color="#333333", border_color="#555555", text_color="#d1d1d1")

    def cadastrar_imovel(self):
        try:
            id_usuario = int(self.entry_user_id.get())
        except ValueError:
            messagebox.showwarning("dado inválido", "o id do usuário deve ser um número inteiro.")
            return

        sucesso, mensagem = connection.cadastrar_imovel_db(
            rua=self.entry_rua.get(), numero=self.entry_numero.get(),
            bairro=self.entry_bairro.get(), cidade=self.entry_cidade.get(),
            estado=self.entry_estado.get(), cep=self.entry_cep.get(),
            concessionaria=self.combobox_concessionaria.get(),
            status_reg=self.combobox_status.get(),
            tipo_imovel=self.combobox_tipo.get(),
            id_usuario=id_usuario
        )

        if sucesso:
            messagebox.showinfo("sucesso", mensagem)
            self.destroy()
        else:
            messagebox.showerror("erro", mensagem)

#painel do portal
class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("Portal de energia")
        self.geometry("700x500")
        self.configure(fg_color="#242424")

        # configura o grid para centralizar o frame de botões
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # carrega a imagem
        try:
            lamp_image_data = Image.open("lightbulb.png")
            lamp_image = customtkinter.CTkImage(light_image=lamp_image_data, size=(20, 20))
        except FileNotFoundError:
            print("aviso: imagem 'lightbulb.png' não encontrada.")
            lamp_image = None
        except Exception as e:
            print(f"erro ao carregar a imagem: {e}")
            lamp_image = None

        # frame para os botões
        self.frame_botoes = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=0, column=0, sticky="")  # sticky vazio centraliza

        # configuração dos botões
        botao_config = {"fg_color": "#4a4a4a", "hover_color": "#5c5c5c", "text_color": "#d1d1d1",
                        "width": 250, "height": 50, "font": customtkinter.CTkFont(size=16),
                        "image": lamp_image, "compound": "left"}

        self.button_cad_user = customtkinter.CTkButton(self.frame_botoes, text="cadastrar usuário",
                                                       command=self.open_user_window, **botao_config)
        self.button_cad_user.pack(padx=20, pady=10)

        self.button_cad_imovel = customtkinter.CTkButton(self.frame_botoes, text="adicionar imóvel",
                                                         command=self.open_property_window, **botao_config)
        self.button_cad_imovel.pack(padx=20, pady=10)

        self.button_list_imoveis = customtkinter.CTkButton(self.frame_botoes, text="ver imóveis por usuário",
                                                           command=self.listar_imoveis_por_usuario, **botao_config)
        self.button_list_imoveis.pack(padx=20, pady=10)

        self.user_window = None
        self.property_window = None

    def open_user_window(self):
        if self.user_window is None or not self.user_window.winfo_exists():
            self.user_window = UserWindow(self)
            self.user_window.grab_set()
        else:
            self.user_window.focus()

    def open_property_window(self):
        if self.property_window is None or not self.property_window.winfo_exists():
            self.property_window = PropertyWindow(self)
            self.property_window.grab_set()
        else:
            self.property_window.focus()

    def listar_imoveis_por_usuario(self):
        sucesso, linhas = connection.listar_imoveis_db()
        resultado_formatado = "\n".join(linhas)

        if not sucesso:
            messagebox.showerror("erro de listagem", resultado_formatado)
            return

        # cria uma nova janela para mostrar os resultados
        results_window = customtkinter.CTkToplevel(self)
        results_window.title("Lista de imóveis por usuário")
        results_window.geometry("600x400")
        results_window.configure(fg_color="#242424")
        results_window.grab_set()

        # adiciona uma caixa de texto na nova janela
        textbox = customtkinter.CTkTextbox(results_window, fg_color="#333333", text_color="#d1d1d1",
                                           border_color="#555555")
        textbox.pack(expand=True, fill="both", padx=10, pady=10)

        textbox.insert("0.0", resultado_formatado)
        textbox.configure(state="disabled")

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    app = App()
    app.mainloop()