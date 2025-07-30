window.onload = function () {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // Resize canvas
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight * 0.8;

  // Background color (optional)
  ctx.fillStyle = "#001F3F"; // dark blue
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Test content
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "36px sans-serif";
  ctx.fillText("🚀 Garage to Galaxy: Coming Soon!", 50, 100);

  // Add test visual (like a wheel)
  ctx.beginPath();
  ctx.arc(canvas.width / 2, canvas.height / 2, 40, 0, Math.PI * 2);
  ctx.fillStyle = "orange";
  ctx.fill();
};
