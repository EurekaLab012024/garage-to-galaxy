const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth * 0.9;
canvas.height = window.innerHeight * 0.6;

// Placeholder animation (orange circle)
let x = 50;
let y = canvas.height / 2;
let dx = 2;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#FFA500";
    ctx.beginPath();
    ctx.arc(x, y, 30, 0, Math.PI * 2);
    ctx.fill();
    x += dx;
    if (x > canvas.width || x < 0) dx *= -1;
    requestAnimationFrame(draw);
}

draw();
