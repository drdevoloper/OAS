document.addEventListener('DOMContentLoaded', function () {
    let currentIndex = 0;
    const carousel = document.querySelector('.carousel');
    const totalImages = document.querySelectorAll('.carousel-image').length;
  
    function showSlide(index) {
      const newTransform = -index * 100 + '%';
      carousel.style.transform = `translateX(${newTransform})`;
    }
  
    window.nextSlide = function () {
      currentIndex = (currentIndex + 1) % totalImages;
      showSlide(currentIndex);
    }
  
    window.prevSlide = function () {
      currentIndex = (currentIndex - 1 + totalImages) % totalImages;
      showSlide(currentIndex);
    }
  
    setInterval(() => {
      window.nextSlide();
    }, 5000);
  });

  /* add */

  document.querySelector("form").addEventListener("submit", function (e) {
    alert("Vehicle submitted successfully!");
  });

  const vehicleType = document.getElementById('vehicleType');
  const vehicleBrand = document.getElementById('vehicleBrand');
  
  const brandOptions = {
    cycle: ["Hero", "BSA", "Firefox", "Montra", "Hercules"],
    bike: ["Hero", "Honda", "Bajaj", "Yamaha", "Suzuki", "KTM", "Royal Enfield", "TVS", "Ducati", "Harley-Davidson", "BMW", "Kawasaki", "Aprilia", "Benelli", "Triumph"],
    car: ["Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Honda", "Toyota", "Kia", "Skoda", "Volkswagen", "BMW", "Mercedes-Benz", "Audi"],
    van: ["Tata", "Mahindra", "Force Motors", "Maruti Suzuki", "Toyota"],
    bus: ["Tata Motors", "Ashok Leyland", "Eicher", "Volvo", "BharatBenz"]
  };
  
  vehicleType.addEventListener('change', function () {
    const selectedType = this.value;
    const brands = brandOptions[selectedType] || [];
  
    vehicleBrand.innerHTML = `<option value="" disabled selected>Select a Brand</option>`;
    brands.forEach(brand => {
      const option = document.createElement('option');
      option.value = brand.toLowerCase().replace(/\s+/g, '');
      option.textContent = brand;
      vehicleBrand.appendChild(option);
    });
  });
  
  