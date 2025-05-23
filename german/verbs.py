import requests
import random
import subprocess
import shutil
import time
import locale

# Lista de verbos B2, com frases que usam estruturas mais avançadas como voz passiva e Konjunktiv II
verbos = [
    {
        "verbo": "begegnen",
        "tradução": "encontrar, deparar-se com",
        "frase": "Gestern bin ich meinem alten Lehrer begegnet, der mir früher Mathematik beigebracht hat.",
        "tradução_frase": "Ontem encontrei meu antigo professor, que me ensinava matemática antes.",
        "sinônimo": ["treffen", "stoßen auf"],
        "perfekt": "ist begegnet",
        "präteritum": "begegnete",
        "regência": "begegnen + Dativ (jemandem begegnen)",
        "outra_frase": "Hätte ich ihn früher getroffen, hätte ich ihn um Hilfe gebeten.",
        "tradução_outra_frase": "Se eu o tivesse encontrado antes, teria pedido ajuda a ele.",
        "reflexivo": False
    },
    {
        "verbo": "erinnern",
        "tradução": "lembrar-se",
        "frase": "Ich erinnere mich nicht daran, ob er gesagt hat, dass er kommt.",
        "tradução_frase": "Eu não me lembro se ele disse que viria.",
        "sinônimo": ["gedenken", "sich ins Gedächtnis rufen"],
        "perfekt": "hat sich erinnert",
        "präteritum": "erinnerte sich",
        "regência": "sich erinnern + an + Akkusativ",
        "outra_frase": "Wenn ich mir die Regeln ins Gedächtnis gerufen hätte, hätte ich den Test bestanden.",
        "tradução_outra_frase": "Se eu tivesse me lembrado melhor das regras, teria passado no teste.",
        "reflexivo": True
    },
    {
        "verbo": "bestehen",
        "tradução": "passar em algo, existir",
        "frase": "Er hat die Prüfung bestanden, obwohl sie sehr schwer war.",
        "tradução_frase": "Ele passou na prova, embora fosse muito difícil.",
        "sinônimo": ["erfolgreich sein", "absolvieren"],
        "perfekt": "hat bestanden",
        "präteritum": "bestand",
        "regência": "bestehen + aus + Dativ / bestehen + in + Dativ",
        "outra_frase": "Wenn ich mehr gelernt hätte, hätte ich die Prüfung auch absolviert.",
        "tradução_outra_frase": "Se eu tivesse estudado mais, também teria passado na prova.",
        "reflexivo": False
    },
    {
        "verbo": "beschweren",
        "tradução": "reclamar",
        "frase": "Ich habe mich beim Manager beschwert, weil der Service schlecht war.",
        "tradução_frase": "Reclamei com o gerente porque o serviço foi ruim.",
        "sinônimo": ["reklamieren", "beanstanden"],
        "perfekt": "hat sich beschwert",
        "präteritum": "beschwerte sich",
        "regência": "sich beschweren + bei + Dativ / über + Akkusativ",
        "outra_frase": "Hätte ich mich früher beanstandet, wäre das Problem vielleicht gelöst worden.",
        "tradução_outra_frase": "Se eu tivesse reclamado antes, o problema talvez tivesse sido resolvido.",
        "reflexivo": True
    },
    {
        "verbo": "erkundigen",
        "tradução": "informar-se",
        "frase": "Ich habe mich danach erkundigt, ob der Kurs noch verfügbar ist.",
        "tradução_frase": "Me informei se o curso ainda está disponível.",
        "sinônimo": ["nachfragen", "sich informieren"],
        "perfekt": "hat sich erkundigt",
        "präteritum": "erkundigte sich",
        "regência": "sich erkundigen + bei + Dativ / nach + Dativ",
        "outra_frase": "Er hätte sich besser über die Firma informieren sollen, bevor er den Vertrag unterschrieb.",
        "tradução_outra_frase": "Ele deveria ter se informado melhor sobre a empresa antes de assinar o contrato.",
        "reflexivo": True
    },
    {
        "verbo": "beeinflussen",
        "tradução": "influenciar",
        "frase": "Die Medien beeinflussen unsere Meinung stärker, als wir denken.",
        "tradução_frase": "Os meios de comunicação influenciam nossa opinião mais do que pensamos.",
        "sinônimo": ["prägen", "einwirken auf"],
        "perfekt": "hat beeinflusst",
        "präteritum": "beeinflusste",
        "regência": "beeinflussen + Akkusativ",
        "outra_frase": "Wenn er sich nicht so leicht hätte einwirken lassen, hätte er eine bessere Entscheidung getroffen.",
        "tradução_outra_frase": "Se ele não tivesse se deixado influenciar tão facilmente, teria tomado uma decisão melhor.",
        "reflexivo": False
    },
    {
        "verbo": "verabreden",
        "tradução": "combinar um encontro",
        "frase": "Wir haben uns verabredet, nachdem wir uns lange nicht gesehen hatten.",
        "tradução_frase": "Marcamos um encontro depois de muito tempo sem nos vermos.",
        "sinônimo": ["ein Treffen ausmachen", "verabreden"],
        "perfekt": "hat sich verabredet",
        "präteritum": "verabredete sich",
        "regência": "sich verabreden + mit + Dativ",
        "outra_frase": "Hätten wir uns früher verabredet, hätten wir mehr Zeit miteinander gehabt.",
        "tradução_outra_frase": "Se tivéssemos marcado antes, teríamos tido mais tempo juntos.",
        "reflexivo": True
    },
    {
        "verbo": "irren",
        "tradução": "equivocar-se",
        "frase": "Ich habe mich geirrt, als ich dachte, dass er ehrlich sei.",
        "tradução_frase": "Me enganei quando pensei que ele fosse honesto.",
        "sinônimo": ["sich täuschen", "sich irren"],
        "perfekt": "hat sich geirrt",
        "präteritum": "irrte sich",
        "regência": "sich irren + in + Dativ",
        "outra_frase": "Wenn du dich nicht getäuscht hättest, wäre alles anders verlaufen.",
        "tradução_outra_frase": "Se você não tivesse se enganado, tudo teria sido diferente.",
        "reflexivo": True
    },
    {
        "verbo": "zwingen",
        "tradução": "forçar, obrigar",
        "frase": "Man kann niemanden dazu zwingen, etwas zu tun, was er nicht will.",
        "tradução_frase": "Não se pode forçar ninguém a fazer algo que não quer.",
        "sinônimo": ["nötigen", "zwingen"],
        "perfekt": "hat gezwungen",
        "präteritum": "zwang",
        "regência": "zwingen + zu + Dativ",
        "outra_frase": "Wenn sie mich nicht gezwungen hätten, hätte ich es nicht gemacht.",
        "tradução_outra_frase": "Se eles não tivessem me forçado, eu não teria feito.",
        "reflexivo": False
    },
    {
        "verbo": "bedrohen",
        "tradução": "ameaçar",
        "frase": "Die Umweltverschmutzung bedroht viele Tierarten.",
        "tradução_frase": "A poluição ameaça muitas espécies de animais.",
        "sinônimo": ["gefährden", "bedrohen"],
        "perfekt": "hat bedroht",
        "präteritum": "bedrohte",
        "regência": "bedrohen + Akkusativ",
        "outra_frase": "Hätte man früher Maßnahmen ergriffen, wäre die Natur nicht so gefährdet worden.",
        "tradução_outra_frase": "Se tivessem tomado medidas antes, a natureza não teria sido tão ameaçada.",
        "reflexivo": False
    },
    {
        "verbo": "ablehnen",
        "tradução": "recusar, rejeitar",
        "frase": "Er hat das Jobangebot abgelehnt, weil er ein besseres gefunden hat.",
        "tradução_frase": "Ele recusou a oferta de emprego porque encontrou uma melhor.",
        "sinônimo": ["zurückweisen", "abweisen"],
        "perfekt": "hat abgelehnt",
        "präteritum": "lehnte ab",
        "regência": "ablehnen + Akkusativ",
        "outra_frase": "Hätte er das Angebot nicht zurückgewiesen, hätte er jetzt einen sicheren Arbeitsplatz.",
        "tradução_outra_frase": "Se ele não tivesse recusado a oferta, teria um emprego seguro agora.",
        "reflexivo": False
    },
    {
        "verbo": "anpassen",
        "tradução": "adaptar-se",
        "frase": "Es ist nicht leicht, sich an eine neue Kultur anzupassen.",
        "tradução_frase": "Não é fácil se adaptar a uma nova cultura.",
        "sinônimo": ["sich gewöhnen", "sich einleben"],
        "perfekt": "hat sich angepasst",
        "präteritum": "passte sich an",
        "regência": "sich anpassen + an + Akkusativ",
        "outra_frase": "Wenn er sich schneller eingelebt hätte, hätte er weniger Probleme gehabt.",
        "tradução_outra_frase": "Se ele tivesse se adaptado mais rápido, teria tido menos problemas.",
        "reflexivo": True
    },
    {
        "verbo": "nachdenken",
        "tradução": "refletir, pensar sobre",
        "frase": "Ich muss über deine Worte nachdenken, bevor ich antworte.",
        "tradução_frase": "Preciso refletir sobre suas palavras antes de responder.",
        "sinônimo": ["überlegen", "erwägen"],
        "perfekt": "hat nachgedacht",
        "präteritum": "dachte nach",
        "regência": "nachdenken + über + Akkusativ",
        "outra_frase": "Wenn sie gründlicher erwogen hätte, hätte sie einen besseren Entschluss gefasst.",
        "tradução_outra_frase": "Se ela tivesse refletido melhor, teria tomado uma decisão melhor.",
        "reflexivo": False
    },
    {
        "verbo": "erwägen",
        "tradução": "considerar, ponderar",
        "frase": "Sie erwägt, ein Semester im Ausland zu verbringen.",
        "tradução_frase": "Ela está considerando passar um semestre no exterior.",
        "sinônimo": ["in Betracht ziehen", "überdenken"],
        "perfekt": "hat erwogen",
        "präteritum": "erwog",
        "regência": "erwägen + Akkusativ",
        "outra_frase": "Wenn er diese Möglichkeit überdacht hätte, hätte er eine andere Entscheidung getroffen.",
        "tradução_outra_frase": "Se ele tivesse considerado essa possibilidade, teria tomado uma decisão diferente.",
        "reflexivo": False
    },
    {
        "verbo": "verschwenden",
        "tradução": "desperdiçar",
        "frase": "Du solltest nicht so viel Zeit mit sozialen Medien verschwenden.",
        "tradução_frase": "Você não deveria desperdiçar tanto tempo com redes sociais.",
        "sinônimo": ["vergeuden", "verspielen"],
        "perfekt": "hat verschwendet",
        "präteritum": "verschwendete",
        "regência": "verschwenden + Akkusativ",
        "outra_frase": "Hätte er sein Geld nicht verspielt, könnte er jetzt ein Auto kaufen.",
        "tradução_outra_frase": "Se ele não tivesse desperdiçado seu dinheiro, poderia comprar um carro agora.",
        "reflexivo": False
    },
    {
        "verbo": "zurechtkommen",
        "tradução": "lidar com algo, dar conta",
        "frase": "Sie kommt gut mit der neuen Situation zurecht.",
        "tradução_frase": "Ela lida bem com a nova situação.",
        "sinônimo": ["klarkommen", "bewältigen"],
        "perfekt": "ist zurechtgekommen",
        "präteritum": "kam zurecht",
        "regência": "zurechtkommen + mit + Dativ",
        "outra_frase": "Wenn er die Situation besser bewältigt hätte, hätte er weniger Stress gehabt.",
        "tradução_outra_frase": "Se ele tivesse lidado melhor, teria tido menos estresse.",
        "reflexivo": False
    },
    {
        "verbo": "einfallen",
        "tradução": "ocorrer, vir à mente",
        "frase": "Mir fällt keine gute Idee ein.",
        "tradução_frase": "Não me ocorre nenhuma boa ideia.",
        "sinônimo": ["in den Sinn kommen", "aufkommen"],
        "perfekt": "ist eingefallen",
        "präteritum": "fiel ein",
        "regência": "einfallen + Dativ",
        "outra_frase": "Wenn mir die Lösung früher in den Sinn gekommen wäre, hätten wir Zeit gespart.",
        "tradução_outra_frase": "Se a solução tivesse me ocorrido antes, teríamos economizado tempo.",
        "reflexivo": False
    },
    {
        "verbo": "annehmen",
        "tradução": "aceitar, supor",
        "frase": "Ich nehme an, dass er heute nicht kommt.",
        "tradução_frase": "Eu suponho que ele não venha hoje.",
        "sinônimo": ["vermuten", "akzeptieren"],
        "perfekt": "hat angenommen",
        "präteritum": "nahm an",
        "regência": "annehmen + Akkusativ",
        "outra_frase": "Wenn er das Angebot akzeptiert hätte, wäre er jetzt Geschäftsführer.",
        "tradução_outra_frase": "Se ele tivesse aceitado a oferta, seria diretor agora.",
        "reflexivo": False
    },
    {
        "verbo": "befürchten",
        "tradução": "temer",
        "frase": "Ich befürchte, dass es morgen regnen wird.",
        "tradução_frase": "Temo que vá chover amanhã.",
        "sinônimo": ["Angst haben", "sich fürchten"],
        "perfekt": "hat befürchtet",
        "präteritum": "befürchtete",
        "regência": "befürchten + Akkusativ",
        "outra_frase": "Wenn sie sich nicht gefürchtet hätte, hätte sie anders gehandelt.",
        "tradução_outra_frase": "Se ela não tivesse temido as consequências, teria agido de forma diferente.",
        "reflexivo": False
    },
    {
        "verbo": "beurteilen",
        "tradução": "julgar, avaliar",
        "frase": "Man sollte Menschen nicht nach ihrem Äußeren beurteilen.",
        "tradução_frase": "Não se deve julgar as pessoas pela aparência.",
        "sinônimo": ["bewerten", "einschätzen"],
        "perfekt": "hat beurteilt",
        "präteritum": "beurteilte",
        "regência": "beurteilen + Akkusativ",
        "outra_frase": "Wenn er die Situation richtig eingeschätzt hätte, hätte er eine bessere Entscheidung getroffen.",
        "tradução_outra_frase": "Se ele tivesse avaliado corretamente a situação, teria tomado uma decisão melhor.",
        "reflexivo": False
    },
{
        "verbo": "einführen",
        "tradução": "introduzir",
        "frase": "Nachdem die Regierung neue Maßnahmen eingeführt hatte, verbesserte sich die Situation im Land erheblich.",
        "tradução_frase": "Após o governo ter introduzido novas medidas, a situação no país melhorou significativamente.",
        "sinônimo": ["implementieren", "einleiten"],
        "perfekt": "hat eingeführt",
        "präteritum": "führte ein",
        "regência": "einführen + Akkusativ",
        "outra_frase": "Wenn die Firma das Produkt früher implementiert hätte, wären die Kunden zufriedener.",
        "tradução_outra_frase": "Se a empresa tivesse implementado o produto mais cedo, os clientes estariam mais satisfeitos.",
        "reflexivo": False
    },
    {
        "verbo": "überzeugen",
        "tradução": "convencer",
        "frase": "Er bemühte sich sehr, sie davon zu überzeugen, dass seine Pläne die besten für das Team waren.",
        "tradução_frase": "Ele se esforçou muito para convencê-la de que seus planos eram os melhores para a equipe.",
        "sinônimo": ["überreden", "gewinnen"],
        "perfekt": "hat überzeugt",
        "präteritum": "überzeugte",
        "regência": "überzeugen + Akkusativ",
        "outra_frase": "Hätte er sie überreden können, wären sie jetzt zusammen.",
        "tradução_outra_frase": "Se ele tivesse conseguido convencê-la, estariam juntos agora.",
        "reflexivo": False
    },
    {
        "verbo": "untersuchen",
        "tradução": "examinar, investigar",
        "frase": "Der Arzt untersuchte den Patienten gründlich, bevor er eine Diagnose stellte.",
        "tradução_frase": "O médico examinou minuciosamente o paciente antes de fazer um diagnóstico.",
        "sinônimo": ["prüfen", "erforschen"],
        "perfekt": "hat untersucht",
        "präteritum": "untersuchte",
        "regência": "untersuchen + Akkusativ",
        "outra_frase": "Wenn er das Problem gründlicher geprüft hätte, hätte er eine Lösung gefunden.",
        "tradução_outra_frase": "Se ele tivesse examinado o problema mais a fundo, teria encontrado uma solução.",
        "reflexivo": False
    },
    {
        "verbo": "bewältigen",
        "tradução": "lidar com, superar",
        "frase": "Obwohl die Krise schwerwiegend war, bewältigte sie die Situation mit Bravour.",
        "tradução_frase": "Apesar de a crise ter sido grave, ela lidou com a situação com destreza.",
        "sinônimo": ["meistern", "überwinden"],
        "perfekt": "hat bewältigt",
        "präteritum": "bewältigte",
        "regência": "bewältigen + Akkusativ",
        "outra_frase": "Wenn sie die Herausforderung gemeistert hätte, wäre sie jetzt erfolgreicher.",
        "tradução_outra_frase": "Se ela tivesse superado o desafio, seria mais bem-sucedida agora.",
        "reflexivo": False
    },
    {
        "verbo": "erschöpfen",
        "tradução": "esgotar",
        "frase": "Die Ressourcen waren so stark erschöpft, dass keine weiteren Maßnahmen ergriffen werden konnten.",
        "tradução_frase": "Os recursos estavam tão esgotados que não puderam ser tomadas mais medidas.",
        "sinônimo": ["aufbrauchen", "verbrauchen"],
        "perfekt": "hat erschöpft",
        "präteritum": "erschöpfte",
        "regência": "erschöpfen + Akkusativ",
        "outra_frase": "Wenn sie die Mittel nicht aufgebraucht hätten, könnten sie jetzt weitermachen.",
        "tradução_outra_frase": "Se eles não tivessem esgotado os recursos, poderiam continuar agora.",
        "reflexivo": False
    },
    {
        "verbo": "ausnutzen",
        "tradução": "aproveitar",
        "frase": "Wenn sie die Gelegenheit genutzt hätte, die ihr gegeben wurde, wäre sie jetzt erfolgreicher.",
        "tradução_frase": "Se ela tivesse aproveitado a oportunidade que lhe foi dada, estaria mais bem-sucedida agora.",
        "sinônimo": ["ausbeuten", "verwerten"],
        "perfekt": "hat ausgenutzt",
        "präteritum": "nutzte aus",
        "regência": "ausnutzen + Akkusativ",
        "outra_frase": "Hätten sie die Ressourcen verwertet, wären sie jetzt weiter fortgeschritten.",
        "tradução_outra_frase": "Se eles tivessem aproveitado os recursos, estariam agora mais avançados.",
        "reflexivo": False
    },
    {
        "verbo": "versichern",
        "tradução": "assegurar",
        "frase": "Er versicherte ihr, dass er ihr immer zur Seite stehen würde, egal was passiert.",
        "tradução_frase": "Ele assegurou a ela que sempre estaria ao seu lado, não importando o que acontecesse.",
        "sinônimo": ["garantieren", "beteuern"],
        "perfekt": "hat versichert",
        "präteritum": "versicherte",
        "regência": "versichern + Dativ + Akkusativ",
        "outra_frase": "Wenn er ihr seine Hilfe garantiert hätte, wäre sie nicht so verzweifelt.",
        "tradução_outra_frase": "Se ele tivesse garantido a ajuda a ela, ela não estaria tão desesperada.",
        "reflexivo": False
    },
    {
        "verbo": "unterstützen",
        "tradução": "apoiar",
        "frase": "Obwohl sie anfänglich Zweifel hatten, unterstützten sie schließlich das Projekt, weil sie an dessen Erfolg glaubten.",
        "tradução_frase": "Apesar de terem dúvidas inicialmente, eles finalmente apoiaram o projeto porque acreditavam no seu sucesso.",
        "sinônimo": ["fördern", "helfen"],
        "perfekt": "hat unterstützt",
        "präteritum": "unterstützte",
        "regência": "unterstützen + Akkusativ",
        "outra_frase": "Hätten sie das Vorhaben gefördert, wäre es heute erfolgreich.",
        "tradução_outra_frase": "Se eles tivessem promovido a iniciativa, ela seria bem-sucedida hoje.",
        "reflexivo": False
    },
    {
        "verbo": "verändern",
        "tradução": "mudar",
        "frase": "Wenn die Umstände anders gewesen wären, hätten sie ihre Pläne verändert.",
        "tradução_frase": "Se as circunstâncias fossem diferentes, eles teriam mudado seus planos.",
        "sinônimo": ["wandeln", "modifizieren"],
        "perfekt": "hat verändert",
        "präteritum": "veränderte",
        "regência": "verändern + Akkusativ",
        "outra_frase": "Würden sie die Bedingungen modifizieren, könnten sie bessere Ergebnisse erzielen.",
        "tradução_outra_frase": "Se eles modificassem as condições, poderiam obter melhores resultados.",
        "reflexivo": True
    },
    {
        "verbo": "beachten",
        "tradução": "observar, considerar",
        "frase": "Da sie die Regeln beachtet haben, konnten sie das Projekt erfolgreich abschließen.",
        "tradução_frase": "Como eles observaram as regras, puderam concluir o projeto com sucesso.",
        "sinônimo": ["berücksichtigen", "einhalten"],
        "perfekt": "hat beachtet",
        "präteritum": "beachtete",
        "regência": "beachten + Akkusativ",
        "outra_frase": "Hätten sie die Vorschriften berücksichtigt, hätten sie keine Probleme gehabt.",
        "tradução_outra_frase": "Se eles tivessem considerado as normas, não teriam tido problemas.",
        "reflexivo": False
    },
    {
        "verbo": "bewerten",
        "tradução": "avaliar",
        "frase": "Der Lehrer bewertete die Prüfungen so streng, dass viele Schüler durchfielen.",
        "tradução_frase": "O professor avaliou as provas tão rigorosamente que muitos alunos foram reprovados.",
        "sinônimo": ["einschätzen", "beurteilen"],
        "perfekt": "hat bewertet",
        "präteritum": "bewertete",
        "regência": "bewerten + Akkusativ",
        "outra_frase": "Hätte er die Leistungen besser eingeschätzt, wären die Ergebnisse anders.",
        "tradução_outra_frase": "Se ele tivesse avaliado melhor os desempenhos, os resultados seriam diferentes.",
        "reflexivo": False
    },
    {
        "verbo": "erreichen",
        "tradução": "alcançar",
        "frase": "Obwohl sie viele Schwierigkeiten hatten, erreichten sie ihr Ziel, was sie sehr stolz machte.",
        "tradução_frase": "Apesar de enfrentarem muitas dificuldades, eles alcançaram seu objetivo, o que os deixou muito orgulhosos.",
        "sinônimo": ["erlangen", "erzielen"],
        "perfekt": "hat erreicht",
        "präteritum": "erreichte",
        "regência": "erreichen + Akkusativ",
        "outra_frase": "Hätten sie das Ziel erlangt, wären sie jetzt zufrieden.",
        "tradução_outra_frase": "Se eles tivessem alcançado o objetivo, estariam satisfeitos agora.",
        "reflexivo": False
    },
    {
        "verbo": "feststellen",
        "tradução": "constatar",
        "frase": "Er stellte fest, dass ein Fehler gemacht worden war, nachdem er die Dokumente gründlich überprüft hatte.",
        "tradução_frase": "Ele constatou que um erro havia sido cometido, depois de revisar minuciosamente os documentos.",
        "sinônimo": ["erkennen", "bemerken"],
        "perfekt": "hat festgestellt",
        "präteritum": "stellte fest",
        "regência": "feststellen + Akkusativ",
        "outra_frase": "Hätten sie den Irrtum bemerkt, hätten sie ihn korrigieren können.",
        "tradução_outra_frase": "Se eles tivessem percebido o erro, poderiam tê-lo corrigido.",
        "reflexivo": False
    },
    {
        "verbo": "umsetzen",
        "tradução": "implementar",
        "frase": "Wenn sie den Plan in die Tat umgesetzt hätten, würden sie jetzt die Früchte ihrer Arbeit ernten.",
        "tradução_frase": "Se eles tivessem implementado o plano, estariam agora colhendo os frutos do seu trabalho.",
        "sinônimo": ["durchführen", "realisieren"],
        "perfekt": "hat umgesetzt",
        "präteritum": "setzte um",
        "regência": "umsetzen + Akkusativ",
        "outra_frase": "Wenn sie die Strategie realisiert hätten, wären sie jetzt erfolgreicher.",
        "tradução_outra_frase": "Se eles tivessem realizado a estratégia, seriam mais bem-sucedidos agora.",
        "reflexivo": False
    },
    {
        "verbo": "verhindern",
        "tradução": "prevenir, impedir",
        "frase": "Sie konnten den Unfall verhindern, indem sie rechtzeitig die richtigen Maßnahmen ergriffen.",
        "tradução_frase": "Eles conseguiram prevenir o acidente tomando as medidas corretas a tempo.",
        "sinônimo": ["vermeiden", "abwehren"],
        "perfekt": "hat verhindert",
        "präteritum": "verhinderte",
        "regência": "verhindern + Akkusativ",
        "outra_frase": "Hätten sie die Gefahr abgewehrt, wären sie jetzt in Sicherheit.",
        "tradução_outra_frase": "Se eles tivessem evitado o perigo, estariam em segurança agora.",
        "reflexivo": False
    },
    {
        "verbo": "veröffentlichen",
        "tradução": "publicar",
        "frase": "Nachdem das Buch veröffentlicht worden war, erhielt es viel Lob von den Kritikern.",
        "tradução_frase": "Depois que o livro foi publicado, recebeu muitos elogios dos críticos.",
        "sinônimo": ["herausgeben", "verbreiten"],
        "perfekt": "hat veröffentlicht",
        "präteritum": "veröffentlichte",
        "regência": "veröffentlichen + Akkusativ",
        "outra_frase": "Wäre das Buch früher herausgegeben worden, hätte es eine größere Leserschaft erreicht.",
        "tradução_outra_frase": "Se o livro tivesse sido publicado mais cedo, teria alcançado um público maior.",
        "reflexivo": False
    },
    {
        "verbo": "versprechen",
        "tradução": "prometer",
        "frase": "Er versprach, dass er das Problem lösen würde, sobald er zurückkäme.",
        "tradução_frase": "Ele prometeu que resolveria o problema assim que voltasse.",
        "sinônimo": ["zusichern", "garantieren"],
        "perfekt": "hat versprochen",
        "präteritum": "versprach",
        "regência": "versprechen + Dativ + Akkusativ",
        "outra_frase": "Hätte er ihr die Unterstützung zugesichert, wäre sie beruhigt gewesen.",
        "tradução_outra_frase": "Se ele tivesse garantido o apoio a ela, ela teria ficado mais tranquila.",
        "reflexivo": False
    },
    {
        "verbo": "verstehen",
        "tradução": "entender",
        "frase": "Er erklärte es so deutlich, dass jeder es verstehen konnte.",
        "tradução_frase": "Ele explicou tão claramente que todos puderam entender.",
        "sinônimo": ["begreifen", "erfassen"],
        "perfekt": "hat verstanden",
        "präteritum": "verstand",
        "regência": "verstehen + Akkusativ",
        "outra_frase": "Hätten sie das Konzept begriffen, könnten sie es anwenden.",
        "tradução_outra_frase": "Se eles tivessem entendido o conceito, poderiam aplicá-lo.",
        "reflexivo": False
    },
    {
        "verbo": "vorbereiten",
        "tradução": "preparar",
        "frase": "Sie bereitete sich gut auf die Prüfung vor, indem sie jeden Tag lernte.",
        "tradução_frase": "Ela se preparou bem para o exame estudando todos os dias.",
        "sinônimo": ["arrangieren", "organisieren"],
        "perfekt": "hat vorbereitet",
        "präteritum": "bereitete vor",
        "regência": "vorbereiten + Akkusativ",
        "outra_frase": "Hätten sie den Event besser arrangiert, wäre alles reibungslos verlaufen.",
        "tradução_outra_frase": "Se eles tivessem organizado melhor o evento, tudo teria corrido bem.",
        "reflexivo": True
    },
    {
        "verbo": "unterscheiden",
        "tradução": "distinguir",
        "frase": "Er konnte nicht zwischen den beiden Zwillingen unterscheiden.",
        "tradução_frase": "Ele não conseguia distinguir entre os dois gêmeos.",
        "sinônimo": ["differenzieren", "erkennen"],
        "perfekt": "hat unterschieden",
        "präteritum": "unterschied",
        "regência": "unterscheiden + zwischen + Dativ",
        "outra_frase": "Hätten sie die Unterschiede erkannt, hätten sie die Situation besser bewältigt.",
        "tradução_outra_frase": "Se eles tivessem reconhecido as diferenças, teriam lidado melhor com a situação.",
        "reflexivo": False
    },
    {
        "verbo": "beschreiben",
        "tradução": "descrever",
        "frase": "Sie beschrieb die Szene so lebhaft, dass man sie sich genau vorstellen konnte.",
        "tradução_frase": "Ela descreveu a cena tão vividamente que se podia imaginá-la com precisão.",
        "sinônimo": ["schildern", "darstellen"],
        "perfekt": "hat beschrieben",
        "präteritum": "beschrieb",
        "regência": "beschreiben + Akkusativ",
        "outra_frase": "Hätte er die Situation besser dargestellt, hätten alle es verstanden.",
        "tradução_outra_frase": "Se ele tivesse representado a situação melhor, todos teriam entendido.",
        "reflexivo": False
    },
    {
        "verbo": "vergleichen",
        "tradução": "comparar",
        "frase": "Sie verglich die beiden Produkte, bevor sie eine Entscheidung traf.",
        "tradução_frase": "Ela comparou os dois produtos antes de tomar uma decisão.",
        "sinônimo": ["gegenüberstellen", "bewerten"],
        "perfekt": "hat verglichen",
        "präteritum": "verglich",
        "regência": "vergleichen + Akkusativ",
        "outra_frase": "Würden sie die Möglichkeiten bewerten, könnten sie die beste Wahl treffen.",
        "tradução_outra_frase": "Se eles avaliassem as opções, poderiam fazer a melhor escolha.",
        "reflexivo": False
    },
    {
        "verbo": "vermeiden",
        "tradução": "evitar",
        "frase": "Um Konflikte zu vermeiden, suchte sie das Gespräch mit allen Beteiligten.",
        "tradução_frase": "Para evitar conflitos, ela buscou conversar com todos os envolvidos.",
        "sinônimo": ["ausweichen", "verhindern"],
        "perfekt": "hat vermieden",
        "präteritum": "vermied",
        "regência": "vermeiden + Akkusativ",
        "outra_frase": "Wenn sie den Streit hätten verhindern können, wäre die Situation besser gewesen.",
        "tradução_outra_frase": "Se eles pudessem ter evitado a briga, a situação teria sido melhor.",
        "reflexivo": False
    },
    {
        "verbo": "zustimmen",
        "tradução": "concordar",
        "frase": "Nachdem er die Argumente gehört hatte, stimmte er dem Vorschlag zu.",
        "tradução_frase": "Depois de ouvir os argumentos, ele concordou com a proposta.",
        "sinônimo": ["akzeptieren", "einwilligen"],
        "perfekt": "hat zugestimmt",
        "präteritum": "stimmte zu",
        "regência": "zustimmen + Dativ",
        "outra_frase": "Hätte er dem Plan eingewilligt, wäre der Prozess einfacher gewesen.",
        "tradução_outra_frase": "Se ele tivesse concordado com o plano, o processo teria sido mais simples.",
        "reflexivo": False
    },
    {
        "verbo": "anerkennen",
        "tradução": "reconhecer, valorizar",
        "frase": "Seine Arbeit wurde von der Firma anerkannt, nachdem er jahrelang exzellente Leistungen erbracht hatte.",
        "tradução_frase": "Seu trabalho foi reconhecido pela empresa depois de anos de desempenho excelente.",
        "sinônimo": ["würdigen", "loben"],
        "perfekt": "hat anerkannt",
        "präteritum": "erkannte an",
        "regência": "anerkennen + Akkusativ",
        "outra_frase": "Wenn sein Beitrag früher gewürdigt worden wäre, hätte er die Firma nicht verlassen.",
        "tradução_outra_frase": "Se sua contribuição tivesse sido valorizada antes, ele não teria deixado a empresa.",
        "reflexivo": False
    },
    {
        "verbo": "anfordern",
        "tradução": "solicitar, requerer",
        "frase": "Die Dokumente wurden gestern von der Behörde angefordert, damit der Prozess schneller abgeschlossen wird.",
        "tradução_frase": "Os documentos foram solicitados ontem pela autoridade para que o processo seja concluído mais rapidamente.",
        "sinônimo": ["beantragen", "erbitten"],
        "perfekt": "hat angefordert",
        "präteritum": "forderte an",
        "regência": "anfordern + Akkusativ",
        "outra_frase": "Hätten sie die Genehmigung rechtzeitig beantragt, wäre das Projekt bereits begonnen worden.",
        "tradução_outra_frase": "Se tivessem solicitado a autorização a tempo, o projeto já teria sido iniciado.",
        "reflexivo": False
    },
    {
        "verbo": "ausdrücken",
        "tradução": "expressar",
        "frase": "Sie konnte ihre Gefühle nicht richtig ausdrücken, weil sie sehr nervös war.",
        "tradução_frase": "Ela não conseguiu expressar seus sentimentos corretamente porque estava muito nervosa.",
        "sinônimo": ["formulieren", "vermitteln"],
        "perfekt": "hat ausgedrückt",
        "präteritum": "drückte aus",
        "regência": "ausdrücken + Akkusativ",
        "outra_frase": "Wenn er seine Meinung klar formuliert hätte, wäre es keine Missverständnisse gegeben.",
        "tradução_outra_frase": "Se ele tivesse formulado sua opinião claramente, não teria havido mal-entendidos.",
        "reflexivo": False
    },
    {
        "verbo": "benachrichtigen",
        "tradução": "notificar, informar",
        "frase": "Die Kunden wurden per E-Mail benachrichtigt, dass ihre Bestellungen versandt wurden.",
        "tradução_frase": "Os clientes foram notificados por e-mail de que seus pedidos foram enviados.",
        "sinônimo": ["informieren", "melden"],
        "perfekt": "hat benachrichtigt",
        "präteritum": "benachrichtigte",
        "regência": "benachrichtigen + Akkusativ",
        "outra_frase": "Hätte das Unternehmen die Kunden früher informiert, wären sie nicht so unzufrieden gewesen.",
        "tradução_outra_frase": "Se a empresa tivesse informado os clientes antes, eles não teriam ficado tão insatisfeitos.",
        "reflexivo": False
    },
    {
        "verbo": "bewahren",
        "tradução": "preservar, manter",
        "frase": "Trotz der schwierigen Umstände bewahrte er immer seine Ruhe.",
        "tradução_frase": "Apesar das circunstâncias difíceis, ele sempre manteve a calma.",
        "sinônimo": ["erhalten", "konservieren"],
        "perfekt": "hat bewahrt",
        "präteritum": "bewahrte",
        "regência": "bewahren + Akkusativ",
        "outra_frase": "Wenn die Natur besser erhalten worden wäre, hätten wir weniger Umweltprobleme.",
        "tradução_outra_frase": "Se a natureza tivesse sido melhor preservada, teríamos menos problemas ambientais.",
        "reflexivo": False
    },
    {
        "verbo": "entlasten",
        "tradução": "aliviar, desafogar",
        "frase": "Die neuen Maßnahmen sollen die Mitarbeiter entlasten, damit sie effizienter arbeiten können.",
        "tradução_frase": "As novas medidas devem aliviar os funcionários para que possam trabalhar de forma mais eficiente.",
        "sinônimo": ["erleichtern", "reduzieren"],
        "perfekt": "hat entlastet",
        "präteritum": "entlastete",
        "regência": "entlasten + Akkusativ",
        "outra_frase": "Wenn die Arbeitsbelastung reduziert worden wäre, hätten die Angestellten weniger Stress gehabt.",
        "tradução_outra_frase": "Se a carga de trabalho tivesse sido reduzida, os funcionários teriam tido menos estresse.",
        "reflexivo": False
    },
    {
        "verbo": "vereinbaren",
        "tradução": "agendar, combinar",
        "frase": "Wir haben einen Termin mit dem Arzt vereinbart, um die Untersuchung durchzuführen.",
        "tradução_frase": "Marcamos uma consulta com o médico para realizar o exame.",
        "sinônimo": ["festlegen", "absprechen"],
        "perfekt": "hat vereinbart",
        "präteritum": "vereinbarte",
        "regência": "vereinbaren + Akkusativ",
        "outra_frase": "Hätten sie den Zeitplan früher festgelegt, wäre alles besser organisiert gewesen.",
        "tradução_outra_frase": "Se tivessem definido o cronograma antes, tudo teria sido melhor organizado.",
        "reflexivo": False
    },
    {
        "verbo": "verlangen",
        "tradução": "exigir, requerer",
        "frase": "Der Kunde verlangte eine Rückerstattung, weil das Produkt defekt war.",
        "tradução_frase": "O cliente exigiu um reembolso porque o produto estava com defeito.",
        "sinônimo": ["fordern", "beanspruchen"],
        "perfekt": "hat verlangt",
        "präteritum": "verlangte",
        "regência": "verlangen + Akkusativ",
        "outra_frase": "Wenn der Vertrag korrekt eingehalten worden wäre, hätte niemand eine Entschädigung beansprucht.",
        "tradução_outra_frase": "Se o contrato tivesse sido cumprido corretamente, ninguém teria requerido uma indenização.",
        "reflexivo": False
    },
    {
        "verbo": "ableiten",
        "tradução": "derivar, deduzir",
        "frase": "Aus diesen Daten kann man wichtige Schlussfolgerungen ableiten, die für die Forschung relevant sind.",
        "tradução_frase": "A partir desses dados, é possível derivar conclusões importantes para a pesquisa.",
        "sinônimo": ["erschließen", "folgern"],
        "perfekt": "hat abgeleitet",
        "präteritum": "leitete ab",
        "regência": "ableiten + aus + Dativ",
        "outra_frase": "Hätte er die richtigen Informationen erschlossen, wäre die Analyse präziser gewesen.",
        "tradução_outra_frase": "Se ele tivesse deduzido as informações corretas, a análise teria sido mais precisa.",
        "reflexivo": False
    },
    {
        "verbo": "abschaffen",
        "tradução": "abolir, eliminar",
        "frase": "Die Regierung hat beschlossen, bestimmte Steuern abzuschaffen, um die Wirtschaft zu fördern.",
        "tradução_frase": "O governo decidiu abolir certos impostos para impulsionar a economia.",
        "sinônimo": ["aufheben", "beseitigen"],
        "perfekt": "hat abgeschafft",
        "präteritum": "schaffte ab",
        "regência": "abschaffen + Akkusativ",
        "outra_frase": "Wären die alten Regelungen früher aufgehoben worden, hätte es weniger bürokratische Hürden gegeben.",
        "tradução_outra_frase": "Se as regras antigas tivessem sido abolidas antes, teria havido menos obstáculos burocráticos.",
        "reflexivo": False
    },
    {
        "verbo": "anstreben",
        "tradução": "almejar, aspirar a",
        "frase": "Er strebt eine Karriere in der Wissenschaft an, weil er sich für Forschung begeistert.",
        "tradução_frase": "Ele almeja uma carreira na ciência porque é apaixonado por pesquisa.",
        "sinônimo": ["sich bemühen um", "nach etwas trachten"],
        "perfekt": "hat angestrebt",
        "präteritum": "strebte an",
        "regência": "anstreben + Akkusativ",
        "outra_frase": "Hätte sie nach einer besseren Position getrachtet, hätte sie schon früher befördert werden können.",
        "tradução_outra_frase": "Se ela tivesse aspirado a um cargo melhor, poderia ter sido promovida mais cedo.",
        "reflexivo": False
    },
    {
        "verbo": "beauftragen",
        "tradução": "encarregar, contratar",
        "frase": "Die Firma hat eine Agentur beauftragt, um eine neue Marketingstrategie zu entwickeln.",
        "tradução_frase": "A empresa encarregou uma agência de desenvolver uma nova estratégia de marketing.",
        "sinônimo": ["betrauen", "anweisen"],
        "perfekt": "hat beauftragt",
        "präteritum": "beauftragte",
        "regência": "beauftragen + Akkusativ + mit + Dativ",
        "outra_frase": "Wenn das Management einen Experten damit betraut hätte, wäre das Projekt erfolgreicher gewesen.",
        "tradução_outra_frase": "Se a gerência tivesse confiado isso a um especialista, o projeto teria sido mais bem-sucedido.",
        "reflexivo": False
    },
    {
        "verbo": "einreichen",
        "tradução": "apresentar, submeter",
        "frase": "Der Antrag muss spätestens bis Freitag eingereicht werden, sonst wird er nicht bearbeitet.",
        "tradução_frase": "O pedido deve ser submetido até sexta-feira, caso contrário, não será processado.",
        "sinônimo": ["vorlegen", "abgeben"],
        "perfekt": "hat eingereicht",
        "präteritum": "reichte ein",
        "regência": "einreichen + Akkusativ",
        "outra_frase": "Hätte er die Dokumente pünktlich vorgelegt, wäre das Verfahren schneller abgeschlossen worden.",
        "tradução_outra_frase": "Se ele tivesse apresentado os documentos a tempo, o processo teria sido concluído mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "nachahmen",
        "tradução": "imitar",
        "frase": "Kinder ahmen oft das Verhalten ihrer Eltern nach, weil sie von ihnen lernen.",
        "tradução_frase": "As crianças costumam imitar o comportamento dos pais porque aprendem com eles.",
        "sinônimo": ["kopieren", "reproduzieren"],
        "perfekt": "hat nachgeahmt",
        "präteritum": "ahmte nach",
        "regência": "nachahmen + Akkusativ",
        "outra_frase": "Wenn er den Stil eines bekannten Künstlers kopiert hätte, wäre sein Werk nicht so originell gewesen.",
        "tradução_outra_frase": "Se ele tivesse copiado o estilo de um artista famoso, sua obra não teria sido tão original.",
        "reflexivo": False
    },
    {
        "verbo": "übertreffen",
        "tradução": "superar, ultrapassar",
        "frase": "Seine Leistung hat alle Erwartungen übertroffen, was ihn zum besten Mitarbeiter des Monats machte.",
        "tradução_frase": "Seu desempenho superou todas as expectativas, tornando-o o melhor funcionário do mês.",
        "sinônimo": ["überbieten", "überragen"],
        "perfekt": "hat übertroffen",
        "präteritum": "übertraf",
        "regência": "übertreffen + Akkusativ",
        "outra_frase": "Wäre sein Konkurrent nicht so stark gewesen, hätte er ihn überboten.",
        "tradução_outra_frase": "Se seu concorrente não tivesse sido tão forte, ele o teria superado.",
        "reflexivo": False
    },
    {
        "verbo": "verarbeiten",
        "tradução": "processar, assimilar",
        "frase": "Nach dem Unfall brauchte er lange, um das Erlebte zu verarbeiten.",
        "tradução_frase": "Depois do acidente, ele precisou de muito tempo para assimilar o que aconteceu.",
        "sinônimo": ["bewältigen", "verwerten"],
        "perfekt": "hat verarbeitet",
        "präteritum": "verarbeitete",
        "regência": "verarbeiten + Akkusativ",
        "outra_frase": "Hätte sie ihre Emotionen besser bewältigt, wäre ihr Zustand stabiler gewesen.",
        "tradução_outra_frase": "Se ela tivesse lidado melhor com suas emoções, seu estado teria sido mais estável.",
        "reflexivo": False
    },
    {
        "verbo": "anwenden",
        "tradução": "aplicar, empregar",
        "frase": "Die neue Methode wurde erfolgreich in mehreren Projekten angewendet, wodurch die Effizienz gesteigert wurde.",
        "tradução_frase": "O novo método foi aplicado com sucesso em vários projetos, aumentando a eficiência.",
        "sinônimo": ["nutzen", "einsetzen"],
        "perfekt": "hat angewendet",
        "präteritum": "wendete an",
        "regência": "anwenden + Akkusativ",
        "outra_frase": "Wenn sie die richtige Technik genutzt hätten, wären die Ergebnisse besser gewesen.",
        "tradução_outra_frase": "Se eles tivessem utilizado a técnica correta, os resultados teriam sido melhores.",
        "reflexivo": False
    },
    {
        "verbo": "auswerten",
        "tradução": "avaliar, analisar",
        "frase": "Die gesammelten Daten wurden gründlich ausgewertet, um eine fundierte Entscheidung treffen zu können.",
        "tradução_frase": "Os dados coletados foram avaliados cuidadosamente para que uma decisão bem fundamentada pudesse ser tomada.",
        "sinônimo": ["analysieren", "interpretieren"],
        "perfekt": "hat ausgewertet",
        "präteritum": "wertete aus",
        "regência": "auswerten + Akkusativ",
        "outra_frase": "Wenn sie die Statistiken richtig analysiert hätten, wäre der Bericht präziser gewesen.",
        "tradução_outra_frase": "Se eles tivessem analisado as estatísticas corretamente, o relatório teria sido mais preciso.",
        "reflexivo": False
    },
    {
        "verbo": "beantragen",
        "tradução": "solicitar, requerer",
        "frase": "Er hat ein Visum beantragt, damit er in Deutschland arbeiten kann.",
        "tradução_frase": "Ele solicitou um visto para poder trabalhar na Alemanha.",
        "sinônimo": ["anfordern", "ersuchen"],
        "perfekt": "hat beantragt",
        "präteritum": "beantragte",
        "regência": "beantragen + Akkusativ",
        "outra_frase": "Wäre die Erlaubnis rechtzeitig ersucht worden, hätten sie früher mit dem Bau begonnen.",
        "tradução_outra_frase": "Se a autorização tivesse sido solicitada a tempo, eles teriam começado a construção mais cedo.",
        "reflexivo": False
    },
    {
        "verbo": "begrenzen",
        "tradução": "limitar, restringir",
        "frase": "Die Anzahl der Teilnehmer wurde auf 100 begrenzt, um die Qualität der Veranstaltung zu gewährleisten.",
        "tradução_frase": "O número de participantes foi limitado a 100 para garantir a qualidade do evento.",
        "sinônimo": ["einschränken", "reduzieren"],
        "perfekt": "hat begrenzt",
        "präteritum": "begrenzte",
        "regência": "begrenzen + Akkusativ",
        "outra_frase": "Hätte man die Nutzung früher eingeschränkt, wären die Ressourcen nicht erschöpft worden.",
        "tradução_outra_frase": "Se o uso tivesse sido restringido antes, os recursos não teriam se esgotado.",
        "reflexivo": False
    },
    {
        "verbo": "beklagen",
        "tradução": "lamentar, reclamar",
        "frase": "Viele Bürger beklagen sich darüber, dass die Preise ständig steigen.",
        "tradução_frase": "Muitos cidadãos reclamam que os preços estão sempre subindo.",
        "sinônimo": ["beschweren", "monieren"],
        "perfekt": "hat beklagt",
        "präteritum": "beklagte",
        "regência": "sich beklagen + über + Akkusativ",
        "outra_frase": "Hätte er den schlechten Service moniert, hätte das Unternehmen reagieren können.",
        "tradução_outra_frase": "Se ele tivesse reclamado do mau serviço, a empresa poderia ter tomado providências.",
        "reflexivo": True
    },
    {
        "verbo": "durchführen",
        "tradução": "realizar, executar",
        "frase": "Die Inspektion wurde von einem Experten durchgeführt, um mögliche Fehler zu identifizieren.",
        "tradução_frase": "A inspeção foi realizada por um especialista para identificar possíveis erros.",
        "sinônimo": ["verwirklichen", "ausführen"],
        "perfekt": "hat durchgeführt",
        "präteritum": "führte durch",
        "regência": "durchführen + Akkusativ",
        "outra_frase": "Wenn die Pläne richtig ausgeführt worden wären, hätte das Projekt früher abgeschlossen werden können.",
        "tradução_outra_frase": "Se os planos tivessem sido executados corretamente, o projeto poderia ter sido concluído antes.",
        "reflexivo": False
    },
    {
        "verbo": "erhöhen",
        "tradução": "aumentar",
        "frase": "Die Regierung hat beschlossen, die Steuern zu erhöhen, um neue Projekte zu finanzieren.",
        "tradução_frase": "O governo decidiu aumentar os impostos para financiar novos projetos.",
        "sinônimo": ["steigern", "verstärken"],
        "perfekt": "hat erhöht",
        "präteritum": "erhöhte",
        "regência": "erhöhen + Akkusativ",
        "outra_frase": "Hätte das Unternehmen die Produktion verstärkt, hätte es die Nachfrage besser gedeckt.",
        "tradução_outra_frase": "Se a empresa tivesse aumentado a produção, teria atendido melhor a demanda.",
        "reflexivo": False
    },
    {
        "verbo": "genehmigen",
        "tradução": "aprovar",
        "frase": "Der Bauplan wurde von den Behörden genehmigt, nachdem alle Vorschriften eingehalten wurden.",
        "tradução_frase": "O plano de construção foi aprovado pelas autoridades depois que todas as regulamentações foram seguidas.",
        "sinônimo": ["bewilligen", "zustimmen"],
        "perfekt": "hat genehmigt",
        "präteritum": "genehmigte",
        "regência": "genehmigen + Akkusativ",
        "outra_frase": "Hätten sie dem Vorschlag zugestimmt, wäre das Problem bereits gelöst worden.",
        "tradução_outra_frase": "Se tivessem concordado com a proposta, o problema já teria sido resolvido.",
        "reflexivo": False
    },
    {
        "verbo": "aufgeben",
        "tradução": "desistir",
        "frase": "Er hätte niemals aufgeben sollen, auch wenn die Situation schwierig war.",
        "tradução_frase": "Ele nunca deveria ter desistido, mesmo que a situação fosse difícil.",
        "sinônimo": ["nachlassen", "aufhören"],
        "perfekt": "hat aufgegeben",
        "präteritum": "gab auf",
        "regência": "aufgeben + Akkusativ",
        "outra_frase": "Wenn er nicht nachgelassen hätte, hätte er das Ziel erreichen können.",
        "tradução_outra_frase": "Se ele não tivesse desistido, ele poderia ter alcançado o objetivo.",
        "reflexivo": False
    },
    {
        "verbo": "einrichten",
        "tradução": "configurar, instalar",
        "frase": "Die neue Software wurde eingerichtet, nachdem die vorherige Version entfernt worden war.",
        "tradução_frase": "O novo software foi configurado após a versão anterior ter sido removida.",
        "sinônimo": ["installieren", "aufbauen"],
        "perfekt": "hat eingerichtet",
        "präteritum": "richtete ein",
        "regência": "einrichten + Akkusativ",
        "outra_frase": "Wenn die Technik richtig installiert worden wäre, hätte das Problem nicht mehr existiert.",
        "tradução_outra_frase": "Se a tecnologia tivesse sido instalada corretamente, o problema não existiria mais.",
        "reflexivo": False
    },
    {
        "verbo": "empfangen",
        "tradução": "receber",
        "frase": "Die Gäste wurden herzlich empfangen, obwohl die Veranstaltung kurzfristig geplant wurde.",
        "tradução_frase": "Os convidados foram recebidos calorosamente, embora o evento tenha sido planejado de última hora.",
        "sinônimo": ["bekommen", "aufnehmen"],
        "perfekt": "hat empfangen",
        "präteritum": "empfing",
        "regência": "empfangen + Akkusativ",
        "outra_frase": "Wäre er höflich aufgenommen worden, hätte er sich wohler gefühlt.",
        "tradução_outra_frase": "Se ele tivesse sido recebido educadamente, ele teria se sentido mais confortável.",
        "reflexivo": False
    },
    {
        "verbo": "erstellen",
        "tradução": "criar, elaborar",
        "frase": "Ein detaillierter Bericht hätte erstellt werden müssen, bevor die Entscheidung getroffen wurde.",
        "tradução_frase": "Um relatório detalhado teria que ter sido criado antes que a decisão fosse tomada.",
        "sinônimo": ["anfertigen", "entwickeln"],
        "perfekt": "hat erstellt",
        "präteritum": "erstellte",
        "regência": "erstellen + Akkusativ",
        "outra_frase": "Wenn ein besserer Plan entwickelt worden wäre, hätte das Projekt reibungsloser verlaufen.",
        "tradução_outra_frase": "Se um plano melhor tivesse sido desenvolvido, o projeto teria corrido mais tranquilamente.",
        "reflexivo": False
    },
    {
        "verbo": "entdecken",
        "tradução": "descobrir",
        "frase": "Die neue Methode wurde zufällig entdeckt, während die Forscher an einem anderen Problem arbeiteten.",
        "tradução_frase": "O novo método foi descoberto por acaso enquanto os pesquisadores trabalhavam em outro problema.",
        "sinônimo": ["finden", "aufspüren"],
        "perfekt": "hat entdeckt",
        "präteritum": "entdeckte",
        "regência": "entdecken + Akkusativ",
        "outra_frase": "Hätten sie das Problem früher aufgespürt, wäre die Lösung schneller gefunden worden.",
        "tradução_outra_frase": "Se eles tivessem detectado o problema antes, a solução teria sido encontrada mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "aufklären",
        "tradução": "esclarecer",
        "frase": "Der Vorfall wurde erst aufgeklärt, nachdem alle Zeugen befragt worden waren.",
        "tradução_frase": "O incidente só foi esclarecido depois que todas as testemunhas foram interrogadas.",
        "sinônimo": ["erklären", "deuten"],
        "perfekt": "hat aufgeklärt",
        "präteritum": "klärte auf",
        "regência": "aufklären + Akkusativ",
        "outra_frase": "Hätte man die Situation früher erklärt, wären die Missverständnisse vermieden worden.",
        "tradução_outra_frase": "Se a situação tivesse sido explicada antes, os mal-entendidos teriam sido evitados.",
        "reflexivo": False
    },
    {
        "verbo": "beweisen",
        "tradução": "provar",
        "frase": "Er hätte seine Unschuld bewiesen, wenn er die richtigen Beweise vorgelegt hätte.",
        "tradução_frase": "Ele teria provado sua inocência se tivesse apresentado as provas corretas.",
        "sinônimo": ["nachweisen", "dokumentieren"],
        "perfekt": "hat bewiesen",
        "präteritum": "bewies",
        "regência": "beweisen + Akkusativ",
        "outra_frase": "Wenn er die Dokumente rechtzeitig nachgewiesen hätte, wäre das Missverständnis vermieden worden.",
        "tradução_outra_frase": "Se ele tivesse apresentado os documentos a tempo, o mal-entendido teria sido evitado.",
        "reflexivo": False
    },
    {
        "verbo": "beobachten",
        "tradução": "observar",
        "frase": "Die Veränderungen hätten genauer beobachtet werden müssen, um rechtzeitig reagieren zu können.",
        "tradução_frase": "As mudanças deveriam ter sido observadas mais atentamente para poder reagir a tempo.",
        "sinônimo": ["überwachen", "anschauen"],
        "perfekt": "hat beobachtet",
        "präteritum": "beobachtete",
        "regência": "beobachten + Akkusativ",
        "outra_frase": "Wären die Markttrends frühzeitig überwacht worden, hätte man schneller reagieren können.",
        "tradução_outra_frase": "Se as tendências do mercado tivessem sido monitoradas antes, poderia ter sido possível reagir mais rápido.",
        "reflexivo": False
    },
    {
        "verbo": "einladen",
        "tradução": "convidar",
        "frase": "Sie hätte ihn eingeladen, wenn sie gewusst hätte, dass er interessiert war.",
        "tradução_frase": "Ela o teria convidado se soubesse que ele estava interessado.",
        "sinônimo": ["auffordern", "bitten"],
        "perfekt": "hat eingeladen",
        "präteritum": "lud ein",
        "regência": "einladen + Akkusativ",
        "outra_frase": "Wenn er höflich aufgefordert worden wäre, hätte er wahrscheinlich teilgenommen.",
        "tradução_outra_frase": "Se ele tivesse sido convidado educadamente, ele provavelmente teria participado.",
        "reflexivo": False
    },
    {
        "verbo": "ersetzen",
        "tradução": "substituir",
        "frase": "Das beschädigte Teil hätte ersetzt werden sollen, bevor die Maschine gestartet wurde.",
        "tradução_frase": "A peça danificada deveria ter sido substituída antes de a máquina ser iniciada.",
        "sinônimo": ["austauschen", "wechseln"],
        "perfekt": "hat ersetzt",
        "präteritum": "ersetzte",
        "regência": "ersetzen + Akkusativ",
        "outra_frase": "Wenn das fehlerhafte Gerät rechtzeitig ausgetauscht worden wäre, hätte die Produktion nicht unterbrochen werden müssen.",
        "tradução_outra_frase": "Se o aparelho defeituoso tivesse sido substituído a tempo, a produção não teria precisado ser interrompida.",
        "reflexivo": False
    },
    {
        "verbo": "warnen",
        "tradução": "avisar",
        "frase": "Er hätte gewarnt werden müssen, damit er sich auf die Gefahr vorbereiten konnte.",
        "tradução_frase": "Ele deveria ter sido avisado para que pudesse se preparar para o perigo.",
        "sinônimo": ["benachrichtigen", "alarmieren"],
        "perfekt": "hat gewarnt",
        "präteritum": "warnte",
        "regência": "warnen + Akkusativ",
        "outra_frase": "Wenn die Behörden die Bürger rechtzeitig alarmiert hätten, hätte die Katastrophe verhindert werden können.",
        "tradução_outra_frase": "Se as autoridades tivessem alertado os cidadãos a tempo, a catástrofe poderia ter sido evitada.",
        "reflexivo": False
    },
    {
        "verbo": "überprüfen",
        "tradução": "verificar",
        "frase": "Die Sicherheitsmaßnahmen hätten regelmäßig überprüft werden müssen, um Probleme zu vermeiden.",
        "tradução_frase": "As medidas de segurança deveriam ter sido verificadas regularmente para evitar problemas.",
        "sinônimo": ["kontrollieren", "nachprüfen"],
        "perfekt": "hat überprüft",
        "präteritum": "überprüfte",
        "regência": "überprüfen + Akkusativ",
        "outra_frase": "Hätten sie die Daten nachgeprüft, wären die Fehler frühzeitig erkannt worden.",
        "tradução_outra_frase": "Se eles tivessem verificado os dados, os erros teriam sido detectados mais cedo.",
        "reflexivo": False
    },
    {
        "verbo": "enttäuschen",
        "tradução": "decepcionar",
        "frase": "Er hätte nicht enttäuscht werden sollen, nachdem er so hart gearbeitet hatte.",
        "tradução_frase": "Ele não deveria ter sido decepcionado depois de ter trabalhado tão duro.",
        "sinônimo": ["frustrieren", "verletzen"],
        "perfekt": "hat enttäuscht",
        "präteritum": "enttäuschte",
        "regência": "enttäuschen + Akkusativ",
        "outra_frase": "Wenn die Erwartungen nicht so hoch gewesen wären, hätte er sich weniger frustriert gefühlt.",
        "tradução_outra_frase": "Se as expectativas não tivessem sido tão altas, ele teria se sentido menos frustrado.",
        "reflexivo": False
    },
    {
        "verbo": "verlängern",
        "tradução": "prorrogar",
        "frase": "Die Frist hätte verlängert werden müssen, um allen Beteiligten genügend Zeit zu geben.",
        "tradução_frase": "O prazo deveria ter sido prorrogado para dar tempo suficiente a todos os envolvidos.",
        "sinônimo": ["ausdehnen", "verzögern"],
        "perfekt": "hat verlängert",
        "präteritum": "verlängerte",
        "regência": "verlängern + Akkusativ",
        "outra_frase": "Wenn die Regierung die Frist ausgedehnt hätte, hätten die Unternehmen besser reagieren können.",
        "tradução_outra_frase": "Se o governo tivesse prorrogado o prazo, as empresas teriam podido reagir melhor.",
        "reflexivo": False
    },
    {
        "verbo": "argumentieren",
        "tradução": "argumentar",
        "frase": "Er hätte besser argumentieren können, wenn er die Fakten vorher recherchiert hätte.",
        "tradução_frase": "Ele poderia ter argumentado melhor se tivesse pesquisado os fatos anteriormente.",
        "sinônimo": ["debattieren", "begründen"],
        "perfekt": "hat argumentiert",
        "präteritum": "argumentierte",
        "regência": "argumentieren + Akkusativ",
        "outra_frase": "Hätte er seine Meinung besser begründet, wäre die Diskussion anders verlaufen.",
        "tradução_outra_frase": "Se ele tivesse fundamentado melhor sua opinião, a discussão teria tomado outro rumo.",
        "reflexivo": False
    },
    {
        "verbo": "begründen",
        "tradução": "justificar",
        "frase": "Die Entscheidung hätte besser begründet werden müssen, um Missverständnisse zu vermeiden.",
        "tradução_frase": "A decisão deveria ter sido melhor justificada para evitar mal-entendidos.",
        "sinônimo": ["erklären", "rechtfertigen"],
        "perfekt": "hat begründet",
        "präteritum": "begründete",
        "regência": "begründen + Akkusativ",
        "outra_frase": "Wenn die Maßnahmen besser erklärt worden wären, hätte es weniger Kritik gegeben.",
        "tradução_outra_frase": "Se as medidas tivessem sido melhor explicadas, teria havido menos críticas.",
        "reflexivo": False
    },
    {
        "verbo": "verhandeln",
        "tradução": "negociar",
        "frase": "Die Bedingungen hätten effektiver verhandelt werden müssen, um ein besseres Ergebnis zu erzielen.",
        "tradução_frase": "As condições deveriam ter sido negociadas de forma mais eficaz para alcançar um resultado melhor.",
        "sinônimo": ["diskutieren", "vereinbaren"],
        "perfekt": "hat verhandelt",
        "präteritum": "verhandelte",
        "regência": "verhandeln + über + Akkusativ",
        "outra_frase": "Wenn die Parteien die Bedingungen klarer diskutiert hätten, wäre die Einigung schneller erreicht worden.",
        "tradução_outra_frase": "Se as partes tivessem discutido as condições de forma mais clara, o acordo teria sido alcançado mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "beschränken",
        "tradução": "limitar",
        "frase": "Die Nutzung sozialer Medien hätte beschränkt werden sollen, um negative Auswirkungen zu vermeiden.",
        "tradução_frase": "O uso das redes sociais deveria ter sido limitado para evitar efeitos negativos.",
        "sinônimo": ["einschränken", "begrenzen"],
        "perfekt": "hat beschränkt",
        "präteritum": "beschränkte",
        "regência": "beschränken + auf + Akkusativ",
        "outra_frase": "Wenn die Zeit für die Bildschirmnutzung begrenzt worden wäre, hätten die Jugendlichen besser geschlafen.",
        "tradução_outra_frase": "Se o tempo de uso de tela tivesse sido limitado, os jovens teriam dormido melhor.",
        "reflexivo": False
    },
    {
        "verbo": "erleichtern",
        "tradução": "facilitar",
        "frase": "Die Digitalisierung hätte viele Arbeitsprozesse erleichtert, wenn die Infrastruktur besser gewesen wäre.",
        "tradução_frase": "A digitalização teria facilitado muitos processos de trabalho se a infraestrutura tivesse sido melhor.",
        "sinônimo": ["vereinfachen", "begünstigen"],
        "perfekt": "hat erleichtert",
        "präteritum": "erleichterte",
        "regência": "erleichtern + Akkusativ",
        "outra_frase": "Wenn die Regierung die Digitalisierung früher vereinfacht hätte, wären viele Abläufe effizienter geworden.",
        "tradução_outra_frase": "Se o governo tivesse simplificado a digitalização antes, muitos processos teriam se tornado mais eficientes.",
        "reflexivo": False
    },
    {
        "verbo": "fordern",
        "tradução": "exigir",
        "frase": "Die Mitarbeiter hätten bessere Arbeitsbedingungen fordern sollen, bevor sie gekündigt haben.",
        "tradução_frase": "Os funcionários deveriam ter exigido melhores condições de trabalho antes de se demitirem.",
        "sinônimo": ["verlangen", "anfordern"],
        "perfekt": "hat gefordert",
        "präteritum": "forderte",
        "regência": "fordern + Akkusativ",
        "outra_frase": "Wenn die Gewerkschaft höhere Löhne verlangt hätte, wären die Verhandlungen anders verlaufen.",
        "tradução_outra_frase": "Se o sindicato tivesse exigido salários mais altos, as negociações teriam sido diferentes.",
        "reflexivo": False
    },
    {
        "verbo": "einleiten",
        "tradução": "iniciar",
        "frase": "Die Reformen hätten früher eingeleitet werden müssen, um die Krise zu verhindern.",
        "tradução_frase": "As reformas deveriam ter sido iniciadas antes para evitar a crise.",
        "sinônimo": ["beginnen", "starten"],
        "perfekt": "hat eingeleitet",
        "präteritum": "leitete ein",
        "regência": "einleiten + Akkusativ",
        "outra_frase": "Wenn die Regierung die Maßnahmen rechtzeitig gestartet hätte, wäre die Wirtschaft stabiler geblieben.",
        "tradução_outra_frase": "Se o governo tivesse iniciado as medidas a tempo, a economia teria permanecido mais estável.",
        "reflexivo": False
    },
    {
        "verbo": "entwickeln",
        "tradução": "desenvolver",
        "frase": "Ein neues Impfstoff hätte schneller entwickelt werden können, wenn die Forschung besser finanziert worden wäre.",
        "tradução_frase": "Uma nova vacina poderia ter sido desenvolvida mais rapidamente se a pesquisa tivesse sido melhor financiada.",
        "sinônimo": ["erschaffen", "gestalten"],
        "perfekt": "hat entwickelt",
        "präteritum": "entwickelte",
        "regência": "entwickeln + Akkusativ",
        "outra_frase": "Hätte die Regierung die Forschung besser gestaltet, wären die Ergebnisse schneller verfügbar gewesen.",
        "tradução_outra_frase": "Se o governo tivesse moldado melhor a pesquisa, os resultados teriam sido disponibilizados mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "vereinfachen",
        "tradução": "simplificar",
        "frase": "Das Verfahren hätte vereinfacht werden sollen, um die Bearbeitungszeit zu verkürzen.",
        "tradução_frase": "O procedimento deveria ter sido simplificado para reduzir o tempo de processamento.",
        "sinônimo": ["erleichtern", "klären"],
        "perfekt": "hat vereinfacht",
        "präteritum": "vereinfachte",
        "regência": "vereinfachen + Akkusativ",
        "outra_frase": "Wenn die Schritte klarer erklärt worden wären, hätte der Prozess schneller abgeschlossen werden können.",
        "tradução_outra_frase": "Se os passos tivessem sido explicados mais claramente, o processo poderia ter sido concluído mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "bestätigen",
        "tradução": "confirmar",
        "frase": "Die Einladung hätte bestätigt werden sollen, damit die Organisation rechtzeitig abgeschlossen werden konnte.",
        "tradução_frase": "O convite deveria ter sido confirmado para que a organização pudesse ser concluída a tempo.",
        "sinônimo": ["anerkennen", "bekräftigen"],
        "perfekt": "hat bestätigt",
        "präteritum": "bestätigte",
        "regência": "bestätigen + Akkusativ",
        "outra_frase": "Wenn die Teilnahme bekräftigt worden wäre, hätte die Planung reibungsloser funktioniert.",
        "tradução_outra_frase": "Se a participação tivesse sido confirmada, o planejamento teria funcionado de forma mais eficiente.",
        "reflexivo": False
    },
    {
        "verbo": "betonen",
        "tradução": "enfatizar",
        "frase": "Der Redner hätte die Wichtigkeit des Projekts stärker betonen sollen, um die Zustimmung der Teilnehmer zu gewinnen.",
        "tradução_frase": "O palestrante deveria ter enfatizado mais a importância do projeto para obter a aprovação dos participantes.",
        "sinônimo": ["unterstreichen", "hervorheben"],
        "perfekt": "hat betont",
        "präteritum": "betonte",
        "regência": "betonen + Akkusativ",
        "outra_frase": "Hätte er die Argumente besser unterstrichen, wäre die Diskussion überzeugender gewesen.",
        "tradução_outra_frase": "Se ele tivesse enfatizado melhor os argumentos, a discussão teria sido mais convincente.",
        "reflexivo": False
    },
    {
        "verbo": "vermehren",
        "tradução": "aumentar (multiplicar)",
        "frase": "Die Produktion hätte vermehrt werden können, wenn die Ressourcen effizienter genutzt worden wären.",
        "tradução_frase": "A produção poderia ter sido aumentada se os recursos tivessem sido utilizados de forma mais eficiente.",
        "sinônimo": ["erhöhen", "ausweiten"],
        "perfekt": "hat vermehrt",
        "präteritum": "vermehrte",
        "regência": "vermehren + Akkusativ",
        "outra_frase": "Wenn die Investitionen ausgeweitet worden wären, hätte die Wirtschaft schneller wachsen können.",
        "tradução_outra_frase": "Se os investimentos tivessem sido ampliados, a economia poderia ter crescido mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "abschließen",
        "tradução": "concluir",
        "frase": "Das Projekt hätte früher abgeschlossen werden können, wenn die Zusammenarbeit besser funktioniert hätte.",
        "tradução_frase": "O projeto poderia ter sido concluído antes se a colaboração tivesse funcionado melhor.",
        "sinônimo": ["beenden", "vollenden"],
        "perfekt": "hat abgeschlossen",
        "präteritum": "schloss ab",
        "regência": "abschließen + Akkusativ",
        "outra_frase": "Wenn das Team die Planung rechtzeitig vollendet hätte, wäre das Ergebnis erfolgreicher gewesen.",
        "tradução_outra_frase": "Se a equipe tivesse concluído o planejamento a tempo, o resultado teria sido mais bem-sucedido.",
        "reflexivo": False
    },
    {
        "verbo": "nachweisen",
        "tradução": "comprovar",
        "frase": "Er hätte seine Qualifikationen nachweisen müssen, bevor er für die Stelle ausgewählt wurde.",
        "tradução_frase": "Ele deveria ter comprovado suas qualificações antes de ser selecionado para o cargo.",
        "sinônimo": ["belegen", "beweisen"],
        "perfekt": "hat nachgewiesen",
        "präteritum": "wies nach",
        "regência": "nachweisen + Akkusativ",
        "outra_frase": "Wenn er die notwendigen Dokumente rechtzeitig vorgelegt hätte, wäre die Auswahl einfacher gewesen.",
        "tradução_outra_frase": "Se ele tivesse apresentado os documentos necessários a tempo, a seleção teria sido mais simples.",
        "reflexivo": False
    },
    {
        "verbo": "erteilen",
        "tradução": "conceder",
        "frase": "Die Genehmigung hätte früher erteilt werden müssen, damit die Bauarbeiten rechtzeitig beginnen konnten.",
        "tradução_frase": "A autorização deveria ter sido concedida antes para que as obras pudessem começar a tempo.",
        "sinônimo": ["gewähren", "geben"],
        "perfekt": "hat erteilt",
        "präteritum": "erteilte",
        "regência": "erteilen + Akkusativ",
        "outra_frase": "Wenn die Erlaubnis rechtzeitig gewährt worden wäre, hätte das Projekt früher starten können.",
        "tradução_outra_frase": "Se a autorização tivesse sido concedida a tempo, o projeto poderia ter começado mais cedo.",
        "reflexivo": False
    },
    {
        "verbo": "beanstanden",
        "tradução": "contestar",
        "frase": "Die Kunden hätten die Qualität der Produkte früher beanstanden sollen, um rechtzeitig eine Lösung zu finden.",
        "tradução_frase": "Os clientes deveriam ter contestado a qualidade dos produtos antes para encontrar uma solução a tempo.",
        "sinônimo": ["kritisieren", "bemängeln"],
        "perfekt": "hat beanstandet",
        "präteritum": "beanstandete",
        "regência": "beanstanden + Akkusativ",
        "outra_frase": "Wenn die Mängel rechtzeitig bemängelt worden wären, hätte die Firma schneller reagieren können.",
        "tradução_outra_frase": "Se os defeitos tivessem sido contestados a tempo, a empresa poderia ter reagido mais rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "integrieren",
        "tradução": "integrar",
        "frase": "Viele Migranten bemühen sich, sich erfolgreich in die Gesellschaft zu integrieren.",
        "tradução_frase": "Muitos migrantes se esforçam para se integrar com sucesso na sociedade.",
        "sinônimo": ["einfügen", "einbinden"],
        "perfekt": "hat integriert",
        "präteritum": "integrierte",
        "regência": "integrieren + Dativ",
        "outra_frase": "Die Schule organisiert spezielle Programme, um neu angekommene Kinder einzubinden.",
        "tradução_outra_frase": "A escola organiza programas especiais para integrar crianças recém-chegadas.",
        "reflexivo": False
    },
    {
        "verbo": "auswandern",
        "tradução": "emigrar",
        "frase": "Viele Menschen wandern aus wirtschaftlichen oder politischen Gründen aus.",
        "tradução_frase": "Muitas pessoas emigraram por razões econômicas ou políticas.",
        "sinônimo": ["migrieren", "verlassen"],
        "perfekt": "ist ausgewandert",
        "präteritum": "wanderte aus",
        "regência": "auswandern (intransitiv)",
        "outra_frase": "Einige Familien entscheiden sich, in ein anderes Land zu migrieren.",
        "tradução_outra_frase": "Algumas famílias decidem emigrar para outro país.",
        "reflexivo": False
    },
    {
        "verbo": "einwandern",
        "tradução": "imigrar",
        "frase": "Jedes Jahr wandern Tausende in ein neues Land ein, um bessere Chancen zu finden.",
        "tradução_frase": "Todos os anos, milhares imigram para um novo país em busca de melhores oportunidades.",
        "sinônimo": ["immigrieren", "einreisen"],
        "perfekt": "ist eingewandert",
        "präteritum": "wanderte ein",
        "regência": "einwandern (intransitiv)",
        "outra_frase": "Die Regierung ermutigt qualifizierte Fachkräfte, in das Land einzureisen.",
        "tradução_outra_frase": "O governo incentiva profissionais qualificados a imigrar para o país.",
        "reflexivo": False
    },
    {
        "verbo": "vernetzen",
        "tradução": "conectar, interligar",
        "frase": "Kulturelle Institutionen vernetzen sich, um den Austausch zwischen verschiedenen Kulturen zu fördern.",
        "tradução_frase": "Instituições culturais se conectam para promover a troca entre diferentes culturas.",
        "sinônimo": ["verbinden", "kooperieren"],
        "perfekt": "hat vernetzt",
        "präteritum": "vernetzte",
        "regência": "vernetzen + Akkusativ",
        "outra_frase": "Soziale Netzwerke verbinden Menschen über Ländergrenzen hinweg.",
        "tradução_outra_frase": "Redes sociais conectam pessoas através das fronteiras dos países.",
        "reflexivo": False
    },
    {
        "verbo": "teilnehmen",
        "tradução": "participar",
        "frase": "Viele Migranten nehmen an interkulturellen Workshops teil, um die Sprache zu lernen.",
        "tradução_frase": "Muitos migrantes participam de oficinas interculturais para aprender o idioma.",
        "sinônimo": ["mitmachen", "partizipieren"],
        "perfekt": "hat teilgenommen",
        "präteritum": "nahm teil",
        "regência": "teilnehmen an + Dativ",
        "outra_frase": "Die Schüler partizipieren an einem Austauschprogramm, das die kulturelle Vielfalt betont.",
        "tradução_outra_frase": "Os alunos participam de um programa de intercâmbio que enfatiza a diversidade cultural.",
        "reflexivo": False
    },
    {
        "verbo": "engagieren",
        "tradução": "engajar-se, dedicar-se",
        "frase": "Viele Freiwillige engagieren sich in Integrationsprojekten, um die kulturelle Vielfalt zu unterstützen.",
        "tradução_frase": "Muitos voluntários se engajam em projetos de integração para apoiar a diversidade cultural.",
        "sinônimo": ["sich einsetzen", "mitwirken"],
        "perfekt": "hat sich engagiert",
        "präteritum": "engagierte sich",
        "regência": "sich engagieren in + Dativ",
        "outra_frase": "Die Gemeinschaft setzt sich aktiv für die Rechte von Migranten ein.",
        "tradução_outra_frase": "A comunidade se engaja ativamente pelos direitos dos migrantes.",
        "reflexivo": True
    },
    {
        "verbo": "einleben",
        "tradução": "estabelecer-se, adaptar-se",
        "frase": "Neueinwanderer brauchen Zeit, um sich in der neuen Umgebung einleben zu können.",
        "tradução_frase": "Os recém-chegados precisam de tempo para se estabelecer na nova região.",
        "sinônimo": ["sich niederlassen", "sich ansiedeln"],
        "perfekt": "hat sich eingelebt",
        "präteritum": "lebte sich ein",
        "regência": "sich einleben in + Dativ",
        "outra_frase": "Mit Unterstützung der Gemeinde können sich Migranten schneller niederlassen.",
        "tradução_outra_frase": "Com o apoio da comunidade, os migrantes podem se adaptar mais rapidamente.",
        "reflexivo": True
    },
    {
        "verbo": "feiern",
        "tradução": "celebrar",
        "frase": "Viele Städte feiern kulturelle Feste, um die Vielfalt ihrer Bevölkerung zu würdigen.",
        "tradução_frase": "Muitas cidades celebram festivais culturais para homenagear a diversidade de sua população.",
        "sinônimo": ["zelebrieren", "begehen"],
        "perfekt": "hat gefeiert",
        "präteritum": "feierte",
        "regência": "feiern + Akkusativ (optional)",
        "outra_frase": "Das gemeinsame zelebrieren stärkt das Miteinander in einer multikulturellen Gesellschaft.",
        "tradução_outra_frase": "Celebrar em conjunto fortalece a convivência em uma sociedade multicultural.",
        "reflexivo": False
    },
    {
        "verbo": "kooperieren",
        "tradução": "cooperar",
        "frase": "Internationale Organisationen kooperieren, um die Herausforderungen der Migration anzugehen.",
        "tradução_frase": "Organizações internacionais cooperam para enfrentar os desafios da migração.",
        "sinônimo": ["zusammenarbeiten", "mitarbeiten"],
        "perfekt": "hat kooperiert",
        "präteritum": "kooperierte",
        "regência": "kooperieren mit + Dativ",
        "outra_frase": "Lokale Behörden arbeiten mit NGOs zusammen, um Integrationsprozesse zu verbessern.",
        "tradução_outra_frase": "Autoridades locais cooperam com ONGs para melhorar os processos de integração.",
        "reflexivo": False
    },
    {
        "verbo": "fördern",
        "tradução": "promover, incentivar",
        "frase": "Staatliche Förderprogramme helfen, die Integration von Migranten zu fördern.",
        "tradução_frase": "Programas de apoio estatais ajudam a promover a integração dos migrantes.",
        "sinônimo": ["unterstützen", "anregen"],
        "perfekt": "hat gefördert",
        "präteritum": "förderte",
        "regência": "fördern + Akkusativ",
        "outra_frase": "Die Kulturzentren unterstützen den interkulturellen Dialog in der Stadt.",
        "tradução_outra_frase": "Os centros culturais promovem o diálogo intercultural na cidade.",
        "reflexivo": False
    },
    {
        "verbo": "akzeptieren",
        "tradução": "aceitar",
        "frase": "Eine offene Gesellschaft akzeptiert unterschiedliche kulturelle Hintergründe und Lebensweisen.",
        "tradução_frase": "Uma sociedade aberta aceita diferentes origens culturais e modos de vida.",
        "sinônimo": ["tolerieren", "dulden"],
        "perfekt": "hat akzeptiert",
        "präteritum": "akzeptierte",
        "regência": "akzeptieren + Akkusativ",
        "outra_frase": "Die Menschen lernen, neue Traditionen zu tolerieren und zu schätzen.",
        "tradução_outra_frase": "As pessoas aprendem a aceitar e valorizar novas tradições.",
        "reflexivo": False
    },
    {
        "verbo": "vermitteln",
        "tradução": "mediar, übertragen",
        "frase": "Soziale Projekte vermitteln Brücken zwischen verschiedenen Kulturen.",
        "tradução_frase": "Projetos sociais constroem pontes entre diferentes culturas.",
        "sinônimo": ["übermitteln", "verknüpfen"],
        "perfekt": "hat vermittelt",
        "präteritum": "vermittelte",
        "regência": "vermitteln zwischen + Dativ und Dativ",
        "outra_frase": "Kulturelle Veranstaltungen übermitteln Verständnis und Toleranz.",
        "tradução_outra_frase": "Eventos culturais transmitem compreensão e tolerância.",
        "reflexivo": False
    },
    {
        "verbo": "diversifizieren",
        "tradução": "diversificar",
        "frase": "Unternehmen diversifizieren ihre Belegschaft, um vielfältige Perspektiven zu integrieren.",
        "tradução_frase": "Empresas diversificam seu quadro de funcionários para integrar perspectivas variadas.",
        "sinônimo": ["variieren", "vervielfältigen"],
        "perfekt": "hat diversifiziert",
        "präteritum": "diversifizierte",
        "regência": "diversifizieren + Akkusativ",
        "outra_frase": "Die Kulturbranche vervielfältigt ihre Programme, um ein breiteres Publikum anzusprechen.",
        "tradução_outra_frase": "A indústria cultural diversifica seus programas para atrair um público mais amplo.",
        "reflexivo": False
    },
    {
        "verbo": "zusammenarbeiten",
        "tradução": "trabalhar junto, colaborar",
        "frase": "Verschiedene Gemeinschaften arbeiten zusammen, um integrative Projekte zu realisieren.",
        "tradução_frase": "Diferentes comunidades trabalham juntas para realizar projetos integradores.",
        "sinônimo": ["kooperieren", "zusammenwirken"],
        "perfekt": "hat zusammengearbeitet",
        "präteritum": "arbeitete zusammen",
        "regência": "zusammenarbeiten mit + Dativ",
        "outra_frase": "Das Zusammenwirken zwischen den Kulturen führt zu innovativen Lösungen.",
        "tradução_outra_frase": "A colaboração entre culturas leva a soluções inovadoras.",
        "reflexivo": False
    },
    {
        "verbo": "repräsentieren",
        "tradução": "representar",
        "frase": "Migranten repräsentieren einen bedeutenden Teil der modernen Gesellschaft.",
        "tradução_frase": "Os migrantes representam uma parte significativa da sociedade moderna.",
        "sinônimo": ["darstellen", "verkörpern"],
        "perfekt": "hat repräsentiert",
        "präteritum": "repräsentierte",
        "regência": "repräsentieren + Akkusativ",
        "outra_frase": "Die ausgewiesene Vielfalt verkörpert die offene Haltung des Landes.",
        "tradução_outra_frase": "A evidente diversidade representa a atitude aberta do país.",
        "reflexivo": False
    },
    {
        "verbo": "respektieren",
        "tradução": "respeitar",
        "frase": "Es ist wichtig, verschiedene kulturelle Traditionen zu respektieren.",
        "tradução_frase": "É importante respeitar diferentes tradições culturais.",
        "sinônimo": ["achten", "wertschätzen"],
        "perfekt": "hat respektiert",
        "präteritum": "respektierte",
        "regência": "respektieren + Akkusativ",
        "outra_frase": "Die Gesellschaft sollte Menschen und ihre Bräuche achten.",
        "tradução_outra_frase": "A sociedade deve respeitar as pessoas e seus costumes.",
        "reflexivo": False
    },
    {
        "verbo": "zusammenleben",
        "tradução": "conviver",
        "frase": "Das Zusammenleben verschiedener Kulturen bereichert die Gesellschaft.",
        "tradução_frase": "A convivência de diferentes culturas enriquece a sociedade.",
        "sinônimo": ["koexistieren", "miteinander leben"],
        "perfekt": "hat zusammengelebt",
        "präteritum": "lebte zusammen",
        "regência": "zusammenleben (intransitiv)",
        "outra_frase": "In vielen Metropolen koexistieren Menschen aus aller Welt.",
        "tradução_outra_frase": "Em muitas metrópoles, pessoas de todo o mundo convivem.",
        "reflexivo": False
    },
    {
        "verbo": "sensibilisieren",
        "tradução": "sensibilizar",
        "frase": "Bildungseinrichtungen sensibilisieren die Öffentlichkeit für interkulturelle Themen.",
        "tradução_frase": "Instituições educacionais sensibilizam o público para questões interculturais.",
        "sinônimo": ["bewusst machen"],
        "perfekt": "hat sensibilisiert",
        "präteritum": "sensibilisierte",
        "regência": "sensibilisieren für + Akkusativ",
        "outra_frase": "Die Kampagne macht die Menschen für die Herausforderungen der Migration bewusst.",
        "tradução_outra_frase": "A campanha conscientiza as pessoas para os desafios da migração.",
        "reflexivo": False
    },
    {
        "verbo": "umziehen",
        "tradução": "mudar de local",
        "frase": "Viele Familien ziehen um, wenn sie in ein neues Land migrieren.",
        "tradução_frase": "Muitas famílias se mudam quando migram para um novo país.",
        "sinônimo": ["wechseln", "verlegen"],
        "perfekt": "ist umgezogen",
        "präteritum": "zog um",
        "regência": "umziehen (intransitiv)",
        "outra_frase": "Der Umzug erleichtert oft den Wechsel in ein neues Leben.",
        "tradução_outra_frase": "A mudança frequentemente facilita o início de uma nova vida.",
        "reflexivo": False
    },
    {
        "verbo": "verbinden",
        "tradução": "conectar, unir",
        "frase": "Kulturelle Veranstaltungen verbinden Menschen unterschiedlicher Herkunft.",
        "tradução_frase": "Eventos culturais conectam pessoas de origens diferentes.",
        "sinônimo": ["verknüpfen", "zusammenführen"],
        "perfekt": "hat verbunden",
        "präteritum": "verband",
        "regência": "verbinden + Akkusativ",
        "outra_frase": "Gemeinsame Projekte verknüpfen Traditionen und Innovation.",
        "tradução_outra_frase": "Projetos conjuntos unem tradição e inovação.",
        "reflexivo": False
    },
    {
        "verbo": "verheiraten",
        "tradução": "casar",
        "frase": "Nach vielen gemeinsamen Jahren haben sich Anna und Markus im kleinen Kreis verheiratet und leben seitdem auf Wolke Sieben.",
        "tradução_frase": "Após muitos anos juntos, Anna e Markus se casaram em uma cerimônia íntima e desde então estão nas nuvens.",
        "sinônimo": ["heiraten", "ehelichen"],
        "perfekt": "hat verheiratet",
        "präteritum": "verheiratete",
        "regência": "verheiraten (reflexiv: sich verheiraten)",
        "outra_frase": "Viele Paare, die sich Hals über Kopf verlieben, entscheiden sich dafür, sich im letzten Moment ehelich zu verbinden.",
        "tradução_outra_frase": "Muitos casais que se apaixonam perdidamente optam por se casar de repente.",
        "reflexivo": True
    },
    {
        "verbo": "scheiden",
        "tradução": "divorciar",
        "frase": "Nach Jahren voller Streit und Missverständnissen entschieden sich die beiden, sich friedlich scheiden zu lassen.",
        "tradução_frase": "Após anos de brigas e mal-entendidos, os dois decidiram se divorciar amigavelmente.",
        "sinônimo": ["trennen", "auseinandergehen"],
        "perfekt": "hat geschieden",
        "präteritum": "scheidete",
        "regência": "sich scheiden lassen (reflexiv/passiv)",
        "outra_frase": "Manchmal ist es besser, getrennte Wege zu gehen, als in einer endlosen Zwickmühle zu verharren.",
        "tradução_outra_frase": "Às vezes é melhor seguir caminhos separados do que permanecer em um beco sem saída.",
        "reflexivo": True
    },
    {
        "verbo": "kümmern",
        "tradução": "cuidar",
        "frase": "Eltern kümmern sich liebevoll um ihre Kinder, auch wenn sie mal den Kopf in den Wolken haben.",
        "tradução_frase": "Os pais cuidam carinhosamente de seus filhos, mesmo quando estão distraídos.",
        "sinônimo": ["sich sorgen", "pflegen"],
        "perfekt": "hat sich gekümmert",
        "präteritum": "kümmerte sich",
        "regência": "sich kümmern um + Akkusativ",
        "outra_frase": "Oma und Opa kümmern sich nicht nur um die Enkel, sondern stehen auch beratend zur Seite, wenn’s mal brenzlig wird.",
        "tradução_outra_frase": "Avós não só cuidam dos netos, como também dão conselhos quando a situação fica complicada.",
        "reflexivo": True
    },
    {
        "verbo": "pflegen",
        "tradução": "cultivar (relações)",
        "frase": "In vielen Familien wird es großgeschrieben, Beziehungen zu pflegen und den Kontakt zu bewahren.",
        "tradução_frase": "Em muitas famílias, cultivar as relações e manter contato é algo valorizado.",
        "sinônimo": ["hegen", "aufrechterhalten"],
        "perfekt": "hat gepflegt",
        "präteritum": "pflegte",
        "regência": "pflegen + Akkusativ",
        "outra_frase": "Oma pflegt den Familientradition, indem sie jeden Sonntag zum gemeinsamen Mittagessen einlädt.",
        "tradução_outra_frase": "A avó cultiva a tradição familiar ao convidar todos para um almoço coletivo aos domingos.",
        "reflexivo": False
    },
    {
        "verbo": "vertrauen",
        "tradução": "confiar",
        "frase": "In einer guten Beziehung weiß man, dass man dem anderen blind vertrauen kann.",
        "tradução_frase": "Em um bom relacionamento, sabe-se que se pode confiar cegamente no outro.",
        "sinônimo": ["glauben", "sich verlassen"],
        "perfekt": "hat vertraut",
        "präteritum": "vertraute",
        "regência": "vertrauen + Dativ",
        "outra_frase": "Kinder lernen früh, ihren Eltern zu vertrauen, auch wenn diese manchmal mit offenen Karten spielen.",
        "tradução_outra_frase": "As crianças aprendem desde cedo a confiar em seus pais, mesmo quando estes agem de forma muito transparente.",
        "reflexivo": False
    },
    {
        "verbo": "ermutigen",
        "tradução": "encorajar",
        "frase": "Eltern ermutigen ihre Kinder stets dazu, den eigenen Weg zu gehen und Fehler als Chance zu sehen.",
        "tradução_frase": "Os pais sempre encorajam seus filhos a seguirem seus próprios caminhos e verem os erros como oportunidades.",
        "sinônimo": ["anfeuern", "motivieren"],
        "perfekt": "hat ermutigt",
        "präteritum": "ermutigte",
        "regência": "ermutigen + Akkusativ",
        "outra_frase": "O Onkel ermutigt seine Nichten, nicht immer den Kopf in den Sand zu stecken, sondern sich den Herausforderungen zu stellen.",
        "tradução_outra_frase": "O tio encoraja suas sobrinhas a não ignorarem os problemas, mas enfrentá-los de frente.",
        "reflexivo": False
    },
    {
        "verbo": "verzeihen",
        "tradução": "perdoar",
        "frase": "In jeder Familie kommt es vor, dass man sich mal in die Quere kommt – wichtig ist, sich gegenseitig zu verzeihen.",
        "tradução_frase": "Em toda família, às vezes há desentendimentos – o importante é perdoar um ao outro.",
        "sinônimo": ["nachsehen", "entschuldigen"],
        "perfekt": "hat verziehen",
        "präteritum": "verzieh",
        "regência": "verzeihen + Dativ",
        "outra_frase": "Auch wenn man sich manchmal in die Haare kriegt, lernt man, über Kleinigkeiten hinwegzusehen und zu verzeihen.",
        "tradução_outra_frase": "Mesmo quando há discussões, aprende-se a perdoar e deixar as pequenas coisas para trás.",
        "reflexivo": False
    },
    {
        "verbo": "treffen",
        "tradução": "encontrar",
        "frase": "Familientreffen finden oft im Kreise der Großeltern statt, wo sich alle Generationen zusammenfinden.",
        "tradução_frase": "Encontros familiares geralmente acontecem com a presença dos avós, onde todas as gerações se reúnem.",
        "sinônimo": ["begegnen", "zusammenkommen"],
        "perfekt": "hat getroffen",
        "präteritum": "traf",
        "regência": "treffen + Akkusativ",
        "outra_frase": "Am Sonntag treffen sich alle Verwandten – ein Tag, an dem man den Ball flach halten und einfach genießen kann.",
        "tradução_outra_frase": "No domingo, todos os parentes se encontram – um dia para manter a calma e simplesmente aproveitar o momento.",
        "reflexivo": False
    },
    {
        "verbo": "zusammenkommen",
        "tradução": "reunir, juntar",
        "frase": "Zu besonderen Anlässen kommt die ganze Familie zusammen, um gemeinsam zu feiern.",
        "tradução_frase": "Em ocasiões especiais, toda a família se reúne para celebrar em conjunto.",
        "sinônimo": ["sich versammeln", "sich treffen"],
        "perfekt": "ist zusammengekommen",
        "präteritum": "kam zusammen",
        "regência": "zusammenkommen (intransitiv)",
        "outra_frase": "Bei Familienfesten kommen oft alle Generationen zusammen, was das Herz erwärmt und die Seele streichelt.",
        "tradução_outra_frase": "Em festas familiares, todas as gerações se reúnem, aquecendo o coração e acariciando a alma.",
        "reflexivo": False
    },
    {
        "verbo": "auseinanderleben",
        "tradução": "viver separados",
        "frase": "Manchmal entwickeln sich Familienmitglieder so unterschiedlich, dass sie anfangen, auseinanderzuleben.",
        "tradução_frase": "Às vezes, os membros da família se desenvolvem de forma tão diferente que começam a viver separados.",
        "sinônimo": ["sich entfremden", "auseinanderdriften"],
        "perfekt": "hat auseinandergelebt",
        "präteritum": "lebte auseinander",
        "regência": "auseinanderleben (intransitiv)",
        "outra_frase": "Wenn sich die Lebenswege trennen, leben manche einfach auseinander, ohne dass der Kontakt völlig abbricht.",
        "tradução_outra_frase": "Quando os caminhos se separam, alguns passam a viver de maneira distinta, sem que o contato seja totalmente perdido.",
        "reflexivo": False
    },
    {
        "verbo": "auseinandergehen",
        "tradução": "se separar",
        "frase": "In manchen Beziehungen gehen die Wege auseinander, was oft schmerzhaft, aber unvermeidlich ist.",
        "tradução_frase": "Em alguns relacionamentos, os caminhos se separam, o que muitas vezes é doloroso, mas inevitável.",
        "sinônimo": ["sich trennen", "scheiden"],
        "perfekt": "ist auseinandergegangen",
        "präteritum": "ging auseinander",
        "regência": "auseinandergehen (intransitiv)",
        "outra_frase": "Wenn sich Lebensziele nicht mehr decken, gehen die Partner manchmal auseinander wie Tag und Nacht.",
        "tradução_outra_frase": "Quando os objetivos de vida não se alinham, os parceiros às vezes se separam como o dia da noite.",
        "reflexivo": False
    },
    {
        "verbo": "annähern",
        "tradução": "aproximar-se",
        "frase": "Nach einer langen Entfremdung versuchen Geschwister, sich wieder anzunähern und alte Zeiten aufleben zu lassen.",
        "tradução_frase": "Após um longo período de afastamento, os irmãos tentam se aproximar novamente e reviver os velhos tempos.",
        "sinônimo": ["sich nähern", "sich rücken"],
        "perfekt": "hat sich angenähert",
        "präteritum": "näherte sich an",
        "regência": "sich annähern (intransitiv)",
        "outra_frase": "Manchmal muss man über den eigenen Schatten springen, um sich wieder anzunähern und die familiären Bande zu erneuern.",
        "tradução_outra_frase": "Às vezes é preciso superar as próprias reservas para se aproximar novamente e renovar os laços familiares.",
        "reflexivo": True
    },
    {
        "verbo": "festigen",
        "tradução": "consolidar, fortalecer",
        "frase": "Gemeinsame Erlebnisse festigen das Vertrauen und die Bindung innerhalb der Familie.",
        "tradução_frase": "Experiências compartilhadas consolidam a confiança e os laços dentro da família.",
        "sinônimo": ["stärken", "kräften"],
        "perfekt": "hat gefestigt",
        "präteritum": "festigte",
        "regência": "festigen + Akkusativ",
        "outra_frase": "Ein Familienausflug kann Wunder wirken und die Beziehungen auf solide Beine stellen.",
        "tradução_outra_frase": "Uma viagem em família pode fazer maravilhas e solidificar as relações.",
        "reflexivo": False
    },
    {
        "verbo": "versöhnen",
        "tradução": "reconciliar",
        "frase": "Nach einem heftigen Streit bemühten sich die Geschwister, ihre Differenzen zu versöhnen und wieder zusammenzufinden.",
        "tradução_frase": "Após uma briga intensa, os irmãos se esforçaram para se reconciliar e voltar a se unir.",
        "sinônimo": ["sich versöhnen", "frieden schließen"],
        "perfekt": "hat versöhnt",
        "präteritum": "versöhnte",
        "regência": "versöhnen + Akkusativ",
        "outra_frase": "Manchmal ist es schwer, den Groll fallen zu lassen, aber echte Liebe versöhnt selbst die größten Konflikte.",
        "tradução_outra_frase": "Às vezes é difícil deixar o ressentimento de lado, mas o amor verdadeiro reconcilia até os maiores conflitos.",
        "reflexivo": False
    },
    {
        "verbo": "zuhören",
        "tradução": "ouvir",
        "frase": "Eltern sollten ihren Kindern immer gut zuhören, um ihre Sorgen und Wünsche zu verstehen.",
        "tradução_frase": "Os pais devem sempre ouvir bem os filhos para entender suas preocupações e desejos.",
        "sinônimo": ["hören", "aufmerksam sein"],
        "perfekt": "hat zugehört",
        "präteritum": "hörte zu",
        "regência": "zuhören (intransitiv, meist mit Dativ: jemandem zuhören)",
        "outra_frase": "In stressigen Zeiten ist es Gold wert, wenn man einfach mal ein offenes Ohr füreinander hat.",
        "tradução_outra_frase": "Em tempos de estresse, ter alguém que ouça de verdade é inestimável.",
        "reflexivo": False
    },
    {
        "verbo": "organisieren",
        "tradução": "organizar",
        "frase": "Die Familie organisiert jedes Jahr ein großes Wiedersehen, bei dem alle Verwandten zusammenkommen.",
        "tradução_frase": "A família organiza todo ano uma grande reunião, onde todos os parentes se encontram.",
        "sinônimo": ["planen", "arrangieren"],
        "perfekt": "hat organisiert",
        "präteritum": "organisierte",
        "regência": "organisieren + Akkusativ",
        "outra_frase": "Ein gut organisiertes Familientreffen sorgt dafür, dass niemand auf dem Schlauch steht und alle bestens informiert sind.",
        "tradução_outra_frase": "Uma reunião familiar bem organizada garante que ninguém fique por fora e todos estejam bem informados.",
        "reflexivo": False
    },
    {
        "verbo": "einigen",
        "tradução": "chegar a um acordo",
        "frase": "Nach langen Diskussionen konnten sich die Familienmitglieder endlich auf einen Kompromiss einigen.",
        "tradução_frase": "Após longas discussões, os membros da família finalmente chegaram a um acordo.",
        "sinônimo": ["sich arrangieren", "übereinkommen"],
        "perfekt": "hat sich geeinigt",
        "präteritum": "einigte sich",
        "regência": "sich einigen auf + Akkusativ",
        "outra_frase": "Auch wenn man sich manchmal in den Haaren liegt, findet man oft einen Weg, sich zu einigen und weiterzumachen.",
        "tradução_outra_frase": "Mesmo quando há atritos, frequentemente se encontra uma forma de chegar a um acordo e seguir em frente.",
        "reflexivo": True
    },
    {
        "verbo": "erziehen",
        "tradução": "educar",
        "frase": "Eltern erziehen ihre Kinder mit viel Liebe, aber auch mit klaren Grenzen, um ihnen den Weg ins Leben zu ebnen.",
        "tradução_frase": "Os pais educam seus filhos com muito amor, mas também com limites claros, para prepará-los para a vida.",
        "sinônimo": ["aufziehen", "bilden"],
        "perfekt": "hat erzogen",
        "präteritum": "erzog",
        "regência": "erziehen + Akkusativ",
        "outra_frase": "Manchmal muss man auch mal die Zügel in die Hand nehmen, um die Kinder richtig zu erziehen.",
        "tradução_outra_frase": "Às vezes é preciso tomar firme o controle para educar bem as crianças.",
        "reflexivo": False
    },
    {
        "verbo": "anvertrauen",
        "tradução": "confiar (segredos)",
        "frase": "In einer engen Beziehung kann man sich all seine Sorgen an den anderen anvertrauen.",
        "tradução_frase": "Em um relacionamento próximo, pode-se confiar todos os segredos ao outro.",
        "sinônimo": ["vertrauen", "anvertrauen"],
        "perfekt": "hat anvertraut",
        "präteritum": "anvertraute",
        "regência": "anvertrauen + Akkusativ",
        "outra_frase": "Es ist nicht immer leicht, das Herz aufzumachen, aber man muss manchmal den Schritt wagen und sich anvertrauen.",
        "tradução_outra_frase": "Nem sempre é fácil se abrir, mas às vezes é necessário dar o passo e confiar os sentimentos.",
        "reflexivo": False
    },
    {
        "verbo": "analysieren",
        "tradução": "analisar",
        "frase": "Wissenschaftler analysieren komplexe Datensätze, um Muster in den Ergebnissen zu erkennen.",
        "tradução_frase": "Cientistas analisam conjuntos de dados complexos para identificar padrões nos resultados.",
        "sinônimo": ["untersuchen", "auswerten"],
        "perfekt": "hat analysiert",
        "präteritum": "analysierte",
        "regência": "analysieren + Akkusativ",
        "outra_frase": "Im Seminar mussten die Studierenden einen Fallbericht analysieren, um die Ursachen eines Phänomens zu verstehen.",
        "tradução_outra_frase": "No seminário, os alunos tiveram que analisar um estudo de caso para compreender as causas de um fenômeno.",
        "reflexivo": False
    },
    {
        "verbo": "interpretieren",
        "tradução": "interpretar",
        "frase": "Die Historiker interpretieren alte Texte, um die Denkweise vergangener Kulturen zu rekonstruieren.",
        "tradução_frase": "Os historiadores interpretam textos antigos para reconstruir a mentalidade de culturas passadas.",
        "sinônimo": ["deuten", "erklären"],
        "perfekt": "hat interpretiert",
        "präteritum": "interpretierte",
        "regência": "interpretieren + Akkusativ",
        "outra_frase": "Im Literaturkurs lernten die Studenten, Gedichte zu interpretieren und deren versteckte Bedeutungen zu entschlüsseln.",
        "tradução_outra_frase": "No curso de literatura, os estudantes aprenderam a interpretar poemas e decifrar seus significados ocultos.",
        "reflexivo": False
    },
    {
        "verbo": "erörtern",
        "tradução": "discutir, debater",
        "frase": "In der Vorlesung erörterten die Professoren die Auswirkungen der Globalisierung auf die Gesellschaft.",
        "tradução_frase": "Na palestra, os professores debateram os impactos da globalização na sociedade.",
        "sinônimo": ["diskutieren", "besprechen"],
        "perfekt": "hat erörtert",
        "präteritum": "erörterte",
        "regência": "erörtern + Akkusativ",
        "outra_frase": "Im Kolloquium wurde das Thema kontrovers erörtert, sodass viele neue Perspektiven entstanden.",
        "tradução_outra_frase": "No colóquio, o tema foi debatido de forma controversa, gerando muitas novas perspectivas.",
        "reflexivo": False
    },
    {
        "verbo": "theoretisieren",
        "tradução": "teorizar",
        "frase": "Forschende theoretisieren häufig, bevor sie empirische Studien durchführen.",
        "tradução_frase": "Pesquisadores frequentemente teoriam antes de realizar estudos empíricos.",
        "sinônimo": ["hypothetisieren", "konzipieren"],
        "perfekt": "hat theoretisiert",
        "präteritum": "theoretisierte",
        "regência": "theoretisieren (intransitiv)",
        "outra_frase": "In Workshops wird oft über zukünftige Entwicklungen theoretisiert, um innovative Lösungsansätze zu finden.",
        "tradução_outra_frase": "Em workshops, frequentemente se teoriza sobre desenvolvimentos futuros para encontrar soluções inovadoras.",
        "reflexivo": False
    },
    {
        "verbo": "experimentieren",
        "tradução": "experimentar",
        "frase": "In den Naturwissenschaften experimentieren Forscher mit verschiedenen Variablen, um Hypothesen zu überprüfen.",
        "tradução_frase": "Nas ciências naturais, os pesquisadores experimentam com diferentes variáveis para testar hipóteses.",
        "sinônimo": ["testen", "ausprobieren"],
        "perfekt": "hat experimentiert",
        "präteritum": "experimentierte",
        "regência": "experimentieren (intransitiv)",
        "outra_frase": "Im Labor experimentierten die Studierenden mit verschiedenen chemischen Lösungen, um Reaktionsmuster zu erkennen.",
        "tradução_outra_frase": "No laboratório, os alunos experimentaram diversas soluções químicas para identificar padrões de reação.",
        "reflexivo": False
    },
    {
        "verbo": "erforschen",
        "tradução": "pesquisar, explorar",
        "frase": "Die Archäologen erforschen antike Stätten, um mehr über vergangene Zivilisationen zu erfahren.",
        "tradução_frase": "Os arqueólogos pesquisam sítios antigos para saber mais sobre civilizações passadas.",
        "sinônimo": ["untersuchen", "studieren"],
        "perfekt": "hat erforscht",
        "präteritum": "erforschte",
        "regência": "erforschen (intransitiv)",
        "outra_frase": "An Universitäten wird intensiv erforscht, wie sich soziale Strukturen im Laufe der Zeit verändern.",
        "tradução_outra_frase": "Nas universidades, pesquisa-se intensivamente como as estruturas sociais mudam ao longo do tempo.",
        "reflexivo": False
    },
    {
        "verbo": "quantifizieren",
        "tradução": "quantificar",
        "frase": "In der Soziologie quantifizieren Wissenschaftler oft subjektive Eindrücke mit Hilfe von Umfragen.",
        "tradução_frase": "Na sociologia, os cientistas frequentemente quantificam impressões subjetivas por meio de pesquisas.",
        "sinônimo": ["vermessen", "messen"],
        "perfekt": "hat quantifiziert",
        "präteritum": "quantifizierte",
        "regência": "quantifizieren + Akkusativ",
        "outra_frase": "Die exakte Messung von Daten hilft, soziale Phänomene zu quantifizieren und besser zu verstehen.",
        "tradução_outra_frase": "A medição precisa de dados ajuda a quantificar fenômenos sociais e a compreendê-los melhor.",
        "reflexivo": False
    },
    {
        "verbo": "konzipieren",
        "tradução": "conceber, planejar",
        "frase": "Ingenieure konzipieren innovative Modelle, die zur Lösung aktueller technischer Probleme beitragen.",
        "tradução_frase": "Engenheiros concebem modelos inovadores que contribuem para a resolução de problemas técnicos atuais.",
        "sinônimo": ["entwerfen", "planen"],
        "perfekt": "hat konzipiert",
        "präteritum": "konzipierte",
        "regência": "konzipieren + Akkusativ",
        "outra_frase": "Im Forschungsprojekt konzipierten die Wissenschaftler ein neues Experiment, um ihre Theorie zu überprüfen.",
        "tradução_outra_frase": "No projeto de pesquisa, os cientistas conceberam um novo experimento para testar sua teoria.",
        "reflexivo": False
    },
    {
        "verbo": "evaluieren",
        "tradução": "avaliar",
        "frase": "Nach Abschluss des Experiments evaluieren die Forscher die Ergebnisse, um deren Aussagekraft zu beurteilen.",
        "tradução_frase": "Após o término do experimento, os pesquisadores avaliam os resultados para julgar sua relevância.",
        "sinônimo": ["bewerten", "abschätzen"],
        "perfekt": "hat evaluiert",
        "präteritum": "evaluierte",
        "regência": "evaluieren + Akkusativ",
        "outra_frase": "In interdisziplinären Studien evaluieren Experten verschiedene Datenquellen, um fundierte Schlüsse zu ziehen.",
        "tradução_outra_frase": "Em estudos interdisciplinares, especialistas avaliam diversas fontes de dados para tirar conclusões fundamentadas.",
        "reflexivo": False
    },
    {
        "verbo": "systematisieren",
        "tradução": "sistematizar",
        "frase": "Die Ergebnisse der Studie wurden sorgfältig systematisiert, um Trends besser sichtbar zu machen.",
        "tradução_frase": "Os resultados do estudo foram cuidadosamente sistematizados para evidenciar melhor as tendências.",
        "sinônimo": ["ordnen", "strukturieren"],
        "perfekt": "hat systematisiert",
        "präteritum": "systematisierte",
        "regência": "systematisieren + Akkusativ",
        "outra_frase": "In wissenschaftlichen Arbeiten ist es oft hilfreich, komplexe Informationen zu systematisieren.",
        "tradução_outra_frase": "Em trabalhos acadêmicos, frequentemente é útil sistematizar informações complexas.",
        "reflexivo": False
    },
    {
        "verbo": "modellieren",
        "tradução": "modelar",
        "frase": "Forscher modellieren reale Prozesse, um sie in Simulationen zu untersuchen.",
        "tradução_frase": "Pesquisadores modelam processos reais para estudá-los em simulações.",
        "sinônimo": ["abbilden", "nachbilden"],
        "perfekt": "hat modelliert",
        "präteritum": "modellierte",
        "regência": "modellieren + Akkusativ",
        "outra_frase": "Die Mathematiker modellierten das Wachstum der Population mithilfe komplexer Gleichungen.",
        "tradução_outra_frase": "Os matemáticos modelaram o crescimento populacional utilizando equações complexas.",
        "reflexivo": False
    },
    {
        "verbo": "validieren",
        "tradução": "validar",
        "frase": "Bevor eine Theorie anerkannt wird, muss sie durch unabhängige Studien validiert werden.",
        "tradução_frase": "Antes de uma teoria ser aceita, ela precisa ser validada por estudos independentes.",
        "sinônimo": ["bestätigen", "verifizieren"],
        "perfekt": "hat validiert",
        "präteritum": "validierte",
        "regência": "validieren + Akkusativ",
        "outra_frase": "Die Ergebnisse des Experiments wurden mehrfach validiert, um ihre Zuverlässigkeit sicherzustellen.",
        "tradução_outra_frase": "Os resultados do experimento foram validados diversas vezes para garantir sua confiabilidade.",
        "reflexivo": False
    },
    {
        "verbo": "debattieren",
        "tradução": "debater",
        "frase": "In den Sozialwissenschaften debattieren Experten über die Ursachen gesellschaftlicher Phänomene.",
        "tradução_frase": "Nas ciências sociais, especialistas debatem as causas de fenômenos sociais.",
        "sinônimo": ["diskutieren", "erörtern"],
        "perfekt": "hat debattiert",
        "präteritum": "debattierte",
        "regência": "debattieren (intransitiv)",
        "outra_frase": "In runden Tischen debattierten die Wissenschaftler leidenschaftlich über Lösungsansätze.",
        "tradução_outra_frase": "Em mesas-redondas, os cientistas debateram apaixonadamente possíveis soluções.",
        "reflexivo": False
    },
    {
        "verbo": "veranschaulichen",
        "tradução": "ilustrar, exemplificar",
        "frase": "Dozenten veranschaulichen komplexe Theorien oft anhand praktischer Beispiele.",
        "tradução_frase": "Professores frequentemente ilustram teorias complexas com exemplos práticos.",
        "sinônimo": ["darstellen", "erklären"],
        "perfekt": "hat veranschaulicht",
        "präteritum": "veranschaulichte",
        "regência": "veranschaulichen + Akkusativ",
        "outra_frase": "Um anschauliches Diagramm kann schwierige Konzepte veranschaulichen und das Verständnis fördern.",
        "tradução_outra_frase": "Um diagrama ilustrativo pode exemplificar conceitos difíceis e facilitar a compreensão.",
        "reflexivo": False
    },
    {
        "verbo": "kontextualisieren",
        "tradução": "contextualizar",
        "frase": "Es ist wichtig, historische Ereignisse im richtigen Kontext zu interpretieren und zu kontextualisieren.",
        "tradução_frase": "É importante interpretar e contextualizar eventos históricos de forma adequada.",
        "sinônimo": ["einordnen", "relativieren"],
        "perfekt": "hat kontextualisiert",
        "präteritum": "kontextualisierte",
        "regência": "kontextualisieren (intransitiv)",
        "outra_frase": "Die Vorlesung half den Studierenden, moderne Theorien in den Kontext vergangener Ereignisse zu stellen.",
        "tradução_outra_frase": "A palestra ajudou os alunos a colocar teorias modernas no contexto de eventos passados.",
        "reflexivo": False
    },
    {
        "verbo": "revidieren",
        "tradução": "revisar",
        "frase": "Nach neuen Erkenntnissen revidieren Forscher ihre bisherigen Hypothesen.",
        "tradução_frase": "Após novas descobertas, os pesquisadores revisam suas hipóteses anteriores.",
        "sinônimo": ["überarbeiten", "korrigieren"],
        "perfekt": "hat revidiert",
        "präteritum": "revidierte",
        "regência": "revidieren + Akkusativ",
        "outra_frase": "Die Studie wurde revidiert, um die neuesten wissenschaftlichen Erkenntnisse einzubeziehen.",
        "tradução_outra_frase": "O estudo foi revisado para incluir os mais recentes avanços científicos.",
        "reflexivo": False
    },
    {
        "verbo": "extrapolieren",
        "tradução": "extrapolar",
        "frase": "Aus den vorliegenden Daten können Wissenschaftler Trends extrapolieren, die zukünftige Entwicklungen andeuten.",
        "tradução_frase": "A partir dos dados disponíveis, os cientistas podem extrapolar tendências que sugerem desenvolvimentos futuros.",
        "sinônimo": ["projizieren", "abschätzen"],
        "perfekt": "hat extrapoliert",
        "präteritum": "extrapolierte",
        "regência": "extrapolieren + Akkusativ",
        "outra_frase": "Die Fähigkeit, aus kleinen Datenmengen zu extrapolieren, ist in der Forschung von großem Vorteil.",
        "tradução_outra_frase": "A capacidade de extrapolar a partir de pequenas quantidades de dados é muito vantajosa na pesquisa.",
        "reflexivo": False
    },
    {
        "verbo": "spezifizieren",
        "tradução": "especificar",
        "frase": "Im Forschungsbericht mussten die Autoren ihre Methoden und Ergebnisse detailliert spezifizieren.",
        "tradução_frase": "No relatório de pesquisa, os autores tiveram que especificar seus métodos e resultados detalhadamente.",
        "sinônimo": ["definieren", "festlegen"],
        "perfekt": "hat spezifiziert",
        "präteritum": "spezifizierte",
        "regência": "spezifizieren + Akkusativ",
        "outra_frase": "Um klar spezifizierter Ansatz ist essentiell, um Missverständnisse in der wissenschaftlichen Kommunikation zu vermeiden.",
        "tradução_outra_frase": "Uma abordagem claramente especificada é essencial para evitar mal-entendidos na comunicação científica.",
        "reflexivo": False
    },
    {
        "verbo": "differenzieren",
        "tradução": "diferenciar",
        "frase": "In den Geisteswissenschaften ist es wichtig, zwischen verschiedenen Interpretationsansätzen zu differenzieren.",
        "tradução_frase": "Nas ciências humanas, é importante diferenciar entre diversas abordagens interpretativas.",
        "sinônimo": ["abgrenzen", "unterscheiden"],
        "perfekt": "hat differenziert",
        "präteritum": "differenzierte",
        "regência": "differenzieren (intransitiv)",
        "outra_frase": "Die Studierenden lernten, wissenschaftliche Konzepte voneinander zu differenzieren, um präzisere Analysen zu erstellen.",
        "tradução_outra_frase": "Os alunos aprenderam a diferenciar conceitos científicos para elaborar análises mais precisas.",
        "reflexivo": False
    },
    {
        "verbo": "formulieren",
        "tradução": "formular",
        "frase": "Eine präzise Fragestellung formulieren ist der erste Schritt jeder wissenschaftlichen Arbeit.",
        "tradução_frase": "Formular uma questão precisa é o primeiro passo de qualquer trabalho científico.",
        "sinônimo": ["ausdrücken", "darstellen"],
        "perfekt": "hat formuliert",
        "präteritum": "formulierte",
        "regência": "formulieren + Akkusativ",
        "outra_frase": "Im Seminar übten die Teilnehmer, ihre Gedanken klar zu formulieren, um Missverständnisse zu vermeiden.",
        "tradução_outra_frase": "No seminário, os participantes praticaram formular claramente seus pensamentos para evitar mal-entendidos.",
        "reflexivo": False
    },
    {
        "verbo": "abstrahieren",
        "tradução": "abstrair",
        "frase": "Mathematiker abstrahieren häufig von konkreten Beispielen, um allgemeingültige Prinzipien zu entwickeln.",
        "tradução_frase": "Matemáticos frequentemente abstraem de exemplos concretos para desenvolver princípios universais.",
        "sinônimo": ["vereinfachen", "generalieren"],
        "perfekt": "hat abstrahiert",
        "präteritum": "abstrahierte",
        "regência": "abstrahieren (intransitiv)",
        "outra_frase": "Beim Problemlösen ist es oft notwendig, von der Realität abzusehen und zu abstrahieren.",
        "tradução_outra_frase": "Ao resolver problemas, muitas vezes é preciso abstrair da realidade.",
        "reflexivo": False
    },
    {
        "verbo": "operationalisieren",
        "tradução": "operacionalizar",
        "frase": "In empirischen Studien wird oft versucht, theoretische Konzepte zu operationalisieren, um sie messbar zu machen.",
        "tradução_frase": "Em estudos empíricos, frequentemente se tenta operacionalizar conceitos teóricos para torná-los mensuráveis.",
        "sinônimo": ["konkretisieren", "definieren"],
        "perfekt": "hat operationalisiert",
        "präteritum": "operationalisierte",
        "regência": "operationalisieren + Akkusativ",
        "outra_frase": "Die Forscher arbeiteten daran, abstrakte Ideen zu operationalisieren und in konkrete Messgrößen zu überführen.",
        "tradução_outra_frase": "Os pesquisadores trabalharam para operacionalizar ideias abstratas e convertê-las em medidas concretas.",
        "reflexivo": False
    },
    {
        "verbo": "konvergieren",
        "tradução": "convergir",
        "frase": "Die Ergebnisse verschiedener Studien konvergieren und deuten auf einen einheitlichen Trend hin.",
        "tradução_frase": "Os resultados de diversos estudos convergem, indicando uma tendência unificada.",
        "sinônimo": ["zusammenlaufen", "sich annähern"],
        "perfekt": "ist konvergiert",
        "präteritum": "konvergierte",
        "regência": "konvergieren (intransitiv)",
        "outra_frase": "Wissenschaftliche Theorien konvergieren oft, wenn mehrere Forschungsansätze zu ähnlichen Schlussfolgerungen führen.",
        "tradução_outra_frase": "Teorias científicas frequentemente convergem quando várias abordagens de pesquisa levam a conclusões semelhantes.",
        "reflexivo": False
    },
    {
        "verbo": "divergieren",
        "tradução": "divergir",
        "frase": "In einigen Forschungsfeldern divergieren die Meinungen, was zu intensiven Debatten führt.",
        "tradução_frase": "Em alguns campos de pesquisa, as opiniões divergem, resultando em debates intensos.",
        "sinônimo": ["auseinandergehen", "sich unterscheiden"],
        "perfekt": "ist divergiert",
        "präteritum": "divergierte",
        "regência": "divergieren (intransitiv)",
        "outra_frase": "Die Ansichten der Experten divergieren, was zeigt, dass das Thema noch immer kontrovers diskutiert wird.",
        "tradução_outra_frase": "As opiniões dos especialistas divergem, demonstrando que o tema ainda é objeto de controvérsia.",
        "reflexivo": False
    },
    {
        "verbo": "synchronisieren",
        "tradução": "sincronizar",
        "frase": "Moderne Technologien ermöglichen es, große Datenmengen in Echtzeit zu synchronisieren.",
        "tradução_frase": "Tecnologias modernas possibilitam sincronizar grandes volumes de dados em tempo real.",
        "sinônimo": ["abgleichen", "koordinieren"],
        "perfekt": "hat synchronisiert",
        "präteritum": "synchronisierte",
        "regência": "synchronisieren + Akkusativ",
        "outra_frase": "In interdisziplinären Projekten müssen verschiedene Systeme häufig synchronisiert werden, um reibungslose Abläufe zu garantieren.",
        "tradução_outra_frase": "Em projetos interdisciplinares, diversos sistemas precisam ser sincronizados para garantir operações sem falhas.",
        "reflexivo": False
    },
    {
        "verbo": "verifizieren",
        "tradução": "verificar",
        "frase": "Umfangreiche Experimente werden durchgeführt, um die erhobenen Daten zu verifizieren.",
        "tradução_frase": "Experimentos abrangentes são realizados para verificar os dados coletados.",
        "sinônimo": ["überprüfen", "bestätigen"],
        "perfekt": "hat verifiziert",
        "präteritum": "verifizierte",
        "regência": "verifizieren + Akkusativ",
        "outra_frase": "Bevor die Ergebnisse veröffentlicht werden, müssen sie von unabhängigen Experten verifiziert werden.",
        "tradução_outra_frase": "Antes da publicação, os resultados precisam ser verificados por especialistas independentes.",
        "reflexivo": False
    },
    {
        "verbo": "komplexifizieren",
        "tradução": "complexificar",
        "frase": "In der Soziologie neigen manche Theorien dazu, sich im Laufe der Zeit komplexifizierten und mehrschichtige Strukturen anzunehmen.",
        "tradução_frase": "Na sociologia, algumas teorias tendem a se complexificar ao longo do tempo e a adotar estruturas multifacetadas.",
        "sinônimo": ["komplizieren", "verschachteln"],
        "perfekt": "hat komplexifiziert",
        "präteritum": "komplexifizierte",
        "regência": "komplexifizieren + Akkusativ",
        "outra_frase": "Durch zusätzliche Variablen können Modelle komplexifiziert werden, was die Analyse anspruchsvoller macht.",
        "tradução_outra_frase": "Com variáveis adicionais, os modelos podem se complexificar, tornando a análise mais exigente.",
        "reflexivo": False
    },
    {
        "verbo": "transformieren",
        "tradução": "transformar",
        "frase": "Die Ergebnisse der Forschung transformieren unser Verständnis von traditionellen Konzepten.",
        "tradução_frase": "Os resultados da pesquisa transformam nossa compreensão de conceitos tradicionais.",
        "sinônimo": ["umwandeln", "verändern"],
        "perfekt": "hat transformiert",
        "präteritum": "transformierte",
        "regência": "transformieren + Akkusativ",
        "outra_frase": "Moderne Technologien haben die Art und Weise, wie Daten verarbeitet werden, grundlegend transformiert.",
        "tradução_outra_frase": "Tecnologias modernas transformaram fundamentalmente a forma como os dados são processados.",
        "reflexivo": False
    },
    {
        "verbo": "modifizieren",
        "tradução": "modificar",
        "frase": "Ingenieure modifizieren bestehende Modelle, um sie an aktuelle Forschungsfragen anzupassen.",
        "tradução_frase": "Engenheiros modificam modelos existentes para adaptá-los a questões de pesquisa atuais.",
        "sinônimo": ["anpassen", "verändern"],
        "perfekt": "hat modifiziert",
        "präteritum": "modifizierte",
        "regência": "modifizieren + Akkusativ",
        "outra_frase": "Durch gezielte Modifikationen konnten die Wissenschaftler die Genauigkeit ihrer Simulationen erheblich steigern.",
        "tradução_outra_frase": "Com modificações direcionadas, os cientistas conseguiram aumentar significativamente a precisão de suas simulações.",
        "reflexivo": False
    },
    {
        "verbo": "reproduzieren",
        "tradução": "reproduzir",
        "frase": "In der Biologie versuchen Forscher, komplexe Lebensprozesse im Labor zu reproduzieren.",
        "tradução_frase": "Na biologia, os pesquisadores tentam reproduzir processos vitais complexos no laboratório.",
        "sinônimo": ["nachbilden", "imitieren"],
        "perfekt": "hat reproduziert",
        "präteritum": "reproduzierte",
        "regência": "reproduzieren + Akkusativ",
        "outra_frase": "Die exakte Reproduktion von Experimenten ist ein wesentlicher Schritt, um die Zuverlässigkeit wissenschaftlicher Erkenntnisse zu sichern.",
        "tradução_outra_frase": "A reprodução exata de experimentos é um passo essencial para garantir a confiabilidade dos achados científicos.",
        "reflexivo": False
    },
    {
        "verbo": "fundieren",
        "tradução": "fundamentar",
        "frase": "Die Theorie wird durch empirische Daten fundiert, um ihre Gültigkeit zu untermauern.",
        "tradução_frase": "A teoria é fundamentada por dados empíricos para apoiar sua validade.",
        "sinônimo": ["begründen", "untermauern"],
        "perfekt": "hat fundiert",
        "präteritum": "fundierte",
        "regência": "fundieren + Akkusativ",
        "outra_frase": "Die Argumentation wurde sorgfältig fundiert, um kritischen Analysen standzuhalten.",
        "tradução_outra_frase": "A argumentação foi cuidadosamente fundamentada para resistir a análises críticas.",
        "reflexivo": False
    },
    {
        "verbo": "postulieren",
        "tradução": "postular",
        "frase": "Der Wissenschaftler postulliert, dass alle natürlichen Phänomene auf einfachen Prinzipien beruhen.",
        "tradução_frase": "O cientista postula que todos os fenômenos naturais se baseiam em princípios simples.",
        "sinônimo": ["voraussetzen", "hypothisieren"],
        "perfekt": "hat postuliert",
        "präteritum": "postulierte",
        "regência": "postulieren (intransitiv)",
        "outra_frase": "In der philosophischen Diskussion postuliere man oft alternative Erklärungsmodelle.",
        "tradução_outra_frase": "Nas discussões filosóficas, frequentemente se postulam modelos explicativos alternativos.",
        "reflexivo": False
    },
    {
        "verbo": "substantiieren",
        "tradução": "substanciar",
        "frase": "Um die Theorie zu untermauern, müssen die Autoren ihre Thesen mit Daten substantiieren.",
        "tradução_frase": "Para fundamentar a teoria, os autores precisam comprovar suas teses com dados.",
        "sinônimo": ["belegen", "untermauern"],
        "perfekt": "hat substanziiert",
        "präteritum": "substantiierte",
        "regência": "substantiieren + Akkusativ",
        "outra_frase": "Die Ergebnisse wurden durch zahlreiche Studien substanziiert, was die Glaubwürdigkeit der Forschung erhöht.",
        "tradução_outra_frase": "Os resultados foram comprovados por inúmeros estudos, aumentando a credibilidade da pesquisa.",
        "reflexivo": False
    },
    {
        "verbo": "reflektieren",
        "tradução": "refletir",
        "frase": "Die Studenten reflektieren über die Bedeutung der historischen Ereignisse und deren Einfluss auf die Gegenwart.",
        "tradução_frase": "Os alunos refletem sobre a importância dos eventos históricos e seu impacto no presente.",
        "sinônimo": ["nachdenken", "überdenken"],
        "perfekt": "hat reflektiert",
        "präteritum": "reflektierte",
        "regência": "reflektieren über + Akkusativ",
        "outra_frase": "In Seminaren wird oft reflektiert, um tiefere Einsichten in komplexe Themen zu gewinnen.",
        "tradução_outra_frase": "Em seminários, frequentemente se reflete para obter insights mais profundos sobre temas complexos.",
        "reflexivo": False
    },
    {
        "verbo": "dekonstruieren",
        "tradução": "deconstruir",
        "frase": "Die Literaturkritiker dekonstruieren traditionelle Erzählstrukturen, um verborgene Bedeutungen aufzudecken.",
        "tradução_frase": "Os críticos literários deconstroem estruturas narrativas tradicionais para revelar significados ocultos.",
        "sinônimo": ["analysieren", "zerlegen"],
        "perfekt": "hat dekonstruierte",
        "präteritum": "dekonstruierte",
        "regência": "dekonstruieren + Akkusativ",
        "outra_frase": "In der Postmoderne wird dekonstruieren oft als Methode angewandt, um bestehende Normen zu hinterfragen.",
        "tradução_outra_frase": "Na pós-modernidade, a deconstrução é frequentemente utilizada para questionar as normas estabelecidas.",
        "reflexivo": False
    },
    {
        "verbo": "synthetisieren",
        "tradução": "sintetizar",
        "frase": "Die Forscher synthetisieren verschiedene Theorien, um ein umfassenderes Modell zu entwickeln.",
        "tradução_frase": "Os pesquisadores sintetizam diversas teorias para desenvolver um modelo mais abrangente.",
        "sinônimo": ["zusammenführen", "vereinigen"],
        "perfekt": "hat synthetisiert",
        "präteritum": "synthetisierte",
        "regência": "synthetisieren + Akkusativ",
        "outra_frase": "Durch die Synthese von Daten aus unterschiedlichen Quellen entstand eine neue Perspektive.",
        "tradução_outra_frase": "Através da síntese de dados de diferentes fontes, surgiu uma nova perspectiva.",
        "reflexivo": False
    },
    {
        "verbo": "problematisieren",
        "tradução": "problematizar",
        "frase": "Die Soziologen problematisieren den Einfluss digitaler Medien auf zwischenmenschliche Beziehungen.",
        "tradução_frase": "Os sociólogos problematizam a influência dos meios digitais nas relações interpessoais.",
        "sinônimo": ["hinterfragen", "kritisch beleuchten"],
        "perfekt": "hat problematisiert",
        "präteritum": "problematisierte",
        "regência": "problematisieren + Akkusativ",
        "outra_frase": "In akademischen Kreisen wird oft problematisiert, wie soziale Ungleichheit reproduziert wird.",
        "tradução_outra_frase": "Nos círculos acadêmicos, frequentemente se discute como a desigualdade social se reproduz.",
        "reflexivo": False
    },
    {
        "verbo": "konzeptualisieren",
        "tradução": "conceitualizar",
        "frase": "Die Theoretiker konzeptualisieren abstrakte Ideen in konkrete Modelle um.",
        "tradução_frase": "Os teóricos conceitualizam ideias abstratas em modelos concretos.",
        "sinônimo": ["definieren", "entwickeln"],
        "perfekt": "hat konzeptualisiert",
        "präteritum": "konzeptualisierte",
        "regência": "konzeptualisieren + Akkusativ",
        "outra_frase": "Ein klar konzeptualisiertes Modell erleichtert die Diskussion über komplexe Themen erheblich.",
        "tradução_outra_frase": "Um modelo bem conceitualizado facilita significativamente a discussão sobre temas complexos.",
        "reflexivo": False
    },
    {
        "verbo": "induzieren",
        "tradução": "induzir",
        "frase": "Experimentelle Studien induzieren oft bestimmte Reaktionen, um Hypothesen zu testen.",
        "tradução_frase": "Estudos experimentais frequentemente induzem certas reações para testar hipóteses.",
        "sinônimo": ["veranlassen", "hervorrufen"],
        "perfekt": "hat induziert",
        "präteritum": "induzierte",
        "regência": "induzieren + Akkusativ",
        "outra_frase": "Durch gezielte Interventionen konnten Forscher spezifische Verhaltensmuster induzieren.",
        "tradução_outra_frase": "Através de intervenções direcionadas, os pesquisadores conseguiram induzir padrões comportamentais específicos.",
        "reflexivo": False
    },
    {
        "verbo": "deduzieren",
        "tradução": "deduzir",
        "frase": "Aus den vorliegenden Daten deduzieren die Wissenschaftler die zugrunde liegenden Zusammenhänge.",
        "tradução_frase": "A partir dos dados apresentados, os cientistas deduzem as relações subjacentes.",
        "sinônimo": ["folgern"],
        "perfekt": "hat deduziert",
        "präteritum": "deduzierte",
        "regência": "deduzieren (intransitiv)",
        "outra_frase": "Logische Schlüsse deduzieren aus empirischen Befunden ist ein zentraler Bestandteil der Forschung.",
        "tradução_outra_frase": "Deduzir conclusões lógicas a partir de dados empíricos é uma parte central da pesquisa.",
        "reflexivo": False
    },
    {
        "verbo": "diskursieren",
        "tradução": "discursar",
        "frase": "Die Akademiker diskursieren regelmäßig über die aktuellen Herausforderungen der Globalisierung.",
        "tradução_frase": "Os acadêmicos discursam regularmente sobre os desafios atuais da globalização.",
        "sinônimo": ["debattieren"],
        "perfekt": "hat diskursiert",
        "präteritum": "diskursierte",
        "regência": "diskursieren (intransitiv)",
        "outra_frase": "In internationalen Konferenzen diskursieren Experten über interkulturelle Herausforderungen.",
        "tradução_outra_frase": "Em conferências internacionais, especialistas discursam sobre desafios interculturais.",
        "reflexivo": False
    },
    {
        "verbo": "kommentieren",
        "tradução": "comentar",
        "frase": "Die Kritiker kommentieren das neue Buch mit scharfsinnigen Analysen und persönlichen Eindrücken.",
        "tradução_frase": "Os críticos comentam o novo livro com análises perspicazes e impressões pessoais.",
        "sinônimo": ["rezensieren", "bewerten"],
        "perfekt": "hat kommentiert",
        "präteritum": "kommentierte",
        "regência": "kommentieren + Akkusativ",
        "outra_frase": "Während des Symposiums kommentierten die Professoren aktuelle Forschungsergebnisse ausführlich.",
        "tradução_outra_frase": "Durante o simpósio, os professores comentaram detalhadamente os resultados de pesquisas atuais.",
        "reflexivo": False
    },
    {
        "verbo": "interpolieren",
        "tradução": "interpolar",
        "frase": "Datenlücken in der Statistik werden oft durch mathematische Modelle interpoliert.",
        "tradução_frase": "Lacunas em estatísticas são frequentemente interpoladas por modelos matemáticos.",
        "sinônimo": ["überbrücken", "ergänzen"],
        "perfekt": "hat interpoliert",
        "präteritum": "interpolierte",
        "regência": "interpolieren + Akkusativ",
        "outra_frase": "Um eine kontinuierliche Datenreihe zu erhalten, müssen fehlende Werte interpoliert werden.",
        "tradução_outra_frase": "Para obter uma série de dados contínua, os valores ausentes precisam ser interpolados.",
        "reflexivo": False
    },
    {
        "verbo": "parametrisieren",
        "tradução": "parametrizar",
        "frase": "Die Forscher parametrisieren ihre Modelle, um verschiedene Einflussfaktoren zu berücksichtigen.",
        "tradução_frase": "Os pesquisadores parametrizam seus modelos para levar em conta diferentes fatores de influência.",
        "sinônimo": ["festlegen", "standardisieren"],
        "perfekt": "hat parametrisiert",
        "präteritum": "parametrisierte",
        "regência": "parametrisieren + Akkusativ",
        "outra_frase": "Eine sorgfältige Parametrisierung ermöglicht präzisere Simulationen in der Physik.",
        "tradução_outra_frase": "Uma parametrização cuidadosa permite simulações mais precisas na física.",
        "reflexivo": False
    },
    {
        "verbo": "aggregieren",
        "tradução": "agregar",
        "frase": "In der Sozialforschung aggregieren die Datenanalysten Informationen aus verschiedenen Quellen, um ein umfassendes Bild zu erhalten.",
        "tradução_frase": "Na pesquisa social, os analistas agregam informações de diversas fontes para obter uma visão abrangente.",
        "sinônimo": ["sammeln", "vereinigen"],
        "perfekt": "hat aggregiert",
        "präteritum": "aggregierte",
        "regência": "aggregieren + Akkusativ",
        "outra_frase": "Die Fähigkeit, unterschiedliche Daten zu aggregieren, ist essenziell für aussagekräftige Analysen.",
        "tradução_outra_frase": "A capacidade de agregar dados distintos é essencial para análises significativas.",
        "reflexivo": False
    },
    {
        "verbo": "charakterisieren",
        "tradução": "caracterizar",
        "frase": "Die Studie charakterisiert die sozialen Dynamiken in urbanen Räumen detailliert.",
        "tradução_frase": "O estudo caracteriza as dinâmicas sociais em áreas urbanas de forma detalhada.",
        "sinônimo": ["beschreiben", "definieren"],
        "perfekt": "hat charakterisiert",
        "präteritum": "charakterisierte",
        "regência": "charakterisieren + Akkusativ",
        "outra_frase": "Experten charakterisieren das Phänomen als ein komplexes Zusammenspiel von Faktoren.",
        "tradução_outra_frase": "Especialistas caracterizam o fenômeno como uma interação complexa de fatores.",
        "reflexivo": False
    },
    {
        "verbo": "philosophieren",
        "tradução": "filosofar",
        "frase": "In den Geisteswissenschaften philosophieren die Denker über die Grundfragen des Seins und der Erkenntnis.",
        "tradução_frase": "Nas ciências humanas, os pensadores filosofam sobre as questões fundamentais do ser e do conhecimento.",
        "sinônimo": ["sinnen", "grübeln"],
        "perfekt": "hat philosophiert",
        "präteritum": "philosophierte",
        "regência": "philosophieren (intransitiv)",
        "outra_frase": "Während der Vorlesung philosophierten die Studenten angeregt über den Sinn des Lebens.",
        "tradução_outra_frase": "Durante a palestra, os alunos filosofaram animadamente sobre o sentido da vida.",
        "reflexivo": False
    },
    {
        "verbo": "reformulieren",
        "tradução": "reformular",
        "frase": "Um die Theorie zu präzisieren, reformulierten die Wissenschaftler ihre ursprünglichen Annahmen.",
        "tradução_frase": "Para precisar a teoria, os cientistas reformularam suas premissas originais.",
        "sinônimo": ["umgestalten", "neu formulieren"],
        "perfekt": "hat reformuliert",
        "präteritum": "reformulierte",
        "regência": "reformulieren + Akkusativ",
        "outra_frase": "Die Autoren reformulierten den Forschungsansatz, um ihn an aktuelle Erkenntnisse anzupassen.",
        "tradução_outra_frase": "Os autores reformularam a abordagem de pesquisa para alinhá-la com os conhecimentos atuais.",
        "reflexivo": False
    },
    {
        "verbo": "explizieren",
        "tradução": "explicitar",
        "frase": "Die Dozenten explizieren die theoretischen Grundlagen, um das Verständnis der Studierenden zu fördern.",
        "tradução_frase": "Os professores explicitam os fundamentos teóricos para promover a compreensão dos alunos.",
        "sinônimo": ["verdeutlichen", "darlegen"],
        "perfekt": "hat expliziert",
        "präteritum": "explizierte",
        "regência": "explizieren + Akkusativ",
        "outra_frase": "In Fachvorträgen explizieren Experten häufig die Zusammenhänge zwischen Theorie und Praxis.",
        "tradução_outra_frase": "Em palestras especializadas, os especialistas frequentemente explicam as inter-relações entre teoria e prática.",
        "reflexivo": False
    },
    {
        "verbo": "elaborieren",
        "tradução": "elaborar",
        "frase": "Die Forscher elaborieren ein detailliertes Konzept, um das komplexe Phänomen zu untersuchen.",
        "tradução_frase": "Os pesquisadores elaboram um conceito detalhado para investigar o fenômeno complexo.",
        "sinônimo": ["ausarbeiten", "entwickeln"],
        "perfekt": "hat elaboriert",
        "präteritum": "elaborierte",
        "regência": "elaborieren + Akkusativ",
        "outra_frase": "In interdisziplinären Projekten elaborieren die Teams innovative Lösungsansätze.",
        "tradução_outra_frase": "Em projetos interdisciplinares, as equipes elaboram abordagens inovadoras para a solução de problemas.",
        "reflexivo": False
    },
    {
        "verbo": "antizipieren",
        "tradução": "antecipar",
        "frase": "Die Soziologen antizipieren zukünftige Entwicklungen in der Arbeitswelt durch den Einsatz neuer Technologien.",
        "tradução_frase": "Os sociólogos antecipam desenvolvimentos futuros no mercado de trabalho com o uso de novas tecnologias.",
        "sinônimo": ["voraussehen", "prognostizieren"],
        "perfekt": "hat antizipiert",
        "präteritum": "antizipierte",
        "regência": "antizipieren + Akkusativ",
        "outra_frase": "Durch die Analyse aktueller Trends antizipieren Experten oft disruptive Veränderungen.",
        "tradução_outra_frase": "Através da análise de tendências atuais, os especialistas frequentemente antecipam mudanças disruptivas.",
        "reflexivo": False
    },
    {
        "verbo": "kategorisieren",
        "tradução": "categorizar",
        "frase": "Die Wissenschaftler kategorisieren die Daten, um klare Strukturen in der Analyse zu schaffen.",
        "tradução_frase": "Os cientistas categorizam os dados para criar estruturas claras na análise.",
        "sinônimo": ["einordnen", "klassifizieren"],
        "perfekt": "hat kategorisiert",
        "präteritum": "kategorisierte",
        "regência": "kategorisieren + Akkusativ",
        "outra_frase": "Eine sorgfältige Kategorisierung erleichtert die spätere Auswertung erheblich.",
        "tradução_outra_frase": "Uma categorização cuidadosa facilita significativamente a análise posterior.",
        "reflexivo": False
    },
    {
        "verbo": "rekontextualisieren",
        "tradução": "recontextualizar",
        "frase": "Die Historiker rekontextualisieren alte Ereignisse, um sie im Lichte aktueller Theorien neu zu bewerten.",
        "tradução_frase": "Os historiadores recontextualizam eventos antigos para reavaliá-los à luz de teorias atuais.",
        "sinônimo": ["neu einordnen", "relativieren"],
        "perfekt": "hat rekontextualisiert",
        "präteritum": "rekontextualisierte",
        "regência": "rekontextualisieren + Akkusativ",
        "outra_frase": "Durch das Rekontextualisieren wird die Bedeutung historischer Daten oft völlig neu definiert.",
        "tradução_outra_frase": "Ao recontextualizar, o significado dos dados históricos é frequentemente redefinido.",
        "reflexivo": False
    },
    {
        "verbo": "marginalisieren",
        "tradução": "marginalizar",
        "frase": "In der Gesellschaftstheorie wird oft untersucht, wie bestimmte Gruppen marginalisiert werden.",
        "tradução_frase": "Na teoria social, frequentemente se investiga como determinados grupos são marginalizados.",
        "sinônimo": ["ausgrenzen", "benachteiligen"],
        "perfekt": "hat marginalisiert",
        "präteritum": "marginalisierte",
        "regência": "marginalisieren + Akkusativ",
        "outra_frase": "Die Forschung zeigt, dass soziale Institutionen manchmal Minderheiten systematisch marginalisieren.",
        "tradução_outra_frase": "A pesquisa mostra que instituições sociais às vezes marginalizam sistematicamente as minorias.",
        "reflexivo": False
    },
    {
        "verbo": "akzentuieren",
        "tradução": "enfatizar",
        "frase": "Die Autoren akzentuieren in ihren Arbeiten die Bedeutung von interkulturellen Dialogen.",
        "tradução_frase": "Os autores enfatizam em seus trabalhos a importância do diálogo intercultural.",
        "sinônimo": ["betonen", "hervorheben"],
        "perfekt": "hat akzentuiert",
        "präteritum": "akzentuierte",
        "regência": "akzentuieren + Akkusativ",
        "outra_frase": "In der Diskussion akzentuieren die Experten immer wieder die Notwendigkeit einer differenzierten Analyse.",
        "tradução_outra_frase": "Na discussão, os especialistas reiteram a necessidade de uma análise diferenciada.",
        "reflexivo": False
    },
    {
        "verbo": "konstituieren",
        "tradução": "constituir",
        "frase": "Die sozialen Normen konstituieren die Grundlage des Zusammenlebens in einer Gesellschaft.",
        "tradução_frase": "As normas sociais constituem a base da convivência em uma sociedade.",
        "sinônimo": ["bilden", "gestalten"],
        "perfekt": "hat konstituiert",
        "präteritum": "konstituierte",
        "regência": "konstituieren (intransitiv)",
        "outra_frase": "Wissenschaftler untersuchen, wie kulturelle Werte soziale Strukturen konstituieren.",
        "tradução_outra_frase": "Cientistas investigam como os valores culturais formam estruturas sociais.",
        "reflexivo": False
    },
    {
        "verbo": "historisieren",
        "tradução": "historicizar",
        "frase": "Die Theoretiker historisieren aktuelle Ereignisse, um deren langfristige Bedeutung zu erfassen.",
        "tradução_frase": "Os teóricos historicizam eventos atuais para capturar seu significado a longo prazo.",
        "sinônimo": ["zeitlich einordnen", "dokumentieren"],
        "perfekt": "hat historisiert",
        "präteritum": "historisierte",
        "regência": "historisieren + Akkusativ",
        "outra_frase": "Durch das Historisieren wird deutlich, wie sich gesellschaftliche Entwicklungen über die Zeit verändern.",
        "tradução_outra_frase": "Ao historicizar, fica evidente como as mudanças sociais se transformam ao longo do tempo.",
        "reflexivo": False
    },
    {
        "verbo": "nuancieren",
        "tradução": "nuançar",
        "frase": "Die Experten nuancieren ihre Argumente, um die Komplexität des Themas darzustellen.",
        "tradução_frase": "Os especialistas matizam seus argumentos para representar a complexidade do tema.",
        "sinônimo": ["fein abstimmen", "detaillieren"],
        "perfekt": "hat nuanciert",
        "präteritum": "nuancierte",
        "regência": "nuancieren + Akkusativ",
        "outra_frase": "In akademischen Diskursen nuancieren die Teilnehmer ihre Standpunkte, um Missverständnisse zu vermeiden.",
        "tradução_outra_frase": "Em debates acadêmicos, os participantes matizam suas posições para evitar mal-entendidos.",
        "reflexivo": False
    },
    {
        "verbo": "assimilieren",
        "tradução": "assimilar",
        "frase": "In den Sozialwissenschaften wird untersucht, wie Minderheiten sich in die Mehrheitskultur assimilieren.",
        "tradução_frase": "Nas ciências sociais, investiga-se como as minorias se assimilam à cultura da maioria.",
        "sinônimo": ["angleichen", "einverleiben"],
        "perfekt": "hat assimiliert",
        "präteritum": "assimilierte",
        "regência": "assimilieren (intransitiv)",
        "outra_frase": "Die Studie zeigt, dass kulturelle Assimilation ein langwieriger Prozess sein kann.",
        "tradução_outra_frase": "O estudo mostra que a assimilação cultural pode ser um processo demorado.",
        "reflexivo": False
    },
    {
        "verbo": "hierarchisieren",
        "tradução": "hierarquizar",
        "frase": "Die Forscher hierarchisieren verschiedene Einflussfaktoren, um ihre Bedeutung besser zu ordnen.",
        "tradução_frase": "Os pesquisadores hierarquizam diferentes fatores de influência para melhor organizá-los.",
        "sinônimo": ["rangieren", "ordnen"],
        "perfekt": "hat hierarchisiert",
        "präteritum": "hierarchisierte",
        "regência": "hierarchisieren + Akkusativ",
        "outra_frase": "Durch das Hierarchisieren der Daten lassen sich prioritäre Themen in der Analyse leichter identifizieren.",
        "tradução_outra_frase": "Ao hierarquizar os dados, é mais fácil identificar os temas prioritários na análise.",
        "reflexivo": False
    },
    {
        "verbo": "demokratisieren",
        "tradução": "democratizar",
        "frase": "Die neue Regierung versucht, das Land zu demokratisieren und mehr Mitsprache zu ermöglichen.",
        "tradução_frase": "O novo governo tenta democratizar o país e possibilitar mais participação.",
        "sinônimo": ["volksbestimmen", "partizipieren"],
        "perfekt": "hat demokratisiert",
        "präteritum": "demokratisierte",
        "regência": "demokratisieren (intransitiv)",
        "outra_frase": "Umfangreiche Reformen wurden durchgeführt, um das politische System zu volksbestimmen.",
        "tradução_outra_frase": "Foram realizadas reformas abrangentes para tornar o sistema político mais democrático.",
        "reflexivo": False
    },
    {
        "verbo": "regulieren",
        "tradução": "regular",
        "frase": "Die EU versucht, den Finanzmarkt strenger zu regulieren, um Stabilität zu gewährleisten.",
        "tradução_frase": "A UE tenta regular o mercado financeiro de forma mais rigorosa para garantir estabilidade.",
        "sinônimo": ["steuern", "kontrollieren"],
        "perfekt": "hat reguliert",
        "präteritum": "regulierte",
        "regência": "regulieren + Akkusativ",
        "outra_frase": "Neue Gesetze wurden erlassen, um die Wirtschaft stärker zu steuern.",
        "tradução_outra_frase": "Novas leis foram aprovadas para controlar a economia de forma mais eficaz.",
        "reflexivo": False
    },
    {
        "verbo": "partizipieren",
        "tradução": "participar",
        "frase": "Bürger sollen aktiv am politischen Geschehen partizipieren, um ihre Stimme zu erheben.",
        "tradução_frase": "Os cidadãos devem participar ativamente da política para fazerem ouvir suas vozes.",
        "sinônimo": ["sich beteiligen", "mitwirken"],
        "perfekt": "hat partizipiert",
        "präteritum": "partizipierte",
        "regência": "partizipieren an + Dativ",
        "outra_frase": "In lokalen Versammlungen beteiligen sich viele Menschen, um ihre Meinung einzubringen.",
        "tradução_outra_frase": "Em assembleias locais, muitas pessoas se envolvem para expressar sua opinião.",
        "reflexivo": False
    },
    {
        "verbo": "protestieren",
        "tradução": "protestar",
        "frase": "Zahlreiche Demonstranten protestieren gegen die geplanten Sparmaßnahmen der Regierung.",
        "tradução_frase": "Diversos manifestantes protestam contra as medidas de austeridade planejadas pelo governo.",
        "sinônimo": ["aufbegehren", "sich widersetzen"],
        "perfekt": "hat protestiert",
        "präteritum": "protestierte",
        "regência": "protestieren gegen + Akkusativ",
        "outra_frase": "Die Bürger setzten sich energisch zur Wehr und begehren, sich gegen Kürzungen aufzubegehren.",
        "tradução_outra_frase": "Os cidadãos se manifestaram com energia, exigindo resistência contra os cortes.",
        "reflexivo": False
    },
    {
        "verbo": "delegieren",
        "tradução": "delegar",
        "frase": "Der Minister delegiert wichtige Aufgaben an erfahrene Berater, um effizientere Entscheidungen zu treffen.",
        "tradução_frase": "O ministro delega tarefas importantes a assessores experientes para tomar decisões mais eficientes.",
        "sinônimo": ["übertragen", "abgeben"],
        "perfekt": "hat delegiert",
        "präteritum": "delegierte",
        "regência": "delegieren + Akkusativ",
        "outra_frase": "In großen Organisationen wird oft Verantwortung an Fachleute übertragen.",
        "tradução_outra_frase": "Em grandes organizações, frequentemente a responsabilidade é delegada a especialistas.",
        "reflexivo": False
    },
    {
        "verbo": "artikulieren",
        "tradução": "articular, expressar",
        "frase": "Die Politiker müssen ihre Argumente klar artikulieren, um die Wähler zu überzeugen.",
        "tradução_frase": "Os políticos precisam articular seus argumentos de forma clara para convencer os eleitores.",
        "sinônimo": ["darlegen", "ausdrücken"],
        "perfekt": "hat artikuliert",
        "präteritum": "artikülierte",
        "regência": "artikulieren + Akkusativ",
        "outra_frase": "In Debatten drückt man seine Standpunkte deutlich aus, um Gehör zu finden.",
        "tradução_outra_frase": "Em debates, as pessoas expressam claramente suas posições para serem ouvidas.",
        "reflexivo": False
    },
    {
        "verbo": "mobilisieren",
        "tradução": "mobilizar",
        "frase": "Sozialaktivisten mobilisieren die Gemeinschaft, um gegen soziale Ungerechtigkeit vorzugehen.",
        "tradução_frase": "Ativistas sociais mobilizam a comunidade para combater as injustiças sociais.",
        "sinônimo": ["aktivieren", "organisieren"],
        "perfekt": "hat mobilisiert",
        "präteritum": "mobilisierte",
        "regência": "mobilisieren (intransitiv)",
        "outra_frase": "Durch Demonstrationen werden die Bürger aktiviert, sich gemeinsam einzusetzen.",
        "tradução_outra_frase": "Por meio de manifestações, os cidadãos são mobilizados para agir em conjunto.",
        "reflexivo": False
    },
    {
        "verbo": "politisieren",
        "tradução": "politisar, politisieren",
        "frase": "Die Medien tragen dazu bei, gesellschaftliche Themen zu politisieren und den Diskurs anzuregen.",
        "tradução_frase": "A mídia contribui para politizar temas sociais e estimular o debate.",
        "sinônimo": ["in den politischen Fokus rücken", "auf die politische Agenda setzen"],
        "perfekt": "hat politisiert",
        "präteritum": "politisierte",
        "regência": "politisieren (intransitiv)",
        "outra_frase": "Durch gezielte Berichterstattung werden Probleme in den politischen Fokus gerückt.",
        "tradução_outra_frase": "Por meio de reportagens direcionadas, os problemas são colocados em evidência na política.",
        "reflexivo": False
    },
    {
        "verbo": "sanktionieren",
        "tradução": "sanctionar, impor sanções",
        "frase": "Internationale Organisationen sanktionieren Staaten, die gegen Menschenrechte verstoßen.",
        "tradução_frase": "Organizações internacionais impõem sanções a Estados que violam os direitos humanos.",
        "sinônimo": ["bestrafen", "maßen Strafen zu"],
        "perfekt": "hat sanktioniert",
        "präteritum": "sanktionierte",
        "regência": "sanktionieren + Akkusativ",
        "outra_frase": "Bei gravierenden Verstößen werden Länder oft mit strengen Maßnahmen bestraft.",
        "tradução_outra_frase": "Em casos de violações graves, os países são frequentemente sancionados com medidas rigorosas.",
        "reflexivo": False
    },
    {
        "verbo": "manifestieren",
        "tradução": "manifestar",
        "frase": "Die Demonstranten manifestieren ihren Unmut über die politischen Entscheidungen auf den Straßen der Hauptstadt.",
        "tradução_frase": "Os manifestantes expressam seu descontentamento com as decisões políticas nas ruas da capital.",
        "sinônimo": ["bekunden", "zum Ausdruck bringen"],
        "perfekt": "hat manifestiert",
        "präteritum": "manifestierte",
        "regência": "manifestieren (intransitiv)",
        "outra_frase": "Viele Bürger bringen ihre Meinung auf öffentlichen Plätzen zum Ausdruck.",
        "tradução_outra_frase": "Muitos cidadãos manifestam suas opiniões em locais públicos.",
        "reflexivo": False
    },
    {
        "verbo": "konsolidieren",
        "tradução": "consolidar",
        "frase": "Die Regierung versucht, ihre Macht zu konsolidieren, indem sie verschiedene Interessen bündelt.",
        "tradução_frase": "O governo tenta consolidar seu poder reunindo diversos interesses.",
        "sinônimo": ["festigen", "stärken"],
        "perfekt": "hat konsolidiert",
        "präteritum": "konsolidierte",
        "regência": "konsolidieren + Akkusativ",
        "outra_frase": "Durch strategische Allianzen konnte die Führung ihre Position stärken.",
        "tradução_outra_frase": "Através de alianças estratégicas, a liderança conseguiu consolidar sua posição.",
        "reflexivo": False
    },
    {
        "verbo": "legitimieren",
        "tradução": "legitimar",
        "frase": "Die neue Verfassung soll die Macht der Regierung legitimieren und den Bürgern Sicherheit geben.",
        "tradução_frase": "A nova constituição deve legitimar o poder do governo e proporcionar segurança aos cidadãos.",
        "sinônimo": ["rechtfertigen", "anerkennen"],
        "perfekt": "hat legitimiert",
        "präteritum": "legitimierte",
        "regência": "legitimieren + Akkusativ",
        "outra_frase": "Durch demokratische Wahlen wird das Handeln der Politiker anerkannt.",
        "tradução_outra_frase": "Por meio de eleições democráticas, as ações dos políticos são legitimadas.",
        "reflexivo": False
    },
    {
        "verbo": "dezentralisieren",
        "tradução": "descentralizar",
        "frase": "Viele Experten fordern, die politischen Strukturen zu dezentralisieren, um regionale Bedürfnisse besser zu berücksichtigen.",
        "tradução_frase": "Muitos especialistas exigem descentralizar as estruturas políticas para melhor atender às necessidades regionais.",
        "sinônimo": ["delegieren", "aufteilen"],
        "perfekt": "hat dezentralisiert",
        "präteritum": "dezentralisierte",
        "regência": "dezentralisieren (intransitiv)",
        "outra_frase": "Die Verwaltung soll regional aufgeteilt werden, um näher am Volk zu sein.",
        "tradução_outra_frase": "A administração deve ser descentralizada para estar mais próxima do povo.",
        "reflexivo": False
    },
    {
        "verbo": "zentralisieren",
        "tradução": "centralizar",
        "frase": "In Krisenzeiten neigen manche Regierungen dazu, die Macht zu zentralisieren.",
        "tradução_frase": "Em tempos de crise, alguns governos tendem a centralizar o poder.",
        "sinônimo": ["konzentrieren", "vereinheitlichen"],
        "perfekt": "hat zentralisiert",
        "präteritum": "zentralisierte",
        "regência": "zentralisieren + Akkusativ",
        "outra_frase": "Die Entscheidung, Ressourcen zu konzentrieren, dient oft der schnellen Krisenbewältigung.",
        "tradução_outra_frase": "A decisão de centralizar os recursos muitas vezes visa a rápida superação da crise.",
        "reflexivo": False
    },
    {
        "verbo": "reformieren",
        "tradução": "reformar",
        "frase": "Das Parlament plant, das Bildungssystem grundlegend zu reformieren.",
        "tradução_frase": "O parlamento planeja reformar fundamentalmente o sistema educacional.",
        "sinônimo": ["erneuern", "umgestalten"],
        "perfekt": "hat reformiert",
        "präteritum": "reformierte",
        "regência": "reformieren + Akkusativ",
        "outra_frase": "Mit mutigen Maßnahmen wird versucht, veraltete Strukturen zu erneuern.",
        "tradução_outra_frase": "Com medidas ousadas, tenta-se renovar estruturas obsoletas.",
        "reflexivo": False
    },
    {
        "verbo": "verankern",
        "tradução": "ancorar, firmieren",
        "frase": "Grundwerte werden in der Verfassung verankert, um die Demokratie zu schützen.",
        "tradução_frase": "Valores fundamentais são ancorados na constituição para proteger a democracia.",
        "sinônimo": ["festschreiben", "eingliedern"],
        "perfekt": "hat verankert",
        "präteritum": "verankerte",
        "regência": "verankern + Akkusativ",
        "outra_frase": "Die Prinzipien der Freiheit werden in das politische System festgeschrieben.",
        "tradução_outra_frase": "Os princípios da liberdade são firmados no sistema político.",
        "reflexivo": False
    },
    {
        "verbo": "intervenieren",
        "tradução": "intervir",
        "frase": "Internationale Organisationen intervenieren, wenn Menschenrechte massiv verletzt werden.",
        "tradução_frase": "Organizações internacionais intervêm quando há violações maciças dos direitos humanos.",
        "sinônimo": ["eingreifen", "sich einmischen"],
        "perfekt": "hat interveniert",
        "präteritum": "intervenierte",
        "regência": "intervenieren (intransitiv)",
        "outra_frase": "In Konfliktsituationen greifen oft Dritte ein, um den Frieden wiederherzustellen.",
        "tradução_outra_frase": "Em situações de conflito, terceiros frequentemente intervêm para restaurar a paz.",
        "reflexivo": False
    },
    {
        "verbo": "opponieren",
        "tradução": "opor, resistir",
        "frase": "Die Opposition opponiert sich vehement gegen die aktuellen Gesetzesvorlagen.",
        "tradução_frase": "A oposição se opõe veementemente às propostas de lei atuais.",
        "sinônimo": ["widersprechen", "sich widersetzen"],
        "perfekt": "hat opponiert",
        "präteritum": "opponierte",
        "regência": "opponieren gegen + Akkusativ",
        "outra_frase": "Viele Politiker widersprechen sich offen in parlamentarischen Debatten.",
        "tradução_outra_frase": "Muitos políticos se opõem abertamente em debates parlamentares.",
        "reflexivo": False
    },
    {
        "verbo": "stabilisieren",
        "tradução": "estabilizar",
        "frase": "Nach turbulenten Zeiten versucht die Regierung, die Wirtschaft zu stabilisieren.",
        "tradução_frase": "Após tempos turbulentos, o governo tenta estabilizar a economia.",
        "sinônimo": ["festigen", "sichern"],
        "perfekt": "hat stabilisiert",
        "präteritum": "stabilisierte",
        "regência": "stabilisieren + Akkusativ",
        "outra_frase": "Durch gezielte Maßnahmen konnte man das politische Klima sichern.",
        "tradução_outra_frase": "Por meio de medidas específicas, conseguiu-se estabilizar o clima político.",
        "reflexivo": False
    },
    {
        "verbo": "radikalisieren",
        "tradução": "radicalizar",
        "frase": "Unzufriedenheit in der Gesellschaft kann dazu führen, dass sich manche Menschen radikalisieren.",
        "tradução_frase": "A insatisfação na sociedade pode levar algumas pessoas a se radicalizarem.",
        "sinônimo": ["extremisieren", "polarisieren"],
        "perfekt": "hat radikalisiert",
        "präteritum": "radikalisierte",
        "regência": "radikalisieren (intransitiv)",
        "outra_frase": "Ohne Dialog können gesellschaftliche Spannungen leicht extremisiert werden.",
        "tradução_outra_frase": "Sem diálogo, as tensões sociais podem facilmente se radicalizar.",
        "reflexivo": False
    },
    {
        "verbo": "koordinieren",
        "tradução": "coordenar",
        "frase": "Verschiedene staatliche Stellen koordinieren ihre Maßnahmen, um effizient auf Krisen zu reagieren.",
        "tradução_frase": "Diversos órgãos estatais coordenam suas ações para reagir de forma eficiente às crises.",
        "sinônimo": ["abstimmen", "synchronisieren"],
        "perfekt": "hat koordiniert",
        "präteritum": "koordinierte",
        "regência": "koordinieren + Akkusativ",
        "outra_frase": "Eine enge Abstimmung zwischen den Behörden ist notwendig, um rasch zu handeln.",
        "tradução_outra_frase": "Uma coordenação estreita entre as autoridades é necessária para agir rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "expropriieren",
        "tradução": "expropriar",
        "frase": "In bestimmten politischen Systemen wird Land expropriiert, um soziale Reformen durchzusetzen.",
        "tradução_frase": "Em determinados sistemas políticos, terras são expropriadas para implementar reformas sociais.",
        "sinônimo": ["enteignen", "konfiszieren"],
        "perfekt": "hat expropriiert",
        "präteritum": "expropriiert",
        "regência": "expropriieren + Akkusativ",
        "outra_frase": "Die Regierung entschied, ungenutzte Grundstücke zu enteignen, um Wohnraum zu schaffen.",
        "tradução_outra_frase": "O governo decidiu expropriar terrenos não utilizados para criar moradias.",
        "reflexivo": False
    },
    {
        "verbo": "deregulieren",
        "tradução": "desregulamentar",
        "frase": "Wirtschaftsverbände fordern, den Markt stärker zu deregulieren, um Innovationen zu fördern.",
        "tradução_frase": "Associações empresariais exigem uma maior desregulamentação do mercado para fomentar inovações.",
        "sinônimo": ["abbauen", "lockern"],
        "perfekt": "hat dereguliert",
        "präteritum": "deregulierte",
        "regência": "deregulieren + Akkusativ",
        "outra_frase": "Viele Experten glauben, dass ein gelockerter Markt zu mehr Wettbewerb führt.",
        "tradução_outra_frase": "Muitos especialistas acreditam que um mercado desregulamentado resulta em mais competição.",
        "reflexivo": False
    },
    {
        "verbo": "interpellieren",
        "tradução": "interpelar, questionar",
        "frase": "Der Abgeordnete interpelliert den Minister in der Sitzung und fordert klare Antworten.",
        "tradução_frase": "O deputado interpela o ministro na sessão e exige respostas claras.",
        "sinônimo": ["hinterfragen", "in Frage stellen"],
        "perfekt": "hat interpelliert",
        "präteritum": "interpellierte",
        "regência": "interpellieren + Akkusativ",
        "outra_frase": "In der Debatte wurde der Politiker wiederholt von kritischen Journalisten hinterfragt.",
        "tradução_outra_frase": "No debate, o político foi várias vezes interpelado por jornalistas críticos.",
        "reflexivo": False
    },
    {
        "verbo": "entpolitisieren",
        "tradução": "despolitizar",
        "frase": "Manche Themen versuchen Politiker zu entpolitisieren, um sachliche Diskussionen zu ermöglichen.",
        "tradução_frase": "Alguns temas os políticos tentam despolitizar para permitir debates mais objetivos.",
        "sinônimo": ["depolitisch machen", "neutralisieren"],
        "perfekt": "hat entpolitisiert",
        "präteritum": "entpolitisiert",
        "regência": "entpolitisieren (intransitiv)",
        "outra_frase": "Durch neutrale Analysen kann man oft heikle Diskussionen entpolitischen.",
        "tradução_outra_frase": "Por meio de análises neutras, frequentemente é possível despolitizar discussões delicadas.",
        "reflexivo": False
    },
    {
        "verbo": "polarisieren",
        "tradução": "polarizar",
        "frase": "Aktuelle Themen polarisieren die Gesellschaft und führen zu scharfen Debatten.",
        "tradução_frase": "Temas atuais polarizam a sociedade e levam a debates acalorados.",
        "sinônimo": ["spalten", "kontrastieren"],
        "perfekt": "hat polarisiert",
        "präteritum": "polarisierte",
        "regência": "polarisieren (intransitiv)",
        "outra_frase": "Die mediale Berichterstattung spaltet oft die öffentliche Meinung.",
        "tradução_outra_frase": "A cobertura midiática frequentemente polariza a opinião pública.",
        "reflexivo": False
    },
    {
        "verbo": "rationalisieren",
        "tradução": "racionalizar",
        "frase": "Umstrukturierungen zielen darauf ab, staatliche Ausgaben zu rationalisieren.",
        "tradução_frase": "Reestruturações visam racionalizar os gastos estatais.",
        "sinônimo": ["optimieren", "effizienter gestalten"],
        "perfekt": "hat rationalisiert",
        "präteritum": "rationalisierte",
        "regência": "rationalisieren + Akkusativ",
        "outra_frase": "Durch den Abbau von Bürokratie können Ressourcen effizienter gestaltet werden.",
        "tradução_outra_frase": "Com a redução da burocracia, os recursos podem ser racionalizados de forma mais eficaz.",
        "reflexivo": False
    },
    {
        "verbo": "subventionieren",
        "tradução": "subsidiar",
        "frase": "Der Staat subventioniert innovative Projekte, um wirtschaftliche Impulse zu setzen.",
        "tradução_frase": "O Estado subsidia projetos inovadores para estimular a economia.",
        "sinônimo": ["finanzieren", "bezuschussen"],
        "perfekt": "hat subventioniert",
        "präteritum": "subventionierte",
        "regência": "subventionieren + Akkusativ",
        "outra_frase": "Viele Kulturprojekte werden durch staatliche Zuschüsse finanziert.",
        "tradução_outra_frase": "Muitos projetos culturais são subsidiados pelo governo.",
        "reflexivo": False
    },
    {
        "verbo": "kompromittieren",
        "tradução": "comprometer, diskreditieren",
        "frase": "Skandale können das Vertrauen der Bevölkerung in die Regierung schnell kompromittieren.",
        "tradução_frase": "Escândalos podem comprometer rapidamente a confiança da população no governo.",
        "sinônimo": ["in Verruf bringen", "diskreditieren"],
        "perfekt": "hat kompromittiert",
        "präteritum": "kompromittierte",
        "regência": "kompromittieren + Akkusativ",
        "outra_frase": "Durch undurchsichtige Geschäfte wurde der Politiker in Verruf gebracht.",
        "tradução_outra_frase": "Através de negócios obscuros, o político acabou sendo comprometido.",
        "reflexivo": False
    },
    {
        "verbo": "revolutionieren",
        "tradução": "revolucionar",
        "frase": "Neue Technologien haben das Potenzial, ganze Wirtschaftssektoren zu revolutionieren.",
        "tradução_frase": "Novas tecnologias têm o potencial de revolucionar setores inteiros da economia.",
        "sinônimo": ["umwälzen", "transformieren"],
        "perfekt": "hat revolutioniert",
        "präteritum": "revolutionierte",
        "regência": "revolutionieren + Akkusativ",
        "outra_frase": "Innovative Ideen können bestehende Systeme grundlegend umwälzen.",
        "tradução_outra_frase": "Ideias inovadoras podem transformar radicalmente os sistemas existentes.",
        "reflexivo": False
    },
    {
        "verbo": "verschmutzen",
        "tradução": "poluir",
        "frase": "Industrielle Anlagen verschmutzen häufig Flüsse und Böden, was langfristige Umweltschäden verursacht.",
        "tradução_frase": "Instalações industriais poluem frequentemente rios e solos, causando danos ambientais a longo prazo.",
        "sinônimo": ["verunreinigen", "beflecken"],
        "perfekt": "hat verschmutzt",
        "präteritum": "verschmutzte",
        "regência": "verschmutzen + Akkusativ",
        "outra_frase": "Ohne konsequente Maßnahmen werden immer mehr Gewässer durch Chemikalien verschmutzt.",
        "tradução_outra_frase": "Sem medidas rigorosas, cada vez mais corpos d'água são poluídos por produtos químicos.",
        "reflexivo": False
    },
    {
        "verbo": "verunreinigen",
        "tradução": "contaminar",
        "frase": "Abwässer aus Fabriken verunreinigen oft das Grundwasser und gefährden die Trinkwasserversorgung.",
        "tradução_frase": "Esgotos de fábricas frequentemente contaminam os aquíferos, colocando em risco o abastecimento de água potável.",
        "sinônimo": ["verschmutzen", "beflecken"],
        "perfekt": "hat verunreinigt",
        "präteritum": "verunreinigte",
        "regência": "verunreinigen + Akkusativ",
        "outra_frase": "Die Behörden fordern strengere Kontrollen, um das Grundwasser vor weiteren Verunreinigungen zu schützen.",
        "tradução_outra_frase": "As autoridades exigem controles mais rigorosos para proteger os aquíferos de mais contaminações.",
        "reflexivo": False
    },
    {
        "verbo": "abholzen",
        "tradução": "desmatar",
        "frase": "Illegale Abholzungen in tropischen Regenwäldern tragen erheblich zum Klimawandel bei.",
        "tradução_frase": "O desmatamento ilegal em florestas tropicais contribui significativamente para as mudanças climáticas.",
        "sinônimo": ["entwalden", "roden"],
        "perfekt": "hat abgeholzt",
        "präteritum": "holzte ab",
        "regência": "abholzen (intransitiv)",
        "outra_frase": "Die internationale Gemeinschaft drängt auf Maßnahmen, um das Abholzen der Wälder zu stoppen.",
        "tradução_outra_frase": "A comunidade internacional pressiona por medidas para acabar com o desmatamento das florestas.",
        "reflexivo": False
    },
    {
        "verbo": "umweltschädigen",
        "tradução": "prejudicar o meio ambiente",
        "frase": "Der Einsatz bestimmter Chemikalien kann nicht nur Menschen, sondern auch ganze Ökosysteme umweltschädigen.",
        "tradução_frase": "O uso de determinados produtos químicos pode prejudicar não apenas as pessoas, mas também ecossistemas inteiros.",
        "sinônimo": ["beschädigen", "schädigen"],
        "perfekt": "hat umweltschädigt",
        "präteritum": "schädigte umwelt",
        "regência": "umweltschädigen (intransitiv)",
        "outra_frase": "Industrieemissionen tragen massiv dazu bei, dass zahlreiche Regionen umweltschädigt werden.",
        "tradução_outra_frase": "Emissões industriais contribuem significativamente para que muitas regiões sejam prejudicadas ambientalmente.",
        "reflexivo": False
    },
    {
        "verbo": "begrünen",
        "tradução": "tornar verde, vegetabilizar",
        "frase": "Städte versuchen, brachliegende Flächen zu begrünen, um das Stadtklima zu verbessern.",
        "tradução_frase": "Cidades tentam vegetabilizar áreas abandonadas para melhorar o clima urbano.",
        "sinônimo": ["begrünnen", "bepflanzen"],
        "perfekt": "hat begrüngt",
        "präteritum": "begrünte",
        "regência": "begrünen + Akkusativ",
        "outra_frase": "Durch umfangreiche Begrünungsprojekte können Luftqualität und Lebensqualität spürbar verbessert werden.",
        "tradução_outra_frase": "Por meio de projetos de vegetabilização, a qualidade do ar e de vida pode ser significativamente melhorada.",
        "reflexivo": False
    },
    {
        "verbo": "aufforsten",
        "tradução": "reflorestar",
        "frase": "Nach großflächigen Abholzungen wird versucht, die Wälder durch Aufforsten wiederherzustellen.",
        "tradução_frase": "Após desmatamentos em larga escala, tenta-se restaurar as florestas por meio do reflorestamento.",
        "sinônimo": ["wiederaufforsten", "aufforsten"],
        "perfekt": "ist aufgeforstet",
        "präteritum": "forstete auf",
        "regência": "aufforsten (intransitiv)",
        "outra_frase": "Naturschutzorganisationen setzen sich intensiv dafür ein, dass entwaldete Gebiete wieder aufgeforstet werden.",
        "tradução_outra_frase": "Organizações ambientalistas trabalham arduamente para que áreas desmatadas sejam reflorestadas.",
        "reflexivo": False
    },
    {
        "verbo": "einsparen",
        "tradução": "economizar, reduzir (Verbrauch)",
        "frase": "Haushalte sollten Energie einsparen, um den CO₂-Ausstoß zu verringern.",
        "tradução_frase": "Os lares devem economizar energia para reduzir a emissão de CO₂.",
        "sinônimo": ["sparen", "reduzieren"],
        "perfekt": "hat eingespart",
        "präteritum": "sparte ein",
        "regência": "einsparen (intransitiv)",
        "outra_frase": "Durch effiziente Technologien können Unternehmen im großen Stil Energie einsparen.",
        "tradução_outra_frase": "Por meio de tecnologias eficientes, empresas podem economizar energia em larga escala.",
        "reflexivo": False
    },
    {
        "verbo": "verbrauchen",
        "tradução": "consumir",
        "frase": "Der massive Verbrauch fossiler Brennstoffe treibt den Klimawandel voran.",
        "tradução_frase": "O consumo massivo de combustíveis fósseis acelera as mudanças climáticas.",
        "sinônimo": ["nutzen", "konsumieren"],
        "perfekt": "hat verbraucht",
        "präteritum": "verbrauchte",
        "regência": "verbrauchen + Akkusativ",
        "outra_frase": "Eine Senkung des Energieverbrauchs ist essenziell, um die Erderwärmung zu bremsen.",
        "tradução_outra_frase": "Reduzir o consumo de energia é essencial para conter o aquecimento global.",
        "reflexivo": False
    },
    {
        "verbo": "entsorgen",
        "tradução": "descartar, dispor",
        "frase": "Alte Elektrogeräte müssen fachgerecht entsorgt werden, um Schadstoffe nicht in die Umwelt freizusetzen.",
        "tradução_frase": "Equipamentos eletrônicos antigos devem ser descartados corretamente para evitar a liberação de substâncias tóxicas no meio ambiente.",
        "sinônimo": ["wegwerfen", "beseitigen"],
        "perfekt": "hat entsorgt",
        "präteritum": "entsorgte",
        "regência": "entsorgen + Akkusativ",
        "outra_frase": "Moderne Recyclingzentren sorgen dafür, dass Abfälle umweltgerecht entsorgt werden.",
        "tradução_outra_frase": "Centros modernos de reciclagem garantem que os resíduos sejam descartados de forma ambientalmente correta.",
        "reflexivo": False
    },
    {
        "verbo": "sammeln",
        "tradução": "coletar",
        "frase": "Bürgeraktionen sammeln Plastikmüll an Stränden, um die Meeresumwelt zu schützen.",
        "tradução_frase": "Ações comunitárias coletam lixo plástico nas praias para proteger o ambiente marinho.",
        "sinônimo": ["auflesen", "eintreiben"],
        "perfekt": "hat gesammelt",
        "präteritum": "sammlte",
        "regência": "sammeln (intransitiv, oft mit Akkusativobjekt)",
        "outra_frase": "In vielen Städten organisieren Freiwillige Sammelaktionen, um Abfälle zu reduzieren.",
        "tradução_outra_frase": "Em muitas cidades, voluntários organizam ações de coleta para reduzir os resíduos.",
        "reflexivo": False
    },
    {
        "verbo": "wiederverwenden",
        "tradução": "reutilizar",
        "frase": "Umweltfreundliche Firmen wiederverwenden alte Materialien, um Ressourcen zu schonen.",
        "tradução_frase": "Empresas ecologicamente corretas reutilizam materiais antigos para conservar recursos.",
        "sinônimo": ["recyceln", "wiederbenutzen"],
        "perfekt": "hat wiederverwendet",
        "präteritum": "wiederverwendete",
        "regência": "wiederverwenden + Akkusativ",
        "outra_frase": "Durch das Wiederverwenden von Verpackungen können Abfälle deutlich reduziert werden.",
        "tradução_outra_frase": "Reutilizando embalagens, é possível reduzir significativamente os resíduos.",
        "reflexivo": False
    },
    {
        "verbo": "aufbereiten",
        "tradução": "tratar, aufbereitar",
        "frase": "Moderne Kläranlagen bereiten Abwässer auf, bevor sie in Flüsse eingeleitet werden.",
        "tradução_frase": "Estações de tratamento modernas tratam os efluentes antes de liberá-los nos rios.",
        "sinônimo": ["reinigen", "verarbeiten"],
        "perfekt": "hat aufbereitet",
        "präteritum": "bereitete auf",
        "regência": "aufbereiten + Akkusativ",
        "outra_frase": "Durch die Aufbereitung von Wasser können auch in trockenen Regionen Ressourcen gespart werden.",
        "tradução_outra_frase": "Através do tratamento da água, é possível economizar recursos até em regiões áridas.",
        "reflexivo": False
    },
    {
        "verbo": "nachrüsten",
        "tradução": "modernizar, nachrüsten",
        "frase": "Viele alte Gebäude werden energetisch nachgerüstet, um den Wärmeverlust zu minimieren.",
        "tradução_frase": "Muitos prédios antigos são modernizados energeticamente para minimizar a perda de calor.",
        "sinônimo": ["aufrüsten", "modernisieren"],
        "perfekt": "hat nachgerüstet",
        "präteritum": "rüstete nach",
        "regência": "nachrüsten (intransitiv)",
        "outra_frase": "Staatliche Förderprogramme helfen, dass Haushalte ihre Heizsysteme nachrüsten können.",
        "tradução_outra_frase": "Programas governamentais auxiliam as famílias a modernizarem seus sistemas de aquecimento.",
        "reflexivo": False
    },
    {
        "verbo": "umstellen",
        "tradução": "mudar, converter",
        "frase": "Viele Industrien stellen ihre Produktion um, um auf erneuerbare Energien zu setzen.",
        "tradução_frase": "Muitas indústrias estão convertendo suas produções para utilizar fontes de energia renovável.",
        "sinônimo": ["wechseln", "anpassen"],
        "perfekt": "hat umgestellt",
        "präteritum": "stellte um",
        "regência": "umstellen (intransitiv, oft mit Präpositionalobjekt)",
        "outra_frase": "Die Umstellung auf Solarenergie ist ein wichtiger Schritt im Kampf gegen den Klimawandel.",
        "tradução_outra_frase": "A transição para a energia solar é um passo importante no combate às mudanças climáticas.",
        "reflexivo": False
    },
    {
        "verbo": "abkühlen",
        "tradução": "resfriar, esfriar",
        "frase": "In Hitzewellen ist es wichtig, Innenräume durch Ventilation abzukühlen.",
        "tradução_frase": "Durante ondas de calor, é importante resfriar ambientes internos por meio de ventilação.",
        "sinônimo": ["kühlen", "erniedrigen"],
        "perfekt": "hat abgekühlt",
        "präteritum": "kühlte ab",
        "regência": "abkühlen (intransitiv)",
        "outra_frase": "Moderne Kühlsysteme helfen, die Temperaturen in Bürogebäuden abzukühlen.",
        "tradução_outra_frase": "Sistemas modernos de refrigeração ajudam a baixar a temperatura em prédios comerciais.",
        "reflexivo": False
    },
    {
        "verbo": "aufheizen",
        "tradução": "aquecer",
        "frase": "Der Treibhauseffekt führt dazu, dass die Erdatmosphäre sich zunehmend aufheizt.",
        "tradução_frase": "O efeito estufa faz com que a atmosfera terrestre se aqueça cada vez mais.",
        "sinônimo": ["erwärmen", "aufwärmen"],
        "perfekt": "hat aufgeheizt",
        "präteritum": "heizte auf",
        "regência": "aufheizen (intransitiv)",
        "outra_frase": "Wissenschaftler warnen, dass ein unkontrolliertes Aufheizen des Klimas katastrophale Folgen haben könnte.",
        "tradução_outra_frase": "Cientistas alertam que o aquecimento descontrolado do clima pode ter consequências catastróficas.",
        "reflexivo": False
    },
    {
        "verbo": "abbauen",
        "tradução": "desconstruir, reduzir, extrair, decompor",
        "frase": "Der intensive Abbau fossiler Brennstoffe belastet nicht nur die Umwelt, sondern treibt auch den Klimawandel voran.",
        "tradução_frase": "A extração intensiva de combustíveis fósseis não só prejudica o meio ambiente como também acelera as mudanças climáticas.",
        "sinônimo": ["fördern", "extrahieren"],
        "perfekt": "hat abgebaut",
        "präteritum": "baute ab",
        "regência": "abbauen + Akkusativ",
        "outra_frase": "Strengere Umweltauflagen sollen den Abbau schädlicher Ressourcen einschränken.",
        "tradução_outra_frase": "Normas ambientais mais rigorosas devem limitar a extração de recursos prejudiciais.",
        "reflexivo": False
    },
    {
        "verbo": "ausbeuten",
        "tradução": "explorar (negativo)",
        "frase": "Die unkontrollierte Ausbeutung natürlicher Ressourcen gefährdet langfristig die ökologische Balance.",
        "tradução_frase": "A exploração descontrolada dos recursos naturais ameaça o equilíbrio ecológico a longo prazo.",
        "sinônimo": ["übernutzen", "ausnutzen"],
        "perfekt": "hat ausgebeutet",
        "präteritum": "beutete aus",
        "regência": "ausbeuten + Akkusativ",
        "outra_frase": "Viele Umweltschützer kritisieren, dass Unternehmen die Natur zu stark ausbeuten.",
        "tradução_outra_frase": "Muitos ambientalistas criticam que as empresas exploram excessivamente a natureza.",
        "reflexivo": False
    },
    {
        "verbo": "wiederaufbauen",
        "tradução": "reconstruir",
        "frase": "Nach Naturkatastrophen versuchen Gemeinden, beschädigte Ökosysteme wiederaufzubauen.",
        "tradução_frase": "Após catástrofes naturais, comunidades tentam reconstruir ecossistemas danificados.",
        "sinônimo": ["restaurieren", "erneuern"],
        "perfekt": "hat wiederaufgebaut",
        "präteritum": "baute wiederauf",
        "regência": "wiederaufbauen + Akkusativ",
        "outra_frase": "Die Wiederaufbauarbeiten in betroffenen Regionen verlaufen langsam, aber stetig.",
        "tradução_outra_frase": "Os trabalhos de reconstrução em áreas afetadas estão ocorrendo de forma lenta, porém constante.",
        "reflexivo": False
    },
    {
        "verbo": "einpflanzen",
        "tradução": "plantar",
        "frase": "Freiwillige Gruppen pflanzen Bäume ein, um den Verlust an Waldflächen zu kompensieren.",
        "tradução_frase": "Grupos de voluntários plantam árvores para compensar a perda de áreas florestais.",
        "sinônimo": ["anpflanzen", "bepflanzen"],
        "perfekt": "hat eingepflanzt",
        "präteritum": "pflanzte ein",
        "regência": "einpflanzen + Akkusativ",
        "outra_frase": "In Schulen werden Projekte gestartet, bei denen Schüler gemeinsam Bäume einpflanzen.",
        "tradução_outra_frase": "Em escolas, projetos incentivam os alunos a plantar árvores juntos.",
        "reflexivo": False
    },
    {
        "verbo": "senken",
        "tradução": "reduzir, diminuir, abaixar",
        "frase": "Politische Maßnahmen zielen darauf ab, den Ausstoß von Treibhausgasen zu senken.",
        "tradução_frase": "Medidas políticas têm como objetivo reduzir a emissão de gases de efeito estufa.",
        "sinônimo": ["verringern", "minimieren"],
        "perfekt": "hat gesenkt",
        "präteritum": "senkte",
        "regência": "senken + Akkusativ",
        "outra_frase": "Mit innovativen Technologien lassen sich die Emissionen in der Industrie deutlich senken.",
        "tradução_outra_frase": "Com tecnologias inovadoras, as emissões na indústria podem ser significativamente reduzidas.",
        "reflexivo": False
    },
    {
        "verbo": "abschirmen",
        "tradução": "proteger, isolar, blindar",
        "frase": "Grüne Dächer helfen, Gebäude vor extremer Hitze abzuschirmen.",
        "tradução_frase": "Telhados verdes ajudam a proteger os edifícios contra o calor extremo.",
        "sinônimo": ["schirmen", "schützen"],
        "perfekt": "hat abgeschirmt",
        "präteritum": "schirmte ab",
        "regência": "abschirmen + Akkusativ",
        "outra_frase": "Innovative Baustoffe können dazu beitragen, dass Häuser besser gegen Umweltbelastungen abgeschirmt werden.",
        "tradução_outra_frase": "Materiais de construção inovadores podem ajudar a proteger as casas contra agressões ambientais.",
        "reflexivo": False
    },
    {
        "verbo": "reinigen",
        "tradução": "limpar, higienizar",
        "frase": "Nach einem Ölunfall müssen die betroffenen Küstenbereiche schnell gereinigt werden.",
        "tradução_frase": "Após um derramamento de óleo, as áreas costeiras afetadas precisam ser rapidamente limpas.",
        "sinônimo": [" säubern", "putzen"],
        "perfekt": "hat gereinigt",
        "präteritum": "reinigte",
        "regência": "reinigen + Akkusativ",
        "outra_frase": "Umweltteams sind im Einsatz, um verseuchte Strände gründlich zu reinigen.",
        "tradução_outra_frase": "Equipes ambientais estão trabalhando para limpar minuciosamente praias contaminadas.",
        "reflexivo": False
    },
    {
        "verbo": "abschöpfen",
        "tradução": "retirar, esgotar, aproveitar",
        "frase": "Bei einem Ölteppich auf dem Wasser versuchen Einsatzkräfte, das Öl von der Oberfläche abzuschöpfen.",
        "tradução_frase": "Em derramamentos de óleo na água, as equipes de resgate tentam retirar o óleo da superfície.",
        "sinônimo": ["abtrennen", "sammeln"],
        "perfekt": "hat abgeschöpft",
        "präteritum": "schöpfte ab",
        "regência": "abschöpfen + Akkusativ",
        "outra_frase": "Mit speziellen Geräten wird das Öl von der Meeresoberfläche abgeschöpft, um weitere Schäden zu vermeiden.",
        "tradução_outra_frase": "Equipamentos especiais são usados para retirar o óleo da superfície do mar e prevenir danos adicionais.",
        "reflexivo": False
    },
    {
        "verbo": "zurückhalten",
        "tradução": "reprimir, conter, reter",
        "frase": "Durch technische Innovationen können Unternehmen ihre CO₂-Emissionen besser zurückhalten.",
        "tradução_frase": "Por meio de inovações tecnológicas, as empresas podem reduzir melhor suas emissões de CO₂.",
        "sinônimo": ["reduzieren", "senken"],
        "perfekt": "hat zurückgehalten",
        "präteritum": "hielt zurück",
        "regência": "zurückhalten + Akkusativ",
        "outra_frase": "Neue Verfahren zielen darauf ab, schädliche Emissionen im industriellen Bereich zurückzuhalten.",
        "tradução_outra_frase": "Novos métodos visam conter emissões prejudiciais no setor industrial.",
        "reflexivo": False
    },
    {
        "verbo": "dämmen",
        "tradução": "isolar, conter, reduzir",
        "frase": "Moderne Gebäude werden mit hochwertigen Materialien gedämmt, um Energieverluste zu minimieren.",
        "tradução_frase": "Edifícios modernos são isolados com materiais de alta qualidade para minimizar perdas de energia.",
        "sinônimo": ["isolieren", "polstern"],
        "perfekt": "hat gedämmt",
        "präteritum": "dämmerte",
        "regência": "dämmen (intransitiv, oft mit Präpositionalobjekt)",
        "outra_frase": "Eine gute Dämmung hilft, den Energieverbrauch in kalten Wintermonaten drastisch zu senken.",
        "tradução_outra_frase": "Um bom isolamento ajuda a reduzir drasticamente o consumo de energia nos meses frios.",
        "reflexivo": False
    },
    {
        "verbo": "abkoppeln",
        "tradução": "desacoplar, desconectar, separar",
        "frase": "Um die Wirtschaft umweltfreundlicher zu gestalten, will man die Abhängigkeit von fossilen Brennstoffen abkoppeln.",
        "tradução_frase": "Para tornar a economia mais ecológica, busca-se desvincular a dependência de combustíveis fósseis.",
        "sinônimo": ["entkoppeln", "trennen"],
        "perfekt": "hat abgekoppelt",
        "präteritum": "koppelte ab",
        "regência": "abkoppeln (intransitiv)",
        "outra_frase": "Experten diskutieren, wie man den Industriesektor von umweltschädlichen Praktiken abkoppeln kann.",
        "tradução_outra_frase": "Especialistas debatem como desvincular o setor industrial de práticas prejudiciais ao meio ambiente.",
        "reflexivo": False
    },
     {
        "verbo": "ernähren",
        "tradução": "alimentar, nutrir",
        "frase": "Er legt großen Wert darauf, sich gesund zu ernähren, um fit zu bleiben.",
        "tradução_frase": "Ele dá muita importância a se alimentar de forma saudável para se manter em forma.",
        "sinônimo": ["sich speisen", "sich versorgen"],
        "perfekt": "hat sich ernährt",
        "präteritum": "ernährte sich",
        "regência": "sich ernähren von + Dativ",
        "outra_frase": "Viele Sportler ernähren sich ausgewogen, um ihre Leistungsfähigkeit zu steigern.",
        "tradução_outra_frase": "Muitos atletas se alimentam de forma equilibrada para aumentar seu desempenho.",
        "reflexivo": True
    },
    {
        "verbo": "zubereiten",
        "tradução": "preparar",
        "frase": "Die Köchin bereitet täglich frische Gerichte zu, die bei den Gästen sehr beliebt sind.",
        "tradução_frase": "A cozinheira prepara pratos frescos diariamente, que são muito apreciados pelos clientes.",
        "sinônimo": ["vorbereiten", "kochen"],
        "perfekt": "hat zubereitet",
        "präteritum": "bereitete zu",
        "regência": "zubereiten + Akkusativ",
        "outra_frase": "Für das Festessen hat er ein besonderes Menü zusammengestellt und liebevoll zubereitet.",
        "tradução_outra_frase": "Para o banquete, ele montou um menu especial e preparou com carinho.",
        "reflexivo": False
    },
    {
        "verbo": "kochen",
        "tradução": "cozinhar",
        "frase": "Jeden Abend kocht sie ein neues Rezept, um ihre Familie zu überraschen.",
        "tradução_frase": "Todas as noites, ela cozinha uma receita nova para surpreender a família.",
        "sinônimo": ["garen", "zubereiten"],
        "perfekt": "hat gekocht",
        "präteritum": "kochte",
        "regência": "kochen (intransitiv) oder kochen + Akkusativ (für Speisen)",
        "outra_frase": "In der Kochschule lernten die Teilnehmer, wie man traditionelle Gerichte richtig kocht.",
        "tradução_outra_frase": "Na escola de culinária, os participantes aprenderam como cozinhar pratos tradicionais corretamente.",
        "reflexivo": False
    },
    {
        "verbo": "backen",
        "tradução": "assar",
        "frase": "Am Sonntag backt er Brot und Kuchen, was den ganzen Haushalt mit angenehmen Düften erfüllt.",
        "tradução_frase": "No domingo, ele assa pães e bolos, enchendo toda a casa com aromas agradáveis.",
        "sinônimo": ["ofen", "zubereiten"],
        "perfekt": "hat gebacken",
        "präteritum": "backte",
        "regência": "backen (intransitiv) oder backen + Akkusativ (für Backwaren)",
        "outra_frase": "Viele Bäcker backen täglich frische Brötchen, um den Morgen zu versüßen.",
        "tradução_outra_frase": "Muitos padeiros assam pães frescos diariamente para adoçar a manhã.",
        "reflexivo": False
    },
    {
        "verbo": "braten",
        "tradução": "fritar, assar (em frigideira)",
        "frase": "Zum Mittagessen brät er das Fleisch in der Pfanne, bis es goldbraun ist.",
        "tradução_frase": "No almoço, ele frita a carne na frigideira até que fique dourada.",
        "sinônimo": ["anbraten", "grillen"],
        "perfekt": "hat gebraten",
        "präteritum": "bratete",
        "regência": "braten + Akkusativ",
        "outra_frase": "In traditionellen Rezepten wird das Gemüse oft zusammen mit Fleisch gebraten.",
        "tradução_outra_frase": "Em receitas tradicionais, os vegetais são frequentemente fritos junto com a carne.",
        "reflexivo": False
    },
    {
        "verbo": "dünsten",
        "tradução": "cozer a vapor, refogar suavemente",
        "frase": "Um die Nährstoffe zu bewahren, lässt sie das Gemüse schonend dünsten.",
        "tradução_frase": "Para preservar os nutrientes, ela deixa o vegetal cozinhar suavemente a vapor.",
        "sinônimo": ["garen", "dämpfen"],
        "perfekt": "hat gedünstet",
        "präteritum": "dünstete",
        "regência": "dünsten + Akkusativ",
        "outra_frase": "Beim Dünsten bleiben die Vitamine weitgehend erhalten, was die Speisen gesünder macht.",
        "tradução_outra_frase": "Ao refogar suavemente, as vitaminas se mantêm, tornando os pratos mais saudáveis.",
        "reflexivo": False
    },
    {
        "verbo": "garen",
        "tradução": "cozinhar lentamente",
        "frase": "Für ein besonders zartes Fleischgericht muss das Fleisch lange garen.",
        "tradução_frase": "Para um prato de carne especialmente macio, é necessário cozinhar a carne lentamente.",
        "sinônimo": ["kochen", "dünsten"],
        "perfekt": "hat gegart",
        "präteritum": "garte",
        "regência": "garen + Akkusativ",
        "outra_frase": "In traditionellen Rezepten wird das Fleisch oft stundenlang gegart, um den Geschmack zu intensivieren.",
        "tradução_outra_frase": "Em receitas tradicionais, a carne é cozida por horas para intensificar o sabor.",
        "reflexivo": False
    },
    {
        "verbo": "abschmecken",
        "tradução": "temperar, ajustar o sabor",
        "frase": "Bevor das Essen serviert wird, muss es noch sorgfältig abgeschmeckt werden.",
        "tradução_frase": "Antes de servir a comida, é preciso temperá-la cuidadosamente.",
        "sinônimo": ["würzen", "verfeinern"],
        "perfekt": "hat abgeschmeckt",
        "präteritum": "schmackspeckte ab",
        "regência": "abschmecken + Akkusativ",
        "outra_frase": "Ein guter Koch weiß, wie man mit Kräutern und Gewürzen ein Gericht richtig abschmeckt.",
        "tradução_outra_frase": "Um bom cozinheiro sabe como ajustar o sabor de um prato com ervas e especiarias.",
        "reflexivo": False
    },
    {
        "verbo": "schälen",
        "tradução": "descascar",
        "frase": "Für den Salat muss man die Kartoffeln zunächst schälen und in Scheiben schneiden.",
        "tradução_frase": "Para a salada, é preciso descascar as batatas e cortá-las em fatias.",
        "sinônimo": ["entfernen", "abziehen"],
        "perfekt": "hat geschält",
        "präteritum": "schälte",
        "regência": "schälen + Akkusativ",
        "outra_frase": "Beim Backen empfiehlt es sich, Obst zu schälen, um eine glatte Konsistenz zu erreichen.",
        "tradução_outra_frase": "Ao assar, recomenda-se descascar as frutas para obter uma consistência suave.",
        "reflexivo": False
    },
    {
        "verbo": "kauen",
        "tradução": "mastigar",
        "frase": "Es ist wichtig, gut zu kauen, damit die Verdauung optimal funktioniert.",
        "tradução_frase": "É importante mastigar bem para que a digestão funcione de maneira ideal.",
        "sinônimo": ["zerkauen", "mampfen"],
        "perfekt": "hat gekaut",
        "präteritum": "kaute",
        "regência": "kauen (intransitiv)",
        "outra_frase": "Die Ärzte empfehlen, langsam zu kauen, um die Nährstoffaufnahme zu verbessern.",
        "tradução_outra_frase": "Os médicos recomendam mastigar devagar para melhorar a absorção de nutrientes.",
        "reflexivo": False
    },
    {
        "verbo": "schlucken",
        "tradução": "engolir",
        "frase": "Nach dem scharfen Essen musste er mehrmals Wasser schlucken, um den Geschmack zu mildern.",
        "tradução_frase": "Após a comida picante, ele precisou engolir água várias vezes para amenizar o sabor.",
        "sinônimo": ["hinunterschlucken", "runterschlucken"],
        "perfekt": "hat geschluckt",
        "präteritum": "schluckte",
        "regência": "schlucken (intransitiv)",
        "outra_frase": "Beim schnellen Essen kann man leicht unbewusst Luft mitschlucken, was zu Beschwerden führt.",
        "tradução_outra_frase": "Ao comer rápido, pode-se engolir ar sem perceber, o que causa desconforto.",
        "reflexivo": False
    },
    {
        "verbo": "genießen",
        "tradução": "desfrutar, saborear",
        "frase": "Es lohnt sich, jeden Bissen zu genießen, um das volle Aroma des Essens zu erleben.",
        "tradução_frase": "Vale a pena saborear cada mordida para experimentar todo o aroma da comida.",
        "sinônimo": ["schlemmen", "sich erfreuen"],
        "perfekt": "hat genossen",
        "präteritum": "genoss",
        "regência": "genießen (intransitiv) oder genießen + Akkusativ (das Essen)",
        "outra_frase": "Viele Feinschmecker genießen es, neue Geschmacksrichtungen zu entdecken.",
        "tradução_outra_frase": "Muitos gourmets gostam de descobrir novos sabores.",
        "reflexivo": False
    },
    {
        "verbo": "verzehren",
        "tradução": "consumir",
        "frase": "In der Kantine werden täglich große Mengen gesunder Speisen verzehrt.",
        "tradução_frase": "Na cantina, grandes quantidades de alimentos saudáveis são consumidas diariamente.",
        "sinônimo": ["essen", "konsumieren"],
        "perfekt": "hat verzehrt",
        "präteritum": "verzehrte",
        "regência": "verzehren + Akkusativ",
        "outra_frase": "Bei festlichen Anlässen verzehren die Gäste in aller Regel reichhaltige Buffets.",
        "tradução_outra_frase": "Em ocasiões festivas, os convidados geralmente consomem bufês fartos.",
        "reflexivo": False
    },
    {
        "verbo": "mischen",
        "tradução": "misturar",
        "frase": "Für den Smoothie werden verschiedene Früchte miteinander gemischt.",
        "tradução_frase": "Para o smoothie, diversas frutas são misturadas entre si.",
        "sinônimo": ["verrühren", "verbinden"],
        "perfekt": "hat gemischt",
        "präteritum": "mischte",
        "regência": "mischen + Akkusativ",
        "outra_frase": "In der Küche ist es wichtig, Zutaten gründlich zu mischen, um einen homogenen Geschmack zu erzielen.",
        "tradução_outra_frase": "Na cozinha, é importante misturar bem os ingredientes para obter um sabor homogêneo.",
        "reflexivo": False
    },
    {
        "verbo": "sieden",
        "tradução": "cozer em fervura",
        "frase": "Das Wasser muss lange sieden, damit sich alle Aromen der Kräuter entfalten können.",
        "tradução_frase": "A água precisa ferver por bastante tempo para que os aromas das ervas se desenvolvam.",
        "sinônimo": ["kochen", "köcheln"],
        "perfekt": "hat gesieden",
        "präteritum": "siedete",
        "regência": "sieden (intransitiv)",
        "outra_frase": "In traditionellen Rezepten sieden Suppen oft stundenlang, um ihren vollen Geschmack zu entfalten.",
        "tradução_outra_frase": "Em receitas tradicionais, as sopas muitas vezes ferver por horas para desenvolver seu sabor completo.",
        "reflexivo": False
    },
    {
        "verbo": "aufkochen",
        "tradução": "levar ao ponto de fervura",
        "frase": "Bevor man Nudeln kocht, bringt man das Wasser erst richtig auf.",
        "tradução_frase": "Antes de cozinhar o macarrão, primeiro faz-se a água ferver completamente.",
        "sinônimo": ["zum Kochen bringen", "erhitzen"],
        "perfekt": "hat aufgekocht",
        "präteritum": "kochte auf",
        "regência": "aufkochen (intransitiv)",
        "outra_frase": "In vielen Rezepten ist es wichtig, die Brühe erst aufkochen zu lassen, bevor weitere Zutaten hinzugegeben werden.",
        "tradução_outra_frase": "Em muitas receitas, é importante deixar o caldo ferver antes de adicionar os demais ingredientes.",
        "reflexivo": False
    },
    {
        "verbo": "dämpfen",
        "tradução": "cozer no vapor",
        "frase": "Um Gemüse kann man schonend dämpfen, um alle Vitamine zu erhalten.",
        "tradução_frase": "Um vegetal pode ser cozido no vapor de forma suave para preservar todas as vitaminas.",
        "sinônimo": ["dünsten", "garen"],
        "perfekt": "hat gedämpft",
        "präteritum": "dämpfte",
        "regência": "dämpfen + Akkusativ",
        "outra_frase": "Viele Diäten empfehlen, Speisen zu dämpfen, anstatt sie zu braten.",
        "tradução_outra_frase": "Muitas dietas recomendam cozinhar os alimentos no vapor em vez de fritá-los.",
        "reflexivo": False
    },
    {
        "verbo": "abnehmen",
        "tradução": "perder (Gewicht)",
        "frase": "Durch eine ausgewogene Ernährung und regelmäßige Bewegung kann man leicht abnehmen.",
        "tradução_frase": "Com uma alimentação equilibrada e exercícios regulares, é possível perder peso facilmente.",
        "sinônimo": ["schlank werden", "reduzieren"],
        "perfekt": "hat abgenommen",
        "präteritum": "nahm ab",
        "regência": "abnehmen (intransitiv)",
        "outra_frase": "Viele Diätprogramme versprechen, dass man schnell abnehmen kann, wenn man auf Zucker verzichtet.",
        "tradução_outra_frase": "Muitos programas de dieta prometem perda de peso rápida ao evitar o açúcar.",
        "reflexivo": False
    },
    {
        "verbo": "zunehmen",
        "tradução": "ganhar (Gewicht)",
        "frase": "Ein Mangel an Bewegung und ungesunde Ernährung können dazu führen, dass man ungewollt zunimmt.",
        "tradução_frase": "A falta de atividade física e uma alimentação pouco saudável podem fazer com que se ganhe peso indesejadamente.",
        "sinônimo": ["an Gewicht gewinnen", "sich anreichern"],
        "perfekt": "hat zugenommen",
        "präteritum": "nahm zu",
        "regência": "zunehmen (intransitiv)",
        "outra_frase": "Ohne ausreichende Bewegung nehmen viele Menschen im Alter automatisch zu.",
        "tradução_outra_frase": "Sem atividade física suficiente, muitas pessoas ganham peso à medida que envelhecem.",
        "reflexivo": False
    },
    {
        "verbo": "ausgleichen",
        "tradução": "equilibrar, balancear, nivelar",
        "frase": "Um den Blutzuckerspiegel stabil zu halten, sollte man Mahlzeiten gut ausleichen.",
        "tradução_frase": "Para manter os níveis de açúcar no sangue estáveis, as refeições devem ser bem balanceadas.",
        "sinônimo": ["balancieren", "angleichen"],
        "perfekt": "hat ausgeglichen",
        "präteritum": "glich aus",
        "regência": "ausleichen (intransitiv)",
        "outra_frase": "Sport und Ernährung müssen miteinander ausbalanciert werden, um optimale Gesundheit zu fördern.",
        "tradução_outra_frase": "Exercício e alimentação precisam ser balanceados para promover uma saúde ideal.",
        "reflexivo": False
    },
    {
        "verbo": "lagern",
        "tradução": "armazenar",
        "frase": "Frische Lebensmittel sollten kühl gelagert werden, um ihre Haltbarkeit zu verlängern.",
        "tradução_frase": "Alimentos frescos devem ser armazenados em ambiente frio para prolongar sua durabilidade.",
        "sinônimo": ["aufbewahren", "speichern"],
        "perfekt": "hat gelagert",
        "präteritum": "lagerte",
        "regência": "lagern + Akkusativ",
        "outra_frase": "Die richtige Lagerung von Obst und Gemüse verhindert, dass sie schnell verderben.",
        "tradução_outra_frase": "O armazenamento correto de frutas e vegetais impede que estraguem rapidamente.",
        "reflexivo": False
    },
    {
        "verbo": "aufbewahren",
        "tradução": "conservar, guardar",
        "frase": "Gewürze sollten lichtgeschützt aufbewahrt werden, um ihr Aroma zu bewahren.",
        "tradução_frase": "Especiarias devem ser guardadas à sombra para preservar seu aroma.",
        "sinônimo": ["lagern", "sichern"],
        "perfekt": "hat aufbewahrt",
        "präteritum": "bewahrte auf",
        "regência": "aufbewahren + Akkusativ",
        "outra_frase": "In der Küche ist es wichtig, Lebensmittel richtig aufzubewahren, um Verschwendung zu vermeiden.",
        "tradução_outra_frase": "Na cozinha, é importante conservar os alimentos corretamente para evitar o desperdício.",
        "reflexivo": False
    },
    {
        "verbo": "verwerten",
        "tradução": "utilizar, aproveitar, reaproveitar",
        "frase": "Übrig gebliebene Reste können kreativ verwertet werden, um neue Gerichte zu kreieren.",
        "tradução_frase": "Restos que sobraram podem ser aproveitados criativamente para criar novos pratos.",
        "sinônimo": ["nutzen", "wiederverwenden"],
        "perfekt": "hat verwertet",
        "präteritum": "verwertete",
        "regência": "verwerten + Akkusativ",
        "outra_frase": "Viele Küchenchefs zeigen, wie man Lebensmittelverschwendung vermeidet, indem man Reste sinnvoll verwertet.",
        "tradução_outra_frase": "Muitos chefs demonstram como evitar o desperdício de alimentos aproveitando as sobras de maneira inteligente.",
        "reflexivo": False
    },
    {
        "verbo": "schlemmen",
        "tradução": "fartar-se, banquetejar",
        "frase": "Zum Feiertag schlemmen die Gäste ausgiebig, ohne an die Kalorien zu denken.",
        "tradução_frase": "No feriado, os convidados se deleitam em um banquete, sem se preocupar com as calorias.",
        "sinônimo": ["schmausen", "schmausen"],
        "perfekt": "hat geschlemmt",
        "präteritum": "schlemmt",
        "regência": "schlemmen (intransitiv)",
        "outra_frase": "Beim jährlichen Fest schlemmen die Teilnehmer, was zu einem ausgelassenen Beisammensein führt.",
        "tradução_outra_frase": "No festival anual, os participantes se banqueteiam, promovendo uma convivência animada.",
        "reflexivo": False
    },
    {
        "verbo": "naschen",
        "tradução": "petiscar, beliscar",
        "frase": "Zwischendurch nascht sie gern an frischem Obst, um den kleinen Hunger zu stillen.",
        "tradução_frase": "Entre as refeições, ela gosta de petiscar frutas frescas para matar a fome leve.",
        "sinônimo": ["knabbern", "snacken"],
        "perfekt": "hat genascht",
        "präteritum": "naschte",
        "regência": "naschen (intransitiv)",
        "outra_frase": "Kinder naschen oft heimlich Süßigkeiten, wenn sie dachten, niemand würde es bemerken.",
        "tradução_outra_frase": "As crianças frequentemente beliscam doces às escondidas, achando que ninguém perceberia.",
        "reflexivo": False
    },
    {
        "verbo": "würzen",
        "tradução": "temperar",
        "frase": "Man sollte das Gericht erst am Ende würzen, um die frischen Kräuter nicht zu verlieren.",
        "tradução_frase": "Deve-se temperar o prato somente no final, para não perder as ervas frescas.",
        "sinônimo": ["abschmecken", "verfeinern"],
        "perfekt": "hat gewürzt",
        "präteritum": "würzte",
        "regência": "würzen + Akkusativ",
        "outra_frase": "Viele Köche betonen, dass richtig gewürzte Speisen den Unterschied im Geschmack ausmachen.",
        "tradução_outra_frase": "Muitos chefs enfatizam que alimentos bem temperados fazem toda a diferença no sabor.",
        "reflexivo": False
    },
    {
        "verbo": "mahlen",
        "tradução": "moer",
        "frase": "Frische Kräuter werden in der Mühle fein gemahlen, um sie als Gewürz zu verwenden.",
        "tradução_frase": "Ervas frescas são moídas finamente no moinho para serem usadas como tempero.",
        "sinônimo": ["zerstoßen", "pulverisieren"],
        "perfekt": "hat gemahlen",
        "präteritum": "mahlte",
        "regência": "mahlen + Akkusativ",
        "outra_frase": "In vielen traditionellen Küchen wird Getreide von Hand gemahlen, um Mehl herzustellen.",
        "tradução_outra_frase": "Em muitas cozinhas tradicionais, os grãos são moídos manualmente para produzir farinha.",
        "reflexivo": False
    },
    {
        "verbo": "pürieren",
        "tradução": "triturar, fazer purê, zu Brei verarbeiten",
        "frase": "Die Suppe wird glatt püriert, bevor sie serviert wird.",
        "tradução_frase": "A sopa é batida até ficar homogênea antes de ser servida.",
        "sinônimo": ["zerdrücken", "verarbeiten"],
        "perfekt": "hat püriert",
        "präteritum": "pürierte",
        "regência": "pürieren + Akkusativ",
        "outra_frase": "Ein guter Mixer hilft, Obst zu pürieren und so leckere Smoothies zu kreieren.",
        "tradução_outra_frase": "Um bom liquidificador auxilia na produção de smoothies saborosos ao purar frutas.",
        "reflexivo": False
    },
    {
        "verbo": "anrichten",
        "tradução": "preparar, servir, causar (negativo)",
        "frase": "Der Teller wird kunstvoll angerichtet, bevor er serviert wird.",
        "tradução_frase": "O prato é decorado artisticamente antes de ser servido.",
        "sinônimo": ["präsentieren", "arrangieren"],
        "perfekt": "hat angerichtet",
        "präteritum": "richtete an",
        "regência": "anrichten + Akkusativ",
        "outra_frase": "In gehobenen Restaurants wird viel Wert darauf gelegt, dass die Speisen ansprechend angerichtet sind.",
        "tradução_outra_frase": "Em restaurantes sofisticados, dá-se muita importância à apresentação atrativa dos pratos.",
        "reflexivo": False
    },
    {
        "verbo": "abwehren",
        "tradução": "repelir, defender",
        "frase": "Das Immunsystem wehrt Krankheitserreger ab, um Infektionen zu verhindern.",
        "tradução_frase": "O sistema imunológico repele os agentes patogênicos para evitar infecções.",
        "sinônimo": ["verteidigen", "bekämpfen"],
        "perfekt": "hat abgewehrt",
        "präteritum": "wehrte ab",
        "regência": "abwehren + Akkusativ",
        "outra_frase": "Regelmäßige Bewegung kann dem Körper helfen, schädliche Erreger besser abzuwehren.",
        "tradução_outra_frase": "Exercícios regulares podem ajudar o corpo a repelir melhor os agentes nocivos.",
        "reflexivo": False
    },
    {
        "verbo": "auskurieren",
        "tradução": "curar completamente",
        "frase": "Nach einer Grippe sollte man sich vollständig auskurieren, um Rückfälle zu vermeiden.",
        "tradução_frase": "Após uma gripe, é preciso se curar completamente para evitar recaídas.",
        "sinônimo": ["genesen", "ausheilen"],
        "perfekt": "hat sich auskuriert",
        "präteritum": "kurierte sich aus",
        "regência": "sich auskurieren",
        "outra_frase": "Manchmal ist es besser, eine Krankheit langsam auszukurieren, als sich zu früh zu belasten.",
        "tradução_outra_frase": "Às vezes, é melhor curar uma doença lentamente do que se esforçar prematuramente.",
        "reflexivo": True
    },
    {
        "verbo": "behandeln",
        "tradução": "tratar",
        "frase": "Der Arzt behandelte den Patienten mit einer Kombination aus Medikamenten und Ruhe.",
        "tradução_frase": "O médico tratou o paciente com uma combinação de medicamentos e repouso.",
        "sinônimo": ["therapieren", "versorgen"],
        "perfekt": "hat behandelt",
        "präteritum": "behandelte",
        "regência": "behandeln + Akkusativ",
        "outra_frase": "Um Infektionen vorzubeugen, sollte man Wunden sofort richtig behandeln.",
        "tradução_outra_frase": "Para prevenir infecções, é necessário tratar os ferimentos corretamente imediatamente.",
        "reflexivo": False
    },
    {
        "verbo": "verdauen",
        "tradução": "digerir",
        "frase": "Schwere Speisen brauchen länger, um verdaut zu werden.",
        "tradução_frase": "Alimentos pesados demoram mais para serem digeridos.",
        "sinônimo": ["aufspalten", "zersetzen"],
        "perfekt": "hat verdaut",
        "präteritum": "verdaute",
        "regência": "verdauen + Akkusativ",
        "outra_frase": "Ein langsames Essen hilft dem Körper, die Nahrung besser zu verdauen.",
        "tradução_outra_frase": "Comer devagar ajuda o corpo a digerir melhor os alimentos.",
        "reflexivo": False
    },
    {
        "verbo": "entzünden",
        "tradução": "inflamar, in Brand setzen (im medizinischen Kontext: sich entzünden)",
        "frase": "Eine Wunde kann sich entzünden, wenn sie nicht sauber versorgt wird.",
        "tradução_frase": "Um ferimento pode se inflamar se não for limpo corretamente.",
        "sinônimo": ["sich entzünden", "infizieren"],
        "perfekt": "hat sich entzündet",
        "präteritum": "entzündete sich",
        "regência": "sich entzünden (intransitiv)",
        "outra_frase": "Um eine Entzündung zu vermeiden, sollte man Verletzungen immer desinfizieren.",
        "tradução_outra_frase": "Para evitar inflamações, deve-se sempre desinfetar as lesões.",
        "reflexivo": True
    },
    {
        "verbo": "immunisieren",
        "tradução": "imunizar",
        "frase": "Kinder werden geimpft, um sie gegen gefährliche Krankheiten zu immunisieren.",
        "tradução_frase": "Crianças são vacinadas para se imunizarem contra doenças perigosas.",
        "sinônimo": ["impfen", "absichern"],
        "perfekt": "hat sich immunisiert",
        "präteritum": "immunisierte sich",
        "regência": "sich immunisieren gegen + Akkusativ",
        "outra_frase": "Durch regelmäßige Impfungen kann man sich effektiv gegen Viren immunisieren.",
        "tradução_outra_frase": "Por meio de vacinas regulares, é possível imunizar-se eficazmente contra vírus.",
        "reflexivo": True
    },
    {
        "verbo": "regenerieren",
        "tradução": "regenerar, sich erholen",
        "frase": "Nach intensivem Sport regeneriert sich der Körper über Nacht.",
        "tradução_frase": "Após exercícios intensos, o corpo se regenera durante a noite.",
        "sinônimo": ["sich erholen", "wiederherstellen"],
        "perfekt": "hat sich regeneriert",
        "präteritum": "regenerierte sich",
        "regência": "sich regenerieren",
        "outra_frase": "Ausreichender Schlaf hilft dem Körper, sich nach Anstrengungen zu regenerieren.",
        "tradução_outra_frase": "Dormir bem ajuda o corpo a se recuperar depois de esforços intensos.",
        "reflexivo": True
    },
    {
        "verbo": "stärken",
        "tradução": "fortalecer",
        "frase": "Eine ausgewogene Ernährung stärkt das Immunsystem.",
        "tradução_frase": "Uma alimentação equilibrada fortalece o sistema imunológico.",
        "sinônimo": ["fördern", "kräftigen"],
        "perfekt": "hat gestärkt",
        "präteritum": "stärkte",
        "regência": "stärken + Akkusativ",
        "outra_frase": "Regelmäßiger Sport kann die Muskeln und das Herz-Kreislauf-System stärken.",
        "tradução_outra_frase": "Exercícios regulares podem fortalecer os músculos e o sistema cardiovascular.",
        "reflexivo": False
    },
    {
        "verbo": "diagnostizieren",
        "tradução": "diagnosticar",
        "frase": "Der Arzt diagnostizierte eine seltene Krankheit anhand umfassender Tests.",
        "tradução_frase": "O médico diagnosticou uma doença rara com base em exames completos.",
        "sinônimo": ["feststellen", "ermitteln"],
        "perfekt": "hat diagnostiziert",
        "präteritum": "diagnostizierte",
        "regência": "diagnostizieren + Akkusativ",
        "outra_frase": "Moderne Geräte ermöglichen es, Krankheiten schon im Frühstadium zu diagnostizieren.",
        "tradução_outra_frase": "Equipamentos modernos possibilitam diagnosticar doenças em estágios iniciais.",
        "reflexivo": False
    },
    {
        "verbo": "vorbeugen",
        "tradução": "prevenir",
        "frase": "Regelmäßige Bewegung und gesunde Ernährung können vielen Krankheiten vorbeugen.",
        "tradução_frase": "Exercícios regulares e uma alimentação saudável podem prevenir muitas doenças.",
        "sinônimo": ["prophylaktisch wirken", "vermeiden"],
        "perfekt": "hat vorgebeugt",
        "präteritum": "beugte vor",
        "regência": "vorbeugen + Dativ (bei Krankheiten)",
        "outra_frase": "Durch Impfungen und gesunde Lebensweisen lässt sich effektiv vorgebeugen.",
        "tradução_outra_frase": "Através de vacinas e hábitos saudáveis, é possível prevenir eficazmente.",
        "reflexivo": False
    },
    {
        "verbo": "erholen",
        "tradução": "recuperar-se, repousar",
        "frase": "Nach einem anstrengenden Arbeitstag erholt sie sich in Ruhe zu Hause.",
        "tradução_frase": "Após um dia de trabalho cansativo, ela se recupera descansando em casa.",
        "sinônimo": ["sich ausruhen", "genesen"],
        "perfekt": "hat sich erholt",
        "präteritum": "erholte sich",
        "regência": "sich erholen",
        "outra_frase": "Ein erholsamer Schlaf ist essenziell, um Körper und Geist zu regenerieren.",
        "tradução_outra_frase": "Um sono reparador é essencial para regenerar corpo e mente.",
        "reflexivo": True
    },
    {
        "verbo": "massieren",
        "tradução": "massagear",
        "frase": "Eine regelmäßige Rückenmassage kann Verspannungen lösen und Schmerzen lindern.",
        "tradução_frase": "Uma massagem regular nas costas pode aliviar tensões e diminuir dores.",
        "sinônimo": ["kneten", "lockern"],
        "perfekt": "hat massiert",
        "präteritum": "massierte",
        "regência": "massieren + Akkusativ",
        "outra_frase": "Viele Menschen lassen sich massieren, um sich zu entspannen und den Kreislauf anzuregen.",
        "tradução_outra_frase": "Muitas pessoas fazem massagens para relaxar e estimular a circulação.",
        "reflexivo": False
    },
    {
        "verbo": "therapieren",
        "tradução": "realizar terapia, behandeln (im therapeutischen Sinne)",
        "frase": "Psychotherapeuten therapieren Patienten, um emotionale Blockaden zu lösen.",
        "tradução_frase": "Psicoterapeutas tratam pacientes para resolver bloqueios emocionais.",
        "sinônimo": ["behandeln", "betreuen"],
        "perfekt": "hat therapiert",
        "präteritum": "therapierte",
        "regência": "therapieren + Akkusativ",
        "outra_frase": "Moderne Therapien helfen, langanhaltende psychische Probleme zu überwinden.",
        "tradução_outra_frase": "Terapias modernas ajudam a superar problemas psicológicos duradouros.",
        "reflexivo": False
    },
    {
        "verbo": "absorbieren",
        "tradução": "absorver",
        "frase": "Der Körper absorbiert Nährstoffe aus der Nahrung, um Energie zu gewinnen.",
        "tradução_frase": "O corpo absorve nutrientes dos alimentos para obter energia.",
        "sinônimo": ["aufnehmen", "einstellen"],
        "perfekt": "hat absorbiert",
        "präteritum": "absorbierte",
        "regência": "absorbieren + Akkusativ",
        "outra_frase": "Vitamine werden im Darm schnell absorbiert, wenn die Verdauung optimal funktioniert.",
        "tradução_outra_frase": "Vitaminas são rapidamente absorvidas no intestino quando a digestão está em dia.",
        "reflexivo": False
    },
    {
        "verbo": "verstoffwechseln",
        "tradução": "metabolizar, umwandeln (Nährstoffe)",
        "frase": "Kohlenhydrate werden in Energie verstoffwechselt, die der Körper für Aktivitäten nutzt.",
        "tradução_frase": "Os carboidratos são convertidos em energia que o corpo usa para as atividades.",
        "sinônimo": ["umwandeln", "metabolisieren"],
        "perfekt": "hat verstoffwechselt",
        "präteritum": "verstoffwechselte",
        "regência": "verstoffwechseln + Akkusativ",
        "outra_frase": "Ein gesunder Stoffwechsel ist die Grundlage für Wohlbefinden und Leistungsfähigkeit.",
        "tradução_outra_frase": "Um metabolismo saudável é fundamental para o bem-estar e o desempenho.",
        "reflexivo": False
    },
    {
        "verbo": "entgiften",
        "tradução": "desintoxicar",
        "frase": "Viele Detox-Kuren zielen darauf ab, den Körper von schädlichen Stoffen zu entgiften.",
        "tradução_frase": "Muitas dietas detox têm como objetivo desintoxicar o corpo de substâncias nocivas.",
        "sinônimo": ["reinigen", "säubern"],
        "perfekt": "hat sich entgiftet",
        "präteritum": "entgiftete sich",
        "regência": "sich entgiften",
        "outra_frase": "Durch vermehrte Wasserzufuhr versucht der Körper, sich selbst zu entgiften.",
        "tradução_outra_frase": "Aumentar a ingestão de água ajuda o corpo a se desintoxicar naturalmente.",
        "reflexivo": True
    },
    {
        "verbo": "entschlacken",
        "tradução": "desintoxicar, den Körper entschlacken",
        "frase": "Einige Ernährungsprogramme versprechen, den Körper durch spezielle Diäten zu entschlacken.",
        "tradução_frase": "Alguns programas alimentares prometem desintoxicar o corpo através de dietas especiais.",
        "sinônimo": ["entgiften", "reinigen"],
        "perfekt": "hat sich entschlackt",
        "präteritum": "entschlackte sich",
        "regência": "sich entschlacken",
        "outra_frase": "Naturheilkundliche Ansätze setzen darauf, den Körper auf natürliche Weise zu entschlacken.",
        "tradução_outra_frase": "Métodos naturais de cura buscam desintoxicar o corpo de forma orgânica.",
        "reflexivo": True
    },
    {
        "verbo": "ergänzen",
        "tradução": "complementar, suplementar",
        "frase": "Eine vitaminreiche Nahrung ergänzt die tägliche Ernährung optimal.",
        "tradução_frase": "Uma alimentação rica em vitaminas complementa a dieta diária de forma ideal.",
        "sinônimo": ["vervollständigen", "bereichern"],
        "perfekt": "hat ergänzt",
        "präteritum": "ergänzte",
        "regência": "ergänzen + Akkusativ",
        "outra_frase": "Mineralstoffe können als Ergänzung zur normalen Ernährung eingenommen werden.",
        "tradução_outra_frase": "Minerais podem ser suplementados junto à alimentação habitual.",
        "reflexivo": False
    },
    {
        "verbo": "aktivieren",
        "tradução": "ativar, in Gang setzen",
        "frase": "Bewegung und frische Luft aktivieren den Stoffwechsel und fördern die Gesundheit.",
        "tradução_frase": "Exercícios e ar fresco ativam o metabolismo e promovem a saúde.",
        "sinônimo": ["anregen", "in Schwung bringen"],
        "perfekt": "hat aktiviert",
        "präteritum": "aktivierte",
        "regência": "aktivieren + Akkusativ",
        "outra_frase": "Ein Spaziergang am Morgen kann den Kreislauf aktivieren und den Tag verbessern.",
        "tradução_outra_frase": "Uma caminhada matinal pode ativar a circulação e melhorar o dia.",
        "reflexivo": False
    },
    {
        "verbo": "kontrollieren",
        "tradução": "controlar, überwachen",
        "frase": "Diabetiker müssen ihren Blutzuckerspiegel regelmäßig kontrollieren.",
        "tradução_frase": "Diabéticos precisam controlar seu nível de açúcar no sangue regularmente.",
        "sinônimo": ["überwachen", "messen"],
        "perfekt": "hat kontrolliert",
        "präteritum": "kontrollierte",
        "regência": "kontrollieren + Akkusativ",
        "outra_frase": "Moderne Geräte erleichtern es, den Gesundheitszustand kontinuierlich zu kontrollieren.",
        "tradução_outra_frase": "Dispositivos modernos facilitam o monitoramento contínuo do estado de saúde.",
        "reflexivo": False
    },
    {
        "verbo": "überwachen",
        "tradução": "monitorar, acompanhar",
        "frase": "Krankenhäuser überwachen die Vitalzeichen der Patienten rund um die Uhr.",
        "tradução_frase": "Hospitais monitoram os sinais vitais dos pacientes 24 horas por dia.",
        "sinônimo": ["beobachten", "kontrollieren"],
        "perfekt": "hat überwacht",
        "präteritum": "überwachte",
        "regência": "überwachen + Akkusativ",
        "outra_frase": "In Intensivstationen werden alle wichtigen Parameter sorgfältig überwacht.",
        "tradução_outra_frase": "Em unidades de terapia intensiva, todos os parâmetros importantes são monitorados cuidadosamente.",
        "reflexivo": False
    },
    {
        "verbo": "anregen",
        "tradução": "estimular, anregen",
        "frase": "Frische Lebensmittel können den Appetit anregen und den Stoffwechsel fördern.",
        "tradução_frase": "Alimentos frescos podem estimular o apetite e favorecer o metabolismo.",
        "sinônimo": ["motivieren", "aktivieren"],
        "perfekt": "hat angeregt",
        "präteritum": "regte an",
        "regência": "anregen + Akkusativ",
        "outra_frase": "Ein kleiner Snack zwischendurch kann den Kreislauf anregen.",
        "tradução_outra_frase": "Um lanche leve pode estimular a circulação.",
        "reflexivo": False
    },
    {
        "verbo": "ausbalancieren",
        "tradução": "equilibrar, ausgleichen",
        "frase": "Eine abwechslungsreiche Ernährung hilft, den Nährstoffhaushalt auszubalancieren.",
        "tradução_frase": "Uma alimentação variada ajuda a equilibrar o consumo de nutrientes.",
        "sinônimo": ["harmonisieren", "angleichen"],
        "perfekt": "hat ausbalanciert",
        "präteritum": "balancierte aus",
        "regência": "ausbalancieren + Akkusativ",
        "outra_frase": "Mit der richtigen Kombination von Lebensmitteln lässt sich der Blutzuckerspiegel gut ausbalancieren.",
        "tradução_outra_frase": "A combinação correta de alimentos pode equilibrar bem o nível de açúcar no sangue.",
        "reflexivo": False
    },
    {
        "verbo": "verbessern",
        "tradução": "melhorar",
        "frase": "Regelmäßige Bewegung und eine gesunde Ernährung können die allgemeine Gesundheit verbessern.",
        "tradução_frase": "Exercícios regulares e uma alimentação saudável podem melhorar a saúde em geral.",
        "sinônimo": ["optimieren", "steigern"],
        "perfekt": "hat verbessert",
        "präteritum": "verbesserte",
        "regência": "verbessern + Akkusativ",
        "outra_frase": "Kleine Änderungen im Lebensstil können langfristig das Wohlbefinden deutlich verbessern.",
        "tradução_outra_frase": "Pequenas mudanças no estilo de vida podem melhorar significativamente o bem-estar a longo prazo.",
        "reflexivo": False
    },
    {
        "verbo": "aufbauen",
        "tradução": "construir, aufbauen (z. B. Muskulatur)",
        "frase": "Regelmäßiges Training hilft, Muskelmasse aufzubauen und den Körper zu stärken.",
        "tradução_frase": "Treinamentos regulares ajudam a desenvolver massa muscular e fortalecer o corpo.",
        "sinônimo": ["entwickeln", "trainieren"],
        "perfekt": "hat aufgebaut",
        "präteritum": "baute auf",
        "regência": "aufbauen + Akkusativ",
        "outra_frase": "Ein gezieltes Krafttraining kann den Muskelaufbau effektiv fördern.",
        "tradução_outra_frase": "Um treinamento de força direcionado pode promover eficazmente o desenvolvimento muscular.",
        "reflexivo": False
    },
    {
        "verbo": "verjüngen",
        "tradução": "rejuvenescer, verjüngen",
        "frase": "Viele Hautcremes versprechen, die Haut zu verjüngen und Falten zu reduzieren.",
        "tradução_frase": "Muitas cremes para a pele prometem rejuvenescer a pele e reduzir rugas.",
        "sinônimo": ["erneuern", "revitalisieren"],
        "perfekt": "hat verjüngt",
        "präteritum": "verjüngte",
        "regência": "verjüngen + Akkusativ",
        "outra_frase": "Moderne Anti-Aging-Produkte zielen darauf ab, die Haut sichtbar zu verjüngen.",
        "tradução_outra_frase": "Produtos anti-idade modernos têm como objetivo rejuvenescer visivelmente a pele.",
        "reflexivo": False
    },
    {
        "verbo": "stimulieren",
        "tradução": "estimular",
        "frase": "Bewegung und frische Luft stimulieren den Kreislauf und fördern die Vitalität.",
        "tradução_frase": "Exercícios e ar fresco estimulam a circulação e promovem a vitalidade.",
        "sinônimo": ["anregen", "aktivieren"],
        "perfekt": "hat stimuliert",
        "präteritum": "stimulierte",
        "regência": "stimulieren + Akkusativ",
        "outra_frase": "Ein regelmäßiger Spaziergang kann den Kreislauf nachhaltig stimulieren.",
        "tradução_outra_frase": "Uma caminhada regular pode estimular a circulação de forma duradoura.",
        "reflexivo": False
    },
    {
        "verbo": "beruhigen",
        "tradução": "acalmar, tranquilizar",
        "frase": "Atemübungen können den Geist beruhigen und Stress abbauen.",
        "tradução_frase": "Exercícios respiratórios podem acalmar a mente e reduzir o estresse.",
        "sinônimo": ["entspannen", "besänftigen"],
        "perfekt": "hat beruhigt",
        "präteritum": "beruhigte",
        "regência": "beruhigen + Akkusativ",
        "outra_frase": "Eine Meditation am Morgen kann helfen, den Geist zu beruhigen und den Tag positiv zu starten.",
        "tradução_outra_frase": "Uma meditação matinal pode ajudar a acalmar a mente e iniciar o dia de forma positiva.",
        "reflexivo": False
    },
    {
        "verbo": "sanieren",
        "tradução": "renovar, reabilitar, sanar, wiederherstellen, verbessern (Gesundheit oder Lebensqualität)",
        "frase": "Nach einem längeren Krankheitsverlauf versucht man, die Lebensqualität durch gezielte Maßnahmen zu sanieren.",
        "tradução_frase": "Após um período prolongado de doença, busca-se melhorar a qualidade de vida com medidas específicas.",
        "sinônimo": ["verbessern", "wiederherstellen"],
        "perfekt": "hat saniert",
        "präteritum": "sanierte",
        "regência": "sanieren + Akkusativ",
        "outra_frase": "Rehabilitationsprogramme zielen darauf ab, die Gesundheit nachhaltig zu sanieren.",
        "tradução_outra_frase": "Programas de reabilitação têm como objetivo restaurar a saúde de forma duradoura.",
        "reflexivo": False
    }
]


