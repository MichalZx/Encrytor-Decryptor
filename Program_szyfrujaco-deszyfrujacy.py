# -*- coding: utf-8 -*-
import os
from cryptography.fernet import Fernet
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MenuWindow(Gtk.Window):
    label1 = Gtk.Label()
    label2 = Gtk.Label()
    def __init__(self):
        super().__init__(title="Szyfrowanie i deszyfrowanie plików")

        self.pliki = []
        self.key=""
        self.error_message=""
        button1 = Gtk.Button(label="Choose File")           # tu buttony widoczne
        button1.connect("clicked", self.on_file_clicked)

        button2 = Gtk.Button(label="Choose Folder")
        button2.connect("clicked", self.on_folder_clicked)

        button3 = Gtk.Button(label="Choose Key")
        button3.connect("clicked", self.on_key_clicked)

        button4 = Gtk.Button(label="Generate new Key")
        button4.connect("clicked", self.on_new_key_clicked)

        button5 = Gtk.Button(label="Encrypt files by key")
        button5.connect("clicked", self.on_encrypt_clicked)

        button6 = Gtk.Button(label="Decrypt files by key")
        button6.connect("clicked", self.on_decrypt_clicked)

        button7 = Gtk.Button(label="Clear all")
        button7.connect("clicked", self.on_clear_clicked)

        self.label1 = Gtk.Label(label="file selected: none")
        self.label2 = Gtk.Label(label="key selected: none")
        label_grid=Gtk.Label()
        self.label_info = Gtk.Label(label="Program gotowy do pracy")


        grid = Gtk.Grid()
        grid.add(button1)
        grid.attach_next_to(button2, button1, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.label1, button1,Gtk.PositionType.RIGHT,3,1)
        grid.attach(button3, 4, 0, 1, 1)
        grid.attach_next_to(button4, button3, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.label2, button4,Gtk.PositionType.LEFT,3,1)
        grid.attach_next_to(label_grid,button2,Gtk.PositionType.BOTTOM,1,1)

        grid.attach_next_to(button5,label_grid, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(button7,label_grid,Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(self.label_info,button7,Gtk.PositionType.RIGHT,3,1)

        self.add(grid)

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            filepath=dialog.get_filename()
            print("File selected: " + filepath)
            if filepath.endswith('.py') or filepath.endswith('.key'):  # wyjatek by nie zaszyfrowac samego programu
                self.error_message = "Selected file is on Black list so it cant be selected"
                self.error_show()

            else:
                self.pliki.append(filepath)
                self.label1.set_text("File selected: " + filepath)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_key = Gtk.FileFilter()
        filter_key.set_name("Key files")
        filter_key.add_pattern("*.key")
        dialog.add_filter(filter_key)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)



    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            homepath = dialog.get_filename()
            print("Selected dir: " + homepath)
            self.label1.set_text("Dir selected: " + homepath)
            for path, subdirs, files in os.walk(
                    homepath):  # wyszukuje wszystkie pliki w bierzacym folderze i pod folderze
                for name in files:
                    if name.endswith('.py') or name.endswith('.key'):  # wyjatek by nie zaszyfrowac samego programu
                        continue
                    self.pliki.append(os.path.join(path, name))
        elif response == Gtk.ResponseType.CANCEL:
            print("Anulowanie wybrania folderu")

        dialog.destroy()
    def on_new_key_clicked(self, widget):
        self.key = Fernet.generate_key()  # tworzy klucz
        with open("klucz.key", "wb") as klucz:  # zapisyuje klucz
            klucz.write(self.key)
        print("Wygenerowano nowy klucz")
        self.label2.set_text("Key selected: " + ("klucz.key".get_filename()))

    def on_key_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a key", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select key clicked")
            key_path = dialog.get_filename()
            if key_path.endswith('.key'):
                print("Key selected: " +key_path)
                self.label2.set_text("Key selected: " + key_path)
                with open(key_path, "rb") as klucz:  # zapisyuje klucz
                    self.key = klucz.read()
            else:
                self.error_message = "Wrong file has benn selected. Selected file is not a key file"
                self.error_show()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()
    def on_encrypt_clicked(self,widget):
        if len(self.pliki)>0:
            if len(self.key)>0:
                print("Encryptiong files in progres...")
                self.label_info.set_text("Encryptiong files in progres...")
                for plik in self.pliki:  # szyfrowanie
                    with open(plik, "rb") as pliczek:
                        content = pliczek.read()
                    contentZaszyfrowany = Fernet(self.key).encrypt(content)
                    with open(plik, "wb") as pliczek:
                        pliczek.write(contentZaszyfrowany)
                print("Files has been Encrypted")
                self.label_info.set_text("Files has been Encrypted")
            else:
                self.error_message = "The key has not been selected"
                self.error_show()
        else:
            self.error_message = "File list to Encrypt is empty"
            self.error_show()

    def on_decrypt_clicked(self,widget):
        if len(self.pliki)>0:
            if len(self.key) >0:
                print("Decryptiong files in progres...")
                self.label_info.set_text("Decryptiong files in progres...")
                for plik in self.pliki:  # odszyfrowanie
                    with open(plik, "rb") as pliczek:
                        content = pliczek.read()
                    contentOdszyfrowany = Fernet(self.key).decrypt(content)
                    with open(plik, "wb") as pliczek:
                        pliczek.write(contentOdszyfrowany)
                print("Files has been Decrypted")
                self.label_info.set_text("Files has been Decrypted")

            else:
                self.error_message = "The key has not been selected"
                self.error_show()
        else:
            self.error_message="File list to Decrypt is empty"
            self.error_show()

    def on_clear_clicked(self,widget):
        self.key=""
        self.error_message=""
        self.pliki.clear()
        self.label1.set_text("file selected: none")
        self.label2.set_text("key selected: none")
        self.label_info.set_text("Program wyczyszczony i gotowy do pracy")

    def error_show(self):
        print(self.error_message)
        dialog_error = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="This is an ERROR Message",
        )
        dialog_error.format_secondary_text(self.error_message)
        dialog_error.run()
        print("ERROR dialog closed")
        dialog_error.destroy()

win = MenuWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
