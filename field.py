class Field:

    def __init__(self, height, width, g_type="EVKLID"):
        self.height = height
        self.width = width
        self.field_storage = []
        for j in range(height * 2):
            storage_str = []
            for i in range(width * 2):
                storage_str.append(" ")
            self.field_storage.append(storage_str)
        self.geometry_field_type = g_type
        self.full_cells_count = 0
        if height == 3:
            self.winner_chain_length = 3
        elif height <= 5:
            self.winner_chain_length = 4
        else:
            self.winner_chain_length = 5

    def right_cord_change(self, y, x):
        if self.geometry_field_type == "EVKLID":
            return self.height - 1, self.width - 1
        if self.geometry_field_type == "TORUS":
            return y, x
        if self.geometry_field_type == "KLEIN":
            return y, x
        if self.geometry_field_type == "PROJECT":
            return self.height - 1 - y, x

    def bottom_cord_change(self, y, x):
        if self.geometry_field_type == "EVKLID":
            return self.height - 1, self.width - 1
        if self.geometry_field_type == "TORUS":
            return y, x
        if self.geometry_field_type == "KLEIN":
            return y, self.width - 1 - x
        if self.geometry_field_type == "PROJECT":
            return y, self.width - 1 - x

    def rb_cord_change(self, y, x):
        y, x = self.bottom_cord_change(y, x)
        return self.right_cord_change(y, x)

    def put(self, y, x):
        if self.field_storage[y][x] != " ":
            return -1
        symbol = "x"
        if self.full_cells_count % 2 == 1:
            symbol = "o"
        self.full_cells_count += 1
        self.field_storage[y][x] = symbol
        yr, xr = self.right_cord_change(y, x)
        self.field_storage[yr][xr + self.width] = symbol
        yb, xb = self.bottom_cord_change(y, x)
        self.field_storage[yb + self.height][xb] = symbol
        yrb, xrb = self.rb_cord_change(y, x)
        self.field_storage[yrb + self.height][xrb + self.width] = symbol
        return 0

    def is_winner_chain(self):
        for i in range(2 * self.height - self.winner_chain_length + 1):
            for j in range(2 * self.width):
                is_same = True
                for k in range(self.winner_chain_length - 1):
                    if self.field_storage[i + k][j] != self.field_storage[i + k + 1][j]:
                        is_same = False
                        break
                    if self.field_storage[i + k][j] == " ":
                        is_same = False
                        break
                if is_same:
                    return True, i, j, "vert"
        for i in range(2 * self.height):
            for j in range(2 * self.width - self.winner_chain_length + 1):
                is_same = True
                for k in range(self.winner_chain_length - 1):
                    if self.field_storage[i][j + k] != self.field_storage[i][j + k + 1]:
                        is_same = False
                        break
                    if self.field_storage[i][j + k] == " ":
                        is_same = False
                        break
                if is_same:
                    return True, i, j, "horiz"
        for i in range(2 * self.height - self.winner_chain_length + 1):
            for j in range(2 * self.width - self.winner_chain_length + 1):
                is_same = True
                for k in range(self.winner_chain_length - 1):
                    if self.field_storage[i + k][j + k] != self.field_storage[i + k + 1][j + k + 1]:
                        is_same = False
                        break
                    if self.field_storage[i + k][j + k] == " ":
                        is_same = False
                        break
                if is_same:
                    return True, i, j, "main_diag"
        for i in range(self.winner_chain_length - 1, 2 * self.height):
            for j in range(2 * self.width - self.winner_chain_length + 1):
                is_same = True
                for k in range(self.winner_chain_length - 1):
                    if self.field_storage[i - k][j + k] != self.field_storage[i - k - 1][j + k + 1]:
                        is_same = False
                        break
                    if self.field_storage[i - k][j + k] == " ":
                        is_same = False
                        break
                if is_same:
                    return True, i, j, "side_diag"
        return False, 0, 0, ""

    def is_end(self):
        is_win, y, x, var = self.is_winner_chain()
        if is_win:
            return is_win, y, x, var
        elif self.width * self.height == self.full_cells_count:
            return True, -1, -1, ""
        return False, -1, -1, ""
