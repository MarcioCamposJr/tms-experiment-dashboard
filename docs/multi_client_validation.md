# Validação manual com múltiplos clientes

As atualizações visuais usam versões independentes por cliente. A aquisição
continua única, e os históricos são copiados para leitura sob um lock curto.
Os marcadores são preparados em lote e os dados preparados são reutilizados
pelos clientes. Os objetos NiceGUI continuam individuais por sessão.

## Comunicação preservada

- Os tópicos, payloads e caminhos de envio e recebimento permanecem iguais.
- A configuração do robô mantém a espera de 1,5 segundo após as requisições.
- A aquisição EMG, o baseline e o cálculo pico a pico mantêm seus parâmetros.
- `status_new_mep` mantém sua confirmação após a primeira atualização visual
  bem-sucedida. Essa confirmação só pode consumir a versão que foi exibida.
- O envio de MEPs continua no processamento de aquisição, com as condições
  existentes. Abrir mais clientes não cria novos emissores.
- A marcação temporal dos estímulos por `status_new_mep_2` permanece igual.
- A solicitação de superfícies mantém `wait_for_stl` e seu tratamento de resposta.
- Os timers de atualização mantêm o intervalo de 100 ms.

`mep_plot_snapshot.revision` identifica somente o que cada tela precisa exibir;
não substitui uma resposta do equipamento nem confirma a aplicação de comandos.
Os snapshots são internos ao Python e não alteram o formato das mensagens.

## Roteiro

1. Inicie o relay e o dashboard como descrito no README.
2. Abra a página em um navegador e depois em mais três abas ou navegadores.
3. Durante a aquisição, confira movimento, deslocamento e rotação nas quatro
   telas. Acumule estímulos suficientes para manter cerca de 20 marcadores na
   janela dos gráficos e confira os marcadores nos dois gráficos.
4. Confira se cada novo MEP aparece nas quatro telas. Abra outro cliente após
   um MEP e confira se ele também mostra o resultado já recebido.
5. Abra e feche o checklist em cada tela durante as atualizações.
6. Solicite a configuração do robô. Confira a espera existente, os valores
   recebidos e o envio ao salvar, usando os registros do relay.
7. Desconecte e reconecte um cliente. Confira se ele volta a receber dados e
   se os outros continuam respondendo.
8. Feche uma aba e aguarde o encerramento da sessão. Confira se não aparecem
   erros de atualização de elementos de um cliente removido.
9. Encerre a navegação/aquisição conforme o fluxo normal do equipamento e
   confira a limpeza dos gráficos quando o estado for resetado.

Falhas de atualização são registradas com o cliente, a etapa e o traceback.
Uma falha persistente com a mesma mensagem é registrada uma vez até recuperar,
para evitar repetir o mesmo erro a cada 100 ms.

## Verificação local desta alteração

Sem adicionar testes unitários, foram utilizadas medições Python com 1 a 4
clientes e navegação em quatro páginas Chrome com aquisição e respostas
simuladas. Esse cenário não substitui a validação com equipamentos reais.
