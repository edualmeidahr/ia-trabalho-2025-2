```mermaid
flowchart TD
    start([Início]) --> q1{Gosta de Codar?}

    %% --- RAMO DO CÓDIGO ---
    q1 -- Sim --> q2{Prefere Visual?}
    
    %% Sub-ramo Visual
    q2 -- Sim --> q4{Foca em Design/Cores?}
    q4 -- Sim --> res1[UI/UX Designer]
    q4 -- Não --> q7{Foca na Lógica Front?}
    q7 -- Sim --> res2[Engenharia Frontend]
    q7 -- Não --> res3[Mobile Dev]

    %% Sub-ramo Backend/Logica
    q2 -- Não --> q5{Gosta de Mat. Avançada?}
    q5 -- Sim --> q8{Interesse Acadêmico?}
    q8 -- Sim --> res4[Pesquisador IA]
    q8 -- Não --> res5[Engenharia de Dados]

    q5 -- Não --> q9{Gosta de Segurança?}
    q9 -- Sim --> res6[Cybersec]
    q9 -- Não --> q13{Gosta de Enterprise?}
    q13 -- Sim --> res7[Backend Java/C#]
    q13 -- Não --> res8[Backend Go/Node]

    %% --- RAMO SEM CÓDIGO ---
    q1 -- Não --> q3{Gosta de Hardware?}
    
    %% Sub-ramo Hardware
    q3 -- Sim --> q10{Gosta de Mecânica?}
    q10 -- Sim --> res9[Robótica]
    q10 -- Não --> res10[IoT / Embarcados]

    %% Sub-ramo Gestão/Ops
    q3 -- Não --> q6{Gosta de Liderança?}
    q6 -- Sim --> q11{Foca no Produto?}
    q11 -- Sim --> res11[Product Owner]
    q11 -- Não --> res12[Scrum Master]

    q6 -- Não --> q12{Gosta de Cloud/Autom.?}
    q12 -- Sim --> res13[DevOps/SRE]
    q12 -- Não --> res14[Suporte/Redes]

    %% Estilos
    classDef question fill:#456,stroke:#333,stroke-width:2px;
    classDef result fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000;
    class q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13 question;
    class res1,res2,res3,res4,res5,res6,res7,res8,res9,res10,res11,res12,res13,res14 result;
    ```