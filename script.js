document.addEventListener('DOMContentLoaded', function() {
  const cardContainer = document.querySelector('.card-container');

  fetch('/drinks')
    .then(response => response.json())
    .then(drinks => {
      drinks.forEach(drink => {
        const card = document.createElement('div');
        card.classList.add('card', 'mb-3');

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const cardTitle = document.createElement('h5');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = `Drink ID: ${drink.drink_id} - ${drink.drink_name}`;

        const cardText = document.createElement('p');
        cardText.classList.add('card-text');
        cardText.textContent = drink.description;

        const cardPrice = document.createElement('p');
        cardPrice.classList.add('card-text', 'font-weight-bold');
        cardPrice.textContent = `Price: $${drink.price}`;

        const cardType = document.createElement('p');
        cardType.classList.add('card-text', 'text-muted');
        cardType.textContent = `Type: ${drink.drink_type}`;

        const cardIngredients = document.createElement('p');
        cardIngredients.classList.add('card-text');
        cardIngredients.textContent = `Ingredients: ${drink.ingredients}`;

        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardText);
        cardBody.appendChild(cardPrice);
        cardBody.appendChild(cardType);
        cardBody.appendChild(cardIngredients);
        card.appendChild(cardBody);
        cardContainer.appendChild(card);
      });
    })
    .catch(error => {
      console.error('Error fetching drinks:', error);
    });
});