from pair import pairing, pairings

class Oracle:
    def __init__(self, public_information, users, points):
        self.points = points
        self.users = users
        self.Rs = []
        self.Qs = []
        for info in public_information:
            self.Rs.append(info[-1])
            self.Qs.append((info[0], info[1]))
        

    def __subtract(self, Rs, Ts):
        res = []
        for R, T in zip(Rs, Ts):
            res.append(R - T)
        return res
    
        
    def __calculate_j_symbol(self, current_user):
        res = 1
        for user_index in range(len(self.users)):
            if user_index == current_user:
                continue
            else:
                res *= (self.users[current_user] - self.users[user_index])
        return 1/res


    def __calculate_last_matrix_row(self):
        last_matrix_row = []
        factorial_n = factorial(n)
        for i in range(len(self.users)):
            last_matrix_row.append(self.__calculate_j_symbol(i))
        
        return last_matrix_row

    def __restore_last_point(self):
        x, y = 0, 0
        for row_element, user_point in zip(self.last_matrix_row, self.points):
            a, b = user_point
            x += row_element * a
            y += row_element * b
        return int(x), int(y)
    
    def restore_secrets(self, W):
        self.last_matrix_row = self.__calculate_last_matrix_row()
        P = self.__restore_last_point()
        return subtract(self.Rs, pairings(self.Qs, P, W))