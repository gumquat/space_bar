document.addEventListener('DOMContentLoaded', function() {
  const cardContainer = document.querySelector('.card-columns');
  const buttons = document.querySelectorAll('button[data-route]');

  buttons.forEach(button => {
    button.addEventListener('click', async function(event) {
      event.preventDefault(); // Prevent the default button click behavior
      const route = this.getAttribute('data-route');
      await fetchDrinks(route); // Wait for the fetch to complete before continuing
    });
  });

  async function fetchDrinks(path) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/${path}`);
      const drinks = await response.json();

      cardContainer.innerHTML = ''; // Clear previous cards
      drinks.forEach(drink => {
        const card = createCard(drink);
        cardContainer.appendChild(card);
      });
    } catch (error) {
      console.error('Error fetching drinks:', error);
    }
  }

  function createCard(drink) {
    const card = document.createElement('div');
    card.classList.add('card', 'mb-3');

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body', 'col-12');

    const cardImg = document.createElement('img');
    cardImg.classList.add('col-12');
    cardImg.src = `${drink.image_url}`;

    const cardTitle = document.createElement('h5');
    cardTitle.classList.add('card-title');
    cardTitle.textContent = `${drink.drink_name}`;

    const cardText = document.createElement('p');
    cardText.textContent = drink.description;

    const cardPrice = document.createElement('p');
    cardPrice.textContent = `Price: $${drink.price}`;

    const cardType = document.createElement('p');
    cardType.textContent = `Type: ${drink.drink_type}`;

    const cardIngredients = document.createElement('p');
    cardIngredients.textContent = `Ingredients: ${drink.ingredients}`;

    card.appendChild(cardImg);
    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(cardPrice);
    cardBody.appendChild(cardType);
    cardBody.appendChild(cardIngredients);
    card.appendChild(cardBody);

    return card;
  }
});