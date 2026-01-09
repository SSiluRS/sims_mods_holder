export function initSparkles(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Адаптация под размер header
    const resizeCanvas = () => {
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // === Мелкие блестки (80 шт) ===
    const sparkles = [];
    const count = 500;

    for (let i = 0; i < count; i++) {
        sparkles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            baseRadius: Math.random() * 0.3 + 0.1, // 0.5–1.5px
            pulseSpeed: Math.random() * 4 + 3, // 0.5–1.3 Гц
            phase: Math.random() * Math.PI * 2,
        });
    }

    // === Анимация ===
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const t = Date.now() / 1000;

        // Рисуем мелкие блестки
        for (const s of sparkles) {
            const pulse = Math.sin(t * s.pulseSpeed + s.phase) * 0.5 + 0.5; // 0 → 1
            const radius = s.baseRadius * (1 + pulse * 0.8);
            const opacity = 0.3 + pulse * 0.7;

            ctx.beginPath();
            ctx.arc(s.x, s.y, radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
            ctx.fill();

            // Фиолетовое свечение
            ctx.shadowBlur = 10 * pulse;
            ctx.shadowColor = `rgba(139, 92, 246, ${pulse * 0.6})`;
            ctx.fill();
            ctx.shadowBlur = 0;
        }

        requestAnimationFrame(animate);
    }

    animate();
}