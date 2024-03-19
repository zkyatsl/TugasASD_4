
import os
os.system('cls')
from prettytable import PrettyTable

class Game:
    def __init__(self, id, judul, genre, harga, jumlah):
        self.id = id
        self.judul = judul
        self.genre = genre
        self.harga = harga
        self.jumlah = jumlah

class Node:
    def __init__(self, game):
        self.game = game
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    

    def tambah_game(self, game, pos="akhir", id_sebelum=None):
        new_node = Node(game)

        if pos == "awal":
            new_node.next = self.head
            self.head = new_node
            self.update_node_ids()
        elif pos == "akhir":
            if not self.head:
                self.head = new_node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
                new_node.game.id = current.game.id + 1
        elif pos == "antara":
            if not self.head or not self.head.next:
                print("Minimal dua node untuk menambah di antara.")
                return

            current = self.head
            while current.next and current.next.game.id != id_sebelum:
                current = current.next

            if current.next:
                new_node.next = current.next
                current.next = new_node
                self.update_node_ids()
            else:
                print(f"Game dengan ID {id_sebelum} tidak ditemukan.")
        else:
            print("Posisi tidak valid.")
        self.length += 1

    def update_node_ids(self):
        current = self.head
        id_counter = 1
        while current:
            current.game.id = id_counter
            id_counter += 1
            current = current.next

    def remove_game(self, pos=None, id_sebelum=None):
        if not self.head:
            print("Linked list kosong. Tidak ada yang dapat dihapus.")
            return False

        if pos == "awal":
            self.head = self.head.next
            self.update_node_ids()
            self.length -= 1
            return True
        elif pos == "akhir":
            current = self.head
            if not current.next:
                self.head = None
                self.length -= 1
                return True
            while current.next.next:
                current = current.next
            current.next = None
            self.length -= 1
            return True
        elif pos == "antara":
            if not self.head or not self.head.next:
                print("Minimal dua node untuk menghapus di antara.")
                return False

            if not id_sebelum:
                print("ID game tidak boleh kosong.")
                return False
            current = self.head

            if current.game.id == id_sebelum:
                self.head = self.head.next
                self.update_node_ids()
                self.length -= 1
                return True

            while current.next and current.next.game.id != id_sebelum:
                current = current.next

            if current.next:
                current.next = current.next.next
                self.update_node_ids()
                self.length -= 1
                return True
            else:
                print(f"Game dengan ID {id_sebelum} tidak ditemukan.")
                return False


    def update_stok(self, game_id, new_stock):
        current = self.head
        while current:
            if current.game.id == game_id:
                current.game.jumlah = new_stock
                return True
            current = current.next
        return False
    
    def fibonacci_search_name_partial(self, partial_name):
        if not partial_name:
            print("Kata kunci pencarian tidak boleh kosong.")
            return []

        sorted_games = self.sorting_judul()  
        n = len(sorted_games)
        fib_minus_2 = 0
        fib_minus_1 = 1
        fib = fib_minus_1 + fib_minus_2

        while fib < n:
            fib_minus_2 = fib_minus_1
            fib_minus_1 = fib
            fib = fib_minus_1 + fib_minus_2

        offset = -1
        while fib > 1:
            i = min(offset + fib_minus_2, n - 1)
            if partial_name.lower() in sorted_games[i].judul.lower():
                return self.find_all_partial_matches(sorted_games, partial_name, i)
            elif sorted_games[i].judul.lower() < partial_name.lower():
                fib = fib_minus_1
                fib_minus_1 = fib_minus_2
                fib_minus_2 = fib - fib_minus_1
                offset = i
            else:
                fib = fib_minus_2
                fib_minus_1 = fib_minus_1 - fib_minus_2
                fib_minus_2 = fib - fib_minus_1

        return []

    def find_all_partial_matches(self, sorted_games, partial_name, index):
        partial_matches = []
        current_index = index
        while current_index >= 0 and partial_name.lower() in sorted_games[current_index].judul.lower():
            partial_matches.append(sorted_games[current_index])
            current_index -= 1
        current_index = index + 1
        while current_index < len(sorted_games) and partial_name.lower() in sorted_games[current_index].judul.lower():
            partial_matches.append(sorted_games[current_index])
            current_index += 1
        return partial_matches
    
    def fibonacci_search_id(self, game_id):
        if not game_id:
            print("ID pencarian tidak boleh kosong.")
            return None

        sorted_games = self.sorting_id()  
        n = len(sorted_games)
        fib_minus_2 = 0
        fib_minus_1 = 1
        fib = fib_minus_1 + fib_minus_2

        while fib < n:
            fib_minus_2 = fib_minus_1
            fib_minus_1 = fib
            fib = fib_minus_1 + fib_minus_2

        offset = -1
        while fib > 1:
            i = min(offset + fib_minus_2, n - 1)
            if sorted_games[i].id == game_id:
                return sorted_games[i]
            elif sorted_games[i].id < game_id:
                fib = fib_minus_1
                fib_minus_1 = fib_minus_2
                fib_minus_2 = fib - fib_minus_1
                offset = i
            else:
                fib = fib_minus_2
                fib_minus_1 = fib_minus_1 - fib_minus_2
                fib_minus_2 = fib - fib_minus_1

        print(f"Tidak ada game dengan ID {game_id}.")
        return None


    def sorting_judul(self, ascending=True):
        current = self.head
        games_list = []
        while current:
            games_list.append(current.game)
            current = current.next
        sorted_games = sorted(games_list, key=lambda x: x.judul.lower(), reverse=not ascending)
        return sorted_games


    def _get_game_name_at(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current.game.judul
            count += 1
            current = current.next
        return None


    
    def sorting_id(self, ascending=True):
        current = self.head
        games_list = []
        while current:
            games_list.append(current.game)
            current = current.next
        sorted_games = sorted(games_list, key=lambda x: x.id, reverse=not ascending)
        return sorted_games

    def sorting_harga(self, ascending=True):
        current = self.head
        games_list = []
        while current:
            games_list.append(current.game)
            current = current.next
        sorted_games = sorted(games_list, key=lambda x: x.harga, reverse=not ascending)
        return sorted_games
    
    def display_table_sort(self, sorted_games):
        table = PrettyTable()
        table.field_names = ["NO", "Judul", "Genre", "Harga", "Jumlah"]
        for game in sorted_games:
            table.add_row([game.id, game.judul, game.genre, game.harga, game.jumlah])
        print(table)
    
    def display_game_at(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                table = PrettyTable()
                table.field_names = ["NO", "Judul", "Genre", "Harga", "Jumlah"]
                table.add_row([current.game.id, current.game.judul, current.game.genre, current.game.harga, current.game.jumlah])
                print(table)
                return
            count += 1
            current = current.next
        print("Game tidak ditemukan.")
    

    def display_games(self):
        current = self.head
        table = PrettyTable()
        table.field_names = ["NO", "Judul", "Genre", "Harga", "Jumlah"]
        while current:
            game = current.game
            table.add_row([game.id, game.judul, game.genre, game.harga, game.jumlah])
            current = current.next
        print(table)

# Menu Utama sekaligus sama CRUD nya
def main():
    game_store = LinkedList()
    game1 = Game(1, "The Last of Us Part II", "Action-Adventure", 630000, 10)
    game2 = Game(2, "God of War", "Action-Adventure", 729000, 5)
    game3 = Game(3, "Uncharted 4: A Thief's End", "Action-Adventure", 250000, 3)
    game4 = Game(4, "Sekiro™: Shadows Die Twice - GOTY Edition", "Action-Adventure", 891000, 7)
    game_store.tambah_game(game1)
    game_store.tambah_game(game2)
    game_store.tambah_game(game3)
    game_store.tambah_game(game4)
    print("\033[93m"+ "="*71)
    print ("\033[93m|                  SELAMAT DATANG DI MAMANK GAMESHOP                  |")
    print("\033[93m"+"="*71)
    game_store.display_games()

    while True:
        print("="*71)
        print("|                         WELCOME, ADMIN Mamanks                      |")
        print("="*71)
        print("Menu:")
        print("1. Tambah Game")
        print("2. Hapus Game")
        print("3. Update Stok Game")
        print("4. Tampilkan Semua Game")
        print("5. Urutkan Game")
        print("6. Cari Nama Game?")
        print("7. Cari ID Game?")
        print("8. Keluar? ")

        choice = input("Pilih opsi: ")

        if choice == "1":
            id = int(input("Masukkan ID Game: "))
            judul = input("Masukkan Judul Game: ")
            genre = input("Masukkan Genre Game: ")
            harga = float(input("Masukkan Harga Game: "))
            jumlah = int(input("Masukkan Stok Game: "))
            print("Pilih posisi tambahan:")
            print("1. Di Awal")
            print("2. Di Akhir")
            print("3. Di Antara")
            posisi_pilihan = input("Pilih posisi (1-3): ")
            if posisi_pilihan == '1':
                game_store.tambah_game(Game(id, judul, genre, harga, jumlah), pos="awal")
            elif posisi_pilihan == '2':
                game_store.tambah_game(Game(id, judul, genre, harga, jumlah), pos="akhir")
            elif posisi_pilihan == '3':
                id_sebelum = int(input("Masukkan ID game sebelum posisi baru: "))
                game_store.tambah_game(Game(id, judul, genre, harga, jumlah), pos="antara", id_sebelum=id_sebelum)
            else:
                print("Pilihan posisi tidak valid.")
            print("Game berhasil ditambahkan!.")

        elif choice == "2":
            print("Pilih posisi penghapusan:")
            print("1. Di Awal")
            print("2. Di Akhir")
            print("3. Di Antara")
            posisi_pilihan_hapus = input("Pilih posisi (1-3): ")
            if posisi_pilihan_hapus == '1':
                if game_store.remove_game(pos="awal"):
                    print("Game di awal berhasil dihapus.")
                else:
                    print("Game di awal tidak ditemukan atau tidak dapat dihapus.")
            elif posisi_pilihan_hapus == '2':
                if game_store.remove_game(pos="akhir"):
                    print("Game di akhir berhasil dihapus.")
                else:
                    print("Game di akhir tidak ditemukan atau tidak dapat dihapus.")
            elif posisi_pilihan_hapus == '3':
                id_sebelum = int(input("Masukkan ID game sebelum posisi yang ingin dihapus: "))
                if game_store.remove_game(pos="antara", id_sebelum=id_sebelum):
                    print(f"Game di antara berhasil dihapus.")
                else:
                    print(f"Game di antara tidak ditemukan atau tidak dapat dihapus.")
            else:
                print("Pilihan posisi tidak valid.")

        elif choice == "3":
            game_id = int(input("Masukkan ID Game yang ingin diupdate stoknya: "))
            new_stock = int(input("Masukkan Stok Baru: "))
            if game_store.update_stok(game_id, new_stock):
                print("Stok game berhasil diupdate!.")
            else:
                print("Game yang kamu cari ga ada!.")

        elif choice == "4":
            game_store.display_games()

        elif choice == "5":
            print("Pilih ketentuan pengurutan yang kamu mau: ")
            print("1. ID ")
            print("2. Harga ")
            ketentuan_urut= input("Mau diurutkan sesuai apa ? (1/2): ")

            if ketentuan_urut == "1":
                pilihan_sorting = input("Pengurutan Ascending atau Descending? (a/d): ").lower()

                if pilihan_sorting == "a":
                    sorted_games = game_store.sorting_id(ascending=True)
                    print("Game diurutkan secara ascending berdasarkan ID:")
                    game_store.display_table_sort(sorted_games)
                elif pilihan_sorting == "d":
                    sorted_games = game_store.sorting_id(ascending=False)
                    print("Game diurutkan secara descending berdasarkan ID:")
                    game_store.display_table_sort(sorted_games)
                else:
                    print("Pilihan tidak valid.")
                    
            elif ketentuan_urut == "2":
                pilihan_sorting = input("Pengurutan Ascending atau Descending? (a/d): ").lower()
                if pilihan_sorting == "a":
                    sorted_games = game_store.sorting_harga(ascending=True)
                    print("Game diurutkan secara ascending berdasarkan Harga:")
                    game_store.display_table_sort(sorted_games)
                elif pilihan_sorting == "d":
                    sorted_games = game_store.sorting_harga(ascending=False)
                    print("Game diurutkan secara descending berdasarkan Harga:")
                    game_store.display_table_sort(sorted_games)
                else:
                    print("Pilihan tidak valid.")
            else:
                print("Pilihan tidak valid.")
        elif choice == "6":
            search_key = input("Masukkan kata kunci game yang ingin dicari: ")
            partial_matches = game_store.fibonacci_search_name_partial(search_key)
            if partial_matches:
                print("Game ditemukan:")
                game_store.display_table_sort(partial_matches)
            else:
                print("Tidak ada game yang cocok dengan kata kunci tersebut.")
        
        elif choice == "7":
            game_id = int(input("Masukkan ID game yang ingin dicari: "))
            found_game = game_store.fibonacci_search_id(game_id)
            if found_game:
                print("Game ditemukan:")
                table = PrettyTable()
                table.field_names = ["NO", "Judul", "Genre", "Harga", "Jumlah"]
                table.add_row([found_game.id, found_game.judul, found_game.genre, found_game.harga, found_game.jumlah])
                print(table)
            else:
                print("Tidak ada game dengan ID tersebut.")

        elif choice == "8":
            print("Terima kasih! Balik ya!")
            break
        
        else:
            print("Opsi tidak valid. Silakan pilih opsi yang benar.")

if __name__ == "__main__":
    main()