lista_ordenada = []
def mostra_lista_verbo(verbos):
    """mostra a lista de verbos em ordem alfabética usando o locale alemão

    Args:
        verbos (lista): lista de verbos, onde a key 'verbo' representa o verbo em alemão
    """
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    for i in verbos:
        for k, v in i.items():
            if k == "verbo":
                lista_ordenada.append(v)
    print(sorted(lista_ordenada, key=locale.strxfrm))
                

def buscar_entrada_duden(verbo):
    """Busca e organiza a entrada do verbo no Duden usando a CLI 'duden'.
    Args:
        verbo (lista): Para cada key 'verbo' na lista de verbos, busca a entrada no Duden.

    Returns:
        list: Uma lista com as linhas da entrada do verbo no Duden.
    """
    if not shutil.which("duden"):
        return ["⚠️ O comando 'duden' não está disponível. Instale-o com 'pip install duden'."]

    try:
        return execute_duden_command(verbo)
    except Exception as e:
        return [f"⚠️ Erro ao buscar entrada no Duden: {e}"]


def execute_duden_command(verbo):
    """
    Executa o comando duden para obter a entrada do dicionário alemão para um verbo.
    Este método usa o CLI duden para consultar o significado e outras informações sobre o verbo especificado.
    Se o comando duden não estiver disponível, ele retorna uma mensagem de erro.

    Args:
        verbo (str): O verbo em alemão que será consultado no Duden.

    Returns:
        list[str]: Uma lista de strings formatadas com a definição, exemplos e sinônimos obtidos do Duden.
                   Retorna mensagens de aviso em caso de erro ou se nenhuma informação útil for encontrada.

    Raises:
        Exception: Se ocorrer um erro inesperado durante a execução do comando duden.

    Exemplo:
        execute_duden_command('gehen')
        
    """
    if not shutil.which("duden"):
        return ["⚠️ O comando 'duden' não está disponível. Instale-o com 'pip install duden'."]

    try:
        # garante que o processo termine antes de capturar a saída
        process = subprocess.Popen(
            ['duden', verbo, '-r', '1'],  
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace'
        )
        time.sleep(0.2)  #Espera um pouco para garantir que o processo finalize
        output, error_output = process.communicate()
        if process.returncode != 0:
            return [f"⚠️ Erro ao executar 'duden': {error_output.strip()}"]
        
    except Exception as e:
        return [f"⚠️ Erro inesperado: {e}"]
    
    print(f"\n📖 🔍 Entrada no Duden para '{verbo}':\n{output}")


