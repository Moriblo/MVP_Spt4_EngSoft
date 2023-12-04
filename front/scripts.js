/* SEMÁFORO
  --------------------------------------------------------------------------------------
  Função para mostrar o resultado da avaliação dos dados do fundo 
  --------------------------------------------------------------------------------------
*/
let R = 'off'
let Y = 'off'
let G = 'off'

// function atualizarSemaforo(R, Y, G) {
const atualizarSemaforo = (R, Y, G, result) => {

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
  let inputCapta = document.getElementById("Captação").value;
  let inputPatLiq = document.getElementById("PatLiq").value;
  let inputPatTotal = document.getElementById("PatTotal").value;
  
  try{

    /* Verifica se todas as entradas estão preenchidas */
    if (inputResgate === '' || inputCapta === ''|| inputPatLiq === '' || inputPatTotal === '') {
      atualizarSemaforo ('off', 'on', 'off');
      setTimeout(() => {
        alert("Erro: Todos os campos devem estar preenchidos!");
        atualizarSemaforo ('off', 'off', 'off');
        letreiro()
      }, 100);
      return;
    }

    // Trata os dados de entrada
    inputResgate = inputResgate.replace(/\s+/g, ''); // remove todos os espaços
    inputResgate = parseFloat(inputResgate)
    console.log(inputResgate);
    console.log(typeof inputResgate)

    inputCapta = inputCapta.replace(/\s+/g, ''); // remove todos os espaços
    inputCapta = parseFloat(inputCapta)
    console.log(inputCapta);
    console.log(typeof inputCapta)

    inputPatLiq = inputPatLiq.replace(/\s+/g, ''); // remove todos os espaços
    inputPatLiq = parseFloat(inputPatLiq)
    console.log(inputPatLiq);
    console.log(typeof inputPatLiq)

    inputPatTotal = inputPatTotal.replace(/\s+/g, ''); // remove todos os espaços
    inputPatTotal = parseFloat(inputPatTotal)
    console.log(inputPatTotal);
    console.log(typeof inputPatTotal)

    /* Regras de Negócio relacionadas às restrições sobre o modelo de machine learning*/
    // Regra de Negócio: VL_PATRIM_LIQ>=1.000.000
    if (inputPatLiq < 1000000) {
      // Msg_2
      atualizarSemaforo ('off', 'on', 'off');
      setTimeout(() => {
        alert("Erro: Patrimônio deve ser >= 1.000.000!");
        atualizarSemaforo ('off', 'off', 'off');
        letreiro()
      }, 100);
      return; // Sai da função
    }

    avalfimult(inputResgate, inputCapta, inputPatLiq, inputPatTotal);
    letreiro("Processando...")
    atualizarSemaforo (R, Y, G)

  }
  
  finally {}
}

/* Chama API AvalFIMult
  --------------------------------------------------------------------------------------
  Chama API para Avaliação de Viabilidade de Investimento em Fundos Multimercado  
  --------------------------------------------------------------------------------------
*/

avalfimult = async (inputResgate, inputCapta, inputPatLiq, inputPatTotal) => {

  try {
    const url = `http://127.0.0.1:5001/avalfimult?resgate=${inputResgate}&capta=${inputCapta}&patliq=${inputPatLiq}&pattotal=${inputPatTotal}`;

    const response = await fetch(url, {
      method: 'get', headers: {
        'Content-Type': 'application/json',
        'X-Origin': 'FIMulti'
      }
    });

    let R, Y, G;

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    } 
    else {
      const data = await response.text();
      if (data === "1") {
        R = "off";
        Y = "off";
        G = "on";
        letreiro("Tá liberado!!!")
      } else if (data === "0") {
        R = "on";
        Y = "off";
        G = "off";
        letreiro("Deu ruim!!!")
      }
      else {
        R = "off";
        Y = "on";
        G = "off";
        letreiro("ERRO DE PROCESSAMENTO!!!")
      }
      atualizarSemaforo(R, Y, G)
      // return {R, Y, G};
    }
  } 
  catch (error) {
  console.log(error);
  }
}

/* SEMÁFORO
  --------------------------------------------------------------------------------------
  Função para mostrar o resultado da avaliação dos dados do fundo 
  --------------------------------------------------------------------------------------
*/
function letreiro(newText) {
  // Seleciona o elemento marquee
  var marquee = document.querySelector('.letreiro marquee');

  // Altera o texto dentro do marquee
  marquee.textContent = newText;
}