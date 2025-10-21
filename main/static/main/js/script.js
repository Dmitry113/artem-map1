// Простой тест JavaScript для проверки подключения
document.addEventListener("DOMContentLoaded", () => {
    console.log("Frontend script loaded successfully ✅");

    // Пример безопасного клика по карте
    const map = document.getElementById("map");
    if (map) {
        map.addEventListener("click", () => {
            console.log("Карта кликнута — всё работает 👍");
        });
    }
});
