const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight * 0.8;

ctx.fillStyle = "#fff";
ctx.font = "36px sans-serif";
ctx.fillText("Garage to Galaxy: Coming Soon!", 50, 100);