def buscar_frases_tatoeba(verbo):
    """
    Busca frases no Tatoeba para um verbo em alemão.
    Esta função faz uma requisição à API do Tatoeba para buscar frases de exemplo em alemão
    e suas traduções em português. Dá prioridade a frases mais longas para assegurar exemplos 
    mais contextualizados.

    Args:
        verbo (str): O verbo em alemão para o qual as frases serão buscadas.

    Returns:
        list[str]: Uma lista de mensagens com o resultado da busca ou mensagens de erro.
                   Se encontrar frases, elas serão exibidas no console.

    Raises:
        Exception: Se ocorrer um erro inesperado ao tentar acessar a API do Tatoeba.

    Example:
        >>> buscar_frases_tatoeba('gehen')
        🇩🇪 Ich gehe nach Hause.
        <Pressiona Enter>
        🇧🇷 Eu estou indo para casa.

        🇩🇪 Er geht in die Schule.
        <Pressiona Enter>
        🇧🇷 Ele vai para a escola.

        🇩🇪 Wir gehen ins Kino.
        <Pressiona Enter>
        🇧🇷 Nós vamos ao cinema.
    """
    url = f"https://tatoeba.org/en/api_v0/search?query={verbo}&from=deu&to=por"

    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if "results" not in dados or not isinstance(dados["results"], list):
            return ["⚠️ Nenhuma frase encontrada no Tatoeba."]

        frases_b2 = []
        frases_curta = []
                
        for item in dados["results"]:
            if not isinstance(item, dict):
                continue
            frase_de = item.get("text", "")
            traducoes = item.get("translations", [])
            frase_pt = None
            for sublist in traducoes:
                if isinstance(sublist, list):
                    for t in sublist:
                        if isinstance(t, dict) and t.get("lang") == "por":
                            frase_pt = t.get("text")
                            break
                if frase_pt:
                    break

            
            if frase_de and frase_pt:
                if len(frase_de.split()) > 8:
                    frases_b2.append((frase_de, frase_pt))  
                else:
                    frases_curta.append((frase_de, frase_pt)) 
        frases_selecionadas = frases_b2 if frases_b2 else frases_curta #prioriza frases longas
        if not frases_selecionadas:
            return ["⚠️ Nenhuma frase encontrada no Tatoeba."]
        elif frases_selecionadas == frases_b2:
            print("\n📚 **Frases encontradas no Tatoeba:**")
            print("\n **Frases B2:**")
        elif frases_selecionadas == frases_curta:
            print("\n📚 **Frases encontradas no Tatoeba:**")
            print("\n **Frases curtas:**")
        for frase_de, frase_pt in frases_selecionadas[:3]:
            print(f"🇩🇪 {frase_de}")  # Exibe a frase em alemão
            input("")  
            print(f"🇧🇷 {frase_pt}\n")  # Exibe a tradução    
    except Exception as e:
        return [f"⚠️ Erro ao buscar frases no Tatoeba: {e}"]


