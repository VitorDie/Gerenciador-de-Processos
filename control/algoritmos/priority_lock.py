class PriorityLock:
    def __init__(self):
        self.owner = None
        self.waiting = []
        self.original_priorities = {}

    def acquire(self, processo, priority_lock_enabled):
        if self.owner is None:
            self.owner = processo
            self.original_priorities[processo.id] = processo.prioridade
            return True
        else:
            if priority_lock_enabled and processo.prioridade < self.owner.prioridade:
                if self.owner.id not in self.original_priorities:
                    self.original_priorities[self.owner.id] = self.owner.prioridade
                self.owner.prioridade = processo.prioridade  # herança de prioridade
            self.waiting.append(processo)
            return False

    def release(self):
        if self.owner and self.owner.id in self.original_priorities:
            self.owner.prioridade = self.original_priorities.pop(self.owner.id)

        if self.waiting:
            self.owner = self.waiting.pop(0)
            self.original_priorities[self.owner.id] = self.owner.prioridade
        else:
            self.owner = None


# class PriorityLock:
#     def __init__(self):
#         self.owner = None
#         self.waiting = []
# 
#     def acquire(self, processo, priority_lock_enabled):
#         if self.owner is None:
#             self.owner = processo
#             return True
#         else:
#             if priority_lock_enabled and processo.prioridade < self.owner.prioridade:
#                 self.owner.prioridade = processo.prioridade  # herança
#             self.waiting.append(processo)
#             return False
# 
#     def release(self):
#         if self.waiting:
#             self.owner = self.waiting.pop(0)
#         else:
#              self.owner = None