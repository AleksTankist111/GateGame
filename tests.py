#### main.py: ####

inp1 = Source()  # False
inp2 = Source()  # False
p1 = NOTGate()
inp1.add_user(p1.inputs[0])  # ==> p1.inputs[0].set(inp1)
p2 = NOTGate()
inp2.add_user(p2.inputs[0])
p3 = ANDGate()
p3.connect(p1.outputs[0])
p4 = NOTGate()
p4.connect(p3.outputs[0])
out1 = Sink()
out1.connect(p4.outputs[0])
print(out1.state)  # -->False
inp1.change()  # True
# Здесь нужно обновить флаг is_used для всех гейтов и их внутренних гейтов и их...
print(out1.state)  # -->True
inp2.change()  # True
print(out1.state)  # -->True

"""
Test case to check if recursive call prevented
"""
p5 = NOTGate()
p5.connect(p5.outputs[0])
print(p5.get())
p5.update()
print(p5.get())

