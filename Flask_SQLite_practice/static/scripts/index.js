$.ajax('/api/realty')
  .done((data) => {
    cardsRender(data)
  })

function cardRender ({title, price, city, id, address}, container) {
  const image = `/static/${id}.jpg`;
  const bodyCard = `
  <div id="card-template" class="card" style="width: 18rem;">
    <img src="${ image }" class="card-img-top" alt="${ title }">
    <div class="card-body">
        <h5 class="card-title">${ address }</h5>
        <h5 class="card-title">${ city }</h5>
        <h5 class="card-title">${ title }</h5>
        <p class="card-price">${ price }</p>
        <a href="${ city }" class="btn btn-primary">Go somewhere</a>
    </div>
  </div>`;

  container.append(bodyCard);
}

function cardsRender (cards) {
  const placeCards = $('#card-container');
  
  cards.forEach((card) => {
    cardRender(card, placeCards);
  });
}