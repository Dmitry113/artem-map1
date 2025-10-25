document.addEventListener('DOMContentLoaded', () => {
  const map = L.map('map', {
    center: [55.751244, 37.618423],
    zoom: 10
  });

  // Подложка карты
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Сайдбар
  const sidebar = L.control.sidebar('sidebar', { position: 'right' }).addTo(map);

  // Пульсирующая иконка
  const pulseIcon = L.icon.pulse({
    iconSize: [12, 12],
    color: 'red',
    heartbeat: 2.5
  });

  // Vue-приложение для сайдбара
  const app = new Vue({
    el: '#sidebar-app',
    template: '#app-template',
    data: {
      selectedPlace: null,
      mainPhotoSrc: null,
      carouselImgs: [],
      promptVisible: true,
      loading: false
    },
    methods: {
      handlePhotosClick(direction) {
        const carouselEl = $('#place-photos');
        if (!carouselEl.length) return;

        if (direction === 'next' || direction === 'prev') {
          carouselEl.carousel(direction);
        } else {
          carouselEl.carousel(direction);
        }
      },
      setPlaceData(place) {
        const base = window.location.origin;
        const fixUrl = url => (url && !url.startsWith('http') ? `${base}${url}` : url);

        const gallery = Array.isArray(place.images)
          ? place.images.filter(Boolean).map(fixUrl)
          : [];

        const main = fixUrl(place.main_image);

        // 🔧 Объединяем главную и галерею
        const allImgs = [main, ...gallery].filter(Boolean);

        this.mainPhotoSrc = main || (allImgs.length ? allImgs[0] : null);
        this.selectedPlace = {
          title: place.title,
          short_description: place.short_description || '',
          long_description: place.long_description || ''
        };
        this.carouselImgs = allImgs;

        this.promptVisible = false;
        this.loading = false;

        // 🧠 Даем Vue отрисовать, затем активируем Bootstrap-слайдер
        this.$nextTick(() => {
          const carouselEl = $('#place-photos');
          if (carouselEl.length) {
            carouselEl.carousel({ interval: 5000 });
          }
        });
      }
    }
  });

  // Загрузка GeoJSON
  fetch('/places.geojson')
    .then(r => r.json())
    .then(data => {
      const markers = L.geoJSON(data, {
        pointToLayer: (feature, latlng) => {
          const marker = L.marker(latlng, { icon: pulseIcon });
          marker.bindTooltip(feature.properties.title || '');

          marker.on('click', () => {
            sidebar.show();
            app.loading = true;

            fetch(feature.properties.detailsUrl)
              .then(r => {
                if (!r.ok) throw new Error('Не удалось загрузить данные места');
                return r.json();
              })
              .then(placeData => {
                app.setPlaceData(placeData);
              })
              .catch(err => {
                console.error('Ошибка загрузки места:', err);
                app.loading = false;
              });
          });

          return marker;
        }
      }).addTo(map);

      // Центрирование карты
      if (markers.getLayers().length) {
        map.fitBounds(markers.getBounds().pad(0.15));
      }
    })
    .catch(err => console.error('Ошибка загрузки places.geojson:', err));
});
