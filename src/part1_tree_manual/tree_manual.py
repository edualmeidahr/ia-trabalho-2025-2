import sys 

# Estrutura de dados para represetnar a Árvore de decisão 
# Formato de dicionário
# 'ID': ("Pergunta", "ID_Se_Sim", "ID_Se_Não")
# Se o nó for folha, o segundo e terceiro elementos serão None

decision_tree = {
    #Nível 1: A grande Divisão (Software vs Outros)
    'q1': ("Você gosta de passar a maior parte do seu tempo escrevendo código?", 'q2', 'q3'),
    
    # Nível 2
    #Ramo A: Gosta de Codar
    'q2': ("Você prefere ver um resultado visual imediato (telas, interfaces)?", 'q4', 'q5'),
    #Ramo B: Não gosta de Codar
    'q3': ("Você gosta de colocar a mão na massa com hardware e circuitos?", 'q10', 'q6'),
    
    #Nível 3
    #Ramo Visual
    'q4': ("Você se precupa muito com estética, cores e a psicologia do usuário?", 'res_ux_ui', 'q7'),
    #Ramo Lógico/Backend
    'q5': ("Você gosta de matemática pesada, estatísticas e probabilidade?", 'q8', 'q9'),
    #Ramo Hardware
    'q10': ("Você tem interesse específico em movimentação mecânica e robôs?", 'res_robotica', 'res_embarcados'),
    #Ramo Gestão/Infra
    'q6': ("Você gosta de liderar pessoas e organizar o trabalho dos outros?", 'q11', 'q12'),
    
    #Nível 4
    # Ramo Frontend/mobile
    'q7': ("Você prefere focar em lógica de funcionamento de interface (React/Angular) ao invés de visual?", 'res_front_eng', 'res_mobile'),
    # Ramo IA/Data Science
    'q8': ("Seu interesse é mais em pesquisa acadêmica e criar novos modelos?", 'res_ia_research', 'res_data_eng'),
    # Ramo Backend 
    'q9': ("Você gosta de encontrar brechas de segurança e 'hackear' sistemas?", 'res_security', 'q13'),
    # Ramo Gestão
    'q11': ("Você prefere focar na estratégia do produto (o 'que fazer)?", 'res_product', 'res_scrum'),
    # Ramo Infra
    'q12': ("Você gosta de automatizar servidores e 'nuvem (AWS/Azure)?", 'res_devops', 'res_suporte'),
    # Ramo Backend Linguagem
    'q13': ("Você prefere a estabilidade de grandes empresas e bancos (Enterprise)?", 'res_back_java', 'res_back_modern'),
    
    # RESULTADOS FINAIS (FOLHAS)
    'res_ux_ui': ("Área sugerida: UI/UX Designer (foco em protótios e telas)", None, None),
    'res_front_eng': ("Área sugerida: Engenharia de Frontend", None, None),
    'res_mobile': ("Área sugerida: Desenvolvimento Mobile (IOS/Android)", None, None),
    'res_ia_research': ("Área sugerida: Cientista de IA/ Pesquisador de Machine Learning", None, None),
    'res_data_eng': ("Área sugerida: Engenharia de Dados e Big Data", None, None),
    'res_security': ("Área sugerida: Segurança da Informação / Ethical Hacking", None),
    'res_back_java': ("Área sugerida: Desenvolvimento Backend (Java/Enterprise)", None, None),
    'res_back_modern': ("Área sugerida: Desenvolvimento Backend Moderno (Node.js/Python/Go)", None, None),
    'res_robotica': ("Área sugerida: Engenharia de Robótica e Automação", None, None),
    'res_embarcados': ("Área sugerida: Sistemas Embarcados / IoT / Firmware", None, None),
    'res_product': ("Área sugerida: Product Owner (PO) / Product Manager", None, None),
    'res_scrum': ("Área sugerida: Agile Coach / Scrum Master", None, None),
    'res_devops': ("Área sugerida: DevOps / SRE (Site Reliability Engineering)", None, None),
    'res_suporte': ("Área sugerida: SysAdmin / Suporte N3 / Redes", None, None),
               
}

def get_answer(question):
    "Função auxiliar para validar entrada do usuário (Sim/Não)"
    while True:
        #pega o input e normaliza
        response = input(f"{question} [s/n]: ").strip().lower()
        
        if response in ['s', 'sim', 'y', 'yes', '1']:
            return True
        elif response in ['n', 'não', 'nao', 'no', '0']:
            return False
            
        print(">> Entrada inválida. Por favor, digite 's' para Sim ou 'n' para Não")
        
def run_tree(node_id):
    #Percorre a árvore de decisão recursivamente
    
    #Desempacota o nó atual
    text, yes_id, no_id = decision_tree[node_id]
    
    #Se for nó folha, mostra o resultado final
    if yes_id is None and no_id is None:
        print("\n" + '='*40)
        print(f"RESULTADO: {text}")
        print('='*40 + "\n")
        return
    
    # Se não é folha, faz a pergunta e decide o próximo passo
    print(f"\n {text}")
    answer = get_answer("Sua resposta")
    
    if answer:
        run_tree(yes_id)
    else:
        run_tree(no_id)
        
def main():
    print("=== Árvore de Decisão: Orientação de Carreira em Computação ===")
    print("Este sistema fará uma série de perguntas para sugerir um caminho profissional.")
    print("Responda com 's' (Sim) ou 'n' (Não).\n")
        
    # Inicia a recursão pela raiz 'q1'
    run_tree('q1')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrando o programa...")
        sys.exit(0)