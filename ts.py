from lib import abm
from rich import print

a = abm.Environment(generate_agents=(abm.Agent, 10))
b = abm.Environment(generate_agents=(abm.Agent, 15))
c = abm.Environment(generate_agents=(abm.Agent, 7))

b.add(c)
a.add(b)

print(a.size(-1))