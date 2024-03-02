var animationFrameID;
localStorage.setItem('gamesFlag', 'true');
startGame();
async function startGame(){

  async function gameOver(){
	 // event.preventDefault()
	let headers = {
	  "X-Requested-With": "XMLHttpRequest",
	  "Content-Type": "application/json"
	}
	const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
	headers['X-CSRFToken'] = csrf

	let response = await fetch("pong", {

	  method:"POST",
	  headers: headers,
	  body:JSON.stringify({
		match_winner: winner,
		match_loser: loser,
		winner_score: winner_score,
		loser_score: loser_score
	  })                 
	});
	// let response_data = await response.json();
	// if (response_data.success){
	//   alert("Game Over. " + winner + " Wins!\n" + loser + "Score: " + loser_score + "\n" + winner +" Score: " + winner_score);
	// }
	// else{
	//   alert("Something went wrong");
	// }
  }

  const leftButton = document.getElementById('leftButton');
  const rightButton = document.getElementById('rightButton');
  const upButton = document.getElementById('upButton');
  const downButton = document.getElementById('downButton');

  function startMovingLeft() {
	leftPaddle.dy = -paddleSpeed;
  }

  function startMovingRight() {
	leftPaddle.dy = paddleSpeed;
  }

  function startMovingUp() {
	rightPaddle.dy = -paddleSpeed;
  }

  function startMovingDown() {
	rightPaddle.dy = paddleSpeed;
  }

  function stopMoving() {
	leftPaddle.dy = 0;
	rightPaddle.dy = 0;
  }

  leftButton.addEventListener('mousedown', startMovingLeft);
  leftButton.addEventListener('touchstart', startMovingLeft);

  rightButton.addEventListener('mousedown', startMovingRight);
  rightButton.addEventListener('touchstart', startMovingRight);

  upButton.addEventListener('mousedown', startMovingUp);
  upButton.addEventListener('touchstart', startMovingUp);

  downButton.addEventListener('mousedown', startMovingDown);
  downButton.addEventListener('touchstart', startMovingDown);

  // Button release events for both click and touch
  document.addEventListener('mouseup', stopMoving);
  document.addEventListener('touchend', stopMoving);


  // Retrieve customization options

  const paddleSpeedInput = document.getElementById('paddleSpeed');
  const ballSpeedInput = document.getElementById('ballSpeed');

  // Apply customization options
  paddleSpeedInput.addEventListener('input', function () {
	paddleSpeed = parseInt(paddleSpeedInput.value);
  });

  ballSpeedInput.addEventListener('input', function () {
	ballSpeed = parseInt(ballSpeedInput.value);
  });

  ballSpeedInput.addEventListener('input', function () {
	  ballSpeed = parseInt(ballSpeedInput.value);
	  ball.dx = (ball.dx > 0) ? ballSpeed : -ballSpeed;
	  ball.dy = (ball.dy > 0) ? ballSpeed : -ballSpeed;
	});

  // Button release events

const canvas = document.getElementById("game");
const context = canvas.getContext("2d");
const grid = 15;
const paddleHeight = grid * 5; // 80
//Retrieving user names
var leftplayer = "{{game.player_2}}";
var rightplayer = "{{game.player_1}}";


// Setting the maximum distance the paddles can move downwards
const LeftmaxPaddleY = canvas.height - grid - paddleHeight ;
const RightmaxPaddleY = canvas.height - grid - paddleHeight;


var paddleSpeed = 6;
var ballSpeed = 4;

// Score
var rp_count = 0;
var lp_count = 0;
// Activate secret level
var secret = false;
// Number of bounces in secret mode
var secret_count = 0;
ballColor = "purple";

// Describe the left paddle
const leftPaddle = {
  // Position it in the center
  x: grid * 2,
  y: canvas.height / 2 - paddleHeight / 2,
  width: grid,
  height: paddleHeight,
  // The paddle doesn't move anywhere at the start
  dy: 0,
};
// Describe the right paddle
const rightPaddle = {
  // Position it in the center on the right side
  x: canvas.width - grid * 3,
  y: canvas.height / 2 - paddleHeight / 2,
  width: grid,
  height: paddleHeight,
  // The right paddle doesn't move anywhere initially
  dy: 0,
};
// Describe the ball
const ball = {
  // It appears in the center of the field
  x: canvas.width / 2,
  y: canvas.height / 2,
  // Square, the size of a grid cell
  width: grid,
  height: grid,
  radius:( grid / 2) + 1,
  // The ball is not scored at the start, so remove the flag indicating that the ball needs to be reintroduced
  resetting: false,
  // Serve the ball to the top right corner
  dx: ballSpeed,
  dy: -ballSpeed,
};
// Check whether two objects with known coordinates intersect or not
// More details here: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
function collides(obj1, obj2) {
  return (
	obj1.x < obj2.x + obj2.width &&
	obj1.x + obj1.width > obj2.x &&
	obj1.y < obj2.y + obj2.height &&
	obj1.y + obj1.height > obj2.y
  );
}

function boundary_check(paddle, top, bottom) {
  if (paddle.y < top) {
	paddle.y = top;
  } else if (paddle.y > bottom) {
	paddle.y = bottom;
  }

}
// Main game loop
function loop() {
  // Clear the game field
  
  if (rp_count == 11 || lp_count == 11) {
	  cancelAnimationFrame(animationFrameID);
	  if(rp_count == 11){            
		winner = rightplayer;
		loser = leftplayer;
		winner_score = rp_count;
		loser_score = lp_count;
	  }
	  else{
		winner = leftplayer;
		loser = rightplayer;
		winner_score = lp_count;
		loser_score = rp_count;
	  }
	  gameOver();           
	  alert("Game Over. " + winner + " Wins!\n" + loser + " Scores: " + loser_score + "\n" +  winner +" Scores: " + winner_score);
	  localStorage.setItem('gamesFlag', 'false');
	}
  else
	animationFrameID = requestAnimationFrame(loop);
  context.clearRect(0, 0, canvas.width, canvas.height);
  // If the paddles were moving somewhere on the previous step, let them continue moving
  leftPaddle.y += leftPaddle.dy;
  rightPaddle.y += rightPaddle.dy;

  // check paddles stay witin the boundary
  boundary_check(leftPaddle, grid, LeftmaxPaddleY);
  boundary_check(rightPaddle, grid, RightmaxPaddleY);

  
  // Draw the paddles
  context.fillStyle = "blue";
  // Each paddle is a rectangle
  context.fillRect(
	leftPaddle.x,
	leftPaddle.y,
	leftPaddle.width,
	leftPaddle.height
  );
  context.fillRect(
	rightPaddle.x,
	rightPaddle.y,
	rightPaddle.width,
	rightPaddle.height
  );
	// If the ball was moving somewhere on the previous step, let it continue moving
  ball.x += ball.dx;
  ball.y += ball.dy;

  //check for wall hits
  if (ball.y < grid) {
	ball.y = grid;
	ball.dy *= -1;
  }
  else if (ball.y + grid > canvas.height - grid) {
	ball.y = canvas.height - grid * 2;
	ball.dy *= -1;
  }

  // If the ball flew off the game field to the left or right, restart it
  if ((ball.x < 0 || ball.x > canvas.width) && !ball.resetting) {
	// Mark that the ball is restarted to avoid looping
	ball.resetting = true;
	if (ball.x < 0) {
	  // If the ball flew off to the left, the right player scores
	  rp_count += 1;
	}
	else {
	  // If the ball flew off to the right, the left player scores
	  lp_count += 1;
	}   
   
	// Give a second for players to prepare
	setTimeout(() => {
	  // Ball is in play again
	  ball.resetting = false;
	  // Launch it again from the center
	  ball.x = canvas.width / 2;
	  ball.y = canvas.height / 2;
	}, 1000);
  }
  // If the ball touches the left paddle,
  if (collides(ball, leftPaddle)) {
	// send it in the opposite direction
	ball.dx *= -1;
	// Increase the ball's coordinates by the paddle's width to prevent a new bounce from being counted
	ball.x = leftPaddle.x + leftPaddle.width;
  }
  // Check and do the same for the right paddle
  else if (collides(ball, rightPaddle)) {
	ball.dx *= -1;
	ball.x = rightPaddle.x - rightPaddle.width;
	// Count the bounces
  //   count += 1;
	// If it reaches 5, activate the secret level
	if (rp_count >= 5 || lp_count >= 5) {
	  secret = true;
	}
	// Here is the secret level itself
	if (secret) {
	  // Increase new bounces
	  secret_count += 1;
	  // If this number is divisible by 3 without a remainder...
	  if (secret_count % 3 == 0) {
		// Increase the ball speed by one
		ball.dx = (ball.dx > 0) ? ballSpeed : -ballSpeed;
		ball.dy = (ball.dy > 0) ? ballSpeed : -ballSpeed;
		// Color the ball randomly
		ballColor =
		  "#" +
		  (Math.random().toString(16) + "000000")
			.substring(2, 8)
			.toUpperCase();
	  }
	}
  }
  // Draw the ball in the appropriate color
  context.fillStyle = ballColor;
  context.beginPath();
  context.arc(ball.x, ball.y, ball.radius, 0, 2 * Math.PI);
  context.fill();
  // Draw the walls
  context.fillStyle = "white";
  context.fillRect(0, 0, canvas.width, grid);
  context.fillRect(0, canvas.height - grid, canvas.width, canvas.height);
  // Draw the grid in the middle
  for (let i = grid; i < canvas.height - grid; i += grid * 2) {
	context.fillRect(canvas.width / 2 - grid / 2, i, grid, grid);
  }
  // Monitor key presses
  document.addEventListener("keydown", function (e) {
	// If the up arrow key is pressed,
	switch (e.which) {
	  case 87: // W key move the left paddle up
		leftPaddle.dy = -paddleSpeed;
		break;
	  case 83: // S key move the left paddle down
		leftPaddle.dy = paddleSpeed;
		break;
	  case 38: // up arrow move the right paddle up
	   rightPaddle.dy = -paddleSpeed;
		break;
	  case 40: // down arrow move the right paddle down
		rightPaddle.dy = paddleSpeed;
		break;
	}
  });

  // Now, watch for when someone releases a key to stop the paddle's movement
  document.addEventListener("keyup", function (e) {
	// If it's the up or down arrow key,
	if (e.which === 38 || e.which === 40) {
	  // stop the right paddle
	  rightPaddle.dy = 0;
	}
	if (e.which === 87 || e.which === 83) {
	  // stop the left paddle
	  leftPaddle.dy = 0;
	}
  });
  // Text color
  context.fillStyle = "#ff0000";
  // Set size and font
  context.font = "20pt Courier";
  // Display left player score
  context.fillText( leftplayer + ": " + lp_count, 50, 650);
  // Display right player score
  context.fillText(rightplayer + " : " + rp_count, 700, 650);

  //context.fillText( "{{user.login}}  : " + rp_count, 700, 650);
}
// Start the game
animationFrameID = requestAnimationFrame(loop);
};

const leftButton = document.getElementById('leftButton');
const rightButton = document.getElementById('rightButton');
const upButton = document.getElementById('upButton');
const downButton = document.getElementById('downButton');

leftButton.addEventListener('click', function(){
  leftPaddle.dy = -paddleSpeed;
});

rightButton.addEventListener('click', function(){
  leftPaddle.dy = paddleSpeed;
});

upButton.addEventListener('click', function(){
  rightPaddle.dy = -paddleSpeed;
});

downButton.addEventListener('click', function(){
  rightPaddle.dy = paddleSpeed;
});

window.addEventListener('beforeunload', function() {
  localStorage.setItem('gamesFlag', 'false');
});

window.addEventListener("popstate", function () {
	localStorage.setItem('gamesFlag', 'false');
});