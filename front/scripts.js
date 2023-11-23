/* > ROTA PARA LISTAR ITENS - /obras/GET
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET pela Rota /obras.
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/obras';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.obras.forEach(item => insertList(item.nome, item.artista, item.estilo, item.tipo, item.link))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/* GetList
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()

/* > ROTA PARA ADIÇÃO DE ITEM - /obra/POST
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST na rota /obra.
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputNome, inputArtista, inputEstilo, inputTipo, inputLink) => {
  const formData = new FormData();
  formData.append('nome', inputNome);
  formData.append('artista', inputArtista);
  formData.append('estilo', inputEstilo);
  formData.append('tipo', inputTipo);
  formData.append('link', inputLink);
 
  let url = 'http://127.0.0.1:5000/obra';
  
  fetch(url, {
    method: 'post',
    body: formData
  })
 
  .then(response => {
      if (response.ok) {
        insertList(inputNome, inputArtista, inputEstilo, inputTipo, inputLink);
        //Msg_4
        alert("Obra inserida com sucesso!");
      }
      else {
        alert("Erro: Inserção mal sucedida!");
      }
  })
}

/* BUTTON
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
function insertButton(parent) {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/* REMOVE ITEM
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
function removeElement() {
  let close = document.getElementsByClassName("close");
  var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const obraItem = div.getElementsByTagName('td')[0].innerHTML;
      const artistaItem = div.getElementsByTagName('td')[1].innerHTML;
  
      // Construção do cenário para envio do comando de deleção do registro 
      // de obra e artista, pela função "deleteItem"
      const nomeItem = 'nome=' + obraItem + '&' + 'artista=' + artistaItem
  
      if (confirm("Você tem certeza?")) {
        div.remove();
        deleteItem(nomeItem);
        alert("Removido!");
      }
    };
  }
}

/* > ROTA PARA DELETAR ITENS - /obra/DELETE
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE na Rota /obra
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/obra?' + item; 
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/* ADICIONA ITEM
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com obra, artista, estilo tipo e link 
  --------------------------------------------------------------------------------------
*/
const newItem = async() => {
  let inputNome = document.getElementById("newNome").value;
  let inputArtista = document.getElementById("newArtista").value;
  let inputEstilo = document.getElementById("newEstilo").value;
  let inputTipo = document.getElementById("newTipo").value;
  let inputLink = document.getElementById("newLink").value;
  
  // Mostra a MENSAGEM DE PROCESSAMENTO
  const loadingMessage = document.getElementById("loading-message");
  loadingMessage.classList.remove("hidden"); // HTML: "Por favor, aguarde em processamento..."

  try{

    // 1ª Regra de Negócio (RN1) - Verifica se há algum campo obrigatório vazio
    if (inputNome === '' || inputArtista === ''|| inputEstilo === '' || inputTipo === '') {
      // Msg_1
      alert("A exceção do campo Link que é opcional, todos os demais campos devem estar preenchidos!");
      return; // Sai da função se houver campos vazios
    }
    // 2ª Regra de Negócio (RN2) - Verifica se já há registro para mesma Obra e Artista
    const obra_nome = inputNome;
    const obra_artista = inputArtista
    const retobrart = await getobrart(obra_nome, obra_artista);
    if (retobrart[2]) {
      // Msg_2
      alert(`Já existe este registro na base: Obra = ${retobrart[0]} e Artista = ${retobrart[1]}`);
      return;
    }

    // Verifica se o campo Link está vazio para ofertar a busca por uma imagem.
    if (inputLink === '') {
      // Msg_3
      busca_imagem = window.confirm("Ok para buscar um link para a obra ou Cancelar para salvar sem link?");
      if (busca_imagem) {
        // Chama a tradução de português para o inglês do "valor_entrada", que contém o 
        //nome da obra inserido no formulário na página web por "inputName".
        const valor_entrada = inputNome;
        const rettradu = await gettradutor(valor_entrada);
        
        // Verifica se a tradução faz sentido
        let obraTraduzida;
        // Msg_5
        const aceita_tradu = window.confirm(`A tradução de: <${inputNome}> foi realizada para <${rettradu[2]}>. Ok para aceitar tradução, Cancelar para seguir com o original`);
        if (aceita_tradu) {
          obraTraduzida = rettradu[2];
        } else {
          obraTraduzida = inputNome;
        }
        
        // Chama a busca por link, utilizando as variáveis "obraTraduzida" que tem o 
        // resultado da aceitação ou não da tradução de português para inglês vindo 
        // de "gettradutor", e "artista" com o nome do artista, inserido da página 
        // principal por "inputArtista".
        const artista = inputArtista;
        const retmuseum = await getsmuseum(obraTraduzida, artista);
        
        // Pega o retorno "getmuseum" e verifica, pelo conteúdo do campo 
        // "retmuseum.link", em JSON, se houve erro na obtenção da informação.
        if (retmuseum.link.includes("Erro")) {
          // Msg_7
          return_link = window.confirm(`Foi recebida a seguinte msg: <${retmuseum.link}>. Ok para salvar sem link, Cancelar para voltar à entrada.`);
          if (return_link) {
            inputLink = '';
            postItem(inputNome, inputArtista, inputEstilo, inputTipo, inputLink);
            return;
          } 
          else {
            return;
          }
        }
        // Msg_8
        let salva_link
        salva_link = window.confirm(`O link obtido para a obra é: <${retmuseum.link}>. Ok para salvar, Cancelar para voltar à entrada.`);
          if (salva_link) {
            inputLink = retmuseum.link
          }
          else {
            inputLink = '';
            return;
          }
      }
      else {
        inputLink = '';
      }
    }
    // Salva os dados na base
    postItem(inputNome, inputArtista, inputEstilo, inputTipo, inputLink);
  }
  catch (error) {
    console.error(error);
  } 
  
  finally {
    // Esconde a MENSAGEM DE PROCESSAMENTO
    loadingMessage.classList.add("hidden");
  }

}

