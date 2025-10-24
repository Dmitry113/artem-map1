// === Создаем карту ===
const map = L.map('map', {
  center: [55.753676, 37.64],
  zoom: 12
});

// === Добавляем слой карты ===
L.tileLayer.provider('OpenStreetMap.Mapnik').addTo(map);

// === Добавляем боковую панель ===
const sidebar = L.control.sidebar('sidebar', {
  autopan: true,
  closeButton: true,
  position: 'right'
}).addTo(map);

// === Пульсирующая иконка ===
const pulsingIcon = L.icon.pulse({
  iconSize: [12, 12],
  color: 'red',
  fillColor: 'red',
  heartbeat: 2.5
});

// === Читаем GeoJSON ===
const geojsonElement = document.getElementById('places-geojson');
let placesGeoJSON = null;

try {
  placesGeoJSON = JSON.parse(geojsonElement.textContent);
} catch (e) {
  console.error('Ошибка чтения GeoJSON:', e);
}

// === Добавляем метки ===
if (placesGeoJSON) {
  L.geoJSON(placesGeoJSON, {
    pointToLayer: (feature, latlng) => {
      const marker = L.marker(latlng, { icon: pulsingIcon });
      marker.bindTooltip(feature.properties.title);

      marker.on('click', async () => {
        try {
          const response = await fetch(feature.properties.detailsUrl);
          if (!response.ok) throw new Error('Ошибка загрузки данных о месте');
          const data = await response.json();

          // Отображаем данные в боковой панели
          sidebar.setContent(`
            <div class="sidebar-content">
              <h3>${data.title}</h3>
              ${data.imgs && data.imgs.length
                ? `<img src="${data.imgs[0]}" class="img-fluid rounded mb-3" alt="${data.title}">`
                : ''
              }
              <p>${data.description_short || ''}</p>
              ${data.imgs && data.imgs.length > 1
                ? `
                <div id="carouselPlacePhotos" class="carousel slide mb-3" data-ride="carousel" data-interval="5000">
                  <div class="carousel-inner">
                    ${data.imgs.map((img, i) => `
                      <div class="carousel-item ${i === 0 ? 'active' : ''}">
                        <img src="${img}" class="d-block w-100 rounded" alt="${data.title}">
                      </div>
                    `).join('')}
                  </div>
                  <a class="carousel-control-prev" href="#carouselPlacePhotos" role="button" data-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                  </a>
                  <a class="carousel-control-next" href="#carouselPlacePhotos" role="button" data-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                  </a>
                </div>` : ''
              }
            </div>
          `);

          // Инициализация карусели после вставки
          setTimeout(() => {
            const carouselEl = document.getElementById('carouselPlacePhotos');
            if (carouselEl) {
              // Запускаем Bootstrap-карусель вручную
              $(carouselEl).carousel();

              // Разрешаем клики по стрелкам внутри боковой панели
              const prev = carouselEl.querySelector('.carousel-control-prev');
              const next = carouselEl.querySelector('.carousel-control-next');
              if (prev && next) {
                L.DomEvent.disableClickPropagation(prev);
                L.DomEvent.disableClickPropagation(next);
                prev.addEventListener('click', (e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  $(carouselEl).carousel('prev');
                });
                next.addEventListener('click', (e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  $(carouselEl).carousel('next');
                });
              }
            }
          }, 200);

          sidebar.show();
        } catch (err) {
          console.error('Ошибка при загрузке места:', err);
        }
      });

      return marker;
    }
  }).addTo(map);
}

// === Кнопка отладки ===
L.control.custom({
  position: 'bottomleft',
  content: `
    <div class="debug-btn" title="Отладка">
      <img src="/static/main/img/debug-option.png" alt="Отладка">
    </div>
  `,
  style: { margin: '10px', cursor: 'pointer' },
  events: {
    click: function () {
      console.log('🧭 Отладка:');
      console.log('Центр карты:', map.getCenter());
      console.log('Масштаб:', map.getZoom());
      alert('Открой консоль (F12), чтобы увидеть данные о карте.');
    }
  }
}).addTo(map);
