class PriorityLock:
    def __init__(self):
        self.owner = None
        self.waiting = []

    def acquire(self, processo, priority_lock_enabled):
        if self.owner is None:
            self.owner = processo
            return True
        else:
            if priority_lock_enabled and processo.prioridade < self.owner.prioridade:
                self.owner.prioridade = processo.prioridade  # herança
            self.waiting.append(processo)
            return False

    def release(self):
        if self.waiting:
            self.owner = self.waiting.pop(0)
        else:
             self.owner = None