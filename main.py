import Ip_grafica as Ip
letrasProposicionalesA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 'A', 'B', 'C', 'D', 'E', 'F', 'G' ,'H', 'I']

formula = "-jY-kYlY-mY-nY-oYpY-qY-rYAYBY-CYDYEYFY-GYHYI"
formula2 = Ip.Tseitin(formula, letrasProposicionalesA)
print(formula2)
formulaF = Ip.formaClausal(formula2)
print(formulaF)
