$(document).ready(function() {
  $.ajax('/api/books')
    .done(function(data) {
      const container = $('#books-container');
      data.forEach(function(book) {
        const card = `
          <div class="col-md-4">
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">${book.title}</h5>
                <p class="card-text">${book.author}</p>
                <p class="card-text">${book.price} $</p>
              </div>
            </div>
          </div>`;
        container.append(card);
      });
    });
});