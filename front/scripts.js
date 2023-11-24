/* SEMÁFORO
  --------------------------------------------------------------------------------------
  Função para mostrar o resultado da avaliação dos dados do fundo 
  --------------------------------------------------------------------------------------
*/

function atualizarSemaforo(R, Y, G) {
  document.getElementById('vermelho').className = 'luz off';
  document.getElementById('amarelo').className = 'luz off';
  document.getElementById('verde').className = 'luz off';

  if (R === 'on' && Y === 'off' && G === 'off') {
    document.getElementById('vermelho').className = 'luz on';
  } 
  else if (R === 'off' && Y === 'on' && G === 'off') {
    document.getElementById('amarelo').className = 'luz on';
  } 
  else if (R === 'off' && Y === 'off' && G === 'on') {
    document.getElementById('verde').className = 'luz on';
  }
}

/* Coleta os dados
  --------------------------------------------------------------------------------------
  Função para coletar os dados inseridos e chamar a API de ML para avaliar os dados 
  --------------------------------------------------------------------------------------
*/
const newItem = async() => {
  let inputResgate = document.getElementById("Resgate").value;
  let inputCaptação = document.getElementById("Captação").value;
  let inputCotistas = document.getElementById("Cotistas").value;
  let inputPatLiq = document.getElementById("PatLiq").value;
  let inputQuota = document.getElementById("Quota").value;
  
  // Mostra a MENSAGEM DE PROCESSAMENTO
  const loadingMessage = document.getElementById("loading-message");
  loadingMessage.classList.remove("hidden"); // HTML: "Por favor, aguarde em processamento..."

  try{
    /* Verifica se todas as entradas estão preenchidas */
    if (inputResgate === '' || inputCaptação === ''|| inputCotistas === '' || inputPatLiq === '' || inputQuota === '') {
      // Msg_1
      alert("Erro: Todos os campos devem estar preenchidos!");
      return; // Sai da função se houver campos vazios
    }

    /* Regras de Negócio relacionadas às restrições sobre o modelo de machine learning*/
    // RN1 :: VL_QUOTA>0
    // RN2 :: NR_COTST>1.000
    // RN3 :: VL_PATRIM_LIQ>1.000.000
    // Regras de Negócio: RN1, RN2 e RN3
    if (inputQuota < 0 || inputCotistas < 1000 || inputPatLiq < 1000000) {
      // Msg_2
      alert(`Erro: O valor da Quota tem que ser > 0 (zero), Número de Cotistas >= 1.000 e Valor do Patrimônio Líquido >= 1.000.000 !`);
      return; // Sai da função
    }

    // NÃO ESTÁ CHAMANDO A FUNÇÃO AvalFIMult
    AvalFIMult(inputResgate, inputCaptação, inputCotistas, inputPatLiq, inputQuota);
    atualizarSemaforo(R, Y, G)

  }
  
  finally {
    // Esconde a MENSAGEM DE PROCESSAMENTO
    loadingMessage.classList.add("hidden");
  }

}


/* Chama API AvalFIMult
  --------------------------------------------------------------------------------------
  Chama API para Avaliação de Viabilidade de Investimento em Fundos Multimercado  
  --------------------------------------------------------------------------------------
*/

const AvalFIMult = async (inputResgate, inputCaptacao, inputCotistas, inputPatLiq, inputQuota) => {
  alert(inputResgate + "," + inputCaptação + "," + inputCotistas + "," + inputPatLiq + "," + "," + inputQuota);
  try {
    const url = `http://127.0.0.1:5001/AvalFIMult?resgate=${inputResgate}&
    capta=${inputCaptacao}&cotistas=${inputCotistas}&patliq=${inputPatLiq}&
    quota=${inputQuota}`;

    const response = await fetch(url, {
      method: 'get', headers: {
        'Content-Type': 'application/json',
        'X-Origin': 'Obras de Arte'
      }
    });

    let R, Y, G;

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    } else {
      const data = await response.text();
      if (data === '1') {
        R = "off";
        Y = "off";
        G = "on";
      } else {
        R = "on";
        Y = "off";
        G = "off";
      }
      return {R, Y, G};
    }
  } catch (error) {
    console.log(error);
  }
}