/* INSERIR ITENS NA LISTA
  --------------------------------------------------------------------------------------
  Função para inserir itens na lista apresentada
  --------------------------------------------------------------------------------------
*/
function insertList(nome, artista, estilo, tipo, link) {
  var item = [nome, artista, estilo, tipo, link];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1));
  document.getElementById("newNome").value = "";
  document.getElementById("newArtista").value = "";
  document.getElementById("newEstilo").value = "";
  document.getElementById("newTipo").value = "";
  document.getElementById("newLink").value = "";

  removeElement();
}

/* > ROTA PARA CONSULTA OBRA E ARTISTA - 5000/obrart/GET
  --------------------------------------------------------------------------------------
  2ª Regra de Negócio (RN2): Não permitir tupla Obra + Artista duplicada na base
  --------------------------------------------------------------------------------------
*/
const getobrart = async (obra_nome, obra_artista) => {
  try {
    const url = `http://127.0.0.1:5000/obrart?nome=${obra_nome}&artista=${obra_artista}`;
    const response = await fetch(url, {
      method: 'get'
    });

    const data = await response.json();

    console.log(data);
    return data;
        
  } catch (error) {
    console.error(error);
    return { error: "Ocorreu um erro na busca." };

  }
};

/* > ROTA PARA TRADUÇÃO DA OBRA (PORT->ING) - 5001/tradutor
--------------------------------------------------------------------------------------
  Função para chamar uma rota para realizar a tradução da obra de português
  para inglês.
--------------------------------------------------------------------------------------
*/
const gettradutor = async (valor_entrada) => {
  try {
    const url = `http://127.0.0.1:5001/tradutor?entrada=${valor_entrada}`;
    const response = await fetch(url, {
      method: 'get', headers: {
        'Content-Type': 'application/json',
        'X-Origin': 'Obras de Arte'
      }
    });

    const data = await response.json();
    let rettradu
    rettradu = data
    console.log(data);
    return rettradu;
        
  } catch (error) {
    console.error(error);
    return { error: "Ocorreu um erro na tradução." };

  }
};

/* > ROTA PARA BUSCA DE LINK PARA IMAGEM - 5002/smuseum
--------------------------------------------------------------------------------------
  Retorna um link de uma imagem para a obra informada no campo de preenchimento 
  obra, quando do registro de uma obra, a partir da pesquisa em uma
  base de um museu informado. Neste caso estou utilizando o Metropolitan Museum.
--------------------------------------------------------------------------------------
*/
const getsmuseum = async (obraTraduzida, artista) => {
  try {
      // Construa a URL com os parâmetros
      // Msg_6
      alert(`A busca será realizada para obra: ${obraTraduzida} e artista: ${artista}`)

      const url = `http://127.0.0.1:5002/smuseum?nome=${obraTraduzida}&artista=${artista}`;

      // Realize a chamada assíncrona
      const response = await fetch(url);
      const data = await response.json();
      return data;
  } catch (error) {
      console.error(error);
      return null; // ou trate o erro de alguma forma
  }
};