def mostrar_informacoes_verbo(verbo):
    """Exibe a entrada do verbo no Duden e frases do Tatoeba."""
    print(f"\n🔹 **Verbo:** {verbo.upper()}")
    buscar_entrada_duden(verbo)
    print("\n📖 **Fim da entrada no Duden**")


    # 📚 Frases B2 no Tatoeba
    print("\n **Buscando frases no Tatoeba... **")
    input("")
    buscar_frases_tatoeba(verbo)


def revelar_info(verbo_info):
    """Exibe progressivamente os detalhes do verbo e permite buscar frases extras."""
    detalhes = [
        ("Tradução", verbo_info["tradução"]),
        ("Frase", verbo_info["frase"]),
        ("Tradução da frase", verbo_info["tradução_frase"]),
        ("Sinônimo", ", ".join(verbo_info["sinônimo"]) if isinstance(verbo_info["sinônimo"], list) else verbo_info["sinônimo"]),
        ("Perfekt", verbo_info["perfekt"]),
        ("Präteritum", verbo_info["präteritum"]),
        ("Regência", verbo_info["regência"]),
        ("Outra frase", verbo_info["outra_frase"]),
        ("Tradução da outra frase", verbo_info["tradução_outra_frase"])
    ]

    for titulo, info in detalhes:
        input(f"\n{titulo}: ")
        print(f"{info}")
        # Morstrar informações do verbo principal e buscar frases nivel b2 no tatoeba
        if titulo == "Tradução":
            mostrar_informacoes_verbo(verbo_info["verbo"])


        # Buscar frases B2 para um sinônimo
        elif titulo == "Tradução da outra frase" and isinstance(verbo_info["sinônimo"], list) and verbo_info["sinônimo"]:
            sinonimo_escolhido = random.choice(verbo_info["sinônimo"])
            print(f"\n🔄 Buscando frases B2 para o sinônimo: {sinonimo_escolhido}")
            buscar_frases_tatoeba(sinonimo_escolhido)

    print("\n✔️ Todas as informações foram exibidas!\n")

