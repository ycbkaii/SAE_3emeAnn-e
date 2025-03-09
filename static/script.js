//Partie Yoannnnnnnnnnnnnnnnnnnn

let id_user = 5;

async function fetchBooks(path, idSection, label) {
  try {
      const response = await fetch("http://127.0.0.1:8000/"+path); 
      const books = await response.json();
      console.log(books); 
     for (let index = 0; index < books.length; index++) {
          const element = books[index];
          let url_image = element[4];
          
          if(label == "Genre que vous pourriez aimer : "){
            label = label+books[0][2];
          }


          addCarouselItem(idSection, "/book?book_id="+element[5], url_image, element[0], label);
      }
      
  } catch (error) {
      console.error("Erreur lors de la récupération des livres :", error);
  }
}

function addCarouselItem(containerSelector, href, src, alt, label="") {
  const container = document.querySelector(`${containerSelector} .carousel--list`);
  titre = document.querySelector(`${containerSelector}`).getElementsByClassName("category--title")[0];
  titre.innerHTML = label;
  if (!container) return;
  
  const listItem = document.createElement('li');
  listItem.classList.add('carousel--item');
  
  const link = document.createElement('a');
  link.href = href;
  
  const image = document.createElement('img');
  image.src = src;
  image.alt = alt;
  
  link.appendChild(image);
  listItem.appendChild(link);
  container.appendChild(listItem);
}

// Exemple d'utilisation :
//fetchBooks("livres/acp_recom/"+id_user, "#section\\ 1", "Livres recommandés");


fetchBooks("livres/acm_recom/"+id_user, "#section\\ 2", "Livres que vous pourriez aimer");

fetchBooks("livres/genres/"+id_user, "#section\\ 3", "Genre que vous pourriez aimer : ");



//Fin partie modifiée

//NAVIGATION SHADOW
window.addEventListener('scroll', function() {
  const nav = document.querySelector('nav');
  if (window.scrollY > 0) { // Verifica se houve scroll
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
});


//SCROLLING CAROUSEL
// Select all carousel containers
const carouselContainers = document.querySelectorAll('.category--carousel');

//Apply function to each container
carouselContainers.forEach(container => {
const carousel = container.querySelector('.carousel--list');
const prevButton = container.querySelector('.carousel-button.prev');
const nextButton = container.querySelector('.carousel-button.next');
const carouselItems = carousel.querySelectorAll('.carousel--item');

// Calculate scroll amount based on the first item's width and margin
const firstItem = carouselItems[0];
const scrollAmount = firstItem.offsetWidth + parseInt(getComputedStyle(firstItem).marginRight);

// Event listeners for each carousel
prevButton.addEventListener('click', () => {
  carousel.scrollBy({
    left: -scrollAmount,
    behavior: 'smooth'
  });
});

nextButton.addEventListener('click', () => {
  carousel.scrollBy({
    left: scrollAmount,
    behavior: 'smooth'
  });
});
});