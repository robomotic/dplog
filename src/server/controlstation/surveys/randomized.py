import math
from .models import ClientVirtual

def simulated_run(n_clients=10):
    clients= [ClientVirtual(clientid) for clientid in range(1,n_clients+1)]