# Conjunto para armazenar verbos já exibidos
verbos_exibidos = set()

# Loop principal para exibir verbos até o usuário decidir sair ou acabarem os verbos
while len(verbos_exibidos) < len(verbos):
    # Sorteia um verbo que ainda não foi mostrado
    verbo_sorteado = random.choice([v for v in verbos if v["verbo"] not in verbos_exibidos])

    # Marca o verbo como já exibido
    verbos_exibidos.add(verbo_sorteado["verbo"])

    # Exibir o verbo corretamente, incluindo "sich" se for reflexivo
    verbo_formatado = f"sich {verbo_sorteado['verbo']}" if verbo_sorteado["reflexivo"] else verbo_sorteado["verbo"]
    if len(verbos_exibidos) == 1:
        a = input("Deseja apenas ver APENAS a lista dos verbos? (sim/não): ").strip().lower()
        if a == "sim":
            mostra_lista_verbo(verbos)
            break
    else:
        print(f"\n🎲 Verbo sorteado: {verbo_formatado}")
        input("Tente dizer o significado em português e pressione Enter para conferir...")

        # Revela as informações do verbo sorteado
        revelar_info(verbo_sorteado)

        # Pergunta ao usuário se deseja ver outro verbo
        resposta = input("❓ Quer ver outro verbo? (sim/não): ").strip().lower()
        if resposta != "sim":
            print("\n📚 Estudo finalizado. Bis bald! 👋")
            break

# Se todos os verbos forem exibidos, o programa encerra automaticamente
if len(verbos_exibidos) == len(verbos):
    print("\n🎉 Você viu todos os verbos disponíveis! Estudo concluído. 🚀🇩🇪")


