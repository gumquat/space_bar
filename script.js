document.addEventListener('DOMContentLoaded', function() {
  const cardContainer = document.querySelector('.card-container');
  const allDrinksButton = document.querySelector('#all-drinks-button');
  const beerButton = document.querySelector('#beer-button');
  const wineButton = document.querySelector('#wine-button');
  const whiskeyButton = document.querySelector('#whiskey-button');
  const cocktailButton = document.querySelector('#cocktail-button');
  const budgetButton = document.querySelector('#budget-button');

  let urlPath = 'drinks';

  function createCard(drink) {
    const card = document.createElement('div');
    card.classList.add('card', 'mb-3', 'col-12', 'col-md-6', 'col-lg-4');

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

    return card;
  }

  function fetchDrinks(path) {
    fetch(`http://localhost:5000/${path}`)
      .then(response => response.json())
      .then(drinks => {
        cardContainer.innerHTML = '';
        drinks.forEach(drink => {
          const card = createCard(drink);
          cardContainer.appendChild(card);
        });
      })
      .catch(error => {
        console.error('Error fetching drinks:', error);
      });
  }

  allDrinksButton.addEventListener('click', () => {
    urlPath = 'drinks';
    fetchDrinks(urlPath);
  });

  beerButton.addEventListener('click', () => {
    urlPath = 'beer';
    fetchDrinks(urlPath);
  });

  wineButton.addEventListener('click', () => {
    urlPath = 'wine';
    fetchDrinks(urlPath);
  });

  whiskeyButton.addEventListener('click', () => {
    urlPath = 'whiskey';
    fetchDrinks(urlPath);
  });

  cocktailButton.addEventListener('click', () => {
    urlPath = 'cocktail';
    fetchDrinks(urlPath);
  });

  budgetButton.addEventListener('click', () => {
    urlPath = 'budget';
    fetchDrinks(urlPath);
  });

  fetchDrinks(urlPath);
});