from time import perf_counter_ns


class Contador:


    def __init__(self):
        self.mutacoes = 0
        self.crossovers = 0
        self.total_mut = 0
        self.total_cros = 0
        self.generacao_timer = 0
        self.total_generacao_timer = 0
        self.crossover_timer = 0
        self.total_crossover_timer = 0
        self.mutacao_timer = 0
        self.total_mutacao_timer = 0
        self.selecao_timer = 0
        self.total_selecao_timer = 0
        self.timer = 0
    

    def mutacao(self, n:int=1) -> None:
        self.mutacoes += n


    def crossover(self, n:int=1) -> None:
        self.crossovers += n


    def start_generation_timer(self):
        self.generacao_timer = perf_counter_ns()
    

    def end_generation_timer(self):
        self.generacao_timer = perf_counter_ns() - self.generacao_timer
    
    
    def start_timer(self):
        self.timer = perf_counter_ns()
    

    def end_timer(self):
        self.timer = perf_counter_ns() - self.timer
    
    
    def start_crossover_timer(self):
        self.crossover_timer = perf_counter_ns()
    

    def end_crossover_timer(self):
        self.crossover_timer = perf_counter_ns() - self.crossover_timer


    def start_mutacao_timer(self):
        self.mutacao_timer = perf_counter_ns()
    

    def end_mutacao_timer(self):
        self.mutacao_timer = perf_counter_ns() - self.mutacao_timer


    def start_selecao_timer(self):
        self.selecao_timer = perf_counter_ns()
    

    def end_selecao_timer(self):
        self.selecao_timer = perf_counter_ns() - self.selecao_timer


    def reset(self) -> None:
        self.total_mut += self.mutacoes
        self.total_cros += self.crossovers
        self.total_generacao_timer += self.generacao_timer
        self.total_selecao_timer += self.selecao_timer
        self.total_crossover_timer += self.crossover_timer
        self.total_mutacao_timer += self.mutacao_timer
        self.mutacoes = 0
        self.crossovers = 0
        self.generacao_timer = 0
        self.selecao_timer = 0
        self.crossover_timer = 0
        self.mutacao_timer = 0
